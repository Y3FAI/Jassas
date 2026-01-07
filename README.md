<div align="center">

# جساس | Jassas

**Search Engine for Saudi Arabia**

[Live Demo](https://jassas.y3f.me) · [API](#api) · [Architecture](#architecture)

![License](https://img.shields.io/badge/License-MIT-yellow)
![Python](http://img.shields.io/badge/Python-3-blue)
!

</div>

---

## Why Jassas?

Saudi Arabia's government portal hosts thousands of services, but finding specific information requires navigating dense, nested Arabic pages. Google indexes broadly but shallowly — it skips PDFs and doesn't crawl deep into government portals.

Jassas goes deep on a focused niche: **Saudi Arabia**.

**Try it live:** [jassas.y3f.me](https://jassas.y3f.me)

---

## Semantic Search in Action

Understanding **what users mean**, not just what they type.

| Query (Saudi Dialect)          | Result (Formal Arabic)              | Time |
| ------------------------------ | ----------------------------------- | ---- |
| ابغى اجدد اقامتي               | تجديد الإقامة                       | 89ms |
| _(I wanna renew my residency)_ | _(Residency Renewal)_               |      |
| كيف افتح محل                   | خدمة طلب اصدار رخصة محل تجاري       | 55ms |
| _(How do I open a shop?)_      | _(Commercial Shop License Service)_ |      |
| ضريبة الشراء                   | التسجيل في ضريبة القيمة المضافة     | 64ms |
| _(Purchase tax)_               | _(VAT Registration)_                |      |
| ابي اسوي شركة                  | دليل الشركات الناشئة                | 74ms |
| _(I wanna make a company)_     | _(Startup Guide)_                   |      |

---

## Key Features

### Self-Contained

No external APIs. No managed services. No vendor lock-in, open source tooling only.

| Component      | Solution               | NOT Using               |
| -------------- | ---------------------- | ----------------------- |
| Embeddings     | FastEmbed (local ONNX) | ~~OpenAI API~~          |
| Vector Index   | USearch (local file)   | ~~Pinecone, Weaviate~~  |
| Lexical Search | NumPy Sparse Matrix    | ~~Elasticsearch, Solr~~ |
| Database       | SQLite                 | ~~PostgreSQL, MongoDB~~ |

**Deploy anywhere with Python. Works offline. Zero API costs.**

### Optimized for Minimal Hardware

Running semantic search on **2 vCPU / 4GB RAM**:

| Optimization                 | Impact                               |
| ---------------------------- | ------------------------------------ |
| NumPy Sparse BM25            | 800ms → 3ms (266x faster)            |
| FastEmbed (ONNX)             | ~500MB vs ~2GB PyTorch               |
| Half-precision vectors (f16) | 50% memory reduction                 |
| Parallel search execution    | Latency = max(BM25, Vector), not sum |

### Hybrid Search Strategy

| Strategy      | Purpose                                            | Speed  |
| ------------- | -------------------------------------------------- | ------ |
| **BM25**      | Exact Arabic keyword matching                      | ~3ms   |
| **Vector**    | Semantic understanding (dialect, synonyms, intent) | ~50ms  |
| **RRF Merge** | Combines rankings without tuning                   | 0.03ms |

---

## Performance

| Metric            | Value         |
| ----------------- | ------------- |
| **Query Latency** | ~65ms         |
| **Indexed Pages** | 5,243         |
| **Vocabulary**    | 15,561 tokens |
| **Index Size**    | 17.5 MB       |

> Production server: 2 vCPU, 4GB RAM , $12/month VPS

---

## Architecture

### Query Pipeline

```
Query: "تجديد الاقامة"
         │
         ▼
   ┌─────────────────┐
   │   Normalize     │  Arabic text normalization
   │    (0.5ms)      │  (tashkeel, alif unification)
   └─────────────────┘
         │
         ├──────────────────────────────┐
         ▼                              ▼
   ┌───────────┐                 ┌─────────────┐
   │   BM25    │    parallel     │   Vector    │
   │  (3ms)    │◄───threads────►│   (50ms)    │
   │           │                 │             │
   │  NumPy    │                 │  FastEmbed  │
   │  Sparse   │                 │  + USearch  │
   └───────────┘                 └─────────────┘
         │                              │
         └──────────────┬───────────────┘
                        ▼
               ┌─────────────────┐
               │    RRF Merge    │
               │    (0.03ms)     │
               │                 │
               │ score = Σ 1/(k+rank) │
               └─────────────────┘
                        │
                        ▼
                 Top 10 Results
                    (~65ms)
```

### System Overview

```
                        ┌─────────────┐
                        │   MANAGER   │
                        │    (CLI)    │
                        └──────┬──────┘
                               │ controls
       ┌───────────┬───────────┼───────────┬───────────┐
       ▼           ▼           ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌───────────┐ ┌──────────┐ ┌──────────┐
│ CRAWLER  │ │ CLEANER  │ │ TOKENIZER │ │  RANKER  │ │   API    │
│          │ │          │ │           │ │          │ │          │
│ BFS      │ │ HTML→Text│ │ BM25+Vec  │ │ RRF      │ │ FastAPI  │
└────┬─────┘ └────┬─────┘ └─────┬─────┘ └────┬─────┘ └────┬─────┘
     │            │             │            │            │
     └────────────┴──────┬──────┴────────────┴────────────┘
                         ▼
                  ┌─────────────┐
                  │  DATABASE   │
                  │   SQLite    │
                  │      +      │
                  │   USearch   │
                  └─────────────┘
```

**Data Flow:**

```
my.gov.sa ──▶ CRAWLER ──▶ CLEANER ──▶ TOKENIZER ──▶ DATABASE
                                                        │
USER QUERY ──▶ RANKER ◀─────────────────────────────────┘
                  │
                  ▼
             API RESPONSE (~65ms)
```

---

## Engineering Deep Dive

### BM25: From 800ms to 3ms

**Problem:** SQL-based BM25 with JOIN operations became O(n²) at scale.

```sql
-- Before: 800ms at 5k documents
SELECT doc_id, SUM(tf * idf) as score
FROM inverted_index JOIN vocab ON ...
GROUP BY doc_id ORDER BY score DESC
```

**Solution:** Precompile inverted index into a NumPy sparse matrix. Scoring becomes a single dot product.

```python
# After: 3ms at 5k documents
scores = self.term_matrix.dot(query_vector)  # O(nnz)
top_k = np.argpartition(scores, -k)[-k:]
```

### Parallel Search Execution

Vector search dominates latency (~50ms). Running BM25 in parallel hides its cost:

```python
with ThreadPoolExecutor(max_workers=2) as executor:
    bm25_future = executor.submit(self._bm25_search, query)
    vector_future = executor.submit(self._vector_search, query)
```

**Result:** Total latency = max(BM25, Vector) instead of sum.

### FastEmbed over Sentence-Transformers

|           | Sentence-Transformers | FastEmbed     |
| --------- | --------------------- | ------------- |
| Runtime   | PyTorch               | ONNX          |
| Memory    | ~2GB                  | ~500MB        |
| Inference | Baseline              | **3x faster** |

---

## Tech Stack

| Component      | Technology                                     |
| -------------- | ---------------------------------------------- |
| **Search**     | NumPy Sparse Matrices + USearch HNSW           |
| **Embeddings** | FastEmbed + `multilingual-e5-large` (1024-dim) |
| **API**        | FastAPI + Uvicorn                              |
| **Database**   | SQLite                                         |
| **Crawling**   | Requests + Cloudscraper + Playwright           |
| **Frontend**   | Pure HTML/CSS (RTL Arabic)                     |

---

## API

```bash
# GET request
curl "https://jassas.y3f.me/api/v1/search?q=تجديد+رخصة&limit=5"

# POST request
curl -X POST "https://jassas.y3f.me/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "كيف افتح محل", "limit": 5}'
```

**Response:**

```json
{
    "query": "كيف افتح محل",
    "count": 5,
    "execution_time_ms": 55.23,
    "results": [
        {
            "title": "خدمة طلب اصدار رخصة محل تجاري",
            "url": "https://my.gov.sa/ar/services/304066",
            "snippet": "خدمة تقدم إلكترونيا وتتيح الخدمة امكانية طلب المستثمرين...",
            "score": 0.0164
        }
    ]
}
```

---

## Quick Start

```bash
git clone https://github.com/y3f/jassas.git
cd jassas
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Build index
./jassas init
./jassas crawl --sitemap "https://my.gov.sa/sitemap.xml" --max-pages 1000
./jassas clean --batch 10
./jassas build --batch 32

# Search
./jassas search "تجديد الاقامة" --limit 10

# Start server
python src/api/main.py
```

---

## Project Structure

```
src/
├── api/          # FastAPI server + endpoints
├── ranker/       # Hybrid search (BM25 + Vector + RRF)
├── tokenizer/    # Indexing pipeline
├── crawler/      # BFS spider with CloudFlare bypass
├── cleaner/      # HTML parsing + Arabic normalization
└── manager/      # CLI (Typer + Rich)

data/
├── jassas.db         # SQLite: pages + metadata
├── bm25_matrix.pkl   # Sparse matrix (5.5 MB)
└── vectors.usearch   # HNSW index (12 MB)
```

---

## Roadmap

| Feature                   | Description                                                                               |
| ------------------------- | ----------------------------------------------------------------------------------------- |
| **Q&A with LLM**          | Direct answers using LLM — "ما هي رسوم تجديد الإقامة؟" returns the answer, not just links |
| **PDF Document Indexing** | OCR + text extraction from government PDFs                                                |
| **Expand Coverage**       | Crawl more Saudi sources: Visit Saudi, MOI, MOFA, Saudi Tourism                           |
| **Query Understanding**   | Better Saudi dialect handling, query expansion, spelling correction                       |

**Goal:** The go-to search engine for Saudi Arabia — for residents, tourists, businesses, and researchers.

---

## Limitations

-   **Saudi focus** — currently indexing my.gov.sa, expanding to more sources
-   **Single-node** — vertically scalable, not horizontally distributed
-   **Full rebuild** — no incremental indexing yet

---

## License

MIT

---

<div align="center">

**[Live Demo](https://jassas.y3f.me)** · Built by [Y3F](https://github.com/y3f)

</div>
