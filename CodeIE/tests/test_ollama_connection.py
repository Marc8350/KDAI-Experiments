
import unittest
import os
import logging
import requests
import json
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestOllamaLangChain(unittest.TestCase):
    def setUp(self):
        # Resolve project root to find .env
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        env_path = os.path.join(project_root, '.env')
        
        load_dotenv(env_path)
        
        self.base_url = os.getenv("CUSTOM_API_BASE_URL", "http://localhost:11434")
        self.model_name = os.getenv("CUSTOM_MODEL_NAME", "falcon")
        
        logger.info(f"--- Ollama LangChain Debug Test ---")
        logger.info(f"Targeting: {self.base_url} | Model: {self.model_name}")

    def test_ollama_inference(self):
        """Test inference and debug empty responses"""
        try:
            # 1. Initialize ChatOllama
            llm = ChatOllama(
                model=self.model_name,
                base_url=self.base_url,
                temperature=0.0,
            )
            
            # Simple test message
            prompt_text = "Hello! Please respond with exactly the word 'OK'."
            messages = [HumanMessage(content=prompt_text)]
            
            logger.info(f"Sending request to Ollama Chat API...")
            response = llm.invoke(messages)
            
            content = response.content.strip()
            
            # 2. Log full response metadata for debugging
            logger.info(f"Model response content: '{content}'")
            if hasattr(response, 'response_metadata'):
                logger.info(f"Response Metadata: {json.dumps(response.response_metadata, indent=2)}")
            
            # 3. Fallback: If empty, try raw request to see error
            if len(content) == 0:
                logger.warning("Empty response detected. Attempting raw API call for debugging...")
                raw_payload = {
                    "model": self.model_name,
                    "prompt": prompt_text,
                    "stream": False
                }
                raw_resp = requests.post(f"{self.base_url}/api/generate", json=raw_payload)
                logger.error(f"Raw API Status: {raw_resp.status_code}")
                logger.error(f"Raw API Body: {raw_resp.text}")
                
                self.fail("Model returned empty response content via LangChain. Check 'Raw API Body' logs above.")

            self.assertGreater(len(content), 0, "Model returned empty response")
            
        except Exception as e:
            self.fail(f"Ollama LangChain inference failed: {e}")

if __name__ == "__main__":
    unittest.main()
