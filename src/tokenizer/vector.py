"""
Vector Engine - Generates embeddings and manages USearch index.
Uses jassas-embedding (ONNX INT8) for fast Arabic semantic search.
"""
import os
from typing import List, Tuple
import numpy as np
from usearch.index import Index

# PERFORMANCE FLAGS - Must be set before importing ONNX runtime
os.environ["OMP_NUM_THREADS"] = "1"

from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForFeatureExtraction


# Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
INDEX_PATH = os.path.join(DATA_DIR, 'vectors.usearch')
MODEL_PATH = 'y3fai/jassas-embedding'  # HuggingFace Hub (private)


class VectorEngine:
    """
    Generates embeddings using jassas-embedding (ONNX INT8).
    Manages USearch vector index for fast similarity search.
    """

    # Model config
    MODEL_NAME = MODEL_PATH  # Local path or HuggingFace hub path
    DIMENSIONS = 768
    MAX_LENGTH = 512

    # USearch config (optimized for recall/speed balance)
    INDEX_CONFIG = {
        'ndim': 768,
        'metric': 'cos',
        'dtype': 'f16',           # Half precision (2x memory savings)
        'connectivity': 32,       # Balanced quality
        'expansion_add': 200,     # Better graph construction
        'expansion_search': 100,  # Better recall
    }

    # Singleton instances for model reuse
    _tokenizer = None
    _model = None

    def __init__(self, batch_size: int = 32, model_path: str = None):
        self.batch_size = batch_size
        self.model_path = model_path or MODEL_PATH
        self.index = None

    @classmethod
    def _load_model_singleton(cls, model_path: str):
        """Load model as singleton for memory efficiency."""
        if cls._tokenizer is None or cls._model is None:
            print(f"Loading jassas-embedding: {model_path}")

            # Tokenizer with critical regex fix
            cls._tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                clean_up_tokenization_spaces=True,
                fix_mistral_regex=True  # CRITICAL for Gemma tokenizer
            )

            # ONNX Runtime model (INT8 quantized)
            cls._model = ORTModelForFeatureExtraction.from_pretrained(
                model_path,
                file_name="model_quantized.onnx"
            )

        return cls._tokenizer, cls._model

    def load_model(self):
        """Load the Jassas embedding model."""
        self._load_model_singleton(self.model_path)

    def create_index(self):
        """Create a new USearch index."""
        self.index = Index(**self.INDEX_CONFIG)

    def load_index(self) -> bool:
        """Load existing index from disk. Returns False if not found."""
        if os.path.exists(INDEX_PATH):
            self.index = Index.restore(INDEX_PATH)
            return True
        return False

    def save_index(self):
        """Save index to disk."""
        if self.index:
            os.makedirs(DATA_DIR, exist_ok=True)
            self.index.save(INDEX_PATH)

    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for texts using jassas-embedding.

        Uses mean pooling + L2 normalization for optimal semantic similarity.
        Target latency: <35ms per query.
        """
        tokenizer, model = self._load_model_singleton(self.model_path)

        # Tokenize
        inputs = tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=self.MAX_LENGTH,
            return_tensors="pt"
        )

        # Inference
        outputs = model(**inputs)

        # Mean pooling over sequence length
        embeddings = outputs.last_hidden_state.mean(dim=1)

        # L2 normalization (required for cosine similarity)
        embeddings = embeddings / embeddings.norm(dim=1, keepdim=True)

        return embeddings.detach().numpy()

    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings in batches for large document sets."""
        self.load_model()

        all_embeddings = []
        for i in range(0, len(texts), self.batch_size):
            batch = texts[i:i + self.batch_size]
            embeddings = self.encode(batch)
            all_embeddings.append(embeddings)

        return np.vstack(all_embeddings)

    def add_documents(self, doc_ids: List[int], texts: List[str]):
        """
        Add documents to the index.

        Args:
            doc_ids: List of document IDs (keys for the index)
            texts: List of text content to embed
        """
        if not texts:
            return

        # Generate embeddings
        embeddings = self.encode_batch(texts)

        # Add to index
        if self.index is None:
            self.create_index()

        # Convert to numpy arrays
        keys = np.array(doc_ids, dtype=np.int64)
        vectors = embeddings.astype(np.float16)  # Match f16 dtype

        self.index.add(keys, vectors)

    def search(self, query: str, limit: int = 10) -> List[Tuple[int, float]]:
        """
        Search for similar documents.

        Args:
            query: Search query text
            limit: Number of results to return

        Returns:
            List of (doc_id, score) tuples
        """
        if self.index is None or len(self.index) == 0:
            return []

        # Encode query
        query_embedding = self.encode([query])[0].astype(np.float16)

        # Search
        matches = self.index.search(query_embedding, limit)

        # Convert to list of tuples
        results = []
        for key, distance in zip(matches.keys, matches.distances):
            # USearch returns distance, convert to similarity for cosine
            # For cosine metric, distance = 1 - similarity
            similarity = 1.0 - float(distance)
            results.append((int(key), similarity))

        return results

    def get_count(self) -> int:
        """Get number of vectors in index."""
        return len(self.index) if self.index else 0
