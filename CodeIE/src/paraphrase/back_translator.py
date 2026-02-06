"""
Back-Translation Module

Generates prompt variations by translating to a foreign language and back.
This technique creates paraphrases through the natural variation introduced
by the translation process.

Languages: Chinese, Spanish, Turkish
"""

import os
import logging
from typing import List, Optional, Tuple
from dataclasses import dataclass

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)


# Languages for back-translation
LANGUAGES = ["Chinese", "Spanish", "Turkish"]


@dataclass
class BackTranslationConfig:
    """Configuration for back-translation."""
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.1  # Lower temp for translation accuracy
    max_tokens: int = 4096
    similarity_threshold: float = 0.9
    api_key: Optional[str] = None


TRANSLATE_TO_SYSTEM = """You are an expert translator. Your task is to translate prompts 
used for NLP annotation tasks while preserving their exact functionality."""


TRANSLATE_TO_TEMPLATE = """Translate the following English prompt into {target_language}.

CRITICAL RULES:
1. Keep all code syntax exactly as-is (function definitions, variable names, brackets, etc.)
2. Keep all placeholders exactly as-is (e.g., {{text}}, {{input_text}}, {{entity_list}})
3. Keep all JSON-like structures exactly as-is
4. Only translate the natural language parts (docstrings, comments, instructions)
5. Preserve line breaks and indentation
6. Do NOT translate entity type names like "person", "location", "organization"

English prompt:
---
{prompt}
---

Provide only the translated prompt in {target_language}, nothing else."""


TRANSLATE_BACK_SYSTEM = """You are an expert translator. Your task is to translate prompts 
back to English while preserving their exact functionality."""


TRANSLATE_BACK_TEMPLATE = """Translate the following {source_language} prompt back into English.

CRITICAL RULES:
1. Keep all code syntax exactly as-is (function definitions, variable names, brackets, etc.)
2. Keep all placeholders exactly as-is (e.g., {{text}}, {{input_text}}, {{entity_list}})
3. Keep all JSON-like structures exactly as-is
4. Only translate the natural language parts (docstrings, comments, instructions)
5. Preserve line breaks and indentation
6. Do NOT translate entity type names like "person", "location", "organization"

{source_language} prompt:
---
{prompt}
---

Provide only the translated prompt in English, nothing else."""


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
        if not api_key:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY environment variable not set")
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=self.config.model_name,
            temperature=self.config.temperature,
            max_output_tokens=self.config.max_tokens,
            google_api_key=api_key
        )
        
        logger.info(f"Initialized BackTranslator with model: {self.config.model_name}")
    
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
        
        response = self.llm.invoke(messages)
        
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
        
        response = self.llm.invoke(messages)
        
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
