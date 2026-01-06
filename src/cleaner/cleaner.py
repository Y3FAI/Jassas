"""
Cleaner - Orchestrates HTML cleaning pipeline.
Processes raw_pages → documents in batches.
"""
import sys
import os
import re
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console

# Log folder for cleaned output dumps
LOG_DIR = Path(__file__).parent.parent.parent / 'log'
from rich.table import Table
from rich import box

from db import RawPages, Documents
from db.connection import get_db
from cleaner.sites import get_parser

console = Console()


class Cleaner:
    """Cleans raw HTML pages and saves to documents table."""

    def __init__(self, batch_size: int = 10, verbose: bool = True):
        self.batch_size = batch_size
        self.verbose = verbose

        # Stats
        self.cleaned = 0
        self.skipped = 0
        self.failed = 0

    def log(self, message: str, style: str = ""):
        """Print if verbose mode."""
        if self.verbose:
            console.print(message, style=style)

    def _dump_cleaned(self, url: str, result: dict):
        """Dump cleaned output to log folder for inspection."""
        LOG_DIR.mkdir(exist_ok=True)
        safe_name = re.sub(r'[^\w\-]', '_', url.split('/')[-1] or 'index')[:50]
        filename = f"cleaned_{safe_name}.txt"

        output = f"""URL: {url}
TITLE: {result['title']}
DESCRIPTION: {result.get('description', '')}
WORDS: {result['doc_len']}
{'='*60}
{result['clean_text']}
"""
        (LOG_DIR / filename).write_text(output, encoding='utf-8')

    def clean(self) -> dict:
        """
        Main cleaning loop.
        Processes uncleaned pages in batches.
        """
        self.log("[bold cyan]Starting Jassas Cleaner[/bold cyan]")
        self.log(f"  Batch size: {self.batch_size}\n")

        while True:
            # Get batch of uncleaned pages
            batch = self._get_uncleaned_batch()

            if not batch:
                self.log("\n[yellow]No more uncleaned pages.[/yellow]")
                break

            self.log(f"[cyan]Processing batch of {len(batch)} pages...[/cyan]")

            for page in batch:
                self._process_page(page)

        # Summary
        self.log("\n[bold green]Cleaning Complete![/bold green]")
        stats = self.get_stats()
        self._print_stats(stats)
        return stats

    def _get_uncleaned_batch(self) -> list:
        """Get raw_pages that haven't been cleaned yet."""
        with get_db() as conn:
            cursor = conn.execute("""
                SELECT rp.id, rp.url, rp.html_content
                FROM raw_pages rp
                LEFT JOIN documents d ON d.raw_page_id = rp.id
                WHERE d.id IS NULL
                LIMIT ?
            """, (self.batch_size,))
            return [dict(row) for row in cursor.fetchall()]

    def _process_page(self, page: dict):
        """Parse and save a single page."""
        page_id = page['id']
        url = page['url']
        html = page['html_content']

        # Decode if bytes
        if isinstance(html, bytes):
            try:
                html = html.decode('utf-8')
            except UnicodeDecodeError:
                html = html.decode('utf-8', errors='replace')

        # Get site-specific parser and parse
        try:
            parser = get_parser(url)
            result = parser.parse(html)
        except Exception as e:
            self.log(f"  [red]Parse error ({url}): {e}[/red]")
            self.failed += 1
            return

        # Skip empty documents
        if result['doc_len'] == 0:
            self.log(f"  [dim]Skipped (empty): {url}[/dim]")
            self.skipped += 1
            return

        # Skip soft 404s (server returns 200 but content is error page)
        if self._is_soft_404(result['clean_text']):
            self.log(f"  [dim]Skipped (soft 404): {url}[/dim]")
            self.skipped += 1
            return

        # Save to documents
        try:
            Documents.create(
                raw_page_id=page_id,
                url=url,
                title=result['title'],
                clean_text=result['clean_text'],
                doc_len=result['doc_len'],
                description=result.get('description', ''),
                title_display=result.get('title_display', ''),
                description_display=result.get('description_display', '')
            )
            self.cleaned += 1
            display_title = result.get('title_display') or result['title']
            self.log(f"  [green]Cleaned[/green]: {display_title[:50]}... ({result['doc_len']} words)")
        except Exception as e:
            self.log(f"  [red]Save error ({url}): {e}[/red]")
            self.failed += 1

    def _is_soft_404(self, text: str) -> bool:
        """Detect soft 404 pages (200 OK but error content)."""
        # Too short to be useful
        if len(text) < 300:
            # Check for error indicators in short content
            error_phrases = [
                '404',
                'لم يتم العثور',
                'لم يتم عثور',
                'الصفحة غير موجودة',
                'صفحة غير موجودة',
                'page not found',
                'not found',
            ]
            text_lower = text.lower()
            for phrase in error_phrases:
                if phrase in text_lower:
                    return True
        return False

    def get_stats(self) -> dict:
        """Get cleaning statistics."""
        return {
            'cleaned': self.cleaned,
            'skipped': self.skipped,
            'failed': self.failed,
            'total': self.cleaned + self.skipped + self.failed
        }

    def _print_stats(self, stats: dict):
        """Print stats summary."""
        table = Table(title="Cleaning Statistics", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green", justify="right")

        table.add_row("Documents Cleaned", str(stats['cleaned']))
        table.add_row("Pages Skipped", str(stats['skipped']))
        table.add_row("Pages Failed", str(stats['failed']))
        table.add_row("Total Processed", str(stats['total']))

        console.print(table)


def start(batch_size: int = 10, verbose: bool = True) -> dict:
    """
    Entry point for the cleaner.
    Called by manager CLI.
    """
    cleaner = Cleaner(batch_size=batch_size, verbose=verbose)
    return cleaner.clean()


if __name__ == "__main__":
    # Quick test
    start(batch_size=5)
