from nervaluate import Evaluator

# Example 1: Direct from article (Strict/Exact/Partial/Type)
print("--- Example from Article ---")

gt = [[
    {"label": "PER", "start": 0, "end": 10},
    {"label": "LOC", "start": 20, "end": 30}
]]

pred_partial = [[
    {"label": "PER", "start": 0, "end": 4},
    {"label": "LOC", "start": 20, "end": 26}
]]

evaluator = Evaluator(gt, pred_partial, tags=['PER', 'LOC'])
results, results_by_tag, evaluator_results, evaluator_results_by_tag = evaluator.evaluate()

print("Partial Results (Micro):")
print("Results keys:", results.keys())

# Example 2: Testing alignment logic for Bag of Entities
print("\n--- Testing Bag-of-Entities Alignment ---")
text = "Apple is an organization. I like Apple."

gt_spans = [[{"label": "ORG", "start": 0, "end": 5}]]

pred_spans = [[{"label": "ORG", "start": 0, "end": 5}]]
evaluator = Evaluator(gt_spans, pred_spans, tags=['ORG'])
print("Hit First Match:")
print(evaluator.evaluate()[0]['strict'])

pred_spans_all = [[
    {"label": "ORG", "start": 0, "end": 5},
    {"label": "ORG", "start": 29, "end": 34}
]]
evaluator = Evaluator(gt_spans, pred_spans_all, tags=['ORG'])
res = evaluator.evaluate()[0]
print("Hit All Matches:")
print(f"Strict F1: {res['strict']['f1']}")
print(f"Precision: {res['strict']['precision']}")
print(f"Recall: {res['strict']['recall']}")
