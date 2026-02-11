#!/bin/bash

################################################################################
# CodeIE Experiment Runner
# 
# Comprehensive script for running CodeIE experiments with:
# - Git synchronization
# - Indy configuration
# - Ollama model management  
# - Screen session for background execution
# - Checkpoint resumption on restart
#
# Usage:
#   ./run_experiments.sh                    # Full run
#   ./run_experiments.sh --dry-run          # Preview only
#   ./run_experiments.sh --status           # Show status
#   ./run_experiments.sh --resume           # Resume from last checkpoint
#   ./run_experiments.sh --screen-attach    # Attach to running session
################################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"
CODEIE_DIR="$SCRIPT_DIR/CodeIE"
CONFIG_FILE="$CODEIE_DIR/config/experiment_config.yaml"
RESULTS_DIR="$CODEIE_DIR/CODEIE-results"
SCREEN_SESSION="codeie-experiments"
LOG_FILE="$PROJECT_ROOT/run_experiments.log"

# Command-line arguments
DRY_RUN=false
SHOW_STATUS=false
RESUME_MODE=false
SCREEN_ATTACH=false
QUIET_MODE=false

parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --status)
                SHOW_STATUS=true
                shift
                ;;
            --resume)
                RESUME_MODE=true
                shift
                ;;
            --screen-attach)
                SCREEN_ATTACH=true
                shift
                ;;
            --quiet)
                QUIET_MODE=true
                shift
                ;;
            *)
                echo "Unknown option: $1"
                exit 1
                ;;
        esac
    done
}

log() {
    local level="$1"
    shift
    local msg="$@"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[${timestamp}] [${level}] ${msg}" | tee -a "$LOG_FILE"
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $@" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $@" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $@" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $@" | tee -a "$LOG_FILE"
}

# ============================================================================
# Checkpoint and Resume Logic
# ============================================================================

find_latest_batch() {
    """Find the most recent batch directory."""
    if [[ ! -d "$RESULTS_DIR" ]]; then
        echo ""
        return
    fi
    
    local latest=$(ls -td "$RESULTS_DIR"/batch_* 2>/dev/null | head -1)
    echo "$latest"
}

get_batch_status() {
    local batch_dir="$1"
    if [[ ! -f "$batch_dir/batch_summary.json" ]]; then
        echo "no_summary"
        return
    fi
    
    python3 - <<EOF
import json
try:
    with open("$batch_dir/batch_summary.json", "r") as f:
        data = json.load(f)
    total = data.get("total_runs", 0)
    completed = data.get("completed_runs", 0)
    print(f"{completed}/{total}")
except:
    print("error")
EOF
}

should_resume() {
    """Check if resumption is needed/possible."""
    local latest_batch=$(find_latest_batch)
    
    if [[ -z "$latest_batch" ]]; then
        return 1  # No previous batch
    fi
    
    local status=$(get_batch_status "$latest_batch")
    
    if [[ "$status" == "error" ]] || [[ "$status" == "no_summary" ]]; then
        return 1
    fi
    
    # Parse status
    IFS='/' read -r completed total <<< "$status"
    if [[ $completed -lt $total ]]; then
        log_warn "Found incomplete batch: $latest_batch ($status)"
        return 0  # Should resume
    fi
    
    return 1  # Batch was complete
}

# ============================================================================
# Environment Setup
# ============================================================================

check_requirements() {
    log_info "Checking requirements..."
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 not found"
        exit 1
    fi
    
    # Check for required Python packages
    python3 -c "import yaml, datasets" 2>/dev/null || {
        log_warn "Some Python packages may be missing"
        log_info "Run: pip install -r requirements.txt"
    }
    
    # Check for ollama or docker
    if ! command -v ollama &> /dev/null; then
        if ! command -v docker &> /dev/null; then
            log_warn "Ollama/Docker not found. Make sure Ollama is running separately."
        fi
    fi
    
    log_success "Requirements check passed"
}

