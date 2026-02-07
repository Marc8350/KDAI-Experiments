
import unittest
import os
import logging
import json
from dotenv import load_dotenv

# Use OllamaLLM for everything since falcon doesn't like Chat API
from langchain_ollama import OllamaLLM

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestOllamaLangChain(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        env_path = os.path.join(project_root, '.env')
        load_dotenv(env_path)
        
        self.base_url = os.getenv("CUSTOM_API_BASE_URL", "http://localhost:11434")
        self.model_name = os.getenv("CUSTOM_MODEL_NAME", "falcon")
        
        logger.info(f"--- Ollama Logic Verified ---")
        logger.info(f"Model: {self.model_name} | URL: {self.base_url}")

    def test_01_basic_generation(self):
        """Test standard completion"""
        logger.info("Testing Completion API...")
        llm = OllamaLLM(
            model=self.model_name,
            base_url=self.base_url,
            temperature=0.0
        )
        response = llm.invoke("Why is the sky blue?")
        logger.info(f"Response length: {len(response)}")
        self.assertGreater(len(response), 0)

    def test_02_ner_with_llm_interface(self):
        """Test NER prompt using the Completion interface (matches CodeIE fix)"""
        logger.info("Testing NER prompt with OllamaLLM...")
        llm = OllamaLLM(
            model=self.model_name,
            base_url=self.base_url,
            temperature=0.0
        )
        ner_prompt = """Extract organization entities:
Input: Apple is based in Cupertino.
Output: [('Apple', 'organization')]
Input: Microsoft is in Redmond.
Output:"""
        
        response = llm.invoke(ner_prompt)
        content = response.strip()
        logger.info(f"NER Result: '{content}'")
        
        self.assertGreater(len(content), 0, "Model returned empty response")
        # Base models like falcon often append just the result or complete the line
        self.assertTrue("Microsoft" in content or "organization" in content, 
                        f"Expected extraction not found in: {content}")

if __name__ == "__main__":
    unittest.main()
