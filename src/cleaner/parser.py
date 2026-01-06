"""
Parser - HTML to clean text with Arabic normalization.
"""
import re
from bs4 import BeautifulSoup
from utils.normalize import normalize_arabic


class Parser:
    """Parses HTML and extracts normalized text."""

    # Tags to remove completely
    NOISE_TAGS = ['script', 'style', 'nav', 'footer', 'header', 'meta', 'noscript', 'aside', 'iframe']

    def parse(self, html: str) -> dict:
        """
        Parse HTML and return cleaned metadata.

        Args:
            html: Raw HTML content

        Returns:
            dict with keys:
                - title: str (cleaned title)
                - description: str (meta description)
                - clean_text: str (normalized body text)
                - doc_len: int (word count for BM25)
        """
        if not html or not html.strip():
            return {'title': '', 'description': '', 'clean_text': '', 'doc_len': 0}

        try:
            soup = BeautifulSoup(html, 'lxml')
        except Exception:
            return {'title': '', 'description': '', 'clean_text': '', 'doc_len': 0}

        # Extract title and description before removing meta tags
        title = self._extract_title(soup)
        description = self._extract_description(soup)

        # Remove noise tags
        for tag in soup(self.NOISE_TAGS):
            tag.decompose()

        # Extract body text
        text = soup.get_text(separator=' ')

        # Normalize
        clean_text = normalize_arabic(text)
        clean_title = normalize_arabic(title)

        return {
            'title': clean_title,
            'description': description,
            'clean_text': clean_text,
            'doc_len': len(clean_text.split())
        }

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract title from <title> or <h1>."""
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        if soup.h1 and soup.h1.string:
            return soup.h1.string.strip()
        # Try first h1 with text
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        return ""

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description."""
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta and meta.get('content'):
            return meta['content'].strip()
        # Try og:description
        og_meta = soup.find('meta', attrs={'property': 'og:description'})
        if og_meta and og_meta.get('content'):
            return og_meta['content'].strip()
        return ""

