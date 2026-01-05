"""
Fine-Tune E5-Large for Arabic Government Search.

Strategy:
1. Contrastive learning with InfoNCE loss
2. Hard negatives from BM25 (same topic, wrong answer)
3. In-batch negatives for efficiency

Usage:
    python scripts/finetune_e5.py

Requirements:
    pip install sentence-transformers datasets accelerate
"""
import os
import sys
import json
import random
from pathlib import Path
from typing import List, Dict

import torch
from torch.utils.data import DataLoader
from sentence_transformers import (
    SentenceTransformer,
    InputExample,
    losses,
    evaluation,
)
from sentence_transformers.trainer import SentenceTransformerTrainer
from sentence_transformers.training_args import SentenceTransformerTrainingArguments

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / 'data' / 'training_pairs.jsonl'
OUTPUT_PATH = PROJECT_ROOT / 'models' / 'jassas-e5-arabic'

# Config
MODEL_NAME = 'intfloat/multilingual-e5-large'
BATCH_SIZE = 8  # Reduce if OOM
EPOCHS = 3
LEARNING_RATE = 2e-5
WARMUP_RATIO = 0.1


def load_training_data() -> List[Dict]:
    """Load training pairs from JSONL file."""
    if not DATA_PATH.exists():
        print(f"Error: Training data not found at {DATA_PATH}")
        print("Run: python scripts/generate_training_data.py first")
        sys.exit(1)

    pairs = []
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            pairs.append(json.loads(line))

    print(f"Loaded {len(pairs)} training pairs")
    return pairs


def create_training_examples(pairs: List[Dict]) -> List[InputExample]:
    """
    Create training examples with E5 prefix format.

    E5 requires:
    - Queries: "query: <text>"
    - Documents: "passage: <text>"
    """
    examples = []

    # Group by doc_id for hard negative mining
    by_doc = {}
    for pair in pairs:
        doc_id = pair.get('doc_id', 0)
        if doc_id not in by_doc:
            by_doc[doc_id] = []
        by_doc[doc_id].append(pair)

    all_positives = [p['positive'] for p in pairs]

    for pair in pairs:
        query = f"query: {pair['query']}"
        positive = f"passage: {pair['positive']}"

        # Hard negative: random document from different doc_id
        negative_candidates = [p for p in all_positives if p != pair['positive']]
        if negative_candidates:
            negative = f"passage: {random.choice(negative_candidates)}"
        else:
            continue

        # Triplet: (anchor, positive, negative)
        examples.append(InputExample(
            texts=[query, positive, negative]
        ))

    print(f"Created {len(examples)} training examples (triplets)")
    return examples


def create_eval_examples(pairs: List[Dict], n_eval: int = 100) -> List[InputExample]:
    """Create evaluation examples."""
    eval_pairs = random.sample(pairs, min(n_eval, len(pairs)))
    examples = []

    for pair in eval_pairs:
        query = f"query: {pair['query']}"
        positive = f"passage: {pair['positive']}"
        examples.append(InputExample(texts=[query, positive], label=1.0))

    return examples


def main():
    print("=" * 60)
    print("Fine-Tuning E5-Large for Jassas Arabic Search")
    print("=" * 60)

    # Load data
    pairs = load_training_data()

    # Split train/eval
    random.shuffle(pairs)
    split_idx = int(len(pairs) * 0.9)
    train_pairs = pairs[:split_idx]
    eval_pairs = pairs[split_idx:]

    print(f"Train: {len(train_pairs)}, Eval: {len(eval_pairs)}")

    # Create examples
    train_examples = create_training_examples(train_pairs)

    # Load model
    print(f"\nLoading model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    # Training with MultipleNegativesRankingLoss (InfoNCE)
    # This is the standard loss for contrastive learning
    train_dataloader = DataLoader(
        train_examples,
        shuffle=True,
        batch_size=BATCH_SIZE
    )

    # Loss function: works with triplets (anchor, positive, negative)
    # Also uses in-batch negatives for efficiency
    train_loss = losses.MultipleNegativesRankingLoss(model)

    # Evaluator
    eval_examples = create_eval_examples(eval_pairs)
    evaluator = evaluation.EmbeddingSimilarityEvaluator.from_input_examples(
        eval_examples,
        name='arabic-gov-eval'
    )

    # Training arguments
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

    # Calculate warmup steps
    total_steps = len(train_dataloader) * EPOCHS
    warmup_steps = int(total_steps * WARMUP_RATIO)

    print(f"\nTraining config:")
    print(f"  Batch size: {BATCH_SIZE}")
    print(f"  Epochs: {EPOCHS}")
    print(f"  Learning rate: {LEARNING_RATE}")
    print(f"  Warmup steps: {warmup_steps}")
    print(f"  Total steps: {total_steps}")

    # Train
    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        evaluator=evaluator,
        epochs=EPOCHS,
        warmup_steps=warmup_steps,
        output_path=str(OUTPUT_PATH),
        show_progress_bar=True,
        evaluation_steps=500,
        save_best_model=True,
    )

    print(f"\n✓ Model saved to: {OUTPUT_PATH}")
    print("\nTo use the fine-tuned model, update VectorEngine:")
    print(f"  MODEL_NAME = '{OUTPUT_PATH}'")


if __name__ == "__main__":
    main()
