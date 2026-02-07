"""
CodeIE Experiments Runner for FewNerd NER (Enhanced with Entity Schema)

This script runs NER experiments using the CodeIE framework on FewNerd,
parallel to the run_gollie_experiments.py script. It supports:
- Multiple prompt variations (code-style and NL-style)
- EXPLICIT entity type definitions in prompts (like GoLLIE)
- Integration with Google Gemini (via LangChain)
- Integration with Ollama (via LangChain)
- Stratified few-shot in-context learning examples from training set
- Evaluation on test set with P/R/F1 metrics

Key enhancement over original CodeIE: Prompts include explicit entity class
definitions, giving the model clearer guidance about valid entity types.

Usage:
    python run_codeie_experiments.py --granularity coarse --style pl --model mistral
    python run_codeie_experiments.py --granularity fine --style nl --model qwen2.5:7b

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

# LangChain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama, OllamaLLM
from langchain_core.messages import HumanMessage

# Setup paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODEIE_ROOT = os.path.dirname(os.path.abspath(__file__))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
if CODEIE_ROOT not in sys.path:
    sys.path.insert(0, CODEIE_ROOT)

from datasets import load_from_disk

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
    max_test_samples: Optional[int] = None  # Limit for testing
    
    # Prompt style
    style: str = "pl"  # "pl" (code) or "nl" (natural language)
    variation: str = "default"  # Variation name (if using dynamic prompts)
    
    # API settings
    api_base_url: Optional[str] = None
    api_key: Optional[str] = None
    model_name: Optional[str] = None
    
    # Generation settings
    max_tokens: int = 256
    temperature: float = 0.0
    
    # Paths
    data_dir: str = "data"
    output_dir: str = "CODEIE-results"
    prompt_path: Optional[str] = None  # Path to pre-generated prompt file


def load_variations(granularity: str):
    """Load prompt variations for the specified granularity."""
    if granularity == "coarse":
        from prompt_variations.coarse_prompt_variations import (
            CODE_STYLE_VARIATIONS, NL_STYLE_VARIATIONS, ENTITY_DEFINITIONS
        )
    else:
        # For fine-grained, generate if not exists
        variations_path = os.path.join(
            CODEIE_ROOT, 'prompt_variations', 'fine_prompt_variations.py'
        )
        if not os.path.exists(variations_path):
            logging.info("Generating fine-grained variations...")
            os.system(f"cd {CODEIE_ROOT} && python generate_codeie_prompt_variations.py --granularity fine")
        
        from prompt_variations.fine_prompt_variations import (
            CODE_STYLE_VARIATIONS, NL_STYLE_VARIATIONS, ENTITY_DEFINITIONS
        )
    
    return CODE_STYLE_VARIATIONS, NL_STYLE_VARIATIONS, ENTITY_DEFINITIONS


# ============================================================================
# Prompt Builders (Enhanced with Entity Schema)
# ============================================================================

def build_entity_schema_block(
    entity_types: List[str],
    entity_definitions: Dict[str, str],
    style: str = "code"
) -> str:
    """
    Build the entity schema block to include in prompts.
    
    Args:
        entity_types: List of valid entity type names
        entity_definitions: Dict mapping type to description
        style: "code" or "nl"
    
    Returns:
        Formatted schema block
    """
    if style == "code":
        lines = []
        for entity_type in entity_types:
            if entity_type in entity_definitions:
                desc = entity_definitions[entity_type]
                lines.append(f'\t# "{entity_type}": {desc}')
            else:
                lines.append(f'\t# "{entity_type}"')
        return '\n'.join(lines)
    else:
        return ', '.join(entity_types)


def build_code_style_prompt(
    text: str,
    entities: List[Dict],
    config: Any,
    entity_types: List[str],
    entity_definitions: Dict[str, str],
    include_schema: bool = True,
    include_output: bool = True
) -> str:
    """
    Build a code-style (pl-func) prompt for NER with entity schema.
    
    Args:
        text: Input text
        entities: List of entity dicts (for examples)
        config: Code style configuration
        entity_types: Valid entity type names
        entity_definitions: Entity type descriptions
        include_schema: Whether to include entity type definitions
        include_output: Whether to include entity appends
    
    Returns:
        Formatted prompt string
    """
    lines = [
        f'def {config.function_name}(input_text):',
        f'\t""" {config.docstring} """',
    ]
    
    # Add entity schema block (key enhancement over original CodeIE)
    if include_schema:
        lines.append(f'\t{config.entity_header}')
        schema_block = build_entity_schema_block(
            entity_types, entity_definitions, style="code"
        )
        lines.append(schema_block)
        lines.append('')  # Empty line after schema
    
    # Input and entity list
    lines.append(f'\tinput_text = "{text}"')
    lines.append('\tentity_list = []')
    lines.append('\t# extracted named entities')
    
    # Add entity outputs for examples
    if include_output:
        for entity in entities:
            entity_text = entity.get('text', entity.get('span', ''))
            entity_type = entity.get('type', entity.get('label', ''))
            lines.append(
                f'\tentity_list.append({{"text": "{entity_text}", "type": "{entity_type}"}})'
            )
    
    return '\n'.join(lines)


def build_nl_style_prompt(
    text: str,
    record: str,
    config: Any,
    entity_types: List[str],
    include_schema: bool = True,
    include_output: bool = True
) -> str:
    """
    Build a natural language style (nl-sel) prompt for NER with entity schema.
    
    Args:
        text: Input text
        record: SEL-format record string (for examples)
        config: NL style configuration
        entity_types: Valid entity type names
        include_schema: Whether to include schema in prompt
        include_output: Whether to include record
    
    Returns:
        Formatted prompt string
    """
    schema_str = ', '.join(entity_types) if include_schema else ''
    
    # Format text_prefix with placeholders
    prompt = config.text_prefix.format(text=text, schema=schema_str)
    prompt += config.entity_prompt
    
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
    """Load few-shot examples from the stratified samples (from training data)."""
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
    variation_config: Any,
    entity_types: List[str],
    entity_definitions: Dict[str, str],
    include_schema: bool = True
) -> str:
    """
    Build the in-context learning prompt from few-shot examples.
    
    Note: Schema is only included in the FIRST example to avoid redundancy.
    """
    prompt_parts = []
    
    for i, example in enumerate(examples):
        text = example['text']
        
        # Only include schema in first example
        use_schema = include_schema and (i == 0)
        
        if style == "pl":
            entities = example.get('spot_asoc', [])
            example_prompt = build_code_style_prompt(
                text=text,
                entities=entities,
                config=variation_config,
                entity_types=entity_types,
                entity_definitions=entity_definitions,
                include_schema=use_schema,
                include_output=True
            )
        else:
            record = example.get('record', '')
            example_prompt = build_nl_style_prompt(
                text=text,
                record=record,
                config=variation_config,
                entity_types=entity_types,
                include_schema=use_schema,
                include_output=True
            )
        
        prompt_parts.append(example_prompt)
        prompt_parts.append(END)
        prompt_parts.append("")  # Empty line between examples
    
    return '\n'.join(prompt_parts)


# ============================================================================
# Inference & Parsing
# ============================================================================

def get_llm_model(config: ExperimentConfig):
    """
    Factory to get the appropriate LangChain chat model based on config.
    """
    # Resolve parameters from config or environment variables
    model_name = config.model_name or os.getenv("CUSTOM_MODEL_NAME", "qwen2.5-7b")
    
    # Resolve API Key
    api_key = config.api_key
    if not api_key:
        api_key = os.getenv("CUSTOM_API_KEY") 
        if not api_key:
            api_key = "not-needed"

    # Resolve Base URL (checking multiple env vars)
    api_base_url = config.api_base_url
    if not api_base_url:
        api_base_url = os.getenv("CUSTOM_API_BASE_URL") or os.getenv("CUSTOM_API_BASE")
        if not api_base_url:
            api_base_url = "http://localhost:11434"

    # Check if Google Model
    if "gemini" in model_name.lower():
        if not api_key or api_key == "not-needed":
            # Try to find standard Google env var
            api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            logging.warning("No API key found for Google model. set CUSTOM_API_KEY or GOOGLE_API_KEY.")
            
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=config.temperature,
            google_api_key=api_key,
            max_output_tokens=config.max_tokens,
            convert_system_message_to_human=True # Sometimes needed for Gemini
        )
    
    # Determine which Ollama wrapper to use
    chat_models = ["mistral", "llama", "gemma", "chat", "instruct", "qwen", "phi3"]
    use_chat_api = any(m in model_name.lower() for m in chat_models)
    
    if use_chat_api:
        logging.info(f"Using ChatOllama (Chat API) for {model_name}")
        return ChatOllama(
            model=model_name,
            temperature=config.temperature,
            base_url=api_base_url,
            num_predict=config.max_tokens
        )
    else:
        logging.info(f"Using OllamaLLM (Completion API) for {model_name}")
        return OllamaLLM(
            model=model_name,
            temperature=config.temperature,
            base_url=api_base_url,
            num_predict=config.max_tokens
        )

def run_inference(prompt: str, llm_model, config: ExperimentConfig) -> str:
    """Run inference using the LangChain model."""
    try:
        messages = [HumanMessage(content=prompt)]
        stop = [END, END_LINE, "\ndef ", "\n\ndef "]
        
        response = llm_model.invoke(messages, stop=stop)
        return response.content
        
    except Exception as e:
        logging.error(f"Inference failed: {e}")
        return ""


def parse_code_style_output(output: str, entity_types: List[str]) -> List[Dict]:
    """Parse code-style output to extract entities."""
    entities = []
    
    # Pattern to match entity_list.append({"text": "...", "type": "..."})
    pattern = r'entity_list\.append\(\{["\']text["\']:\s*["\']([^"\']*)["\'],\s*["\']type["\']:\s*["\']([^"\']*)["\']'
    
    # Also try reverse order
    pattern_alt = r'entity_list\.append\(\{["\']type["\']:\s*["\']([^"\']*)["\'],\s*["\']text["\']:\s*["\']([^"\']*)["\']'
    
    for match in re.finditer(pattern, output):
        text, entity_type = match.groups()
        if entity_type in entity_types and text:
            entities.append({'text': text, 'type': entity_type})
    
    for match in re.finditer(pattern_alt, output):
        entity_type, text = match.groups()
        if entity_type in entity_types and text:
            entities.append({'text': text, 'type': entity_type})
    
    return entities


def parse_nl_style_output(output: str, text: str, entity_types: List[str]) -> List[Dict]:
    """Parse NL-style output to extract entities. Supports both SEL (<0> type <5> text) and (type: text) formats."""
    entities = []
    
    # 1. Try parsing (type: text) format (New CodeIE format)
    # The model may output entities on multiple lines or with extra content
    # Pattern matches (type: text) where text can contain anything except unbalanced parens
    # We process line by line to handle multi-line outputs better
    
    # More robust pattern: Find all (key: value) patterns
    # This pattern allows for entity types with hyphens and captures text until closing paren
    pattern_new = r'\(([a-zA-Z][a-zA-Z0-9\-/]+):\s*([^)]+)\)'
    
    matches_new = list(re.finditer(pattern_new, output))
    if matches_new:
        for match in matches_new:
            entity_type = match.group(1).strip()
            entity_text = match.group(2).strip()
            
            # Normalize: match entity type case-insensitively
            matched_type = None
            for et in entity_types:
                if et.lower() == entity_type.lower():
                    matched_type = et
                    break
            
            if matched_type:
                entities.append({'text': entity_text, 'type': matched_type})
        
        if entities:
            return entities

    # 2. Fallback to parsing SEL format: <0> type <5> span <1> (Old format)
    # Clean up output
    output_clean = output.replace('<extra_id_', '<').replace('>', '>')
    pattern = r'<0>\s*(\w+(?:\s+\w+)*)\s*<5>\s*([^<]+?)\s*<1>'
    
    for match in re.finditer(pattern, output_clean):
        entity_type = match.group(1).strip().lower().replace(' ', '-')
        entity_text = match.group(2).strip()
        
        if entity_type in entity_types and entity_text:
            entities.append({'text': entity_text, 'type': entity_type})
    
    return entities

# ============================================================================
# Evaluation
# ============================================================================

# Import from dedicated evaluation module for macro F1 support
from evaluation import evaluate_predictions, evaluate_ner, EvaluationResult


# ============================================================================
# Main Experiment Loop
# ============================================================================

def run_experiment(config: ExperimentConfig):
    """Run a complete NER experiment with CodeIE."""
    logging.info("="*60)
    logging.info("CodeIE NER Experiment (Enhanced with Entity Schema)")
    logging.info("="*60)
    logging.info(f"Granularity: {config.granularity}")
    logging.info(f"Style: {config.style}")
    logging.info(f"Variation: {config.variation}")
    logging.info(f"Model: {config.model_name}")
    logging.info("="*60)
    
    # Setup output directory
    output_dir = os.path.join(CODEIE_ROOT, config.output_dir)
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize the Model
    llm_model = get_llm_model(config)
    
    # Load prompt variations and entity definitions
    CODE_STYLE_VARIATIONS, NL_STYLE_VARIATIONS, ENTITY_DEFINITIONS = load_variations(
        config.granularity
    )
    
    # Get variation config (with fallback handling)
    if config.style == "pl":
        available_variations = list(CODE_STYLE_VARIATIONS.keys())
        variation_config = CODE_STYLE_VARIATIONS.get(config.variation)
        if not variation_config:
            # Try fallback to 'default'
            if 'default' in CODE_STYLE_VARIATIONS:
                logging.warning(f"Variation '{config.variation}' not found, using 'default' instead")
                logging.info(f"Available PL variations: {available_variations}")
                variation_config = CODE_STYLE_VARIATIONS['default']
                config.variation = 'default'
            else:
                raise ValueError(
                    f"Unknown code-style variation: {config.variation}. "
                    f"Available: {available_variations}"
                )
    else:
        available_variations = list(NL_STYLE_VARIATIONS.keys())
        variation_config = NL_STYLE_VARIATIONS.get(config.variation)
        if not variation_config:
            # Try fallback to 'default'
            if 'default' in NL_STYLE_VARIATIONS:
                logging.warning(f"Variation '{config.variation}' not found, using 'default' instead")
                logging.info(f"Available NL variations: {available_variations}")
                variation_config = NL_STYLE_VARIATIONS['default']
                config.variation = 'default'
            else:
                raise ValueError(
                    f"Unknown NL-style variation: {config.variation}. "
                    f"Available: {available_variations}"
                )
    
    # Get entity types and definitions
    entity_types = list(ENTITY_DEFINITIONS.keys())
    entity_definitions = ENTITY_DEFINITIONS
    
    logging.info(f"Entity types ({len(entity_types)}): {entity_types}")
    
    # Load test data
    tag_key = 'ner_tags' if config.granularity == 'coarse' else 'fine_ner_tags'
    test_path = os.path.join(PROJECT_ROOT, 'few-nerd_test')
    
    logging.info(f"Loading test data from: {test_path}")
    ds_test = load_from_disk(test_path)
    
    # Determine ICL prompt source (check base prompts first!)
    icl_prompt = None
    prompt_source = "dynamic"  # Track where prompt came from
    
    # Option 1: Use explicitly provided prompt path
    if config.prompt_path and os.path.exists(config.prompt_path):
        logging.info(f"Loading pre-generated prompt from: {config.prompt_path}")
        with open(config.prompt_path, 'r') as f:
            icl_prompt = f.read()
        prompt_source = "custom"
    
    # Option 2: Use base prompt files from prompts/base/
    if icl_prompt is None:
        base_prompt_file = os.path.join(
            CODEIE_ROOT, "prompts", "base",
            f"{config.granularity}_{config.style}_1shot.txt"
        )
        
        if os.path.exists(base_prompt_file):
            logging.info(f"Using base prompt from: {base_prompt_file}")
            with open(base_prompt_file, 'r') as f:
                icl_prompt = f.read()
            prompt_source = "base"
    
    # No base prompt found - error out
    if icl_prompt is None:
        logging.error(f"Base prompt not found: {base_prompt_file}")
        logging.error("Please ensure prompts/base/ directory contains the required prompt files.")
        logging.error(f"Expected file: {config.granularity}_{config.style}_1shot.txt")
        return None
    
    logging.info(f"ICL prompt length: {len(icl_prompt)} characters")
    
    # Show sample of the prompt for verification
    logging.info("Sample ICL prompt (first 1000 chars):")
    logging.info("-" * 40)
    for line in icl_prompt[:1000].split('\n'):
        logging.info(line)
    logging.info("-" * 40)
    
    # Prepare results storage
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_tag = config.model_name or "default_model"
    
    # Filename format: simpler since base prompts are always 1-shot
    result_file = os.path.join(
        output_dir,
        f"{config.granularity}_{config.style}_{model_tag}_{timestamp}.json"
    )
    
    all_gold = []
    all_pred = []
    sentence_results = []
    
    # Determine test samples to process
    num_samples = len(ds_test)
    if config.max_test_samples:
        num_samples = min(num_samples, config.max_test_samples)
    
    logging.info(f"Processing {num_samples} test samples...")
    
    tag_names = ds_test.features[tag_key].feature.names
    
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
        # When using base prompts, use simple format matching the base prompt structure
        if config.style == "pl":
            # Code style: just the function signature with text
            test_prompt = f'def named_entity_recognition(input_text="{text}"):\n    entity_list = []\n'
        else:
            # NL style: matches the base prompt format
            test_prompt = f'The text is "{text}". The named entities in the text:'
        
        # Full prompt = ICL + test input
        full_prompt = icl_prompt + "\n" + test_prompt
        
        # Run inference
        start_time = time.time()
        generated = run_inference(full_prompt, llm_model, config)
        elapsed = time.time() - start_time
        
        # Parse output
        if config.style == "pl":
            # Append generated output to prompt to provide context for parsing if needed, 
            # but usually output is enough if it matches expected format.
            # CodeIE parser might expect full code or just the appended part.
            # Re-checking parse_code_style_output: it regexes for entity_list.append.
            # So generated part is what matters.
            # Wait, the parser regex is:
            # entity_list.append({"text": "...", "type": "..."})
            # Generated output from recent models usually continues the code.
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
        
        # Calculate per-sentence score
        sentence_eval = evaluate_ner([gold_entities], [pred_entities], entity_types)
        
        sentence_result = {
            'index': i,
            'timestamp': datetime.now().isoformat(),
            'text': text,
            'gold': [f"{e['type']}(span='{e['text']}')" for e in gold_entities],
            'prediction': [f"{e['type']}(span='{e['text']}')" for e in pred_entities],
            'generated_raw': generated[:500],  # Truncate for logging
            'elapsed_time': elapsed,
            'score': {
                'entities': {
                    'precision': sentence_eval.micro_precision,
                    'recall': sentence_eval.micro_recall,
                    'f1-score': sentence_eval.micro_f1,
                    'class_scores': {
                        etype: {
                            'tp': m.tp,
                            'total_pos': m.support,  # Gold count for this type
                            'total_pre': m.tp + m.fp,  # Predicted count for this type
                            'precision': m.precision,
                            'recall': m.recall,
                            'f1-score': m.f1
                        }
                        for etype, m in sentence_eval.per_type_metrics.items()
                        if m.support > 0 or m.tp + m.fp > 0  # Only include types with activity
                    }
                }
            }
        }
        sentence_results.append(sentence_result)
        
        # Periodic logging and saving
        if (i + 1) % 10 == 0 or i == num_samples - 1:
            current_eval = evaluate_ner(all_gold, all_pred, entity_types)
            logging.info(
                f"Progress: {i+1}/{num_samples} | "
                f"P: {current_eval.micro_precision:.4f} | "
                f"R: {current_eval.micro_recall:.4f} | "
                f"Micro-F1: {current_eval.micro_f1:.4f} | "
                f"Macro-F1: {current_eval.macro_f1:.4f}"
            )
            
            # Build overall class scores
            overall_class_scores = {
                etype: {
                    'tp': m.tp,
                    'total_pos': m.support,
                    'total_pre': m.tp + m.fp,
                    'precision': m.precision,
                    'recall': m.recall,
                    'f1-score': m.f1
                }
                for etype, m in current_eval.per_type_metrics.items()
                if m.support > 0 or m.tp + m.fp > 0
            }
            
            # Save intermediate results (GoLLIE-compatible format)
            results = {
                'module': f"codeie_{config.granularity}_{config.style}_{config.variation}",
                'timestamp': timestamp,
                'config': asdict(config),
                'entity_types': entity_types,
                'overall_score': {
                    'entities': {
                        'precision': current_eval.micro_precision,
                        'recall': current_eval.micro_recall,
                        'micro_f1': current_eval.micro_f1,
                        'macro_f1': current_eval.macro_f1,
                        'f1-score': current_eval.micro_f1,  # Alias for compatibility
                        'class_scores': overall_class_scores
                    }
                },
                'processed_count': len(sentence_results),
                'sentences': sentence_results
            }
            with open(result_file, 'w') as f:
                json.dump(results, f, indent=2)
    
    # Final evaluation
    final_eval = evaluate_ner(all_gold, all_pred, entity_types)
    final_metrics = evaluate_predictions(all_gold, all_pred)  # For backwards compatibility
    
    logging.info("="*60)
    logging.info("Final Results")
    logging.info("="*60)
    logging.info(f"Precision:  {final_eval.micro_precision:.4f}")
    logging.info(f"Recall:     {final_eval.micro_recall:.4f}")
    logging.info(f"Micro F1:   {final_eval.micro_f1:.4f}")
    logging.info(f"Macro F1:   {final_eval.macro_f1:.4f}")
    logging.info("-"*40)
    logging.info("Per-Type F1 Scores:")
    for etype, m in sorted(final_eval.per_type_metrics.items()):
        if m.support > 0:
            logging.info(f"  {etype:<30} F1: {m.f1:.4f} (P: {m.precision:.4f}, R: {m.recall:.4f})")
    logging.info("-"*40)
    logging.info(f"Results saved to: {result_file}")
    logging.info("="*60)
    
    return final_metrics


def main():
    parser = argparse.ArgumentParser(description="Run CodeIE NER experiments")
    
    # Dataset settings
    parser.add_argument('--granularity', choices=['coarse', 'fine'], default='coarse',
                        help="Entity granularity")
    # num_shots and seed removed - base prompts are always 1-shot
    parser.add_argument('--max_test', type=int, default=None,
                        help="Maximum test samples (for debugging)")
    
    # Prompt settings
    parser.add_argument('--style', choices=['pl', 'nl'], default='pl',
                        help="Prompt style: pl (code) or nl (natural language)")
    parser.add_argument('--variation', default='default',
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
        # Load variations
        CODE_STYLE_VARIATIONS, NL_STYLE_VARIATIONS, _ = load_variations(args.granularity)
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
