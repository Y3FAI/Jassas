"""
Mine Hard Negatives using BM25.

Hard negatives = documents that are lexically similar but semantically different.
These are crucial for teaching the model to distinguish subtle differences.

Example:
  Query: "غرامة تأخير الجواز" (passport late fine)
  Positive: "غرامة التأخير 500 ريال" (fine is 500 SAR)
  Hard Negative: "رسوم تجديد الجواز 300 ريال" (renewal FEE is 300 SAR)

The hard negative has high lexical overlap (جواز, ريال) but wrong meaning.

Usage:
    python scripts/mine_hard_negatives.py
"""
import os
import sys
import json
from pathlib import Path
from typing import List, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from db import Documents, Vocab
from db.connection import get_db
from ranker.bm25_numpy import NumPyBM25Engine
from tokenizer.bm25 import BM25Tokenizer

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
INPUT_PATH = PROJECT_ROOT / 'data' / 'training_pairs.jsonl'
OUTPUT_PATH = PROJECT_ROOT / 'data' / 'training_triplets.jsonl'
BM25_PATH = PROJECT_ROOT / 'data' / 'bm25_matrix.pkl'


def load_training_pairs() -> List[dict]:
    """Load existing training pairs."""
    if not INPUT_PATH.exists():
        print(f"Error: {INPUT_PATH} not found")
        print("Run generate_training_data.py first")
        sys.exit(1)

    pairs = []
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            pairs.append(json.loads(line))
    return pairs


def mine_hard_negatives(
    query: str,
    positive_doc_id: int,
    bm25_engine: NumPyBM25Engine,
    tokenizer: BM25Tokenizer,
    top_k: int = 10
) -> List[int]:
    """
    Find hard negatives: BM25-similar docs that are NOT the positive.

    Returns doc_ids of hard negatives (lexically similar but different docs).
    """
    # Tokenize query
    tokens = tokenizer.tokenize(query)
    if not tokens:
        return []

    # Convert to vocab IDs
    token_ids = []
    for token in tokens:
        vocab = Vocab.get_by_token(token)
        if vocab:
            token_ids.append(vocab['id'])

    if not token_ids:
        return []

    # BM25 search
    results = bm25_engine.search(token_ids, k=top_k + 1)

    # Filter out the positive document
    hard_negatives = [
        doc_id for doc_id, score in results
        if doc_id != positive_doc_id
    ]

    return hard_negatives[:top_k]


def main():
    print("Mining Hard Negatives with BM25...")

    # Load BM25 engine
    if not BM25_PATH.exists():
        print(f"Error: BM25 index not found at {BM25_PATH}")
        print("Run: jassas bm25")
        sys.exit(1)

    bm25_engine = NumPyBM25Engine(index_path=str(BM25_PATH))
    if not bm25_engine.load():
        print("Error: Failed to load BM25 index")
        sys.exit(1)

    tokenizer = BM25Tokenizer()

    # Load documents for text lookup
    doc_texts = {}
    with get_db() as conn:
        cursor = conn.execute(
            "SELECT id, title, description FROM documents WHERE status = 'tokenized'"
        )
        for row in cursor:
            doc_texts[row['id']] = f"{row['title']}. {row['description'] or ''}"

    # Load training pairs
    pairs = load_training_pairs()
    print(f"Loaded {len(pairs)} training pairs")

    # Mine hard negatives
    triplets = []
    skipped = 0

    for i, pair in enumerate(pairs):
        if i % 100 == 0:
            print(f"Processing {i}/{len(pairs)}...")

        query = pair['query']
        positive = pair['positive']
        positive_doc_id = pair.get('doc_id')

        if not positive_doc_id:
            skipped += 1
            continue

        # Find hard negatives
        hard_neg_ids = mine_hard_negatives(
            query, positive_doc_id, bm25_engine, tokenizer, top_k=3
        )

        if not hard_neg_ids:
            skipped += 1
            continue

        # Get text for hard negatives
        for neg_id in hard_neg_ids:
            if neg_id in doc_texts:
                triplets.append({
                    'query': query,
                    'positive': positive,
                    'negative': doc_texts[neg_id],
                    'positive_doc_id': positive_doc_id,
                    'negative_doc_id': neg_id
                })
                break  # Just take the first valid hard negative

    # Save triplets
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        for triplet in triplets:
            f.write(json.dumps(triplet, ensure_ascii=False) + '\n')

    print(f"\n✓ Generated {len(triplets)} triplets with hard negatives")
    print(f"  Skipped: {skipped}")
    print(f"  Saved to: {OUTPUT_PATH}")
    print("\nUpdate finetune_e5.py to use training_triplets.jsonl for better results!")


if __name__ == "__main__":
    main()
