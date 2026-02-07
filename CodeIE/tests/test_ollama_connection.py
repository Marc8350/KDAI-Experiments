
import unittest
import os
import logging
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestOllamaLangChain(unittest.TestCase):
    def setUp(self):
        # Resolve project root to find .env
        # tests/ is inside CodeIE/ which is inside KDAI-Experiments/
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        env_path = os.path.join(project_root, '.env')
        
        load_dotenv(env_path)
        
        self.base_url = os.getenv("CUSTOM_API_BASE_URL", "http://localhost:11434")
        self.model_name = os.getenv("CUSTOM_MODEL_NAME", "falcon")
        
        logger.info(f"Connecting to Ollama via LangChain")
        logger.info(f"Base URL: {self.base_url}")
        logger.info(f"Model: {self.model_name}")

    def test_ollama_inference(self):
        """Test basic inference using ChatOllama wrapper"""
        try:
            # Initialize ChatOllama
            llm = ChatOllama(
                model=self.model_name,
                base_url=self.base_url,
                temperature=0.0,
                num_predict=50
            )
            
            # Simple test message
            messages = [
                HumanMessage(content="Hello! Please respond with exactly the word 'ACKNOWLEDGED' if you can hear me.")
            ]
            
            logger.info("Sending request to Ollama...")
            response = llm.invoke(messages)
            
            content = response.content.strip()
            logger.info(f"Model Response: {content}")
            
            self.assertGreater(len(content), 0, "Model returned empty response")
            # We don't strictly assert 'ACKNOWLEDGED' in case the model is talkative, 
            # but we verify we got content back.
            
        except Exception as e:
            self.fail(f"Ollama LangChain inference failed: {e}")

if __name__ == "__main__":
    unittest.main()
