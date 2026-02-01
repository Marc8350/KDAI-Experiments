"""
CodeIE Prompt Variation Generator with Entity Schema

This script generates prompt variations for CodeIE NER experiments by:
1. Including explicit entity type definitions (like GoLLIE)
2. Varying the function docstrings and entity descriptions (like GoLLIE paraphrasing)
3. Supporting both code-style (pl-func) and natural language (nl-sel) formats

The key difference from original CodeIE is that entity classes are EXPLICITLY listed
in the prompt, giving the model clearer guidance about valid entity types.

Usage:
    python generate_codeie_prompt_variations.py --granularity coarse
    python generate_codeie_prompt_variations.py --granularity fine --generate_llm
"""

import os
import sys
import json
import argparse
from typing import Dict, List, Optional
from dataclasses import dataclass

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CODEIE_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ============================================================================
# Entity Type Definitions (with descriptions for each granularity)
# ============================================================================

# Coarse-grained entity types (8 classes)
COARSE_ENTITY_DEFINITIONS = {
    "person": "A named individual, including fictional characters, historical figures, celebrities, and common people.",
    "location": "A geographical location such as a city, country, continent, region, or landmark.",
    "organization": "A named organization, institution, company, or group.",
    "building": "A named structure or building, such as a stadium, museum, or hotel.",
    "art": "A work of art including films, books, music, paintings, or other creative works.",
    "product": "A named commercial product, software, vehicle model, or branded item.",
    "event": "A named event such as a war, sports event, festival, or historical occurrence.",
    "other": "Other named entities that don't fit into the above categories.",
}

# Fine-grained entity types (66 classes organized by coarse type)
FINE_ENTITY_DEFINITIONS = {
    # Person subtypes
    "person-actor": "An actor or actress in film, television, or theater.",
    "person-artist/author": "A creative artist, writer, or author.",
    "person-athlete": "A professional or amateur sports player.",
    "person-director": "A film, television, or theater director.",
    "person-politician": "A political figure or government official.",
    "person-scholar": "An academic, researcher, or scholar.",
    "person-soldier": "A military personnel or soldier.",
    "person-other": "Other individuals not fitting specific person categories.",
    
    # Location subtypes
    "location-GPE": "A geo-political entity like a country, state, or city.",
    "location-bodiesofwater": "A named body of water like an ocean, sea, river, or lake.",
    "location-island": "A named island or archipelago.",
    "location-mountain": "A named mountain, mountain range, or hill.",
    "location-park": "A named park, nature reserve, or recreational area.",
    "location-road/railway/highway/transit": "A named road, railway, highway, or transit route.",
    "location-other": "Other geographical locations.",
    
    # Organization subtypes
    "organization-company": "A business company or corporation.",
    "organization-education": "An educational institution like a university or school.",
    "organization-government/governmentagency": "A government body or agency.",
    "organization-media/newspaper": "A media outlet, newspaper, or broadcast company.",
    "organization-politicalparty": "A political party or movement.",
    "organization-religion": "A religious organization or denomination.",
    "organization-showorganization": "An entertainment or performance organization.",
    "organization-sportsleague": "A sports league or athletic organization.",
    "organization-sportsteam": "A named sports team.",
    "organization-other": "Other organizations.",
    
    # Building subtypes
    "building-airport": "A named airport.",
    "building-hospital": "A named hospital or medical facility.",
    "building-hotel": "A named hotel or lodging establishment.",
    "building-library": "A named library.",
    "building-restaurant": "A named restaurant or dining establishment.",
    "building-sportsfacility": "A named sports stadium, arena, or facility.",
    "building-theater": "A named theater or performance venue.",
    "building-other": "Other named buildings or structures.",
    
    # Art subtypes
    "art-broadcastprogram": "A television or radio program.",
    "art-film": "A movie or film.",
    "art-music": "A musical work, song, or album.",
    "art-painting": "A painting or visual artwork.",
    "art-writtenart": "A book, poem, or other written work.",
    "art-other": "Other works of art.",
    
    # Product subtypes
    "product-airplane": "A named aircraft or airplane model.",
    "product-car": "A named car or vehicle model.",
    "product-food": "A named food product or brand.",
    "product-game": "A named game or video game.",
    "product-ship": "A named ship or watercraft.",
    "product-software": "A named software product or application.",
    "product-train": "A named train or railway vehicle.",
    "product-weapon": "A named weapon or weapons system.",
    "product-other": "Other products.",
    
    # Event subtypes
    "event-attack/battle/war/militaryconflict": "A military conflict, battle, or attack.",
    "event-disaster": "A natural or man-made disaster.",
    "event-election": "A political election.",
    "event-protest": "A protest or demonstration.",
    "event-sportsevent": "A sports event or competition.",
    "event-other": "Other named events.",
    
    # Other subtypes
    "other-astronomything": "An astronomical object or phenomenon.",
    "other-award": "A named award or prize.",
    "other-biologything": "A biological entity such as a species or organism.",
    "other-chemicalthing": "A chemical compound or substance.",
    "other-currency": "A named currency.",
    "other-disease": "A named disease or medical condition.",
    "other-educationaldegree": "An educational degree or qualification.",
    "other-god": "A deity or god from mythology or religion.",
    "other-language": "A named language.",
    "other-law": "A named law or legal document.",
    "other-livingthing": "Other living things not covered by biologything.",
    "other-medical": "Medical terms or procedures.",
}


