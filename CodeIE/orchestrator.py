#!/usr/bin/env python3
"""
CodeIE Experiment Orchestrator (One-Stop Shop)

Complete pipeline for running NER experiments:
1. Check and generate prompt variations if needed
2. Run experiments across all configurations
3. Display and save results

Variations per base prompt: 6 (3 paraphrase + 3 back-translation)
Total variations: 4 base prompts × 6 variations = 24

Usage:
    python orchestrator.py                              # Full run
    python orchestrator.py --dry-run                    # Preview without running
    python orchestrator.py --generate-only              # Only generate variations
    python orchestrator.py --granularity coarse         # Filter by granularity
"""

import os
import sys
import json
import yaml
import time
import logging
import argparse
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from itertools import product

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
CODEIE_ROOT = Path(__file__).parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(CODEIE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODEIE_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import asdict
from run_codeie_experiments import run_experiment, ExperimentConfig, update_experiment_matrix

# =============================================================================
# Ollama Configuration for Dual A100 Setup
# =============================================================================
# Optimal settings for 2x A100 GPUs:
# - OLLAMA_NUM_PARALLEL: Number of concurrent requests Ollama handles
#   With 2x A100 (80GB each), you can run 4-8 parallel requests for 7B models
# - OLLAMA_MAX_LOADED_MODELS: Can keep multiple model copies in VRAM
# - Workers in orchestrator should match OLLAMA_NUM_PARALLEL

OLLAMA_RESTART_MAX_ATTEMPTS = 3
OLLAMA_RESTART_WAIT_SECONDS = 10
OLLAMA_HEALTH_CHECK_INTERVAL = 50  # Check every N completed runs

# Model size to recommended parallel workers mapping
# Based on VRAM requirements (bfloat16) and dual A100 80GB setup
MODEL_SIZE_WORKERS = {
    "3b": 8,    # ~6GB per model, can run many
    "7b": 6,    # ~14GB per model
    "8b": 6,    # ~16GB per model  
    "13b": 4,   # ~26GB per model
    "14b": 4,   # ~28GB per model
    "30b": 2,   # ~60GB per model
    "32b": 2,   # ~64GB per model
    "34b": 2,   # ~68GB per model
    "70b": 1,   # ~140GB, needs both GPUs
    "72b": 1,   # ~144GB, needs both GPUs
}

DEFAULT_WORKERS_FALLBACK = 4  # Conservative default if model size unknown


def estimate_workers_for_model(model_name: str, gpu_count: int = 2) -> int:
    """
    Estimate optimal worker count based on model size.
    
    Args:
        model_name: Model name (e.g., "qwen2.5:7b", "llama3:70b")
        gpu_count: Number of GPUs available
        
    Returns:
        Recommended number of parallel workers
    """
    model_lower = model_name.lower()
    
    # Extract size from model name (looks for patterns like "7b", "70b", "3b")
    import re
    size_match = re.search(r'(\d+)b', model_lower)
    
    if size_match:
        size_str = size_match.group(1) + "b"
        if size_str in MODEL_SIZE_WORKERS:
            base_workers = MODEL_SIZE_WORKERS[size_str]
            # Scale by GPU count (base is for 2 GPUs)
            return max(1, int(base_workers * gpu_count / 2))
    
    # Check for known small models without explicit size
    small_models = ["phi3", "phi-3", "gemma:2b", "tinyllama"]
    if any(m in model_lower for m in small_models):
        return max(1, int(8 * gpu_count / 2))
    
    # Check for known large models
    large_models = ["mixtral", "command-r", "llama-3.1:405b"]
    if any(m in model_lower for m in large_models):
        return 1
    
    logger.warning(f"Could not determine size for model '{model_name}', using default {DEFAULT_WORKERS_FALLBACK} workers")
    return DEFAULT_WORKERS_FALLBACK


class OllamaManager:
    """
    Manages Ollama server lifecycle with auto-recovery capabilities.
    
    For dual A100 setup, this class helps:
    1. Start Ollama with optimal parallel settings
    2. Monitor health and restart on failures
    3. Pre-warm models to avoid first-request latency
    """
    
    def __init__(self, base_url: str = "http://localhost:11434", gpu_count: int = 2):
        self.base_url = base_url.rstrip("/")
        self.gpu_count = gpu_count
        self.restart_count = 0
        self.last_health_check = time.time()
        
    def check_health(self, timeout: int = 10) -> bool:
        """Check if Ollama server is responsive."""
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=timeout)
            return resp.status_code < 400
        except Exception as e:
            logger.warning(f"Ollama health check failed: {e}")
            return False
    
    def get_loaded_models(self) -> List[str]:
        """Get list of currently loaded models."""
        try:
            resp = requests.get(f"{self.base_url}/api/ps", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return [m.get("name", "") for m in data.get("models", [])]
        except Exception:
            pass
        return []
    
    def preload_model(self, model_name: str) -> bool:
        """Pre-load a model into VRAM to avoid first-request latency."""
        logger.info(f"Pre-loading model: {model_name}")
        try:
            # Send a minimal request to load the model
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json={"model": model_name, "prompt": "Hi", "stream": False},
                timeout=120  # Model loading can take time
            )
            if resp.status_code == 200:
                logger.info(f"Model {model_name} pre-loaded successfully")
                return True
            else:
                logger.warning(f"Failed to pre-load {model_name}: HTTP {resp.status_code}")
                return False
        except Exception as e:
            logger.warning(f"Failed to pre-load {model_name}: {e}")
            return False
    
    def stop_ollama(self) -> bool:
        """Stop Ollama server (via pkill or systemctl)."""
        logger.info("Stopping Ollama server...")
        try:
            # Try graceful shutdown first
            import subprocess
            result = subprocess.run(
                ["pkill", "-f", "ollama serve"],
                capture_output=True,
                timeout=10
            )
            time.sleep(2)  # Wait for process to terminate
            return True
        except Exception as e:
            logger.warning(f"Failed to stop Ollama: {e}")
            return False
    
    def start_ollama(self, num_parallel: int = None) -> bool:
        """
        Start Ollama server with optimal settings for multi-GPU.
        
        Environment variables set:
        - OLLAMA_NUM_PARALLEL: Concurrent request handling
        - CUDA_VISIBLE_DEVICES: GPU selection (if needed)
        """
        if num_parallel is None:
            num_parallel = DEFAULT_WORKERS_FALLBACK
            
        logger.info(f"Starting Ollama server with OLLAMA_NUM_PARALLEL={num_parallel}")
        
        try:
            import subprocess
            
            # Set environment for the subprocess
            env = os.environ.copy()
            env["OLLAMA_NUM_PARALLEL"] = str(num_parallel)
            env["OLLAMA_MAX_LOADED_MODELS"] = str(self.gpu_count)  # One model per GPU
            
            # Start Ollama in background
            process = subprocess.Popen(
                ["ollama", "serve"],
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True  # Detach from parent
            )
            
            # Wait for server to be ready
            for i in range(30):  # Wait up to 30 seconds
                time.sleep(1)
                if self.check_health(timeout=5):
                    logger.info("Ollama server started successfully")
                    return True
                    
            logger.error("Ollama server failed to start within 30 seconds")
            return False
            
        except FileNotFoundError:
            logger.error("Ollama binary not found. Please install Ollama first.")
            return False
        except Exception as e:
            logger.error(f"Failed to start Ollama: {e}")
            return False
    
    def restart_ollama(self, num_parallel: int = None) -> bool:
        """Restart Ollama server with auto-recovery."""
        if self.restart_count >= OLLAMA_RESTART_MAX_ATTEMPTS:
            logger.error(f"Max restart attempts ({OLLAMA_RESTART_MAX_ATTEMPTS}) reached. Manual intervention required.")
            return False
            
        self.restart_count += 1
        logger.warning(f"Restarting Ollama (attempt {self.restart_count}/{OLLAMA_RESTART_MAX_ATTEMPTS})")
        
        self.stop_ollama()
        time.sleep(OLLAMA_RESTART_WAIT_SECONDS)
        
        if self.start_ollama(num_parallel):
            logger.info("Ollama restarted successfully")
            return True
        else:
            logger.error("Ollama restart failed")
            return False
    
    def ensure_healthy(self, num_parallel: int = None) -> bool:
        """
        Ensure Ollama is healthy, restart if necessary.
        
        Returns:
            True if Ollama is healthy (possibly after restart), False if unrecoverable
        """
        if self.check_health():
            return True
            
        logger.warning("Ollama unhealthy, attempting recovery...")
        return self.restart_ollama(num_parallel)
    
    def reset_restart_count(self):
        """Reset restart counter (call after successful batch completion)."""
        self.restart_count = 0

