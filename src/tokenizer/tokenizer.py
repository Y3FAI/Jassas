"""
Tokenizer - Orchestrates BM25 and vector indexing.
Processes documents → inverted_index + vectors.usearch
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.table import Table
from rich import box

from db import Documents, Vocab, InvertedIndex
from db.connection import get_db
from tokenizer.bm25 import BM25Tokenizer
from tokenizer.vector import VectorEngine

console = Console()


class Tokenizer:
    """Builds BM25 inverted index and vector embeddings."""

    def __init__(self, batch_size: int = 32, verbose: bool = True, save_every: int = 5):
        self.batch_size = batch_size
        self.verbose = verbose
        self.save_every = save_every  # Save index every N batches

        self.bm25 = BM25Tokenizer()
        self.vector = VectorEngine(batch_size=batch_size)

        # Stats
        self.docs_processed = 0
        self.tokens_added = 0
        self.vectors_added = 0
        self.batches_processed = 0

    def log(self, message: str, style: str = ""):
        """Print if verbose mode."""
        if self.verbose:
            console.print(message, style=style)

    def tokenize(self) -> dict:
        """
        Main tokenization loop.
        Processes pending documents in batches.
        """
        self.log("[bold cyan]Starting Jassas Tokenizer[/bold cyan]")
        self.log(f"  Batch size: {self.batch_size}")
        self.log(f"  Vector model: {self.vector.MODEL_NAME}\n")

        # Load or create vector index
        if self.vector.load_index():
            self.log(f"[dim]Loaded existing vector index ({self.vector.get_count()} vectors)[/dim]")
        else:
            self.log("[dim]Creating new vector index[/dim]")
            self.vector.create_index()

        # Load model once
        self.log("[cyan]Loading embedding model...[/cyan]")
        self.vector.load_model()
        self.log("[green]Model loaded[/green]\n")

        while True:
            # Get batch of pending documents
            batch = Documents.get_pending(limit=self.batch_size)

            if not batch:
                self.log("\n[yellow]No more pending documents.[/yellow]")
                break

            self.log(f"[cyan]Processing batch of {len(batch)} documents...[/cyan]")
            self._process_batch(batch)
            self.batches_processed += 1

            # Save incrementally every N batches (allows searching while tokenizing)
            if self.batches_processed % self.save_every == 0:
                self.log(f"[dim]Saving checkpoint ({self.vector.get_count()} vectors)...[/dim]")
                self.vector.save_index()

        # Final save
        self.log("\n[cyan]Saving vector index...[/cyan]")
        self.vector.save_index()
        self.log(f"[green]Saved {self.vector.get_count()} vectors[/green]")

        # Summary
        self.log("\n[bold green]Tokenization Complete![/bold green]")
        stats = self.get_stats()
        self._print_stats(stats)
        return stats

    def _process_batch(self, batch: list):
        """Process a batch of documents."""
        doc_ids = []
        texts = []

        for doc in batch:
            doc_id = doc['id']
            text = doc['clean_text']
            title = doc['title']

            # 1. BM25: Build inverted index
            term_freqs = self.bm25.get_term_frequencies(text)
            self._add_to_index(doc_id, term_freqs)

            # 2. Prepare for vector embedding (title + description only)
            doc_ids.append(doc_id)
            description = doc.get('description', '')
            # E5 works best with concise text - title + description
            embed_text = f"{title}. {description}" if description else title
            texts.append(embed_text)

            self.docs_processed += 1

        # 3. Vector: Generate embeddings for batch
        if doc_ids:
            self.vector.add_documents(doc_ids, texts)
            self.vectors_added += len(doc_ids)

        # 4. Mark documents as tokenized
        for doc in batch:
            Documents.mark_tokenized(doc['id'])
            self.log(f"  [green]Tokenized[/green]: {doc['title'][:50]}...")

    def _add_to_index(self, doc_id: int, term_freqs: dict):
        """Add document terms to inverted index."""
        entries = []

        for token, freq in term_freqs.items():
            # Get or create vocab entry
            vocab_id = Vocab.get_or_create(token)

            # Increment doc count for this term
            Vocab.increment_doc_count(vocab_id)

            # Add to inverted index
            entries.append((vocab_id, doc_id, freq))
            self.tokens_added += 1

        # Bulk insert
        if entries:
            InvertedIndex.add_entries(entries)

    def get_stats(self) -> dict:
        """Get tokenization statistics."""
        return {
            'docs_processed': self.docs_processed,
            'tokens_added': self.tokens_added,
            'vectors_added': self.vectors_added,
            'total_vectors': self.vector.get_count(),
        }

    def _print_stats(self, stats: dict):
        """Print stats summary."""
        table = Table(title="Tokenization Statistics", box=box.ROUNDED)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green", justify="right")

        table.add_row("Documents Processed", str(stats['docs_processed']))
        table.add_row("Index Entries Added", str(stats['tokens_added']))
        table.add_row("Vectors Added", str(stats['vectors_added']))
        table.add_row("Total Vectors in Index", str(stats['total_vectors']))

        console.print(table)


def start(batch_size: int = 32, verbose: bool = True) -> dict:
    """
    Entry point for the tokenizer.
    Called by manager CLI.
    """
    tokenizer = Tokenizer(batch_size=batch_size, verbose=verbose)
    return tokenizer.tokenize()


if __name__ == "__main__":
    # Quick test
    start(batch_size=10)
