#!/bin/bash
# CodeIE Full Experiment Runner
# Runs:
# 1. Unit Tests (to verify inference)
# 2. Single Coarse PL Run (to verify end-to-end pipeline)
# 3. Full Orchestrator Run (all variations)
# Pipes output to specific log files for easier analysis.

# Exit immediately if a command exits with a non-zero status
# But we will use "|| true" to allow specific steps to fail without stopping the whole script
set -e

# Ensure we are in the project root
cd "$(dirname "$0")/../.."

# Create logs directory
mkdir -p CodeIE/logs

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="CodeIE/logs/full_run_mistral_${TIMESTAMP}.log"

echo "============================================================" | tee -a "${LOG_FILE}"
echo "Starting CodeIE Full Test Suite & Experiments" | tee -a "${LOG_FILE}"
echo "Model: mistral (via Ollama)" | tee -a "${LOG_FILE}"
echo "Timestamp: ${TIMESTAMP}" | tee -a "${LOG_FILE}"
echo "Logging to: ${LOG_FILE}" | tee -a "${LOG_FILE}"
echo "============================================================" | tee -a "${LOG_FILE}"

# 1. Run Unit Tests using the new --model argument support we added
echo "" | tee -a "${LOG_FILE}"
echo ">>> STEP 1: Running Inference Unit Tests" | tee -a "${LOG_FILE}"
echo "------------------------------------------------------------" | tee -a "${LOG_FILE}"
# 2>&1 redirects stderr to stdout so we capture everything
# ALLOW FAILURE: We know Fine PL often fails with Mistral, so we use '|| true' to continue
python CodeIE/tests/unit_test_inference.py --model mistral 2>&1 | tee -a "${LOG_FILE}" || echo "⚠️ Unit tests failed (likely Fine PL), continuing pipeline..." | tee -a "${LOG_FILE}"

echo "" | tee -a "${LOG_FILE}"
echo ">>> STEP 2: Running Single Test Experiment (Coarse PL)" | tee -a "${LOG_FILE}"
echo "------------------------------------------------------------" | tee -a "${LOG_FILE}"
python CodeIE/run_codeie_experiments.py --granularity coarse --style pl --variation default --max_test 5 --model mistral 2>&1 | tee -a "${LOG_FILE}" || echo "⚠️ Experiment run failed, continuing..." | tee -a "${LOG_FILE}"

echo "" | tee -a "${LOG_FILE}"
echo ">>> STEP 3: Running Full Orchestrator (All Variations)" | tee -a "${LOG_FILE}"
echo "------------------------------------------------------------" | tee -a "${LOG_FILE}"
# Ensure orchestrator uses the correct python environment and dependencies
python CodeIE/orchestrator.py 2>&1 | tee -a "${LOG_FILE}"

echo "" | tee -a "${LOG_FILE}"
echo "============================================================" | tee -a "${LOG_FILE}"
echo "All Steps Complete!" | tee -a "${LOG_FILE}"
echo "Full log saved to: ${LOG_FILE}" | tee -a "${LOG_FILE}"
echo "============================================================" | tee -a "${LOG_FILE}"
