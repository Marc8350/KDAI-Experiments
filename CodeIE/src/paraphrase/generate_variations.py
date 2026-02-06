"""
Generate Prompt Variations for CodeIE Experiments

This script generates 6 prompt variations for each base prompt:
- 3 variations from direct paraphrasing
- 3 variations from back-translation (Chinese, Spanish, Turkish)

Each variation is validated against a similarity threshold (0.9) and
logged with creation metadata and similarity scores.
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from CodeIE.src.paraphrase.paraphraser import DirectParaphraser, ParaphraseConfig
from CodeIE.src.paraphrase.back_translator import BackTranslator, BackTranslationConfig
from CodeIE.src.paraphrase.similarity import SemanticSimilarity

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class VariationResult:
    """Result of a single variation generation."""
    name: str
    method: str  # "paraphrase" or "back_translation"
    language: Optional[str]  # For back-translation
    similarity_score: float
    accepted: bool
    model_used: str
    content: str
    intermediate_content: Optional[str] = None  # For back-translation


@dataclass
class VariationLog:
    """Log entry for variation generation."""
    base_prompt_name: str
    base_prompt_path: str
    created_at: str
    model_used: str
    similarity_threshold: float
    variations: List[Dict[str, Any]]
    total_generated: int
    total_accepted: int
    total_rejected: int


def load_base_prompt(prompt_path: Path) -> str:
    """Load a base prompt from file."""
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()


def save_variation(
    output_dir: Path, 
    variation_name: str, 
    content: str
) -> Path:
    """Save a variation to file."""
    output_path = output_dir / f"{variation_name}.txt"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    return output_path


def save_log(output_dir: Path, log: VariationLog) -> Path:
    """Save the creation log to JSON."""
    log_path = output_dir / "creation_log.json"
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(asdict(log), f, indent=2)
    return log_path


def generate_variations_for_prompt(
    base_prompt_path: Path,
    output_dir: Path,
    prompt_style: str = "code",
    entity_types: Optional[List[str]] = None,
    similarity_threshold: float = 0.9,
    max_retries: int = 3
) -> VariationLog:
    """
    Generate all 6 variations for a single base prompt.
    
    Args:
        base_prompt_path: Path to the base prompt file
        output_dir: Directory to save variations
        prompt_style: "code" or "nl"
        entity_types: List of valid entity types
        similarity_threshold: Minimum similarity score to accept
        max_retries: Max retries for rejected variations
    
    Returns:
        VariationLog with all generation results
    """
    logger.info(f"Generating variations for: {base_prompt_path.name}")
    
    # Load base prompt
    base_prompt = load_base_prompt(base_prompt_path)
    base_name = base_prompt_path.stem
    
    # Create output directory
    output_dir = output_dir / base_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize components
    paraphraser = DirectParaphraser(ParaphraseConfig(
        temperature=0.3,
        num_variations=3,
        similarity_threshold=similarity_threshold
    ))
    
    back_translator = BackTranslator(BackTranslationConfig(
        temperature=0.1,
        similarity_threshold=similarity_threshold
    ))
    
    similarity_calc = SemanticSimilarity()
    
    variations: List[VariationResult] = []
    
    # Generate 3 paraphrase variations
    logger.info("Generating paraphrase variations...")
    for i in range(3):
        retry_count = 0
        accepted = False
        
        while not accepted and retry_count < max_retries:
            try:
                paraphrased = paraphraser.paraphrase(
                    base_prompt, 
                    prompt_style, 
                    entity_types
                )
                
                # Check similarity
                score = similarity_calc.compute_similarity(base_prompt, paraphrased)
                
                if score >= similarity_threshold:
                    accepted = True
                    variation = VariationResult(
                        name=f"paraphrase_v{i+1}",
                        method="paraphrase",
                        language=None,
                        similarity_score=score,
                        accepted=True,
                        model_used=paraphraser.config.model_name,
                        content=paraphrased
                    )
                    variations.append(variation)
                    
                    # Save to file
                    save_variation(output_dir, variation.name, paraphrased)
                    logger.info(f"  paraphrase_v{i+1}: similarity={score:.4f} ✓")
                else:
                    retry_count += 1
                    logger.warning(f"  paraphrase_v{i+1} attempt {retry_count}: similarity={score:.4f} < {similarity_threshold} (retrying)")
            
            except Exception as e:
                retry_count += 1
                logger.error(f"  paraphrase_v{i+1} error: {e}")
        
        if not accepted:
            logger.error(f"  paraphrase_v{i+1}: Failed after {max_retries} retries")
            # Save the last attempt anyway with accepted=False
            variations.append(VariationResult(
                name=f"paraphrase_v{i+1}",
                method="paraphrase",
                language=None,
                similarity_score=score if 'score' in locals() else 0.0,
                accepted=False,
                model_used=paraphraser.config.model_name,
                content=paraphrased if 'paraphrased' in locals() else ""
            ))
    
    # Generate 3 back-translation variations
    logger.info("Generating back-translation variations...")
    languages = ["Chinese", "Spanish", "Turkish"]
    
    for lang in languages:
        retry_count = 0
        accepted = False
        
        while not accepted and retry_count < max_retries:
            try:
                intermediate, back_translated = back_translator.back_translate(
                    base_prompt, lang
                )
                
                # Check similarity
                score = similarity_calc.compute_similarity(base_prompt, back_translated)
                
                lang_code = lang.lower()[:2]  # "ch", "sp", "tu"
                
                if score >= similarity_threshold:
                    accepted = True
                    variation = VariationResult(
                        name=f"backtrans_{lang_code}",
                        method="back_translation",
                        language=lang,
                        similarity_score=score,
                        accepted=True,
                        model_used=back_translator.config.model_name,
                        content=back_translated,
                        intermediate_content=intermediate
                    )
                    variations.append(variation)
                    
                    # Save to file
                    save_variation(output_dir, variation.name, back_translated)
                    logger.info(f"  backtrans_{lang_code}: similarity={score:.4f} ✓")
                else:
                    retry_count += 1
                    logger.warning(f"  backtrans_{lang_code} attempt {retry_count}: similarity={score:.4f} < {similarity_threshold} (retrying)")
            
            except Exception as e:
                retry_count += 1
                logger.error(f"  backtrans_{lang_code} error: {e}")
        
        if not accepted:
            logger.error(f"  backtrans_{lang_code}: Failed after {max_retries} retries")
            variations.append(VariationResult(
                name=f"backtrans_{lang_code}",
                method="back_translation",
                language=lang,
                similarity_score=score if 'score' in locals() else 0.0,
                accepted=False,
                model_used=back_translator.config.model_name,
                content=back_translated if 'back_translated' in locals() else "",
                intermediate_content=intermediate if 'intermediate' in locals() else None
            ))
    
    # Create log
    accepted_count = sum(1 for v in variations if v.accepted)
    log = VariationLog(
        base_prompt_name=base_name,
        base_prompt_path=str(base_prompt_path),
        created_at=datetime.now().isoformat(),
        model_used=paraphraser.config.model_name,
        similarity_threshold=similarity_threshold,
        variations=[asdict(v) for v in variations],
        total_generated=len(variations),
        total_accepted=accepted_count,
        total_rejected=len(variations) - accepted_count
    )
    
    # Save log
    save_log(output_dir, log)
    
    logger.info(f"Completed: {accepted_count}/{len(variations)} variations accepted")
    return log


def generate_all_variations(
    base_prompts_dir: Path,
    output_dir: Path,
    granularities: List[str] = ["coarse", "fine"],
    styles: List[str] = ["pl", "nl"],
    similarity_threshold: float = 0.9
) -> Dict[str, VariationLog]:
    """
    Generate variations for all base prompts.
    
    Args:
        base_prompts_dir: Directory containing base prompts
        output_dir: Directory to save variations
        granularities: List of granularities to process
        styles: List of styles to process
        similarity_threshold: Minimum similarity score
    
    Returns:
        Dict mapping prompt names to their variation logs
    """
    logger.info("=" * 60)
    logger.info("Starting prompt variation generation")
    logger.info("=" * 60)
    
    # Load entity types for each granularity
    entity_types = {
        "coarse": ["person", "location", "organization", "building", 
                   "art", "product", "event", "other"],
        "fine": None  # Will use defaults
    }
    
    all_logs = {}
    
    for granularity in granularities:
        for style in styles:
            prompt_name = f"{granularity}_{style}_3shot"
            prompt_path = base_prompts_dir / f"{prompt_name}.txt"
            
            if not prompt_path.exists():
                logger.warning(f"Base prompt not found: {prompt_path}")
                continue
            
            logger.info(f"\nProcessing: {prompt_name}")
            logger.info("-" * 40)
            
            try:
                log = generate_variations_for_prompt(
                    base_prompt_path=prompt_path,
                    output_dir=output_dir,
                    prompt_style=style,
                    entity_types=entity_types.get(granularity),
                    similarity_threshold=similarity_threshold
                )
                all_logs[prompt_name] = log
            
            except Exception as e:
                logger.error(f"Failed to process {prompt_name}: {e}")
    
    # Save summary
    summary = {
        "generated_at": datetime.now().isoformat(),
        "total_prompts": len(all_logs),
        "similarity_threshold": similarity_threshold,
        "prompts": {
            name: {
                "accepted": log.total_accepted,
                "rejected": log.total_rejected
            }
            for name, log in all_logs.items()
        }
    }
    
    summary_path = output_dir / "generation_summary.json"
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info("\n" + "=" * 60)
    logger.info(f"Generation complete. Summary saved to: {summary_path}")
    logger.info("=" * 60)
    
    return all_logs


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate prompt variations for CodeIE")
    parser.add_argument(
        "--base-dir", 
        type=str, 
        default="CodeIE/prompts/base",
        help="Directory containing base prompts"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="CodeIE/prompts/variations",
        help="Directory to save variations"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.9,
        help="Similarity threshold (default: 0.9)"
    )
    parser.add_argument(
        "--granularity",
        type=str,
        nargs="+",
        default=["coarse", "fine"],
        help="Granularities to process"
    )
    parser.add_argument(
        "--style",
        type=str,
        nargs="+",
        default=["pl", "nl"],
        help="Styles to process"
    )
    
    args = parser.parse_args()
    
    base_dir = PROJECT_ROOT / args.base_dir
    output_dir = PROJECT_ROOT / args.output_dir
    
    generate_all_variations(
        base_prompts_dir=base_dir,
        output_dir=output_dir,
        granularities=args.granularity,
        styles=args.style,
        similarity_threshold=args.threshold
    )
