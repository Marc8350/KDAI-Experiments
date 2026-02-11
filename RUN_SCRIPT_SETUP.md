# CodeIE Experiment Runner Setup

## Overview
The `run_experiments.sh` script automates the complete pipeline for running CodeIE experiments with checkpoint resumption.

## Features
- **Git Sync**: Pulls latest changes before running
- **Indy Configuration**: Sets up Indy environment if available
- **Ollama Model Management**: Automatically loads enabled models from config
- **Background Execution**: Runs in a `screen` session so you can close your terminal
- **Checkpoint Resumption**: Automatically detects and resumes incomplete batches

## Quick Start

### Initial Setup
```bash
cd /path/to/KDAI-Experiments
chmod +x run_experiments.sh
```

### Run Full Pipeline
```bash
./run_experiments.sh
```

### Run in Background & Detach
```bash
./run_experiments.sh
# Press Ctrl+A then D to detach from screen (process continues)
```

### Reattach to Running Session
```bash
./run_experiments.sh --screen-attach
# Or manually:
screen -r codeie-experiments
```

### Preview Without Running
```bash
./run_experiments.sh --dry-run
```

### Check Status
```bash
./run_experiments.sh --status
```

## How Resumption Works

1. **Checkpoint Detection**: Script looks for incomplete batch directories in `CODEIE-results/`
2. **Batch Summary**: Reads `batch_summary.json` to find completed vs. total runs
3. **Auto-Resume**: If incomplete runs exist, orchestrator filters them out and continues
4. **Progress Tracking**: New runs are added to the same batch summary

### Example Resume Scenario
```
Batch 1: 56 total runs, only 20 completed → Session dies
↓
Run script again → Automatically detects batch 1 is incomplete
↓
Resumes with 36 remaining runs, saves to same batch directory
```

## Configuration

Edit `CodeIE/config/experiment_config.yaml`:

```yaml
models:
  qwen2.5:
    enabled: true      # Will be loaded by Ollama
    type: "ollama"
    name: "qwen2.5:7b"
    base_url: "http://localhost:11434"
    temperature: 0.0
    max_tokens: 512

execution:
  max_samples: 3765    # Samples per run
  resume: true         # Automatic resumption (handled by script)
```

## Sample Count Verification

With current config:
- **Enabled Models**: 2 (qwen2.5, qwen2.5-coder)
- **Granularities**: 2 (coarse, fine)
- **Styles**: 2 (pl, nl)
- **Variations**: 7 (base + 6 paraphrases/back-translations)
- **Total Runs**: 2 × 2 × 2 × 7 = **56 runs**
- **Samples per Run**: 3,765 (capped by dataset)
- **Total Expected Samples**: 56 × 3,765 = **~210,840 samples**

Progress bar will show: "Total Progress (Samples): 210840"

## Troubleshooting

### Script Hangs
- Ollama may be unresponsive. Check: `ollama list`
- View warnings in script output for unreachable endpoints

### Incomplete Results
- Check screen session: `screen -r codeie-experiments`
- View logs: `tail -f run_experiments.log`
- Batch info: `cat CODEIE-results/batch_*/batch_summary.json | jq`

### Resume Not Working
- Ensure `batch_summary.json` exists in latest batch directory
- Check permissions on results directory

## File Locations

| File/Dir | Purpose |
|----------|---------|
| `run_experiments.sh` | Main runner script |
| `CodeIE/orchestrator.py` | Experiment orchestrator |
| `CodeIE/config/experiment_config.yaml` | Configuration |
| `CodeIE/CODEIE-results/batch_*` | Results & checkpoints |
| `run_experiments.log` | Execution log |

## Next Steps (Remote Testing)

1. Transfer `run_experiments.sh` and `orchestrator.py` to remote
2. Verify Ollama is running: `ollama list`
3. Run: `./run_experiments.sh --dry-run` to preview
4. Run: `./run_experiments.sh` to start full pipeline
5. Detach: `Ctrl+A` then `D`
6. Reattach: `./run_experiments.sh --screen-attach`

---

**Last Updated**: 2026-02-11
