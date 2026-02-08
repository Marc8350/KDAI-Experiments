import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# CRITICAL for remote/headless servers: Use the 'Agg' backend to avoid GUI crashes
plt.switch_backend('Agg')

def calculate_similarities(model, prompt_files):
    """Calculates a cosine similarity matrix for a list of prompt files."""
    texts = []
    labels = []
    
    # Sort keys to ensure consistent matrix indexing
    sorted_labels = sorted(prompt_files.keys(), key=lambda x: (x != "Base", x))
    
    for label in sorted_labels:
        path = prompt_files[label]
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    texts.append(content)
                    labels.append(label)
                else:
                    print(f"⚠️ Warning: File is empty: {path}")
        else:
            print(f"⚠️ Warning: File not found: {path}")
    
    if len(texts) < 2:
        print("❌ Error: Not enough files found to create a matrix.")
        return None, None

    # Generate embeddings
    print(f"  Encoding {len(texts)} files...")
    embeddings = model.encode(texts, convert_to_numpy=True).astype('float32')
    
    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)
    
    # Calculate pairwise cosine similarity using dot product on normalized vectors
    # Matrix multiplication: (N x D) @ (D x N) = (N x N)
    similarity_matrix = np.dot(embeddings, embeddings.T)
    
    return similarity_matrix, labels

def process_setting(model, setting_name, base_dir, variation_dir, output_dir):
    print(f"\n📊 Processing Setting: {setting_name}")
    
    # Define the 7 files for the 7x7 matrix
    # Note: 'reodering.txt' is spelled as found in your directory structure
    prompt_files = {
        "Base": os.path.join(base_dir, f"{setting_name}_1shot.txt"),
        "Backtrans CH": os.path.join(variation_dir, setting_name + "_1shot", "backtrans_ch.txt"),
        "Backtrans SP": os.path.join(variation_dir, setting_name + "_1shot", "backtrans_sp.txt"),
        "Backtrans TU": os.path.join(variation_dir, setting_name + "_1shot", "backtrans_tu.txt"),
        "Lexical Sub": os.path.join(variation_dir, setting_name + "_1shot", "lexical_substitution.txt"),
        "Sentence Reorder": os.path.join(variation_dir, setting_name + "_1shot", "sentence_reordering.txt"),
        "Reordering": os.path.join(variation_dir, setting_name + "_1shot", "reodering.txt"),
    }
    
    matrix, labels = calculate_similarities(model, prompt_files)
    
    if matrix is None:
        return

    # Create DataFrame
    df = pd.DataFrame(matrix, index=labels, columns=labels)
    
    # Save CSV
    csv_path = os.path.join(output_dir, f"similarity_{setting_name}.csv")
    df.to_csv(csv_path)
    print(f"  💾 Saved CSV: {csv_path}")
    
    # Plot Heatmap
    plt.figure(figsize=(12, 10))
    # Use a high-contrast color scheme for research visibility
    sns.heatmap(df, annot=True, fmt=".3f", cmap="vlag", center=0.8, vmin=0.5, vmax=1.0)
    plt.title(f"Semantic Similarity Matrix: {setting_name.upper().replace('_', ' ')}")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Save Image
    img_path = os.path.join(output_dir, f"heatmap_{setting_name}.png")
    plt.savefig(img_path, dpi=300)
    plt.close()
    print(f"  🖼️ Saved Heatmap: {img_path}")

def main():
    # Use the script's directory as the project root to make it cross-platform
    ROOT = os.path.dirname(os.path.abspath(__file__))
    MODEL_NAME = "all-MiniLM-L6-v2"
    BASE_DIR = os.path.join(ROOT, "CodeIE/prompts/base")
    VARIATION_DIR = os.path.join(ROOT, "CodeIE/prompts/variations")
    OUTPUT_DIR = os.path.join(ROOT, "CodeIE/prompts/similarity_analysis")
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"🚀 Initializing Semantic Similarity Script")
    print(f"🤖 Loading Transformer Model: {MODEL_NAME}")
    
    try:
        model = SentenceTransformer(MODEL_NAME)
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return
    
    # The 4 settings you requested
    settings = ["coarse_nl", "coarse_pl", "fine_nl", "fine_pl"]
    
    for setting in settings:
        process_setting(model, setting, BASE_DIR, VARIATION_DIR, OUTPUT_DIR)
        
    print(f"\n✅ All analysis files saved in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
