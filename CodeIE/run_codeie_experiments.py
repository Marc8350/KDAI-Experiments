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
import csv
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
EXPERIMENT_MATRIX_FILE = "experiment_matrix.csv"


def update_experiment_matrix(
    output_dir: str,
    config: 'ExperimentConfig',
    results: Dict,
    result_file: str
) -> None:
    """Update the experiment matrix CSV with a new run's results."""
    matrix_path = os.path.join(output_dir, EXPERIMENT_MATRIX_FILE)
    
    # Base columns
    base_columns = [
        'datetime',
        'granularity',
        'style', 
        'variation',
        'model',
        'n_samples',
        'precision',
        'recall',
        'micro_f1',
        'macro_f1',
        'result_file'
    ]
    
    # Extract overall scores from nervaluate (strict mode)
    nervaluate_data = results.get('overall_score', {}).get('nervaluate', {})
    overall_strict = nervaluate_data.get('overall', {}).get('strict', {})
    by_tag = nervaluate_data.get('by_tag', {})
    macro = nervaluate_data.get('macro', {})
    
    # Prepare row data using nervaluate strict scores
    row = {
        'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'granularity': config.granularity,
        'style': config.style,
        'variation': config.variation or 'base',
        'model': config.model_name or 'default',
        'n_samples': results.get('processed_count', 0),
        'precision': round(overall_strict.get('precision', 0), 4),
        'recall': round(overall_strict.get('recall', 0), 4),
        'micro_f1': round(overall_strict.get('f1', 0), 4),
        'macro_f1': round(macro.get('strict', 0), 4),
        'result_file': os.path.basename(result_file)
    }
    
    # Add class scores from nervaluate by_tag (strict mode)
    for class_name, metrics in by_tag.items():
        col_name = f"f1_{class_name}"
        strict_metrics = metrics.get('strict', {}) if isinstance(metrics, dict) else {}
        row[col_name] = round(strict_metrics.get('f1', 0), 4)

    # Determine columns for this run
    # Start with base columns, then add any class f1 columns found in this run
    current_class_cols = [k for k in row.keys() if k.startswith('f1_')]
    current_columns = base_columns + sorted(current_class_cols)
    
    # Handle CSV file update
    if os.path.exists(matrix_path):
        # Read existing header
        existing_header = []
        with open(matrix_path, 'r', newline='') as f:
            reader = csv.reader(f)
            try:
                existing_header = next(reader)
            except StopIteration:
                pass
        
        if not existing_header:
             # Empty file, treat as new
             all_columns = current_columns
             rewrite = True
             existing_rows = []
        else:
            # Determine if we have new columns
            all_columns = list(existing_header)
            rewrite = False
            for col in current_columns:
                if col not in all_columns:
                    all_columns.append(col)
                    rewrite = True
            
            if rewrite:
                logging.info(f"Updating experiment matrix header with new columns...")
                # Read all existing rows
                with open(matrix_path, 'r', newline='') as f:
                    reader = csv.DictReader(f)
                    existing_rows = list(reader)
            else:
                existing_rows = []

        if rewrite:
             # Write back with new header
             with open(matrix_path, 'w', newline='') as f:
                 writer = csv.DictWriter(f, fieldnames=all_columns)
                 writer.writeheader()
                 writer.writerows(existing_rows)
                 writer.writerow(row)
        else:
             # Just append
             with open(matrix_path, 'a', newline='') as f:
                 writer = csv.DictWriter(f, fieldnames=existing_header, extrasaction='ignore') 
                 # extrasaction='ignore' is safer if we decided NOT to rewrite, but here we cover all cols.
                 # However, if row has 'f1_A' and header doesn't (should be covered by rewrite logic), but just in case.
                 # Actually, if we are NOT rewriting, it means current_columns is subset of existing_header.
                 writer.writerow(row)

    else:
        # Create new file
        with open(matrix_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=current_columns)
            writer.writeheader()
            writer.writerow(row)
            
    logging.info(f"Updated experiment matrix: {matrix_path}")


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
    matrix_dir: Optional[str] = None  # Directory where experiment_matrix.csv should be saved
    prompt_path: Optional[str] = None  # Path to pre-generated prompt file
    quiet: bool = False  # Suppress non-critical logging
    skip_matrix_update: bool = False  # Skip updating the central experiment matrix CSV


