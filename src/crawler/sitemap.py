"""
Sitemap Parser - Extract URLs from XML sitemaps.
Handles both sitemap.xml and sitemap index files.
"""
import re
import xml.etree.ElementTree as ET
from typing import List, Tuple, Set
from urllib.parse import urlparse

from rich.console import Console

console = Console()


class SitemapParser:
    """Parse XML sitemaps and extract URLs with priorities."""

    # XML namespaces used in sitemaps
    NAMESPACES = {
        'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9',
    }

    # Priority patterns (same as extractor)
    PRIORITY_RULES = [
        (r'/services/', 50),
        (r'/service/', 50),
        (r'/الخدمات/', 50),
        (r'/خدمة/', 50),
        (r'/categories/', 20),
        (r'/الفئات/', 20),
        (r'/[^/]+/[^/]+/[^/]+/[^/]+/', -10),
    ]

    def __init__(self, fetcher, verbose: bool = True):
        self.fetcher = fetcher
        self.verbose = verbose
        self.discovered_urls: Set[str] = set()

    def log(self, msg: str):
        if self.verbose:
            console.print(msg)

    def parse(self, sitemap_url: str) -> List[Tuple[str, int]]:
        """
        Parse sitemap and return list of (url, priority) tuples.
        Handles sitemap index files recursively.
        """
        self.log(f"[cyan]Fetching sitemap:[/cyan] {sitemap_url}")

        result = self.fetcher.fetch(sitemap_url)
        if result['error']:
            self.log(f"[red]Error: {result['error']}[/red]")
            return []

        xml_content = result['html']

        # Detect sitemap type
        if '<sitemapindex' in xml_content:
            return self._parse_sitemap_index(xml_content)
        elif '<urlset' in xml_content:
            return self._parse_urlset(xml_content)
        else:
            self.log("[red]Not a valid sitemap XML[/red]")
            return []

    def _parse_sitemap_index(self, xml_content: str) -> List[Tuple[str, int]]:
        """Parse sitemap index and recursively fetch child sitemaps."""
        self.log("[yellow]Detected sitemap index, parsing...[/yellow]")

        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            self.log(f"[red]XML parse error: {e}[/red]")
            return []

        all_urls = []

        # Find all sitemap entries
        for sitemap in root.findall('.//sm:sitemap', self.NAMESPACES):
            loc = sitemap.find('sm:loc', self.NAMESPACES)
            if loc is not None and loc.text:
                child_url = loc.text.strip()
                # Prefer Arabic sitemaps
                if '/en/' in child_url:
                    arabic_url = child_url.replace('/en/', '/ar/')
                    self.log(f"[dim]Converting to Arabic: {arabic_url}[/dim]")
                    child_url = arabic_url

                child_urls = self.parse(child_url)
                all_urls.extend(child_urls)

        # Also try without namespace (some sitemaps don't use it)
        if not all_urls:
            for sitemap in root.findall('.//sitemap'):
                loc = sitemap.find('loc')
                if loc is not None and loc.text:
                    child_url = loc.text.strip()
                    if '/en/' in child_url:
                        child_url = child_url.replace('/en/', '/ar/')
                    child_urls = self.parse(child_url)
                    all_urls.extend(child_urls)

        return all_urls

    def _parse_urlset(self, xml_content: str) -> List[Tuple[str, int]]:
        """Parse urlset and extract URLs."""
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as e:
            self.log(f"[red]XML parse error: {e}[/red]")
            return []

        urls = []

        # Try with namespace
        for url_elem in root.findall('.//sm:url', self.NAMESPACES):
            loc = url_elem.find('sm:loc', self.NAMESPACES)
            if loc is not None and loc.text:
                url = self._process_url(loc.text.strip())
                if url and url not in self.discovered_urls:
                    self.discovered_urls.add(url)
                    priority = self._calculate_priority(url)
                    urls.append((url, priority))

        # Try without namespace
        if not urls:
            for url_elem in root.findall('.//url'):
                loc = url_elem.find('loc')
                if loc is not None and loc.text:
                    url = self._process_url(loc.text.strip())
                    if url and url not in self.discovered_urls:
                        self.discovered_urls.add(url)
                        priority = self._calculate_priority(url)
                        urls.append((url, priority))

        self.log(f"[green]Found {len(urls)} URLs[/green]")
        return urls

    def _process_url(self, url: str) -> str:
        """Process URL: convert /en/ to /ar/, validate domain."""
        # Convert English to Arabic
        if '/en/' in url or url.endswith('/en'):
            url = url.replace('/en/', '/ar/').replace('/en', '/ar')

        # Validate domain
        parsed = urlparse(url)
        if parsed.netloc not in ('my.gov.sa', 'www.my.gov.sa'):
            return None

        return url

    def _calculate_priority(self, url: str) -> int:
        """Calculate priority score for URL."""
        priority = 0
        for pattern, score in self.PRIORITY_RULES:
            if re.search(pattern, url):
                priority += score
        return priority


def crawl_sitemap(sitemap_url: str, verbose: bool = True) -> List[Tuple[str, int]]:
    """
    Convenience function to crawl a sitemap.
    Returns list of (url, priority) tuples.
    """
    from crawler.fetcher import Fetcher

    fetcher = Fetcher()
    parser = SitemapParser(fetcher, verbose=verbose)

    try:
        urls = parser.parse(sitemap_url)
        return urls
    finally:
        fetcher.close()
