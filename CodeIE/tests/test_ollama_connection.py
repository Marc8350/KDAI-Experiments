
import unittest
import requests
import json
import os
from dotenv import load_dotenv

class TestOllamaConnection(unittest.TestCase):
    def setUp(self):
        # Load env for CUSTOM_API_BASE_URL if available
        load_dotenv()
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

    def test_03_inference_basic(self):
        """Run a minimal inference to test the full pipeline"""
        payload = {
            "model": self.model_name,
            "prompt": "Say 'Connection Successful'",
            "stream": False,
            "options": {"num_predict": 10}
        }
        
        print("Sending test inference request...")
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=30
        )
        
        self.assertEqual(response.status_code, 200, "Inference request failed")
        result = response.json().get("response", "")
        print(f"Model Response: {result.strip()}")
        self.assertGreater(len(result), 0, "Model returned an empty response")

if __name__ == "__main__":
    unittest.main()
