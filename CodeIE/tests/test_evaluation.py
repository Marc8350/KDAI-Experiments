#!/usr/bin/env python3
"""
Unit Tests for NER Evaluation Module

Tests the evaluation.py module to ensure:
1. Micro F1 is calculated correctly
2. Macro F1 is calculated correctly  
3. Per-type metrics are accurate
4. Edge cases are handled (empty predictions, no matches, etc.)
"""

import unittest
import sys
from pathlib import Path

# Add CodeIE to path
CODEIE_ROOT = Path(__file__).parent.parent
if str(CODEIE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODEIE_ROOT))

from evaluation import (
    evaluate_ner,
    evaluate_predictions,
    EntityMetrics,
    EvaluationResult
)


class TestEntityMetrics(unittest.TestCase):
    """Test the EntityMetrics dataclass."""
    
    def test_perfect_precision(self):
        """Test when all predictions are correct."""
        m = EntityMetrics(entity_type="person", tp=10, fp=0, fn=5)
        self.assertEqual(m.precision, 1.0)
        self.assertAlmostEqual(m.recall, 10/15, places=4)
    
    def test_perfect_recall(self):
        """Test when all gold entities are found."""
        m = EntityMetrics(entity_type="person", tp=10, fp=5, fn=0)
        self.assertEqual(m.recall, 1.0)
        self.assertAlmostEqual(m.precision, 10/15, places=4)
    
    def test_zero_predictions(self):
        """Test when there are no predictions."""
        m = EntityMetrics(entity_type="person", tp=0, fp=0, fn=10)
        self.assertEqual(m.precision, 0.0)
        self.assertEqual(m.recall, 0.0)
        self.assertEqual(m.f1, 0.0)
    
    def test_no_gold_entities(self):
        """Test when there are no gold entities (all FP)."""
        m = EntityMetrics(entity_type="person", tp=0, fp=10, fn=0)
        self.assertEqual(m.precision, 0.0)
        self.assertEqual(m.recall, 0.0)  # 0/0 case
        self.assertEqual(m.f1, 0.0)
        self.assertEqual(m.support, 0)
    
    def test_f1_calculation(self):
        """Test F1 calculation: 2*P*R / (P+R)"""
        # P = 0.8, R = 0.5 -> F1 = 2*0.8*0.5 / 1.3 = 0.615...
        m = EntityMetrics(entity_type="person", tp=8, fp=2, fn=8)
        self.assertAlmostEqual(m.precision, 0.8, places=4)
        self.assertAlmostEqual(m.recall, 0.5, places=4)
        expected_f1 = 2 * 0.8 * 0.5 / (0.8 + 0.5)
        self.assertAlmostEqual(m.f1, expected_f1, places=4)


