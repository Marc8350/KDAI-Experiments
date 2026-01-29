import os
from google import genai

def load_env():
    env_path = '.env'
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    try:
                        key, value = line.strip().split('=', 1)
                        if (value.startswith('"') and value.endswith('"')) or \
                           (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                        os.environ[key] = value.strip()
                    except ValueError:
                        continue
load_env()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

try:
    print("Listing models...")
    for model in client.models.list():
        print(model.name)
except Exception as e:
    print(f"Error listing models: {e}")
