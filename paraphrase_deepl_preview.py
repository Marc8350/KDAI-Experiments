import os
import re
import deepl
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get API key from .env
auth_key = os.getenv("DEEPL_API_KEY")

if not auth_key:
    # Set a dummy key if missing to allow dry-run for character counting
    auth_key = "DRY_RUN"

# Initialize DeepL client
try:
    if auth_key != "DRY_RUN":
        deepl_client = deepl.DeepLClient(auth_key)
    else:
        deepl_client = None
except Exception as e:
    print(f"Error initializing DeepLClient: {e}")
    deepl_client = None

# Tracker for character counts
char_counter = 0

def back_translate(text, target_lang, dry_run=True):
    """Paraphrases text by translating to target_lang and back to English."""
    global char_counter
    if not text.strip():
        return text
    
    # Count characters for both directions (English -> Target and Target -> English)
    # Note: Precise character count for the back path is estimated based on source length
    char_counter += len(text) * 2 
    
    if dry_run or not deepl_client:
        return f"[PARAPHRASED: {text}]"
    
    try:
        # Step 1: Translate to the selected language
        result = deepl_client.translate_text(text, target_lang=target_lang)
        intermediate_text = result.text
        
        # Step 2: Translate back to English
        result_back = deepl_client.translate_text(intermediate_text, target_lang="EN-US")
        return result_back.text
    except Exception as e:
        print(f"  ❌ Translation error ({target_lang}): {e}")
        return text

def preview_processing(source_path):
    print(f"\n🔍 PREVIEWING FIELDS FOR: {source_path}")
    
    if not os.path.exists(source_path):
        print(f"❌ Error: Source file {source_path} not found.")
        return

    with open(source_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 1. Header Preview
    first_15_block = "".join(lines[:15])
    print("\n--- [FIELD 1: HEADER (Lines 1-15)] ---")
    print(first_15_block.strip())
    
    # 2. Content Preview
    rest_lines = lines[15:]
    print("\n--- [FIELDS 2+: SAMPLE CONTENT] ---")
    
    found_count = 0
    for i, line in enumerate(rest_lines):
        # Pattern for input_text = "..."
        input_pattern = r'(input_text\s*=\s*")([^"]+)(")'
        input_match = re.search(input_pattern, line)
        if input_match:
            content = input_match.group(2)
            print(f"Line {i+16} [input_text]: {content}")
            found_count += 1
            
        # Pattern for "text": "..."
        text_pattern = r'("text":\s*")([^"]+)(")'
        text_match = re.search(text_pattern, line)
        if text_match:
            content = text_match.group(2)
            print(f"Line {i+16} [text key]: {content}")
            found_count += 1
            
        if found_count >= 10: # Just show first 10 for preview
            print("... (truncated preview)")
            break

def calculate_total_characters(source_path, num_languages=2):
    global char_counter
    char_counter = 0
    
    if not os.path.exists(source_path):
        return 0
        
    with open(source_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    # Header
    char_counter += len("".join(lines[:15])) * 2
    
    # Rest of the file
    for line in lines[15:]:
        # Find input_text and "text" values
        input_match = re.search(r'input_text\s*=\s*"([^"]+)"', line)
        if input_match:
            char_counter += len(input_match.group(1)) * 2
            
        text_match = re.search(r'"text":\s*"([^"]+)"', line)
        if text_match:
            char_counter += len(text_match.group(1)) * 2
            
    total = char_counter * num_languages
    return total

if __name__ == "__main__":
    base_prompt_file = "/Users/marcrodig/Development/kdai/KDAI-Experiments/CodeIE/prompts/base/fine_pl_1shot.txt"
    
    # 1. Preview the fields we are going to translate
    preview_processing(base_prompt_file)
    
    # 2. Calculate character usage impact (for 2 languages: CH and TU)
    total_chars = calculate_total_characters(base_prompt_file, num_languages=2)
    
    print(f"\n📈 ESTIMATED USAGE IMPACT")
    print(f"Characters detected per file: {char_counter}")
    print(f"Total languages planned: 2 (CH, TU)")
    print(f"Total billing impact: ~{total_chars} characters")
    print(f"Monthly limit remaining: {500000 - total_chars} (assuming 0 used so far)")
    
    if total_chars > 500000:
        print("⚠️ WARNING: This will exceed your monthly limit!")
    else:
        print("✅ This is well within your 500,000 limit.")
