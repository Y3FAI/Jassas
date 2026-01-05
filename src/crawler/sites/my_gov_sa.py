"""
Configuration for my.gov.sa
"""
from .base import SiteConfig


class MyGovSaConfig(SiteConfig):
    """my.gov.sa specific configuration."""

    def __init__(self):
        super().__init__(
            domain="my.gov.sa",
            sitemap_url="https://my.gov.sa/sitemap.xml",
            sitemap_only=True,  # Don't extract links, sitemap has everything
            url_filters=["/services/"],  # Only service pages
            language="ar",  # Prefer Arabic
            use_playwright=True,  # Site uses JS rendering
            delay=1.5,  # Faster with fresh context per request
            max_pages=10000,  # Handle all services
            max_depth=1,  # Flat structure from sitemap
        )
