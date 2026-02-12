#!/usr/bin/env python3
"""
Test script to verify nervaluate behavior with edge cases.

Edge cases:
1. Both gold and pred empty
2. Gold empty, pred has entities (should count FPs)
3. Gold has entities, pred empty (should count FNs)
4. Normal case (both have entities)
"""

from nervaluate import Evaluator

def test_case(name, gold, pred, tags):
    """Test a single case and print results."""
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    print(f"Gold: {gold}")
    print(f"Pred: {pred}")
    
    try:
        evaluator = Evaluator(gold, pred, tags=tags, loader="default")
        results = evaluator.evaluate()
        
        # Handle both dict and tuple return types
        if isinstance(results, tuple):
            overall = results[0]
        else:
            overall = results.get('overall', results)
        
        print(f"\n✅ SUCCESS - nervaluate handled this case")
        print(f"Results: {overall}")
        return True, overall
        
    except Exception as e:
        print(f"\n❌ FAILED - nervaluate crashed")
        print(f"Error: {type(e).__name__}: {e}")
        return False, None


def main():
    tags = ["person", "location", "organization"]
    
    print("\n" + "="*60)
    print("NERVALUATE EDGE CASE TESTS")
    print("="*60)
    
    results = {}
    
    # Case 1: Both empty (single sentence)
    results["both_empty_single"] = test_case(
        "Both empty (single sentence)",
        gold=[[]],
        pred=[[]],
        tags=tags
    )
    
    # Case 2: Gold empty, pred has entities (single sentence)
    results["gold_empty_single"] = test_case(
        "Gold empty, pred has entities (single sentence)",
        gold=[[]],
        pred=[[{"label": "person", "start": 0, "end": 5}]],
        tags=tags
    )
    
    # Case 3: Gold has entities, pred empty (single sentence)
    results["pred_empty_single"] = test_case(
        "Gold has entities, pred empty (single sentence)",
        gold=[[{"label": "person", "start": 0, "end": 5}]],
        pred=[[]],
        tags=tags
    )
    
    # Case 4: Normal case (single sentence)
    results["normal_single"] = test_case(
        "Normal case (single sentence)",
        gold=[[{"label": "person", "start": 0, "end": 5}]],
        pred=[[{"label": "person", "start": 0, "end": 5}]],
        tags=tags
    )
    
    # Case 5: Multiple sentences, first is empty
    results["first_empty_multi"] = test_case(
        "Multiple sentences, first is empty",
        gold=[[], [{"label": "person", "start": 0, "end": 5}]],
        pred=[[], [{"label": "person", "start": 0, "end": 5}]],
        tags=tags
    )
    
    # Case 6: Multiple sentences, first gold empty but pred has entities
    results["first_gold_empty_multi"] = test_case(
        "Multiple sentences, first gold empty but pred has entities",
        gold=[[], [{"label": "person", "start": 0, "end": 5}]],
        pred=[[{"label": "location", "start": 0, "end": 3}], [{"label": "person", "start": 0, "end": 5}]],
        tags=tags
    )
    
    # Case 7: All sentences empty
    results["all_empty_multi"] = test_case(
        "All sentences empty",
        gold=[[], [], []],
        pred=[[], [], []],
        tags=tags
    )
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for success, _ in results.values() if success)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    print("\nDetails:")
    for name, (success, _) in results.items():
        status = "✅" if success else "❌"
        print(f"  {status} {name}")
    
    # What we learned
    print("\n" + "="*60)
    print("CONCLUSIONS")
    print("="*60)
    
    failed_cases = [name for name, (success, _) in results.items() if not success]
    if failed_cases:
        print("\nnervaluate CANNOT handle these cases:")
        for case in failed_cases:
            print(f"  - {case}")
        print("\nWe need to handle these in our wrapper function.")
    else:
        print("\nnervaluate handles all edge cases correctly!")


if __name__ == "__main__":
    main()
