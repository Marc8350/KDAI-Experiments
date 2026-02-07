import json
import unittest
import os
import sys
import logging
import argparse
from pathlib import Path
from datasets import load_from_disk
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Add module to path
CODEIE_ROOT = Path(__file__).parent.parent
PROJECT_ROOT = CODEIE_ROOT.parent

# Resolve paths
if str(CODEIE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODEIE_ROOT))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Load Env using dotenv
load_dotenv(PROJECT_ROOT / '.env')

from run_codeie_experiments import (
    ExperimentConfig,
    run_inference,
    get_llm_model,
    parse_code_style_output,
    parse_nl_style_output
)


# ============================================================================
# Custom Test Result to Track Results for Summary
# ============================================================================

class TestResultWithSummary(unittest.TestResult):
    """Custom test result that tracks pass/fail for summary."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successes = []
        self.test_details = {}  # Store details for each test
    
    def addSuccess(self, test):
        super().addSuccess(test)
        self.successes.append(test)
        self.test_details[str(test)] = {'status': 'PASSED', 'message': None}
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.test_details[str(test)] = {'status': 'FAILED', 'message': str(err[1])}
    
    def addError(self, test, err):
        super().addError(test, err)
        self.test_details[str(test)] = {'status': 'ERROR', 'message': str(err[1])}
    
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.test_details[str(test)] = {'status': 'SKIPPED', 'message': reason}


class TestInference(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Load dataset once for all tests"""
        test_path = os.path.join(PROJECT_ROOT, 'few-nerd_test')
        if not os.path.exists(test_path):
             raise FileNotFoundError(f"Test dataset not found at {test_path}")
        
        logger.info(f"Loading test data from: {test_path}")
        ds_test = load_from_disk(test_path)
        # Get just the first sentence as requested
        cls.test_sample = ds_test[0]
        cls.tokens = cls.test_sample['tokens']
        cls.text = ' '.join(cls.tokens)
        logger.info(f"Test Sentence: {cls.text}\n")

    def setUp(self):
        # Base config 
        # API Env vars are automatically handled by get_llm_model if set in .env
        self.config = ExperimentConfig(
            num_shots=1,
            seed=42,
            # If CUSTOM_MODEL_NAME is in env, this will be overridden or used as default
            # Defaulting to gemini-1.5-flash as requested standard
            model_name=os.getenv("CUSTOM_MODEL_NAME", "gemini-1.5-flash"), 
            temperature=0.0,
            max_tokens=512,
            # granularity will be set in each test
        )
        
        # Initialize Model
        try:
            self.llm_model = get_llm_model(self.config)
        except Exception as e:
            self.fail(f"Failed to initialize model: {e}")

    def _get_entity_types(self, granularity):
        """Helper to dynamically load entity types for a given granularity from schema file"""
        schema_path = CODEIE_ROOT / "data" / f"few-nerd-{granularity}" / "entity.schema"
        if not schema_path.exists():
            self.fail(f"Schema file not found: {schema_path}")
            
        with open(schema_path, 'r') as f:
            try:
                first_line = f.readline().strip()
                entity_types = json.loads(first_line)
                return entity_types
            except Exception as e:
                self.fail(f"Failed to parse schema file {schema_path}: {e}")

    def _build_pl_test_query(self, text: str) -> str:
        """Build a code-style test query with clear instruction to continue code."""
        # Add explicit instruction for code completion
        return f'''
def named_entity_recognition(input_text):
    """ extract named entities from the input_text . """
    input_text = "{text}"
    entity_list = []
    # Continue by adding entity_list.append statements for each named entity found:'''

    def test_coarse_pl_inference(self):
        """Test Coarse Granularity with Code Style (Python) using Prompts from File"""
        logger.info("\n" + "="*60)
        logger.info("TEST: Coarse PL Inference (Code Style)")
        logger.info("="*60)
        self.config.granularity = "coarse"
        self.config.style = "pl"
        
        # Dynamic Entity Types
        entity_types = self._get_entity_types("coarse")

        # 1. Load ICL Prompt from File
        prompt_path = CODEIE_ROOT / "prompts/base/coarse_pl_1shot.txt"
        if not prompt_path.exists():
            self.fail(f"Prompt file not found: {prompt_path}")
            
        with open(prompt_path, 'r') as f:
            icl_prompt = f.read()

        # 2. Construct Test Input with clear instruction
        test_query = self._build_pl_test_query(self.text)

        full_prompt = icl_prompt + "\n" + test_query
        
        # 3. Run Inference
        response = run_inference(full_prompt, self.llm_model, self.config)
        logger.info(f"Model Response:\n{response[:500]}...")

        # 4. Parse & Validate
        full_output = test_query + response 
        parsed_entities = parse_code_style_output(full_output, entity_types)
        
        logger.info(f"Parsed Entities: {parsed_entities}")
        self.assertIsInstance(parsed_entities, list)
        self.assertTrue(len(parsed_entities) > 0, "Expected at least one entity extracted (Model might not be following code format)")

    def test_coarse_nl_inference(self):
        """Test Coarse Granularity with NL Style (SEL) using Prompts from File"""
        logger.info("\n" + "="*60)
        logger.info("TEST: Coarse NL Inference (Natural Language Style)")
        logger.info("="*60)
        self.config.granularity = "coarse"
        self.config.style = "nl"

        # Dynamic Entity Types
        entity_types = self._get_entity_types("coarse")

        # 1. Load ICL Prompt from File
        prompt_path = CODEIE_ROOT / "prompts/base/coarse_nl_1shot.txt"
        if not prompt_path.exists():
            self.fail(f"Prompt file not found: {prompt_path}")
            
        with open(prompt_path, 'r') as f:
            icl_prompt = f.read()

        # 2. Construct Test Input (Manual Construction)
        test_query = f'The text is "{self.text}". The named entities in the text:'
        
        full_prompt = icl_prompt + "\n" + test_query

        # 3. Run Inference
        response = run_inference(full_prompt, self.llm_model, self.config)
        logger.info(f"Model Response:\n{response[:500]}...")

        # 4. Parse & Validate
        parsed_entities = parse_nl_style_output(response, self.text, entity_types)
        
        logger.info(f"Parsed Entities: {parsed_entities}")
        self.assertIsInstance(parsed_entities, list)
        self.assertTrue(len(parsed_entities) > 0, "Expected at least one entity extracted (Model might be failing or 404ing)")

    def test_fine_pl_inference(self):
        """Test Fine Granularity with Code Style (Python) using Prompts from File
        
        NOTE: This test may fail with chat models (e.g., mistral) on very long prompts.
        Fine-grained PL has 66 entity types and 60+ examples, making the prompt ~680 lines.
        Some models explain the code instead of completing it. This is expected behavior
        and not a bug - consider using code-focused models (codellama, deepseek-coder) 
        or NL style for fine-grained extraction with chat models.
        """
        logger.info("\n" + "="*60)
        logger.info("TEST: Fine PL Inference (Code Style)")
        logger.info("="*60)
        
        # Check if we should skip for known problematic models
        model_name = self.config.model_name.lower()
        skip_models = ['mistral', 'llama', 'gemma']  # Models that struggle with long code prompts
        
        for skip_model in skip_models:
            if skip_model in model_name and 'code' not in model_name:
                logger.warning(f"⚠️  Fine PL test often fails with {model_name} due to very long prompt")
                logger.warning("   Consider using NL style or a code-focused model for fine-grained extraction")
        
        self.config.granularity = "fine"
        self.config.style = "pl"

        # Dynamic Entity Types
        entity_types = self._get_entity_types("fine")
        
        # 1. Load ICL Prompt from File
        prompt_path = CODEIE_ROOT / "prompts/base/fine_pl_1shot.txt"
        if not prompt_path.exists():
            self.fail(f"Prompt file not found: {prompt_path}")
            
        with open(prompt_path, 'r') as f:
            icl_prompt = f.read()

        # 2. Construct Test Input with clear instruction
        test_query = self._build_pl_test_query(self.text)

        full_prompt = icl_prompt + "\n" + test_query
        
        # 3. Run Inference
        response = run_inference(full_prompt, self.llm_model, self.config)
        logger.info(f"Model Response:\n{response[:500]}...")

        # 4. Parse & Validate
        full_output = test_query + response 
        parsed_entities = parse_code_style_output(full_output, entity_types)
        
        logger.info(f"Parsed Entities: {parsed_entities}")
        self.assertIsInstance(parsed_entities, list)
        self.assertTrue(len(parsed_entities) > 0, "Expected at least one entity extracted (Fine PL often fails with chat models - try NL style or code-focused model)")

    def test_fine_nl_inference(self):
        """Test Fine Granularity with NL Style (SEL) using Prompts from File"""
        logger.info("\n" + "="*60)
        logger.info("TEST: Fine NL Inference (Natural Language Style)")
        logger.info("="*60)
        self.config.granularity = "fine"
        self.config.style = "nl"
        
        # Dynamic Entity Types
        entity_types = self._get_entity_types("fine")

        # 1. Load ICL Prompt from File
        prompt_path = CODEIE_ROOT / "prompts/base/fine_nl_1shot.txt"
        if not prompt_path.exists():
            self.fail(f"Prompt file not found: {prompt_path}")
            
        with open(prompt_path, 'r') as f:
            icl_prompt = f.read()

        # 2. Construct Test Input (Manual Construction)
        test_query = f'The text is "{self.text}". The named entities in the text:'
        
        full_prompt = icl_prompt + "\n" + test_query

        # 3. Run Inference
        response = run_inference(full_prompt, self.llm_model, self.config)
        logger.info(f"Model Response:\n{response[:500]}...")

        # 4. Parse & Validate
        parsed_entities = parse_nl_style_output(response, self.text, entity_types)
        
        logger.info(f"Parsed Entities: {parsed_entities}")
        self.assertIsInstance(parsed_entities, list)
        self.assertTrue(len(parsed_entities) > 0, "Expected at least one entity extracted")


