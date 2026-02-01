import os
import json
import re
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

def get_embedding(text):
    result = client.models.embed_content(
        model="models/text-embedding-004",
        contents=text
    )
    return np.array(result.embeddings[0].values, dtype='float32')

def calculate_cosine_similarity(v1, v2):
    # Normalize vectors for cosine similarity
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    
    # Faiss uses IndexFlatIP for inner product (which is cosine similarity on normalized vectors)
    d = v1.shape[0]
    index = faiss.IndexFlatIP(d)
    index.add(np.array([v1]))
    D, I = index.search(np.array([v2]), 1)
    return float(D[0][0])

def paraphrase_prompt(content):
    prompt = f"""Paraphrase the following prompt that will be used for automated data annotation.
Key requirements:
- Preserve the Annotation Task as well as the structure of the prompt.
- Only use lexical substitutions and syntactic reordering.
- You are only Allowed to rename the class comments in \"\"\" \"\"\" or after # .
- Return the FULL file content with the modifications.

FILE CONTENT:
{content}
"""
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.7
        )
    )
    
    text = response.text
    # Remove markdown code blocks if present
    if "```python" in text:
        text = text.split("```python")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    return text.strip()

def process_file(file_path):
    print(f"Processing {file_path}...")
    with open(file_path, 'r') as f:
        original_content = f.read()
    
    variation_content = paraphrase_prompt(original_content)
    
    # Save the variation
    base_name = os.path.basename(file_path)
    variation_name = base_name.replace(".py", "_variation.py")
    variation_path = os.path.join(os.path.dirname(file_path), variation_name)
    
    with open(variation_path, 'w') as f:
        f.write(variation_content)
    
    print(f"Saved variation to {variation_path}")
    
    # Calculate similarity
    emb_original = get_embedding(original_content)
    emb_variation = get_embedding(variation_content)
    
    similarity = calculate_cosine_similarity(emb_original, emb_variation)
    print(f"Cosine Similarity for {base_name}: {similarity:.4f}")
    
    return similarity

if __name__ == "__main__":
    files = [
        "annotation-guidelines/guidelines_coarse_gollie.py",
        "annotation-guidelines/guidelines_fine_gollie.py"
    ]
    
    for f in files:
        if os.path.exists(f):
            process_file(f)
        else:
            print(f"File not found: {f}")
