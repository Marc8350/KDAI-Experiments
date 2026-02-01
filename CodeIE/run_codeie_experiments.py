"""
CodeIE Experiments Runner for FewNerd NER

This script runs NER experiments using the CodeIE framework on FewNerd,
parallel to the run_gollie_experiments.py script. It supports:
- Multiple prompt variations (code-style and NL-style)
- Custom API endpoint (Qwen2.5-7B or compatible)
- Stratified few-shot in-context learning examples from training set
- Evaluation on test set with P/R/F1 metrics

Usage:
    python run_codeie_experiments.py --granularity coarse --style pl --num_shots 5
    python run_codeie_experiments.py --granularity fine --style nl --num_shots 3

Author: Adapted for seminar thesis
"""

import os
import sys
import json
import time
import re
import logging
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Setup paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODEIE_ROOT = os.path.dirname(os.path.abspath(__file__))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if CODEIE_ROOT not in sys.path:
    sys.path.insert(0, CODEIE_ROOT)

from datasets import load_from_disk

# Import prompt variations
from prompt_variations import CODE_STYLE_VARIATIONS, NL_STYLE_VARIATIONS
from prompt_variations.code_style_variations import CodeStyleConfig
from prompt_variations.nl_style_variations import NLStyleConfig

# Import custom API wrapper
from src.api.custom_api_wrapper import CustomAPIWrapper

# Import evaluation
from src.eval.scorer import EntityScorer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Constants
END = "# END"
END_LINE = "\n----------------------------------------"


# ============================================================================
# Configuration
# ============================================================================

@dataclass
class ExperimentConfig:
    """Configuration for a single experiment run."""
    # Dataset settings
    granularity: str = "coarse"  # "coarse" or "fine"
    num_shots: int = 5
    seed: int = 1
    max_test_samples: Optional[int] = None  # Limit for testing
    
    # Prompt style
    style: str = "pl"  # "pl" (code) or "nl" (natural language)
    variation: str = "v0_original"
    
    # API settings
    api_base_url: str = os.getenv("CUSTOM_API_BASE_URL", "http://localhost:8000/v1")
    api_key: str = os.getenv("CUSTOM_API_KEY", "not-needed")
    model_name: str = os.getenv("CUSTOM_MODEL_NAME", "qwen2.5-7b")
    
    # Generation settings
    max_tokens: int = 256
    temperature: float = 0.0
    
    # Paths
    data_dir: str = "data"
    output_dir: str = "CODEIE-results"


# ============================================================================
# Prompt Builders
# ============================================================================

def build_code_style_prompt(
    text: str,
    entities: List[Dict],
    config: CodeStyleConfig,
    include_output: bool = True
) -> str:
    """
    Build a code-style (pl-func) prompt for NER.
    
    Args:
        text: Input text
        entities: List of entity dicts with 'text' and 'type' keys (for examples)
        config: Code style configuration
        include_output: Whether to include entity appends (for examples) or not (for test)
    
    Returns:
        Formatted prompt string
    """
    lines = [
        f'def {config.function_name}({config.function_input}):',
        f'\t""" {config.docstring} . """',
        f'\t{config.input_var} = "{text}"',
        f'\t{config.list_var} = []',
        f'\t# {config.inline_comment}',
    ]
    
    if include_output:
        for entity in entities:
            entity_text = entity.get('text', entity.get('span', ''))
            entity_type = entity.get('type', entity.get('label', ''))
            lines.append(
                f'\t{config.list_var}.append({{"{config.entity_text_key}": "{entity_text}", "{config.entity_type_key}": "{entity_type}"}})'
            )
    
    return '\n'.join(lines)


def build_nl_style_prompt(
    text: str,
    record: str,
    config: NLStyleConfig,
    include_output: bool = True
) -> str:
    """
    Build a natural language style (nl-sel) prompt for NER.
    
    Args:
        text: Input text
        record: SEL-format record string (for examples)
        config: NL style configuration
        include_output: Whether to include record (for examples) or not (for test)
    
    Returns:
        Formatted prompt string
    """
    prompt = f'{config.input_prefix} "{text}" {config.input_suffix} {config.entity_prompt} '
    
    if include_output and record:
        prompt += record
    
    return prompt


