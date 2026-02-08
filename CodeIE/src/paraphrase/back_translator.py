"""
Back-Translation Module

Generates prompt variations by translating to a foreign language and back.
This technique creates paraphrases through the natural variation introduced
by the translation process.

Languages: Chinese, Spanish, Turkish
"""

import os
import logging
import time
from typing import List, Optional, Tuple
from dataclasses import dataclass

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)


# Languages for back-translation
LANGUAGES = ["Chinese", "Spanish", "Turkish"]


@dataclass
class BackTranslationConfig:
    """Configuration for back-translation."""
    model_name: str = "gemini-2.0-flash"
    temperature: float = 1.0  # Increased for more variation
    max_tokens: int = 4096
    max_tokens: int = 4096
    similarity_threshold: float = 0.9
    api_key: Optional[str] = None
    request_delay: float = 10.0  # Delay in seconds between requests to avoid rate limits


TRANSLATE_TO_SYSTEM = """"""


TRANSLATE_TO_TEMPLATE = """### The Variable Technical Translator Prompt

**Target Language:** {target_language}

**Task:** You are a technical localization expert. Translate the provided NLP NER prompt into the **Target Language**.

**CRITICAL TRANSLATION MAP:**
You must replace the following English structural phrases with their natural equivalents in the **Target Language**:

1. "The text is:" ➔ [Translate this phrase]
2. "The named entities in the text:" ➔ [Translate this phrase]
3. "Annotation Guidelines:" ➔ [Translate this phrase]
4. "Extract named entities based on the following categories:" ➔ [Translate this phrase]

**STRICT RULES:**

* **DO NOT TRANSLATE** these exact keys: `art`, `building`, `event`, `location`, `organization`, `other`, `person`, `product`. They must remain in English.
* **TRANSLATE** the actual content of the sample sentences.
* **TRANSLATE** the entity value inside the parentheses to match your translated sentence.
* **FORMAT**: Keep the `(key: value)` structure exactly. Dont translate the key but the value as well. 

---

**SOURCE PROMPT:**

{prompt}

---

**Provide only the translated prompt in the Target Language, nothing else.**

"""


TRANSLATE_BACK_SYSTEM = """"""


TRANSLATE_BACK_TEMPLATE = """You are a technical localization expert. Your task is to translate a prompt from {source_language} back into English. 

**GOAL**: The final output must look exactly like an English NLP research prompt. No {source_language} should remain.

**CRITICAL TRANSLATION SCOPE:**
1. **STRING VALUES**: You MUST translate the content of all string variables (e.g., the text inside `input_text = "..."` or `prompt = "..."`).
2. **DICTIONARY VALUES**: You MUST translate the values associated with the "text" key in dictionary objects (e.g., {{ "text": "..." }}).
3. **MAPPING**: Ensure the translated entity name in the `entity_list.append` line matches the translated sentence in the input variable (e.g., `input_text` or `prompt`).
4. **PROSE**: Translate all comments (#), docstrings, and instructional headers.

**STRICT PRESERVATION RULES (DO NOT CHANGE):**
1. **LABEL LOCK**: Do NOT translate the entity types/categories (e.g., "person", "location", "organization", "building", "event", "art", "product", "other"). These are functional keys.
2. **CODE STRUCTURE**: Keep all Python syntax, function names, variable names (`input_text`, `prompt`, `entity_list`), and indentation exactly as-is.
3. **NO EXPLANATIONS**: Provide only the translated code and text. Do not add "Here is the translation" or any conversational filler.

**SOURCE PROMPT TO TRANSLATE:**
---
{prompt}
---

**Provide the English translation below:**"""


