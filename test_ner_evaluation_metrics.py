#!/usr/bin/env python3
"""
Test script to verify NER evaluation metrics definitions for strict matching.

This script demonstrates how True Positives (TP), False Positives (FP), and 
False Negatives (FN) are computed in Named Entity Recognition evaluation 
using both nervaluate and the GoLLIE-style evaluation framework.
"""

from typing import List, Dict
from nervaluate import Evaluator
import sys
import os

# Import local evaluation module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'CodeIE'))
from evaluation import evaluate_ner, EvaluationResult


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def test_case_1_perfect_match():
    """Test Case 1: Perfect match - all predictions are correct."""
    print_section("TEST CASE 1: Perfect Match (All Correct)")
    
    text = "Apple Inc. was founded by Steve Jobs in California."
    
    # Gold standard (ground truth)
    gold_entities = [
        {'text': 'Apple Inc.', 'type': 'organization'},
        {'text': 'Steve Jobs', 'type': 'person'},
        {'text': 'California', 'type': 'location'}
    ]
    
    # Predictions (same as gold)
    pred_entities = [
        {'text': 'Apple Inc.', 'type': 'organization'},
        {'text': 'Steve Jobs', 'type': 'person'},
        {'text': 'California', 'type': 'location'}
    ]
    
    print("\nScenario:")
    print(f"Text: \"{text}\"")
    print(f"Gold: {gold_entities}")
    print(f"Pred: {pred_entities}")
    
    # Evaluate using CodeIE evaluation
    result = evaluate_ner([gold_entities], [pred_entities])
    
    print("\n📊 Results:")
    print(f"True Positives (TP):  {result.total_tp}")
    print(f"False Positives (FP): {result.total_fp}")
    print(f"False Negatives (FN): {result.total_fn}")
    print(f"Precision: {result.micro_precision:.2%}")
    print(f"Recall: {result.micro_recall:.2%}")
    print(f"F1-Score: {result.micro_f1:.2%}")
    
    print("\n✅ Expected: TP=3, FP=0, FN=0 (Perfect match)")
    assert result.total_tp == 3, f"Expected TP=3, got {result.total_tp}"
    assert result.total_fp == 0, f"Expected FP=0, got {result.total_fp}"
    assert result.total_fn == 0, f"Expected FN=0, got {result.total_fn}"
    print("✓ Test passed!")


def test_case_2_false_positives():
    """Test Case 2: False Positives - spurious predictions."""
    print_section("TEST CASE 2: False Positives (Spurious Predictions)")
    
    text = "Apple Inc. was founded by Steve Jobs in California."
    
    # Gold standard
    gold_entities = [
        {'text': 'Apple Inc.', 'type': 'organization'},
        {'text': 'Steve Jobs', 'type': 'person'}
    ]
    
    # Predictions include extra spurious entities
    pred_entities = [
        {'text': 'Apple Inc.', 'type': 'organization'},  # TP
        {'text': 'Steve Jobs', 'type': 'person'},      # TP
        {'text': 'California', 'type': 'location'},     # FP (not in gold)
        {'text': 'Inc.', 'type': 'organization'}        # FP (not in gold)
    ]
    
    print("\nScenario:")
    print(f"Text: \"{text}\"")
    print(f"Gold: {gold_entities}")
    print(f"Pred: {pred_entities}")
    
    result = evaluate_ner([gold_entities], [pred_entities])
    
    print("\n📊 Results:")
    print(f"True Positives (TP):  {result.total_tp}")
    print(f"False Positives (FP): {result.total_fp}")
    print(f"False Negatives (FN): {result.total_fn}")
    print(f"Precision: {result.micro_precision:.2%}")
    print(f"Recall: {result.micro_recall:.2%}")
    print(f"F1-Score: {result.micro_f1:.2%}")
    
    print("\n✅ Expected: TP=2, FP=2, FN=0")
    print("   Explanation: 'California' and 'Inc.' are spurious (False Positives)")
    assert result.total_tp == 2, f"Expected TP=2, got {result.total_tp}"
    assert result.total_fp == 2, f"Expected FP=2, got {result.total_fp}"
    assert result.total_fn == 0, f"Expected FN=0, got {result.total_fn}"
    print("✓ Test passed!")


