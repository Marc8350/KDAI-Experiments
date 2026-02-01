"""
Auto-generated prompt variations for CodeIE NER (coarse granularity)

This module contains prompt variations that include explicit entity schema,
following the GoLLIE methodology of providing entity type definitions.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

# Entity definitions for coarse granularity
ENTITY_DEFINITIONS = {
    "person": "A named individual, including fictional characters, historical figures, celebrities, and common people.",
    "location": "A geographical location such as a city, country, continent, region, or landmark.",
    "organization": "A named organization, institution, company, or group.",
    "building": "A named structure or building, such as a stadium, museum, or hotel.",
    "art": "A work of art including films, books, music, paintings, or other creative works.",
    "product": "A named commercial product, software, vehicle model, or branded item.",
    "event": "A named event such as a war, sports event, festival, or historical occurrence.",
    "other": "Other named entities that don't fit into the above categories."
}


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
CODE_STYLE_VARIATIONS = {
    "v0_original": CodeStyleConfig(
        id="v0_original",
        name="Original CodeIE Style",
        function_name="named_entity_recognition",
        docstring="extract named entities from the input_text",
        entity_header="# Entity types to extract",
        entity_descriptions=ENTITY_DEFINITIONS,
    ),
    "v1_schema_aware": CodeStyleConfig(
        id="v1_schema_aware",
        name="Schema-Aware Extraction",
        function_name="extract_entities",
        docstring="Identify and extract named entities from the input text based on the defined entity schema",
        entity_header="# Valid entity types for this task",
        entity_descriptions=ENTITY_DEFINITIONS,
    ),
    "v2_typed_extraction": CodeStyleConfig(
        id="v2_typed_extraction",
        name="Typed Entity Extraction",
        function_name="typed_ner",
        docstring="Perform typed named entity recognition, extracting entities according to the type definitions",
        entity_header="# Entity type definitions",
        entity_descriptions=ENTITY_DEFINITIONS,
    ),
    "v3_structured": CodeStyleConfig(
        id="v3_structured",
        name="Structured NER",
        function_name="structured_entity_extraction",
        docstring="Extract structured entity mentions from text following the entity type schema below",
        entity_header="# Recognized entity categories",
        entity_descriptions=ENTITY_DEFINITIONS,
    ),
    "v4_guided": CodeStyleConfig(
        id="v4_guided",
        name="Guided Entity Recognition",
        function_name="guided_ner",
        docstring="Identify named entities in the input text using the entity type guidelines defined below",
        entity_header="# Entity type guidelines",
        entity_descriptions=ENTITY_DEFINITIONS,
    ),
    "v5_classification": CodeStyleConfig(
        id="v5_classification",
        name="Entity Classification Style",
        function_name="classify_entities",
        docstring="Find and classify named entity mentions in the text according to the schema",
        entity_header="# Classification schema",
        entity_descriptions=ENTITY_DEFINITIONS,
    ),
    "v6_annotation": CodeStyleConfig(
        id="v6_annotation",
        name="Annotation Task Style",
        function_name="annotate_entities",
        docstring="Annotate the input text with named entity labels from the allowed types",
        entity_header="# Allowed entity annotations",
        entity_descriptions=ENTITY_DEFINITIONS,
    ),
}

# Natural language style prompt variations
NL_STYLE_VARIATIONS = {
    "v0_original": NLStyleConfig(
        id="v0_original",
        name="Original CodeIE NL Style",
        text_prefix='The text is : "{text}". ',
        entity_prompt="The named entities in the text: ",
    ),
    "v1_schema_list": NLStyleConfig(
        id="v1_schema_list",
        name="Schema List Style",
        text_prefix='Given the entity types: {schema}\n\nText: "{text}"\n\n',
        entity_prompt="Named entities found: ",
    ),
    "v2_instruction": NLStyleConfig(
        id="v2_instruction",
        name="Instruction Style",
        text_prefix='Identify entities of types ({schema}) in: "{text}"\n\n',
        entity_prompt="Entities: ",
    ),
    "v3_task_description": NLStyleConfig(
        id="v3_task_description",
        name="Task Description Style",
        text_prefix='Task: Named Entity Recognition\nEntity Types: {schema}\nInput: "{text}"\n\n',
        entity_prompt="Output: ",
    ),
    "v4_detailed": NLStyleConfig(
        id="v4_detailed",
        name="Detailed Annotation Style",
        text_prefix='Analyze the following text for named entities.\nValid entity types are: {schema}\n\nText for analysis: "{text}"\n\n',
        entity_prompt="Identified entities: ",
    ),
}
