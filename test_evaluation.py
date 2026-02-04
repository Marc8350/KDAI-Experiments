"""
Test script for GoLLIE evaluation pipeline.

This script simulates the actual evaluation pipeline used in run_gollie_experiments.py:
1. Creates gold standard entities from dataset labels
2. Creates mock predictions (simulating model output)
3. Runs them through the MyEntityScorer to verify evaluation metrics

This tests the complete evaluation workflow without requiring model inference.
"""

import os
import sys
import re

# Setup paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

GOLLIE_PATH = os.path.join(PROJECT_ROOT, "GoLLIE")
if GOLLIE_PATH not in sys.path:
    sys.path.append(GOLLIE_PATH)

from typing import Dict, List, Type, Any
from src.tasks.utils_typing import Entity
from src.tasks.utils_scorer import SpanScorer
from annotation_guidelines import (
    guidelines_coarse_gollie,
    guidelines_fine_gollie
)


class MyEntityScorer(SpanScorer):
    """Compute the F1 score for Named Entity Recognition Tasks"""
    
    # We will set valid_types dynamically per module
    valid_types: List[Type] = []

    def __call__(self, reference: List[List[Entity]], predictions: List[List[Entity]]) -> Dict[str, Any]:
        output = super().__call__(reference, predictions)
        return {"entities": output["spans"]}


def label_to_classname(label):
    """
    Convert dataset label to PascalCase class name.
    
    Examples:
        'art-broadcastprogram' -> 'ArtBroadcastprogram'
        'location-GPE' -> 'LocationGpe'
        'event-attack/battle/war/militaryconflict' -> 'EventAttackBattleWarMilitaryconflict'
    """
    if label == "O":
        return None
    
    # Convert to lowercase first, then split by delimiters
    label_lower = label.lower()
    # Split by both - and / and capitalize first letter of each part
    parts = re.split(r'[-/]', label_lower)
    # Capitalize first letter of each part to create PascalCase
    return "".join(part.capitalize() for part in parts if part)


def test_evaluation_pipeline_coarse():
    """
    Simulate the evaluation pipeline for coarse-grained entities.
    Tests: label conversion -> entity creation -> scoring
    """
    print("\n" + "="*60)
    print("Testing Coarse-Grained Evaluation Pipeline")
    print("="*60)
    
    # Simulate a sentence with tokens and labels (like from the dataset)
    tokens = ["John", "Doe", "visited", "the", "Louvre", "Museum", "in", "Paris"]
    labels = ["person", "person", "O", "O", "building", "building", "O", "location"]
    
    print(f"\nSample sentence: {' '.join(tokens)}")
    print(f"Labels: {labels}")
    
    # Step 1: Create gold standard entities (simulating what happens in run_experiment)
    gold = []
    for token, label in zip(tokens, labels):
        class_name = label_to_classname(label)
        if class_name:
            entity_class = getattr(guidelines_coarse_gollie, class_name, None)
            if entity_class:
                gold.append(entity_class(span=token))
    
    print(f"\nGold entities created: {len(gold)}")
    for entity in gold:
        print(f"  - {entity.__class__.__name__}(span='{entity.span}')")
    
    # Step 2: Create mock predictions (simulating model output)
    # Scenario: Model correctly predicts 2 entities, misses 1, and has 1 false positive
    Person = getattr(guidelines_coarse_gollie, "Person")
    Building = getattr(guidelines_coarse_gollie, "Building")
    Location = getattr(guidelines_coarse_gollie, "Location")
    Organization = getattr(guidelines_coarse_gollie, "Organization")
    
    predictions = [
        Person(span="John"),      # Correct
        Person(span="Doe"),       # Correct
        Building(span="Louvre"),  # Correct
        # Missing: Building(span="Museum")
        Location(span="Paris"),   # Correct
        Organization(span="Museum"),  # False positive (wrong type)
    ]
    
    print(f"\nPredicted entities: {len(predictions)}")
    for entity in predictions:
        print(f"  - {entity.__class__.__name__}(span='{entity.span}')")
    
    # Step 3: Initialize scorer with valid entity types
    scorer = MyEntityScorer()
    scorer.valid_types = guidelines_coarse_gollie.ENTITY_DEFINITIONS
    
    # Step 4: Run evaluation
    print("\n" + "-"*60)
    print("Running scorer...")
    print("-"*60)
    
    results = scorer(reference=[gold], predictions=[predictions])
    
    # Step 5: Display results
    print("\nEvaluation Results:")
    print(f"  Precision: {results['entities']['precision']:.4f}")
    print(f"  Recall: {results['entities']['recall']:.4f}")
    print(f"  F1 Score: {results['entities']['f1-score']:.4f}")
    
    # Verify results make sense
    # We have 6 gold entities, 5 predictions
    # Expected: some matches, some misses
    all_passed = True
    
    if results['entities']['f1-score'] > 0 and results['entities']['f1-score'] <= 1.0:
        print("\n✓ F1 score is in valid range (0, 1]")
    else:
        print(f"\n✗ F1 score {results['entities']['f1-score']} is out of range!")
        all_passed = False
    
    if results['entities']['precision'] > 0 and results['entities']['precision'] <= 1.0:
        print("✓ Precision is in valid range (0, 1]")
    else:
        print(f"✗ Precision {results['entities']['precision']} is out of range!")
        all_passed = False
    
    if results['entities']['recall'] > 0 and results['entities']['recall'] <= 1.0:
        print("✓ Recall is in valid range (0, 1]")
    else:
        print(f"✗ Recall {results['entities']['recall']} is out of range!")
        all_passed = False
    
    return all_passed


