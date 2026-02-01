"""
CodeIE Prompt Variation Generator

This module creates prompt variations for CodeIE experiments, following the same
methodology used in the GoLLIE annotation-guidelines but adapted for CodeIE's
code-style and natural-language prompt formats.

CodeIE Prompt Anatomy
=====================
1. Code Style (pl-func):
   - Function definition: def named_entity_recognition(input_text):
   - Docstring describing the task
   - Input assignment: input_text = "..."
   - Entity list init: entity_list = []
   - Inline comment: # extracted named entities
   - Entity appends: entity_list.append({"text": "...", "type": "..."})

2. Natural Language Style (nl-sel):
   - Input: The text is : "..." .
   - Prompt: The named entities in the text:
   - Output: SEL format with special tokens

Variation Strategies
====================
1. Docstring variations (for pl-func)
2. Function name variations (for pl-func)
3. Comment style variations (for pl-func)
4. Natural language phrasing variations (for nl-sel)
5. Entity type description variations (both styles)

Usage:
    python generate_codeie_prompt_variations.py
"""

import os
import sys
import json
import time
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass, field, asdict

# Load environment
def load_env():
    env_path = '.env'
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

load_env()


# ============================================================================
# Prompt Template Definitions
# ============================================================================

@dataclass
class CodeStylePromptTemplate:
    """
    Template for code-style (pl-func) prompts.
    Each field can be varied independently.
    """
    # Function definition elements
    function_name: str = "named_entity_recognition"
    function_input: str = "input_text"
    
    # Docstring - the main element to vary
    docstring: str = "extract named entities from the input_text"
    
    # Variable names
    input_var: str = "input_text"
    list_var: str = "entity_list"
    
    # Inline comment before entity extraction
    inline_comment: str = "extracted named entities"
    
    # Entity append format
    entity_text_key: str = "text"
    entity_type_key: str = "type"
    
    def render_prompt_head(self, text: str) -> str:
        """Render the prompt head (before entity appends)."""
        lines = [
            f'def {self.function_name}({self.function_input}):',
            f'\t""" {self.docstring} . """',
            f'\t{self.input_var} = "{text}"',
            f'\t{self.list_var} = []',
            f'\t# {self.inline_comment}',
        ]
        return '\n'.join(lines)
    
    def render_entity_append(self, entity_text: str, entity_type: str) -> str:
        """Render a single entity append line."""
        return f'\t{self.list_var}.append({{"{self.entity_text_key}": "{entity_text}", "{self.entity_type_key}": "{entity_type}"}})'


@dataclass 
class NLStylePromptTemplate:
    """
    Template for natural language style (nl-sel) prompts.
    """
    # Input phrasing
    input_prefix: str = "The text is :"
    input_suffix: str = "."
    
    # Entity prompt phrasing
    entity_prompt: str = "The named entities in the text:"
    
    def render_prompt_head(self, text: str) -> str:
        """Render the NL-style prompt head."""
        return f'{self.input_prefix} "{text}" {self.input_suffix} {self.entity_prompt} '


# ============================================================================
# Pre-defined Prompt Variations
# ============================================================================

CODE_STYLE_VARIATIONS: Dict[str, CodeStylePromptTemplate] = {
    # Original/baseline
    "v0_original": CodeStylePromptTemplate(
        function_name="named_entity_recognition",
        docstring="extract named entities from the input_text",
        inline_comment="extracted named entities",
    ),
    
    # Variation 1: More formal docstring
    "v1_formal": CodeStylePromptTemplate(
        function_name="extract_entities",
        docstring="identify and extract all named entities present in the input text",
        inline_comment="identified named entities",
    ),
    
    # Variation 2: Task-focused docstring  
    "v2_task_focused": CodeStylePromptTemplate(
        function_name="ner_extraction",
        docstring="perform named entity recognition on the given text and return all entities",
        inline_comment="recognized entities",
    ),
    
    # Variation 3: Minimal/concise
    "v3_concise": CodeStylePromptTemplate(
        function_name="get_entities",
        docstring="find named entities in text",
        inline_comment="entities found",
    ),
    
    # Variation 4: Detailed/verbose
    "v4_detailed": CodeStylePromptTemplate(
        function_name="named_entity_extraction",
        docstring="analyze the input text and extract all named entities including persons, locations, organizations and other entity types",
        inline_comment="all extracted named entities with their types",
    ),
    
    # Variation 5: Academic style
    "v5_academic": CodeStylePromptTemplate(
        function_name="perform_ner",
        docstring="apply named entity recognition to identify and classify entity mentions in the text",
        inline_comment="classified entity mentions",
    ),
    
    # Variation 6: Instruction-like
    "v6_instruction": CodeStylePromptTemplate(
        function_name="identify_entities", 
        docstring="given the input text, identify all spans that refer to named entities",
        inline_comment="named entity spans",
    ),
}