# ============================================================================
# Few-Shot Example Builder
# ============================================================================

def load_fewshot_examples(
    data_dir: str,
    granularity: str,
    num_shots: int,
    seed: int
) -> List[Dict]:
    """
    Load few-shot examples from the stratified samples (from training data).
    
    Args:
        data_dir: Base data directory
        granularity: "coarse" or "fine"
        num_shots: Number of shots
        seed: Random seed used for sampling
    
    Returns:
        List of example dictionaries
    """
    shot_dir = os.path.join(
        data_dir,
        f"fewnerd_{granularity}_shot",
        f"seed{seed}",
        f"{num_shots}shot"
    )
    
    train_file = os.path.join(shot_dir, "train.json")
    
    if not os.path.exists(train_file):
        logging.warning(f"Few-shot file not found: {train_file}")
        logging.info("Run prepare_fewnerd_for_codeie.py first to create the data.")
        return []
    
    examples = []
    with open(train_file, 'r') as f:
        for line in f:
            if line.strip():
                examples.append(json.loads(line))
    
    logging.info(f"Loaded {len(examples)} few-shot examples from {train_file}")
    return examples


def build_icl_prompt(
    examples: List[Dict],
    style: str,
    variation_config: Any
) -> str:
    """
    Build the in-context learning prompt from few-shot examples.
    
    Args:
        examples: List of example dictionaries
        style: "pl" or "nl"
        variation_config: Style-specific configuration
    
    Returns:
        Concatenated ICL prompt string
    """
    prompt_parts = []
    
    for example in examples:
        text = example['text']
        
        if style == "pl":
            # Use spot_asoc for entities
            entities = example.get('spot_asoc', [])
            example_prompt = build_code_style_prompt(
                text=text,
                entities=entities,
                config=variation_config,
                include_output=True
            )
        else:  # nl style
            record = example.get('record', '')
            example_prompt = build_nl_style_prompt(
                text=text,
                record=record,
                config=variation_config,
                include_output=True
            )
        
        prompt_parts.append(example_prompt)
        prompt_parts.append(END)
        prompt_parts.append("")  # Empty line between examples
    
    return '\n'.join(prompt_parts)


# ============================================================================
# Inference & Parsing
# ============================================================================

def run_inference(
    prompt: str,
    config: ExperimentConfig
) -> str:
    """
    Run inference using the custom API.
    
    Args:
        prompt: The full prompt (ICL + test input)
        config: Experiment configuration
    
    Returns:
        Generated completion text
    """
    try:
        response = CustomAPIWrapper.call(
            prompt=prompt,
            max_tokens=config.max_tokens,
            model=config.model_name,
            temperature=config.temperature,
            base_url=config.api_base_url,
            api_key=config.api_key,
            stop=[END, END_LINE, "\ndef ", "\n\ndef "]
        )
        
        return CustomAPIWrapper.parse_response(response)
        
    except Exception as e:
        logging.error(f"Inference failed: {e}")
        return ""


def parse_code_style_output(
    output: str,
    entity_types: List[str]
) -> List[Dict]:
    """
    Parse code-style output to extract entities.
    
    Args:
        output: Generated code output
        entity_types: Valid entity type names
    
    Returns:
        List of extracted entity dictionaries
    """
    entities = []
    
    # Pattern to match entity_list.append({"text": "...", "type": "..."})
    pattern = r'entity_list\.append\(\{["\']text["\']: ["\']([^"\']*)["\'], ["\']type["\']: ["\']([^"\']*)["\']'
    
    # Also try reverse order: {"type": "...", "text": "..."}
    pattern_alt = r'entity_list\.append\(\{["\']type["\']: ["\']([^"\']*)["\'], ["\']text["\']: ["\']([^"\']*)["\']'
    
    for match in re.finditer(pattern, output):
        text, entity_type = match.groups()
        if entity_type in entity_types and text:
            entities.append({'text': text, 'type': entity_type})
    
    for match in re.finditer(pattern_alt, output):
        entity_type, text = match.groups()
        if entity_type in entity_types and text:
            entities.append({'text': text, 'type': entity_type})
    
    return entities