def test_evaluation_pipeline_fine():
    """
    Simulate the evaluation pipeline for fine-grained entities using REAL data.
    Uses actual example from few-nerd test dataset (index 3).
    Tests: label conversion -> entity creation -> scoring (with complex labels)
    """
    print("\n" + "="*60)
    print("Testing Fine-Grained Evaluation Pipeline (Real Data)")
    print("="*60)
    
    # Real example from few-nerd test dataset (index 3)
    # Sentence: "The B-52 pilot, Major Larry G. Messinger, later recalled,"
    tokens = ["The", "B-52", "pilot", ",", "Major", "Larry", "G.", "Messinger", ",", "later", "recalled", ","]
    labels = ["O", "product-other", "O", "O", "O", "person-other", "person-other", "person-other", "O", "O", "O", "O"]
    
    print(f"\nReal example from dataset (index 3):")
    print(f"Sentence: {' '.join(tokens)}")
    print(f"Labels: {labels}")
    
    # Step 1: Create gold standard entities (simulating what happens in run_experiment)
    gold = []
    for token, label in zip(tokens, labels):
        class_name = label_to_classname(label)
        if class_name:
            entity_class = getattr(guidelines_fine_gollie, class_name, None)
            if entity_class:
                gold.append(entity_class(span=token))
            else:
                print(f"✗ WARNING: Class '{class_name}' not found for label '{label}'")
    
    print(f"\nGold entities created: {len(gold)}")
    for entity in gold:
        print(f"  - {entity.__class__.__name__}(span='{entity.span}')")
    
    # Step 2: Create mock predictions (simulating model output)
    # Scenario: Model gets most entities right but makes some mistakes
    ProductOther = getattr(guidelines_fine_gollie, "ProductOther")
    PersonOther = getattr(guidelines_fine_gollie, "PersonOther")
    PersonSoldier = getattr(guidelines_fine_gollie, "PersonSoldier")  # Wrong type for testing
    
    predictions = [
        ProductOther(span="B-52"),      # Correct
        PersonOther(span="Larry"),      # Correct
        PersonOther(span="G."),         # Correct
        PersonOther(span="Messinger"),  # Correct
        # Model incorrectly predicts "Major" as PersonSoldier instead of PersonOther
        PersonSoldier(span="Major"),    # False positive (wrong type)
    ]
    
    print(f"\nPredicted entities: {len(predictions)}")
    for entity in predictions:
        print(f"  - {entity.__class__.__name__}(span='{entity.span}')")
    
    # Step 3: Initialize scorer
    scorer = MyEntityScorer()
    scorer.valid_types = guidelines_fine_gollie.ENTITY_DEFINITIONS
    
    # Step 4: Run evaluation
    print("\n" + "-"*60)
    print("Running scorer...")
    print("-"*60)
    
    results = scorer(reference=[gold], predictions=[predictions])
    
    # Step 5: Display results
    print("\nEvaluation Results:")
    print(f"  Precision: {results['entities']['precision']:.4f}")
    print(f"  Recall: {results['entities']['recall']:.4f}")
    print(f"  F1 Score: {results['entities']['f1-score']:.4f}")
    
    # Verify results
    all_passed = True
    
    if results['entities']['f1-score'] > 0 and results['entities']['f1-score'] <= 1.0:
        print("\n✓ F1 score is in valid range (0, 1]")
    else:
        print(f"\n✗ F1 score {results['entities']['f1-score']} is out of range!")
        all_passed = False
    
    if results['entities']['precision'] > 0 and results['entities']['precision'] <= 1.0:
        print("✓ Precision is in valid range (0, 1]")
    else:
        print(f"✗ Precision {results['entities']['precision']} is out of range!")
        all_passed = False
    
    if results['entities']['recall'] > 0 and results['entities']['recall'] <= 1.0:
        print("✓ Recall is in valid range (0, 1]")
    else:
        print(f"✗ Recall {results['entities']['recall']} is out of range!")
        all_passed = False
    
    return all_passed