def run_experiment_task(run_config_dict: Dict, run_id: str, progress_queue=None, ollama_base_url: str = None) -> Dict:
    """
    Worker task to run experiment in a separate process.
    
    Note: Each worker creates its own OllamaManager for health checks.
    The manager can trigger health checks but NOT restart (that's main process responsibility).
    """
    try:
        # Reconstruct config
        config = ExperimentConfig(**run_config_dict)
        
        # Set environment variables for API access consistency
        if config.model_name:
            os.environ["CUSTOM_MODEL_NAME"] = config.model_name
        if config.api_base_url:
            os.environ["CUSTOM_API_BASE"] = config.api_base_url
        if config.api_key:
            os.environ["CUSTOM_API_KEY"] = config.api_key
            if "gemini" in (config.model_name or "").lower():
                os.environ["GOOGLE_API_KEY"] = config.api_key
        
        # Run experiment (skipping matrix update to avoid race conditions)
        config.skip_matrix_update = True
        
        # Pass Ollama base URL for health checks within the experiment
        metrics = run_experiment(
            config, 
            progress_queue=progress_queue,
            ollama_base_url=ollama_base_url or config.api_base_url
        )
        if metrics is None:
            return {
                "run_id": run_id,
                "status": "failed",
                "error": "run_experiment returned None (likely prompt/variation discovery failure)"
            }
        return {"run_id": run_id, "status": "completed", "result": metrics}
    except Exception as e:
        # Log the full traceback for debugging
        import traceback
        traceback.print_exc()
        return {"run_id": run_id, "status": "failed", "error": str(e)}



# Load .env file
def load_env():
    """Load environment variables from .env file."""
    env_path = PROJECT_ROOT / '.env'
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value
        logger.info("Loaded environment from .env file")

load_env()


# Variation naming conventions
VARIATION_NAMES = {
    "paraphrase": ["paraphrase_v1", "paraphrase_v2", "paraphrase_v3"],
    "back_translation": ["backtrans_chinese", "backtrans_spanish", "backtrans_turkish"]
}


@dataclass
class VariationStatus:
    """Status of prompt variations for a base prompt."""
    base_name: str
    base_path: Path
    variations_dir: Path
    existing: List[str]
    missing: List[str]
    
    @property
    def is_complete(self) -> bool:
        return len(self.missing) == 0


@dataclass
class ExperimentRun:
    """Configuration for a single experiment run."""
    run_id: str
    granularity: str
    style: str
    variation: str
    model_id: str
    model_config: Dict[str, Any]
    prompt_path: Path
    status: str = "pending"
    
    def to_dict(self) -> Dict:
        return {
            "run_id": self.run_id,
            "granularity": self.granularity,
            "style": self.style,
            "variation": self.variation,
            "model_id": self.model_id,
            "model_name": self.model_config.get("name", "unknown"),
            "prompt_path": str(self.prompt_path),
            "status": self.status
        }


