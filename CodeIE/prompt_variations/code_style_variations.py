"""
Code-style (pl-func) prompt variations for CodeIE NER experiments.
"""

from dataclasses import dataclass

@dataclass
class CodeStyleConfig:
    function_name: str
    docstring: str
    inline_comment: str
    function_input: str = "input_text"
    input_var: str = "input_text"
    list_var: str = "entity_list"
    entity_text_key: str = "text"
    entity_type_key: str = "type"

# Predefined variations
VARIATIONS = {
    "v0_original": CodeStyleConfig(
        function_name="named_entity_recognition",
        docstring="extract named entities from the input_text",
        inline_comment="extracted named entities",
    ),
    "v1_formal": CodeStyleConfig(
        function_name="extract_entities",
        docstring="identify and extract all named entities present in the input text",
        inline_comment="identified named entities",
    ),
    "v2_task_focused": CodeStyleConfig(
        function_name="ner_extraction",
        docstring="perform named entity recognition on the given text and return all entities",
        inline_comment="recognized entities",
    ),
    "v3_concise": CodeStyleConfig(
        function_name="get_entities",
        docstring="find named entities in text",
        inline_comment="entities found",
    ),
    "v4_detailed": CodeStyleConfig(
        function_name="named_entity_extraction",
        docstring="analyze the input text and extract all named entities including persons, locations, organizations and other entity types",
        inline_comment="all extracted named entities with their types",
    ),
    "v5_academic": CodeStyleConfig(
        function_name="perform_ner",
        docstring="apply named entity recognition to identify and classify entity mentions in the text",
        inline_comment="classified entity mentions",
    ),
    "v6_instruction": CodeStyleConfig(
        function_name="identify_entities",
        docstring="given the input text, identify all spans that refer to named entities",
        inline_comment="named entity spans",
    ),
}
