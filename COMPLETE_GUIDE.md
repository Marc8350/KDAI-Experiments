# CodeIE Orchestrator - Complete Robustness & Diagnostics Guide

## What Was Improved

### 1. ✅ **Sample Count Verification**
- Validates 210,840 expected samples (56 runs × 3,765 per run)
- Progress bar shows accurate total
- Estimates based on actual dataset size, not just config

### 2. ✅ **Ollama Server Monitoring**
- Preflight health check before execution
- Periodic health checks every 10 completed runs
- Logs warnings if server becomes unresponsive
- Auto-detection prevents silent failures

### 3. ✅ **Inference Timeout Protection**
- 120-second timeout on all inference calls
- Prevents single stuck request from blocking entire pipeline
- Gracefully degrades to empty result + log warning
- Customizable timeout via parameter

### 4. ✅ **Process Pool Safety**
- 2-hour timeout per worker future
- 30-second timeout on result retrieval
- Prevents indefinite waiting on stuck workers
- Logs timeout errors with context

### 5. ✅ **Checkpoint & Resume**
- Auto-detects incomplete batches
- Filters already-completed runs
- Continues from exact stopping point
- Results merged into same batch directory

### 6. ✅ **Empty Results Detection**
- Treats `None` results as failures
- Prevents silent completion of crashed runs
- Proper error logging and reporting

### 7. ✅ **Comprehensive Diagnostics**
- Documents 8 likely root causes
- Provides testing strategy
- Includes monitoring commands
- Clear troubleshooting guide

### 8. ✅ **Automation Scripts**
- `run_experiments.sh` - Full pipeline automation
- Git sync, Ollama setup, screen session, resume logic
- Status checking, dry-run preview
- Detailed usage documentation

---

## Root Cause Analysis: Why It Stalled

### Most Probable: **Ollama Server Crash/Hang**
**Evidence:**
- Process stopped cleanly (no crash)
- Mid-execution stall (120/3765 samples)
- No Python exceptions logged
- Multiple runs showed no completion

**How New Code Detects It:**
```python
# Every 10 runs:
if not self._check_ollama_health(base_url):
    logger.warning("ALERT: Ollama health check failed after N runs")
```

### Secondary: **Inference Timeout**
**Evidence:**
- LangChain `invoke()` has no built-in timeout
- Single slow request could block worker
- Both workers (max_workers=2) could hang simultaneously

**How New Code Detects It:**
```python
# 120-second timeout on inference
signal.alarm(120)
response = llm_model.invoke(...)  # Raises TimeoutError if hung
```

### Tertiary: **Process Pool Deadlock**
**Evidence:**
- Progress queue communication between processes
- If both workers hang, nothing completes
- Main thread waits on `as_completed()` forever

**How New Code Detects It:**
```python
# Timeout on waiting for futures
for future in as_completed(future_to_run, timeout=7200):
    result_data = future.result(timeout=30)
```

---

## How to Test on Remote

### Immediate Test (No Changes Needed)
```bash
cd /path/to/KDAI-Experiments

# 1. Verify setup
./run_experiments.sh --status

# 2. Dry run to see experiment matrix
./run_experiments.sh --dry-run

# 3. Start full pipeline (in background)
./run_experiments.sh
# Press Ctrl+A then D to detach

# 4. Monitor progress
tail -f run_experiments.log
./run_experiments.sh --status
```

### Advanced Test (To Verify Diagnostics)
```bash
# Terminal 1: Start experiments
./run_experiments.sh
# Let it run for ~30-50 samples

# Terminal 2: Kill Ollama to trigger health check
pkill -f ollama

# Watch Terminal 1: Should see "ALERT: Ollama health check failed" 
# (or in logs within ~100 samples, every 10 completed)

# Terminal 2: Restart Ollama
ollama serve

# Terminal 1: Should pause briefly then resume
# (or fail gracefully with timeout)
```

---

## Files Modified/Created

| File | Changes |
|------|---------|
| `CodeIE/orchestrator.py` | Added health checks, timeouts, resume logic |
| `CodeIE/run_codeie_experiments.py` | Added timeout to inference |
| `run_experiments.sh` | New automation script |
| `RUN_EXPERIMENTS.md` | Usage guide |
| `RUN_SCRIPT_SETUP.md` | Setup instructions |
| `DIAGNOSIS_RUN_STALL.md` | Root cause analysis |
| `ROBUSTNESS_IMPROVEMENTS.md` | Technical summary |

