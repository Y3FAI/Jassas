"""
Playwright Fetcher - For JS-rendered pages.
"""
import hashlib
from typing import Dict, Optional
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


class PlaywrightFetcher:
    """Fetches pages with full JS rendering using Playwright."""

    def __init__(self, timeout: int = 30000, headless: bool = True):
        self.timeout = timeout
        self.headless = headless
        self._playwright = None
        self._browser = None
        self._context = None

    def _ensure_browser(self):
        """Lazily initialize browser with stealth settings."""
        if self._browser is None:
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(
                headless=self.headless,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                ]
            )
            # Create context with realistic settings
            self._context = self._browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                locale='ar-SA',
                timezone_id='Asia/Riyadh',
            )

    def fetch(self, url: str) -> dict:
        """
        Fetch a URL with JS rendering.

        Returns:
            dict with keys:
                - html: str (rendered page content)
                - title: str (page title)
                - description: str (meta description)
                - status_code: int
                - content_hash: str (SHA256)
                - error: str or None
        """
        result = {
            'html': '',
            'title': '',
            'description': '',
            'status_code': 0,
            'content_hash': '',
            'error': None
        }

        try:
            self._ensure_browser()

            # Fresh context per request to avoid fingerprinting
            context = self._browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                locale='ar-SA',
                timezone_id='Asia/Riyadh',
            )
            page = context.new_page()

            # Navigate and wait for network idle
            response = page.goto(url, wait_until='domcontentloaded', timeout=self.timeout)

            if response:
                result['status_code'] = response.status

                if response.status != 200:
                    result['error'] = f"HTTP {response.status}"
                    page.close()
                    return result

            # Wait for JS to render content (not just loading spinner)
            try:
                page.wait_for_load_state('networkidle', timeout=15000)
            except PlaywrightTimeout:
                pass

            # Wait for loading indicators to disappear
            loading_selectors = [
                '.loading',
                '[class*="loading"]',
                '[class*="spinner"]',
                'text=جاري التحميل',
                'text=جاري تحميل',
            ]
            for selector in loading_selectors:
                try:
                    page.wait_for_selector(selector, state='hidden', timeout=3000)
                except:
                    pass

            # Extra wait for dynamic content
            page.wait_for_timeout(1000)

            # Extract title
            result['title'] = page.title() or ''

            # Extract meta description
            try:
                desc_elem = page.locator('meta[name="description"]').first
                result['description'] = desc_elem.get_attribute('content', timeout=1000) or ''
            except:
                result['description'] = ''

            # Get rendered HTML
            result['html'] = page.content()
            result['content_hash'] = self._hash_content(result['html'])

            page.close()
            context.close()

        except PlaywrightTimeout:
            result['error'] = "Timeout"
        except Exception as e:
            result['error'] = f"{type(e).__name__}: {e}"

        return result

    def _hash_content(self, content: str) -> str:
        """Generate SHA256 hash of content."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def close(self):
        """Close browser and playwright."""
        if self._context:
            self._context.close()
            self._context = None
        if self._browser:
            self._browser.close()
            self._browser = None
        if self._playwright:
            self._playwright.stop()
            self._playwright = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
