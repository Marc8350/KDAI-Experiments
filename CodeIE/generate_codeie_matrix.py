import json, glob, os
import pandas as pd
from datetime import datetime

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "batch_20260212_101910")
OUTPUT_CSV  = os.path.join(os.path.dirname(__file__), "codeie_experiment_matrix.csv")

rows = []
for fp in sorted(glob.glob(os.path.join(RESULTS_DIR, "*.json"))):
    with open(fp) as f:
        data = json.load(f)

    # --- parse filename: {gran}_{style}_{variation...}_{model}_{date}_{time}.json ---
    parts = os.path.basename(fp).removesuffix(".json").split("_")
    ts = f"{parts[-2]}_{parts[-1]}"
    try:
        dt = datetime.strptime(ts, "%Y%m%d_%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        dt = "unknown"

    row = {
        "datetime":    dt,
        "granularity": parts[0],
        "style":       parts[1],
        "variation":   "_".join(parts[2:-3]),
        "model":       parts[-3],
        "n_samples":   data.get("processed_count", 0),
    }

    # --- nervaluate strict scores ---
    nerv = data.get("overall_score", {}).get("nervaluate", {})
    strict = nerv.get("overall", {}).get("strict", {})
    row["precision"] = round(strict.get("precision", 0.0), 4)
    row["recall"]    = round(strict.get("recall", 0.0), 4)
    row["micro_f1"]  = round(strict.get("f1", 0.0), 4)
    row["macro_f1"]  = round(nerv.get("macro", {}).get("strict", 0.0), 4)

    # --- per-tag strict f1 ---
    for tag, scores in nerv.get("by_tag", {}).items():
        row[f"f1_{tag}"] = round(scores.get("strict", {}).get("f1", 0.0), 4)

    rows.append(row)

df = pd.DataFrame(rows).sort_values("datetime", ascending=False).reset_index(drop=True)
df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Saved {len(df)} rows × {len(df.columns)} columns to {OUTPUT_CSV}")
