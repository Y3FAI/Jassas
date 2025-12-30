"""
Spider - The Crawler Orchestrator.
Manages the crawl loop with stop/resume capability.
"""
import time
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import Frontier, RawPages
from crawler.fetcher import Fetcher
from crawler.extractor import Extractor

console = Console()


class Spider:
    """Crawl orchestrator with configurable limits."""

    def __init__(
        self,
        max_pages: int = 100,
        max_depth: int = 5,
        delay: float = 2.0,
        verbose: bool = True
    ):
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.delay = delay
        self.verbose = verbose

        self.fetcher = Fetcher()
        self.extractor = Extractor()

        # Stats
        self.pages_crawled = 0
        self.pages_skipped = 0
        self.pages_failed = 0
        self.urls_discovered = 0

    def log(self, message: str, style: str = ""):
        """Print if verbose mode."""
        if self.verbose:
            console.print(message, style=style)

    def crawl(self) -> dict:
        """
        Main crawl loop.
        Returns stats dict when complete.
        """
        self.log("[bold cyan]Starting Jassas Spider[/bold cyan]")
        self.log(f"  Max pages: {self.max_pages}")
        self.log(f"  Max depth: {self.max_depth}")
        self.log(f"  Delay: {self.delay}s\n")

        while self.pages_crawled < self.max_pages:
            # 1. Get next pending URL (respecting max_depth)
            pending = Frontier.get_next_pending(limit=1)

            if not pending:
                self.log("\n[yellow]No more pending URLs. Crawl complete.[/yellow]")
                break

            url_record = pending[0]
            url = url_record['url']
            depth = url_record['depth']
            priority = url_record.get('priority', 0)
            url_id = url_record['id']

            # Check depth limit
            if depth > self.max_depth:
                self.log(f"[dim]Skipping (depth {depth} > {self.max_depth}): {url}[/dim]")
                Frontier.mark_crawled(url_id)  # Mark as done, don't retry
                self.pages_skipped += 1
                continue

            # 2. Mark as in progress
            Frontier.mark_in_progress(url_id)
            priority_tag = f"[magenta]P{priority}[/magenta]" if priority > 0 else ""
            self.log(f"[cyan]Fetching[/cyan] {priority_tag} (d={depth}): {url}")

            # 3. Fetch page
            result = self.fetcher.fetch(url)

            if result['error']:
                self.log(f"  [red]Error: {result['error']}[/red]")
                Frontier.mark_error(url_id, result['error'])
                self.pages_failed += 1
                continue

            # 4. Check for duplicate content
            if RawPages.exists_by_hash(result['content_hash']):
                self.log(f"  [yellow]Duplicate content, skipping[/yellow]")
                Frontier.mark_crawled(url_id)
                self.pages_skipped += 1
                continue

            # 5. Save raw page
            RawPages.save(
                url=url,
                html_content=result['html'].encode('utf-8'),
                content_hash=result['content_hash'],
                http_status=result['status_code']
            )
            self.pages_crawled += 1
            self.log(f"  [green]Saved[/green] ({result['status_code']}, {len(result['html'])} bytes)")

            # 6. Extract new URLs with priority (only if we haven't hit max_pages)
            if self.pages_crawled < self.max_pages:
                url_priorities = self.extractor.extract(result['html'], url)
                new_depth = depth + 1

                if url_priorities and new_depth <= self.max_depth:
                    # Format: (url, depth, priority)
                    urls_with_depth = [(u, new_depth, p) for u, p in url_priorities]
                    added = Frontier.add_urls(urls_with_depth)
                    self.urls_discovered += added
                    if added > 0:
                        # Show priority stats
                        high_priority = sum(1 for _, p in url_priorities if p >= 30)
                        self.log(f"  [blue]Discovered {added} URLs ({high_priority} high-priority)[/blue]")

            # 7. Mark as crawled
            Frontier.mark_crawled(url_id)

            # 8. Rate limit (skip on last iteration)
            if self.pages_crawled < self.max_pages:
                time.sleep(self.delay)

        # Cleanup
        self.fetcher.close()

        # Summary
        self.log("\n[bold green]Crawl Complete![/bold green]")
        stats = self.get_stats()
        self._print_stats(stats)
        return stats

    def get_stats(self) -> dict:
        """Get crawl statistics."""
        return {
            'pages_crawled': self.pages_crawled,
            'pages_skipped': self.pages_skipped,
            'pages_failed': self.pages_failed,
            'urls_discovered': self.urls_discovered,
            'max_pages': self.max_pages,
            'max_depth': self.max_depth,
        }

    def _print_stats(self, stats: dict):
        """Print stats summary."""
        from rich.table import Table
        from rich import box

        table = Table(title="Crawl Statistics", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green", justify="right")

        table.add_row("Pages Crawled", str(stats['pages_crawled']))
        table.add_row("Pages Skipped", str(stats['pages_skipped']))
        table.add_row("Pages Failed", str(stats['pages_failed']))
        table.add_row("URLs Discovered", str(stats['urls_discovered']))

        console.print(table)


def start(
    max_pages: int = 100,
    max_depth: int = 5,
    delay: float = 2.0,
    verbose: bool = True
) -> dict:
    """
    Entry point for the crawler.
    Called by manager CLI.
    """
    spider = Spider(
        max_pages=max_pages,
        max_depth=max_depth,
        delay=delay,
        verbose=verbose
    )
    return spider.crawl()


if __name__ == "__main__":
    # Quick test
    start(max_pages=5, max_depth=2, delay=1.0)