def test_perfect_prediction():
    """Test case where predictions exactly match gold standard."""
    print("\n" + "="*60)
    print("Testing Perfect Prediction Scenario")
    print("="*60)
    
    # Create identical gold and predictions
    Person = getattr(guidelines_coarse_gollie, "Person")
    Location = getattr(guidelines_coarse_gollie, "Location")
    
    gold = [
        Person(span="Alice"),
        Location(span="London"),
    ]
    
    predictions = [
        Person(span="Alice"),
        Location(span="London"),
    ]
    
    print(f"Gold: {[f'{e.__class__.__name__}({e.span})' for e in gold]}")
    print(f"Pred: {[f'{e.__class__.__name__}({e.span})' for e in predictions]}")
    
    scorer = MyEntityScorer()
    scorer.valid_types = guidelines_coarse_gollie.ENTITY_DEFINITIONS
    
    results = scorer(reference=[gold], predictions=[predictions])
    
    print(f"\nResults: P={results['entities']['precision']:.4f}, "
          f"R={results['entities']['recall']:.4f}, F1={results['entities']['f1-score']:.4f}")
    
    # Perfect match should give F1 = 1.0
    expected_f1 = 1.0
    tolerance = 0.001
    
    if abs(results['entities']['f1-score'] - expected_f1) < tolerance:
        print(f"✓ Perfect prediction gives F1 ≈ {expected_f1}")
        return True
    else:
        print(f"✗ Expected F1 ≈ {expected_f1}, got {results['entities']['f1-score']}")
        return False


def test_zero_prediction():
    """Test case where model predicts nothing."""
    print("\n" + "="*60)
    print("Testing Zero Prediction Scenario")
    print("="*60)
    
    Person = getattr(guidelines_coarse_gollie, "Person")
    
    gold = [Person(span="Bob")]
    predictions = []
    
    print(f"Gold: {[f'{e.__class__.__name__}({e.span})' for e in gold]}")
    print(f"Pred: {predictions}")
    
    scorer = MyEntityScorer()
    scorer.valid_types = guidelines_coarse_gollie.ENTITY_DEFINITIONS
    
    results = scorer(reference=[gold], predictions=[predictions])
    
    print(f"\nResults: P={results['entities']['precision']:.4f}, "
          f"R={results['entities']['recall']:.4f}, F1={results['entities']['f1-score']:.4f}")
    
    # Zero predictions should give recall = 0
    if results['entities']['recall'] == 0.0:
        print("✓ Zero predictions gives recall = 0.0")
        return True
    else:
        print(f"✗ Expected recall = 0.0, got {results['entities']['recall']}")
        return False


def main():
    """Run all evaluation pipeline tests."""
    print("\n" + "="*60)
    print("GoLLIE Evaluation Pipeline Test Suite")
    print("="*60)
    print("\nThis test simulates the actual evaluation workflow:")
    print("  1. Convert dataset labels to PascalCase class names")
    print("  2. Create gold standard entity instances")
    print("  3. Create mock prediction entity instances")
    print("  4. Run through MyEntityScorer")
    print("  5. Verify evaluation metrics make sense")
    
    tests = [
        ("Coarse-Grained Pipeline", test_evaluation_pipeline_coarse),
        ("Fine-Grained Pipeline", test_evaluation_pipeline_fine),
        ("Perfect Prediction", test_perfect_prediction),
        ("Zero Prediction", test_zero_prediction),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 All evaluation pipeline tests passed!")
        print("The label conversion and scoring logic is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total_tests - total_passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit(main())
