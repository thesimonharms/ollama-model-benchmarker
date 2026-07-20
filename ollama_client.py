import requests
import json
from typing import List, Dict, Any, Optional

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url

    def chat(self, model: str, messages: List[Dict[str, str]], options: Optional[Dict[str, Any]] = None) -> str:
        """Sends a chat request to Ollama and returns the content of the assistant's response."""
        endpoint = f"{self.base_url}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
            ** (options or {})
        }
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"]
        except Exception as e:
            print(f"Error calling Ollama API: {e}")
            return ""

    def generate(self, model: str, prompt: str, system: Optional[str] = None, options: Optional[Dict[str, Any]] = None) -> str:
        """Sends a generation request to Ollama."""
        endpoint = f"{self.base_url}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "system": system,
            "stream": False,
            ** (options or {})
        }
        try:
            response = requests.post(endpoint, json=payload)
            response.raise_for_status()
            result = response.json()
            return result["response"]
        except Exception as e:
            print(f"Error calling Ollama API: {e}")
            return ""

if __name__ == "__main__":
    # Quick test
    client = OllamaClient()
    res = client.generate("llama3", "Hi")
    print(f"Response: {res}")
