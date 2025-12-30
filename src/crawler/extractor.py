"""
Extractor - Extract and filter URLs from HTML.
"""
from typing import List, Set
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


class Extractor:
    """Extracts valid URLs from HTML content."""

    # File extensions to skip
    SKIP_EXTENSIONS = {
        '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp',
        '.zip', '.rar', '.tar', '.gz',
        '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        '.mp3', '.mp4', '.avi', '.mov', '.wmv',
        '.css', '.js', '.json', '.xml',
    }

    # URL patterns to skip
    SKIP_PATTERNS = {
        'mailto:', 'tel:', 'javascript:', 'whatsapp:',
        '#',  # Fragment-only links
        'print', 'email', 'share',  # Action links
    }

    # Allowed domains (only crawl these)
    ALLOWED_DOMAINS = {
        'my.gov.sa',
        'www.my.gov.sa',
    }

    def extract(self, html: str, base_url: str) -> List[str]:
        """
        Extract valid URLs from HTML.

        Args:
            html: HTML content
            base_url: URL of the page (for resolving relative links)

        Returns:
            List of valid, absolute URLs
        """
        soup = BeautifulSoup(html, 'lxml')
        urls: Set[str] = set()

        for link in soup.find_all('a', href=True):
            href = link['href'].strip()

            if not href:
                continue

            # Convert to absolute URL
            absolute_url = urljoin(base_url, href)

            # Validate and clean
            cleaned = self._clean_url(absolute_url)
            if cleaned and self._is_valid(cleaned):
                urls.add(cleaned)

        return list(urls)

    def _clean_url(self, url: str) -> str:
        """Clean and normalize URL."""
        parsed = urlparse(url)

        # Remove fragment
        cleaned = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

        # Remove trailing slash (normalize)
        if cleaned.endswith('/') and len(parsed.path) > 1:
            cleaned = cleaned[:-1]

        # Keep query string if present (some sites need it)
        if parsed.query:
            cleaned = f"{cleaned}?{parsed.query}"

        return cleaned

    def _is_valid(self, url: str) -> bool:
        """Check if URL should be crawled."""
        parsed = urlparse(url)

        # Must be http or https
        if parsed.scheme not in ('http', 'https'):
            return False

        # Must be allowed domain
        domain = parsed.netloc.lower()
        if domain not in self.ALLOWED_DOMAINS:
            return False

        # Check skip patterns
        url_lower = url.lower()
        for pattern in self.SKIP_PATTERNS:
            if pattern in url_lower:
                return False

        # Check file extensions
        path_lower = parsed.path.lower()
        for ext in self.SKIP_EXTENSIONS:
            if path_lower.endswith(ext):
                return False

        return True
