import os
import json
import time
import numpy as np
import faiss
from google import genai
from google.genai import types

# Load environment variables
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

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL_NAME = "gemini-3-flash-preview"
TEMPERATURE = 1.0

def get_embedding(text):
    result = client.models.embed_content(
        model="models/text-embedding-004",
        contents=text
    )
    return np.array(result.embeddings[0].values, dtype='float32')

def calculate_cosine_similarity(v1, v2):
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    d = v1.shape[0]
    index = faiss.IndexFlatIP(d)
    index.add(np.array([v1]))
    D, I = index.search(np.array([v2]), 1)
    return float(D[0][0])

def paraphrase_prompt(content, mode="standard"):
    if mode == "detailed":
        instruction = f"""Paraphrase the following prompt that will be used for automated data annotation.
Key requirements:
- Base your paraphrase on the content in the original prompt without adding new information.
- Improve clarity while maintaining the original meaning.
- Preserve the Annotation Task as well as the structure of the prompt.
- Use lexical substitutions and syntactic reordering for the docstrings and descriptions.
- Return the FULL file content with the modifications.

FILE CONTENT:
{content}
"""
    else: # standard mode
        instruction = f"""Paraphrase the following prompt that will be used for automated data annotation.
Key requirements:
- Preserve the Annotation Task as well as the structure of the prompt.
- Use lexical substitutions and syntactic reordering for the docstrings and descriptions.
- You ARE allowed and encouraged to substitute the examples provided after the '#' or within the 'span' field comments with different, equally valid examples of that class.
- You are allowed to rename the class comments in \"\"\" \"\"\" or after # .
- Return the FULL file content with the modifications.

FILE CONTENT:
{content}
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=instruction,
        config=types.GenerateContentConfig(
            temperature=TEMPERATURE
        )
    )
    
    text = response.text
    if "```python" in text:
        text = text.split("```python")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    return text.strip(), instruction

def process_variation(file_path, var_index, mode="standard"):
    mode_suffix = f"_{mode}" if mode != "standard" else ""
    print(f"Generating {mode} variation {var_index} for {file_path}...")
    with open(file_path, 'r') as f:
        original_content = f.read()
    
    emb_original = get_embedding(original_content)
    
    max_retries = 3
    for attempt in range(max_retries):
        variation_content, used_instruction = paraphrase_prompt(original_content, mode=mode)
        emb_variation = get_embedding(variation_content)
        similarity = calculate_cosine_similarity(emb_original, emb_variation)
        
        # Requirement: if similarity < 5% (0.05), recreate.
        if similarity >= 0.05:
            break
        print(f"Similarity too low ({similarity:.4f}), retrying attempt {attempt+1}...")
    
    # Save the variation
    base_name = os.path.basename(file_path)
    variation_filename = base_name.replace(".py", f"{mode_suffix}_v{var_index}.py")
    output_dir = os.path.dirname(file_path)
    variation_path = os.path.join(output_dir, variation_filename)
    
    with open(variation_path, 'w') as f:
        f.write(variation_content)
    
    # Create log
    log_filename = variation_filename.replace(".py", ".json")
    log_path = os.path.join(output_dir, log_filename)
    
    log_data = {
        "model_name": MODEL_NAME,
        "mode": mode,
        "model_configuration": {
            "temperature": TEMPERATURE,
            "max_retries": max_retries,
            "embedding_model": "models/text-embedding-004"
        },
        "input_prompt": used_instruction,
        "similarity_to_base_prompt": float(similarity),
        "similarity_measure": "Cosine Similarity / Faiss IndexFlatIP",
        "timestamp": time.ctime()
    }
    
    with open(log_path, 'w') as f:
        json.dump(log_data, f, indent=2)
        
    print(f"{mode.capitalize()} Variation {var_index} saved to {variation_path} (Similarity: {similarity:.4f})")

if __name__ == "__main__":
    files = [
        "annotation-guidelines/guidelines_coarse_gollie.py",
        "annotation-guidelines/guidelines_fine_gollie.py"
    ]
    
    for f in files:
        if os.path.exists(f):
            # Generate 3 standard variations
            for i in range(1, 4):
                process_variation(f, i, mode="standard")
            # Generate 3 detailed variations
            for i in range(1, 4):
                process_variation(f, i, mode="detailed")
        else:
            print(f"File not found: {f}")
