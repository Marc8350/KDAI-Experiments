#!/bin/bash
# =============================================================================
# CodeIE Server Experiment Runner
# =============================================================================
# Automated script for running CodeIE experiments on the A100 server.
# Designed to be run inside a screen session for long-running experiments.
#
# Usage:
#   screen -S codeie
#   ./CodeIE/run_server_experiments.sh
#   # Press Ctrl+A, D to detach
#   # screen -r codeie to reattach
#
# Configuration:
#   - Edit the variables below to match your server setup
#   - Expected runtime: ~10-24 hours for full dataset (210K samples)
# =============================================================================

set -e  # Exit on error (will be handled gracefully in the main loop)

# =============================================================================
# CONFIGURATION - EDIT THESE FOR YOUR SERVER
# =============================================================================
PROJECT_DIR="/home/ann/fiz-ddb/notebook/KDAI-Experiments-CodeIE"  # <-- CHANGE THIS to your server path
BRANCH_NAME="feature/codeie-integration"                 # <-- CHANGE THIS to your branch name
CONDA_ENV_NAME="CodeIE"                           # <-- CHANGE THIS to your conda env name
GPU_COUNT=2                                      # Number of A100 GPUs
OLLAMA_URL="http://localhost:11434"              # Ollama server URL

# Expected experiment counts (based on config)
# 2 granularities × 2 styles × 7 variations (base + 6) × 1 model = 28 runs
# But with 2 models enabled: 2 × 2 × 7 × 2 = 56 runs
# Adjust based on your experiment_config.yaml
EXPECTED_RUNS=28                                 # <-- Adjust based on enabled models
EXPECTED_SAMPLES=3765                            # <-- Match your max_samples in config

# Retry settings
MAX_RETRIES=3
RETRY_DELAY=60  # seconds

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1" >&2
}

check_ollama() {
    log "Checking Ollama server at $OLLAMA_URL..."
    if curl -s "$OLLAMA_URL/api/tags" > /dev/null 2>&1; then
        log "✅ Ollama server is running"
        return 0
    else
        error "Ollama server not responding at $OLLAMA_URL"
        return 1
    fi
}

start_ollama() {
    log "Attempting to start Ollama server..."
    
    # Set optimal parallel settings for dual A100
    export OLLAMA_NUM_PARALLEL=6
    export OLLAMA_MAX_LOADED_MODELS=2
    
    # Start Ollama in background
    nohup ollama serve > /tmp/ollama_server.log 2>&1 &
    
    # Wait for server to be ready
    for i in {1..30}; do
        sleep 2
        if check_ollama; then
            return 0
        fi
        log "Waiting for Ollama to start... ($i/30)"
    done
    
    error "Failed to start Ollama server"
    return 1
}

