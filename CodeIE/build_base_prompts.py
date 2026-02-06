#!/usr/bin/env python3
"""
Build Base Prompts from Few-Shot Examples

This script creates the 4 base prompts from the few-shot training examples:
- coarse_pl_3shot.txt (code style, coarse-grained)
- coarse_nl_3shot.txt (NL style, coarse-grained)  
- fine_pl_3shot.txt (code style, fine-grained)
- fine_nl_3shot.txt (NL style, fine-grained)

Each prompt uses 3 examples per entity class from the stratified samples.
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any

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


# Entity definitions for schema block
COARSE_ENTITY_DEFINITIONS = {
    "person": "A named individual, including fictional characters, historical figures, celebrities, and common people.",
    "location": "A geographical location such as a city, country, continent, region, or landmark.",
    "organization": "A named organization, institution, company, or group.",
    "building": "A named structure or building, such as a stadium, museum, or hotel.",
    "art": "A work of art including films, books, music, paintings, or other creative works.",
    "product": "A named commercial product, software, vehicle model, or branded item.",
    "event": "A named event such as a war, sports event, festival, or historical occurrence.",
    "other": "Other named entities that don't fit into the above categories."
}


def load_fewshot_examples(data_dir: Path, granularity: str, num_shots: int = 3, seed: int = 42) -> List[Dict]:
    """Load few-shot examples from the stratified samples."""
    shot_dir = data_dir / f"few-nerd-{granularity}_shot" / f"seed{seed}" / f"{num_shots}shot"
    train_path = shot_dir / "train.json"
    
    if not train_path.exists():
        raise FileNotFoundError(f"Few-shot examples not found: {train_path}")
    
    examples = []
    with open(train_path, 'r') as f:
        for line in f:
            examples.append(json.loads(line.strip()))
    
    logger.info(f"Loaded {len(examples)} few-shot examples from {train_path}")
    return examples


def load_schema(data_dir: Path, granularity: str) -> List[str]:
    """Load entity types from schema file."""
    schema_path = data_dir / f"few-nerd-{granularity}" / "entity.schema"
    
    with open(schema_path, 'r') as f:
        entity_types = [line.strip() for line in f if line.strip()]
    
    return entity_types


def build_code_style_prompt(
    examples: List[Dict],
    entity_types: List[str],
    entity_definitions: Dict[str, str] = None
) -> str:
    """
    Build a code-style (pl-func) prompt from examples.
    
    Format follows CodeIE's structure2pl_func.py style.
    """
    prompt_parts = []
    
    # Build entity schema block
    if entity_definitions:
        schema_block = "# Entity type definitions:\n"
        for etype in entity_types:
            # For fine-grained, use the main category from coarse definitions
            base_type = etype.split('-')[0] if '-' in etype else etype
            desc = entity_definitions.get(base_type, f"Entities of type {etype}")
            schema_block += f"# - {etype}: {desc}\n"
        prompt_parts.append(schema_block)
    
    # Add examples
    for example in examples:
        text = example.get("text", "")
        entities = example.get("entity", [])
        
        # Build function
        func = f'''def named_entity_recognition(input_text):
\t""" extract named entities from the input_text . """
\tinput_text = \"{text}\"
\tentity_list = []
\t# extracted named entities'''
        
        # Add entity extractions
        for entity in entities:
            entity_text = entity.get("text", "")
            entity_type = entity.get("type", "")
            func += f'\n\tentity_list.append({{"text": "{entity_text}", "type": "{entity_type}"}})'
        
        func += "\n# END"
        prompt_parts.append(func)
    
    return "\n\n".join(prompt_parts)


def build_nl_style_prompt(
    examples: List[Dict],
    entity_types: List[str]
) -> str:
    """
    Build a natural language style (nl-sel) prompt from examples.
    
    Format follows CodeIE's structure2nl_sel.py style with SEL format.
    """
    prompt_parts = []
    
    # Add schema info
    schema_str = ", ".join(entity_types)
    header = f"Entity types: {schema_str}\n"
    prompt_parts.append(header)
    
    # Add examples in SEL format
    for example in examples:
        text = example.get("text", "")
        spot_asoc = example.get("spot_asoc", [])
        
        # Build SEL-format output
        # Format: <0> type <5> span <1> ; <0> type <5> span <1>
        sel_parts = []
        for item in spot_asoc:
            label = item.get("label", "")
            span = item.get("span", "")
            sel_parts.append(f"<0> {label} <5> {span} <1>")
        
        sel_output = " ; ".join(sel_parts) if sel_parts else "<5> <1>"
        
        example_block = f'''The text is : "{text}".
The named entities in the text: {sel_output}
----------------------------------------'''
        prompt_parts.append(example_block)
    
    return "\n\n".join(prompt_parts)


def build_base_prompts(
    data_dir: Path,
    output_dir: Path,
    granularity: str,
    num_shots: int = 3,
    seed: int = 42
) -> Dict[str, Path]:
    """
    Build both code and NL style prompts for a granularity.
    
    Returns:
        Dict mapping style to output path
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load data
    examples = load_fewshot_examples(data_dir, granularity, num_shots, seed)
    entity_types = load_schema(data_dir, granularity)
    
    # Determine entity definitions
    if granularity == "coarse":
        entity_definitions = COARSE_ENTITY_DEFINITIONS
    else:
        # For fine-grained, create definitions based on coarse categories
        entity_definitions = {}
        for etype in entity_types:
            base_type = etype.split('-')[0] if '-' in etype else etype
            entity_definitions[etype] = COARSE_ENTITY_DEFINITIONS.get(
                base_type, 
                f"Entities categorized as {etype}"
            )
    
    outputs = {}
    
    # Build code-style (pl) prompt
    pl_prompt = build_code_style_prompt(examples, entity_types, entity_definitions)
    pl_path = output_dir / f"{granularity}_pl_{num_shots}shot.txt"
    with open(pl_path, 'w') as f:
        f.write(pl_prompt)
    outputs["pl"] = pl_path
    logger.info(f"Created: {pl_path}")
    
    # Build NL-style prompt
    nl_prompt = build_nl_style_prompt(examples, entity_types)
    nl_path = output_dir / f"{granularity}_nl_{num_shots}shot.txt"
    with open(nl_path, 'w') as f:
        f.write(nl_prompt)
    outputs["nl"] = nl_path
    logger.info(f"Created: {nl_path}")
    
    return outputs


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Build base prompts from few-shot examples")
    parser.add_argument(
        "--data-dir",
        type=str,
        default="CodeIE/data",
        help="Directory containing converted FewNerd data"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="CodeIE/prompts/base",
        help="Directory to save base prompts"
    )
    parser.add_argument(
        "--granularity",
        type=str,
        nargs="+",
        default=["coarse", "fine"],
        help="Granularities to process"
    )
    parser.add_argument(
        "--coarse-shots",
        type=int,
        default=3,
        help="Number of shots per class for coarse (default: 3)"
    )
    parser.add_argument(
        "--fine-shots",
        type=int,
        default=1,
        help="Number of shots per class for fine (default: 1 due to 66 types)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed used for sampling"
    )
    
    args = parser.parse_args()
    
    # Resolve paths - if relative and starting with CodeIE or data, use CODEIE_ROOT
    if args.data_dir.startswith("CodeIE/"):
        data_dir = PROJECT_ROOT / args.data_dir
    elif args.data_dir.startswith("data"):
        data_dir = CODEIE_ROOT / args.data_dir
    else:
        data_dir = Path(args.data_dir)
    
    if args.output_dir.startswith("CodeIE/"):
        output_dir = PROJECT_ROOT / args.output_dir
    elif args.output_dir.startswith("prompts"):
        output_dir = CODEIE_ROOT / args.output_dir
    else:
        output_dir = Path(args.output_dir)
    
    logger.info("=" * 60)
    logger.info("Building base prompts")
    logger.info("=" * 60)
    
    all_outputs = {}
    
    for granularity in args.granularity:
        # Use granularity-specific shot count
        num_shots = args.coarse_shots if granularity == "coarse" else args.fine_shots
        logger.info(f"\nProcessing: {granularity} ({num_shots}-shot)")
        try:
            outputs = build_base_prompts(
                data_dir=data_dir,
                output_dir=output_dir,
                granularity=granularity,
                num_shots=num_shots,
                seed=args.seed
            )
            all_outputs[granularity] = outputs
        except Exception as e:
            logger.error(f"Failed to build prompts for {granularity}: {e}")
    
    logger.info("\n" + "=" * 60)
    logger.info("Base prompts created successfully!")
    logger.info(f"Output directory: {output_dir}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
