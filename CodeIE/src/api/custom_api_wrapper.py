"""
Custom API Wrapper for Qwen2.5-7B (OpenAI-compatible endpoint)

This module replaces the OpenAI API wrapper to use a custom endpoint
for the Qwen2.5-7B model. The endpoint is expected to be OpenAI-compatible.
"""

import os
import requests
import json
from typing import Dict, Any, Optional

from src.prompt.constants import END, END_LINE


class CustomAPIWrapper:
    """
    Wrapper for calling a custom OpenAI-compatible API endpoint.
    Designed for Qwen2.5-7B or similar models.
    """
    
    # Default configuration - can be overridden via environment variables
    DEFAULT_BASE_URL = os.getenv("CUSTOM_API_BASE_URL", "http://localhost:8000/v1")
    DEFAULT_API_KEY = os.getenv("CUSTOM_API_KEY", "not-needed")  # Many local endpoints don't require a key
    DEFAULT_MODEL = os.getenv("CUSTOM_MODEL_NAME", "qwen2.5-7b")
    
    @staticmethod
    def call(
        prompt: str,
        max_tokens: int,
        engine: str = None,  # Kept for compatibility, but we use DEFAULT_MODEL
        temperature: float = 0.0,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
        stop: list = None,
        best_of: int = 1,
        base_url: str = None,
        api_key: str = None,
        model: str = None,
    ) -> dict:
        """
        Call the custom API endpoint.
        
        Args:
            prompt: The input prompt text
            max_tokens: Maximum tokens to generate
            engine: Model engine (for backward compatibility, uses model instead)
            temperature: Sampling temperature (0.0 for deterministic)
            top_p: Nucleus sampling parameter
            frequency_penalty: Frequency penalty
            presence_penalty: Presence penalty
            stop: List of stop sequences
            best_of: Number of completions to generate
            base_url: Override the base URL
            api_key: Override the API key
            model: Override the model name
            
        Returns:
            dict: Response in OpenAI format
        """
        # Use provided values or defaults
        base_url = base_url or CustomAPIWrapper.DEFAULT_BASE_URL
        api_key = api_key or CustomAPIWrapper.DEFAULT_API_KEY
        model = model or engine or CustomAPIWrapper.DEFAULT_MODEL
        
        # Set default stop sequences if not provided
        if stop is None:
            stop = [END, END_LINE]
        
        # Build the request payload
        payload = {
            "model": model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "stop": stop,
            "n": 1,  # Number of completions
        }
        
        # Add best_of only if > 1 (some endpoints don't support it)
        if best_of > 1:
            payload["best_of"] = best_of
        
        headers = {
            "Content-Type": "application/json",
        }
        
        # Add authorization header if API key is provided and not empty
        if api_key and api_key != "not-needed":
            headers["Authorization"] = f"Bearer {api_key}"
        
        # Make the API call
        endpoint = f"{base_url.rstrip('/')}/completions"
        
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=120  # 2 minute timeout for long generations
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            # Wrap in a format similar to OpenAI errors for compatibility
            error_response = {
                "error": {
                    "message": str(e),
                    "type": "api_error",
                    "code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
                }
            }
            raise Exception(f"API call failed: {e}")
    
    @staticmethod
    def call_chat(
        messages: list,
        max_tokens: int,
        model: str = None,
        temperature: float = 0.0,
        top_p: float = 1.0,
        stop: list = None,
        base_url: str = None,
        api_key: str = None,
    ) -> dict:
        """
        Alternative method using chat completions API format.
        Some endpoints prefer this format over the completions API.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens to generate
            model: Model name
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            stop: List of stop sequences
            base_url: Override the base URL
            api_key: Override the API key
            
        Returns:
            dict: Response in OpenAI chat format
        """
        base_url = base_url or CustomAPIWrapper.DEFAULT_BASE_URL
        api_key = api_key or CustomAPIWrapper.DEFAULT_API_KEY
        model = model or CustomAPIWrapper.DEFAULT_MODEL
        
        if stop is None:
            stop = [END, END_LINE]
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stop": stop,
        }
        
        headers = {
            "Content-Type": "application/json",
        }
        
        if api_key and api_key != "not-needed":
            headers["Authorization"] = f"Bearer {api_key}"
        
        endpoint = f"{base_url.rstrip('/')}/chat/completions"
        
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Chat API call failed: {e}")
    
    @staticmethod
    def parse_response(response: dict) -> str:
        """
        Parse the API response to extract the generated text.
        
        Args:
            response: The API response dict
            
        Returns:
            str: The generated text
        """
        # Handle both completion and chat completion formats
        if "choices" in response:
            choice = response["choices"][0]
            if "text" in choice:  # Completion API format
                return choice["text"]
            elif "message" in choice:  # Chat API format
                return choice["message"]["content"]
        
        raise ValueError(f"Unexpected response format: {response}")
    
    @staticmethod
    def test_connection(base_url: str = None) -> bool:
        """
        Test if the API endpoint is reachable.
        
        Args:
            base_url: The base URL to test
            
        Returns:
            bool: True if connection successful
        """
        base_url = base_url or CustomAPIWrapper.DEFAULT_BASE_URL
        
        try:
            # Try to hit the models endpoint (common in OpenAI-compatible APIs)
            response = requests.get(
                f"{base_url.rstrip('/')}/models",
                timeout=10
            )
            return response.status_code in [200, 401, 403]  # 401/403 = auth needed but reachable
        except:
            return False


# For backward compatibility with the original OpenAI wrapper
class OpenaiAPIWrapper(CustomAPIWrapper):
    """
    Backward-compatible wrapper that mimics the original OpenAI API interface.
    Uses the custom endpoint under the hood.
    """
    pass


if __name__ == "__main__":
    # Test the connection
    print(f"Testing connection to: {CustomAPIWrapper.DEFAULT_BASE_URL}")
    if CustomAPIWrapper.test_connection():
        print("✓ Connection successful!")
    else:
        print("✗ Connection failed. Make sure your API endpoint is running.")
    
    # Example usage
    print("\nExample usage:")
    print("""
    from custom_api_wrapper import CustomAPIWrapper
    
    # Set environment variables or pass directly
    os.environ["CUSTOM_API_BASE_URL"] = "http://localhost:8000/v1"
    os.environ["CUSTOM_MODEL_NAME"] = "qwen2.5-7b"
    
    # Call the API
    response = CustomAPIWrapper.call(
        prompt="def hello_world():",
        max_tokens=100
    )
    
    # Parse the response
    generated_text = CustomAPIWrapper.parse_response(response)
    print(generated_text)
    """)