validate_results() {
    local results_dir="$1"
    local batch_dir=$(ls -td "$results_dir"/batch_* 2>/dev/null | head -1)
    
    if [ -z "$batch_dir" ]; then
        log "No batch directory found"
        return 1
    fi
    
    log "Validating results in: $batch_dir"
    
    # Check batch_summary.json
    local summary_file="$batch_dir/batch_summary.json"
    if [ ! -f "$summary_file" ]; then
        error "batch_summary.json not found"
        return 1
    fi
    
    # Parse summary to check completion
    local total_runs=$(python3 -c "import json; d=json.load(open('$summary_file')); print(d.get('total_runs', 0))")
    local completed_runs=$(python3 -c "import json; d=json.load(open('$summary_file')); print(d.get('completed_runs', 0))")
    
    log "Runs: $completed_runs / $total_runs completed"
    
    if [ "$completed_runs" -lt "$total_runs" ]; then
        error "Not all runs completed: $completed_runs / $total_runs"
        return 1
    fi
    
    # Count result files (excluding batch_summary.json)
    local file_count=$(find "$batch_dir" -name "*.json" -not -name "batch_summary.json" | wc -l | tr -d ' ')
    log "Result files found: $file_count"
    
    if [ "$file_count" -lt "$EXPECTED_RUNS" ]; then
        error "Expected $EXPECTED_RUNS result files, found $file_count"
        return 1
    fi
    
    # Validate sample counts in each result file
    log "Validating sample counts in result files..."
    local incomplete_files=0
    
    for result_file in "$batch_dir"/*.json; do
        if [[ "$(basename "$result_file")" == "batch_summary.json" ]]; then
            continue
        fi
        
        local processed=$(python3 -c "import json; d=json.load(open('$result_file')); print(d.get('processed_count', 0))" 2>/dev/null || echo "0")
        
        if [ "$processed" -lt "$EXPECTED_SAMPLES" ]; then
            error "File $(basename "$result_file") has only $processed samples (expected $EXPECTED_SAMPLES)"
            incomplete_files=$((incomplete_files + 1))
        fi
    done
    
    if [ "$incomplete_files" -gt 0 ]; then
        error "$incomplete_files files have incomplete sample counts"
        return 1
    fi
    
    # Check experiment_matrix.csv
    local matrix_file="$results_dir/experiment_matrix.csv"
    if [ ! -f "$matrix_file" ]; then
        log "Warning: experiment_matrix.csv not found (may be created after completion)"
    else
        local matrix_rows=$(wc -l < "$matrix_file" | tr -d ' ')
        log "Experiment matrix has $((matrix_rows - 1)) entries (excluding header)"
    fi
    
    log "✅ All validations passed!"
    return 0
}

# =============================================================================
# MAIN SCRIPT
# =============================================================================

log "=========================================="
log "CodeIE Server Experiment Runner"
log "=========================================="

# Step 1: Navigate to project directory
log "Step 1: Navigating to project directory..."
if [ ! -d "$PROJECT_DIR" ]; then
    error "Project directory not found: $PROJECT_DIR"
    error "Please update PROJECT_DIR in this script"
    exit 1
fi

cd "$PROJECT_DIR"
log "Working directory: $(pwd)"

# Step 2: Activate conda environment
log "Step 2: Activating conda environment..."

# Try to locate conda.sh in common locations
CONDA_SH=""
for CANDIDATE in \
    "$HOME/anaconda3/etc/profile.d/conda.sh" \
    "$HOME/miniconda3/etc/profile.d/conda.sh" \
    "/opt/conda/etc/profile.d/conda.sh" \
    "/usr/local/anaconda3/etc/profile.d/conda.sh" \
    "/usr/local/miniconda3/etc/profile.d/conda.sh"; do
    if [ -f "$CANDIDATE" ]; then
        CONDA_SH="$CANDIDATE"
        break
    fi
done

if [ -n "$CONDA_SH" ]; then
    source "$CONDA_SH"
else
    if command -v conda >/dev/null 2>&1; then
        eval "$(conda shell.bash hook)"
    else
        error "Conda not found. Please install Anaconda/Miniconda or update CONDA_SH path."
        exit 1
    fi
fi

if [ -n "$CONDA_ENV_NAME" ]; then
    conda activate "$CONDA_ENV_NAME"
    log "✅ Activated conda env: $CONDA_ENV_NAME"
    log "   Python: $(which python)"
else
    error "CONDA_ENV_NAME is not set. Please set it in the CONFIGURATION section."
    exit 1
fi

# Step 3: Check and switch to correct branch
log "Step 3: Checking git branch..."
current_branch=$(git branch --show-current)
log "Current branch: $current_branch"

if [ "$current_branch" != "$BRANCH_NAME" ]; then
    log "Switching to branch: $BRANCH_NAME"
    git checkout "$BRANCH_NAME" || {
        error "Failed to switch to branch $BRANCH_NAME"
        exit 1
    }
fi
log "✅ On correct branch: $BRANCH_NAME"

# Step 4: Git pull latest changes
log "Step 4: Pulling latest changes..."
git pull origin "$BRANCH_NAME" || {
    error "Git pull failed"
    exit 1
}
log "✅ Repository updated"

# Step 5: Clean results directory (with backup)
log "Step 5: Cleaning results directory..."
RESULTS_DIR="$PROJECT_DIR/CodeIE/CODEIE-results"

if [ -d "$RESULTS_DIR" ]; then
    # Create backup of existing results
    BACKUP_DIR="$RESULTS_DIR.backup_$(date +%Y%m%d_%H%M%S)"
    log "Backing up existing results to: $BACKUP_DIR"
    mv "$RESULTS_DIR" "$BACKUP_DIR"
fi

mkdir -p "$RESULTS_DIR"
log "✅ Clean results directory created: $RESULTS_DIR"

# Step 6: Check/Start Ollama server
log "Step 6: Checking Ollama server..."
if ! check_ollama; then
    log "Ollama not running, attempting to start..."
    if ! start_ollama; then
        error "Failed to start Ollama server. Please start it manually:"
        error "  OLLAMA_NUM_PARALLEL=6 ollama serve"
        exit 1
    fi
fi

# Step 7: Run experiments with retry logic
log "Step 7: Running experiments..."
log "   GPU Count: $GPU_COUNT"
log "   Expected runs: $EXPECTED_RUNS"
log "   Expected samples per run: $EXPECTED_SAMPLES"

retry_count=0
success=false

while [ $retry_count -lt $MAX_RETRIES ] && [ "$success" = false ]; do
    retry_count=$((retry_count + 1))
    log ""
    log "=========================================="
    log "Experiment Attempt $retry_count / $MAX_RETRIES"
    log "=========================================="
    
    # Check if orchestrator thinks it's already complete (from previous run)
    # This prevents infinite retries if validation is misconfigured
    latest_batch=$(ls -td "$RESULTS_DIR"/batch_* 2>/dev/null | head -1)
    if [ -n "$latest_batch" ] && [ -f "$latest_batch/batch_summary.json" ]; then
        prev_total=$(python3 -c "import json; d=json.load(open('$latest_batch/batch_summary.json')); print(d.get('total_runs', 0))" 2>/dev/null || echo "0")
        prev_completed=$(python3 -c "import json; d=json.load(open('$latest_batch/batch_summary.json')); print(d.get('completed_runs', 0))" 2>/dev/null || echo "0")
        
        if [ "$prev_completed" -eq "$prev_total" ] && [ "$prev_total" -gt 0 ]; then
            log "WARNING: Orchestrator reports all $prev_total runs completed."
            log "         If validation still fails, check EXPECTED_RUNS ($EXPECTED_RUNS) and EXPECTED_SAMPLES ($EXPECTED_SAMPLES) settings."
            
            # If this is retry 2+, likely a config mismatch - don't retry indefinitely
            if [ $retry_count -gt 1 ]; then
                log "Multiple retries with orchestrator reporting completion - likely validation config mismatch."
                log "Exiting to prevent unnecessary retries. Please check validation settings."
                break
            fi
        fi
    fi
    
    # Run the orchestrator
    python CodeIE/orchestrator.py \
        --gpu-count "$GPU_COUNT" \
        --skip-generation \
        2>&1 | tee -a "$RESULTS_DIR/orchestrator_run_$retry_count.log"
    
    orchestrator_exit_code=${PIPESTATUS[0]}
    
    # FAIL-FAST: If orchestrator crashed with error, don't retry
    # Error codes: 1 = general error, but RuntimeError from fail-fast will also be 1
    # Check log for FATAL messages to distinguish
    if [ $orchestrator_exit_code -ne 0 ]; then
        error "Orchestrator exited with code $orchestrator_exit_code"
        
        # Check if this was a fail-fast crash (FATAL in log)
        if grep -q "FATAL:" "$RESULTS_DIR/orchestrator_run_$retry_count.log" 2>/dev/null; then
            error "FAIL-FAST triggered: Persistent errors detected. NOT retrying."
            error "Check the log for details: $RESULTS_DIR/orchestrator_run_$retry_count.log"
            
            # Show the fatal error
            grep "FATAL:" "$RESULTS_DIR/orchestrator_run_$retry_count.log" | tail -1
            
            # Exit immediately - don't waste time retrying
            exit 1
        fi
    fi
    
    # Validate results
    log ""
    log "Validating results..."
    if validate_results "$RESULTS_DIR"; then
        success=true
        log "✅ Experiments completed successfully!"
    else
        if [ $retry_count -lt $MAX_RETRIES ]; then
            log "Retrying in $RETRY_DELAY seconds..."
            log "The orchestrator will resume from checkpoint automatically."
            sleep $RETRY_DELAY
        fi
    fi
done

# Step 8: Final summary
log ""
log "=========================================="
log "FINAL SUMMARY"
log "=========================================="

if [ "$success" = true ]; then
    log "✅ All experiments completed successfully!"
    log ""
    log "Results location: $RESULTS_DIR"
    log ""
    
    # Show final statistics
    latest_batch=$(ls -td "$RESULTS_DIR"/batch_* 2>/dev/null | head -1)
    if [ -n "$latest_batch" ]; then
        log "Latest batch: $(basename "$latest_batch")"
        
        file_count=$(find "$latest_batch" -name "*.json" -not -name "batch_summary.json" | wc -l | tr -d ' ')
        log "Total result files: $file_count"
        
        if [ -f "$RESULTS_DIR/experiment_matrix.csv" ]; then
            matrix_rows=$(wc -l < "$RESULTS_DIR/experiment_matrix.csv" | tr -d ' ')
            log "Experiment matrix entries: $((matrix_rows - 1))"
        fi
    fi
    
    log ""
    log "You can now analyze the results!"
    exit 0
else
    error "Experiments failed after $MAX_RETRIES attempts"
    error ""
    error "Please check:"
    error "  1. Ollama server logs: /tmp/ollama_server.log"
    error "  2. Orchestrator logs: $RESULTS_DIR/orchestrator_run_*.log"
    error "  3. Batch summary: $RESULTS_DIR/batch_*/batch_summary.json"
    error ""
    error "To retry manually:"
    error "  cd $PROJECT_DIR"
    error "  source $VENV_NAME/bin/activate"
    error "  python CodeIE/orchestrator.py --gpu-count $GPU_COUNT"
    exit 1
fi