class TestEvaluateNER(unittest.TestCase):
    """Test the main evaluate_ner function."""
    
    def test_perfect_match(self):
        """Test when predictions match gold exactly."""
        gold = [
            [{'text': 'Apple', 'type': 'organization'}],
            [{'text': 'Paris', 'type': 'location'}, {'text': 'France', 'type': 'location'}]
        ]
        pred = [
            [{'text': 'Apple', 'type': 'organization'}],
            [{'text': 'Paris', 'type': 'location'}, {'text': 'France', 'type': 'location'}]
        ]
        
        result = evaluate_ner(gold, pred)
        
        self.assertEqual(result.total_tp, 3)
        self.assertEqual(result.total_fp, 0)
        self.assertEqual(result.total_fn, 0)
        self.assertEqual(result.micro_f1, 1.0)
        self.assertEqual(result.macro_f1, 1.0)
    
    def test_no_matches(self):
        """Test when nothing matches."""
        gold = [[{'text': 'Apple', 'type': 'organization'}]]
        pred = [[{'text': 'Microsoft', 'type': 'organization'}]]
        
        result = evaluate_ner(gold, pred)
        
        self.assertEqual(result.total_tp, 0)
        self.assertEqual(result.total_fp, 1)
        self.assertEqual(result.total_fn, 1)
        self.assertEqual(result.micro_f1, 0.0)
    
    def test_empty_predictions(self):
        """Test when model predicts nothing."""
        gold = [
            [{'text': 'Apple', 'type': 'organization'}],
            [{'text': 'Paris', 'type': 'location'}]
        ]
        pred = [[], []]
        
        result = evaluate_ner(gold, pred)
        
        self.assertEqual(result.total_tp, 0)
        self.assertEqual(result.total_fp, 0)
        self.assertEqual(result.total_fn, 2)
        self.assertEqual(result.micro_recall, 0.0)
    
    def test_empty_gold(self):
        """Test when gold has no entities but model predicts some."""
        gold = [[], []]
        pred = [
            [{'text': 'Apple', 'type': 'organization'}],
            []
        ]
        
        result = evaluate_ner(gold, pred)
        
        self.assertEqual(result.total_tp, 0)
        self.assertEqual(result.total_fp, 1)
        self.assertEqual(result.total_fn, 0)
        self.assertEqual(result.micro_precision, 0.0)
    
    def test_partial_match(self):
        """Test partial matching scenario."""
        gold = [
            [
                {'text': 'Apple', 'type': 'organization'},
                {'text': 'Google', 'type': 'organization'},
                {'text': 'Paris', 'type': 'location'}
            ]
        ]
        pred = [
            [
                {'text': 'Apple', 'type': 'organization'},  # TP
                {'text': 'Microsoft', 'type': 'organization'},  # FP
                # Missing Google (FN) and Paris (FN)
            ]
        ]
        
        result = evaluate_ner(gold, pred)
        
        self.assertEqual(result.total_tp, 1)  # Apple
        self.assertEqual(result.total_fp, 1)  # Microsoft
        self.assertEqual(result.total_fn, 2)  # Google, Paris
        
        # Precision = 1/2 = 0.5
        # Recall = 1/3 = 0.333
        self.assertAlmostEqual(result.micro_precision, 0.5, places=4)
        self.assertAlmostEqual(result.micro_recall, 1/3, places=4)
    
    def test_type_mismatch(self):
        """Test that type matters for matching."""
        gold = [[{'text': 'Apple', 'type': 'organization'}]]
        pred = [[{'text': 'Apple', 'type': 'product'}]]  # Wrong type!
        
        result = evaluate_ner(gold, pred)
        
        self.assertEqual(result.total_tp, 0)  # Type mismatch
        self.assertEqual(result.total_fp, 1)
        self.assertEqual(result.total_fn, 1)
    
    def test_per_type_metrics(self):
        """Test that per-type metrics are calculated correctly."""
        gold = [
            [
                {'text': 'Apple', 'type': 'organization'},
                {'text': 'Google', 'type': 'organization'},
                {'text': 'Paris', 'type': 'location'},
                {'text': 'London', 'type': 'location'},
            ]
        ]
        pred = [
            [
                {'text': 'Apple', 'type': 'organization'},  # TP
                {'text': 'Paris', 'type': 'location'},  # TP
                {'text': 'Berlin', 'type': 'location'},  # FP
            ]
        ]
        
        result = evaluate_ner(gold, pred)
        
        # Organization: 1 TP, 0 FP, 1 FN (Google) -> P=1.0, R=0.5
        org_metrics = result.per_type_metrics['organization']
        self.assertEqual(org_metrics.tp, 1)
        self.assertEqual(org_metrics.fp, 0)
        self.assertEqual(org_metrics.fn, 1)
        self.assertEqual(org_metrics.precision, 1.0)
        self.assertEqual(org_metrics.recall, 0.5)
        
        # Location: 1 TP, 1 FP (Berlin), 1 FN (London) -> P=0.5, R=0.5
        loc_metrics = result.per_type_metrics['location']
        self.assertEqual(loc_metrics.tp, 1)
        self.assertEqual(loc_metrics.fp, 1)
        self.assertEqual(loc_metrics.fn, 1)
        self.assertEqual(loc_metrics.precision, 0.5)
        self.assertEqual(loc_metrics.recall, 0.5)
    
    def test_macro_vs_micro_f1(self):
        """Test that macro F1 differs from micro F1 when class distribution is imbalanced."""
        # Create imbalanced scenario:
        # Type A: 100 gold, 50 TP, 25 FP, 50 FN -> P=0.667, R=0.5, F1=0.571
        # Type B: 10 gold, 10 TP, 0 FP, 0 FN -> P=1.0, R=1.0, F1=1.0
        
        gold_a = [{'text': f'entity_{i}', 'type': 'type_a'} for i in range(100)]
        gold_b = [{'text': f'b_entity_{i}', 'type': 'type_b'} for i in range(10)]
        
        # Predictions for type A: first 50 correct, 25 wrong
        pred_a = [{'text': f'entity_{i}', 'type': 'type_a'} for i in range(50)]
        pred_a += [{'text': f'wrong_{i}', 'type': 'type_a'} for i in range(25)]
        
        # Predictions for type B: all correct
        pred_b = [{'text': f'b_entity_{i}', 'type': 'type_b'} for i in range(10)]
        
        gold = [gold_a + gold_b]
        pred = [pred_a + pred_b]
        
        result = evaluate_ner(gold, pred)
        
        # Micro: aggregates all
        # Total: TP=60, FP=25, FN=50
        # Micro P = 60/85 = 0.706
        # Micro R = 60/110 = 0.545
        self.assertEqual(result.total_tp, 60)
        self.assertEqual(result.total_fp, 25)
        self.assertEqual(result.total_fn, 50)
        
        # Macro: average of per-type F1s
        # Type A F1 ≈ 0.571
        # Type B F1 = 1.0
        # Macro F1 ≈ 0.786
        
        # The key insight: macro F1 should be higher than micro F1 here
        # because the smaller class (type_b) has perfect F1
        self.assertGreater(result.macro_f1, result.micro_f1)