@dataclass
class PromptVariation:
    """A single prompt variation configuration."""
    id: str
    name: str
    # Code-style components
    function_name: str
    docstring: str
    entity_header: str  # Comment before entity definitions
    # NL-style components
    text_prefix: str
    entity_prompt: str
    # Entity descriptions (can be customized per variation)
    entity_descriptions: Optional[Dict[str, str]] = None


# ============================================================================
# Predefined Prompt Variations
# ============================================================================

def get_code_style_variations() -> List[PromptVariation]:
    """Get predefined code-style prompt variations."""
    return [
        PromptVariation(
            id="v0_original",
            name="Original CodeIE Style",
            function_name="named_entity_recognition",
            docstring="extract named entities from the input_text",
            entity_header="# Entity types to extract",
            text_prefix="",
            entity_prompt="",
        ),
        PromptVariation(
            id="v1_schema_aware",
            name="Schema-Aware Extraction",
            function_name="extract_entities",
            docstring="Identify and extract named entities from the input text based on the defined entity schema",
            entity_header="# Valid entity types for this task",
            text_prefix="",
            entity_prompt="",
        ),
        PromptVariation(
            id="v2_typed_extraction",
            name="Typed Entity Extraction",
            function_name="typed_ner",
            docstring="Perform typed named entity recognition, extracting entities according to the type definitions",
            entity_header="# Entity type definitions",
            text_prefix="",
            entity_prompt="",
        ),
        PromptVariation(
            id="v3_structured",
            name="Structured NER",
            function_name="structured_entity_extraction",
            docstring="Extract structured entity mentions from text following the entity type schema below",
            entity_header="# Recognized entity categories",
            text_prefix="",
            entity_prompt="",
        ),
        PromptVariation(
            id="v4_guided",
            name="Guided Entity Recognition",
            function_name="guided_ner",
            docstring="Identify named entities in the input text using the entity type guidelines defined below",
            entity_header="# Entity type guidelines",
            text_prefix="",
            entity_prompt="",
        ),
        PromptVariation(
            id="v5_classification",
            name="Entity Classification Style",
            function_name="classify_entities",
            docstring="Find and classify named entity mentions in the text according to the schema",
            entity_header="# Classification schema",
            text_prefix="",
            entity_prompt="",
        ),
        PromptVariation(
            id="v6_annotation",
            name="Annotation Task Style",
            function_name="annotate_entities",
            docstring="Annotate the input text with named entity labels from the allowed types",
            entity_header="# Allowed entity annotations",
            text_prefix="",
            entity_prompt="",
        ),
    ]


