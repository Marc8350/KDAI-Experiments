# CodeIE Experiment Runner

Complete automated script for running CodeIE NER experiments with checkpoint resumption.

## Quick Start

```bash
# From the project root directory
./run_experiments.sh
```

The script will:
1. ✅ Sync with git (pull latest changes)
2. ✅ Ensure Ollama is running
3. ✅ Pull required models from Ollama
4. ✅ Start experiments in a background screen session
5. ✅ Auto-resume from checkpoint if interrupted

## Usage

### Full Run (Background)
```bash
./run_experiments.sh
```
Starts experiments in a detached screen session. You can close your terminal and experiments continue.

### Preview (Dry Run)
```bash
./run_experiments.sh --dry-run
```
Shows the experiment matrix without executing anything.

### Check Status
```bash
./run_experiments.sh --status
```
Shows:
- Whether experiments are running
- Latest batch status
- Available Ollama models

### Resume from Checkpoint
```bash
./run_experiments.sh --resume
```
Explicitly resume from the last incomplete batch (usually auto-detected).

### Attach to Running Session
```bash
./run_experiments.sh --screen-attach
```
Connect to the background screen session to monitor progress.

### Minimal Output
```bash
./run_experiments.sh --quiet
```
Only shows critical info and progress bar.

## Screen Session Commands

Once experiments are running in the background:

### Attach to Session
```bash
screen -r codeie-experiments
```

### Detach from Session
Press `Ctrl-a` then `d`

### List All Sessions
```bash
screen -ls
```

### Kill Session
```bash
screen -X -S codeie-experiments quit
```

## How It Works

### 1. Prerequisites Check
- Python 3 with required packages
- Ollama or Docker available
- Git repository access

### 2. Git Sync
Pulls latest changes from the repository to ensure up-to-date code and configs.

### 3. Ollama Setup
- Checks if Ollama is running at `http://localhost:11434`
- Extracts enabled models from `CodeIE/config/experiment_config.yaml`
- Pulls each model if not already available (one-time, may take time)

### 4. Experiment Execution
- Runs the orchestrator in a screen session
- Full run with 2 models, 2 granularities, 2 styles, 7 variations = **56 experiment configurations**
- **~210,840 samples total** (3,765 per configuration × 56)
- Progress bar shows real sample count

### 5. Checkpoint & Resume
If execution is interrupted (e.g., Ollama crashes, terminal closes):
1. Latest batch summary is automatically detected
2. Completed run IDs are extracted
3. Only remaining runs are re-executed
4. Results are merged into the same batch directory

## Configuration

Edit `CodeIE/config/experiment_config.yaml` to:
- Enable/disable models
- Change max_samples per run
- Adjust granularities and styles
- Configure Ollama endpoints

Example: To use only 1 model and 10 samples for testing:
```yaml
models:
  qwen2.5:
    enabled: true
  qwen2.5-coder:
    enabled: false

execution:
  max_samples: 10
```

## Output

Results are saved in `CodeIE/CODEIE-results/batch_YYYYMMDD_HHMMSS/`:
- Individual run results: `{granularity}_{style}_{variation}_{model}_{timestamp}.json`
- Batch summary: `batch_summary.json` (tracks progress for resumption)

## Troubleshooting

### Ollama Not Found
```bash
# Start Ollama manually in another terminal
ollama serve
```

### Models Won't Pull
```bash
# Check Ollama status
ollama list

# Manually pull a model
ollama pull qwen2.5:7b
```

### Script Won't Execute
```bash
# Make script executable
chmod +x run_experiments.sh

# Run with bash explicitly
bash run_experiments.sh
```

### Resume Not Working
```bash
# Check latest batch
ls -la CodeIE/CODEIE-results/

# View batch summary
cat CodeIE/CODEIE-results/batch_*/batch_summary.json
```

### Connection Refused
If you see "Ollama endpoint unreachable", ensure:
1. Ollama is running (`ollama serve`)
2. It's accessible at `http://localhost:11434`
3. Check `experiment_config.yaml` for correct base_url

## Logs

Main execution logs are saved to:
```
run_experiments.log
```

View real-time logs while running:
```bash
tail -f run_experiments.log
```

Or check logs within the screen session:
```bash
screen -r codeie-experiments
```

## Monitoring Long Runs

For a ~210k sample run (2 models):

**Estimated duration:**
- Per sample: ~1-2 seconds (Ollama inference + parsing)
- Total: ~4-7 hours

**Monitor progress:**
```bash
# Attach to session
screen -r codeie-experiments

# Or check latest batch results
ls -ltrh CodeIE/CODEIE-results/batch_*/[a-z]*.json | tail -5
```

## Advanced

### Manual Orchestrator Execution
```bash
cd CodeIE
python3 orchestrator.py --help
```

### Override Models
```bash
python3 CodeIE/orchestrator.py --model qwen2.5 --granularity coarse
```

### Environment Variables
```bash
# Set API key if using Gemini
export GOOGLE_API_KEY="your-key"

# Set custom Ollama endpoint
export CUSTOM_API_BASE="http://ollama-server:11434"
```

## Tips

1. **Start Ollama first** - Pull models take time, do it once before running script
2. **Use screen** - Keeps experiments running even if you disconnect
3. **Check status regularly** - Monitor `--status` to ensure progress
4. **Review configs** - Always verify `experiment_config.yaml` before large runs
5. **Save space** - Results JSON files can be large; archive completed batches

---

For more info: `./run_experiments.sh --help`
