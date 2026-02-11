# Diagnosis: Why Run Stalled at 120/3765 Samples

## Key Observations
- ✅ Orchestrator started successfully (2 models × 4 base prompts × 7 variations = 56 runs planned)
- ✅ One run completed: `coarse_pl_v0_original_qwen2.5:7b_20260210_195146.json` (120 samples)
- ⚠️ Only 5 result files found, many runs missing
- ❌ Process stopped cleanly (no error log, no exception)
- ❌ Progress halted mid-execution

## Likely Causes (Ranked by Probability)

### 1. **Ollama Server Crashed or Became Unresponsive** (HIGHEST)
**Evidence:**
- Process didn't crash—it just stopped
- No Python exceptions logged
- Worker processes don't have visibility into Ollama failures unless they call it
- Ollama can crash silently or become unresponsive to requests

**Indicators to Check:**
```bash
# On remote: check if Ollama is still running
ps aux | grep ollama
ollama list   # Will timeout if server is down
# Check system logs for OOM or crashes
dmesg | tail -20
```

**How to Detect:** 
- `run_inference()` returns empty string on exception (`except Exception: return ""`)
- Empty generation → parsing fails → results still saved
- But if Ollama is completely unresponsive, requests hang indefinitely with no timeout

---

### 2. **Inference Timeout (Ollama Hung)**
**Evidence:**
- `run_inference()` calls `llm_model.invoke()` with no timeout
- LangChain ChatOllama has no built-in timeout
- If model hangs, the worker thread just waits forever
- Main process may think worker is still working

**Code Gap:**
```python
# run_codeie_experiments.py line 503-515
def run_inference(prompt: str, llm_model, config: ExperimentConfig) -> str:
    try:
        messages = [HumanMessage(content=prompt)]
        response = llm_model.invoke(messages, stop=stop)  # ← NO TIMEOUT HERE
        if hasattr(response, 'content'):
            return response.content
        return str(response)
    except Exception as e:
        logging.error(f"Inference failed: {e}")
        return ""
```

**Fix Needed:**
- Add timeout to inference calls
- Add timeout to worker processes

---

### 3. **Worker Process Silently Hangs**
**Evidence:**
- ProcessPoolExecutor with 2 workers
- If both workers hang, no new runs can start
- `as_completed()` only yields completed futures—incomplete futures wait forever

**Possible Triggers:**
- Prompt loading fails for certain variation
- Dataset access issue mid-run
- Queue deadlock (progress_queue.put() blocked)

---

### 4. **Progress Queue Deadlock**
**Evidence:**
- Main process reads from `progress_queue` in separate thread
- Worker puts `1` for each sample
- If queue fills up without being read, worker blocks

**Unlikely but Possible:**
```python
# orchestrator.py line 816-820
# Progress bar updater thread
def update_pbar(queue, total):
    with tqdm(...) as pbar:
        while True:
            item = queue.get()  # ← Could be blocked if daemon thread dies
            if item is None:
                break
            pbar.update(item)
```

---

### 5. **Variation Files Missing for Some Configurations**
**Evidence:**
- Only 5 results files out of 56 expected runs
- If prompt file not found, `_get_prompt_path()` returns None
- Run is skipped in matrix generation
- But then only ~5 runs would be in the matrix, not 56

**Less Likely** but would explain fewer runs.

---

### 6. **Enabled Model Not Actually Available**
**Evidence:**
- Config says models are enabled
- But `ollama list` might not show them
- First run (qwen2.5) completed
- Second model (qwen2.5-coder) might not have been pulled

**Check:**
```bash
ollama list | grep qwen
# Should show both qwen2.5:7b and qwen2.5-coder:7b
```

---

### 7. **Disk Space / File Handle Limits**
**Evidence:**
- Process stops cleanly without error
- OS resource limit hit
- Worker processes killed by OS

**Check:**
```bash
df -h  # Disk space
ulimit -n  # File descriptor limit
```

---

### 8. **Parent Process Killed / Screen Session Terminated**
**Evidence:**
- If run in screen and terminal closed unexpectedly
- Worker processes orphaned
- Batch results partial

---

## Recommended Diagnostics to Add

### Immediate Fixes for Production
Add these to `run_experiment()` in `run_codeie_experiments.py`:

```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Inference timed out after 60 seconds")

# Set timeout for inference
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(60)  # 60-second timeout

try:
    response = llm_model.invoke(messages, stop=stop)
finally:
    signal.alarm(0)  # Cancel alarm
```

### Monitoring Improvements

1. **Log inference attempts:**
```python
logging.info(f"Calling inference for sample {i}/{num_samples}")
# ... then after response
logging.info(f"Inference complete in {elapsed:.2f}s")
```

2. **Check Ollama health between runs:**
```python
if i % 10 == 0:
    check_ollama_health()  # Verify server is still responsive
```

3. **Process pool monitoring:**
```python
# In orchestrator.py before as_completed loop
for future in as_completed(future_to_run, timeout=3600):
    # 1-hour timeout per future
```

---

## Data to Collect When Testing Remotely

When run stalls next time, capture:

```bash
# 1. Check Ollama status
ollama list
curl -s http://localhost:11434/api/tags

# 2. Check system resources
free -h
ps aux | grep -E "ollama|python"
top -n 1

# 3. View batch summary
cat CODEIE-results/batch_*/batch_summary.json | jq

# 4. Count result files
ls -1 CODEIE-results/batch_*/*.json | wc -l

# 5. Check logs
tail -100 run_experiments.log
```

---

## Hypothesis Test Priority

1. **First:** Check if Ollama is still running (`ollama list`)
2. **Second:** Review logs for any inference errors
3. **Third:** Check system resources (disk, memory, file descriptors)
4. **Fourth:** Add timeouts and re-run with monitoring

---

## Prevention Strategy

Implement in `run_experiments.sh`:

```bash
# Monitor Ollama health in background
while true; do
    if ! ollama list > /dev/null 2>&1; then
        log_error "Ollama has stopped!"
        # Restart or alert
    fi
    sleep 60
done &
```

And in orchestrator:

```python
# Health check every N runs
if completed_count % 10 == 0:
    check_ollama_health()
    if not is_ollama_healthy():
        log_error("Ollama unresponsive, pausing...")
        wait_for_ollama()
```

---

## Most Likely Culprit

**Based on pattern (clean stop, mid-execution):** 
→ **Ollama server crash or hang** (60% confidence)
→ **Inference timeout with no recovery** (25% confidence)
→ **Process pool deadlock** (10% confidence)
→ **Other** (5% confidence)

Next run should use enhanced monitoring to confirm.
