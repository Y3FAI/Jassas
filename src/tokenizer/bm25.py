"""
BM25 Tokenizer - Builds inverted index for lexical search.
"""
import re
from typing import List, Dict
from collections import Counter
from utils.normalize import ARABIC_STOPWORDS


class BM25Tokenizer:
    """Tokenizes text and builds inverted index."""

    def __init__(self, min_token_len: int = 2):
        self.min_token_len = min_token_len

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into list of tokens.

        Steps:
        1. Split on non-word characters
        2. Filter stopwords
        3. Filter by minimum length
        """
        if not text:
            return []

        # Split on whitespace and punctuation
        tokens = re.findall(r'[\w]+', text, re.UNICODE)

        # Filter
        result = []
        for token in tokens:
            # Skip stopwords (uses centralized pre-normalized set)
            if token in ARABIC_STOPWORDS:
                continue
            # Skip short tokens
            if len(token) < self.min_token_len:
                continue
            result.append(token)

        return result

    def get_term_frequencies(self, text: str) -> Dict[str, int]:
        """Get token -> frequency mapping for a document."""
        tokens = self.tokenize(text)
        return dict(Counter(tokens))