def load_variations(granularity: str, style: str):
    """
    Discovery of all available variations for a given granularity and style.
    Looks in prompts/base/ and prompts/variations/{granularity}_{style}_1shot/
    """
    variations = {"default": "base"} # 'default' always maps to the base prompt
    
    # 1. Check variations directory
    var_dir = os.path.join(CODEIE_ROOT, "prompts", "variations", f"{granularity}_{style}_1shot")
    if os.path.exists(var_dir):
        for f in os.listdir(var_dir):
            if f.endswith(".txt"):
                var_name = f.replace(".txt", "")
                variations[var_name] = os.path.join(var_dir, f)
                
    # 2. Get Entity Definitions (still needed for schema building)
    if granularity == "coarse":
        from prompt_variations.coarse_prompt_variations import ENTITY_DEFINITIONS
    else:
        from prompt_variations.fine_prompt_variations import ENTITY_DEFINITIONS
        
    return variations, ENTITY_DEFINITIONS


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
    lines.append('\t# Continue by adding entity_list.append statements for each named entity found:')
    
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


def build_base_prompt(
    examples: List[Dict],
    style: str,
    variation_config: Any,
    entity_types: List[str],
    entity_definitions: Dict[str, str],
    include_schema: bool = True
) -> str:
    """
    Build the few-shot base prompt from examples.
    
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

# Default timeout for Ollama requests (seconds)
DEFAULT_OLLAMA_TIMEOUT = 180  # 3 minutes per request
DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_RETRY_BACKOFF = 2.0  # Exponential backoff multiplier


def get_llm_model(config: ExperimentConfig, timeout: int = DEFAULT_OLLAMA_TIMEOUT):
    """
    Factory to get the appropriate LangChain chat model based on config.
    
    Args:
        config: Experiment configuration
        timeout: Request timeout in seconds (for Ollama)
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
        logging.info(f"Using ChatOllama (Chat API) for {model_name} with timeout={timeout}s")
        return ChatOllama(
            model=model_name,
            temperature=config.temperature,
            base_url=api_base_url,
            num_predict=config.max_tokens,
            timeout=timeout,  # Request timeout
        )
    else:
        logging.info(f"Using OllamaLLM (Completion API) for {model_name} with timeout={timeout}s")
        return OllamaLLM(
            model=model_name,
            temperature=config.temperature,
            base_url=api_base_url,
            num_predict=config.max_tokens,
            timeout=timeout,  # Request timeout
        )

def run_inference(
    prompt: str, 
    llm_model, 
    config: ExperimentConfig, 
    timeout: int = DEFAULT_OLLAMA_TIMEOUT,
    max_retries: int = DEFAULT_RETRY_ATTEMPTS,
    backoff_factor: float = DEFAULT_RETRY_BACKOFF,
    health_check_callback=None
) -> str:
    """
    Run inference using the LangChain model with thread-based timeout and retry logic.
    
    This implementation uses ThreadPoolExecutor for timeouts, which works correctly
    in subprocess workers (unlike signal.SIGALRM which only works in main thread).
    
    Args:
        prompt: Input prompt
        llm_model: LangChain model instance
        config: Experiment config
        timeout: Maximum seconds to wait for response
        max_retries: Number of retry attempts on failure
        backoff_factor: Multiplier for exponential backoff between retries
        health_check_callback: Optional callable to check/restart Ollama on failure
    
    Returns:
        Generated text or empty string on failure/timeout
    """
    from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
    
    def _invoke():
        """Inner function to run in thread with timeout."""
        messages = [HumanMessage(content=prompt)]
        # Add common stop sequences to keep output clean
        stop = [END, END_LINE, "\ndef ", "\n\ndef "]
        return llm_model.invoke(messages, stop=stop)
    
    last_error = None
    
    for attempt in range(max_retries):
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(_invoke)
                try:
                    response = future.result(timeout=timeout)
                    
                    if hasattr(response, 'content'):
                        return response.content
                    return str(response)
                    
                except FuturesTimeoutError:
                    last_error = f"Inference timeout after {timeout}s (attempt {attempt + 1}/{max_retries})"
                    logging.warning(last_error)
                    
                    # Try health check/recovery if provided
                    if health_check_callback and attempt < max_retries - 1:
                        logging.info("Triggering health check after timeout...")
                        health_check_callback()
                    
        except Exception as e:
            last_error = f"Inference failed (attempt {attempt + 1}/{max_retries}): {e}"
            logging.warning(last_error)
            
            # Try health check/recovery if provided
            if health_check_callback and attempt < max_retries - 1:
                logging.info("Triggering health check after error...")
                health_check_callback()
        
        # Exponential backoff before retry (except on last attempt)
        if attempt < max_retries - 1:
            wait_time = backoff_factor ** attempt
            logging.info(f"Retrying in {wait_time:.1f}s...")
            time.sleep(wait_time)
    
    logging.error(f"All {max_retries} inference attempts failed. Last error: {last_error}")
    return ""


