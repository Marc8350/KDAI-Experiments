import os
import deepl
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_deepl():
    auth_key = os.getenv("DEEPL_API_KEY")
    if not auth_key:
        print("❌ Error: DEEPL_API_KEY not found in .env")
        return

    print(f"Connecting to DeepL with key: {auth_key[:10]}...")
    
    try:
        translator = deepl.DeepLClient(auth_key)
        
        test_text = "I love developing AI agents with DeepL."
        target_lang = "DE" # German
        
        print(f"\nTesting Translation: '{test_text}' -> {target_lang}")
        result = translator.translate_text(test_text, target_lang=target_lang)
        intermediate = result.text
        print(f"Result: {intermediate}")
        
        print(f"\nTesting Back-Translation: {target_lang} -> EN-US")
        result_back = translator.translate_text(intermediate, target_lang="EN-US")
        final = result_back.text
        print(f"Result: {final}")
        
        print("\n✅ DeepL API is working correctly!")
        
    except Exception as e:
        print(f"❌ DeepL API Error: {e}")

if __name__ == "__main__":
    test_deepl()
