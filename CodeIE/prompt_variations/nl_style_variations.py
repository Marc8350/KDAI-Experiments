"""
Natural language style (nl-sel) prompt variations for CodeIE NER experiments.
"""

from dataclasses import dataclass

@dataclass
class NLStyleConfig:
    input_prefix: str
    entity_prompt: str
    input_suffix: str = "."

# Predefined variations
VARIATIONS = {
    "v0_original": NLStyleConfig(
        input_prefix="The text is :",
        entity_prompt="The named entities in the text:",
    ),
    "v1_formal": NLStyleConfig(
        input_prefix="Input text:",
        entity_prompt="Named entities found:",
    ),
    "v2_question": NLStyleConfig(
        input_prefix="Given the following text:",
        entity_prompt="What are the named entities?",
    ),
    "v3_task": NLStyleConfig(
        input_prefix="Text for entity extraction:",
        entity_prompt="Extracted entities:",
    ),
    "v4_detailed": NLStyleConfig(
        input_prefix="Analyze the following sentence:",
        entity_prompt="The named entities (persons, locations, organizations, etc.) are:",
    ),
    "v5_concise": NLStyleConfig(
        input_prefix="Text:",
        entity_prompt="Entities:",
    ),
}