def match_entity_type(etype_raw: str, entity_types: List[str]) -> Optional[str]:
    """
    Robustly match a raw entity type string to a list of allowed types.
    Handles:
    1. Exact match (case-insensitive)
    2. Underscore/Dash normalization
    3. Suffix matching (e.g. 'product-hotel' -> 'building-hotel')
    4. Prefix matching (e.g. 'location' -> 'location-GPE')
    """
    if not etype_raw:
        return None
        
    etype_norm = etype_raw.strip().lower().replace("_", "-")
    
    # 1. Exact or normalized matching
    for t in entity_types:
        if t.lower() == etype_norm:
            return t

    # 2. Suffix Fallback (e.g. 'product-hotel' -> 'building-hotel')
    # Use only if the raw type has a hyphen (indicating it's trying to be specific)
    if "-" in etype_norm:
        suffix = etype_norm.split("-")[-1]
        for t in entity_types:
            if t.lower().endswith("-" + suffix):
                return t

    # 3. Prefix Fallback (e.g. 'location' -> 'location-GPE')
    # Use if the raw type is just a base category or if above failed
    # But try to match the base category
    if "-" not in etype_norm:
        for t in entity_types:
            if t.lower().startswith(etype_norm + "-"):
                return t
    else:
        # Also try base category of a hyphenated type
        base_cat = etype_norm.split("-")[0]
        for t in entity_types:
            if t.lower().startswith(base_cat + "-"):
                return t
                
    return None

def parse_code_style_output(output: str, entity_types: List[str]) -> List[Dict]:
    """Parse code-style output to extract entities, handling Markdown blocks."""
    entities = []
    
    # Clean up output: remove Markdown code blocks if present
    clean_output = output
    if "```" in output:
        # Try to extract content inside ```python ... ``` or just ``` ... ```
        code_blocks = re.findall(r'```(?:python)?(.*?)```', output, re.DOTALL)
        if code_blocks:
            clean_output = "\n".join(code_blocks)

    # Regex patterns to match entity_list.append(...)
    # Improved patterns: handles varying whitespace, quote types, and key order
    patterns = [
        # Standard: {"text": "...", "type": "..."}
        r'entity_list\.append\(\s*\{\s*["\']text["\']\s*:\s*["\'](.*?)["\']\s*,\s*["\']type["\']\s*:\s*["\'](.*?)["\']\s*\}\s*\)',
        # Reverse: {"type": "...", "text": "..."}
        r'entity_list\.append\(\s*\{\s*["\']type["\']\s*:\s*["\'](.*?)["\']\s*,\s*["\']text["\']\s*:\s*["\'](.*?)["\']\s*\}\s*\)',
        # Simple dict: dict(text="...", type="...")
        r'entity_list\.append\(\s*dict\(\s*text\s*=\s*["\'](.*?)["\']\s*,\s*type\s*=\s*["\'](.*?)["\']\s*\)\s*\)',
        # Simple dict reverse: dict(type="...", text="...")
        r'entity_list\.append\(\s*dict\(\s*type\s*=\s*["\'](.*?)["\']\s*,\s*text\s*=\s*["\'](.*?)["\']\s*\)\s*\)',
        # Even more robust JSON-like: {"text": "...", "type": "..."}
        r'\{\s*["\']text["\']\s*:\s*["\'](.*?)["\']\s*,\s*["\']type["\']\s*:\s*["\'](.*?)["\']\s*\}',
        r'\{\s*["\']type["\']\s*:\s*["\'](.*?)["\']\s*,\s*["\']text["\']\s*:\s*["\'](.*?)["\']\s*\}',
        # Set-based syntax: {"text", "type"} or {"type", "text"}
        # Captures two strings in a set-like structure
        r'entity_list\.append\(\s*\{\s*["\'](.*?)["\']\s*,\s*["\'](.*?)["\']\s*\}\s*\)'
    ]

    for p in patterns:
        for match in re.finditer(p, clean_output):
            groups = match.groups()
            
            # For set syntax, we don't know order, so we have to guess
            # Strategy: Check if one of the groups matches a valid entity type
            if "{" in p and "text" not in p: 
                val1, val2 = groups
                # Check if val1 is type
                if match_entity_type(val1, entity_types):
                    etype, text = val1, val2
                # Check if val2 is type
                elif match_entity_type(val2, entity_types):
                    etype, text = val2, val1
                else:
                    # Heuristic: Uppercase/spaces usually mean text; lowercase/hyphens usually mean type
                    # But safer to fail if we can't identify a type
                    continue
            # Determine which group is text and which is type based on pattern structure
            elif "type" in p.split("text")[0]: # type comes first
                etype, text = groups
            else: # text comes first
                text, etype = groups
            
            # Normalize and check type
            matched_type = match_entity_type(etype, entity_types)
            
            if matched_type and text:
                # Avoid duplicates
                if not any(e['text'] == text and e['type'] == matched_type for e in entities):
                    entities.append({'text': text, 'type': matched_type})

    return entities