def get_nl_style_variations() -> List[PromptVariation]:
    """Get predefined natural language style prompt variations."""
    return [
        PromptVariation(
            id="v0_original",
            name="Original CodeIE NL Style",
            function_name="",
            docstring="",
            entity_header="",
            text_prefix='The text is : "{text}". ',
            entity_prompt="The named entities in the text: ",
        ),
        PromptVariation(
            id="v1_schema_list",
            name="Schema List Style",
            function_name="",
            docstring="",
            entity_header="",
            text_prefix='Given the entity types: {schema}\n\nText: "{text}"\n\n',
            entity_prompt="Named entities found: ",
        ),
        PromptVariation(
            id="v2_instruction",
            name="Instruction Style",
            function_name="",
            docstring="",
            entity_header="",
            text_prefix='Identify entities of types ({schema}) in: "{text}"\n\n',
            entity_prompt="Entities: ",
        ),
        PromptVariation(
            id="v3_task_description",
            name="Task Description Style",
            function_name="",
            docstring="",
            entity_header="",
            text_prefix='Task: Named Entity Recognition\nEntity Types: {schema}\nInput: "{text}"\n\n',
            entity_prompt="Output: ",
        ),
        PromptVariation(
            id="v4_detailed",
            name="Detailed Annotation Style",
            function_name="",
            docstring="",
            entity_header="",
            text_prefix='Analyze the following text for named entities.\nValid entity types are: {schema}\n\nText for analysis: "{text}"\n\n',
            entity_prompt="Identified entities: ",
        ),
    ]


# ============================================================================
# Prompt Generation Functions
# ============================================================================

def generate_entity_schema_block(
    entity_types: List[str],
    entity_definitions: Dict[str, str],
    style: str = "code",
    include_descriptions: bool = True
) -> str:
    """
    Generate the entity schema block to include in prompts.
    
    Args:
        entity_types: List of entity type names
        entity_definitions: Dict mapping type names to descriptions
        style: 'code' for Python-like or 'nl' for natural language
        include_descriptions: Whether to include entity descriptions
    
    Returns:
        Formatted schema block string
    """
    if style == "code":
        lines = []
        for entity_type in entity_types:
            if include_descriptions and entity_type in entity_definitions:
                desc = entity_definitions[entity_type]
                lines.append(f'\t# "{entity_type}": {desc}')
            else:
                lines.append(f'\t# "{entity_type}"')
        return '\n'.join(lines)
    else:  # nl style
        if include_descriptions:
            items = [f'{t} ({entity_definitions.get(t, "")})' for t in entity_types]
        else:
            items = entity_types
        return ', '.join(items)


def build_code_prompt(
    text: str,
    entity_types: List[str],
    entity_definitions: Dict[str, str],
    variation: PromptVariation,
    include_schema: bool = True
) -> str:
    """
    Build a code-style prompt with entity schema.
    
    Args:
        text: Input text to extract entities from
        entity_types: List of valid entity types
        entity_definitions: Entity type descriptions
        variation: Prompt variation configuration
        include_schema: Whether to include entity schema block
    
    Returns:
        Complete prompt string
    """
    lines = []
    
    # Function definition
    lines.append(f"def {variation.function_name}(input_text):")
    lines.append(f'\t""" {variation.docstring} """')
    
    # Entity schema (this is the enhancement over original CodeIE)
    if include_schema:
        lines.append(f'\t{variation.entity_header}')
        schema_block = generate_entity_schema_block(
            entity_types, entity_definitions, style="code"
        )
        lines.append(schema_block)
        lines.append('')  # Empty line after schema
    
    # Input text
    lines.append(f'\tinput_text = "{text}"')
    lines.append('\tentity_list = []')
    lines.append('\t# extracted named entities')
    
    return '\n'.join(lines)


