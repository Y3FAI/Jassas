"""
Central Arabic text normalization and stopwords.
Used by cleaner, tokenizer, and ranker for consistent text processing.
"""
import re
import unicodedata


# =============================================================================
# ARABIC STOPWORDS (pre-normalized)
# =============================================================================

_RAW_STOPWORDS = {
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


def normalize_arabic(text: str) -> str:
    """
    Normalize Arabic text for consistent indexing and search.

    Steps:
    1. Unicode NFKC normalization
    2. Remove Arabic diacritics (tashkeel)
    3. Unify Alif variants (أ إ آ → ا)
    4. Unify Teh Marbuta (ة → ه)
    5. Unify Yeh (ى → ي)
    6. Strip Arabic definite article (ال) from long words
    7. Collapse whitespace
    8. Lowercase (for English parts)

    Args:
        text: Raw text to normalize

    Returns:
        Normalized text
    """
    if not text:
        return ""

    # Unicode normalize
    text = unicodedata.normalize('NFKC', text)

    # Remove Arabic diacritics (tashkeel)
    # Range: \u064B-\u065F (fatha, damma, kasra, shadda, sukun, etc.)
    # Plus \u0670 (superscript alef)
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)

    # Unify Alif variants: أ إ آ → ا
    text = re.sub(r'[أإآ]', 'ا', text)

    # Unify Teh Marbuta: ة → ه
    text = re.sub(r'ة', 'ه', text)

    # Unify Yeh: ى (alef maksura) → ي
    text = re.sub(r'ى', 'ي', text)

    # Strip Arabic definite article (ال) with length guard
    # Only strip from words > 4 chars to protect roots like الله, الا
    words = text.split()
    words = [re.sub(r'^ال', '', w) if w.startswith('ال') and len(w) > 4 else w for w in words]
    text = ' '.join(words)

    # Collapse whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Lowercase for English parts
    return text.lower()


# =============================================================================
# PRE-NORMALIZED STOPWORDS
# Built once at module load by applying normalize_arabic to raw stopwords
# =============================================================================

ARABIC_STOPWORDS = {normalize_arabic(sw) for sw in _RAW_STOPWORDS}
