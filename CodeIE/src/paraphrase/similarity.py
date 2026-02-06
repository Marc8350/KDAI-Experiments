"""
Semantic Similarity Module using FAISS

Computes semantic similarity between original and paraphrased prompts
using Google's text embedding API and FAISS IndexFlatIP for cosine similarity.
This matches the GoLLIE paraphrasing implementation.
"""

import os
import logging
from typing import List, Tuple, Optional
import numpy as np

logger = logging.getLogger(__name__)

# Try to import FAISS
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("faiss not available. Install with: pip install faiss-cpu")

# Try to import Google GenAI for embeddings
try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logger.warning("google-genai not available. Install with: pip install google-genai")


class SemanticSimilarity:
    """
    Computes semantic similarity between prompts using Google embeddings + FAISS.
    
    Uses Google's text-embedding-004 model for embeddings and FAISS IndexFlatIP
    for computing cosine similarity on normalized vectors.
    
    This matches the GoLLIE paraphrasing implementation.
    """
    
    def __init__(
        self, 
        embedding_model: str = "models/text-embedding-004",
        api_key: Optional[str] = None
    ):
        """
        Initialize the similarity calculator.
        
        Args:
            embedding_model: Name of the Google embedding model to use
            api_key: Google API key (defaults to GOOGLE_API_KEY env var)
        """
        self.embedding_model = embedding_model
        self.client = None
        
        if GENAI_AVAILABLE and FAISS_AVAILABLE:
            api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
            if api_key:
                try:
                    self.client = genai.Client(api_key=api_key)
                    logger.info(f"Initialized SemanticSimilarity with embedding model: {embedding_model}")
                except Exception as e:
                    logger.warning(f"Failed to initialize Google GenAI client: {e}")
            else:
                logger.warning("No API key found for embeddings")
        else:
            if not FAISS_AVAILABLE:
                logger.warning("FAISS not available - using fallback similarity")
            if not GENAI_AVAILABLE:
                logger.warning("Google GenAI not available - using fallback similarity")
    
    def _get_embedding(self, text: str) -> Optional[np.ndarray]:
        """
        Get embedding for a text using Google's embedding API.
        
        Args:
            text: Text to embed
        
        Returns:
            Numpy array of embedding values, or None if embedding fails
        """
        if self.client is None:
            return None
        
        try:
            # Truncate very long texts to avoid API limits
            max_chars = 30000  # Google embedding API has limits
            if len(text) > max_chars:
                logger.warning(f"Truncating text from {len(text)} to {max_chars} chars for embedding")
                text = text[:max_chars]
            
            result = self.client.models.embed_content(
                model=self.embedding_model,
                contents=text
            )
            return np.array(result.embeddings[0].values, dtype='float32')
        
        except Exception as e:
            logger.error(f"Embedding failed: {e}")
            return None
    
    def _faiss_cosine_similarity(self, v1: np.ndarray, v2: np.ndarray) -> float:
        """
        Compute cosine similarity using FAISS IndexFlatIP.
        
        FAISS IndexFlatIP computes inner product, which equals cosine similarity
        when vectors are normalized.
        
        Args:
            v1: First embedding vector
            v2: Second embedding vector
        
        Returns:
            Cosine similarity score (0 to 1)
        """
        # Normalize vectors for cosine similarity
        v1 = v1 / np.linalg.norm(v1)
        v2 = v2 / np.linalg.norm(v2)
        
        # Create FAISS index
        d = v1.shape[0]
        index = faiss.IndexFlatIP(d)
        index.add(np.array([v1]))
        
        # Search for similarity
        D, I = index.search(np.array([v2]), 1)
        return float(D[0][0])
    
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
        
        Uses Google embeddings + FAISS if available, otherwise falls back
        to trigram-based Jaccard similarity.
        
        Args:
            original: Original prompt text
            variation: Paraphrased prompt text
        
        Returns:
            Similarity score between 0 and 1
        """
        if self.client is not None and FAISS_AVAILABLE:
            emb_original = self._get_embedding(original)
            emb_variation = self._get_embedding(variation)
            
            if emb_original is not None and emb_variation is not None:
                return self._faiss_cosine_similarity(emb_original, emb_variation)
        
        # Fallback to basic similarity
        logger.debug("Using fallback trigram similarity")
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
        if self.client is not None and FAISS_AVAILABLE:
            emb_original = self._get_embedding(original)
            
            if emb_original is not None:
                # Normalize original embedding once
                emb_original = emb_original / np.linalg.norm(emb_original)
                
                # Create FAISS index with original
                d = emb_original.shape[0]
                index = faiss.IndexFlatIP(d)
                index.add(np.array([emb_original]))
                
                similarities = []
                for var in variations:
                    emb_var = self._get_embedding(var)
                    if emb_var is not None:
                        emb_var = emb_var / np.linalg.norm(emb_var)
                        D, I = index.search(np.array([emb_var]), 1)
                        similarities.append(float(D[0][0]))
                    else:
                        similarities.append(self._basic_similarity(original, var))
                
                return similarities
        
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
