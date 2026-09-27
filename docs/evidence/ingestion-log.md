# Evidence: ingestion pipeline (task #8)

Command: `uv run python -m cra.ingest` · run 2026-09-27 06:40 UTC

```
Ingested 40 documents as 72 chunks; 72 chunks in the index at .rag_data/chroma
```

Embeddings: ChromaDB default local model (all-MiniLM-L6-v2, ONNX), cosine
distance. No API key needed. Expected chunk count equals chunks produced, and
every corpus document is indexed (checked by `tests/test_cra.py`).
