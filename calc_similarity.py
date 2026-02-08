#!/Users/marcrodig/Development/kdai/KDAI-Experiments/.venv/bin/python
import argparse
import sys
import os
import faiss
from sentence_transformers import SentenceTransformer

def main():
    parser = argparse.ArgumentParser(description="Calculate semantic similarity between two text files using FAISS.")
    parser.add_argument("file1", type=str, help="Path to the first text file")
    parser.add_argument("file2", type=str, help="Path to the second text file")
    parser.add_argument("--model", type=str, default="all-MiniLM-L6-v2", help="SentenceTransformer model name (default: all-MiniLM-L6-v2)")
    
    args = parser.parse_args()
    
    try:
        with open(args.file1, 'r', encoding='utf-8') as f:
            text1 = f.read().strip()
            
        with open(args.file2, 'r', encoding='utf-8') as f:
            text2 = f.read().strip()
            
        if not text1 or not text2:
            print("Error: One or both files are empty.")
            sys.exit(1)
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading files: {e}")
        sys.exit(1)
        
    print(f"Loading model: {args.model}...")
    try:
        model = SentenceTransformer(args.model)
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)
    
    print("Generating embeddings...")
    # Generate embeddings
    # convert to numpy array explicitly as faiss expects float32
    embedding1 = model.encode(text1, convert_to_numpy=True).astype('float32')
    embedding2 = model.encode(text2, convert_to_numpy=True).astype('float32')
    
    # Reshape for FAISS (1, d)
    embedding1 = embedding1.reshape(1, -1)
    embedding2 = embedding2.reshape(1, -1)
    
    # Normalize vectors for cosine similarity
    faiss.normalize_L2(embedding1)
    faiss.normalize_L2(embedding2)
    
    # Build FAISS index for Inner Product (cosine similarity on normalized vectors)
    d = embedding1.shape[1]
    index = faiss.IndexFlatIP(d)
    index.add(embedding1)
    
    # Search
    D, I = index.search(embedding2, 1)
    
    similarity = D[0][0]
    print(f"\nSemantic Similarity: {similarity:.4f}")
    
if __name__ == "__main__":
    main()
