| Model       | Layers | Server (ms) | MacBook Air (ms) | Accuracy |
| ----------- | ------ | ----------- | ---------------- | -------- |
| MiniLM-L12  | 12     | 362.5ms     | 66.4ms           | 100%     |
| MiniLM-L6   | 6      | 168.9ms     | 30.6ms           | 100%     |
| MiniLM-L4   | 4      | 115.8ms     | 22.4ms           | 100%     |
| TinyBERT-L2 | 2      | 11.7ms      | 16.7ms           | 43%      |

---

Running Benchmark...
BAAI/bge-reranker-base  
 Report  
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Metric ┃ Value ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ Average Latency │ 822.6 ms │
│ Accuracy │ 100.0% │
└─────────────────┴──────────┘

---

Jina V2 Performance Report  
┏━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Metric           ┃ Value     ┃
┡━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ Average Latency  │ 839.0 ms  │
│ 95th Percentile  │ 1173.8 ms │
│ Accuracy (Top-1) │ 100.0%    │
└──────────────────┴───────────┘

---

          Xenova vs Arabic Bureaucracy

┏━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ Model ┃ Latency ┃ Accuracy ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ ms-marco-MiniLM-L-6-v2 │ 167.9 ms │ 100.0% │
│ ms-marco-MiniLM-L-12-v2 │ 320.6 ms │ 100.0% │
└─────────────────────────┴──────────┴──────────┘

---

Phase 2: Benchmarking
Warming up engine...
MiniLM-L6 INT8 Turbo Report  
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Metric ┃ Value ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ Average Latency │ 153.0 ms │
│ Throughput │ 7 queries/sec │
│ Accuracy │ 100.0% │
└─────────────────┴───────────────┘
