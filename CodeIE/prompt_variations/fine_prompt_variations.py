"""
Auto-generated prompt variations for CodeIE NER (fine granularity)

This module contains prompt variations that include explicit entity schema,
following the GoLLIE methodology of providing entity type definitions.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

# Entity definitions for fine granularity
ENTITY_DEFINITIONS = {
    "person-actor": "An actor or actress in film, television, or theater.",
    "person-artist/author": "A creative artist, writer, or author.",
    "person-athlete": "A professional or amateur sports player.",
    "person-director": "A film, television, or theater director.",
    "person-politician": "A political figure or government official.",
    "person-scholar": "An academic, researcher, or scholar.",
    "person-soldier": "A military personnel or soldier.",
    "person-other": "Other individuals not fitting specific person categories.",
    "location-GPE": "A geo-political entity like a country, state, or city.",
    "location-bodiesofwater": "A named body of water like an ocean, sea, river, or lake.",
    "location-island": "A named island or archipelago.",
    "location-mountain": "A named mountain, mountain range, or hill.",
    "location-park": "A named park, nature reserve, or recreational area.",
    "location-road/railway/highway/transit": "A named road, railway, highway, or transit route.",
    "location-other": "Other geographical locations.",
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
    "building-airport": "A named airport.",
    "building-hospital": "A named hospital or medical facility.",
    "building-hotel": "A named hotel or lodging establishment.",
    "building-library": "A named library.",
    "building-restaurant": "A named restaurant or dining establishment.",
    "building-sportsfacility": "A named sports stadium, arena, or facility.",
    "building-theater": "A named theater or performance venue.",
    "building-other": "Other named buildings or structures.",
    "art-broadcastprogram": "A television or radio program.",
    "art-film": "A movie or film.",
    "art-music": "A musical work, song, or album.",
    "art-painting": "A painting or visual artwork.",
    "art-writtenart": "A book, poem, or other written work.",
    "art-other": "Other works of art.",
    "product-airplane": "A named aircraft or airplane model.",
    "product-car": "A named car or vehicle model.",
    "product-food": "A named food product or brand.",
    "product-game": "A named game or video game.",
    "product-ship": "A named ship or watercraft.",
    "product-software": "A named software product or application.",
    "product-train": "A named train or railway vehicle.",
    "product-weapon": "A named weapon or weapons system.",
    "product-other": "Other products.",
    "event-attack/battle/war/militaryconflict": "A military conflict, battle, or attack.",
    "event-disaster": "A natural or man-made disaster.",
    "event-election": "A political election.",
    "event-protest": "A protest or demonstration.",
    "event-sportsevent": "A sports event or competition.",
    "event-other": "Other named events.",
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
    "other-medical": "Medical terms or procedures."
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