def build_nl_prompt(
    text: str,
    entity_types: List[str],
    entity_definitions: Dict[str, str],
    variation: PromptVariation,
    include_schema: bool = True
) -> str:
    """
    Build a natural language style prompt with entity schema.
    
    Args:
        text: Input text to extract entities from
        entity_types: List of valid entity types
        entity_definitions: Entity type descriptions
        variation: Prompt variation configuration
        include_schema: Whether to include entity schema in prompt
    
    Returns:
        Complete prompt string (input part only)
    """
    if include_schema:
        schema_str = ', '.join(entity_types)
        text_part = variation.text_prefix.format(text=text, schema=schema_str)
    else:
        text_part = variation.text_prefix.format(text=text, schema='')
    
    return text_part + variation.entity_prompt


# ============================================================================
# LLM-based Variation Generation (following GoLLIE paraphrase methodology)
# ============================================================================

def load_env():
    """Load environment variables from .env file."""
    env_path = os.path.join(PROJECT_ROOT, '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    try:
                        key, value = line.strip().split('=', 1)
                        if (value.startswith('"') and value.endswith('"')) or \
                           (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                        os.environ[key] = value.strip()
                    except ValueError:
                        continue


def paraphrase_entity_definitions(
    entity_definitions: Dict[str, str],
    variation_id: str
) -> Dict[str, str]:
    """
    Use LLM to paraphrase entity definitions (similar to GoLLIE approach).
    
    Args:
        entity_definitions: Original entity type definitions
        variation_id: Identifier for this variation
    
    Returns:
        Paraphrased entity definitions
    """
    load_env()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not found, skipping LLM paraphrasing")
        return entity_definitions
    
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=api_key)
        
        prompt = f"""Paraphrase the following entity type definitions for a Named Entity Recognition task.

Key requirements:
- Preserve the meaning of each definition
- Use lexical substitutions and syntactic reordering only
- Maintain the same level of detail
- Keep definitions concise (1-2 sentences)
- Return as JSON with the same keys

Original definitions:
{json.dumps(entity_definitions, indent=2)}

Return ONLY the JSON object with paraphrased definitions, no other text."""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.7)
        )
        
        text = response.text
        # Extract JSON from response
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        return json.loads(text.strip())
        
    except Exception as e:
        print(f"Error in LLM paraphrasing: {e}")
        return entity_definitions


def generate_llm_variations(
    base_variations: List[PromptVariation],
    entity_definitions: Dict[str, str],
    num_variations: int = 3
) -> List[PromptVariation]:
    """
    Generate additional variations using LLM paraphrasing.
    
    Args:
        base_variations: Base variation templates
        entity_definitions: Original entity definitions
        num_variations: Number of LLM variations to generate
    
    Returns:
        List of new variations with paraphrased definitions
    """
    load_env()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not found, skipping LLM variations")
        return []
    
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=api_key)
        
        new_variations = []
        
        for i in range(num_variations):
            # Paraphrase entity definitions
            paraphrased_defs = paraphrase_entity_definitions(
                entity_definitions, f"llm_v{i}"
            )
            
            # Also paraphrase the docstring/function components
            base = base_variations[i % len(base_variations)]
            
            prompt = f"""Paraphrase these NER prompt components while preserving their meaning:

Function name: {base.function_name}
Docstring: {base.docstring}
Entity header: {base.entity_header}

Requirements:
- Keep the same intent and structure
- Use only lexical substitutions
- Return as JSON with keys: function_name, docstring, entity_header"""

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.7)
            )
            
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            components = json.loads(text.strip())
            
            new_var = PromptVariation(
                id=f"llm_v{i}",
                name=f"LLM Generated Variation {i+1}",
                function_name=components.get("function_name", base.function_name),
                docstring=components.get("docstring", base.docstring),
                entity_header=components.get("entity_header", base.entity_header),
                text_prefix=base.text_prefix,
                entity_prompt=base.entity_prompt,
                entity_descriptions=paraphrased_defs,
            )
            new_variations.append(new_var)
            print(f"Generated LLM variation {i+1}/{num_variations}")
        
        return new_variations
        
    except Exception as e:
        print(f"Error generating LLM variations: {e}")
        return []


