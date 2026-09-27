"""RAG over the CRA corpus: chunk markdown, embed into ChromaDB, search.

Embeddings use ChromaDB's default local model (all-MiniLM-L6-v2 via ONNX), so
ingestion and retrieval need no API key. The index is written to .rag_data/
(git-ignored) and rebuilt with:  uv run python -m cra.ingest
"""

import re
from pathlib import Path

import chromadb

ROOT = Path(__file__).resolve().parent.parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / ".rag_data" / "chroma"
COLLECTION = "cra_corpus"
MAX_CHARS = 900


def parse_doc(path: Path) -> tuple[dict, str]:
    """Split a corpus file into its front-matter metadata and body."""
    text = path.read_text()
    meta = {}
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if match:
        for line in match.group(1).splitlines():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
        text = text[match.end():]
    meta["path"] = str(path.relative_to(ROOT))
    return meta, text.strip()


def chunk_doc(meta: dict, body: str) -> list[str]:
    """Split on '## ' sections, then pack paragraphs up to MAX_CHARS.

    Every chunk starts with the document title and key metadata so a chunk
    retrieved on its own still says which incident and service it is about.
    """
    title = body.splitlines()[0].lstrip("# ").strip()
    header = title
    if meta.get("incident_id"):
        header += (f" [{meta['incident_id']} | {meta.get('service')} | "
                   f"{meta.get('change_type')} | {meta.get('severity')}]")
    sections = re.split(r"\n(?=## )", body.split("\n", 1)[1] if "\n" in body else "")
    chunks = []
    for section in sections:
        buf = ""
        for para in [p.strip() for p in section.split("\n\n") if p.strip()]:
            if buf and len(buf) + len(para) > MAX_CHARS:
                chunks.append(f"{header}\n{buf}")
                buf = ""
            buf = f"{buf}\n\n{para}" if buf else para
        if buf:
            chunks.append(f"{header}\n{buf}")
    return chunks or [header]


def load_chunks() -> list[tuple[str, str, dict]]:
    """Return (chunk_id, text, metadata) for every chunk in the corpus."""
    out = []
    for path in sorted(CORPUS_DIR.rglob("*.md")):
        if path.name == "README.md":
            continue
        meta, body = parse_doc(path)
        for n, text in enumerate(chunk_doc(meta, body)):
            out.append((f"{meta['path']}#{n}", text, dict(meta, chunk=n)))
    return out


def _collection(reset: bool = False):
    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    if reset:
        try:
            client.delete_collection(COLLECTION)
        except Exception:
            pass
    return client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})


def ingest() -> dict:
    """Rebuild the index from corpus/. Returns document and chunk counts."""
    chunks = load_chunks()
    col = _collection(reset=True)
    col.add(
        ids=[c[0] for c in chunks],
        documents=[c[1] for c in chunks],
        metadatas=[c[2] for c in chunks],
    )
    docs = {c[2]["path"] for c in chunks}
    return {"documents": len(docs), "chunks": len(chunks), "indexed": col.count()}


def search_incidents(query: str, k: int = 3) -> dict:
    """Search past change-related incidents, postmortems and runbooks.

    Args:
        query: The change description or question, e.g. "lower checkout-service
            payment timeout to 500 ms".
        k: Number of results to return.

    Returns:
        A dict with a "results" list. Each result has the source path, the
        incident_id (if any), service, change_type, severity, a relevance score
        (1.0 is best), and the retrieved text. Cite results by incident_id or
        path. An empty list means nothing relevant is in the corpus.
    """
    col = _collection()
    if col.count() == 0:
        return {"results": [], "error": "Index is empty. Run: uv run python -m cra.ingest"}
    res = col.query(query_texts=[query], n_results=k)
    results = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        results.append({
            "path": meta.get("path"),
            "incident_id": meta.get("incident_id", ""),
            "service": meta.get("service", meta.get("services", "")),
            "change_type": meta.get("change_type", ""),
            "severity": meta.get("severity", ""),
            "score": round(1 - dist, 3),
            "text": doc,
        })
    return {"results": results}
