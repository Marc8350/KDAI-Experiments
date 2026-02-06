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
    model_name: str = "gemini-2.5-flash"
    temperature: float = 0.3
    max_tokens: int = 4096
    num_variations: int = 3
    similarity_threshold: float = 0.9
    api_key: Optional[str] = None


PARAPHRASE_SYSTEM_PROMPT = """You are an expert at paraphrasing prompts for NLP annotation tasks.
Your task is to rephrase prompts while maintaining their exact meaning and functionality.
You must preserve all code syntax, variable names, placeholders, and the overall task structure."""


PARAPHRASE_USER_TEMPLATE = """Paraphrase the following prompt that will be used for automated data annotation.

Key requirements:
- Preserve the exact same annotation task
- Keep all placeholders (e.g., {{text}}, {{input_text}}) unchanged
- Keep all code syntax (function definitions, variable names, etc.) exactly as they are
- Ensure the paraphrased prompt guides the model to output ONLY the keys from this mapping dictionary: {output_mapping}
- Base your paraphrase on the content in the original prompt without adding new information
- Improve clarity and structure while maintaining the original meaning
- For code-style prompts: only paraphrase the docstring and comments, not the code structure

Original prompt to paraphrase:
---
{prompt}
---

Provide only the paraphrased prompt, nothing else."""


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
        
        # Get API key
        api_key = self.config.api_key or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
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
        
        if prompt_style == "code" or prompt_style == "pl":
            return f'{{"text": "<entity span>", "type": "one of [{types_str}]"}}'
        else:  # nl style
            return f'"<entity_type> : <entity_span>" where entity_type is one of [{types_str}]'
    
    def paraphrase(
        self, 
        prompt: str, 
        prompt_style: str = "code",
        entity_types: Optional[List[str]] = None
    ) -> str:
        """
        Generate a single paraphrased version of the prompt.
        
        Args:
            prompt: Original prompt to paraphrase
            prompt_style: "code" or "nl" 
            entity_types: List of valid entity types for output mapping
        
        Returns:
            Paraphrased prompt string
        """
        entity_types = entity_types or ["person", "location", "organization", "other"]
        output_mapping = self._build_output_mapping(prompt_style, entity_types)
        
        user_message = PARAPHRASE_USER_TEMPLATE.format(
            output_mapping=output_mapping,
            prompt=prompt
        )
        
        messages = [
            SystemMessage(content=PARAPHRASE_SYSTEM_PROMPT),
            HumanMessage(content=user_message)
        ]
        
        try:
            response = self.llm.invoke(messages)
            paraphrased = response.content.strip()
            
            # Remove any markdown code block wrappers if present
            if paraphrased.startswith("```"):
                lines = paraphrased.split("\n")
                # Remove first and last lines if they're code block markers
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                paraphrased = "\n".join(lines)
            
            return paraphrased
            
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