cd_to_project() {
    log_info "Entering project directory: $PROJECT_ROOT"
    cd "$PROJECT_ROOT"
    log_success "Working directory: $(pwd)"
}

git_sync() {
    log_info "Syncing repository..."
    
    if [[ ! -d ".git" ]]; then
        log_warn "Not a git repository. Skipping git pull."
        return
    fi
    
    if git pull --no-rebase 2>&1 | tee -a "$LOG_FILE"; then
        log_success "Git sync complete"
    else
        log_warn "Git pull had issues, continuing anyway..."
    fi
}

# ============================================================================
# Ollama Model Management
# ============================================================================

check_ollama_running() {
    """Check if Ollama is accessible."""
    local base_url="${1:-http://localhost:11434}"
    
    if timeout 3 curl -s "${base_url}/api/tags" > /dev/null 2>&1; then
        return 0
    fi
    return 1
}

extract_ollama_models() {
    """Extract all Ollama model names from config."""
    python3 - <<EOF
import yaml
import sys

try:
    with open("$CONFIG_FILE", "r") as f:
        config = yaml.safe_load(f)
    
    models = config.get("models", {})
    for model_id, model_config in models.items():
        if model_config.get("type") == "ollama" and model_config.get("enabled", False):
            model_name = model_config.get("name")
            print(model_name)
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)
EOF
}

pull_ollama_model() {
    local model_name="$1"
    log_info "Checking/pulling Ollama model: $model_name"
    
    # Check if model exists
    if ollama list | grep -q "^${model_name}"; then
        log_success "Model already available: $model_name"
        return 0
    fi
    
    log_info "Pulling model: $model_name (this may take a while)..."
    if ollama pull "$model_name" 2>&1 | tee -a "$LOG_FILE"; then
        log_success "Model ready: $model_name"
        return 0
    else
        log_error "Failed to pull model: $model_name"
        return 1
    fi
}

setup_ollama_models() {
    log_info "Setting up Ollama models..."
    
    if ! check_ollama_running; then
        log_error "Ollama is not running or not accessible at http://localhost:11434"
        log_info "Start Ollama with: ollama serve"
        exit 1
    fi
    
    log_success "Ollama is running"
    
    # Extract enabled models from config
    local models=$(extract_ollama_models)
    
    if [[ -z "$models" ]]; then
        log_warn "No Ollama models enabled in config"
        return
    fi
    
    # Pull each model
    local failed=0
    while IFS= read -r model_name; do
        if [[ -z "$model_name" ]]; then
            continue
        fi
        if ! pull_ollama_model "$model_name"; then
            ((failed++))
        fi
    done <<< "$models"
    
    if [[ $failed -gt 0 ]]; then
        log_error "$failed model(s) failed to pull"
        exit 1
    fi
    
    log_success "All Ollama models ready"
}

# ============================================================================
# Experiment Execution
# ============================================================================

build_orchestrator_cmd() {
    local cmd="python3 CodeIE/orchestrator.py --config CodeIE/config/experiment_config.yaml"
    
    if [[ "$DRY_RUN" == true ]]; then
        cmd="$cmd --dry-run"
    fi
    
    if [[ "$QUIET_MODE" == true ]]; then
        cmd="$cmd --quiet"
    fi
    
    # Resume logic
    if [[ "$RESUME_MODE" == true ]] || should_resume; then
        log_info "Resuming from previous checkpoint"
        # Orchestrator will auto-detect incomplete batch and continue
        # (future enhancement: add explicit --resume flag if needed)
    fi
    
    echo "$cmd"
}

