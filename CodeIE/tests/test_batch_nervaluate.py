import json
import re
import sys
from pathlib import Path

CODEIE_ROOT = Path(__file__).resolve().parents[1]
if str(CODEIE_ROOT) not in sys.path:
    sys.path.append(str(CODEIE_ROOT))

from src.evaluation_nervaluate import evaluate_with_nervaluate


def parse_entity_string(entity_str):
    match = re.match(r"^([\w-]+)\(span='(.*)'\)$", entity_str)
    if match:
        return {'type': match.group(1), 'text': match.group(2)}
    return None


def test_batch_evaluation():
    batch_file = CODEIE_ROOT / "CODEIE-results" / "batch_20260210_195146" / "coarse_pl_v0_original_qwen2.5-coder:7b_20260210_195146.json"

    if not batch_file.exists():
        print(f"File not found: {batch_file}")
        return

    print(f"Loading results from {batch_file}...")
    with batch_file.open('r') as f:
        data = json.load(f)

    sentences = data.get('sentences', [])
    entity_types = data.get('entity_types', [])

    if not entity_types:
        entity_types = ["person", "organization", "location", "building", "event", "product", "art-work", "other"]

    all_gold = []
    all_pred = []
    all_texts = []

    print(f"Processing {len(sentences)} sentences...")

    for s in sentences:
        text = s['text']
        gold_strs = s['gold']
        pred_strs = s.get('prediction', [])

        gold_objs = [parse_entity_string(g) for g in gold_strs if parse_entity_string(g)]
        pred_objs = [parse_entity_string(p) for p in pred_strs if parse_entity_string(p)]

        all_gold.append(gold_objs)
        all_pred.append(pred_objs)
        all_texts.append(text)

    print("Running Nervaluate...")
    results = evaluate_with_nervaluate(all_gold, all_pred, all_texts, entity_types)

    print("-" * 50)
    print("CodeIE Original Micro F1 (from file):", data.get('overall_score', {}).get('entities', {}).get('micro_f1'))
    print("-" * 50)
    print("Nervaluate Metrics (Recalculated from Bag):")

    overall = results['overall']
    macro = results['macro']

    print(f"Strict:  Micro F1={overall['strict']['f1']:.4f}, Macro F1={macro['strict']:.4f}")
    print(f"Exact:   Micro F1={overall['exact']['f1']:.4f}, Macro F1={macro['exact']:.4f}")
    print(f"Partial: Micro F1={overall['partial']['f1']:.4f}, Macro F1={macro['partial']:.4f}")
    print(f"Type:    Micro F1={overall['ent_type']['f1']:.4f}, Macro F1={macro['ent_type']:.4f}")

    print("-" * 50)
    print("Detailed Stats (Strict):")
    print(f"Correct: {overall['strict']['correct']}")
    print(f"Incorrect: {overall['strict']['incorrect']}")
    print(f"Partial: {overall['strict']['partial']}")
    print(f"Missed: {overall['strict']['missed']}")
    print(f"Spurious: {overall['strict']['spurious']}")


if __name__ == "__main__":
    test_batch_evaluation()