---

## Key Code Additions

### Timeout on Inference
```python
def run_inference(prompt: str, llm_model, config, timeout: int = 120):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)
    try:
        response = llm_model.invoke(messages, stop=stop)
    except TimeoutError:
        logging.error(f"Inference timeout after {timeout}s")
        return ""
    finally:
        signal.alarm(0)
```

### Health Check During Execution
```python
if completed_count % 10 == 0:
    for model in enabled_models:
        if model.type == "ollama":
            if not self._check_ollama_health(model.base_url):
                logger.warning("ALERT: Ollama unresponsive")
```

### Checkpoint Resume
```python
incomplete = self.find_incomplete_batch()
if incomplete:
    runs = self.filter_completed_runs(runs, completed_run_ids)
    logger.info(f"Resuming: {len(runs)} runs remaining")
```

### Process Pool Timeout
```python
for future in as_completed(future_to_run, timeout=7200):
    result_data = future.result(timeout=30)
```

---

## Expected Behavior After Improvements

### Scenario 1: Normal Execution
```
✓ Preflight checks pass
✓ All 56 runs submitted to process pool
✓ Progress bar shows 210,840 samples
✓ Every 10 runs: Health check runs quietly
✓ Results files appear incrementally
✓ All samples processed successfully
```

### Scenario 2: Ollama Crashes Mid-Run
```
✓ Progress bar advancing normally
✓ Run 25 completes (sample 95,000/210,840)
✓ Health check (run 30) detects Ollama down
✗ Logs "ALERT: Ollama health check failed after 300 completed runs"
✗ Worker 1 times out on next inference (120s)
✗ Worker 2 times out on next inference (120s)
✗ Batch incomplete with 300 samples processed
✓ Restarting script auto-resumes from checkpoint
```

### Scenario 3: Single Slow Request
```
✓ Worker A processing samples normally
✗ Worker B hits slow model response
✗ No timeout, Worker B blocks
✓ But only affects Worker B, Worker A continues
✓ After 120s timeout, Worker B recovers
✓ Execution continues with both workers
```

---

## Monitoring Commands for Remote

```bash
# Watch Ollama status
watch -n 2 'ollama list'

# Watch log in real-time
tail -f run_experiments.log

# Check batch progress
watch 'cat CODEIE-results/batch_*/batch_summary.json | jq .completed_runs'

# Count result files
watch 'ls CODEIE-results/batch_*/*.json | wc -l'

# Monitor system resources
watch -n 5 'free -h && echo "---" && top -bn1 | head -15'

# Check screen session
screen -ls

# Attach to running session
screen -r codeie-experiments
```

---

## Checklist for Remote Testing

- [ ] Clone/pull latest code
- [ ] Verify `run_experiments.sh` is executable (`chmod +x`)
- [ ] Verify Ollama is installed and runnable (`ollama --version`)
- [ ] Start Ollama in background: `ollama serve &`
- [ ] Test script: `./run_experiments.sh --dry-run`
- [ ] Review experiment matrix output
- [ ] Start full run: `./run_experiments.sh`
- [ ] Detach from screen: `Ctrl+A` then `D`
- [ ] Let run for ~100 samples
- [ ] Reattach: `./run_experiments.sh --screen-attach`
- [ ] Check logs for health check messages
- [ ] Let run to completion or until confident

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Sample count accuracy | 210,840 shown in progress bar |
| Ollama detection | Health check every 10 runs in logs |
| Timeout protection | No hangs >2min without log message |
| Resume capability | Script can restart and continue from batch |
| Result files | Incrementally appear in batch directory |
| Batch summary | Tracks completed_runs count accurately |

---

## Support Resources

- **Quick Setup:** `RUN_SCRIPT_SETUP.md`
- **Usage Guide:** `RUN_EXPERIMENTS.md`
- **Troubleshooting:** `DIAGNOSIS_RUN_STALL.md`
- **Technical Details:** `ROBUSTNESS_IMPROVEMENTS.md`

---

## Summary

✅ **Orchestrator is now robust against:**
- Ollama server crashes
- Inference timeouts
- Process pool deadlocks
- Empty results
- Execution interruptions

✅ **Users can:**
- Monitor health via periodic checks
- Recover from failures via checkpoints
- See realistic progress
- Diagnose issues with comprehensive logs

**Ready for remote testing** 🚀
