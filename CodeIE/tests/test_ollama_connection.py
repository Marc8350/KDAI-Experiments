
import unittest
import os
import logging
import requests
import json
from dotenv import load_dotenv
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
        
        logger.info(f"--- Ollama NER Diagnostic ---")

    def test_01_verify_basic(self):
        """Re-verify that basic prompt still works"""
        llm = OllamaLLM(model=self.model_name, base_url=self.base_url)
        response = llm.invoke("Why is the sky blue?")
        logger.info(f"Basic Response length: {len(response)}")
        self.assertGreater(len(response), 0)

    def test_02_debug_ner_prompt(self):
        """Test NER prompt and print RAW JSON if it fails"""
        ner_prompt = "Extract organization entities:\nInput: Apple is based in Cupertino.\nOutput: [('Apple', 'organization')]\nInput: Microsoft is in Redmond.\nOutput:"
        
        logger.info("Testing NER prompt via LangChain...")
        llm = OllamaLLM(model=self.model_name, base_url=self.base_url, temperature=0.0)
        response = llm.invoke(ner_prompt)
        
        logger.info(f"NER Response (LangChain): '{response}'")
        
        if not response:
            logger.warning("Empty response. Retrying with RAW API to see metadata...")
            payload = {
                "model": self.model_name,
                "prompt": ner_prompt,
                "stream": False,
                "options": {"temperature": 0.0}
            }
            raw_resp = requests.post(f"{self.base_url}/api/generate", json=payload)
            logger.info(f"Raw API Status: {raw_resp.status_code}")
            try:
                data = raw_resp.json()
                logger.info(f"Raw API JSON Response:\n{json.dumps(data, indent=2)}")
                
                # Check why it stopped
                if data.get("done") and data.get("eval_count") == 0:
                    logger.error("Model stopped immediately without generating any tokens.")
                    logger.error(f"Stop Reason: {data.get('done_reason')} | Context size: {len(data.get('context', []))}")
            except:
                logger.error(f"Raw API Text: {raw_resp.text}")

        self.assertGreater(len(response), 0, "Model returned empty response for NER prompt")

if __name__ == "__main__":
    unittest.main()