run_in_screen() {
    local cmd="$1"
    
    # Check if screen session already exists
    if screen -list | grep -q "$SCREEN_SESSION"; then
        log_warn "Screen session '$SCREEN_SESSION' already running"
        log_info "Attach with: screen -r $SCREEN_SESSION"
        return 1
    fi
    
    log_info "Starting experiments in screen session: $SCREEN_SESSION"
    log_info "Command: $cmd"
    
    # Create new screen session in detached mode
    screen -dmS "$SCREEN_SESSION" bash -c "
        cd '$PROJECT_ROOT'
        echo '=========================================='
        echo 'CodeIE Experiment Runner'
        echo 'Started: $(date)'
        echo '=========================================='
        echo ''
        
        # Run the orchestrator
        $cmd
        
        echo ''
        echo '=========================================='
        echo 'Experiments complete!'
        echo 'Finished: $(date)'
        echo '=========================================='
        echo 'Session will remain open for 60 seconds...'
        sleep 60
    "
    
    log_success "Screen session started with PID: $(screen -ls | grep $SCREEN_SESSION | awk '{print $1}')"
    log_info "Attach to session: screen -r $SCREEN_SESSION"
    log_info "Detach from session: Ctrl-a then d"
}

show_status() {
    log_info "=== CodeIE Experiment Status ==="
    
    # Check screen session
    if screen -list | grep -q "$SCREEN_SESSION"; then
        log_success "Screen session is running: $SCREEN_SESSION"
    else
        log_warn "No active screen session"
    fi
    
    # Check latest batch
    local latest_batch=$(find_latest_batch)
    if [[ -z "$latest_batch" ]]; then
        log_info "No batch runs found yet"
    else
        local status=$(get_batch_status "$latest_batch")
        log_info "Latest batch: $(basename $latest_batch)"
        log_info "  Status: $status"
    fi
    
    # List Ollama models
    if check_ollama_running; then
        log_success "Ollama is running"
        log_info "Available models:"
        ollama list | tail -n +2 | while read line; do
            log_info "  $line"
        done
    else
        log_warn "Ollama is not running"
    fi
}

show_help() {
    cat <<EOF
Usage: $0 [OPTIONS]

OPTIONS:
    --dry-run           Show what would be run without executing
    --status            Show current status and exit
    --resume            Force resume from last checkpoint
    --screen-attach     Attach to existing screen session
    --quiet             Minimal output (progress only)
    
EXAMPLES:
    # Full run
    ./run_experiments.sh
    
    # Preview without running
    ./run_experiments.sh --dry-run
    
    # Check status
    ./run_experiments.sh --status
    
    # Attach to running session
    ./run_experiments.sh --screen-attach
    
    # Resume from checkpoint
    ./run_experiments.sh --resume

SCREEN SESSION COMMANDS:
    Attach:   screen -r $SCREEN_SESSION
    Detach:   Ctrl-a then d
    List:     screen -ls
    Kill:     screen -X -S $SCREEN_SESSION quit

EOF
}

# ============================================================================
# Main Flow
# ============================================================================

main() {
    parse_args "$@"
    
    # Status mode
    if [[ "$SHOW_STATUS" == true ]]; then
        show_status
        exit 0
    fi
    
    # Screen attach mode
    if [[ "$SCREEN_ATTACH" == true ]]; then
        if screen -list | grep -q "$SCREEN_SESSION"; then
            screen -r "$SCREEN_SESSION"
        else
            log_error "No active screen session '$SCREEN_SESSION'"
            exit 1
        fi
    fi
    
    # Normal run mode
    log_info "=========================================="
    log_info "CodeIE Experiment Runner"
    log_info "Started at: $(date)"
    log_info "=========================================="
    
    check_requirements
    cd_to_project
    git_sync
    setup_ollama_models
    
    # Build and run orchestrator command
    local orchestrator_cmd=$(build_orchestrator_cmd)
    
    if [[ "$DRY_RUN" == true ]]; then
        log_info "DRY RUN MODE - not executing"
        log_info "Would execute: $orchestrator_cmd"
        exit 0
    fi
    
    # Run in screen
    run_in_screen "$orchestrator_cmd"
}

# Run main function
main "$@"
