
import unittest
import sys
import os
import shutil
import tempfile
import logging

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from run_gollie_experiments import process_module, MODULE_MAP

# Configure logging to see output
logging.basicConfig(level=logging.INFO)

class TestRunGollieReal(unittest.TestCase):
    """
    Real execution test for GoLLIE experiments.
    WARNING: This test loads the model and runs inference.
    It is designed to run on the remote machine with GPU support.
    It runs only 1 example on 1 module to verify the pipeline.
    """

    def setUp(self):
        # Dynamically pick the first available module to ensure the key exists
        if not MODULE_MAP:
            self.fail("MODULE_MAP is empty. Cannot run test.")
        self.test_module_name = list(MODULE_MAP.keys())[0]
        self.max_examples = 1 # Run only 1 example

    def test_single_module_execution(self):
        print(f"\n[TEST] Running real execution test for {self.test_module_name} with {self.max_examples} example(s)...")
        
        # Run the process_module function directly (synchronously)
        # This bypasses the ProcessPoolExecutor to make debugging easier in the test
        # and avoids pickling issues with unittest if any.
        try:
            result_file = process_module(self.test_module_name, self.max_examples)
            
            print(f"[TEST] Execution finished. Result file: {result_file}")
            
            # Assertions
            self.assertIsNotNone(result_file, "Process failed to return a result filename")
            self.assertTrue(os.path.exists(result_file), f"Result file {result_file} was not created")
            
            # Verify content
            import json
            with open(result_file, 'r') as f:
                data = json.load(f)
                
            self.assertEqual(data["module"], self.test_module_name)
            self.assertEqual(data["processed_count"], 1)
            self.assertTrue(len(data["sentences"]) > 0)
            self.assertIn("score", data["sentences"][0])
            
            print("[TEST] SUCCESS: Pipeline verified with real model.")
            
        except Exception as e:
            self.fail(f"Execution failed with exception: {e}")

if __name__ == '__main__':
    unittest.main()
