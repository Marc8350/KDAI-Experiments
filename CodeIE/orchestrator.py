#!/usr/bin/env python3
"""
CodeIE Experiment Orchestrator

Runs experiments across all configurations:
- All enabled models
- All granularities (coarse, fine)
- All styles (pl, nl)
- All 6 prompt variations per base prompt

Total experiments per model: 2 × 2 × 6 = 24 runs

Usage:
    python orchestrator.py --config config/experiment_config.yaml
    python orchestrator.py --config config/experiment_config.yaml --dry-run
    python orchestrator.py --granularity coarse --style pl --model gemini_flash
"""

import os
import sys
import yaml
import logging
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
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
    Orchestrates CodeIE experiments across all configurations.
    
    Iterates through:
    - Enabled models from config
    - Granularities: coarse, fine
    - Styles: pl (code), nl (natural language)
    - Variations: 3 paraphrase + 3 back-translation
    """
    
    def __init__(self, config_path: Path):
        """
        Initialize orchestrator with configuration.
        
        Args:
            config_path: Path to experiment_config.yaml
        """
        self.config_path = config_path
        self.config = self._load_config()
        
        self.variations_dir = CODEIE_ROOT / "prompts" / "variations"
        self.results_dir = CODEIE_ROOT / self.config["output"]["results_dir"]
        
        # Track all experiment runs
        self.runs: List[ExperimentRun] = []
        self.completed_runs: List[str] = []
        
        logger.info(f"Orchestrator initialized with config: {config_path}")
    
    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _get_enabled_models(self) -> Dict[str, Dict]:
        """Get all enabled models from configuration."""
        models = {}
        for model_id, model_config in self.config["models"].items():
            if model_config.get("enabled", False):
                models[model_id] = model_config
        return models
    
    def _get_variation_names(self) -> List[str]:
        """Get all variation names."""
        variations = []
        variations.extend(self.config["prompts"]["variations"]["paraphrase"])
        variations.extend(self.config["prompts"]["variations"]["back_translation"])
        return variations
    
    def _get_prompt_path(
        self, 
        granularity: str, 
        style: str, 
        variation: str
    ) -> Optional[Path]:
        """Get path to a specific prompt variation."""
        # Use granularity-specific shot count for base prompt name
        shots = self.config["prompts"]["coarse_shots"] if granularity == "coarse" else self.config["prompts"]["fine_shots"]
        base_name = f"{granularity}_{style}_{shots}shot"
        prompt_path = self.variations_dir / base_name / f"{variation}.txt"
        
        if prompt_path.exists():
            return prompt_path
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
        """
        Generate all experiment runs based on configuration.
        
        Args:
            filter_model: Only include this model
            filter_granularity: Only include this granularity
            filter_style: Only include this style
            filter_variation: Only include this variation
        
        Returns:
            List of ExperimentRun configurations
        """
        models = self._get_enabled_models()
        granularities = self.config["dataset"]["granularities"]
        styles = self.config["prompts"]["styles"]
        variations = self._get_variation_names()
        
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
        
        for model_id, model_config in models.items():
            for granularity, style, variation in product(granularities, styles, variations):
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
    
    def run_single_experiment(self, run: ExperimentRun) -> Dict[str, Any]:
        """
        Execute a single experiment run.
        
        Args:
            run: ExperimentRun configuration
        
        Returns:
            Dict with experiment results
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Running: {run.run_id}")
        logger.info(f"  Model: {run.model_config['name']}")
        logger.info(f"  Granularity: {run.granularity}")
        logger.info(f"  Style: {run.style}")
        logger.info(f"  Variation: {run.variation}")
        logger.info(f"  Prompt: {run.prompt_path}")
        logger.info(f"{'='*60}")
        
        # Import here to avoid circular imports
        from CodeIE.run_codeie_experiments import run_experiment, ExperimentConfig
        
        # Create experiment config
        config = ExperimentConfig(
            granularity=run.granularity,
            style=run.style,
            variation=run.variation,
            model_name=run.model_config["name"],
            max_tokens=run.model_config.get("max_tokens", 512),
            temperature=run.model_config.get("temperature", 0.0),
            max_test_samples=self.config["execution"].get("max_samples"),
        )
        
        # Set environment variables for API access
        if run.model_config["type"] == "google":
            api_key_env = run.model_config.get("api_key_env", "GOOGLE_API_KEY")
            if os.getenv(api_key_env):
                os.environ["CUSTOM_API_KEY"] = os.getenv(api_key_env)
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
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Run all experiments in the matrix.
        
        Args:
            filter_model: Only run this model
            filter_granularity: Only run this granularity
            filter_style: Only run this style
            filter_variation: Only run this variation
            dry_run: If True, only print what would be run
        
        Returns:
            Summary of all experiment results
        """
        runs = self.generate_experiment_matrix(
            filter_model=filter_model,
            filter_granularity=filter_granularity,
            filter_style=filter_style,
            filter_variation=filter_variation
        )
        
        if not runs:
            logger.warning("No experiments to run!")
            return {"runs": [], "summary": "No experiments configured"}
        
        logger.info(f"\n{'#'*60}")
        logger.info(f"# CodeIE Experiment Orchestrator")
        logger.info(f"# Total experiments: {len(runs)}")
        logger.info(f"# Dry run: {dry_run}")
        logger.info(f"{'#'*60}")
        
        if dry_run:
            logger.info("\nExperiment matrix (dry run):")
            for i, run in enumerate(runs, 1):
                logger.info(f"  {i:3d}. {run.run_id}")
            return {
                "runs": [r.to_dict() for r in runs],
                "summary": f"Would run {len(runs)} experiments"
            }
        
        # Create results directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_results_dir = self.results_dir / f"batch_{timestamp}"
        batch_results_dir.mkdir(parents=True, exist_ok=True)
        
        # Run all experiments
        all_results = []
        
        for i, run in enumerate(runs, 1):
            logger.info(f"\n[{i}/{len(runs)}] Starting: {run.run_id}")
            
            try:
                result = self.run_single_experiment(run)
                all_results.append({
                    "run": run.to_dict(),
                    "result": result
                })
                self.completed_runs.append(run.run_id)
                
            except KeyboardInterrupt:
                logger.warning("\nInterrupted by user. Saving progress...")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                all_results.append({
                    "run": run.to_dict(),
                    "result": {"error": str(e)}
                })
        
        # Save batch summary
        summary = {
            "timestamp": timestamp,
            "total_runs": len(runs),
            "completed_runs": len(self.completed_runs),
            "config_path": str(self.config_path),
            "results": all_results
        }
        
        summary_path = batch_results_dir / "batch_summary.json"
        import json
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Batch complete: {len(self.completed_runs)}/{len(runs)} runs")
        logger.info(f"Results saved to: {batch_results_dir}")
        logger.info(f"{'='*60}")
        
        return summary


def main():
    parser = argparse.ArgumentParser(
        description="CodeIE Experiment Orchestrator"
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
        "--list-models",
        action="store_true",
        help="List all configured models and exit"
    )
    
    args = parser.parse_args()
    
    config_path = PROJECT_ROOT / args.config
    
    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        sys.exit(1)
    
    orchestrator = Orchestrator(config_path)
    
    if args.list_models:
        models = orchestrator._get_enabled_models()
        print("\nEnabled models:")
        for model_id, config in models.items():
            print(f"  - {model_id}: {config['name']} ({config['type']})")
        return
    
    orchestrator.run_all(
        filter_model=args.model,
        filter_granularity=args.granularity,
        filter_style=args.style,
        filter_variation=args.variation,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