def test_case_3_false_negatives():
    """Test Case 3: False Negatives - missed entities."""
    print_section("TEST CASE 3: False Negatives (Missed Entities)")
    
    text = "Apple Inc. was founded by Steve Jobs in California."
    
    # Gold standard - 3 entities
    gold_entities = [
        {'text': 'Apple Inc.', 'type': 'organization'},
        {'text': 'Steve Jobs', 'type': 'person'},
        {'text': 'California', 'type': 'location'}
    ]
    
    # Predictions - only 1 entity found
    pred_entities = [
        {'text': 'Apple Inc.', 'type': 'organization'}  # TP
        # 'Steve Jobs' and 'California' are missed (FN)
    ]
    
    print("\nScenario:")
    print(f"Text: \"{text}\"")
    print(f"Gold: {gold_entities}")
    print(f"Pred: {pred_entities}")
    
    result = evaluate_ner([gold_entities], [pred_entities])
    
    print("\n📊 Results:")
    print(f"True Positives (TP):  {result.total_tp}")
    print(f"False Positives (FP): {result.total_fp}")
    print(f"False Negatives (FN): {result.total_fn}")
    print(f"Precision: {result.micro_precision:.2%}")
    print(f"Recall: {result.micro_recall:.2%}")
    print(f"F1-Score: {result.micro_f1:.2%}")
    
    print("\n✅ Expected: TP=1, FP=0, FN=2")
    print("   Explanation: 'Steve Jobs' and 'California' were not predicted (False Negatives)")
    assert result.total_tp == 1, f"Expected TP=1, got {result.total_tp}"
    assert result.total_fp == 0, f"Expected FP=0, got {result.total_fp}"
    assert result.total_fn == 2, f"Expected FN=2, got {result.total_fn}"
    print("✓ Test passed!")


def test_case_4_wrong_type():
    """Test Case 4: Wrong entity type - correct text, wrong label."""
    print_section("TEST CASE 4: Wrong Entity Type (Type Error)")
    
    text = "Apple Inc. was founded by Steve Jobs in California."
    
    # Gold standard
    gold_entities = [
        {'text': 'Apple Inc.', 'type': 'organization'},
        {'text': 'Steve Jobs', 'type': 'person'}
    ]
    
    # Predictions with wrong types
    pred_entities = [
        {'text': 'Apple Inc.', 'type': 'product'},      # FP+FN (wrong type)
        {'text': 'Steve Jobs', 'type': 'organization'}  # FP+FN (wrong type)
    ]
    
    print("\nScenario:")
    print(f"Text: \"{text}\"")
    print(f"Gold: {gold_entities}")
    print(f"Pred: {pred_entities}")
    print("\n⚠️  Note: In STRICT mode, wrong type = FP+FN")
    
    result = evaluate_ner([gold_entities], [pred_entities])
    
    print("\n📊 Results:")
    print(f"True Positives (TP):  {result.total_tp}")
    print(f"False Positives (FP): {result.total_fp}")
    print(f"False Negatives (FN): {result.total_fn}")
    print(f"Precision: {result.micro_precision:.2%}")
    print(f"Recall: {result.micro_recall:.2%}")
    print(f"F1-Score: {result.micro_f1:.2%}")
    
    print("\n✅ Expected: TP=0, FP=2, FN=2")
    print("   Explanation: Each wrong type counts as both FP (wrong prediction) and FN (missed correct type)")
    assert result.total_tp == 0, f"Expected TP=0, got {result.total_tp}"
    assert result.total_fp == 2, f"Expected FP=2, got {result.total_fp}"
    assert result.total_fn == 2, f"Expected FN=2, got {result.total_fn}"
    print("✓ Test passed!")


def test_case_5_partial_overlap():
    """Test Case 5: Partial text overlap - not a match in strict mode."""
    print_section("TEST CASE 5: Partial Text Overlap (Not a Match)")
    
    text = "Apple Inc. was founded by Steve Jobs in California."
    
    # Gold standard
    gold_entities = [
        {'text': 'Apple Inc.', 'type': 'organization'},
        {'text': 'Steve Jobs', 'type': 'person'}
    ]
    
    # Predictions with partial text
    pred_entities = [
        {'text': 'Apple', 'type': 'organization'},  # FP+FN (partial match)
        {'text': 'Steve', 'type': 'person'}         # FP+FN (partial match)
    ]
    
    print("\nScenario:")
    print(f"Text: \"{text}\"")
    print(f"Gold: {gold_entities}")
    print(f"Pred: {pred_entities}")
    print("\n⚠️  Note: In STRICT mode, partial text match ≠ correct prediction")
    
    result = evaluate_ner([gold_entities], [pred_entities])
    
    print("\n📊 Results:")
    print(f"True Positives (TP):  {result.total_tp}")
    print(f"False Positives (FP): {result.total_fp}")
    print(f"False Negatives (FN): {result.total_fn}")
    print(f"Precision: {result.micro_precision:.2%}")
    print(f"Recall: {result.micro_recall:.2%}")
    print(f"F1-Score: {result.micro_f1:.2%}")
    
    print("\n✅ Expected: TP=0, FP=2, FN=2")
    print("   Explanation: Partial text matches are not accepted in strict evaluation")
    assert result.total_tp == 0, f"Expected TP=0, got {result.total_tp}"
    assert result.total_fp == 2, f"Expected FP=2, got {result.total_fp}"
    assert result.total_fn == 2, f"Expected FN=2, got {result.total_fn}"
    print("✓ Test passed!")