# ============================================================================
# Prompt Export Functions (Readable .md and Log Files)
# ============================================================================

def generate_sample_prompt(
    variation: PromptVariation,
    entity_types: List[str],
    entity_definitions: Dict[str, str],
    style: str = "code"
) -> str:
    """Generate a sample prompt for display/export purposes."""
    sample_text = "Apple announced that Steve Jobs would present the new iPhone at WWDC in San Francisco."
    
    if style == "code":
        return build_code_prompt(
            text=sample_text,
            entity_types=entity_types,
            entity_definitions=entity_definitions,
            variation=variation,
            include_schema=True
        )
    else:
        return build_nl_prompt(
            text=sample_text,
            entity_types=entity_types,
            entity_definitions=entity_definitions,
            variation=variation,
            include_schema=True
        )


def save_prompt_as_markdown(
    output_dir: str,
    variation: PromptVariation,
    entity_types: List[str],
    entity_definitions: Dict[str, str],
    style: str,
    granularity: str
):
    """
    Save a prompt variation as a readable markdown file.
    
    Args:
        output_dir: Directory to save the file
        variation: Prompt variation to save
        entity_types: List of entity type names
        entity_definitions: Entity type descriptions
        style: 'code' or 'nl'
        granularity: 'coarse' or 'fine'
    """
    from datetime import datetime
    
    # Generate the full prompt
    sample_prompt = generate_sample_prompt(
        variation, entity_types, entity_definitions, style
    )
    
    # Create markdown content
    style_name = "Code-Style (pl-func)" if style == "code" else "Natural Language (nl-sel)"
    
    md_content = f"""# CodeIE Prompt Variation: {variation.name}

## Metadata
- **Variation ID**: `{variation.id}`
- **Style**: {style_name}
- **Granularity**: {granularity}
- **Entity Types**: {len(entity_types)}
- **Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Configuration

"""
    
    if style == "code":
        md_content += f"""| Property | Value |
|----------|-------|
| Function Name | `{variation.function_name}` |
| Docstring | "{variation.docstring}" |
| Entity Header | `{variation.entity_header}` |

"""
    else:
        md_content += f"""| Property | Value |
|----------|-------|
| Text Prefix | `{variation.text_prefix[:50]}...` |
| Entity Prompt | `{variation.entity_prompt}` |

"""
    
    md_content += f"""## Entity Definitions

The following entity types are included in this prompt:

| Entity Type | Description |
|-------------|-------------|
"""
    
    for entity_type in entity_types:
        desc = entity_definitions.get(entity_type, "")
        md_content += f"| `{entity_type}` | {desc} |\n"
    
    md_content += f"""

## Sample Prompt

Below is a sample prompt generated with this variation:

```python
{sample_prompt}
```

## Usage

To use this variation in experiments:

```bash
python run_codeie_experiments.py --granularity {granularity} --style {'pl' if style == 'code' else 'nl'} --variation {variation.id}
```
"""
    
    # Save markdown file
    style_tag = "code" if style == "code" else "nl"
    filename = f"{granularity}_{style_tag}_{variation.id}.md"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        f.write(md_content)
    
    return filepath


