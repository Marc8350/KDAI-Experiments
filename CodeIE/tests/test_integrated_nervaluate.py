import sys
from pathlib import Path

CODEIE_ROOT = Path(__file__).resolve().parents[1]
if str(CODEIE_ROOT) not in sys.path:
    sys.path.append(str(CODEIE_ROOT))

from src.evaluation_nervaluate import evaluate_with_nervaluate

print("--- Testing Integrated Nervaluate Wrapper ---")

# Mock Data
# Text: "John Smith went to London."
# Indices: 01234567890123456789012345
#          John Smith         London
texts = ["John Smith went to London."]

gold = [[
    {"type": "PER", "text": "John Smith", "start": 0, "end": 10},
    {"type": "LOC", "text": "London", "start": 19, "end": 25}
]]

# Pred (Bag of Entities style - no spans)
pred = [[
    {"type": "PER", "text": "John"},   # Partial overlap
    {"type": "LOC", "text": "London"}  # Exact match
]]

results = evaluate_with_nervaluate(gold, pred, texts, ["PER", "LOC"])
print(f"Type of results: {type(results)}")
print(f"Results: {results}")

try:
    print(f"Strict F1:  {results['overall']['strict']['f1']}")
    print(f"Macro Strict F1: {results['macro']['strict']}")
    print(f"Partial F1: {results['overall']['partial']['f1']}")
    print(f"Macro Partial F1: {results['macro']['partial']}")
    print(f"Exact F1:   {results['overall']['exact']['f1']}")

    len_gold = results['overall']['strict']['actual']
    len_pred = results['overall']['strict']['possible']
    print(f"\nGold Count: {len_gold}")
    print(f"Pred Count: {len_pred}")
    print(f"Strict Correct: {results['overall']['strict']['correct']}")
    print(f"Partial Correct: {results['overall']['partial']['correct']}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