NL_STYLE_VARIATIONS: Dict[str, NLStylePromptTemplate] = {
    # Original
    "v0_original": NLStylePromptTemplate(
        input_prefix="The text is :",
        entity_prompt="The named entities in the text:",
    ),
    
    # Variation 1: More formal
    "v1_formal": NLStylePromptTemplate(
        input_prefix="Input text:",
        entity_prompt="Named entities found:",
    ),
    
    # Variation 2: Question style
    "v2_question": NLStylePromptTemplate(
        input_prefix="Given the following text:",
        entity_prompt="What are the named entities?",
    ),
    
    # Variation 3: Task description
    "v3_task": NLStylePromptTemplate(
        input_prefix="Text for entity extraction:",
        entity_prompt="Extracted entities:",
    ),
    
    # Variation 4: Detailed instruction
    "v4_detailed": NLStylePromptTemplate(
        input_prefix="Analyze the following sentence:",
        entity_prompt="The named entities (persons, locations, organizations, etc.) are:",
    ),
    
    # Variation 5: Concise
    "v5_concise": NLStylePromptTemplate(
        input_prefix="Text:",
        entity_prompt="Entities:",
    ),
}


# ============================================================================  
# LLM-based Variation Generation (using Gemini like GoLLIE)
# ============================================================================

def generate_llm_variation(template_dict: dict, mode: str = "standard") -> Tuple[dict, str, float]:
    """
    Generate a variation of a prompt template using an LLM.
    
    Args:
        template_dict: Dictionary representation of a prompt template
        mode: "standard" or "detailed" variation mode
        
    Returns:
        Tuple of (varied_template_dict, prompt_used, similarity_score)
    """
    try:
        from google import genai
        from google.genai import types
        import faiss
    except ImportError:
        print("Warning: google-genai or faiss not installed. Using predefined variations only.")
        return template_dict, "", 1.0
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not set. Using predefined variations only.")
        return template_dict, "", 1.0
    
    client = genai.Client(api_key=api_key)
    model_name = "gemini-3-flash-preview"
    
    template_json = json.dumps(template_dict, indent=2)
    
    if mode == "detailed":
        instruction = f"""Paraphrase the following prompt template for named entity recognition.
Key requirements:
- Maintain the structure and field names exactly
- Paraphrase the text values (docstring, comments, prompts) while preserving meaning
- Make the language clearer and more precise
- Keep field names unchanged

Template:
{template_json}

Return ONLY a valid JSON object with the same structure."""
    else:
        instruction = f"""Create a variation of this prompt template for named entity recognition.
Key requirements:
- Keep the exact same structure and field names
- Vary the text content (docstrings, comments, prompts) using synonyms and rephrasing
- Maintain the same semantic meaning
- Return ONLY valid JSON

Template:
{template_json}"""
    
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=instruction,
            config=types.GenerateContentConfig(temperature=0.8)
        )
        
        text = response.text
        # Extract JSON from response
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        varied_dict = json.loads(text.strip())
        
        # Calculate similarity
        def get_embedding(text_content):
            result = client.models.embed_content(
                model="models/text-embedding-004",
                contents=text_content
            )
            return np.array(result.embeddings[0].values, dtype='float32')
        
        orig_emb = get_embedding(template_json)
        var_emb = get_embedding(json.dumps(varied_dict))
        
        # Normalize and compute cosine similarity
        orig_emb = orig_emb / np.linalg.norm(orig_emb)
        var_emb = var_emb / np.linalg.norm(var_emb)
        similarity = float(np.dot(orig_emb, var_emb))
        
        return varied_dict, instruction, similarity
        
    except Exception as e:
        print(f"LLM variation failed: {e}")
        return template_dict, "", 1.0


