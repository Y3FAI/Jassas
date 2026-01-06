"""
Reranker - Uses jassas-embedding for precise Arabic reranking.
Stage 2 of two-stage retrieval pipeline.
"""
import os
from typing import List, Dict
import numpy as np

# PERFORMANCE FLAGS
os.environ["OMP_NUM_THREADS"] = "1"

from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForFeatureExtraction


MODEL_PATH = 'y3fai/jassas-embedding'


class Reranker:
    """
    Reranks candidates using jassas-embedding.
    Uses title-only for fast, focused semantic matching.
    """

    MAX_LENGTH = 128  # Shorter for titles only

    # Singleton
    _tokenizer = None
    _model = None

    def __init__(self):
        self._loaded = False

    @classmethod
    def _load_model(cls):
        """Load model as singleton."""
        if cls._tokenizer is None or cls._model is None:
            print("Loading reranker: jassas-embedding")

            hf_token = os.environ.get('HF_TOKEN')

            cls._tokenizer = AutoTokenizer.from_pretrained(
                MODEL_PATH,
                clean_up_tokenization_spaces=True,
                token=hf_token,
            )

            cls._model = ORTModelForFeatureExtraction.from_pretrained(
                MODEL_PATH,
                file_name="model_quantized.onnx",
                token=hf_token,
            )

        return cls._tokenizer, cls._model

    def load(self):
        """Pre-load model."""
        if not self._loaded:
            self._load_model()
            self._loaded = True

    def _encode(self, texts: List[str]) -> np.ndarray:
        """Encode texts to embeddings."""
        tokenizer, model = self._load_model()

        inputs = tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=self.MAX_LENGTH,
            return_tensors="pt"
        )

        outputs = model(**inputs)

        # Mean pooling
        embeddings = outputs.last_hidden_state.mean(dim=1)

        # L2 normalize
        embeddings = embeddings / embeddings.norm(dim=1, keepdim=True)

        return embeddings.detach().numpy()

    def rerank(self, query: str, candidates: List[Dict], k: int = 10) -> List[Dict]:
        """
        Rerank candidates by semantic similarity to query.

        Args:
            query: Search query
            candidates: List of dicts with 'title', 'doc_id', etc.
            k: Number of results to return

        Returns:
            Reranked list of candidates
        """
        if not candidates:
            return []

        self.load()

        # Extract titles
        titles = [c['title'] for c in candidates]

        # Encode query + titles in one batch
        all_texts = [query] + titles
        embeddings = self._encode(all_texts)

        query_emb = embeddings[0]
        title_embs = embeddings[1:]

        # Compute cosine similarities
        scores = np.dot(title_embs, query_emb)

        # Sort by score
        ranked_indices = np.argsort(scores)[::-1][:k]

        # Build reranked results
        results = []
        for idx in ranked_indices:
            candidate = candidates[idx].copy()
            candidate['rerank_score'] = float(scores[idx])
            results.append(candidate)

        return results
