import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def calculate_similarities(model, prompt_files):
    """Calculates a cosine similarity matrix for a list of prompt files."""
    texts = []
    labels = []
    
    for label, path in prompt_files.items():
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                texts.append(f.read().strip())
                labels.append(label)
        else:
            print(f"⚠️ Warning: File not found: {path}")
    
    if not texts:
        return None, None

    # Generate embeddings
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
        print(f"❌ Could not process {setting_name}")
        return

    # Create DataFrame
    df = pd.DataFrame(matrix, index=labels, columns=labels)
    
    # Save CSV
    csv_path = os.path.join(output_dir, f"similarity_{setting_name}.csv")
    df.to_csv(csv_path)
    print(f"💾 Saved CSV: {csv_path}")
    
    # Plot Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df, annot=True, fmt=".3f", cmap="YlGnBu", vmin=0.5, vmax=1.0)
    plt.title(f"Semantic Similarity Heatmap - {setting_name}")
    plt.tight_layout()
    
    # Save Image
    img_path = os.path.join(output_dir, f"heatmap_{setting_name}.png")
    plt.savefig(img_path, dpi=300)
    plt.close()
    print(f"🖼️ Saved Heatmap: {img_path}")

def main():
    # Configuration
    MODEL_NAME = "all-MiniLM-L6-v2"
    BASE_DIR = "/Users/marcrodig/Development/kdai/KDAI-Experiments/CodeIE/prompts/base"
    VARIATION_DIR = "/Users/marcrodig/Development/kdai/KDAI-Experiments/CodeIE/prompts/variations"
    OUTPUT_DIR = "/Users/marcrodig/Development/kdai/KDAI-Experiments/CodeIE/prompts/similarity_analysis"
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"🚀 Initializing Semantic Similarity Script")
    print(f"🤖 Loading Model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    
    settings = ["coarse_nl", "coarse_pl", "fine_nl", "fine_pl"]
    
    for setting in settings:
        process_setting(model, setting, BASE_DIR, VARIATION_DIR, OUTPUT_DIR)
        
    print("\n✅ All similarity analysis complete!")

if __name__ == "__main__":
    main()
