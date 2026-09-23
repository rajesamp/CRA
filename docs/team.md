# Team & Stack — ChangeRiskAdvisor (CRA)

## Persona / Product owner
**Raj Sam (DevOps engineer)** — reviews a dozen proposed changes a day, needs
fast evidence-backed risk reads. Advisory only: the agent never approves,
blocks, merges, or deploys.

## Roles
Solo build (capstone format): all ownership below is Raj Sam's.

| Area | Owner |
|---|---|
| Prompt / system prompt | Raj Sam |
| RAG (corpus, ingestion, retrieval) | Raj Sam |
| Tools / MCP | Raj Sam |
| Memory (risk-appetite persistence) | Raj Sam |
| Guardrails / caching | Raj Sam |
| Observability / UI (Gradio) | Raj Sam |

## Stack (agreed)
| Layer | Choice |
|---|---|
| Agent framework | Google ADK (python) — `google-adk` 2.9.x |
| Model | `gemini-2.5-flash` on Gemini Enterprise Agent Platform (Vertex AI), versioned ID |
| GCP project / region | project ID in local `.env` (not committed) / `us-central1` |
| Vector store | ChromaDB (local); Vertex Knowledge Engine as later option (ADR-002) |
| Memory | ADK `DatabaseSessionService` (SQLite) + `user:` state (ADR-003) |
| Guardrails | ADK before/after model callbacks (ADR-004) |
| Tools | FastMCP stdio server consumed via `McpToolset` (ADR-005) |
| UI | Gradio `ChatInterface` on ADK `Runner` |
| Deploy | Hardened Cloud Run (distroless, cosign, SBOM) — ADR-006 |
| Python | 3.13 (managed by uv; `requires-python >=3.10,<3.14`) |
| Eval / obs | `adk eval` + Cloud Trace/Logging via `--otel_to_cloud` |

## Confirmation
- [x] Raj Sam read `Sep-Projects/ChangeRiskAdvisor/requirements.md` (all six
  sample queries, five guardrails, constraints).
