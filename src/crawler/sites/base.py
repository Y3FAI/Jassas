"""
Base site configuration.
"""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SiteConfig:
    """Base configuration for a crawl target."""

    # Domain
    domain: str = ""

    # Sitemap
    sitemap_url: Optional[str] = None
    sitemap_only: bool = False  # If True, don't extract links from pages

    # URL filtering
    url_filters: List[str] = field(default_factory=list)  # Only crawl URLs containing these
    url_exclude: List[str] = field(default_factory=list)  # Skip URLs containing these

    # Language preference
    language: Optional[str] = None  # e.g., 'ar' - convert /en/ to /ar/

    # Crawl settings
    use_playwright: bool = False  # Use Playwright for JS rendering
    delay: float = 2.0  # Delay between requests
    max_pages: int = 100
    max_depth: int = 5

    def should_crawl(self, url: str) -> bool:
        """Check if URL should be crawled based on filters."""
        # Must match at least one filter (if filters defined)
        if self.url_filters:
            if not any(f in url for f in self.url_filters):
                return False

        # Must not match any exclusion
        if self.url_exclude:
            if any(e in url for e in self.url_exclude):
                return False

        return True

    def transform_url(self, url: str) -> str:
        """Transform URL (e.g., language conversion)."""
        if self.language == 'ar':
            if '/en/' in url:
                url = url.replace('/en/', '/ar/')
            elif url.endswith('/en'):
                url = url.replace('/en', '/ar')
        return url