def parse_nl_style_output(output: str, text: str, entity_types: List[str]) -> List[Dict]:
    """Parse NL-style output to extract entities. Supports both SEL (<0> type <5> text) and (type: text) formats."""
    entities = []
    
    # 1. Try parsing bullet list or line-based format (New CodeIE format)
    # Handles: "* type: text", "- type: text", "type: text", etc.
    lines = output.split('\n')
    for line in lines:
        line = line.strip()
        if not line: continue
        
        m = re.match(r'^(?:[*•-]\s*)?(?:\*\*)?([a-zA-Z0-9\-/]+)(?:\*\*)?:\s*(.*)', line)
        if m:
            etype_raw = m.group(1).strip()
            etext = m.group(2).strip()
            
            matched_type = match_entity_type(etype_raw, entity_types)
            
            if matched_type and etext:
                entities.append({'text': etext, 'type': matched_type})
    
    if entities:
        return entities

    # 2. Try parsing (type: text) format
    # Non-greedy match for text inside parens to avoid capturing trailing content
    pattern_paren = r'\(([a-zA-Z][a-zA-Z0-9\-/]+):\s*([^)]+?)\)'
    for match in re.finditer(pattern_paren, output):
        etype_raw = match.group(1).strip()
        etext = match.group(2).strip()
        matched_type = match_entity_type(etype_raw, entity_types)

        if matched_type:
            entities.append({'text': etext, 'type': matched_type})
            
    if entities:
        return entities

    # 3. Fallback to SEL format: <0> type <5> span <1>
    output_clean = output.replace('<extra_id_', '<').replace('>', '>')
    pattern_sel = r'<0>\s*([^<]+)\s*<5>\s*([^<]+)\s*<1>'
    for match in re.finditer(pattern_sel, output_clean):
        etype_raw = match.group(1).strip().replace(' ', '-')
        etext = match.group(2).strip()
        matched_type = match_entity_type(etype_raw, entity_types)

        if matched_type:
            entities.append({'text': etext, 'type': matched_type})
    
    return entities

# ============================================================================
# Evaluation
# ============================================================================

# Import from dedicated evaluation module (nervaluate only)
from src.evaluation_nervaluate import evaluate_with_nervaluate


