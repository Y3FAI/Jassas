"""
Generate Synthetic Training Data for E5 Fine-Tuning.
Uses LLM to create Arabic questions for each document.

Usage:
    python scripts/generate_training_data.py --limit 1000

Output:
    data/training_pairs.jsonl
"""
import os
import sys
import json
import argparse
import requests
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from db import Documents
from db.connection import get_db
from dotenv import load_dotenv

load_dotenv()

# Output path
OUTPUT_PATH = Path(__file__).parent.parent / 'data' / 'training_pairs.jsonl'


def generate_queries_batch(documents: list, api_key: str) -> list:
    """
    Generate synthetic Arabic queries for documents using LLM.
    Returns list of (query, positive_doc, hard_negative_doc) tuples.
    """
    # Build prompt for batch generation
    doc_texts = []
    for i, doc in enumerate(documents):
        title = doc['title']
        desc = doc.get('description', '')
        text = doc.get('clean_text', '')[:500]
        doc_texts.append(f"[مستند {i+1}]\nالعنوان: {title}\nالوصف: {desc}\nالمحتوى: {text[:300]}")

    prompt = f"""أنت خبير في إنشاء أسئلة بحث باللغة العربية للبوابات الحكومية السعودية.

لكل مستند أدناه، أنشئ 3 أسئلة بحث طبيعية قد يطرحها مواطن سعودي:
- سؤال مباشر (ما هو، كم، متى)
- سؤال عن الإجراء (كيف أقوم بـ)
- سؤال عن الشروط (ما هي شروط/متطلبات)

{chr(10).join(doc_texts)}

أجب بتنسيق JSON فقط:
[
  {{"doc_id": 1, "queries": ["سؤال 1", "سؤال 2", "سؤال 3"]}},
  ...
]"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "google/gemini-2.0-flash-001",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 2000
        }
    )

    if response.status_code != 200:
        print(f"API Error: {response.status_code}")
        return []

    try:
        content = response.json()['choices'][0]['message']['content']
        # Extract JSON from response
        start = content.find('[')
        end = content.rfind(']') + 1
        if start >= 0 and end > start:
            return json.loads(content[start:end])
    except Exception as e:
        print(f"Parse error: {e}")

    return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=500, help='Number of documents to process')
    parser.add_argument('--batch-size', type=int, default=5, help='Documents per API call')
    args = parser.parse_args()

    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("Error: OPENROUTER_API_KEY not found in .env")
        sys.exit(1)

    print(f"Generating training data for {args.limit} documents...")

    # Get documents
    with get_db() as conn:
        cursor = conn.execute("""
            SELECT id, title, description, clean_text
            FROM documents
            WHERE status = 'tokenized'
            LIMIT ?
        """, (args.limit,))
        documents = [dict(row) for row in cursor.fetchall()]

    print(f"Loaded {len(documents)} documents")

    # Generate queries in batches
    training_pairs = []

    for i in range(0, len(documents), args.batch_size):
        batch = documents[i:i + args.batch_size]
        print(f"Processing batch {i//args.batch_size + 1}/{(len(documents)-1)//args.batch_size + 1}...")

        results = generate_queries_batch(batch, api_key)

        for result in results:
            doc_idx = result.get('doc_id', 1) - 1
            if 0 <= doc_idx < len(batch):
                doc = batch[doc_idx]
                for query in result.get('queries', []):
                    training_pairs.append({
                        'query': query,
                        'positive': f"{doc['title']}. {doc.get('description', '')}",
                        'doc_id': doc['id']
                    })

    # Save training data
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        for pair in training_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')

    print(f"\n✓ Generated {len(training_pairs)} training pairs")
    print(f"  Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