def parse_nl_style_output(
    output: str,
    text: str,
    entity_types: List[str]
) -> List[Dict]:
    """
    Parse NL-style (SEL format) output to extract entities.
    
    This is more complex as it uses special tokens like <0>, <1>, <5>
    which represent structure in the UIE format.
    
    Args:
        output: Generated NL output
        text: Original input text (for validation)
        entity_types: Valid entity type names
    
    Returns:
        List of extracted entity dictionaries
    """
    entities = []
    
    # SEL format: <0> <0> type <5> span <1> <0> type <5> span <1> <1>
    # Simplified parsing - extract type-span pairs
    
    # Remove outer markers and split by entity boundaries
    output = output.replace('<extra_id_', '<').replace('>', '>')
    
    # Pattern for: <0> type <5> span <1>
    pattern = r'<0>\s*(\w+(?:\s+\w+)*)\s*<5>\s*([^<]+?)\s*<1>'
    
    for match in re.finditer(pattern, output):
        entity_type = match.group(1).strip().lower()
        entity_text = match.group(2).strip()
        
        # Normalize entity type
        entity_type = entity_type.replace(' ', '-')
        
        if entity_type in entity_types and entity_text:
            entities.append({'text': entity_text, 'type': entity_type})
    
    return entities


# ============================================================================
# Evaluation
# ============================================================================

def evaluate_predictions(
    gold_list: List[List[Dict]],
    pred_list: List[List[Dict]]
) -> Dict[str, float]:
    """
    Evaluate predictions against gold standard.
    
    Args:
        gold_list: List of gold entity lists per sample
        pred_list: List of predicted entity lists per sample
    
    Returns:
        Dictionary with precision, recall, F1 scores
    """
    # Convert to format expected by EntityScorer
    gold_formatted = []
    pred_formatted = []
    
    for gold_entities, pred_entities in zip(gold_list, pred_list):
        # String-based matching (more lenient than offset-based)
        gold_formatted.append({
            'string': [(e['type'], e['text']) for e in gold_entities],
            'offset': []  # Not using offset-based evaluation
        })
        pred_formatted.append({
            'string': [(e['type'], e['text']) for e in pred_entities],
            'offset': []
        })
    
    # Manual F1 calculation
    total_tp = 0
    total_gold = 0
    total_pred = 0
    
    for gold, pred in zip(gold_formatted, pred_formatted):
        gold_set = set(gold['string'])
        pred_set = set(pred['string'])
        
        tp = len(gold_set & pred_set)
        total_tp += tp
        total_gold += len(gold_set)
        total_pred += len(pred_set)
    
    precision = total_tp / total_pred if total_pred > 0 else 0
    recall = total_tp / total_gold if total_gold > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'tp': total_tp,
        'gold_count': total_gold,
        'pred_count': total_pred
    }


# ============================================================================
# Main Experiment Loop
# ============================================================================

