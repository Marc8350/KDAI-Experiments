import json
import os
from pathlib import Path

def find_empty_predictions(batch_dir):
    batch_path = Path(batch_dir)
    results = []

    for file_path in batch_path.glob("*.json"):
        if "summary" in file_path.name.lower():
            continue
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if "sentences" not in data:
                continue
            
            for sentence in data["sentences"]:
                prediction = sentence.get("prediction", [])
                
                # Check for empty predictions OR zero F1 score
                f1_score = sentence.get("score", {}).get("entities", {}).get("f1-score", -1)
                
                if not prediction or f1_score == 0:
                    results.append({
                        "file": file_path.name,
                        "model": data.get("config", {}).get("model_name"),
                        "style": data.get("config", {}).get("style"),
                        "variation": data.get("config", {}).get("variation"),
                        "index": sentence.get("index"),
                        "text": sentence.get("text"),
                        "gold": sentence.get("gold", []),
                        "prediction": prediction,
                        "generated_raw": sentence.get("generated_raw", ""),
                        "f1_score": f1_score,
                        "issue": "Empty Prediction" if not prediction else "Zero F1 Score"
                    })
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")

    output_path = batch_path / "failed_predictions.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    return output_path, len(results)

if __name__ == "__main__":
    batch_dir = "/Users/marcrodig/Development/kdai/KDAI-Experiments/CodeIE/CODEIE-results/batch_20260210_162129"
    out_file, count = find_empty_predictions(batch_dir)
    print(f"Found {count} sentences with empty predictions or 0 F1 score.")
    print(f"Results saved to: {out_file}")
