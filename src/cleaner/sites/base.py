"""
Base site parser.
"""
from bs4 import BeautifulSoup


class SiteParser:
    """Base parser - extracts content generically."""

    def parse(self, html: str) -> dict:
        """
        Parse HTML and return structured content.

        Returns:
            dict with: title, description, clean_text, doc_len
        """
        if not html or not html.strip():
            return {'title': '', 'description': '', 'clean_text': '', 'doc_len': 0}

        try:
            soup = BeautifulSoup(html, 'lxml')
        except Exception:
            return {'title': '', 'description': '', 'clean_text': '', 'doc_len': 0}

        title = self._extract_title(soup)
        description = self._extract_description(soup)
        clean_text = self._extract_content(soup)

        return {
            'title': title,
            'description': description,
            'clean_text': clean_text,
            'doc_len': len(clean_text.split())
        }

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract title."""
        if soup.title:
            return soup.title.get_text(strip=True)
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        return ""

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description."""
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta and meta.get('content'):
            return meta['content'].strip()
        return ""

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main content - override in subclasses."""
        # Remove noise tags
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'noscript', 'iframe']):
            tag.decompose()

        # Get text from main or body
        main = soup.find('main') or soup.find('body')
        if main:
            return main.get_text(separator=' ', strip=True)
        return soup.get_text(separator=' ', strip=True)