def normalize_nervaluate_by_tag(by_tag: Dict[str, Any]) -> Dict[str, Any]:
    """Convert nervaluate per-tag metrics into JSON-serializable dicts."""
    normalized: Dict[str, Any] = {}
    for tag, metrics in by_tag.items():
        tag_dict: Dict[str, Any] = {}
        for scheme, scheme_metrics in metrics.items():
            if isinstance(scheme_metrics, dict):
                tag_dict[scheme] = scheme_metrics
            else:
                tag_dict[scheme] = {
                    'precision': getattr(scheme_metrics, 'precision', 0.0),
                    'recall': getattr(scheme_metrics, 'recall', 0.0),
                    'f1': getattr(scheme_metrics, 'f1', 0.0),
                    'correct': getattr(scheme_metrics, 'correct', 0),
                    'incorrect': getattr(scheme_metrics, 'incorrect', 0),
                    'partial': getattr(scheme_metrics, 'partial', 0),
                    'missed': getattr(scheme_metrics, 'missed', 0),
                    'spurious': getattr(scheme_metrics, 'spurious', 0),
                    'actual': getattr(scheme_metrics, 'actual', 0),
                    'possible': getattr(scheme_metrics, 'possible', 0)
                }
        normalized[tag] = tag_dict
    return normalized


# ============================================================================
# Main Experiment Loop
# ============================================================================

