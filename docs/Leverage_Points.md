# Leverage Points

---

## fine tune an embedding model for better performance on a specific task or dataset.

> For this project, I'm testing several approaches. On the API side, I'm comparing Isaacus, OpenAI, Voyage AI (with opt-out enabled), and Google Gemini — all using their best models at maximum embedding dimensions. I picked these because they either have reasonable terms or, in Voyage's case, at least let you opt out of training (but you must do this from the get-go, the opt-out won't retroactively apply to any data you've already submitted). I'll also show you performance results from a small and fast local model I fine-tuned myself: a sentence-transformers model based on BAAI/bge-small-en, trained specifically on High Court of Australia case law from the Open Australian Legal Corpus... which happens to be the exact dataset I'm searching through here.

---

## 1 Vector ONNX Runtime (Quantized Model) 2-3x faster
