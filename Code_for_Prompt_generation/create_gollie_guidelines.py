import json
import os
import sys
from google import genai
from google.genai import types

# Load environment variables from .env file
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

def generate_guidelines(input_file, output_file, num_examples=4):
    print(f"Processing {input_file} -> {output_file} (examples per class: {num_examples})...")
    
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found.")
        return

    with open(input_file, 'r') as f:
        data = json.load(f)
        
    # Slice data to limit examples per class
    sliced_data = {}
    for label, examples in data.items():
        sliced_data[label] = examples[:num_examples]

    schema_example = """
from typing import List
from src.tasks.utils_typing import Entity, dataclass

@dataclass
class PrivateSpaceCompany(Entity):
    \"\"\"Refers to private companies primarily focused on space exploration...\"\"\"
    span: str  # Such as: "Blue origin", "Boeing"

ENTITY_DEFINITIONS: List[Entity] = [
    PrivateSpaceCompany,
]
"""
    
    prompt_text = f"""
You are an expert in defining Named Entity Recognition (NER) guidelines for GOllie.
I have a dataset of entities with examples. 
Please generate a Python file defining these entities using `dataclass` and inheriting from `Entity`.

Follow this exact schema structure:
{schema_example}

Requirements:
1.  **Imports**: MUST include `from typing import List` and `from src.tasks.utils_typing import Entity, dataclass`.
2.  **Classes**: Create a class for EACH label in the input JSON. 
    - Convert label names to PascalCase (e.g., "art-film" -> "ArtFilm", "person" -> "Person").
    - The docstring should define the entity based on the provided examples and generic knowledge about the entity type.
    - The `span` field should be `span: str` and include a comment with representative examples extracted from the provided data.
3.  **Entity List**: At the end, define `ENTITY_DEFINITIONS: List[Entity]` containing all the classes you defined.
4.  **Formatting**: The output must be valid Python code.

Here is the input JSON data with labels and examples (entities are marked with #Label#):
{json.dumps(sliced_data, indent=2)}
"""

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment.")
        return

    client = genai.Client(api_key=api_key)
    
    # Using the user-specified model which is available!
    model_id = "gemini-3-flash-preview"

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt_text),
            ],
        ),
    ]

    # Trying with thinking config as requested
    generate_content_config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="HIGH",
        ),
        response_mime_type="text/plain", # text/x-python not supported usually
    )

    try:
        response = client.models.generate_content(
            model=model_id,
            contents=contents,
            config=generate_content_config,
        )
        
        # Extract code
        code = response.text
        # Cleanup code blocks
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0]
        elif "```" in code:
            code = code.split("```")[1].split("```")[0]
            
        with open(output_file, 'w') as f:
            f.write(code.strip())
        print(f"Successfully generated {output_file}")
        
    except Exception as e:
        print(f"Error generating content: {e}")
        # Fallback without thinking config if that was the issue
        if "ThinkingConfig" in str(e) or "thinking" in str(e).lower():
             print("Retrying without thinking config...")
             generate_content_config = types.GenerateContentConfig(
                response_mime_type="text/plain",
                temperature=0.0 # Low temperature for guidelines
             )
             try:
                response = client.models.generate_content(
                    model=model_id,
                    contents=contents,
                    config=generate_content_config,
                )
                code = response.text
                if "```python" in code:
                    code = code.split("```python")[1].split("```")[0]
                elif "```" in code:
                    code = code.split("```")[1].split("```")[0]
                with open(output_file, 'w') as f:
                    f.write(code.strip())
                print(f"Successfully generated {output_file} (fallback)")
             except Exception as e2:
                 print(f"Error in fallback: {e2}")

if __name__ == "__main__":
    # Standard Guidelines (4 examples)
    generate_guidelines('coarse_labels_examples.json', 'annotation_guidelines/guidelines_coarse_gollie.py', num_examples=4)
    generate_guidelines('fine_labels_examples.json', 'annotation_guidelines/guidelines_fine_gollie.py', num_examples=4)
    
    # Detailed Guidelines Source (8 examples) - used for generating detailed variations
    generate_guidelines('coarse_labels_examples.json', 'annotation_guidelines/guidelines_coarse_gollie_8_examples.py', num_examples=8)
    generate_guidelines('fine_labels_examples.json', 'annotation_guidelines/guidelines_fine_gollie_8_examples.py', num_examples=8)
