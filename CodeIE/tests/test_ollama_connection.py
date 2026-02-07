
import unittest
import requests
import json
import os
from dotenv import load_dotenv

# LangChain imports
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

class TestOllamaConnection(unittest.TestCase):
    def setUp(self):
        # Load env for CUSTOM_API_BASE_URL if available
        # Find .env in project root (two levels up from tests/)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        load_dotenv(os.path.join(project_root, '.env'))
        
        self.base_url = os.getenv("CUSTOM_API_BASE_URL", "http://localhost:11434")
        self.model_name = os.getenv("CUSTOM_MODEL_NAME", "falcon")
        print(f"\nTesting connection to Ollama at: {self.base_url}")
        print(f"Target model: {self.model_name}")

    def test_01_api_health(self):
        """Check if Ollama server is reachable and running"""
        try:
            # Ollama doesn't have a /health but /api/tags is a good heartbeat
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            self.assertEqual(response.status_code, 200, "Ollama server returned non-200 status")
            print("Successfully reached Ollama server.")
        except requests.exceptions.ConnectionError:
            self.fail(f"Could not connect to Ollama at {self.base_url}. Is it running?")

    def test_02_model_availability(self):
        """Check if the requested model is downloaded and available"""
        response = requests.get(f"{self.base_url}/api/tags")
        models = [m['name'] for m in response.json().get('models', [])]
        
        # Check for partial match (Ollama tags often include :latest)
        found = any(self.model_name in m for m in models)
        self.assertTrue(found, f"Model '{self.model_name}' not found in Ollama. Available: {models}")
        print(f"Model '{self.model_name}' is available.")

    def test_03_raw_api_inference(self):
        """Run a minimal inference using raw requests to test the API directly"""
        payload = {
            "model": self.model_name,
            "prompt": "Say 'Raw API Success'",
            "stream": False,
            "options": {"num_predict": 10}
        }
        
        print("Sending raw API inference request...")
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=30
        )
        
        self.assertEqual(response.status_code, 200, "Inference request failed")
        result = response.json().get("response", "")
        print(f"Raw API Response: {result.strip()}")
        self.assertGreater(len(result), 0, "Model returned an empty response")

    def test_04_langchain_ollama_inference(self):
        """Run a minimal inference using LangChain ChatOllama"""
        print(f"Initializing LangChain ChatOllama with base_url={self.base_url}...")
        
        try:
            llm = ChatOllama(
                model=self.model_name,
                base_url=self.base_url,
                temperature=0,
                num_predict=10
            )
            
            messages = [HumanMessage(content="Say 'LangChain Success'")]
            
            print("Sending LangChain inference request...")
            response = llm.invoke(messages)
            
            print(f"LangChain Response: {response.content.strip()}")
            self.assertGreater(len(response.content), 0, "LangChain returned an empty response")
            
        except Exception as e:
            self.fail(f"LangChain inference failed: {e}")

if __name__ == "__main__":
    unittest.main()
