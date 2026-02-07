
import unittest
import os
import logging
import json
from dotenv import load_dotenv
from langchain_ollama import ChatOllama, OllamaLLM
from langchain_core.messages import HumanMessage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestOllamaMistral(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        env_path = os.path.join(project_root, '.env')
        load_dotenv(env_path)
        
        self.base_url = os.getenv("CUSTOM_API_BASE_URL", "http://localhost:11434")
        self.model_name = os.getenv("CUSTOM_MODEL_NAME", "mistral")
        
        logger.info(f"--- Ollama Model Switch Test ---")
        logger.info(f"Targeting Model: {self.model_name}")

    def test_01_completion_interface(self):
        """Test standard completion API"""
        logger.info(f"Testing {self.model_name} with OllamaLLM...")
        llm = OllamaLLM(model=self.model_name, base_url=self.base_url)
        response = llm.invoke("Why is the sky blue? Answer in 5 words.")
        logger.info(f"LLM Response: '{response.strip()}'")
        self.assertGreater(len(response), 0)

    def test_02_chat_interface(self):
        """Test Chat API (Mistral should pass this)"""
        logger.info(f"Testing {self.model_name} with ChatOllama...")
        chat = ChatOllama(model=self.model_name, base_url=self.base_url)
        messages = [HumanMessage(content="Extract organization: Microsoft is based in Redmond.")]
        response = chat.invoke(messages)
        content = response.content.strip()
        logger.info(f"Chat Response: '{content}'")
        self.assertGreater(len(content), 0)
        self.assertIn("Microsoft", content)

if __name__ == "__main__":
    unittest.main()
