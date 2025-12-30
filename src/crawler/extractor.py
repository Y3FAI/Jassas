"""
Extractor - Extract and filter URLs from HTML.
With URL priority scoring and Arabic preference.
"""
from typing import List, Set, Tuple
from urllib.parse import urljoin, urlparse
import re

from bs4 import BeautifulSoup


class Extractor:
    """Extracts valid URLs from HTML content with priority scoring."""

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

    # Priority patterns (higher score = crawl first)
    PRIORITY_RULES = [
        # High priority - service pages
        (r'/services/', 50),
        (r'/service/', 50),
        (r'/الخدمات/', 50),
        (r'/خدمة/', 50),
        # Category/listing pages
        (r'/categories/', 20),
        (r'/الفئات/', 20),
        # Deep paths - slightly lower
        (r'/[^/]+/[^/]+/[^/]+/[^/]+/', -10),
    ]

    def extract(self, html: str, base_url: str) -> List[Tuple[str, int]]:
        """
        Extract valid URLs from HTML with priority scores.

        Args:
            html: HTML content
            base_url: URL of the page (for resolving relative links)

        Returns:
            List of tuples: (url, priority)
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
                # Try Arabic version if this is English
                arabic_url = self._try_arabic_version(cleaned)
                if arabic_url:
                    urls.add(arabic_url)
                else:
                    urls.add(cleaned)

        # Return with priorities
        return [(url, self._calculate_priority(url)) for url in urls]

    def _try_arabic_version(self, url: str) -> str:
        """
        If URL contains /en/, return /ar/ version.
        Caller should verify it exists before using.
        """
        if '/en/' in url or url.endswith('/en'):
            arabic_url = url.replace('/en/', '/ar/').replace('/en', '/ar')
            return arabic_url
        return None

    def _calculate_priority(self, url: str) -> int:
        """Calculate priority score for URL based on patterns."""
        priority = 0
        for pattern, score in self.PRIORITY_RULES:
            if re.search(pattern, url):
                priority += score
        return priority

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
