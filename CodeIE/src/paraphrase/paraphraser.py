"""
Direct Paraphrasing Module

Generates prompt variations by asking an LLM to paraphrase the original prompt
while preserving the annotation task semantics and all placeholders.
"""

import os
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass, field

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

logger = logging.getLogger(__name__)


@dataclass
class ParaphraseConfig:
    """Configuration for paraphrasing."""
    model_name: str = "gemini-2.0-flash"
    temperature: float = 0.3
    max_tokens: int = 4096
    num_variations: int = 3
    similarity_threshold: float = 0.9
    api_key: Optional[str] = None


PARAPHRASE_SYSTEM_PROMPT = """You are an expert at paraphrasing prompts for NLP annotation tasks.
Your task is to rephrase prompts while maintaining their exact meaning and functionality.
You must preserve all code structure and placeholders exactly as requested."""

PARAPHRASE_CODE_TEMPLATE = """You are paraphrasing a Python function used for Named Entity Recognition prompt injection.

CRITICAL RULES FOR CODE PROMPTS:
1. PRESERVE THE CODE STRUCTURE EXACTLY.
2. The function signature `def named_entity_recognition(input_text):` MUST NOT CHANGE.
3. The variable `input_text = "..."` MUST NOT CHANGE (except the placeholder).
4. The entity list creation `entity_list = []` and the `entity_list.append(...)` calls MUST BE PRESERVED EXACTLY.
5. ONLY paraphrase the Docstrings (\"\"\"...\"\"\") and Comments (# ...).
6. Do NOT change the keys in the dictionaries (e.g. "text", "type").
7. Do NOT change the return statement or logic.

Original prompt to paraphrase:
---
{prompt}
---

Output only the paraphrased Python code, with the exact same logic but different docstrings/comments."""

PARAPHRASE_NL_TEMPLATE = """Paraphrase the following Natural Language prompt for Named Entity Recognition.

Key requirements:
- Preserve the exact same annotation task
- Keep all placeholders (e.g., {{text}}, {{input_text}}) unchanged
- Ensure the paraphrased prompt guides the model to output ONLY the keys from specified mapping.
- Improve clarity and structure while maintaining the original meaning.

Original prompt to paraphrase:
---
{prompt}
---

Output only the paraphrased text."""


class DirectParaphraser:
    """
    Generates prompt variations using direct LLM paraphrasing.
    
    Uses Google Gemini to create semantically equivalent prompts
    with different wording while preserving all functional elements.
    """
    
    def __init__(self, config: Optional[ParaphraseConfig] = None):
        """
        Initialize the paraphraser.
        
        Args:
            config: Configuration for paraphrasing. Uses defaults if not provided.
        """
        self.config = config or ParaphraseConfig()
        
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
        
        logger.info(f"Initialized DirectParaphraser with model: {self.config.model_name}")
    
    def _build_output_mapping(self, prompt_style: str, entity_types: List[str]) -> str:
        """
        Build the output mapping description based on prompt style.
        
        Args:
            prompt_style: "code" or "nl"
            entity_types: List of valid entity types
        
        Returns:
            JSON-like string describing expected output format
        """
        types_str = ", ".join(f'"{t}"' for t in entity_types[:5])
        if len(entity_types) > 5:
            types_str += ", ..."
        
        if prompt_style == "code":
            return f"List of dictionaries with keys 'text' and 'type' (some of: {types_str})"
        else:
            return f"Format: Text: ... Entities: type : text ; type : text ..."
    
    def paraphrase(self, prompt: str, prompt_style: str = "nl") -> str:
        """
        Generate a paraphrase of the prompt.
        
        Args:
            prompt: The original prompt text
            prompt_style: "code" (pl) or "nl"
            
        Returns:
            Paraphrased prompt text
        """
        # Select template based on style
        if prompt_style == "pl" or "def named_entity_recognition" in prompt:
            template = PARAPHRASE_CODE_TEMPLATE
        else:
            template = PARAPHRASE_NL_TEMPLATE

        # Create message with explicit output mapping if available (mocked for now as we don't have types here easily)
        # Actually the template doesn't use output_mapping anymore for code style to be stricter.
        
        content = template.format(
            prompt=prompt
        )
        
        messages = [
            SystemMessage(content=PARAPHRASE_SYSTEM_PROMPT),
            HumanMessage(content=content)
        ]
        
        try:
            response = self.llm.invoke(messages)
            
            # Safe content extraction
            if isinstance(response.content, list):
                # If content is a list of parts, join the text parts
                text_parts = []
                for part in response.content:
                    if isinstance(part, str):
                        text_parts.append(part)
                    elif hasattr(part, 'text'):
                        text_parts.append(part.text)
                result = "".join(text_parts).strip()
            else:
                result = str(response.content).strip()
            
            # Remove markdown code blocks if present
            if result.startswith("```"):
                lines = result.split("\n")
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                result = "\n".join(lines).strip()
            
            return result
            
        except Exception as e:
            logger.error(f"Paraphrasing failed: {e}")
            raise
    
    def generate_variations(
        self,
        prompt: str,
        prompt_style: str = "code",
        entity_types: Optional[List[str]] = None,
        num_variations: Optional[int] = None
    ) -> List[str]:
        """
        Generate multiple paraphrased variations of the prompt.
        
        Args:
            prompt: Original prompt to paraphrase
            prompt_style: "code" or "nl"
            entity_types: List of valid entity types
            num_variations: Number of variations to generate
        
        Returns:
            List of paraphrased prompts
        """
        n = num_variations or self.config.num_variations
        variations = []
        
        for i in range(n):
            try:
                logger.info(f"Generating paraphrase variation {i+1}/{n}")
                variation = self.paraphrase(prompt, prompt_style, entity_types)
                variations.append(variation)
            except Exception as e:
                logger.error(f"Failed to generate variation {i+1}: {e}")
                # Continue trying to generate remaining variations
        
        return variations


if __name__ == "__main__":
    # Test the paraphraser
    import json
    
    test_prompt = '''def named_entity_recognition(input_text):
    """ extract named entities from the input_text . """
    input_text = "Barack Obama was born in Hawaii."
    entity_list = []
    # extracted named entities
    entity_list.append({"text": "Barack Obama", "type": "person"})
    entity_list.append({"text": "Hawaii", "type": "location"})
# END'''

    config = ParaphraseConfig(num_variations=1)
    paraphraser = DirectParaphraser(config)
    
    result = paraphraser.paraphrase(test_prompt, "code")
    print("Original:")
    print(test_prompt)
    print("\nParaphrased:")
    print(result)
