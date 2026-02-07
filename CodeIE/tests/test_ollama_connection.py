
import unittest
import os
import logging
import json
import requests
from dotenv import load_dotenv
from langchain_ollama import ChatOllama, OllamaLLM
from langchain_core.messages import HumanMessage

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
        
        logger.info(f"--- Ollama Deep Diagnostic ---")
        logger.info(f"Model: {self.model_name}")

    def test_01_exact_curl_mirror(self):
        """Test with the exact same prompt and settings as your successful CURL"""
        logger.info("Test 1: Mirroring your successful CURL prompt...")
        try:
            # We use OllamaLLM as it maps 1:1 to the /api/generate used by CURL
            llm = OllamaLLM(
                model=self.model_name,
                base_url=self.base_url,
                # Using default temperature (omit) to match CURL exactly
            )
            prompt = "Why is the sky blue?"
            response = llm.invoke(prompt)
            
            logger.info(f"Response (length {len(response)}): '{response[:50]}...'")
            
            # If this is still 'User', falcon might be sensitive to the User-Agent or slight header diffs
            self.assertGreater(len(response), 10, "Response is too short compared to CURL!")
            self.assertNotIn("User", response[:10], "Model is hallucinating 'User' tag again.")
            
        except Exception as e:
            logger.error(f"CURL Mirror failed: {e}")
            raise

    def test_02_ner_style_test(self):
        """Test a tiny NER task to see if it handles CodeIE style prompts"""
        logger.info("Test 2: Tiny NER task (CodeIE logic)...")
        try:
            chat = ChatOllama(
                model=self.model_name,
                base_url=self.base_url,
                temperature=0.0
            )
            # Simulating a CodeIE style prompt
            ner_prompt = """Extract organization entities:
Input: Apple is based in Cupertino.
Output: [('Apple', 'organization')]
Input: Microsoft is in Redmond.
Output:"""
            
            messages = [HumanMessage(content=ner_prompt)]
            response = chat.invoke(messages)
            content = response.content.strip()
            
            logger.info(f"NER Response: '{content}'")
            self.assertIn("Microsoft", content, "Model failed to extract entity in few-shot test")
            
        except Exception as e:
            logger.error(f"NER Test failed: {e}")
            raise

if __name__ == "__main__":
    unittest.main()
