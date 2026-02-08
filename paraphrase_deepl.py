import os
import re
import deepl
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get API key from .env
auth_key = os.getenv("DEEPL_API_KEY")

if not auth_key:
    print("❌ Error: DEEPL_API_KEY not found in .env")
    exit(1)

# Initialize DeepL client
try:
    deepl_client = deepl.DeepLClient(auth_key)
except Exception as e:
    print(f"❌ Error initializing DeepLClient: {e}")
    exit(1)

import time

# Tracker for character counts
total_billing_chars = 0

def back_translate(text, target_lang, max_retries=3):
    """Paraphrases text by translating to target_lang and back to English with retries."""
    global total_billing_chars
    if not text.strip():
        return text
    
    # Small delay between calls to avoid hitting rate limits too fast
    time.sleep(0.5)

    for attempt in range(max_retries):
        try:
            # Step 1: Translate to the selected language
            result = deepl_client.translate_text(text, target_lang=target_lang)
            intermediate_text = result.text
            
            # Step 2: Translate back to English
            result_back = deepl_client.translate_text(intermediate_text, target_lang="EN-US")
            
            # Log chars
            total_billing_chars += len(text)
            total_billing_chars += len(intermediate_text)
            
            return result_back.text
        except deepl.TooManyRequestsException:
            wait_time = (attempt + 1) * 5
            print(f"  ⚠️ Rate limit hit. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}...")
            time.sleep(wait_time)
        except Exception as e:
            print(f"  ❌ Translation error ({target_lang}): {e}")
            if "Too Many Requests" in str(e):
                wait_time = (attempt + 1) * 5
                time.sleep(wait_time)
                continue
            return text
    return text

def process_file(source_path, target_lang, output_path):
    print(f"\n🚀 Processing: {source_path}")
    print(f"🌍 Target Language: {target_lang}")
    
    if not os.path.exists(source_path):
        print(f"❌ Error: Source file {source_path} not found.")
        return

    with open(source_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # 1. Back-translate the first 15 lines as a single block (Instructions & Schema)
    first_15_block = "".join(lines[:15])
    print(f"🔄 Paraphrasing Header (Lines 1-15)...")
    paraphrased_header = back_translate(first_15_block, target_lang)
    if not paraphrased_header.endswith('\n'):
        paraphrased_header += '\n'
    
    # 2. Process the rest of the lines for input_text content and 'text' key values
    processed_lines = []
    rest_lines = lines[15:]
    
    for i, line in enumerate(rest_lines):
        modified_line = line
        
        # Pattern for input_text = "..."
        input_pattern = r'(input_text\s*=\s*")([^"]+)(")'
        input_match = re.search(input_pattern, modified_line)
        if input_match:
            prefix, content, suffix = input_match.groups()
            new_content = back_translate(content, target_lang)
            modified_line = modified_line.replace(f'{prefix}{content}{suffix}', f'{prefix}{new_content}{suffix}')
            
        # Pattern for "text": "..." 
        text_pattern = r'("text":\s*")([^"]+)(")'
        text_match = re.search(text_pattern, modified_line)
        if text_match:
            prefix, content, suffix = text_match.groups()
            new_content = back_translate(content, target_lang)
            modified_line = modified_line.replace(f'{prefix}{content}{suffix}', f'{prefix}{new_content}{suffix}')
            
        processed_lines.append(modified_line)
    
    # Reassemble and save
    final_content = paraphrased_header + "".join(processed_lines)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_content)
    
    print(f"✅ Successfully saved to {output_path}")

if __name__ == "__main__":
    base_prompt_file = "/Users/marcrodig/Development/kdai/KDAI-Experiments/CodeIE/prompts/base/fine_pl_1shot.txt"
    
    tasks = [
        ("ZH", "backtrans_ch.txt"), # Chinese
        ("TR", "backtrans_tu.txt"), # Turkish
        ("ES", "backtrans_sp.txt")  # Spanish
    ]
    
    for lang_code, out_filename in tasks:
        target_output = f"/Users/marcrodig/Development/kdai/KDAI-Experiments/CodeIE/prompts/variations/fine_pl_1shot/{out_filename}"
        process_file(base_prompt_file, lang_code, target_output)

    print(f"\n📊 TOTAL CHARACTERS BILLED: {total_billing_chars}")
