"""
Backfill title_display and description_display for existing documents.
Re-parses raw HTML to extract original (non-normalized) text.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import sqlite3
from cleaner.sites import get_parser

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'jassas.db')


def backfill():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get documents missing display fields
    cursor.execute("""
        SELECT d.id, d.url, rp.html_content
        FROM documents d
        JOIN raw_pages rp ON rp.id = d.raw_page_id
        WHERE d.title_display IS NULL OR d.title_display = ''
    """)

    docs = cursor.fetchall()
    print(f"Found {len(docs)} documents to backfill\n")

    updated = 0
    for doc in docs:
        doc_id = doc['id']
        url = doc['url']
        html = doc['html_content']

        # Decode HTML
        if isinstance(html, bytes):
            try:
                html = html.decode('utf-8')
            except:
                html = html.decode('utf-8', errors='replace')

        # Parse with site-specific parser
        parser = get_parser(url)
        result = parser.parse(html)

        title_display = result.get('title_display', '')
        description_display = result.get('description_display', '')

        if title_display or description_display:
            cursor.execute("""
                UPDATE documents
                SET title_display = ?, description_display = ?
                WHERE id = ?
            """, (title_display, description_display, doc_id))
            updated += 1
            print(f"[{updated}] {title_display[:60]}...")

    conn.commit()
    conn.close()
    print(f"\nDone! Updated {updated} documents.")


if __name__ == "__main__":
    backfill()
