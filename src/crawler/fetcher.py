"""
Fetcher - HTTP requests with CloudFlare bypass.
"""
import hashlib
from typing import Dict, Optional
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import cloudscraper


class RobotChecker:
    """Caches and checks robots.txt rules."""

    def __init__(self, scraper):
        self._cache: Dict[str, RobotFileParser] = {}
        self._scraper = scraper
        self._user_agent = "*"

    def can_fetch(self, url: str) -> bool:
        """Check if URL is allowed by robots.txt."""
        parsed = urlparse(url)
        domain = f"{parsed.scheme}://{parsed.netloc}"

        if domain not in self._cache:
            self._cache[domain] = self._fetch_robots(domain)

        parser = self._cache[domain]
        if parser is None:
            return True

        return parser.can_fetch(self._user_agent, url)

    def _fetch_robots(self, domain: str) -> Optional[RobotFileParser]:
        """Fetch and parse robots.txt for domain."""
        robots_url = f"{domain}/robots.txt"

        try:
            response = self._scraper.get(robots_url, timeout=10)
            if response.status_code == 200:
                parser = RobotFileParser()
                parser.parse(response.text.splitlines())
                return parser
        except Exception:
            pass

        return None


class Fetcher:
    """Fetches pages with CloudFlare bypass."""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'darwin',
                'desktop': True
            }
        )
        self.robot_checker = RobotChecker(self.scraper)

    def fetch(self, url: str) -> dict:
        """
        Fetch a URL with CloudFlare bypass.

        Returns:
            dict with keys:
                - html: str (page content)
                - status_code: int
                - content_hash: str (SHA256)
                - error: str or None
        """
        result = {
            'html': '',
            'status_code': 0,
            'content_hash': '',
            'error': None
        }

        # Check robots.txt
        if not self.robot_checker.can_fetch(url):
            result['error'] = "Blocked by robots.txt"
            return result

        try:
            response = self.scraper.get(url, timeout=self.timeout)
            result['status_code'] = response.status_code

            if response.status_code != 200:
                result['error'] = f"HTTP {response.status_code}"
                return result

            # Check content type
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' not in content_type.lower() and 'text/xml' not in content_type.lower():
                result['error'] = f"Not HTML: {content_type}"
                return result

            result['html'] = response.text
            result['content_hash'] = self._hash_content(response.text)

        except cloudscraper.exceptions.CloudflareChallengeError as e:
            result['error'] = f"CloudFlare challenge failed: {e}"
        except Exception as e:
            result['error'] = f"{type(e).__name__}: {e}"

        return result

    def _hash_content(self, content: str) -> str:
        """Generate SHA256 hash of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def close(self):
        """Close scraper session."""
        self.scraper.close()