def run_experiment(config: ExperimentConfig):
    """
    Run a complete NER experiment with CodeIE.
    
    Args:
        config: Experiment configuration
    """
    logging.info("="*60)
    logging.info("CodeIE NER Experiment")
    logging.info("="*60)
    logging.info(f"Granularity: {config.granularity}")
    logging.info(f"Style: {config.style}")
    logging.info(f"Variation: {config.variation}")
    logging.info(f"Shots: {config.num_shots}")
    logging.info(f"Seed: {config.seed}")
    logging.info("="*60)
    
    # Setup output directory
    output_dir = os.path.join(CODEIE_ROOT, config.output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Get variation config
    if config.style == "pl":
        variation_config = CODE_STYLE_VARIATIONS.get(config.variation)
        if not variation_config:
            raise ValueError(f"Unknown code-style variation: {config.variation}")
    else:
        variation_config = NL_STYLE_VARIATIONS.get(config.variation)
        if not variation_config:
            raise ValueError(f"Unknown NL-style variation: {config.variation}")
    
    # Load test data
    tag_key = 'ner_tags' if config.granularity == 'coarse' else 'fine_ner_tags'
    test_path = os.path.join(PROJECT_ROOT, 'few-nerd_test')
    
    logging.info(f"Loading test data from: {test_path}")
    ds_test = load_from_disk(test_path)
    tag_names = ds_test.features[tag_key].feature.names
    entity_types = [t for t in tag_names if t != 'O']
    
    logging.info(f"Entity types: {entity_types}")
    
    # Load few-shot examples (from training data)
    data_dir = os.path.join(CODEIE_ROOT, config.data_dir)
    examples = load_fewshot_examples(
        data_dir=data_dir,
        granularity=config.granularity,
        num_shots=config.num_shots,
        seed=config.seed
    )
    
    if not examples:
        logging.error("No few-shot examples found. Please run prepare_fewnerd_for_codeie.py first.")
        return
    
    # Build ICL prompt
    icl_prompt = build_icl_prompt(
        examples=examples,
        style=config.style,
        variation_config=variation_config
    )
    
    logging.info(f"ICL prompt length: {len(icl_prompt)} characters")
    
    # Prepare results storage
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = os.path.join(
        output_dir,
        f"{config.granularity}_{config.style}_{config.variation}_{config.num_shots}shot_seed{config.seed}_{timestamp}.json"
    )
    
    all_gold = []
    all_pred = []
    sentence_results = []
    
    # Determine test samples to process
    num_samples = len(ds_test)
    if config.max_test_samples:
        num_samples = min(num_samples, config.max_test_samples)
    
    logging.info(f"Processing {num_samples} test samples...")
    
    for i in range(num_samples):
        sample = ds_test[i]
        tokens = sample['tokens']
        text = ' '.join(tokens)
        tags = sample[tag_key]
        
        # Extract gold entities
        gold_entities = []
        current_entity = None
        for j, (token, tag_idx) in enumerate(zip(tokens, tags)):
            tag_name = tag_names[tag_idx]
            if tag_name == 'O':
                if current_entity:
                    gold_entities.append(current_entity)
                    current_entity = None
            else:
                if current_entity is None or current_entity['type'] != tag_name:
                    if current_entity:
                        gold_entities.append(current_entity)
                    current_entity = {'type': tag_name, 'text': token}
                else:
                    current_entity['text'] += ' ' + token
        if current_entity:
            gold_entities.append(current_entity)
        
        # Build test prompt
        if config.style == "pl":
            test_prompt = build_code_style_prompt(
                text=text,
                entities=[],
                config=variation_config,
                include_output=False
            )
        else:
            test_prompt = build_nl_style_prompt(
                text=text,
                record="",
                config=variation_config,
                include_output=False
            )
        
        # Full prompt = ICL + test input
        full_prompt = icl_prompt + "\n" + test_prompt
        
        # Run inference
        start_time = time.time()
        generated = run_inference(full_prompt, config)
        elapsed = time.time() - start_time
        
        # Parse output
        if config.style == "pl":
            pred_entities = parse_code_style_output(
                output=test_prompt + generated,
                entity_types=entity_types
            )
        else:
            pred_entities = parse_nl_style_output(
                output=generated,
                text=text,
                entity_types=entity_types
            )
        
        # Store results
        all_gold.append(gold_entities)
        all_pred.append(pred_entities)
        
        sentence_result = {
            'index': i,
            'text': text,
            'gold': gold_entities,
            'prediction': pred_entities,
            'generated': generated[:500],  # Truncate for logging
            'elapsed_time': elapsed
        }
        sentence_results.append(sentence_result)
        
        # Periodic logging and saving
        if (i + 1) % 10 == 0 or i == num_samples - 1:
            current_metrics = evaluate_predictions(all_gold, all_pred)
            logging.info(
                f"Progress: {i+1}/{num_samples} | "
                f"P: {current_metrics['precision']:.4f} | "
                f"R: {current_metrics['recall']:.4f} | "
                f"F1: {current_metrics['f1']:.4f}"
            )
            
            # Save intermediate results
            results = {
                'config': asdict(config),
                'metrics': current_metrics,
                'processed_count': len(sentence_results),
                'timestamp': timestamp,
                'sentences': sentence_results
            }
            with open(result_file, 'w') as f:
                json.dump(results, f, indent=2)
    
    # Final evaluation
    final_metrics = evaluate_predictions(all_gold, all_pred)
    
    logging.info("="*60)
    logging.info("Final Results")
    logging.info("="*60)
    logging.info(f"Precision: {final_metrics['precision']:.4f}")
    logging.info(f"Recall: {final_metrics['recall']:.4f}")
    logging.info(f"F1: {final_metrics['f1']:.4f}")
    logging.info(f"Results saved to: {result_file}")
    logging.info("="*60)
    
    return final_metrics


def main():
    parser = argparse.ArgumentParser(description="Run CodeIE NER experiments")
    
    # Dataset settings
    parser.add_argument('--granularity', choices=['coarse', 'fine'], default='coarse',
                        help="Entity granularity")
    parser.add_argument('--num_shots', type=int, default=5,
                        help="Number of few-shot examples per entity type")
    parser.add_argument('--seed', type=int, default=1,
                        help="Random seed for few-shot sampling")
    parser.add_argument('--max_test', type=int, default=None,
                        help="Maximum test samples (for debugging)")
    
    # Prompt settings
    parser.add_argument('--style', choices=['pl', 'nl'], default='pl',
                        help="Prompt style: pl (code) or nl (natural language)")
    parser.add_argument('--variation', default='v0_original',
                        help="Prompt variation name")
    parser.add_argument('--run_all_variations', action='store_true',
                        help="Run all variations for the selected style")
    
    # API settings
    parser.add_argument('--api_url', default=None,
                        help="Custom API base URL")
    parser.add_argument('--api_key', default=None,
                        help="API key")
    parser.add_argument('--model', default=None,
                        help="Model name")
    
    # Generation settings
    parser.add_argument('--max_tokens', type=int, default=256,
                        help="Maximum tokens to generate")
    parser.add_argument('--temperature', type=float, default=0.0,
                        help="Sampling temperature")
    
    args = parser.parse_args()
    
    # Build config
    config = ExperimentConfig(
        granularity=args.granularity,
        num_shots=args.num_shots,
        seed=args.seed,
        max_test_samples=args.max_test,
        style=args.style,
        variation=args.variation,
        max_tokens=args.max_tokens,
        temperature=args.temperature
    )
    
    if args.api_url:
        config.api_base_url = args.api_url
    if args.api_key:
        config.api_key = args.api_key
    if args.model:
        config.model_name = args.model
    
    if args.run_all_variations:
        # Run all variations for the selected style
        variations = CODE_STYLE_VARIATIONS if args.style == 'pl' else NL_STYLE_VARIATIONS
        
        all_results = {}
        for var_name in variations.keys():
            config.variation = var_name
            logging.info(f"\n\n{'#'*60}")
            logging.info(f"Running variation: {var_name}")
            logging.info(f"{'#'*60}\n")
            
            metrics = run_experiment(config)
            all_results[var_name] = metrics
        
        # Summary
        logging.info("\n\n" + "="*60)
        logging.info("SUMMARY - All Variations")
        logging.info("="*60)
        for var_name, metrics in all_results.items():
            logging.info(f"{var_name}: F1={metrics['f1']:.4f}")
    else:
        # Run single variation
        run_experiment(config)


if __name__ == "__main__":
    main()
