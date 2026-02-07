import unittest
import os
import sys
import logging
import requests
import argparse
from dotenv import load_dotenv
from langchain_ollama import ChatOllama, OllamaLLM
from langchain_core.messages import HumanMessage

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestOllamaModel(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        env_path = os.path.join(project_root, '.env')
        load_dotenv(env_path)
        
        self.base_url = os.getenv("CUSTOM_API_BASE_URL", "http://localhost:11434")
        self.model_name = os.getenv("CUSTOM_MODEL_NAME", "mistral")
        
        logger.info(f"--- Ollama Model Discovery ---")
        logger.info(f"Targeting Code: {self.model_name}")

    def test_00_list_all_models(self):
        """List what models are actually installed on the server"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = [m['name'] for m in response.json().get('models', [])]
                logger.info(f"Available models on server: {models}")
            else:
                logger.error("Failed to list models from API")
        except Exception as e:
            logger.error(f"Error connecting to Ollama to list models: {e}")

    def test_01_mistral_check(self):
        """Test the specified model with the best interface for it"""
        # I updated the main runner logic, so let's mirror it here
        chat_models = ["mistral", "llama", "gemma", "instruct", "chat"]
        is_chat = any(m in self.model_name.lower() for m in chat_models)
        
        if is_chat:
            logger.info(f"Testing {self.model_name} using ChatOllama (Chat API)")
            llm = ChatOllama(model=self.model_name, base_url=self.base_url)
            messages = [HumanMessage(content="Hello!")]
            response = llm.invoke(messages).content
        else:
            logger.info(f"Testing {self.model_name} using OllamaLLM (Completion API)")
            llm = OllamaLLM(model=self.model_name, base_url=self.base_url)
            response = llm.invoke("Hello!")
            
        logger.info(f"Response: '{response.strip()}'")
        self.assertGreater(len(response), 0)

if __name__ == "__main__":
    # Allow overriding model via command line: --model mistral
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('--model', type=str, default=None)
    args, unknown = parser.parse_known_args()
    
    if args.model:
        os.environ["CUSTOM_MODEL_NAME"] = args.model
        print(f"Command line override: Model set to {args.model}")
    
    # Pass only unknown arguments to unittest
    sys.argv = [sys.argv[0]] + unknown
    unittest.main()