def test_case_6_nervaluate_span_based():
    """Test Case 6: Span-based evaluation with nervaluate (strict mode)."""
    print_section("TEST CASE 6: Nervaluate Span-Based Evaluation (Strict)")
    
    text = "Apple Inc. was founded by Steve Jobs in California."
    
    # Gold annotations with spans
    gold_spans = [
        [
            {'label': 'organization', 'start': 0, 'end': 10},   # "Apple Inc."
            {'label': 'person', 'start': 26, 'end': 37},        # "Steve Jobs"
            {'label': 'location', 'start': 41, 'end': 51}       # "California"
        ]
    ]
    
    # Predictions with spans - 2 correct, 1 wrong type
    pred_spans = [
        [
            {'label': 'organization', 'start': 0, 'end': 10},   # TP: correct
            {'label': 'organization', 'start': 26, 'end': 37},  # FP: wrong type (should be person)
            {'label': 'location', 'start': 41, 'end': 51}       # TP: correct
        ]
    ]
    
    print("\nScenario:")
    print(f"Text: \"{text}\"")
    print(f"Gold spans: {gold_spans[0]}")
    print(f"Pred spans: {pred_spans[0]}")
    
    # Evaluate with nervaluate
    evaluator = Evaluator(gold_spans, pred_spans, tags=['organization', 'person', 'location'])
    results = evaluator.evaluate()
    
    # Access strict mode results from nested structure
    strict_results = results['overall']['strict']
    
    print("\n📊 Nervaluate Results (Strict mode):")
    print(f"True Positives (TP):  {strict_results.correct}")
    print(f"False Positives (FP): {strict_results.spurious}")
    print(f"False Negatives (FN): {strict_results.missed + strict_results.incorrect}")
    print(f"Incorrect (Type Error): {strict_results.incorrect}")
    print(f"Precision: {strict_results.precision:.2%}")
    print(f"Recall: {strict_results.recall:.2%}")
    print(f"F1-Score: {strict_results.f1:.2%}")
    
    print("\n✅ Expected: TP=2 (Apple Inc., California), Type Errors=1 (Steve Jobs)")
    print("   Explanation: Steve Jobs has correct span but wrong type → counts as 'incorrect' in nervaluate")
    print("   In strict mode: incorrect entities count as both FP and FN conceptually")
    assert strict_results.correct == 2, f"Expected correct=2, got {strict_results.correct}"
    assert strict_results.incorrect == 1, f"Expected incorrect=1, got {strict_results.incorrect}"
    print("✓ Test passed!")


def print_thesis_paragraph():
    """Print the thesis paragraph explaining the metrics."""
    print_section("THESIS PARAGRAPH: NER Evaluation Metrics (Strict Mode)")
    
    paragraph = """
In Named Entity Recognition (NER) evaluation, the assessment of model performance 
relies on computing precision, recall, and F1-score based on four fundamental 
classification outcomes. Under the **strict matching** criterion employed by both 
the nervaluate library and the GoLLIE evaluation framework, an entity prediction 
is considered correct if and only if both the entity type (label) and the exact 
text span match the gold standard annotation precisely. A **True Positive (TP)** 
occurs when a predicted entity exactly matches a gold entity in both type and 
span boundaries (character-level start and end positions). A **False Positive (FP)** 
corresponds to any predicted entity that does not match a gold entity—this includes 
completely spurious predictions, predictions with incorrect entity types despite 
correct span boundaries, and predictions with incorrect span boundaries. Conversely, 
a **False Negative (FN)** occurs when a gold standard entity is not correctly 
predicted by the system—this encompasses entities that are completely missed by 
the model as well as gold entities for which the model produced a prediction with 
either the wrong type or wrong span boundaries. Notably, **True Negatives (TN)** 
are not computed in NER evaluation, as this would require enumerating all possible 
text spans that were correctly identified as non-entities, which is computationally 
infeasible and provides limited interpretive value for sequence labeling tasks. 
The strict evaluation criterion is stringent: even minor discrepancies such as 
predicting "Apple" instead of "Apple Inc." or labeling "Steve Jobs" as an 
organization rather than a person result in both a false positive (for the 
incorrect prediction) and a false negative (for the missed correct annotation), 
thereby directly impacting both precision and recall metrics.
"""
    
    print(paragraph)


if __name__ == "__main__":
    print()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  NER EVALUATION METRICS VERIFICATION (STRICT MODE)".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "═" * 78 + "╝")
    
    try:
        # Run all test cases
        test_case_1_perfect_match()
        test_case_2_false_positives()
        test_case_3_false_negatives()
        test_case_4_wrong_type()
        test_case_5_partial_overlap()
        test_case_6_nervaluate_span_based()
        
        # Print the thesis paragraph
        print_thesis_paragraph()
        
        # Final summary
        print_section("✅ ALL TESTS PASSED")
        print("\nAll test cases validate the definitions of TP, FP, and FN in strict NER evaluation.")
        print("The thesis paragraph accurately describes these metrics.")
        print("\nKey Takeaways:")
        print("  • Strict mode requires EXACT match of both type AND span")
        print("  • Wrong type = FP + FN (prediction is both wrong and gold is missed)")
        print("  • Partial text match = FP + FN (not accepted in strict mode)")
        print("  • True Negatives (TN) are not computed in NER evaluation")
        print()
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