class BackTranslator:
    """
    Generates prompt variations using back-translation.
    
    Translates prompts to Chinese, Spanish, and Turkish, then back to English.
    The natural variation introduced by translation creates semantic paraphrases.
    """
    
    def __init__(self, config: Optional[BackTranslationConfig] = None):
        """
        Initialize the back-translator.
        
        Args:
            config: Configuration for back-translation. Uses defaults if not provided.
        """
        self.config = config or BackTranslationConfig()
        self.languages = LANGUAGES
        
        # Get API key (check both GOOGLE_API_KEY and GEMINI_API_KEY)
        api_key = self.config.api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        
        # Initialize LLM based on model name or availability of API key
        if self.config.model_name.startswith("ollama/") or (not api_key and not self.config.model_name.startswith("gemini")):
             # Use Ollama
             model = self.config.model_name.replace("ollama/", "")
             logger.info(f"Using Ollama with model: {model}")
             self.llm = ChatOllama(
                 model=model,
                 temperature=self.config.temperature,
                 num_ctx=self.config.max_tokens
             )
        else:
            # Default to Google Gemini
            if not api_key:
                raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY environment variable not set for Gemini model")
            
            self.llm = ChatGoogleGenerativeAI(
                model=self.config.model_name,
                temperature=self.config.temperature,
                max_output_tokens=self.config.max_tokens,
                google_api_key=api_key
            )
        
        logger.info(f"Initialized BackTranslator with model: {self.config.model_name}")
    
    def _invoke_with_delay(self, messages):
        """Invoke LLM with rate limiting delay."""
        if self.config.request_delay > 0:
            logger.info(f"Sleeping for {self.config.request_delay}s to respect rate limits...")
            time.sleep(self.config.request_delay)
        return self.llm.invoke(messages)

    def _translate_to(self, prompt: str, target_language: str) -> str:
        """
        Translate a prompt to the target language.
        
        Args:
            prompt: Original English prompt
            target_language: Target language name
        
        Returns:
            Translated prompt
        """
        user_message = TRANSLATE_TO_TEMPLATE.format(
            target_language=target_language,
            prompt=prompt
        )
        
        messages = [
            SystemMessage(content=TRANSLATE_TO_SYSTEM),
            HumanMessage(content=user_message)
        ]
        
        response = self._invoke_with_delay(messages)
        
        # Handle different response formats - content can be a list or string
        content = response.content
        if isinstance(content, list):
            translated = "\n".join(
                str(block.get("text", block) if isinstance(block, dict) else block)
                for block in content
            )
        else:
            translated = str(content)
        
        translated = translated.strip()
        
        # Remove any markdown code block wrappers if present
        if translated.startswith("```"):
            lines = translated.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            translated = "\n".join(lines)
        
        return translated
    
    def _translate_back(self, prompt: str, source_language: str) -> str:
        """
        Translate a prompt back to English.
        
        Args:
            prompt: Prompt in foreign language
            source_language: Source language name
        
        Returns:
            Back-translated English prompt
        """
        user_message = TRANSLATE_BACK_TEMPLATE.format(
            source_language=source_language,
            prompt=prompt
        )
        
        messages = [
            SystemMessage(content=TRANSLATE_BACK_SYSTEM),
            HumanMessage(content=user_message)
        ]
        
        response = self._invoke_with_delay(messages)
        
        # Handle different response formats - content can be a list or string
        content = response.content
        if isinstance(content, list):
            translated = "\n".join(
                str(block.get("text", block) if isinstance(block, dict) else block)
                for block in content
            )
        else:
            translated = str(content)
        
        translated = translated.strip()
        
        # Remove any markdown code block wrappers if present
        if translated.startswith("```"):
            lines = translated.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            translated = "\n".join(lines)
        
        return translated
    
    def back_translate(
        self, 
        prompt: str, 
        target_language: str
    ) -> Tuple[str, str]:
        """
        Perform back-translation through a single language.
        
        Args:
            prompt: Original English prompt
            target_language: Intermediate language for translation
        
        Returns:
            Tuple of (intermediate translation, final back-translation)
        """
        logger.info(f"Back-translating via {target_language}")
        
        # Step 1: Translate to target language
        intermediate = self._translate_to(prompt, target_language)
        logger.debug(f"Intermediate ({target_language}):\n{intermediate[:200]}...")
        
        # Step 2: Translate back to English
        back_translated = self._translate_back(intermediate, target_language)
        logger.debug(f"Back-translated:\n{back_translated[:200]}...")
        
        return intermediate, back_translated
    
    def generate_variations(
        self,
        prompt: str,
        languages: Optional[List[str]] = None
    ) -> List[Tuple[str, str, str]]:
        """
        Generate back-translation variations for all specified languages.
        
        Args:
            prompt: Original English prompt
            languages: List of languages to use (defaults to Chinese, Spanish, Turkish)
        
        Returns:
            List of tuples: (language, intermediate_translation, back_translation)
        """
        languages = languages or self.languages
        variations = []
        
        for lang in languages:
            try:
                intermediate, back_translated = self.back_translate(prompt, lang)
                variations.append((lang, intermediate, back_translated))
            except Exception as e:
                logger.error(f"Back-translation via {lang} failed: {e}")
                # Continue with other languages
        
        return variations


if __name__ == "__main__":
    # Test the back-translator
    test_prompt = '''def named_entity_recognition(input_text):
    """ extract named entities from the input_text . """
    input_text = "Barack Obama was born in Hawaii."
    entity_list = []
    # extracted named entities'''

    translator = BackTranslator()
    
    for lang in ["Chinese"]:
        print(f"\n=== Back-translation via {lang} ===")
        intermediate, result = translator.back_translate(test_prompt, lang)
        print(f"\nIntermediate ({lang}):")
        print(intermediate)
        print(f"\nBack to English:")
        print(result)