def save_creation_log(
    output_dir: str,
    variation: PromptVariation,
    entity_types: List[str],
    entity_definitions: Dict[str, str],
    style: str,
    granularity: str,
    base_prompt: str = None,
    similarity_score: float = None
):
    """
    Save a creation log file with metadata (matching GoLLIE format).
    
    Args:
        output_dir: Directory to save the file
        variation: Prompt variation
        entity_types: List of entity type names
        entity_definitions: Entity type descriptions
        style: 'code' or 'nl'
        granularity: 'coarse' or 'fine'
        base_prompt: Original base prompt for similarity comparison
        similarity_score: Cosine similarity to base prompt
    """
    from datetime import datetime
    import time
    
    # Generate the prompt
    sample_prompt = generate_sample_prompt(
        variation, entity_types, entity_definitions, style
    )
    
    # Build the log entry
    log_entry = {
        "variation_id": variation.id,
        "variation_name": variation.name,
        "style": "code" if style == "code" else "nl",
        "granularity": granularity,
        "entity_count": len(entity_types),
        "model_name": "gemini-2.0-flash" if variation.id.startswith("llm_") else None,
        "mode": "llm_paraphrase" if variation.id.startswith("llm_") else "predefined",
        "configuration": {
            "function_name": variation.function_name if style == "code" else None,
            "docstring": variation.docstring if style == "code" else None,
            "entity_header": variation.entity_header if style == "code" else None,
            "text_prefix": variation.text_prefix if style == "nl" else None,
            "entity_prompt": variation.entity_prompt if style == "nl" else None,
        },
        "entity_types": entity_types,
        "entity_definitions": entity_definitions,
        "generated_prompt": sample_prompt,
        "similarity_to_base_prompt": similarity_score,
        "similarity_measure": "Cosine Similarity / Faiss IndexFlatIP" if similarity_score else None,
        "timestamp": time.strftime("%a %b %d %H:%M:%S %Y")
    }
    
    # Remove None values for cleaner output
    log_entry = {k: v for k, v in log_entry.items() if v is not None}
    if log_entry.get("configuration"):
        log_entry["configuration"] = {k: v for k, v in log_entry["configuration"].items() if v is not None}
    
    # Save log file
    style_tag = "code" if style == "code" else "nl"
    filename = f"{granularity}_{style_tag}_{variation.id}.json"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w') as f:
        json.dump(log_entry, f, indent=2)
    
    return filepath


def calculate_prompt_similarity(prompt1: str, prompt2: str) -> float:
    """
    Calculate cosine similarity between two prompts using embeddings.
    
    Args:
        prompt1: First prompt
        prompt2: Second prompt
    
    Returns:
        Cosine similarity score (0-1)
    """
    load_env()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None
    
    try:
        from google import genai
        import numpy as np
        
        client = genai.Client(api_key=api_key)
        
        # Get embeddings
        result1 = client.models.embed_content(
            model="models/text-embedding-004",
            contents=prompt1
        )
        result2 = client.models.embed_content(
            model="models/text-embedding-004",
            contents=prompt2
        )
        
        v1 = np.array(result1.embeddings[0].values, dtype='float32')
        v2 = np.array(result2.embeddings[0].values, dtype='float32')
        
        # Cosine similarity
        v1 = v1 / np.linalg.norm(v1)
        v2 = v2 / np.linalg.norm(v2)
        
        return float(np.dot(v1, v2))
        
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return None


# ============================================================================
# Main Script
# ============================================================================