class TestBackwardsCompatibility(unittest.TestCase):
    """Test backwards compatibility with original evaluate_predictions function."""
    
    def test_evaluate_predictions_returns_dict(self):
        """Test that evaluate_predictions returns expected dict format."""
        gold = [[{'text': 'Apple', 'type': 'organization'}]]
        pred = [[{'text': 'Apple', 'type': 'organization'}]]
        
        result = evaluate_predictions(gold, pred)
        
        # Check all expected keys exist
        self.assertIn('precision', result)
        self.assertIn('recall', result)
        self.assertIn('f1', result)
        self.assertIn('micro_f1', result)
        self.assertIn('macro_f1', result)
        self.assertIn('tp', result)
        self.assertIn('gold_count', result)
        self.assertIn('pred_count', result)
        
        # Check values for perfect match
        self.assertEqual(result['precision'], 1.0)
        self.assertEqual(result['recall'], 1.0)
        self.assertEqual(result['f1'], 1.0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_empty_lists(self):
        """Test with completely empty lists."""
        result = evaluate_ner([], [])
        self.assertEqual(result.micro_f1, 0.0)
        self.assertEqual(result.macro_f1, 0.0)
    
    def test_all_empty_instances(self):
        """Test when all instances are empty."""
        result = evaluate_ner([[], [], []], [[], [], []])
        self.assertEqual(result.total_tp, 0)
        self.assertEqual(result.total_fp, 0)
        self.assertEqual(result.total_fn, 0)
    
    def test_duplicate_entities(self):
        """Test handling of duplicate entities (set-based matching)."""
        # Duplicate in gold should only count once
        gold = [[
            {'text': 'Apple', 'type': 'organization'},
            {'text': 'Apple', 'type': 'organization'},  # Duplicate
        ]]
        pred = [[{'text': 'Apple', 'type': 'organization'}]]
        
        result = evaluate_ner(gold, pred)
        
        # Set-based matching means duplicate gold only counts once
        self.assertEqual(result.total_tp, 1)
        self.assertEqual(result.total_fn, 0)  # Not missing


def print_test_summary(result):
    """Print a summary of test results."""
    print("\n")
    print("=" * 60)
    print("              EVALUATION TESTS SUMMARY")
    print("=" * 60)
    
    tests_run = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = tests_run - failures - errors
    
    print(f"\nTests Run: {tests_run}")
    print(f"Passed:    {passed} ✅")
    print(f"Failed:    {failures} ❌")
    print(f"Errors:    {errors} 💥")
    
    if failures > 0:
        print("\nFailures:")
        for test, trace in result.failures:
            print(f"  - {test}: {trace.split(chr(10))[0]}")
    
    if errors > 0:
        print("\nErrors:")
        for test, trace in result.errors:
            print(f"  - {test}: {trace.split(chr(10))[0]}")
    
    print("=" * 60)
    
    if failures == 0 and errors == 0:
        print("🎉 ALL TESTS PASSED! 🎉")
    
    print()


class TestEvaluationWithInference(unittest.TestCase):
    """
    Integration tests that use real inference outputs.
    
    These tests run actual model inference and evaluate the predictions
    against gold standard entities from the FewNerd dataset.
    
    NOTE: Requires Ollama running with mistral model, same as unit_test_inference.py.
    Skip if model is not available.
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up shared resources for all integration tests."""
        # Import inference dependencies
        try:
            # Add project root to path
            PROJECT_ROOT = Path(__file__).parent.parent.parent
            if str(PROJECT_ROOT) not in sys.path:
                sys.path.insert(0, str(PROJECT_ROOT))
            
            from CodeIE.run_codeie_experiments import (
                get_llm_model, run_inference, parse_nl_style_output,
                ExperimentConfig
            )
            
            cls.get_llm_model = get_llm_model
            cls.run_inference = run_inference
            cls.parse_nl_style_output = parse_nl_style_output
            cls.ExperimentConfig = ExperimentConfig
            
            # Sample text from FewNerd test set
            cls.test_text = "George Hall and His Hotel Taft Orchestra was an American dance band during the swing era."
            
            # Gold entities for this text (FewNerd fine-grained)
            cls.gold_entities = [
                {'text': 'George Hall and His Hotel Taft Orchestra', 'type': 'art-music'},
                {'text': 'American', 'type': 'location-GPE'},
            ]
            
            # Coarse gold entities
            cls.gold_entities_coarse = [
                {'text': 'George Hall and His Hotel Taft Orchestra', 'type': 'art'},
                {'text': 'American', 'type': 'location'},
            ]
            
            # Try to initialize model
            cls.config = ExperimentConfig(
                model_name="mistral",
                api_base_url="http://localhost:11434",
                temperature=0.0,
                max_tokens=256
            )
            
            try:
                cls.llm_model = get_llm_model(cls.config)
                cls.model_available = True
            except Exception as e:
                print(f"⚠️  Model not available: {e}")
                cls.model_available = False
                
        except ImportError as e:
            print(f"⚠️  Could not import inference modules: {e}")
            cls.model_available = False
    
    def test_evaluation_with_real_inference_fine_nl(self):
        """Test evaluation using real Fine NL inference output."""
        if not self.model_available:
            self.skipTest("Model not available - skipping integration test")
        
        # Load prompt
        prompt_path = CODEIE_ROOT / "prompts/base/fine_nl_1shot.txt"
        if not prompt_path.exists():
            self.skipTest(f"Prompt file not found: {prompt_path}")
        
        with open(prompt_path, 'r') as f:
            icl_prompt = f.read()
        
        # Build test query
        test_query = f'The text is "{self.test_text}". The named entities in the text:'
        full_prompt = icl_prompt + "\n" + test_query
        
        # Run inference - use the class-level function reference
        from CodeIE.run_codeie_experiments import run_inference as do_inference
        response = do_inference(full_prompt, self.llm_model, self.config)
        
        # Get entity types for fine-grained
        import json
        
        schema_path = CODEIE_ROOT / "data/entity.schema"
        if schema_path.exists():
            with open(schema_path, 'r') as f:
                schema = json.load(f)
            entity_types = list(schema.get("fine", {}).keys())
        else:
            entity_types = ['person', 'location', 'organization', 'art-music', 'location-GPE']
        
        # Parse predictions
        from CodeIE.run_codeie_experiments import parse_nl_style_output
        parsed_entities = parse_nl_style_output(response, self.test_text, entity_types)
        
        # Evaluate
        gold_list = [self.gold_entities]
        pred_list = [parsed_entities]
        
        result = evaluate_ner(gold_list, pred_list)
        
        # Log results
        print(f"\n--- Integration Test: Fine NL ---")
        print(f"Gold: {self.gold_entities}")
        print(f"Pred: {parsed_entities}")
        print(f"Micro F1: {result.micro_f1:.2%}, Macro F1: {result.macro_f1:.2%}")
        
        # Basic sanity checks - evaluation module must return valid numbers
        self.assertIsInstance(result.micro_f1, float)
        self.assertIsInstance(result.macro_f1, float)
        self.assertGreaterEqual(result.micro_f1, 0.0)
        self.assertLessEqual(result.micro_f1, 1.0)
        self.assertGreaterEqual(result.macro_f1, 0.0)
        self.assertLessEqual(result.macro_f1, 1.0)
        
        # Verify the counts are correct
        # If model predicts nothing: FN = 2 (both gold entities missed)
        # If model predicts something: we should have some counts
        self.assertEqual(result.total_tp + result.total_fn, len(self.gold_entities),
                        "TP + FN should equal gold count")
        
        # Verify to_dict works
        result_dict = result.to_dict()
        self.assertIn('micro', result_dict)
        self.assertIn('macro', result_dict)
    
    def test_evaluation_summary_output(self):
        """Test that the summary output is properly formatted."""
        # Use mock data for this test to verify formatting
        gold = [
            [{'text': 'Apple', 'type': 'organization'}, {'text': 'Paris', 'type': 'location'}],
            [{'text': 'Google', 'type': 'organization'}]
        ]
        pred = [
            [{'text': 'Apple', 'type': 'organization'}],  # Missing Paris
            [{'text': 'Google', 'type': 'organization'}, {'text': 'Berlin', 'type': 'location'}]  # Extra Berlin
        ]
        
        result = evaluate_ner(gold, pred)
        
        # Get summary
        summary = result.summary(include_per_type=True)
        
        # Check summary contains expected sections
        self.assertIn("EVALUATION RESULTS", summary)
        self.assertIn("Micro F1:", summary)
        self.assertIn("Macro F1:", summary)
        self.assertIn("Per-Type Metrics:", summary)
        
        # Check to_dict output
        result_dict = result.to_dict()
        self.assertIn('micro', result_dict)
        self.assertIn('macro', result_dict)
        self.assertIn('per_type', result_dict)
        self.assertIn('counts', result_dict)
        
        print(f"\n--- Summary Test ---")
        print(summary)


if __name__ == '__main__':
    # Run tests and capture results
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestEntityMetrics))
    suite.addTests(loader.loadTestsFromTestCase(TestEvaluateNER))
    suite.addTests(loader.loadTestsFromTestCase(TestBackwardsCompatibility))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Add integration tests (will be skipped if model not available)
    suite.addTests(loader.loadTestsFromTestCase(TestEvaluationWithInference))
    
    # Run with verbosity
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    
    # Print summary
    print_test_summary(result)
    
    sys.exit(0 if result.wasSuccessful() else 1)