def save_variations_as_python_configs(output_dir: str = "prompt_variations"):
    """
    Save all prompt variations as Python configuration files.
    This creates importable modules similar to GoLLIE's annotation_guidelines.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate Python files for code-style variations
    code_style_file = os.path.join(output_dir, "code_style_variations.py")
    with open(code_style_file, 'w') as f:
        f.write('"""\nCode-style (pl-func) prompt variations for CodeIE NER experiments.\n"""\n\n')
        f.write('from dataclasses import dataclass\n\n')
        
        f.write('@dataclass\nclass CodeStyleConfig:\n')
        f.write('    function_name: str\n')
        f.write('    docstring: str\n')
        f.write('    inline_comment: str\n')
        f.write('    function_input: str = "input_text"\n')
        f.write('    input_var: str = "input_text"\n')
        f.write('    list_var: str = "entity_list"\n')
        f.write('    entity_text_key: str = "text"\n')
        f.write('    entity_type_key: str = "type"\n\n')
        
        f.write('# Predefined variations\n')
        f.write('VARIATIONS = {\n')
        for name, template in CODE_STYLE_VARIATIONS.items():
            f.write(f'    "{name}": CodeStyleConfig(\n')
            f.write(f'        function_name="{template.function_name}",\n')
            f.write(f'        docstring="{template.docstring}",\n')
            f.write(f'        inline_comment="{template.inline_comment}",\n')
            f.write('    ),\n')
        f.write('}\n')
    
    print(f"Created: {code_style_file}")
    
    # Generate Python files for NL-style variations
    nl_style_file = os.path.join(output_dir, "nl_style_variations.py")
    with open(nl_style_file, 'w') as f:
        f.write('"""\nNatural language style (nl-sel) prompt variations for CodeIE NER experiments.\n"""\n\n')
        f.write('from dataclasses import dataclass\n\n')
        
        f.write('@dataclass\nclass NLStyleConfig:\n')
        f.write('    input_prefix: str\n')
        f.write('    entity_prompt: str\n')
        f.write('    input_suffix: str = "."\n\n')
        
        f.write('# Predefined variations\n')
        f.write('VARIATIONS = {\n')
        for name, template in NL_STYLE_VARIATIONS.items():
            f.write(f'    "{name}": NLStyleConfig(\n')
            f.write(f'        input_prefix="{template.input_prefix}",\n')
            f.write(f'        entity_prompt="{template.entity_prompt}",\n')
            f.write('    ),\n')
        f.write('}\n')
    
    print(f"Created: {nl_style_file}")
    
    # Create __init__.py
    init_file = os.path.join(output_dir, "__init__.py")
    with open(init_file, 'w') as f:
        f.write('from .code_style_variations import VARIATIONS as CODE_STYLE_VARIATIONS, CodeStyleConfig\n')
        f.write('from .nl_style_variations import VARIATIONS as NL_STYLE_VARIATIONS, NLStyleConfig\n')
    
    print(f"Created: {init_file}")
    
    # Save as JSON for logging/documentation
    json_file = os.path.join(output_dir, "all_variations.json")
    all_variations = {
        "code_style": {
            name: asdict(template) for name, template in CODE_STYLE_VARIATIONS.items()
        },
        "nl_style": {
            name: asdict(template) for name, template in NL_STYLE_VARIATIONS.items()
        }
    }
    with open(json_file, 'w') as f:
        json.dump(all_variations, f, indent=2)
    
    print(f"Created: {json_file}")
    
    return output_dir


def main():
    """Generate and save all prompt variations."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate CodeIE prompt variations")
    parser.add_argument('--output_dir', default='prompt_variations',
                        help="Output directory for variations")
    parser.add_argument('--generate_llm', action='store_true',
                        help="Also generate LLM-based variations (requires GEMINI_API_KEY)")
    parser.add_argument('--num_llm_variations', type=int, default=3,
                        help="Number of LLM variations to generate per base template")
    
    args = parser.parse_args()
    
    print("="*60)
    print("CodeIE Prompt Variation Generator")
    print("="*60)
    
    # Create base output directory
    base_output = os.path.join(os.path.dirname(__file__), args.output_dir)
    
    # Save predefined variations
    save_variations_as_python_configs(base_output)
    
    if args.generate_llm:
        print("\nGenerating LLM-based variations...")
        
        llm_dir = os.path.join(base_output, "llm_generated")
        os.makedirs(llm_dir, exist_ok=True)
        
        # Generate LLM variations for code-style
        for name, template in CODE_STYLE_VARIATIONS.items():
            if name == "v0_original":  # Use original as base
                for i in range(args.num_llm_variations):
                    for mode in ["standard", "detailed"]:
                        varied, prompt, sim = generate_llm_variation(asdict(template), mode)
                        
                        out_file = os.path.join(llm_dir, f"code_style_{mode}_v{i+1}.json")
                        with open(out_file, 'w') as f:
                            json.dump({
                                "variation": varied,
                                "base": name,
                                "mode": mode,
                                "similarity": sim,
                                "prompt_used": prompt,
                                "timestamp": time.ctime()
                            }, f, indent=2)
                        print(f"Created: {out_file} (similarity: {sim:.4f})")
                        time.sleep(1)  # Rate limiting
    
    print("\n" + "="*60)
    print("Prompt variation generation complete!")
    print(f"Output directory: {base_output}")
    print("="*60)


if __name__ == "__main__":
    main()