def run_experiment(config: ExperimentConfig, progress_queue=None, ollama_base_url: str = None):
    """
    Run a complete NER experiment with CodeIE.
    
    Args:
        config: Experiment configuration
        progress_queue: Optional queue for progress updates (multiprocessing)
        ollama_base_url: Optional Ollama base URL for health checks
    """
    if config.quiet:
        # Suppress logging for all loggers except for the root if needed,
        # but easier to just set level to WARNING for the current module's logger
        logging.getLogger().setLevel(logging.WARNING)
    else:
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
    
    # Discovery of available variations and entity definitions
    available_variations, ENTITY_DEFINITIONS = load_variations(
        config.granularity, config.style
    )
    
    entity_types = list(ENTITY_DEFINITIONS.keys())
    entity_definitions = ENTITY_DEFINITIONS
    
    logging.info(f"Discovered variations: {list(available_variations.keys())}")
    logging.info(f"Entity types ({len(entity_types)}): {entity_types}")
    
    # Load test data
    tag_key = 'ner_tags' if config.granularity == 'coarse' else 'fine_ner_tags'
    test_path = os.path.join(PROJECT_ROOT, 'few-nerd_test')
    
    logging.info(f"Loading test data from: {test_path}")
    ds_test = load_from_disk(test_path)
    
    # Determine Prompt Source using discovered variations
    base_prompt = None
    prompt_source = "dynamic" 
    
    # Strategy 1: Explicitly provided prompt path
    if config.prompt_path and os.path.exists(config.prompt_path):
        logging.info(f"Loading custom prompt from: {config.prompt_path}")
        with open(config.prompt_path, 'r') as f:
            base_prompt = f.read()
        prompt_source = "custom"
    
    # Strategy 2: Use discovered variation (including 'default' as 'base')
    if base_prompt is None:
        var_path = available_variations.get(config.variation)
        if var_path == "base":
            # Map 'default' to binary base files
            patterns = [
                f"{config.granularity}_{config.style}_1shot.txt",
                f"{config.granularity}_{config.style}.txt"
            ]
            for p in patterns:
                base_file = os.path.join(CODEIE_ROOT, "prompts", "base", p)
                if os.path.exists(base_file):
                    logging.info(f"Using base prompt: {base_file}")
                    with open(base_file, 'r') as f:
                        base_prompt = f.read()
                    prompt_source = "base"
                    break
        elif var_path and os.path.exists(var_path):
            logging.info(f"Using variations directory prompt: {var_path}")
            with open(var_path, 'r') as f:
                base_prompt = f.read()
            prompt_source = f"variation:{config.variation}"
        else:
            logging.error(f"Variation '{config.variation}' not found in discovery.")
            return None
    
    if base_prompt is None:
        logging.error("No suitable prompt file found in prompts/base/ or prompts/variations/")
        return None
    
    logging.info(f"Base prompt loaded (Length: {len(base_prompt)})")
    
    # Show sample of the prompt for verification
    logging.info("Sample base prompt (first 1000 chars):")
    logging.info("-" * 40)
    for line in base_prompt[:1000].split('\n'):
        logging.info(line)
    logging.info("-" * 40)
    
    # Prepare results storage
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_tag = config.model_name or "default_model"
    variation_tag = config.variation or "base"
    
    # Filename includes: granularity, style, variation, model, timestamp
    result_file = os.path.join(
        output_dir,
        f"{config.granularity}_{config.style}_{variation_tag}_{model_tag}_{timestamp}.json"
    )
    
    all_gold = []
    all_pred = []
    all_texts = []
    sentence_results = []
    
    # Fail-fast tracking for empty outputs
    MAX_CONSECUTIVE_EMPTY_OUTPUTS = 10  # Crash if 10 consecutive empty model outputs
    MAX_EMPTY_OUTPUT_RATIO = 0.5        # Crash if >50% empty outputs after 20+ samples
    consecutive_empty_outputs = 0
    total_empty_outputs = 0
    
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
        
        # Build test prompt dynamically for the current sentence
        if config.style == "pl":
            # Code style: matches working unit test format with docstring and trigger comment
            test_prompt = (
                f'def named_entity_recognition(input_text):\n'
                f'    """ extract named entities from the input_text . """\n'
                f'    input_text = "{text}"\n'
                f'    entity_list = []\n'
                f'    # Continue by adding entity_list.append statements for each named entity found:'
            )
        else:
            # NL style: matches the base prompt format
            test_prompt = f'The text is "{text}". The named entities in the text:'

        # Full prompt = few-shot context + test input
        full_prompt = base_prompt + "\n" + test_prompt
        
        # Run inference
        start_time = time.time()
        generated = run_inference(full_prompt, llm_model, config)
        elapsed = time.time() - start_time
        
        # =================================================================
        # FAIL-FAST: Check for empty model outputs
        # =================================================================
        if not generated or generated.strip() == "":
            consecutive_empty_outputs += 1
            total_empty_outputs += 1
            logging.warning(f"Empty model output for sample {i} (consecutive: {consecutive_empty_outputs})")
            
            # Crash if too many consecutive empty outputs
            if consecutive_empty_outputs >= MAX_CONSECUTIVE_EMPTY_OUTPUTS:
                error_msg = (
                    f"FATAL: {MAX_CONSECUTIVE_EMPTY_OUTPUTS} consecutive empty model outputs. "
                    f"Model is not generating responses. Check Ollama server and model availability."
                )
                logging.error(error_msg)
                raise RuntimeError(error_msg)
        else:
            consecutive_empty_outputs = 0  # Reset on successful output
        
        # Check empty output ratio after sufficient samples
        samples_processed = i + 1
        if samples_processed >= 20:
            empty_ratio = total_empty_outputs / samples_processed
            if empty_ratio > MAX_EMPTY_OUTPUT_RATIO:
                error_msg = (
                    f"FATAL: {empty_ratio:.1%} of outputs are empty ({total_empty_outputs}/{samples_processed}). "
                    f"Model is failing too often. Check Ollama server health."
                )
                logging.error(error_msg)
                raise RuntimeError(error_msg)
        # =================================================================
        
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
        all_texts.append(text)
        
        # Update progress
        if progress_queue:
            progress_queue.put(1)
        
        # Calculate per-sentence score using nervaluate
        # Edge cases are handled inside evaluate_with_nervaluate
        sentence_nervaluate = evaluate_with_nervaluate(
            all_gold_entities=[gold_entities],
            all_pred_entities=[pred_entities],
            all_texts=[text],
            entity_types=entity_types
        )
        sentence_nervaluate_by_tag = normalize_nervaluate_by_tag(
            sentence_nervaluate.get('by_tag', {})
        )
        
        # Extract strict metrics for sentence result
        strict_overall = sentence_nervaluate.get('overall', {}).get('strict', {})
        
        sentence_result = {
            'index': i,
            'timestamp': datetime.now().isoformat(),
            'text': text,
            'gold': [f"{e['type']}(span='{e['text']}')" for e in gold_entities],
            'prediction': [f"{e['type']}(span='{e['text']}')" for e in pred_entities],
            'generated_raw': generated[:500],  # Truncate for logging
            'elapsed_time': elapsed,
            'score': {
                'nervaluate': {
                    'overall': sentence_nervaluate.get('overall', {}),
                    'macro': sentence_nervaluate.get('macro', {}),
                    'by_tag': sentence_nervaluate_by_tag
                }
            }
        }
        sentence_results.append(sentence_result)
        
        # Periodic logging and saving
        if (i + 1) % 10 == 0 or i == num_samples - 1:
            current_nervaluate = evaluate_with_nervaluate(
                all_gold_entities=all_gold,
                all_pred_entities=all_pred,
                all_texts=all_texts,
                entity_types=entity_types
            )
            current_nervaluate_by_tag = normalize_nervaluate_by_tag(
                current_nervaluate.get('by_tag', {})
            )
            
            # Extract strict metrics for logging
            curr_strict = current_nervaluate.get('overall', {}).get('strict', {})
            curr_macro = current_nervaluate.get('macro', {}).get('strict', 0.0)
            
            logging.info(
                f"Progress: {i+1}/{num_samples} | "
                f"P: {curr_strict.get('precision', 0):.4f} | "
                f"R: {curr_strict.get('recall', 0):.4f} | "
                f"Micro-F1: {curr_strict.get('f1', 0):.4f} | "
                f"Macro-F1: {curr_macro:.4f}"
            )
            
            # Save intermediate results (nervaluate only)
            results = {
                'module': f"codeie_{config.granularity}_{config.style}_{config.variation}",
                'timestamp': timestamp,
                'config': asdict(config),
                'entity_types': entity_types,
                'overall_score': {
                    'nervaluate': {
                        'overall': current_nervaluate.get('overall', {}),
                        'macro': current_nervaluate.get('macro', {}),
                        'by_tag': current_nervaluate_by_tag
                    }
                },
                'processed_count': len(sentence_results),
                'sentences': sentence_results
            }
            with open(result_file, 'w') as f:
                json.dump(results, f, indent=2)
    
    # Final evaluation using nervaluate only
    final_nervaluate = evaluate_with_nervaluate(
        all_gold_entities=all_gold,
        all_pred_entities=all_pred,
        all_texts=all_texts,
        entity_types=entity_types
    )
    final_nervaluate_by_tag = normalize_nervaluate_by_tag(
        final_nervaluate.get('by_tag', {})
    )
    
    # Extract strict metrics for logging
    strict_overall = final_nervaluate.get('overall', {}).get('strict', {})
    macro_strict = final_nervaluate.get('macro', {}).get('strict', 0.0)
    
    logging.info("="*60)
    logging.info("Final Results (nervaluate strict)")
    logging.info("="*60)
    logging.info(f"Precision:  {strict_overall.get('precision', 0):.4f}")
    logging.info(f"Recall:     {strict_overall.get('recall', 0):.4f}")
    logging.info(f"Micro F1:   {strict_overall.get('f1', 0):.4f}")
    logging.info(f"Macro F1:   {macro_strict:.4f}")
    logging.info("-"*40)
    logging.info("Per-Type F1 Scores (strict):")
    for etype, metrics in sorted(final_nervaluate_by_tag.items()):
        strict = metrics.get('strict', {}) if isinstance(metrics, dict) else {}
        f1 = strict.get('f1', 0) if isinstance(strict, dict) else 0
        p = strict.get('precision', 0) if isinstance(strict, dict) else 0
        r = strict.get('recall', 0) if isinstance(strict, dict) else 0
        possible = strict.get('possible', 0) if isinstance(strict, dict) else 0
        if possible > 0 or f1 > 0:
            logging.info(f"  {etype:<30} F1: {f1:.4f} (P: {p:.4f}, R: {r:.4f})")
    logging.info("-"*40)
    logging.info(f"Results saved to: {result_file}")
    logging.info("="*60)
    
    # Build final_results using nervaluate only
    final_results = {
        'overall_score': {
            'nervaluate': {
                'overall': final_nervaluate.get('overall', {}),
                'macro': final_nervaluate.get('macro', {}),
                'by_tag': final_nervaluate_by_tag
            }
        },
        'processed_count': len(all_gold)
    }
    
    # Use config.matrix_dir if provided, otherwise fallback to output_dir
    if config.matrix_dir:
        if os.path.isabs(config.matrix_dir):
            matrix_save_dir = config.matrix_dir
        else:
            matrix_save_dir = os.path.join(CODEIE_ROOT, config.matrix_dir)
    else:
        matrix_save_dir = output_dir
    
    # Ensure matrix directory exists
    os.makedirs(matrix_save_dir, exist_ok=True)
    
    if not config.skip_matrix_update:
        update_experiment_matrix(matrix_save_dir, config, final_results, result_file)
    
    final_metrics['result_file'] = result_file
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
        # Discover all variations for this style
        variations, _ = load_variations(args.granularity, args.style)
        
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
