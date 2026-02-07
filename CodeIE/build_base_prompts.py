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

FINE_ENTITY_DEFINITIONS = {
    "art-broadcastprogram": "A named television or radio program.",
    "art-film": "A named movie or film.",
    "art-music": "A named song, album, or musical composition.",
    "art-other": "Other works of art not covered by specific categories.",
    "art-painting": "A named painting or visual artwork.",
    "art-writtenart": "A named book, poem, essay, or other written work.",
    "building-airport": "A named airport or airfield.",
    "building-hospital": "A named hospital, clinic, or medical center.",
    "building-hotel": "A named hotel, motel, or resort.",
    "building-library": "A named library or archive.",
    "building-other": "Other named buildings or structures.",
    "building-restaurant": "A named restaurant, cafe, or bar.",
    "building-sportsfacility": "A named stadium, arena, or sports complex.",
    "building-theater": "A named theater or cinema.",
    "event-attack/battle/war/militaryconflict": "A named military conflict, battle, or war.",
    "event-disaster": "A named natural or man-made disaster.",
    "event-election": "A named election or political campaign.",
    "event-other": "Other named events.",
    "event-protest": "A named protest, demonstration, or strike.",
    "event-sportsevent": "A named sports competition or event.",
    "location-GPE": "A geopolitical entity such as a city, state, country, or nation.",
    "location-bodiesofwater": "A named ocean, sea, lake, river, or other body of water.",
    "location-island": "A named island or archipelago.",
    "location-mountain": "A named mountain, hill, or range.",
    "location-other": "Other named locations.",
    "location-park": "A named park, garden, or nature reserve.",
    "location-road/railway/highway/transit": "A named street, road, highway, or transit line.",
    "organization-company": "A named commercial company or business.",
    "organization-education": "A named educational institution like a university or school.",
    "organization-government/governmentagency": "A named government body or agency.",
    "organization-media/newspaper": "A named media organization or publication.",
    "organization-other": "Other named organizations.",
    "organization-politicalparty": "A named political party.",
    "organization-religion": "A named religious organization or group.",
    "organization-showorganization": "A named performing arts group or organization.",
    "organization-sportsleague": "A named sports league.",
    "organization-sportsteam": "A named sports team.",
    "other-astronomything": "A named astronomical object.",
    "other-award": "A named award or honor.",
    "other-biologything": "A named biological entity or species.",
    "other-chemicalthing": "A named chemical substance or compound.",
    "other-currency": "A named currency.",
    "other-disease": "A named disease or medical condition.",
    "other-educationaldegree": "A named academic degree.",
    "other-god": "A named deity or mythological figure.",
    "other-language": "A named language.",
    "other-law": "A named law or legal statute.",
    "other-livingthing": "A named living organism not covered elsewhere.",
    "other-medical": "Other medical terms or entities.",
    "person-actor": "A named actor or actress.",
    "person-artist/author": "A named artist, writer, or creator.",
    "person-athlete": "A named athlete or sports player.",
    "person-director": "A named film or theater director.",
    "person-other": "Other named individuals.",
    "person-politician": "A named politician or government official.",
    "person-scholar": "A named scholar, scientist, or academic.",
    "person-soldier": "A named soldier or military personnel.",
    "product-airplane": "A named aircraft model.",
    "product-car": "A named automobile model.",
    "product-food": "A named food or drink product.",
    "product-game": "A named game or video game.",
    "product-other": "Other commercial products.",
    "product-ship": "A named ship or boat.",
    "product-software": "A named software application or system.",
    "product-train": "A named train model or locomotive.",
    "product-weapon": "A named weapon or military equipment."
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
        # The schema file contains a JSON list on the first line
        try:
            first_line = f.readline().strip()
            entity_types = json.loads(first_line)
            if not isinstance(entity_types, list):
                # Fallback or error if not a list
                logger.warning(f"Schema first line is not a list: {first_line}")
                # Try reading all lines non-empty if JSON parsing failed conceptually
                f.seek(0)
                entity_types = [line.strip() for line in f if line.strip()]
        except json.JSONDecodeError:
            # Fallback for plain text list (one per line)
            f.seek(0)
            entity_types = [line.strip() for line in f if line.strip()]
    
    return entity_types


def build_code_style_prompt(
    examples: List[Dict],
    entity_types: List[str],
    entity_definitions: Dict[str, str] = None
) -> str:
    """
    Build a code-style (pl-func) prompt from examples.
    
    Structure:
    1. Task instruction (explicit code completion directive)
    2. Role assignment
    3. Annotation guidelines (in comments)
    4. Examples (Function definition + entity extraction logic)
    """
    prompt_parts = []
    
    # 1. Task Instruction (CRITICAL for model to understand it should complete code)
    prompt_parts.append("# TASK: Complete the Python code by adding entity_list.append() statements.")
    prompt_parts.append("# DO NOT explain the code. Just output the entity_list.append() lines.")
    prompt_parts.append("")
    
    # 2. Role Assignment
    prompt_parts.append("# You are an expert Named Entity Recognition (NER) system specializing in extracting entities from text.")
    prompt_parts.append("# For each input_text, identify named entities and add them using entity_list.append().")
    prompt_parts.append("")
    
    # 3. Annotation Guidelines  
    if entity_definitions:
        guidelines = ["# Entity Types:"]
        for etype in entity_types:
            # Try exact match first, then fallback to base type
            desc = entity_definitions.get(etype)
            if not desc:
                base_type = etype.split('-')[0] if '-' in etype else etype
                desc = entity_definitions.get(base_type, f"Entities of type {etype}")
            guidelines.append(f"# - {etype}: {desc}")
        prompt_parts.append("\n".join(guidelines))
    
    # Add Examples header
    prompt_parts.append("\n# Examples:")
    
    # 4. Examples
    for i, example in enumerate(examples, 1):
        text = example.get("text", "")
        entities = example.get("entity", [])
        
        # Build function structure
        func = f'''def named_entity_recognition(input_text):
    """ extract named entities from the input_text . """
    input_text = "{text}"
    entity_list = []'''
        
        # Add entity extractions
        for entity in entities:
            entity_text = entity.get("text", "")
            entity_type = entity.get("type", "")
            func += f'\n    entity_list.append({{"text": "{entity_text}", "type": "{entity_type}"}})'
        
        prompt_parts.append(func)
    
    return "\n".join(prompt_parts)


def build_nl_style_prompt(
    examples: List[Dict],
    entity_types: List[str],
    entity_definitions: Dict[str, str] = None
) -> str:
    """
    Build a natural language style (nl-sel) prompt from examples.
    
    Structure:
    1. Role assignment
    2. Annotation guidelines (text)
    3. Examples (Text + Entity list in ((type: text)) format)
    """
    prompt_parts = []
    
    # 1. Role Assignment
    prompt_parts.append("You are an expert Named Entity Recognition (NER) system specializing in extracting entities from text.")
    
    # 2. Annotation Guidelines
    guidelines = ["Annotation Guidelines:", "Extract named entities based on the following categories:"]
    
    if entity_definitions:
        for etype in entity_types:
            # Try exact match first, then fallback to base type
            desc = entity_definitions.get(etype)
            if not desc:
                base_type = etype.split('-')[0] if '-' in etype else etype
                desc = entity_definitions.get(base_type, f"Entities of type {etype}")
            guidelines.append(f"- {etype}: {desc}")
    else:
        guidelines.append(", ".join(entity_types))
        
    prompt_parts.append("\n".join(guidelines))
    
    # 3. Examples
    for example in examples:
        text = example.get("text", "")
        entities = example.get("entity", [])
        
        # Build Output Format: ((type: text)(type: text))
        entity_strs = []
        for entity in entities:
            entity_text = entity.get("text", "")
            entity_type = entity.get("type", "")
            entity_strs.append(f"({entity_type}: {entity_text})")
        
        if not entity_strs:
            # Handle empty entities if necessary, though 1-shot per class usually implies entities exist.
            # Using empty parens or something else? User didn't specify empty case.
            # Assuming typical CodeIE empty behavior or just empty list string.
            output_str = "" 
        else:
            output_str = "".join(entity_strs)
        
        # Format: The text is "Steve became CEO of Apple in 1998 .". The named entities in the text:
        example_block = f'''The text is "{text}". The named entities in the text: {output_str}'''
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
        # Use fine-grained definitions
        entity_definitions = FINE_ENTITY_DEFINITIONS
    
    outputs = {}
    
    # Build code-style (pl) prompt
    pl_prompt = build_code_style_prompt(examples, entity_types, entity_definitions)
    pl_path = output_dir / f"{granularity}_pl_{num_shots}shot.txt"
    with open(pl_path, 'w') as f:
        f.write(pl_prompt)
    outputs["pl"] = pl_path
    logger.info(f"Created: {pl_path}")
    
    # Build NL-style prompt
    nl_prompt = build_nl_style_prompt(examples, entity_types, entity_definitions)
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
