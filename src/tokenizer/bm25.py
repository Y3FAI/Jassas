"""
BM25 Tokenizer - Builds inverted index for lexical search.
"""
import re
from typing import List, Dict
from collections import Counter


class BM25Tokenizer:
    """Tokenizes text and builds inverted index."""

    # Arabic stopwords (common words to skip)
    ARABIC_STOPWORDS = {
        # Particles
        'في', 'من', 'إلى', 'على', 'عن', 'مع', 'أو', 'و', 'ثم', 'بل',
        # Pronouns
        'هو', 'هي', 'هم', 'هن', 'أنا', 'نحن', 'أنت', 'أنتم', 'أنتن',
        # Demonstratives
        'هذا', 'هذه', 'ذلك', 'تلك', 'هؤلاء', 'أولئك',
        # Relative
        'الذي', 'التي', 'الذين', 'اللذان', 'اللتان', 'اللواتي',
        # Question words
        'ما', 'ماذا', 'من', 'أين', 'متى', 'كيف', 'لماذا', 'كم',
        # Common verbs
        'كان', 'كانت', 'يكون', 'تكون', 'كانوا',
        'هناك', 'ليس', 'ليست',
        # Articles/Prepositions
        'ال', 'لل', 'بال', 'وال', 'فال', 'كال',
        'إن', 'أن', 'لأن', 'حتى', 'لكن', 'بعد', 'قبل', 'عند', 'بين',
        # Common
        'كل', 'بعض', 'غير', 'أي', 'كذلك', 'أيضا', 'فقط', 'جدا',
        'يمكن', 'يجب', 'قد', 'لقد', 'سوف', 'لن', 'لم',
    }

    # English stopwords
    ENGLISH_STOPWORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'shall', 'can',
        'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them',
        'he', 'she', 'his', 'her', 'we', 'you', 'i', 'my', 'your', 'our',
        'not', 'no', 'if', 'then', 'than', 'so', 'just', 'also', 'very',
    }

    STOPWORDS = ARABIC_STOPWORDS | ENGLISH_STOPWORDS

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
            # Skip stopwords
            if token in self.STOPWORDS:
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
