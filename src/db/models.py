"""
Database models (CRUD operations) for Jassas Search Engine.
Each class handles operations for one table.
"""
from datetime import datetime
from typing import Optional, List, Tuple
from .connection import get_db


class Frontier:
    """URL queue operations for Crawler with priority support."""

    @staticmethod
    def add_url(url: str, depth: int = 0, priority: int = 0) -> bool:
        """Add URL to frontier with priority. Returns False if already exists."""
        with get_db() as conn:
            try:
                conn.execute(
                    "INSERT INTO frontier (url, depth, priority) VALUES (?, ?, ?)",
                    (url, depth, priority)
                )
                return True
            except Exception:
                return False

    @staticmethod
    def add_urls(urls: List[Tuple[str, int, int]]) -> int:
        """
        Bulk add URLs with priority. Returns count of newly added.
        Each tuple: (url, depth, priority)
        """
        added = 0
        with get_db() as conn:
            for item in urls:
                try:
                    if len(item) == 3:
                        url, depth, priority = item
                    else:
                        # Backward compatibility: (url, depth)
                        url, depth = item
                        priority = 0
                    conn.execute(
                        "INSERT INTO frontier (url, depth, priority) VALUES (?, ?, ?)",
                        (url, depth, priority)
                    )
                    added += 1
                except Exception:
                    pass
        return added

    @staticmethod
    def get_next_pending(limit: int = 1) -> List[dict]:
        """Get next pending URLs ordered by priority (desc), then depth (asc)."""
        with get_db() as conn:
            cursor = conn.execute(
                """SELECT id, url, depth, priority FROM frontier
                   WHERE status = 'pending'
                   ORDER BY priority DESC, depth ASC, id ASC
                   LIMIT ?""",
                (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def mark_in_progress(url_id: int) -> None:
        """Mark URL as being crawled."""
        with get_db() as conn:
            conn.execute(
                """UPDATE frontier
                   SET status = 'in_progress', updated_at = ?
                   WHERE id = ?""",
                (datetime.now(), url_id)
            )

    @staticmethod
    def mark_crawled(url_id: int) -> None:
        """Mark URL as successfully crawled."""
        with get_db() as conn:
            conn.execute(
                """UPDATE frontier
                   SET status = 'crawled', updated_at = ?
                   WHERE id = ?""",
                (datetime.now(), url_id)
            )

    @staticmethod
    def mark_error(url_id: int, error_message: str) -> None:
        """Mark URL as failed with error message."""
        with get_db() as conn:
            conn.execute(
                """UPDATE frontier
                   SET status = 'error', error_message = ?, updated_at = ?
                   WHERE id = ?""",
                (error_message, datetime.now(), url_id)
            )

    @staticmethod
    def get_stats() -> dict:
        """Get frontier statistics."""
        with get_db() as conn:
            cursor = conn.execute(
                """SELECT status, COUNT(*) as count
                   FROM frontier GROUP BY status"""
            )
            return {row['status']: row['count'] for row in cursor.fetchall()}


class RawPages:
    """Raw HTML storage operations for Crawler."""

    @staticmethod
    def save(url: str, html_content: bytes, content_hash: str, http_status: int) -> int:
        """Save raw page. Returns page ID."""
        with get_db() as conn:
            cursor = conn.execute(
                """INSERT INTO raw_pages (url, html_content, content_hash, http_status)
                   VALUES (?, ?, ?, ?)""",
                (url, html_content, content_hash, http_status)
            )
            return cursor.lastrowid

    @staticmethod
    def exists_by_hash(content_hash: str) -> bool:
        """Check if page with same content already exists."""
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT 1 FROM raw_pages WHERE content_hash = ? LIMIT 1",
                (content_hash,)
            )
            return cursor.fetchone() is not None

    @staticmethod
    def get_by_id(page_id: int) -> Optional[dict]:
        """Get raw page by ID."""
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM raw_pages WHERE id = ?",
                (page_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_uncleaned(limit: int = 10) -> List[dict]:
        """Get raw pages not yet cleaned."""
        with get_db() as conn:
            cursor = conn.execute(
                """SELECT rp.* FROM raw_pages rp
                   LEFT JOIN documents d ON d.raw_page_id = rp.id
                   WHERE d.id IS NULL
                   LIMIT ?""",
                (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]


class Documents:
    """Cleaned document operations for Cleaner/Tokenizer."""

    @staticmethod
    def create(raw_page_id: int, url: str, title: str, clean_text: str, doc_len: int, description: str = None) -> int:
        """Create cleaned document. Returns document ID."""
        with get_db() as conn:
            cursor = conn.execute(
                """INSERT INTO documents (raw_page_id, url, title, description, clean_text, doc_len)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (raw_page_id, url, title, description, clean_text, doc_len)
            )
            return cursor.lastrowid

    @staticmethod
    def get_pending(limit: int = 10) -> List[dict]:
        """Get documents pending tokenization."""
        with get_db() as conn:
            cursor = conn.execute(
                """SELECT id, url, title, description, clean_text, doc_len
                   FROM documents
                   WHERE status = 'pending'
                   LIMIT ?""",
                (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def mark_tokenized(doc_id: int) -> None:
        """Mark document as tokenized."""
        with get_db() as conn:
            conn.execute(
                "UPDATE documents SET status = 'tokenized' WHERE id = ?",
                (doc_id,)
            )

    @staticmethod
    def get_by_id(doc_id: int) -> Optional[dict]:
        """Get document by ID."""
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM documents WHERE id = ?",
                (doc_id,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_avg_doc_len() -> float:
        """Get average document length (for BM25)."""
        with get_db() as conn:
            cursor = conn.execute("SELECT AVG(doc_len) FROM documents")
            result = cursor.fetchone()[0]
            return result if result else 0.0

    @staticmethod
    def get_total_count() -> int:
        """Get total document count."""
        with get_db() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM documents")
            return cursor.fetchone()[0]

    @staticmethod
    def get_tokenized_count() -> int:
        """Get tokenized (searchable) document count."""
        with get_db() as conn:
            cursor = conn.execute("SELECT COUNT(*) FROM documents WHERE status = 'tokenized'")
            return cursor.fetchone()[0]


class Vocab:
    """Vocabulary operations for Tokenizer."""

    @staticmethod
    def get_or_create(token: str) -> int:
        """Get token ID, creating if needed."""
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT id FROM vocab WHERE token = ?",
                (token,)
            )
            row = cursor.fetchone()
            if row:
                return row['id']

            cursor = conn.execute(
                "INSERT INTO vocab (token, doc_count) VALUES (?, 0)",
                (token,)
            )
            return cursor.lastrowid

    @staticmethod
    def increment_doc_count(vocab_id: int) -> None:
        """Increment document count for a token."""
        with get_db() as conn:
            conn.execute(
                "UPDATE vocab SET doc_count = doc_count + 1 WHERE id = ?",
                (vocab_id,)
            )

    @staticmethod
    def get_by_token(token: str) -> Optional[dict]:
        """Get vocab entry by token."""
        with get_db() as conn:
            cursor = conn.execute(
                "SELECT * FROM vocab WHERE token = ?",
                (token,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None

    @staticmethod
    def get_by_tokens(tokens: List[str]) -> List[dict]:
        """Get vocab entries for multiple tokens."""
        if not tokens:
            return []
        placeholders = ','.join(['?'] * len(tokens))
        with get_db() as conn:
            cursor = conn.execute(
                f"SELECT * FROM vocab WHERE token IN ({placeholders})",
                tokens
            )
            return [dict(row) for row in cursor.fetchall()]


class InvertedIndex:
    """Inverted index operations for Tokenizer/Ranker."""

    @staticmethod
    def add_entry(vocab_id: int, doc_id: int, frequency: int) -> None:
        """Add index entry."""
        with get_db() as conn:
            conn.execute(
                """INSERT OR REPLACE INTO inverted_index (vocab_id, doc_id, frequency)
                   VALUES (?, ?, ?)""",
                (vocab_id, doc_id, frequency)
            )

    @staticmethod
    def add_entries(entries: List[Tuple[int, int, int]]) -> None:
        """Bulk add index entries. Each entry: (vocab_id, doc_id, frequency)."""
        with get_db() as conn:
            conn.executemany(
                """INSERT OR REPLACE INTO inverted_index (vocab_id, doc_id, frequency)
                   VALUES (?, ?, ?)""",
                entries
            )

    @staticmethod
    def search(vocab_ids: List[int]) -> List[dict]:
        """Search index for documents containing any of the vocab IDs."""
        if not vocab_ids:
            return []
        placeholders = ','.join(['?'] * len(vocab_ids))
        with get_db() as conn:
            cursor = conn.execute(
                f"""SELECT doc_id, vocab_id, frequency
                    FROM inverted_index
                    WHERE vocab_id IN ({placeholders})""",
                vocab_ids
            )
            return [dict(row) for row in cursor.fetchall()]

    @staticmethod
    def get_doc_frequencies(doc_id: int) -> List[dict]:
        """Get all term frequencies for a document."""
        with get_db() as conn:
            cursor = conn.execute(
                """SELECT v.token, ii.frequency
                   FROM inverted_index ii
                   JOIN vocab v ON v.id = ii.vocab_id
                   WHERE ii.doc_id = ?""",
                (doc_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
