#!/bin/bash
# =============================================================================
# Local Testing Script for MacBook M1
# =============================================================================
# This script helps you test the orchestrator locally before running on A100s.
# Ollama works on Apple Silicon via Metal - no CUDA needed!

set -e

# Get script directory and project root
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=========================================="
echo "CodeIE Local Testing Setup (MacBook M1)"
echo "=========================================="
echo "Project root: $PROJECT_ROOT"

# Step 0: Activate virtual environment
VENV_PATH="$PROJECT_ROOT/.venv"
if [ -d "$VENV_PATH" ]; then
    echo "Activating virtual environment: $VENV_PATH"
    source "$VENV_PATH/bin/activate"
    echo "✅ Virtual environment activated"
    echo "   Python: $(which python)"
elif [ -d "$PROJECT_ROOT/venv" ]; then
    VENV_PATH="$PROJECT_ROOT/venv"
    echo "Activating virtual environment: $VENV_PATH"
    source "$VENV_PATH/bin/activate"
    echo "✅ Virtual environment activated"
    echo "   Python: $(which python)"
else
    echo "⚠️  No virtual environment found at .venv or venv"
    echo "   Using system Python: $(which python)"
    echo "   Consider creating a venv: python -m venv .venv"
fi

# Step 1: Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Installing..."
    echo "   Run: brew install ollama"
    echo "   Or download from: https://ollama.ai/download"
    exit 1
fi

echo "✅ Ollama found"

# Step 2: Start Ollama if not running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Starting Ollama server..."
    ollama serve &
    sleep 5
fi

echo "✅ Ollama server running"

# Step 3: Pull a small test model (3B is fast on M1)
TEST_MODEL="qwen2.5:3b"
echo "Pulling test model: $TEST_MODEL (this may take a few minutes first time)..."
ollama pull $TEST_MODEL

echo "✅ Model ready: $TEST_MODEL"

# Step 4: Create a minimal test config
cat > /tmp/test_config.yaml << 'EOF'
# Minimal test config for local M1 testing
dataset:
  granularities: ["coarse"]
  path: "few-nerd_test"

models:
  qwen_3b_test:
    name: "qwen2.5:3b"
    type: "ollama"
    enabled: true
    base_url: "http://localhost:11434"
    max_tokens: 256
    temperature: 0.0

prompts:
  styles: ["pl"]
  coarse_shots: 1
  fine_shots: 1
  variations:
    paraphrase: []
    back_translation: []

execution:
  max_samples: 5  # Only 5 samples for quick test!
  max_workers: 1  # Single worker for M1

output:
  results_dir: "CODEIE-results"
EOF

echo "✅ Test config created"

# Step 5: Run a minimal test
echo ""
echo "=========================================="
echo "Running minimal test (5 samples)..."
echo "=========================================="

cd "$PROJECT_ROOT"

python CodeIE/orchestrator.py \
    --config /tmp/test_config.yaml \
    --max-workers 1 \
    --gpu-count 1 \
    --skip-generation \
    --variation base

echo ""
echo "=========================================="
echo "✅ Test completed!"
echo "=========================================="

# Step 6: Cleanup - delete the test model to save disk space
echo ""
echo "Cleaning up: Removing test model $TEST_MODEL to save disk space..."
ollama rm $TEST_MODEL 2>/dev/null || true
echo "✅ Model removed"

# Also clean up the temp config
rm -f /tmp/test_config.yaml

echo ""
echo "If this worked, your setup is correct."
echo "For full runs on A100, use:"
echo "  python CodeIE/orchestrator.py --gpu-count 2"