def print_summary(result: TestResultWithSummary):
    """Print a clear summary of test results."""
    print("\n")
    print("=" * 70)
    print("                        TEST RESULTS SUMMARY")
    print("=" * 70)
    
    # Define test display names
    test_names = {
        'test_coarse_nl_inference': 'Coarse NL (Natural Language)',
        'test_coarse_pl_inference': 'Coarse PL (Python Code)',
        'test_fine_nl_inference': 'Fine NL (Natural Language)',
        'test_fine_pl_inference': 'Fine PL (Python Code)',
    }
    
    passed = 0
    failed = 0
    
    print()
    print(f"{'Test Name':<40} {'Status':<10} {'Details'}")
    print("-" * 70)
    
    for test_id, details in result.test_details.items():
        # Extract test method name from the test ID
        method_name = test_id.split()[0]  # e.g., "test_coarse_pl_inference"
        display_name = test_names.get(method_name, method_name)
        
        status = details['status']
        
        if status == 'PASSED':
            status_str = "✅ PASSED"
            passed += 1
        elif status == 'FAILED':
            status_str = "❌ FAILED"
            failed += 1
        elif status == 'ERROR':
            status_str = "💥 ERROR"
            failed += 1
        else:
            status_str = "⏭️  SKIPPED"
        
        # Truncate message if too long
        message = details.get('message', '')
        if message and len(message) > 30:
            message = message[:30] + "..."
        
        print(f"{display_name:<40} {status_str:<10} {message}")
    
    print("-" * 70)
    print()
    print(f"Total: {passed + failed} | Passed: {passed} | Failed: {failed}")
    print()
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! 🎉")
    else:
        print(f"⚠️  {failed} test(s) failed. See details above.")
    
    print("=" * 70)
    print()


if __name__ == '__main__':
    # Allow overriding model via command line: --model mistral
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--model', type=str, default=None)
    args, unknown = parser.parse_known_args()
    
    if args.model:
        os.environ["CUSTOM_MODEL_NAME"] = args.model
        logger.info(f"Command line override: Model set to {args.model}")
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestInference)
    
    # Run with custom result
    result = TestResultWithSummary()
    
    print("\n" + "=" * 70)
    print("          CODEIE INFERENCE UNIT TESTS")
    print(f"          Model: {args.model or os.getenv('CUSTOM_MODEL_NAME', 'gemini-1.5-flash')}")
    print("=" * 70)
    
    suite.run(result)
    
    # Print summary
    print_summary(result)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
