"""
CodeIE Prompt Paraphrasing Module

This module provides functionality to create prompt variations using:
1. Direct paraphrasing - Using an LLM to rephrase prompts while preserving semantics
2. Back-translation - Translating to a foreign language and back to English

Both techniques aim to create semantically equivalent prompts for testing
model robustness to prompt wording.
"""

from .paraphraser import DirectParaphraser
from .back_translator import BackTranslator
from .similarity import SemanticSimilarity
from .generate_variations import generate_all_variations

__all__ = [
    "DirectParaphraser",
    "BackTranslator", 
    "SemanticSimilarity",
    "generate_all_variations"
]
