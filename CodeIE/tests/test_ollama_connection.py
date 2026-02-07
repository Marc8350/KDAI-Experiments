
import unittest
import os
import logging
import json
from dotenv import load_dotenv

# Import both Chat and standard LLM interfaces
from langchain_ollama import ChatOllama, OllamaLLM
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
        
        logger.info(f"--- Ollama LangChain Diagnostic ---")
        logger.info(f"Base URL: {self.base_url}")
        logger.info(f"Model: {self.model_name}")

    def test_01_ollama_llm_generate(self):
        """Test standard completion (matches your CURL success)"""
        logger.info("Testing OllamaLLM (Completion API)...")
        try:
            llm = OllamaLLM(
                model=self.model_name,
                base_url=self.base_url,
                temperature=0.0
            )
            response = llm.invoke("Why is the sky blue? Answer in 5 words.")
            logger.info(f"OllamaLLM Response: '{response.strip()}'")
            self.assertGreater(len(response), 0, "OllamaLLM returned empty response")
        except Exception as e:
            logger.error(f"OllamaLLM failed: {e}")
            raise

    def test_02_chat_ollama_invoke(self):
        """Test ChatOllama (The interface used in CodeIE)"""
        logger.info("Testing ChatOllama (Chat API)...")
        try:
            chat = ChatOllama(
                model=self.model_name,
                base_url=self.base_url,
                temperature=0.0
            )
            messages = [HumanMessage(content="Why is the sky blue? Answer in 5 words.")]
            response = chat.invoke(messages)
            
            content = response.content.strip()
            logger.info(f"ChatOllama Response content: '{content}'")
            
            # Additional debug info
            if hasattr(response, 'response_metadata'):
                logger.info(f"Metadata: {json.dumps(response.response_metadata, indent=2)}")
            
            self.assertGreater(len(content), 0, "ChatOllama returned empty response. This model might not support the Chat API.")
        except Exception as e:
            logger.error(f"ChatOllama failed: {e}")
            raise

if __name__ == "__main__":
    unittest.main()
