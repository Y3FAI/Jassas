"""
Deduplication Script - Clean database from duplicate URLs.
Handles www vs non-www and http vs https variations.
"""
import sys
import os
from urllib.parse import urlparse
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_db
from rich.console import Console
from rich.table import Table

console = Console()


def normalize_url(url: str) -> str:
    """
    Normalize URL to canonical form.
    - Force https
    - Remove www subdomain for my.gov.sa domain
    - Keep path, query as-is
    """
    parsed = urlparse(url)

    # Force https
    scheme = 'https'

    # Remove www subdomain for my.gov.sa
    netloc = parsed.netloc.lower()
    if netloc.startswith('www.'):
        netloc = netloc[4:]

    # Rebuild URL
    path = parsed.path
    # Remove trailing slash (except for root)
    if path.endswith('/') and len(path) > 1:
        path = path[:-1]

    normalized = f"{scheme}://{netloc}{path}"

    # Keep query string if present
    if parsed.query:
        normalized = f"{normalized}?{parsed.query}"

    return normalized


def find_duplicates_in_table(table_name: str, url_column: str = 'url') -> dict:
    """
    Find duplicate URLs in a table based on normalized form.
    Returns: {normalized_url: [list of (id, original_url) tuples]}
    """
    with get_db() as conn:
        cursor = conn.execute(f"SELECT id, {url_column} FROM {table_name}")
        rows = cursor.fetchall()

    # Group by normalized URL
    url_groups = defaultdict(list)
    for row_id, url in rows:
        normalized = normalize_url(url)
        url_groups[normalized].append((row_id, url))

    # Filter to only duplicates (2+ entries)
    duplicates = {
        norm_url: entries
        for norm_url, entries in url_groups.items()
        if len(entries) > 1
    }

    return duplicates


def deduplicate_frontier():
    """Remove duplicate URLs from frontier table."""
    console.print("\n[cyan]Checking frontier table...[/cyan]")

    duplicates = find_duplicates_in_table('frontier')

    if not duplicates:
        console.print("[green]No duplicates found in frontier![/green]")
        return 0

    console.print(f"[yellow]Found {len(duplicates)} groups of duplicate URLs[/yellow]")

    # For each duplicate group, keep the one with highest priority, then oldest
    removed_count = 0
    with get_db() as conn:
        for norm_url, entries in duplicates.items():
            # Sort by: priority DESC, id ASC (oldest first)
            cursor = conn.execute(
                f"""SELECT id, url, priority, status
                    FROM frontier
                    WHERE id IN ({','.join(['?'] * len(entries))})
                    ORDER BY priority DESC, id ASC""",
                [entry[0] for entry in entries]
            )
            rows = cursor.fetchall()

            # Keep first (highest priority/oldest), delete rest
            keep_id = rows[0]['id']
            keep_url = rows[0]['url']
            delete_ids = [row['id'] for row in rows[1:]]

            if delete_ids:
                conn.execute(
                    f"DELETE FROM frontier WHERE id IN ({','.join(['?'] * len(delete_ids))})",
                    delete_ids
                )
                removed_count += len(delete_ids)

                console.print(f"  [dim]Kept: {keep_url} (id={keep_id})[/dim]")
                console.print(f"  [dim]Removed {len(delete_ids)} duplicates[/dim]")

    console.print(f"[green]Removed {removed_count} duplicate URLs from frontier[/green]")
    return removed_count


