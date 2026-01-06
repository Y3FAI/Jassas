"""
Ranker Engine - Hybrid RRF Search (BM25 + Vector).
The "Judge" that merges lexical and semantic results.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from usearch.index import Index

from db import Documents, Vocab
from utils.normalize import normalize_arabic
from tokenizer.bm25 import BM25Tokenizer
from tokenizer.vector import VectorEngine
from ranker.bm25_numpy import NumPyBM25Engine

# Paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
INDEX_PATH = os.path.join(DATA_DIR, 'vectors.usearch')


class Ranker:
    """Hybrid search engine using RRF fusion."""

    # RRF constant (industry standard)
    RRF_K = 60

    # BM25 parameters
    BM25_K1 = 1.2
    BM25_B = 0.75

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.vector_engine = None
        self.vector_index = None
        self.tokenizer = BM25Tokenizer()

        # Initialize NumPy BM25 Engine (in-memory matrix)
        self.bm25_engine = NumPyBM25Engine(
            index_path=os.path.join(DATA_DIR, 'bm25_matrix.pkl')
        )
        if not self.bm25_engine.load():
            self._log("[yellow]BM25 matrix index not found. Run: python src/scripts/build_index.py[/yellow]")

        # Pre-load stats (for legacy compatibility)
        self.total_docs = 0
        self.avgdl = 0.0
        self._load_stats()

    def _log(self, msg: str):
        if self.verbose:
            print(msg)

    def _load_stats(self):
        """Pre-load global stats for BM25."""
        self.total_docs = Documents.get_total_count()
        self.avgdl = Documents.get_avg_doc_len()
        if self.total_docs == 0:
            self._log("Warning: Index is empty.")

    def _load_vector_engine(self):
        """Lazy load vector model and index."""
        if self.vector_engine is None:
            self._log("Loading model...")
            self.vector_engine = VectorEngine()
            self.vector_engine.load_model()

        if self.vector_index is None and os.path.exists(INDEX_PATH):
            self._log("Loading vector index...")
            self.vector_index = Index.restore(INDEX_PATH, view=True)

    def search(self, query: str, k: int = 10, debug: bool = False, mode: str = "hybrid") -> List[dict]:
        """
        Execute search with configurable mode.

        Args:
            query: Search query
            k: Number of results to return
            debug: Print timing breakdown
            mode: "hybrid" (default), "vector", or "bm25"

        Returns:
            List of result dicts with score, title, url
        """
        import time
        timings = {}

        # Normalize query (same as indexing)
        start = time.perf_counter()
        normalized_query = normalize_arabic(query)
        timings['normalize'] = (time.perf_counter() - start) * 1000

        bm25_results = []
        vector_results = []

        # Execute searches based on mode
        start = time.perf_counter()

        if mode == "hybrid":
            # Both searches in parallel
            with ThreadPoolExecutor(max_workers=2) as executor:
                future_bm25 = executor.submit(self._bm25_search, normalized_query, 50)
                future_vector = executor.submit(self._vector_search, normalized_query, 50)
                bm25_results = future_bm25.result()
                vector_results = future_vector.result()
        elif mode == "vector":
            # Vector only
            vector_results = self._vector_search(normalized_query, k * 2)
        elif mode == "bm25":
            # BM25 only
            bm25_results = self._bm25_search(normalized_query, k * 2)

        timings['search'] = (time.perf_counter() - start) * 1000

        # Merge/score results
        merged_scores: Dict[int, float] = {}

        if mode == "hybrid":
            # RRF merge for hybrid
            for rank, doc_id in enumerate(bm25_results):
                if doc_id not in merged_scores:
                    merged_scores[doc_id] = 0.0
                merged_scores[doc_id] += 1.0 / (self.RRF_K + rank + 1)

            for rank, doc_id in enumerate(vector_results):
                if doc_id not in merged_scores:
                    merged_scores[doc_id] = 0.0
                merged_scores[doc_id] += 1.0 / (self.RRF_K + rank + 1)
        else:
            # Single mode - use rank as score
            results_list = vector_results if mode == "vector" else bm25_results
            for rank, doc_id in enumerate(results_list):
                merged_scores[doc_id] = 1.0 / (rank + 1)  # Simple rank score

        # Sort by score
        start = time.perf_counter()
        top_doc_ids = sorted(merged_scores, key=merged_scores.get, reverse=True)[:k]
        timings['sort'] = (time.perf_counter() - start) * 1000

        # Fetch full results
        start = time.perf_counter()
        results = self._fetch_results(top_doc_ids, merged_scores)
        timings['fetch'] = (time.perf_counter() - start) * 1000

        if debug or self.verbose:
            total = sum(timings.values())
            print(f"[Ranker:{mode}] normalize={timings['normalize']:.1f}ms, search={timings['search']:.1f}ms, sort={timings['sort']:.1f}ms, fetch={timings['fetch']:.1f}ms, total={total:.1f}ms")

        return results

    def _bm25_search(self, query: str, limit: int = 50) -> List[int]:
        """
        High-performance in-memory BM25 search using NumPy sparse matrices.
        Replaces SQL CTE with vectorized linear algebra.

        Performance: ~2-3ms per query (vs 100-800ms with SQL)
        """
        # Check if BM25 engine loaded successfully
        if self.bm25_engine.term_matrix is None:
            self._log("[yellow]BM25 index not loaded. Using vector search fallback.[/yellow]")
            return []

        # Tokenize query (same as indexing)
        tokens = self.tokenizer.tokenize(query)

        if not tokens:
            return []

        # Convert tokens to vocab IDs
        token_ids = []
        for token in tokens:
            vocab = Vocab.get_by_token(token)
            if vocab:
                token_ids.append(vocab['id'])

        if not token_ids:
            return []

        # Fast NumPy BM25 search (no SQL joins)
        results = self.bm25_engine.search(token_ids, k=limit)

        # Extract just document IDs (scores discarded, merged with vector via RRF)
        return [doc_id for doc_id, score in results]

    def _vector_search(self, query: str, limit: int = 50) -> List[int]:
        """Semantic search via USearch using jassas-embedding."""
        import time

        start = time.perf_counter()
        self._load_vector_engine()
        load_time = (time.perf_counter() - start) * 1000

        if self.vector_index is None or self.vector_engine is None:
            return []

        if len(self.vector_index) == 0:
            return []

        # Encode query (no prefix needed for jassas-embedding)
        start = time.perf_counter()
        embedding = self.vector_engine.encode([query])[0].astype(np.float16)
        encode_time = (time.perf_counter() - start) * 1000

        # Search
        start = time.perf_counter()
        matches = self.vector_index.search(embedding, limit)
        search_time = (time.perf_counter() - start) * 1000

        if self.verbose:
            print(f"[Vector] load={load_time:.1f}ms, encode={encode_time:.1f}ms, search={search_time:.1f}ms")

        return [int(key) for key in matches.keys]

    def _fetch_results(self, doc_ids: List[int], scores: Dict[int, float]) -> List[dict]:
        """Fetch full document info for results."""
        results = []

        for doc_id in doc_ids:
            doc = Documents.get_by_id(doc_id)
            if doc:
                results.append({
                    'doc_id': doc_id,
                    'score': scores[doc_id],
                    'title': doc['title'],
                    'url': doc['url'],
                    'clean_text': doc.get('clean_text', ''),
                })

        return results
