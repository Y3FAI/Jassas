"""
Base site parser.
"""
from bs4 import BeautifulSoup
from utils.normalize import normalize_arabic


class SiteParser:
    """Base parser - extracts content generically."""

    def parse(self, html: str) -> dict:
        """
        Parse HTML and return structured content.

        Returns:
            dict with: title, title_display, description, description_display, clean_text, doc_len
        """
        if not html or not html.strip():
            return {'title': '', 'title_display': '', 'description': '', 'description_display': '', 'clean_text': '', 'doc_len': 0}

        try:
            soup = BeautifulSoup(html, 'lxml')
        except Exception:
            return {'title': '', 'title_display': '', 'description': '', 'description_display': '', 'clean_text': '', 'doc_len': 0}

        # Extract original text for display
        title_display = self._extract_title(soup)
        description_display = self._extract_description(soup)
        content = self._extract_content(soup)

        # Normalize for search
        title = normalize_arabic(title_display)
        description = normalize_arabic(description_display)
        clean_text = normalize_arabic(content)

        return {
            'title': title,
            'title_display': title_display,
            'description': description,
            'description_display': description_display,
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
