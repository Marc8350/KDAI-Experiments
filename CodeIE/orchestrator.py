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
    """
    
    def __init__(self, config_path: Path):
        """Initialize orchestrator with configuration."""
        self.config_path = config_path
        self.config = self._load_config()
        
        self.base_prompts_dir = CODEIE_ROOT / "prompts" / "base"
        self.variations_dir = CODEIE_ROOT / "prompts" / "variations"
        self.results_dir = CODEIE_ROOT / self.config["output"]["results_dir"]
        
        # Ensure directories exist
        self.variations_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Track experiment runs
        self.runs: List[ExperimentRun] = []
        self.completed_runs: List[str] = []
        
        logger.info(f"Orchestrator initialized with config: {config_path}")
    
    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
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
    def _get_all_variation_names(self) -> List[str]:
        """Get all expected variation names."""
        return ["base"] + VARIATION_NAMES["paraphrase"] + VARIATION_NAMES["back_translation"]
    
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
        skip_generation: bool = False
    ) -> Dict[str, Any]:
        """
        Run the complete pipeline.
        
        Args:
            filter_model: Only run this model
            filter_granularity: Only run this granularity
            filter_style: Only run this style
            filter_variation: Only run this variation
            dry_run: If True, only print what would be run
            skip_generation: If True, skip variation generation check
        
        Returns:
            Summary of all experiment results
        """
        logger.info(f"\n{'#'*60}")
        logger.info(f"# CodeIE Experiment Orchestrator")
        logger.info(f"# One-Stop Shop Pipeline")
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
        
        if dry_run:
            logger.info("\n[DRY RUN] Experiment matrix:")
            for i, run in enumerate(runs, 1):
                logger.info(f"  {i:3d}. {run.run_id}")
            return {
                "runs": [r.to_dict() for r in runs],
                "summary": f"Would run {len(runs)} experiments"
            }
        
        # Step 3: Run experiments
        logger.info("\n[Step 3/3] Running experiments...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        batch_results_dir = self.results_dir / f"batch_{timestamp}"
        batch_results_dir.mkdir(parents=True, exist_ok=True)
        
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
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        # Display results summary
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
    
    args = parser.parse_args()
    
    # Find config path
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / args.config
    
    if not config_path.exists():
        logger.error(f"Config file not found: {config_path}")
        sys.exit(1)
    
    orchestrator = Orchestrator(config_path)
    
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
        skip_generation=args.skip_generation
    )


if __name__ == "__main__":
    main()
