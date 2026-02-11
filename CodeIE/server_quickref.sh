#!/bin/bash
# =============================================================================
# Quick Server Commands Reference
# =============================================================================
# Copy-paste commands for running CodeIE experiments on the A100 server
# =============================================================================

cat << 'EOF'
========================================
CODEIE SERVER QUICK REFERENCE
========================================

1. CONNECT TO SERVER:
   ssh your_user@your_server

2. START A SCREEN SESSION:
   screen -S codeie

3. EDIT THE SCRIPT (first time only):
   nano CodeIE/run_server_experiments.sh
   # Change these lines:
   #   PROJECT_DIR="/home/your_user/KDAI-Experiments"
   #   BRANCH_NAME="codeie-experiments"

4. RUN EXPERIMENTS:
   ./CodeIE/run_server_experiments.sh

5. DETACH FROM SCREEN (keep running):
   Press: Ctrl+A, then D

6. REATTACH TO CHECK PROGRESS:
   screen -r codeie

7. CHECK OLLAMA STATUS:
   curl http://localhost:11434/api/tags

8. MONITOR GPU USAGE:
   watch -n 1 nvidia-smi

9. CHECK EXPERIMENT PROGRESS:
   tail -f CodeIE/CODEIE-results/orchestrator_run_*.log

10. LIST COMPLETED RESULTS:
    ls -la CodeIE/CODEIE-results/batch_*/

========================================
EXPECTED OUTPUT FILES (with 2 models):
========================================
- 2 granularities × 2 styles × 7 variations × 2 models = 56 result files
- Plus batch_summary.json = 57 files total per batch
- Plus experiment_matrix.csv in results root

With 1 model enabled:
- 2 × 2 × 7 × 1 = 28 result files + batch_summary = 29 files

========================================
TROUBLESHOOTING:
========================================
# If Ollama isn't running:
OLLAMA_NUM_PARALLEL=6 OLLAMA_MAX_LOADED_MODELS=2 ollama serve &

# If experiments stall:
# Check the batch_summary.json for failed runs
cat CodeIE/CODEIE-results/batch_*/batch_summary.json | jq '.completed_runs, .total_runs'

# Kill stuck processes:
pkill -f "ollama serve"
pkill -f "orchestrator.py"

# Restart from checkpoint (orchestrator auto-resumes):
python CodeIE/orchestrator.py --gpu-count 2

EOF
