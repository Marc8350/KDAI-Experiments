import json
import os
import glob
import csv
from datetime import datetime

# Directory path
results_dir = "/Users/marcrodig/Development/kdai/KDAI-Experiments/GOLLIE-results"

# Output file
output_file = "/Users/marcrodig/Development/kdai/KDAI-Experiments/GOLLIE-results/gollie_experiment_matrix.csv"

# Fixed columns
fixed_columns = [
    "datetime", "granularity", "style", "variation", "model", "n_samples",
    "precision", "recall", "micro_f1", "macro_f1", "result_file"
]

files = glob.glob(os.path.join(results_dir, "*.json"))
valid_files = [f for f in files if os.path.basename(f).startswith("annotation_guidelines.guidelines_")]

# Normalization mapping
# usage: normalize_map.get(key, key)
normalize_map = {
    "LocationGpe": "LocationGPE",
    "EventAttackBattleWarMilitaryconflict": "EventAttackBattleWarMilitaryConflict",
    "ArtBroadcastprogram": "ArtBroadcastProgram"
}

def normalize_key(key):
    return normalize_map.get(key, key)

# First pass: Collect all unique class names across all files
all_class_keys = set()
file_contents = {} # Cache content to avoid re-reading

for file_path in valid_files:
    try:
        with open(file_path, "r") as f:
            content = json.load(f)
            file_contents[file_path] = content
            
            class_scores = content.get("overall_score", {}).get("entities", {}).get("class_scores", {})
            for key in class_scores.keys():
                norm_key = normalize_key(key)
                all_class_keys.add(norm_key)
                
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

# Sort class keys alphabetically
sorted_class_keys = sorted(list(all_class_keys))

# Create column names for these classes
class_columns = [f"f1_{key}" for key in sorted_class_keys]

# Final column list
all_columns = fixed_columns + class_columns

data_rows = []

# Second pass: Process data
for file_path in valid_files:
    if file_path not in file_contents:
        continue
        
    content = file_contents[file_path]
    filename = os.path.basename(file_path)

    # Parse metadata
    try:
        core_name = filename.replace("annotation_guidelines.guidelines_", "").replace(".json", "")
        parts = core_name.split("_")
        
        # Identify timestamp (YYYYMMDD_HHMMSS)
        if len(parts) >= 2 and len(parts[-1]) == 6 and len(parts[-2]) == 8 and parts[-1].isdigit() and parts[-2].isdigit():
            ts_str = f"{parts[-2]}_{parts[-1]}"
            try:
                dt_obj = datetime.strptime(ts_str, "%Y%m%d_%H%M%S")
                datetime_val = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
                meta_parts = parts[:-2]
            except ValueError:
                 datetime_val = "unknown"
                 meta_parts = parts
        else:
            datetime_val = "unknown"
            meta_parts = parts

        granularity = meta_parts[0] if meta_parts else "unknown"
        
        try:
            g_idx = meta_parts.index("gollie")
            variation_parts = meta_parts[g_idx+1:]
        except ValueError:
            variation_parts = meta_parts[1:] if len(meta_parts) > 1 else []

        variation = "_".join(variation_parts) if variation_parts else "default"

        model_name = content.get("model_load_params", {}).get("model_weights_name_or_path", "unknown")
        if model_name.startswith("HiTZ/"):
            model_name = model_name.replace("HiTZ/", "")
            
        n_samples = content.get("processed_count", 0)
        
        scores = content.get("overall_score", {}).get("entities", {})
        precision = scores.get("precision", 0.0)
        recall = scores.get("recall", 0.0)
        micro_f1 = scores.get("f1-score", 0.0)
        
        class_scores = scores.get("class_scores", {})
        
        # Create a normalized version of class_scores for lookups
        normalized_class_scores = {}
        for k, v in class_scores.items():
            norm_k = normalize_key(k)
            # If duplicates exist (unlikely in one file), last one wins
            normalized_class_scores[norm_k] = v

        # Macro F1
        f1_vals = [c.get("f1-score", 0.0) for c in class_scores.values()]
        macro_f1 = sum(f1_vals) / len(f1_vals) if f1_vals else 0.0
        
        row = {
            "datetime": datetime_val,
            "granularity": granularity,
            "style": "pl",
            "variation": variation,
            "model": model_name,
            "n_samples": n_samples,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "micro_f1": round(micro_f1, 4),
            "macro_f1": round(macro_f1, 4),
            "result_file": filename
        }
        
        # Populate class columns
        for key in sorted_class_keys:
            col_name = f"f1_{key}"
            if key in normalized_class_scores:
                val = normalized_class_scores[key].get("f1-score", 0.0)
                row[col_name] = round(val, 4)
            else:
                row[col_name] = "" 

        data_rows.append(row)

    except Exception as e:
        print(f"Error processing {filename}: {e}")

# Sort by datetime (descending)
data_rows.sort(key=lambda x: x["datetime"], reverse=True)

# Write CSV
with open(output_file, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=all_columns)
    writer.writeheader()
    for r in data_rows:
        writer.writerow(r)

print(f"Matrix saved to {output_file}")
print(f"Total columns: {len(all_columns)}")
