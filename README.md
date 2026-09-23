# CRA — ChangeRiskAdvisor

Pre-deployment change-risk assessment agent. RAG over past change-related
postmortems, live system-health/freeze-window and dependency-graph tools,
persistent team risk-appetite memory. **Advisory only** — it never approves,
blocks, merges, or deploys.

- Stack: Google ADK (python) 2.9.x, `gemini-2.5-flash` on Vertex AI
  (project `REDACTED`, region `us-central1`), Gradio UI
- Spec: [Sep-Projects/ChangeRiskAdvisor](../Sep-Projects/ChangeRiskAdvisor/requirements.md)
- Decisions: [docs/adr/](docs/adr/) · running notes: [docs/adr/architecture-journal.md](docs/adr/architecture-journal.md)

## Prerequisites

- `uv` (installs Python 3.13 automatically)
- `gcloud` authed to project `REDACTED`: `gcloud auth application-default login`

## Setup (fresh clone)

```sh
git clone https://github.com/rajesamp/CRA.git
cd CRA
uv sync
cp .env.example .env   # GOOGLE_CLOUD_PROJECT=REDACTED, region us-central1
```

## Run

```sh
uv run adk web --port 8000 .   # browser UI at http://127.0.0.1:8000
uv run adk run .               # console REPL (type exit to quit)
```

## Layout

| Path | Purpose |
|---|---|
| `agent.py` | ADK `root_agent` (hello agent until ST-1.5 wires RAG + tools) |
| `docs/team.md` | roles + agreed stack |
| `docs/adr/` | architecture decision records + journal |
| `data/`, `corpus/` | synthetic dataset + RAG corpus (Week 1) |
| `workspace/` (not in repo) | kanban board + ADK research notes |
