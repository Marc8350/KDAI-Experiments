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
logging.basicConfig(level=logging.INFO)
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
        logger.info(f"Test Sentence: {cls.text}")

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

    def test_coarse_pl_inference(self):
        """Test Coarse Granularity with Code Style (Python) using Prompts from File"""
        logger.info("\n--- Testing Coarse PL Inference (File-based Prompt) ---")
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

        # 2. Construct Test Input (Manual Construction)
        test_query = f'''
def named_entity_recognition(input_text):
    """ extract named entities from the input_text . """
    input_text = "{self.text}"
    entity_list = []'''

        full_prompt = icl_prompt + "\n" + test_query
        
        # 3. Run Inference
        response = run_inference(full_prompt, self.llm_model, self.config)
        logger.info(f"Model Response:\n{response}")

        # 4. Parse & Validate
        full_output = test_query + response 
        parsed_entities = parse_code_style_output(full_output, entity_types)
        
        logger.info(f"Parsed Entities: {parsed_entities}")
        self.assertIsInstance(parsed_entities, list)
        self.assertTrue(len(parsed_entities) > 0, "Expected at least one entity extracted (Model might be failing or 404ing)")

    def test_coarse_nl_inference(self):
        """Test Coarse Granularity with NL Style (SEL) using Prompts from File"""
        logger.info("\n--- Testing Coarse NL Inference (File-based Prompt) ---")
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
        logger.info(f"Model Response:\n{response}")

        # 4. Parse & Validate
        parsed_entities = parse_nl_style_output(response, self.text, entity_types)
        
        logger.info(f"Parsed Entities: {parsed_entities}")
        self.assertIsInstance(parsed_entities, list)
        self.assertTrue(len(parsed_entities) > 0, "Expected at least one entity extracted (Model might be failing or 404ing)")

    def test_fine_pl_inference(self):
        """Test Fine Granularity with Code Style (Python) using Prompts from File"""
        logger.info("\n--- Testing Fine PL Inference (File-based Prompt) ---")
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

        # 2. Construct Test Input (Manual Construction)
        test_query = f'''
def named_entity_recognition(input_text):
    """ extract named entities from the input_text . """
    input_text = "{self.text}"
    entity_list = []'''

        full_prompt = icl_prompt + "\n" + test_query
        
        # 3. Run Inference
        response = run_inference(full_prompt, self.llm_model, self.config)
        logger.info(f"Model Response:\n{response}")

        # 4. Parse & Validate
        full_output = test_query + response 
        parsed_entities = parse_code_style_output(full_output, entity_types)
        
        logger.info(f"Parsed Entities: {parsed_entities}")
        self.assertIsInstance(parsed_entities, list)
        self.assertTrue(len(parsed_entities) > 0, "Expected at least one entity extracted")

    def test_fine_nl_inference(self):
        """Test Fine Granularity with NL Style (SEL) using Prompts from File"""
        logger.info("\n--- Testing Fine NL Inference (File-based Prompt) ---")
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
        logger.info(f"Model Response:\n{response}")

        # 4. Parse & Validate
        parsed_entities = parse_nl_style_output(response, self.text, entity_types)
        
        logger.info(f"Parsed Entities: {parsed_entities}")
        self.assertIsInstance(parsed_entities, list)
        self.assertTrue(len(parsed_entities) > 0, "Expected at least one entity extracted")

if __name__ == '__main__':
    # Allow overriding model via command line: --model mistral
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--model', type=str, default=None)
    args, unknown = parser.parse_known_args()
    
    if args.model:
        os.environ["CUSTOM_MODEL_NAME"] = args.model
        logger.info(f"Command line override: Model set to {args.model}")
    
    # Pass only unknown arguments to unittest
    sys.argv = [sys.argv[0]] + unknown
    unittest.main()
