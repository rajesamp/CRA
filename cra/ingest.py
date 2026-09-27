"""Rebuild the RAG index from corpus/.  Usage: uv run python -m cra.ingest"""

from cra.rag import INDEX_DIR, ROOT, ingest


def main():
    stats = ingest()
    print(f"Ingested {stats['documents']} documents as {stats['chunks']} chunks; "
          f"{stats['indexed']} chunks in the index at {INDEX_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