def deduplicate_raw_pages():
    """Remove duplicate URLs from raw_pages table."""
    console.print("\n[cyan]Checking raw_pages table...[/cyan]")

    duplicates = find_duplicates_in_table('raw_pages')

    if not duplicates:
        console.print("[green]No duplicates found in raw_pages![/green]")
        return 0

    console.print(f"[yellow]Found {len(duplicates)} groups of duplicate URLs[/yellow]")

    # For each duplicate group, keep the oldest (lowest id)
    # But first need to handle foreign key references in documents
    removed_count = 0
    with get_db() as conn:
        for norm_url, entries in duplicates.items():
            # Sort by id ASC (oldest first)
            ids = [entry[0] for entry in entries]
            ids.sort()

            keep_id = ids[0]
            delete_ids = ids[1:]

            # Update documents table to point to the kept raw_page
            for delete_id in delete_ids:
                conn.execute(
                    "UPDATE documents SET raw_page_id = ? WHERE raw_page_id = ?",
                    (keep_id, delete_id)
                )

            # Now delete the duplicate raw_pages
            conn.execute(
                f"DELETE FROM raw_pages WHERE id IN ({','.join(['?'] * len(delete_ids))})",
                delete_ids
            )
            removed_count += len(delete_ids)

            keep_url = next(e[1] for e in entries if e[0] == keep_id)
            console.print(f"  [dim]Kept: {keep_url} (id={keep_id})[/dim]")
            console.print(f"  [dim]Removed {len(delete_ids)} duplicates, updated documents[/dim]")

    console.print(f"[green]Removed {removed_count} duplicate URLs from raw_pages[/green]")
    return removed_count


def deduplicate_documents():
    """
    Remove duplicate URLs from documents table.
    Note: documents table doesn't have UNIQUE constraint on url,
    but we should still check for duplicates.
    """
    console.print("\n[cyan]Checking documents table...[/cyan]")

    duplicates = find_duplicates_in_table('documents')

    if not duplicates:
        console.print("[green]No duplicates found in documents![/green]")
        return 0

    console.print(f"[yellow]Found {len(duplicates)} groups of duplicate URLs[/yellow]")

    # For each duplicate group, keep the oldest (lowest id)
    removed_count = 0
    with get_db() as conn:
        for norm_url, entries in duplicates.items():
            # Sort by id ASC (oldest first)
            ids = [entry[0] for entry in entries]
            ids.sort()

            keep_id = ids[0]
            delete_ids = ids[1:]

            # Delete entries from inverted_index first (foreign key constraint)
            for delete_id in delete_ids:
                conn.execute(
                    "DELETE FROM inverted_index WHERE doc_id = ?",
                    (delete_id,)
                )

            # Now delete the duplicate documents
            conn.execute(
                f"DELETE FROM documents WHERE id IN ({','.join(['?'] * len(delete_ids))})",
                delete_ids
            )
            removed_count += len(delete_ids)

            keep_url = next(e[1] for e in entries if e[0] == keep_id)
            console.print(f"  [dim]Kept: {keep_url} (id={keep_id})[/dim]")
            console.print(f"  [dim]Removed {len(delete_ids)} duplicates[/dim]")

    console.print(f"[green]Removed {removed_count} duplicate URLs from documents[/green]")
    return removed_count


def show_summary():
    """Show database statistics after cleanup."""
    console.print("\n[bold cyan]Database Summary[/bold cyan]")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Table", style="cyan")
    table.add_column("Row Count", justify="right", style="green")

    with get_db() as conn:
        for table_name in ['frontier', 'raw_pages', 'documents']:
            cursor = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            table.add_row(table_name, str(count))

    console.print(table)


def main():
    """Run deduplication on all tables."""
    console.print("[bold cyan]Jassas URL Deduplication Script[/bold cyan]")
    console.print("Normalizing: https, no www, canonical paths\n")

    # Show stats before
    show_summary()

    # Deduplicate each table
    frontier_removed = deduplicate_frontier()
    raw_pages_removed = deduplicate_raw_pages()
    documents_removed = deduplicate_documents()

    # Show stats after
    show_summary()

    # Summary
    total_removed = frontier_removed + raw_pages_removed + documents_removed
    console.print(f"\n[bold green]Total URLs removed: {total_removed}[/bold green]")

    if documents_removed > 0:
        console.print("[yellow]Note: Run 'jassas build' to rebuild search indexes since documents were modified[/yellow]")


if __name__ == "__main__":
    main()