class Orchestrator:
    """
    Complete orchestration of CodeIE experiments.
    
    Handles:
    1. Checking and generating prompt variations
    2. Running experiments across all configurations
    3. Saving and displaying results
    4. Ollama auto-recovery and health management
    
    Optimization for dual A100:
    - Recommended max_workers: 4-6 (matches OLLAMA_NUM_PARALLEL)
    - Pre-loads models to avoid cold start latency
    - Auto-restarts Ollama on failures
    """
    
    def __init__(self, config_path: Path, gpu_count: int = 2):
        """
        Initialize orchestrator with configuration.
        
        Args:
            config_path: Path to experiment YAML config
            gpu_count: Number of GPUs available (default 2 for dual A100)
        """
        self.config_path = config_path
        self.config = self._load_config()
        self.gpu_count = gpu_count
        
        self.base_prompts_dir = CODEIE_ROOT / "prompts" / "base"
        self.variations_dir = CODEIE_ROOT / "prompts" / "variations"
        self.results_dir = CODEIE_ROOT / self.config["output"]["results_dir"]
        
        # Ensure directories exist
        self.variations_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Track experiment runs
        self.runs: List[ExperimentRun] = []
        self.completed_runs: List[str] = []
        
        # Initialize Ollama manager for auto-recovery
        self.ollama_manager: Optional[OllamaManager] = None
        
        logger.info(f"Orchestrator initialized with config: {config_path}")
        logger.info(f"GPU count: {gpu_count}")
    
    def _get_ollama_base_url(self) -> str:
        """Get Ollama base URL from config or default."""
        models = self._get_enabled_models()
        for model_config in models.values():
            if model_config.get("type") == "ollama":
                return model_config.get("base_url", "http://localhost:11434")
        return "http://localhost:11434"
    
    def _init_ollama_manager(self) -> OllamaManager:
        """Initialize Ollama manager if not already done."""
        if self.ollama_manager is None:
            base_url = self._get_ollama_base_url()
            self.ollama_manager = OllamaManager(base_url=base_url, gpu_count=self.gpu_count)
        return self.ollama_manager
    
    def ensure_ollama_ready(self, preload_models: List[str] = None) -> bool:
        """
        Ensure Ollama is running and optionally pre-load models.
        
        Args:
            preload_models: List of model names to pre-load into VRAM
            
        Returns:
            True if Ollama is ready, False if unrecoverable
        """
        manager = self._init_ollama_manager()
        
        # Calculate optimal parallel setting (will be refined based on model size)
        num_parallel = self.config.get("execution", {}).get(
            "ollama_num_parallel", 
            DEFAULT_WORKERS_FALLBACK
        )
        
        # Ensure Ollama is healthy
        if not manager.ensure_healthy(num_parallel):
            logger.error("Failed to ensure Ollama is healthy")
            return False
        
        # Pre-load models if requested
        if preload_models:
            for model_name in preload_models:
                manager.preload_model(model_name)
        
        return True
    
    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _resolve_dataset_path(self) -> Path:
        """Resolve dataset path from config or default location."""
        dataset_path = self.config.get("dataset", {}).get("path", "few-nerd_test")
        return (PROJECT_ROOT / dataset_path).resolve()

    def _get_dataset_size(self) -> Optional[int]:
        """Return dataset size if available, else None."""
        try:
            from datasets import load_from_disk
            dataset_path = self._resolve_dataset_path()
            if not dataset_path.exists():
                logger.warning(f"Dataset path not found: {dataset_path}")
                return None
            ds_test = load_from_disk(str(dataset_path))
            return len(ds_test)
        except Exception as e:
            logger.warning(f"Could not load dataset for size check: {e}")
            return None

    def _estimate_total_samples(self, runs: List[ExperimentRun]) -> Tuple[int, int]:
        """Estimate total samples based on dataset size and max_samples."""
        dataset_size = self._get_dataset_size()
        max_samples_per_run = self.config.get("execution", {}).get("max_samples")
        if dataset_size is None:
            effective_per_run = max_samples_per_run or 0
        else:
            if max_samples_per_run:
                effective_per_run = min(dataset_size, max_samples_per_run)
            else:
                effective_per_run = dataset_size
        return effective_per_run, len(runs) * effective_per_run

    def _check_ollama_servers(self, models: Dict[str, Dict[str, Any]]) -> None:
        """Warn if any Ollama endpoints are unreachable."""
        for model_id, model_config in models.items():
            if model_config.get("type") != "ollama":
                continue
            base_url = model_config.get("base_url", "http://localhost:11434").rstrip("/")
            try:
                resp = requests.get(f"{base_url}/api/tags", timeout=3)
                if resp.status_code >= 400:
                    logger.warning(
                        f"Ollama health check failed for {model_id} at {base_url} "
                        f"(HTTP {resp.status_code}). Runs may fail or stall."
                    )
            except Exception as e:
                logger.warning(
                    f"Ollama endpoint unreachable for {model_id} at {base_url}: {e}. "
                    "Runs may fail or stall."
                )

    def _check_ollama_health(self, base_url: str = "http://localhost:11434") -> bool:
        """
        Check if Ollama server is responsive.
        
        Returns:
            True if healthy, False if unreachable or error
        """
        try:
            resp = requests.get(f"{base_url.rstrip('/')}/api/tags", timeout=5)
            return resp.status_code < 400
        except Exception:
            return False

    def find_incomplete_batch(self) -> Optional[Tuple[Path, Dict, List[str]]]:
        """
        Find the most recent incomplete batch and return its metadata.
        
        Returns:
            Tuple of (batch_dir, summary_dict, completed_run_ids) or None if all complete
        """
        if not self.results_dir.exists():
            return None
        
        # Find all batches, sorted by timestamp (newest first)
        batches = sorted(
            self.results_dir.glob("batch_*"),
            key=lambda p: p.name,
            reverse=True
        )
        
        for batch_dir in batches:
            summary_path = batch_dir / "batch_summary.json"
            if not summary_path.exists():
                continue
            
            try:
                with open(summary_path, 'r') as f:
                    summary = json.load(f)
                
                total_runs = summary.get("total_runs", 0)
                completed_runs = summary.get("completed_runs", 0)
                
                if completed_runs < total_runs:
                    logger.info(f"Found incomplete batch: {batch_dir.name}")
                    logger.info(f"  Completed: {completed_runs}/{total_runs}")
                    
                    # Extract completed run IDs
                    completed_run_ids = [
                        r.get("run", {}).get("run_id") 
                        for r in summary.get("results", [])
                        if r.get("result") is not None
                    ]
                    
                    return batch_dir, summary, completed_run_ids
            except Exception as e:
                logger.warning(f"Could not read batch summary {batch_dir}: {e}")
                continue
        
        return None

    def filter_completed_runs(
        self, 
        runs: List[ExperimentRun], 
        completed_run_ids: List[str]
    ) -> List[ExperimentRun]:
        """Filter out already completed runs."""
        remaining = [r for r in runs if r.run_id not in completed_run_ids]
        if remaining:
            logger.info(f"Resuming: {len(remaining)} runs remaining (skipped {len(runs) - len(remaining)})")
        return remaining
    
    def _get_base_prompts(self) -> List[Tuple[str, Path]]:
        """Get all base prompt files."""
        base_prompts = []
        
        for granularity in self.config["dataset"]["granularities"]:
            shots = (self.config["prompts"]["coarse_shots"] 
                     if granularity == "coarse" 
                     else self.config["prompts"]["fine_shots"])
            
            for style in self.config["prompts"]["styles"]:
                base_name = f"{granularity}_{style}_{shots}shot"
                base_path = self.base_prompts_dir / f"{base_name}.txt"
                
                if base_path.exists():
                    base_prompts.append((base_name, base_path))
                else:
                    logger.warning(f"Base prompt not found: {base_path}")
        
        return base_prompts
    

    def _get_all_variation_names(self) -> List[str]:
        """Get all expected variation names."""
        variations = ["base"]
        
        # Load from config
        if "prompts" in self.config and "variations" in self.config["prompts"]:
            vars_config = self.config["prompts"]["variations"]
            if "paraphrase" in vars_config:
                variations.extend(vars_config["paraphrase"])
            if "back_translation" in vars_config:
                variations.extend(vars_config["back_translation"])
        else:
             # Fallback to defaults if config is missing structure
             variations.extend(VARIATION_NAMES["paraphrase"])
             variations.extend(VARIATION_NAMES["back_translation"])
             
        return variations
    
    def check_variations(self) -> List[VariationStatus]:
        """Check which variations exist and which are missing."""
        statuses = []
        all_variations = self._get_all_variation_names()
        
        for base_name, base_path in self._get_base_prompts():
            var_dir = self.variations_dir / base_name
            var_dir.mkdir(parents=True, exist_ok=True)
            
            existing = []
            missing = []
            
            for var_name in all_variations:
                if var_name == "base":
                    if base_path.exists():
                        existing.append(var_name)
                    else:
                        missing.append(var_name)
                    continue

                var_path = var_dir / f"{var_name}.txt"
                if var_path.exists():
                    existing.append(var_name)
                else:
                    missing.append(var_name)
            
            statuses.append(VariationStatus(
                base_name=base_name,
                base_path=base_path,
                variations_dir=var_dir,
                existing=existing,
                missing=missing
            ))
        
        return statuses
    
    def generate_missing_variations(
        self, 
        statuses: Optional[List[VariationStatus]] = None,
        force: bool = False
    ) -> Dict[str, Any]:
        """
        Generate missing prompt variations.
        
        Args:
            statuses: Variation statuses (will check if not provided)
            force: If True, regenerate all variations
        
        Returns:
            Summary of generation results
        """
        from src.paraphrase.paraphraser import DirectParaphraser, ParaphraseConfig
        from src.paraphrase.back_translator import BackTranslator, BackTranslationConfig
        from src.paraphrase.similarity import SemanticSimilarity
        
        if statuses is None:
            statuses = self.check_variations()
        
        # Check if any variations need to be generated
        total_missing = sum(len(s.missing) for s in statuses)
        if total_missing == 0 and not force:
            logger.info("All variations exist. Use --force to regenerate.")
            return {"generated": 0, "skipped": 24, "errors": 0}
        
        logger.info(f"Generating {total_missing} missing variations...")
        
        # Initialize modules
        paraphraser = DirectParaphraser(ParaphraseConfig(num_variations=3))
        back_translator = BackTranslator(BackTranslationConfig())
        similarity = SemanticSimilarity()
        
        results = {
            "generated": 0,
            "skipped": 0,
            "errors": 0,
            "details": []
        }
        
        for status in statuses:
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing: {status.base_name}")
            logger.info(f"Missing: {len(status.missing)} variations")
            
            # Load base prompt
            with open(status.base_path, 'r') as f:
                base_prompt = f.read()
            
            # Determine style from base name
            style = "pl" if "_pl_" in status.base_name else "nl"
            
            # Generate paraphrase variations
            for var_name in VARIATION_NAMES["paraphrase"]:
                if var_name == "base":
                    continue

                var_path = status.variations_dir / f"{var_name}.txt"
                
                if var_path.exists() and not force:
                    logger.info(f"  Skipping existing: {var_name}")
                    results["skipped"] += 1
                    continue
                
                try:
                    logger.info(f"  Generating: {var_name}")
                    variation = paraphraser.paraphrase(base_prompt, style)
                    
                    # Calculate similarity
                    sim_score = similarity.compute_similarity(base_prompt, variation)
                    logger.info(f"    Similarity: {sim_score:.4f}")
                    
                    # Save variation
                    with open(var_path, 'w') as f:
                        f.write(variation)
                    
                    results["generated"] += 1
                    results["details"].append({
                        "base": status.base_name,
                        "variation": var_name,
                        "similarity": sim_score,
                        "status": "success"
                    })
                    
                    # Rate limiting
                    time.sleep(20)
                    
                except Exception as e:
                    logger.error(f"    Failed: {e}")
                    results["errors"] += 1
                    results["details"].append({
                        "base": status.base_name,
                        "variation": var_name,
                        "error": str(e),
                        "status": "failed"
                    })
            
            # Generate back-translation variations
            language_map = {
                "backtrans_chinese": "Chinese",
                "backtrans_spanish": "Spanish",
                "backtrans_turkish": "Turkish"
            }
            
            for var_name, language in language_map.items():
                var_path = status.variations_dir / f"{var_name}.txt"
                
                if var_path.exists() and not force:
                    logger.info(f"  Skipping existing: {var_name}")
                    results["skipped"] += 1
                    continue
                
                try:
                    logger.info(f"  Generating: {var_name} (via {language})")
                    _, variation = back_translator.back_translate(base_prompt, language)
                    
                    # Calculate similarity
                    sim_score = similarity.compute_similarity(base_prompt, variation)
                    logger.info(f"    Similarity: {sim_score:.4f}")
                    
                    # Save variation
                    with open(var_path, 'w') as f:
                        f.write(variation)
                    
                    results["generated"] += 1
                    results["details"].append({
                        "base": status.base_name,
                        "variation": var_name,
                        "language": language,
                        "similarity": sim_score,
                        "status": "success"
                    })
                    
                    # Rate limiting
                    time.sleep(20)
                    
                except Exception as e:
                    logger.error(f"    Failed: {e}")
                    results["errors"] += 1
                    results["details"].append({
                        "base": status.base_name,
                        "variation": var_name,
                        "error": str(e),
                        "status": "failed"
                    })
        
        # Save generation log
        log_path = self.variations_dir / "generation_log.json"
        with open(log_path, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "results": results
            }, f, indent=2)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Generation complete:")
        logger.info(f"  Generated: {results['generated']}")
        logger.info(f"  Skipped: {results['skipped']}")
        logger.info(f"  Errors: {results['errors']}")
        logger.info(f"Log saved to: {log_path}")
        
        return results
    
    def _get_enabled_models(self) -> Dict[str, Dict]:
        """Get all enabled models from configuration."""
        models = {}
        for model_id, model_config in self.config["models"].items():
            if model_config.get("enabled", False):
                models[model_id] = model_config
        return models
    
    def _get_prompt_path(
        self, 
        granularity: str, 
        style: str, 
        variation: str
    ) -> Optional[Path]:
        """Get path to a specific prompt variation."""
        shots = (self.config["prompts"]["coarse_shots"] 
                 if granularity == "coarse" 
                 else self.config["prompts"]["fine_shots"])
        base_name = f"{granularity}_{style}_{shots}shot"
        if variation == "base":
            prompt_path = self.base_prompts_dir / f"{base_name}.txt"
        else:
            prompt_path = self.variations_dir / base_name / f"{variation}.txt"
        
        if prompt_path.exists():
            return prompt_path
        else:
            if variation == "base":
                logger.warning(f"Base prompt not found: {prompt_path}")
                logger.warning("Please run build_base_prompts.py first.")
            else:
                logger.warning(f"Prompt not found: {prompt_path}")
            return None
    
    def generate_experiment_matrix(
        self,
        filter_model: Optional[str] = None,
        filter_granularity: Optional[str] = None,
        filter_style: Optional[str] = None,
        filter_variation: Optional[str] = None
    ) -> List[ExperimentRun]:
        """Generate all experiment runs based on configuration."""
        models = self._get_enabled_models()
        granularities = self.config["dataset"]["granularities"]
        styles = self.config["prompts"]["styles"]
        variations = self._get_all_variation_names()
        
        # Apply filters
        if filter_model:
            models = {k: v for k, v in models.items() if k == filter_model}
        if filter_granularity:
            granularities = [g for g in granularities if g == filter_granularity]
        if filter_style:
            styles = [s for s in styles if s == filter_style]
        if filter_variation:
            variations = [v for v in variations if v == filter_variation]
        
        runs = []
        
        for granularity, style, variation in product(granularities, styles, variations):
            for model_id, model_config in models.items():
                prompt_path = self._get_prompt_path(granularity, style, variation)
                
                if prompt_path is None:
                    continue
                
                run_id = f"{model_id}_{granularity}_{style}_{variation}"
                
                run = ExperimentRun(
                    run_id=run_id,
                    granularity=granularity,
                    style=style,
                    variation=variation,
                    model_id=model_id,
                    model_config=model_config,
                    prompt_path=prompt_path
                )
                runs.append(run)
        
        self.runs = runs
        logger.info(f"Generated {len(runs)} experiment runs")
        return runs
    
    def run_single_experiment(self, run: ExperimentRun, output_dir_override: Optional[str] = None, matrix_dir_override: Optional[str] = None, quiet: bool = False) -> Dict[str, Any]:
        """Execute a single experiment run."""
        logger.info(f"\n{'='*60}")
        logger.info(f"Running: {run.run_id}")
        logger.info(f"  Model: {run.model_config['name']}")
        logger.info(f"  Granularity: {run.granularity}")
        logger.info(f"  Style: {run.style}")
        logger.info(f"  Variation: {run.variation}")
        logger.info(f"  Prompt: {run.prompt_path}")
        logger.info(f"{'='*60}")
        
        # Import here to avoid circular imports
        from run_codeie_experiments import run_experiment, ExperimentConfig
        
        # Create experiment config
        config = ExperimentConfig(
            granularity=run.granularity,
            style=run.style,
            variation=run.variation if run.variation != "base" else "v0_original",  # Use default config for base
            prompt_path=str(run.prompt_path),  # Pass the path to prompt file
            model_name=run.model_config["name"],
            max_tokens=run.model_config.get("max_tokens", 512),
            temperature=run.model_config.get("temperature", 0.0),
            max_test_samples=self.config["execution"].get("max_samples"),
            output_dir=output_dir_override or self.config["output"].get("results_dir", "CODEIE-results"),
            matrix_dir=matrix_dir_override,
            quiet=quiet
        )
        
        # Set environment variables for API access
        if run.model_config["type"] == "google":
            api_key_env = run.model_config.get("api_key_env", "GOOGLE_API_KEY")
            api_key = os.getenv(api_key_env) or os.getenv("GEMINI_API_KEY")
            if api_key:
                os.environ["CUSTOM_API_KEY"] = api_key
                os.environ["CUSTOM_API_BASE"] = "https://generativelanguage.googleapis.com/v1beta"
        elif run.model_config["type"] == "ollama":
            os.environ["CUSTOM_API_BASE"] = run.model_config.get("base_url", "http://localhost:11434")
        
        os.environ["CUSTOM_MODEL_NAME"] = run.model_config["name"]
        
        # Run experiment
        try:
            results = run_experiment(config)
            run.status = "completed"
            return results
        except Exception as e:
            logger.error(f"Experiment failed: {e}")
            run.status = "failed"
            return {"error": str(e)}
    

    def run_all(
        self,
        filter_model: Optional[str] = None,
        filter_granularity: Optional[str] = None,
        filter_style: Optional[str] = None,
        filter_variation: Optional[str] = None,
        dry_run: bool = False,
        skip_generation: bool = False,
        quiet: bool = False,
        max_workers: int = None,  # Will auto-calculate if None
        auto_recover_ollama: bool = True,
        preload_models: bool = True
    ) -> Dict[str, Any]:
        """
        Run the complete pipeline with Ollama auto-recovery.
        
        Args:
            filter_model: Only run this model
            filter_granularity: Only run this granularity
            filter_style: Only run this style
            filter_variation: Only run this variation
            dry_run: If True, only print what would be run
            skip_generation: If True, skip variation generation check
            max_workers: Number of parallel processes (auto-calculated if None)
            auto_recover_ollama: If True, automatically restart Ollama on failures
            preload_models: If True, pre-load models into VRAM before starting
        
        Returns:
            Summary of all experiment results
            
        Optimization Notes for Dual A100:
        - Default max_workers is set to OLLAMA_NUM_PARALLEL (6 for dual A100)
        - Ensure Ollama is started with: OLLAMA_NUM_PARALLEL=6 ollama serve
        - With 2x A100 80GB, you can run ~6-8 parallel 7B model requests
        - Larger models (13B+) may need fewer parallel workers
        """
        # Auto-calculate optimal workers based on model size and GPU count
        if max_workers is None:
            # Check config first
            max_workers = self.config.get("execution", {}).get("max_workers")
            
            # If not in config, calculate based on largest model being used
            if max_workers is None:
                models = self._get_enabled_models()
                ollama_models = [m["name"] for m in models.values() if m.get("type") == "ollama"]
                
                if ollama_models:
                    # Use the most conservative (lowest) worker count for the largest model
                    worker_estimates = [estimate_workers_for_model(m, self.gpu_count) for m in ollama_models]
                    max_workers = min(worker_estimates)
                    logger.info(f"Auto-calculated max_workers={max_workers} based on model sizes: {ollama_models}")
                else:
                    max_workers = DEFAULT_WORKERS_FALLBACK
        
        logger.info(f"\n{'#'*60}")
        logger.info(f"# CodeIE Experiment Orchestrator")
        logger.info(f"# One-Stop Shop Pipeline (Parallel Execution)")
        logger.info(f"# GPU Count: {self.gpu_count} | Max Workers: {max_workers}")
        logger.info(f"{'#'*60}")
        
        # Step 1: Check and generate variations
        if not skip_generation and not dry_run:
            logger.info("\n[Step 1/3] Checking prompt variations...")
            statuses = self.check_variations()
            
            total_missing = sum(len(s.missing) for s in statuses)
            total_existing = sum(len(s.existing) for s in statuses)
            
            logger.info(f"  Existing: {total_existing}/24")
            logger.info(f"  Missing: {total_missing}/24")
            
            if total_missing > 0:
                logger.info("\nGenerating missing variations...")
                self.generate_missing_variations(statuses)
        else:
            logger.info("\n[Step 1/3] Skipping variation check")
        
        # Step 2: Generate experiment matrix
        logger.info("\n[Step 2/3] Generating experiment matrix...")
        runs = self.generate_experiment_matrix(
            filter_model=filter_model,
            filter_granularity=filter_granularity,
            filter_style=filter_style,
            filter_variation=filter_variation
        )
        
        if not runs:
            logger.warning("No experiments to run!")
            logger.warning("Check that models are enabled in config and variations exist.")
            return {"runs": [], "summary": "No experiments configured"}
        
        logger.info(f"  Total experiments: {len(runs)}")
        
        # Check for incomplete batch to resume
        incomplete = self.find_incomplete_batch()
        if incomplete and not dry_run:
            batch_dir, summary, completed_run_ids = incomplete
            logger.info("\n[RESUME MODE] Continuing from previous checkpoint...")
            runs = self.filter_completed_runs(runs, completed_run_ids)
            if not runs:
                logger.info("All runs already completed in this batch!")
                return {"runs": [], "summary": "All runs already completed"}

        # Preflight checks and Ollama initialization
        models_dict = self._get_enabled_models()
        ollama_models = [m["name"] for m in models_dict.values() if m.get("type") == "ollama"]
        
        if ollama_models and auto_recover_ollama and not dry_run:
            logger.info("\n[OLLAMA SETUP] Initializing Ollama with auto-recovery...")
            
            # Get unique model names to preload
            unique_models = list(set(ollama_models))
            
            # Ensure Ollama is running and healthy
            if not self.ensure_ollama_ready(preload_models=unique_models if preload_models else None):
                logger.error("Failed to initialize Ollama. Aborting.")
                return {"runs": [], "summary": "Ollama initialization failed"}
            
            logger.info(f"  Ollama ready with models: {unique_models}")
            logger.info(f"  Auto-calculated workers: {max_workers} (based on model size)")
        else:
            # Legacy preflight check
            self._check_ollama_servers(models_dict)

        # Estimate total samples (more accurate than max_samples × runs)
        effective_per_run, total_samples_est = self._estimate_total_samples(runs)
        logger.info(
            "  Estimated samples per run: "
            f"{effective_per_run} (max_samples={self.config.get('execution', {}).get('max_samples')})"
        )
        logger.info(f"  Estimated total samples: {total_samples_est}")
        
        if dry_run:
            logger.info("\n[DRY RUN] Experiment matrix:")
            for i, run in enumerate(runs, 1):
                logger.info(f"  {i:3d}. {run.run_id}")
            return {
                "runs": [r.to_dict() for r in runs],
                "summary": f"Would run {len(runs)} experiments"
            }
        
        # Step 3: Run experiments
        if quiet:
            logger.setLevel(logging.WARNING)
            # Suppress other loggers
            logging.getLogger("run_codeie_experiments").setLevel(logging.WARNING)
            print(f"\n[Step 3/3] Running {len(runs)} experiments in quiet mode (Parallel: {max_workers})...")
        else:
            logger.info(f"\n[Step 3/3] Running experiments (Parallel workers: {max_workers})...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_results_dir = self.results_dir / f"batch_{timestamp}"
        batch_results_dir.mkdir(parents=True, exist_ok=True)
        
        # Relative paths for config
        batch_rel_dir = str(batch_results_dir.relative_to(CODEIE_ROOT))
        matrix_root_dir = str(self.results_dir.relative_to(CODEIE_ROOT))
        
        all_results = []
        start_time = time.time()
        
        from tqdm import tqdm
        from multiprocessing import Manager
        import threading
        
        # Create a manager for shared queue
        manager = Manager()
        progress_queue = manager.Queue()
        
        # Calculate total samples (ensure total reflects expected sample count)
        effective_per_run, total_samples = self._estimate_total_samples(runs)
        if total_samples == 0:
            fallback_max = self.config.get("execution", {}).get("max_samples") or 0
            if fallback_max > 0:
                effective_per_run = fallback_max
                total_samples = len(runs) * fallback_max
        
        # Progress bar updater thread
        def update_pbar(queue, total):
            with tqdm(total=total, desc="Total Progress (Samples)", unit="sample") as pbar:
                while True:
                    try:
                        # Use timeout to prevent indefinite blocking if main thread crashes
                        item = queue.get(timeout=300)  # 5 minute timeout
                        if item is None:  # Sentinel
                            break
                        pbar.update(item)
                    except Exception:
                        # queue.Empty on timeout - check if we should exit
                        # If the main process is dead, this daemon thread will be killed anyway
                        continue
        
        # Start progress thread
        pbar_thread = threading.Thread(target=update_pbar, args=(progress_queue, total_samples))
        pbar_thread.daemon = True
        pbar_thread.start()
        
        # Prepare tasks
        future_to_run = {}
        
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            for i, run in enumerate(runs, 1):
                # Prepare config values
                # Logic copied/adapted from run_single_experiment
                
                # Resolve API Key/URL for config
                api_key = None
                api_base_url = None
                
                if run.model_config["type"] == "google":
                    api_key_env = run.model_config.get("api_key_env", "GOOGLE_API_KEY")
                    api_key = os.getenv(api_key_env) or os.getenv("GEMINI_API_KEY")
                elif run.model_config["type"] == "ollama":
                    api_base_url = run.model_config.get("base_url", "http://localhost:11434")
                
                # Create config dict
                config_dict = {
                    "granularity": run.granularity,
                    "style": run.style,
                    "variation": run.variation if run.variation != "base" else "v0_original",
                    "prompt_path": str(run.prompt_path),
                    "model_name": run.model_config["name"],
                    "max_tokens": run.model_config.get("max_tokens", 512),
                    "temperature": run.model_config.get("temperature", 0.0),
                    "max_test_samples": self.config["execution"].get("max_samples"),
                    "output_dir": batch_rel_dir,
                    "matrix_dir": matrix_root_dir,
                    "quiet": quiet,
                    "api_key": api_key,
                    "api_base_url": api_base_url,
                    "skip_matrix_update": True # Explicitly set true for worker
                }
                
                future = executor.submit(run_experiment_task, config_dict, run.run_id, progress_queue, api_base_url)
                future_to_run[future] = run
                
            # Process results as they complete
            completed_count = 0
            failed_consecutive = 0  # Track consecutive failures for recovery trigger
            total_failures = 0      # Track total failures for fail-fast
            
            # Fail-fast thresholds
            MAX_CONSECUTIVE_RUN_FAILURES = 5   # Crash if 5 consecutive runs fail
            MAX_TOTAL_FAILURE_RATIO = 0.8      # Crash if >80% of runs fail
            
            # Process results as they complete
            for future in as_completed(future_to_run, timeout=7200):  # 2-hour timeout per future
                    run = future_to_run[future]
                    completed_count += 1
                    
                    # Periodic Ollama health check with auto-recovery
                    if completed_count % OLLAMA_HEALTH_CHECK_INTERVAL == 0 and auto_recover_ollama:
                        if self.ollama_manager:
                            if not self.ollama_manager.check_health():
                                logger.warning(
                                    f"ALERT: Ollama health check failed after {completed_count} runs. "
                                    "Attempting auto-recovery..."
                                )
                                if self.ollama_manager.ensure_healthy():
                                    logger.info("Ollama recovered successfully, continuing...")
                                    self.ollama_manager.reset_restart_count()
                                else:
                                    logger.error("Ollama recovery failed. Remaining runs may fail.")
                    
                    try:
                        result_data = future.result(timeout=30)  # Additional timeout for result retrieval
                        
                        if result_data["status"] == "completed":
                            metrics = result_data["result"]
                            if not metrics:
                                raise RuntimeError("Experiment returned empty results")
                            self.completed_runs.append(run.run_id)
                            run.status = "completed"
                            failed_consecutive = 0  # Reset on success
                            
                            # Log completion even if quiet is not on (verbose logging) 
                            # But if quiet, tqdm handles the UI.
                            if not quiet:
                                logger.info(f"Completed: {run.run_id}")
                            
                            # Handle Matrix Update in Main Process
                            result_file = metrics.get('result_file')
                            if result_file and os.path.exists(result_file):
                                try:
                                    with open(result_file, 'r') as f:
                                        final_results_data = json.load(f)
                                    
                                    # Reconstruct config for update function
                                    temp_config = ExperimentConfig(
                                        granularity=run.granularity,
                                        style=run.style,
                                        variation=run.variation,
                                        model_name=run.model_config["name"]
                                    )
                                    
                                    # Use matrix_dir from config or default
                                    matrix_save_dir = self.results_dir
                                    update_experiment_matrix(str(matrix_save_dir), temp_config, final_results_data, result_file)
                                    
                                except Exception as e:
                                    logger.error(f"Failed to update matrix for {run.run_id}: {e}")
                            
                            all_results.append({
                                "run": run.to_dict(),
                                "result": metrics
                            })
                            
                        else:
                            run.status = "failed"
                            error_msg = result_data.get("error", "Unknown error")
                            logger.error(f"Failed: {run.run_id} - {error_msg}")
                            all_results.append({
                                "run": run.to_dict(),
                                "result": {"error": error_msg}
                            })
                            
                            # Track failures
                            failed_consecutive += 1
                            total_failures += 1
                            
                            # FAIL-FAST: Check for too many consecutive failures
                            if failed_consecutive >= MAX_CONSECUTIVE_RUN_FAILURES:
                                error_msg = (
                                    f"FATAL: {MAX_CONSECUTIVE_RUN_FAILURES} consecutive run failures. "
                                    f"Model or Ollama is persistently failing. Aborting to prevent wasted time."
                                )
                                logger.error(error_msg)
                                progress_queue.put(None)  # Stop progress thread
                                raise RuntimeError(error_msg)
                            
                            # Trigger recovery after 3 consecutive failures
                            if failed_consecutive >= 3 and auto_recover_ollama and self.ollama_manager:
                                logger.warning(f"{failed_consecutive} consecutive failures detected. Triggering Ollama recovery...")
                                if not self.ollama_manager.ensure_healthy():
                                    logger.error("Ollama recovery failed!")
                                failed_consecutive = 0  # Reset after recovery attempt
                            
                    except Exception as e:
                        logger.error(f"Exception for {run.run_id}: {e}")
                        all_results.append({
                            "run": run.to_dict(),
                            "result": {"error": str(e)}
                        })
                        
                        # Track failures
                        failed_consecutive += 1
                        total_failures += 1
                        
                        # FAIL-FAST: Check for too many consecutive failures
                        if failed_consecutive >= MAX_CONSECUTIVE_RUN_FAILURES:
                            error_msg = (
                                f"FATAL: {MAX_CONSECUTIVE_RUN_FAILURES} consecutive run failures. "
                                f"Model or Ollama is persistently failing. Aborting."
                            )
                            logger.error(error_msg)
                            progress_queue.put(None)  # Stop progress thread
                            raise RuntimeError(error_msg)
                        
                        # Trigger recovery after 3 consecutive failures
                        if failed_consecutive >= 3 and auto_recover_ollama and self.ollama_manager:
                            logger.warning(f"{failed_consecutive} consecutive failures. Triggering Ollama recovery...")
                            self.ollama_manager.ensure_healthy()
                            failed_consecutive = 0
            
            # FAIL-FAST: Check total failure ratio after all runs complete
            if len(runs) > 0 and total_failures > 0:
                failure_ratio = total_failures / len(runs)
                if failure_ratio > MAX_TOTAL_FAILURE_RATIO:
                    error_msg = (
                        f"FATAL: {failure_ratio:.1%} of runs failed ({total_failures}/{len(runs)}). "
                        f"Too many failures to continue. Check Ollama and model configuration."
                    )
                    logger.error(error_msg)
                    progress_queue.put(None)  # Stop progress thread
                    raise RuntimeError(error_msg)

        
        # Signal progress thread to stop
        progress_queue.put(None)
        pbar_thread.join()

        # Save batch summary
        summary = {
            "timestamp": timestamp,
            "total_runs": len(runs),
            "completed_runs": len(self.completed_runs),
            "config_path": str(self.config_path),
            "results": all_results
        }
        
        summary_path = batch_results_dir / "batch_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        if quiet:
            print("\n") # New line after the progress bar
            
        # Display results summary
        if quiet:
            logger.setLevel(logging.INFO) # Restoration for the final summary

        logger.info(f"\n{'='*60}")
        logger.info(f"Pipeline complete!")
        logger.info(f"  Completed: {len(self.completed_runs)}/{len(runs)} runs")
        logger.info(f"  Results saved to: {batch_results_dir}")
        logger.info(f"{'='*60}")
        
        return summary
    
    def show_status(self):
        """Display current status of variations and configuration."""
        logger.info(f"\n{'='*60}")
        logger.info("CodeIE Orchestrator Status")
        logger.info(f"{'='*60}")
        
        # Check variations
        statuses = self.check_variations()
        
        logger.info("\nPrompt Variations:")
        for status in statuses:
            check = "✓" if status.is_complete else "✗"
            logger.info(f"  [{check}] {status.base_name}")
            total_variations = len(self._get_all_variation_names())
            logger.info(f"      Existing: {len(status.existing)}/{total_variations}")
            if status.missing:
                logger.info(f"      Missing: {', '.join(status.missing)}")
        
        # Show enabled models
        models = self._get_enabled_models()
        logger.info(f"\nEnabled Models ({len(models)}):")
        for model_id, config in models.items():
            logger.info(f"  - {model_id}: {config['name']} ({config['type']})")
        
        if not models:
            logger.warning("  No models enabled! Enable models in config/experiment_config.yaml")
        
        # Count potential experiments
        total_variations = len(self._get_all_variation_names())
        total_runs = len(models) * 4 * total_variations  # models × base_prompts × variations
        logger.info(f"\nPotential experiments: {total_runs}")


def main():
    parser = argparse.ArgumentParser(
        description="CodeIE Experiment Orchestrator - One-Stop Shop"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="CodeIE/config/experiment_config.yaml",
        help="Path to experiment configuration YAML"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Filter to specific model ID"
    )
    parser.add_argument(
        "--granularity",
        type=str,
        choices=["coarse", "fine"],
        default=None,
        help="Filter to specific granularity"
    )
    parser.add_argument(
        "--style",
        type=str,
        choices=["pl", "nl"],
        default=None,
        help="Filter to specific style"
    )
    parser.add_argument(
        "--variation",
        type=str,
        default=None,
        help="Filter to specific variation"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only print experiment matrix, don't run"
    )
    parser.add_argument(
        "--generate-only",
        action="store_true",
        help="Only generate missing variations, don't run experiments"
    )
    parser.add_argument(
        "--force-generate",
        action="store_true",
        help="Regenerate all variations even if they exist"
    )
    parser.add_argument(
        "--skip-generation",
        action="store_true",
        help="Skip variation generation check"
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show current status and exit"
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List all configured models and exit"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only show critical warnings, progress, and remaining time"
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=None,
        help="Number of parallel workers (default: auto-calculated based on model size)"
    )
    parser.add_argument(
        "--gpu-count",
        type=int,
        default=2,
        help="Number of GPUs available (default: 2 for dual A100)"
    )
    parser.add_argument(
        "--no-auto-recover",
        action="store_true",
        help="Disable automatic Ollama restart on failures"
    )
    parser.add_argument(
        "--no-preload",
        action="store_true",
        help="Skip pre-loading models into VRAM"
    )
    parser.add_argument(
        "--ollama-parallel",
        type=int,
        default=None,
        help=f"OLLAMA_NUM_PARALLEL setting (default: {DEFAULT_WORKERS_FALLBACK}, auto-adjusted per model)"
    )
    
    args = parser.parse_args()
    
    # Find config path
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / args.config
    
    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        sys.exit(1)
    
    orchestrator = Orchestrator(config_path, gpu_count=args.gpu_count)
    
    # Handle different modes
    if args.status:
        orchestrator.show_status()
        return
    
    if args.list_models:
        models = orchestrator._get_enabled_models()
        print("\nEnabled models:")
        for model_id, config in models.items():
            print(f"  - {model_id}: {config['name']} ({config['type']})")
        return
    
    if args.generate_only:
        orchestrator.generate_missing_variations(force=args.force_generate)
        return
    
    # Run full pipeline
    orchestrator.run_all(
        filter_model=args.model,
        filter_granularity=args.granularity,
        filter_style=args.style,
        filter_variation=args.variation,
        dry_run=args.dry_run,
        skip_generation=args.skip_generation,
        quiet=args.quiet,
        max_workers=args.max_workers,
        auto_recover_ollama=not args.no_auto_recover,
        preload_models=not args.no_preload
    )


if __name__ == "__main__":
    main()
