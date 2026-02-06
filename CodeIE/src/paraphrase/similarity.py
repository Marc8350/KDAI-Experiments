"""
Semantic Similarity Module

Computes semantic similarity between original and paraphrased prompts
using sentence embeddings. Used to validate that paraphrases maintain
the original meaning above a threshold (0.9 by default).
"""

import logging
from typing import List, Tuple
import numpy as np

logger = logging.getLogger(__name__)

# Try to import sentence-transformers, fall back to basic similarity if not available
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning("sentence-transformers not available. Using basic text similarity.")


class SemanticSimilarity:
    """
    Computes semantic similarity between prompts using sentence embeddings.
    
    Uses the 'all-MiniLM-L6-v2' model for efficient embedding computation.
    Falls back to basic character-level similarity if sentence-transformers
    is not installed.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the similarity calculator.
        
        Args:
            model_name: Name of the sentence-transformers model to use
        """
        self.model_name = model_name
        self.model = None
        
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                logger.info(f"Loading sentence-transformers model: {model_name}")
                self.model = SentenceTransformer(model_name)
                logger.info("Model loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load model: {e}. Using fallback.")
    
    def _cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Compute cosine similarity between two vectors."""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))
    
    def _basic_similarity(self, text1: str, text2: str) -> float:
        """
        Compute basic character-level similarity as fallback.
        Uses Jaccard similarity on character trigrams.
        """
        def get_trigrams(text: str) -> set:
            text = text.lower()
            return set(text[i:i+3] for i in range(len(text) - 2))
        
        trigrams1 = get_trigrams(text1)
        trigrams2 = get_trigrams(text2)
        
        if not trigrams1 or not trigrams2:
            return 0.0
        
        intersection = len(trigrams1 & trigrams2)
        union = len(trigrams1 | trigrams2)
        
        return intersection / union if union > 0 else 0.0
    
    def compute_similarity(self, original: str, variation: str) -> float:
        """
        Compute semantic similarity between original and variation.
        
        Args:
            original: Original prompt text
            variation: Paraphrased prompt text
        
        Returns:
            Similarity score between 0 and 1
        """
        if self.model is not None:
            try:
                embeddings = self.model.encode([original, variation])
                return self._cosine_similarity(embeddings[0], embeddings[1])
            except Exception as e:
                logger.warning(f"Embedding failed: {e}. Using fallback.")
        
        # Fallback to basic similarity
        return self._basic_similarity(original, variation)
    
    def compute_batch_similarity(
        self, 
        original: str, 
        variations: List[str]
    ) -> List[float]:
        """
        Compute similarity for multiple variations against the original.
        
        Args:
            original: Original prompt text
            variations: List of paraphrased prompts
        
        Returns:
            List of similarity scores
        """
        if self.model is not None:
            try:
                all_texts = [original] + variations
                embeddings = self.model.encode(all_texts)
                original_embedding = embeddings[0]
                
                similarities = []
                for i, var_embedding in enumerate(embeddings[1:], 1):
                    sim = self._cosine_similarity(original_embedding, var_embedding)
                    similarities.append(sim)
                
                return similarities
            except Exception as e:
                logger.warning(f"Batch embedding failed: {e}. Using fallback.")
        
        # Fallback to basic similarity
        return [self._basic_similarity(original, var) for var in variations]
    
    def filter_by_threshold(
        self,
        original: str,
        variations: List[str],
        threshold: float = 0.9
    ) -> Tuple[List[str], List[str], List[float]]:
        """
        Filter variations by similarity threshold.
        
        Args:
            original: Original prompt text
            variations: List of paraphrased prompts
            threshold: Minimum similarity score to accept
        
        Returns:
            Tuple of (accepted_variations, rejected_variations, all_scores)
        """
        scores = self.compute_batch_similarity(original, variations)
        
        accepted = []
        rejected = []
        
        for var, score in zip(variations, scores):
            if score >= threshold:
                accepted.append(var)
                logger.info(f"Accepted variation with similarity {score:.4f}")
            else:
                rejected.append(var)
                logger.warning(f"Rejected variation with similarity {score:.4f} (threshold: {threshold})")
        
        return accepted, rejected, scores


if __name__ == "__main__":
    # Test similarity computation
    original = '''def named_entity_recognition(input_text):
    """ extract named entities from the input_text . """
    input_text = "Barack Obama was born in Hawaii."
    entity_list = []
    # extracted named entities'''
    
    variation = '''def named_entity_recognition(input_text):
    """ identify and extract named entities from the given text . """
    input_text = "Barack Obama was born in Hawaii."
    entity_list = []
    # identified named entities'''
    
    different = '''This is a completely different text about something else entirely.'''
    
    sim = SemanticSimilarity()
    
    print(f"Similarity (similar): {sim.compute_similarity(original, variation):.4f}")
    print(f"Similarity (different): {sim.compute_similarity(original, different):.4f}")