def save_variations(
    output_dir: str,
    granularity: str,
    code_variations: List[PromptVariation],
    nl_variations: List[PromptVariation],
    entity_definitions: Dict[str, str],
    export_prompts: bool = True,
    calculate_similarities: bool = False
):
    """Save prompt variations to files with optional prompt exports and logs."""
    os.makedirs(output_dir, exist_ok=True)
    
    entity_types = list(entity_definitions.keys())
    
    # Create subdirectory for readable prompts
    prompts_dir = os.path.join(output_dir, "prompts")
    logs_dir = os.path.join(output_dir, "logs")
    os.makedirs(prompts_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    
    # Save as Python module
    py_content = f'''"""
Auto-generated prompt variations for CodeIE NER ({granularity} granularity)

This module contains prompt variations that include explicit entity schema,
following the GoLLIE methodology of providing entity type definitions.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

# Entity definitions for {granularity} granularity
ENTITY_DEFINITIONS = {json.dumps(entity_definitions, indent=4)}


@dataclass
class CodeStyleConfig:
    """Configuration for code-style prompts."""
    id: str
    name: str
    function_name: str
    docstring: str
    entity_header: str
    entity_descriptions: Optional[Dict[str, str]] = None


@dataclass 
class NLStyleConfig:
    """Configuration for natural language style prompts."""
    id: str
    name: str
    text_prefix: str
    entity_prompt: str


# Code-style prompt variations
CODE_STYLE_VARIATIONS = {{
'''
    
    for var in code_variations:
        desc_str = f'ENTITY_DEFINITIONS' if var.entity_descriptions is None else repr(var.entity_descriptions)
        py_content += f'''    "{var.id}": CodeStyleConfig(
        id="{var.id}",
        name="{var.name}",
        function_name="{var.function_name}",
        docstring="{var.docstring}",
        entity_header="{var.entity_header}",
        entity_descriptions={desc_str},
    ),
'''
    
    py_content += "}\n\n# Natural language style prompt variations\nNL_STYLE_VARIATIONS = {\n"
    
    for var in nl_variations:
        py_content += f'''    "{var.id}": NLStyleConfig(
        id="{var.id}",
        name="{var.name}",
        text_prefix={repr(var.text_prefix)},
        entity_prompt="{var.entity_prompt}",
    ),
'''
    
    py_content += "}\n"
    
    # Write Python module
    py_path = os.path.join(output_dir, f'{granularity}_prompt_variations.py')
    with open(py_path, 'w') as f:
        f.write(py_content)
    print(f"Saved: {py_path}")
    
    # Also save as JSON for reference
    json_data = {
        "granularity": granularity,
        "entity_definitions": entity_definitions,
        "code_variations": [
            {
                "id": v.id,
                "name": v.name,
                "function_name": v.function_name,
                "docstring": v.docstring,
                "entity_header": v.entity_header,
            }
            for v in code_variations
        ],
        "nl_variations": [
            {
                "id": v.id,
                "name": v.name,
                "text_prefix": v.text_prefix,
                "entity_prompt": v.entity_prompt,
            }
            for v in nl_variations
        ],
    }
    
    json_path = os.path.join(output_dir, f'{granularity}_variations.json')
    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=2)
    print(f"Saved: {json_path}")
    
    # Export individual prompt files and logs if requested
    if export_prompts:
        print(f"\nExporting prompt files to: {prompts_dir}")
        print(f"Exporting log files to: {logs_dir}")
        
        # Generate base prompt for similarity calculation
        base_code_prompt = None
        base_nl_prompt = None
        
        if code_variations:
            base_code_prompt = generate_sample_prompt(
                code_variations[0], entity_types, entity_definitions, "code"
            )
        if nl_variations:
            base_nl_prompt = generate_sample_prompt(
                nl_variations[0], entity_types, entity_definitions, "nl"
            )
        
        # Export code-style variations
        for var in code_variations:
            # Save markdown prompt file
            md_path = save_prompt_as_markdown(
                prompts_dir, var, entity_types, entity_definitions, "code", granularity
            )
            
            # Calculate similarity to base if requested
            similarity = None
            if calculate_similarities and base_code_prompt:
                current_prompt = generate_sample_prompt(
                    var, entity_types, entity_definitions, "code"
                )
                if var.id != code_variations[0].id:
                    similarity = calculate_prompt_similarity(base_code_prompt, current_prompt)
            
            # Save log file
            log_path = save_creation_log(
                logs_dir, var, entity_types, entity_definitions,
                "code", granularity, base_code_prompt, similarity
            )
            
            print(f"  ✓ {var.id}: {os.path.basename(md_path)}, {os.path.basename(log_path)}")
        
        # Export NL-style variations
        for var in nl_variations:
            # Save markdown prompt file
            md_path = save_prompt_as_markdown(
                prompts_dir, var, entity_types, entity_definitions, "nl", granularity
            )
            
            # Calculate similarity to base if requested
            similarity = None
            if calculate_similarities and base_nl_prompt:
                current_prompt = generate_sample_prompt(
                    var, entity_types, entity_definitions, "nl"
                )
                if var.id != nl_variations[0].id:
                    similarity = calculate_prompt_similarity(base_nl_prompt, current_prompt)
            
            # Save log file
            log_path = save_creation_log(
                logs_dir, var, entity_types, entity_definitions,
                "nl", granularity, base_nl_prompt, similarity
            )
            
            print(f"  ✓ {var.id}: {os.path.basename(md_path)}, {os.path.basename(log_path)}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate CodeIE prompt variations with entity schema"
    )
    parser.add_argument(
        '--granularity', choices=['coarse', 'fine'], default='coarse',
        help="Entity granularity (coarse: 8 types, fine: 66 types)"
    )
    parser.add_argument(
        '--output_dir', default='prompt_variations',
        help="Output directory for variations"
    )
    parser.add_argument(
        '--generate_llm', action='store_true',
        help="Generate additional LLM-based variations (requires GEMINI_API_KEY)"
    )
    parser.add_argument(
        '--num_llm_variations', type=int, default=3,
        help="Number of LLM variations to generate"
    )
    parser.add_argument(
        '--calculate_similarities', action='store_true',
        help="Calculate cosine similarity between variations (requires GEMINI_API_KEY)"
    )
    parser.add_argument(
        '--no_export', action='store_true',
        help="Skip exporting individual prompt .md and log .json files"
    )
    
    args = parser.parse_args()
    
    # Select entity definitions based on granularity
    if args.granularity == 'coarse':
        entity_definitions = COARSE_ENTITY_DEFINITIONS
    else:
        entity_definitions = FINE_ENTITY_DEFINITIONS
    
    print(f"\n{'='*60}")
    print(f"CodeIE Prompt Variation Generator")
    print(f"{'='*60}")
    print(f"Granularity: {args.granularity}")
    print(f"Entity types: {len(entity_definitions)}")
    print(f"Export prompts: {not args.no_export}")
    print(f"Calculate similarities: {args.calculate_similarities}")
    print(f"{'='*60}\n")
    
    # Get base variations
    code_variations = get_code_style_variations()
    nl_variations = get_nl_style_variations()
    
    print(f"Generated {len(code_variations)} code-style variations")
    print(f"Generated {len(nl_variations)} NL-style variations")
    
    # Generate LLM variations if requested
    if args.generate_llm:
        print(f"\nGenerating {args.num_llm_variations} LLM-based variations...")
        llm_code_vars = generate_llm_variations(
            code_variations, entity_definitions, args.num_llm_variations
        )
        code_variations.extend(llm_code_vars)
        print(f"Total code-style variations: {len(code_variations)}")
    
    # Save variations
    output_dir = os.path.join(CODEIE_ROOT, args.output_dir)
    save_variations(
        output_dir,
        args.granularity,
        code_variations,
        nl_variations,
        entity_definitions,
        export_prompts=not args.no_export,
        calculate_similarities=args.calculate_similarities
    )
    
    print(f"\n{'='*60}")
    print("Generation complete!")
    print(f"Output directory: {output_dir}")
    print(f"  - Python module: {args.granularity}_prompt_variations.py")
    print(f"  - JSON config: {args.granularity}_variations.json")
    if not args.no_export:
        print(f"  - Prompts: prompts/")
        print(f"  - Logs: logs/")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()

