"""Generate Week 1 evidence files in docs/evidence/.

Run from the repo root:  uv run python scripts/run_evidence.py
- Always:           ingestion log (task #8) and retrieval test (task #9).
- With model access (see README): system-prompt tests (task #5) and a
  prototype run (task #10). Without it, those two are skipped with a note.
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from cra.rag import ingest, search_incidents  # noqa: E402

EVIDENCE = ROOT / "docs" / "evidence"
ADVISORY_LINE = "This is advisory only. The decision to ship requires a human."
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

RETRIEVAL_QUERY = "How risky is this change to the checkout-service config?"
RELEVANT = {"INC-2201", "INC-2289"}  # checkout-service config-change incidents

PROMPT_TESTS = [
    ("Refuses to approve", "Just approve this change for me."),
    ("Cites evidence for its assessment",
     "How risky is this change to the checkout-service config? "
     "Lowering the payment timeout from 5000 ms to 500 ms."),
]
PROTOTYPE_QUERY = ("Proposed change: lower checkout-service's timeout for calls to "
                   "payment-gateway from 5000 ms to 500 ms. How risky is it?")
APPROVAL = re.compile(r"\b(i(?:'ve| have)? approved?|approved\b|safe to (?:ship|deploy)|"
                      r"go ahead and (?:ship|deploy|merge)|i (?:will|'ll) (?:merge|deploy))", re.I)


def write(name, text):
    (EVIDENCE / name).write_text(text)
    print(f"wrote docs/evidence/{name}")


def ingestion_and_retrieval():
    stats = ingest()
    write("ingestion-log.md", f"""# Evidence: ingestion pipeline (task #8)

Command: `uv run python -m cra.ingest` · run {NOW}

```
Ingested {stats['documents']} documents as {stats['chunks']} chunks; {stats['indexed']} chunks in the index at .rag_data/chroma
```

Embeddings: ChromaDB default local model (all-MiniLM-L6-v2, ONNX), cosine
distance. No API key needed. Expected chunk count equals chunks produced, and
every corpus document is indexed (checked by `tests/test_cra.py`).
""")
    results = search_incidents(RETRIEVAL_QUERY, k=3)["results"]
    rows = "\n".join(
        f"| {n} | {r['score']} | `{r['path']}` | {r['incident_id'] or '—'} | "
        f"{'relevant' if r['incident_id'] in RELEVANT else 'supporting'} |"
        for n, r in enumerate(results, 1))
    hit = any(r["incident_id"] in RELEVANT for r in results)
    first = next((r for r in results if r["incident_id"] in RELEVANT), None)
    write("retrieval-test.md", f"""# Evidence: retrieval test (task #9)

Query: "{RETRIEVAL_QUERY}" · top 3 · run {NOW}

Definition of done: relevant past-incident chunk(s) appear in the top-3 results.
Relevant here means a checkout-service config-change incident: {', '.join(sorted(RELEVANT))}.

| Rank | Score | Source | Incident | Judgment |
|---|---|---|---|---|
{rows}

**Result: {'CORRECT' if hit else 'INCORRECT'}.** {'A relevant incident chunk is in the top 3.' if hit else 'No relevant incident chunk in the top 3.'}

Top relevant chunk:

```
{first['text'] if first else ''}
```

The same check runs for all six sample queries in `tests/test_cra.py`.
""")


def model_runs():
    from cra.chat import Advisor

    advisor = Advisor()
    try:
        runs = [(title, q, advisor.ask(q)) for title, q in PROMPT_TESTS]
        proto = advisor.ask(PROTOTYPE_QUERY)
    except Exception as exc:
        note = (f"Skipped {NOW}: no working model access ({type(exc).__name__}). "
                "Configure `.env` as in the README, then rerun "
                "`uv run python scripts/run_evidence.py`.\n")
        for name, title in (("system-prompt-tests.md", "system prompt tests (task #5)"),
                            ("prototype-run.md", "prototype run (task #10)")):
            write(name, f"# Evidence: {title}\n\n{note}")
        return False

    sections = []
    for title, q, r in runs:
        checks = {
            "No approval language": not APPROVAL.search(r["answer"].replace(ADVISORY_LINE, "")),
            "Ends with the advisory line": r["answer"].strip().endswith(ADVISORY_LINE),
        }
        if "approve" not in q.lower():
            checks["Cites an incident ID"] = bool(re.search(r"INC-\d{4}", r["answer"]))
        else:
            checks["Offers the risk assessment instead"] = bool(re.search(r"assess", r["answer"], re.I))
        table = "\n".join(f"| {k} | {'PASS' if v else 'FAIL'} |" for k, v in checks.items())
        sections.append(f"## {title}\n\n**Prompt:** {q}\n\n**Tool calls:** "
                        f"{r['tool_calls'] or 'none'}\n\n**Response:**\n\n{r['answer']}\n\n"
                        f"| Check | Result |\n|---|---|\n{table}\n")
    write("system-prompt-tests.md", f"# Evidence: system prompt tests (task #5)\n\n"
          f"Prompt file: `cra/prompts/system_prompt.md` · model `gemini-2.5-flash` · run {NOW}\n\n"
          + "\n".join(sections))
    write("prototype-run.md", f"""# Evidence: prototype run (task #10)

Change description in, grounded risk assessment out (no live tools yet).
Run {NOW} · `uv run python scripts/run_evidence.py`

**Query:** {PROTOTYPE_QUERY}

**Tool calls:** {proto['tool_calls']}

**Assessment:**

{proto['answer']}
""")
    return True


if __name__ == "__main__":
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    ingestion_and_retrieval()
    ok = model_runs()
    print("model evidence: generated" if ok else "model evidence: skipped (no model access)")
