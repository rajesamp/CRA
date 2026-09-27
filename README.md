# CRA — ChangeRiskAdvisor

Pre-deployment change-risk assessment agent. RAG over past change-related
postmortems, live system-health/freeze-window and dependency-graph tools,
persistent team risk-appetite memory. **Advisory only** — it never approves,
blocks, merges, or deploys.

- Stack: Google ADK (python) 2.9.x, `gemini-2.5-flash`, Gradio UI
- Spec: [Sep-Projects/ChangeRiskAdvisor/requirements.md](https://github.com/abhineer/Sep-Projects/blob/main/ChangeRiskAdvisor/requirements.md)
  · plan: [tasks.md](https://github.com/abhineer/Sep-Projects/blob/main/ChangeRiskAdvisor/tasks.md)
  · progress: [docs/progress.md](docs/progress.md)
- Decisions: [docs/adr/](docs/adr/) · running notes: [docs/adr/architecture-journal.md](docs/adr/architecture-journal.md)

## Prerequisites

- `git`
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/). It installs
  Python 3.13 for you (pinned in `.python-version`).
- Model access, **one** of:
  - **Gemini API key** (easiest; no GCP access needed): create one at
    https://aistudio.google.com/apikey
  - **Vertex AI** in a GCP project you can use, with the
    [`gcloud` CLI](https://cloud.google.com/sdk/docs/install) installed

## Setup (fresh clone)

```sh
git clone https://github.com/rajesamp/CRA.git
cd CRA
uv sync
cp .env.example .env
```

Then edit `.env` and keep **one** option active:

| Option | Set in `.env` | Extra step |
|---|---|---|
| A. Gemini API key | `GOOGLE_GENAI_USE_ENTERPRISE=False` and `GOOGLE_API_KEY=<your key>` | none |
| B. Vertex AI | `GOOGLE_GENAI_USE_ENTERPRISE=True`, `GOOGLE_CLOUD_PROJECT=<project id>`, `GOOGLE_CLOUD_LOCATION=us-central1` | `gcloud auth application-default login` |

`.env` is git-ignored. Never commit it.

## Run

```sh
uv run python -m cra.ingest    # build the RAG index (first run downloads a ~80 MB local embedding model)
uv run python app.py           # Gradio chat UI at http://127.0.0.1:7860 (CRA_SHARE=1 for a share link)
uv run adk run .               # console chat (type exit to quit)
uv run adk web --port 8000 .   # ADK dev UI at http://127.0.0.1:8000
```

## Check it works

1. Without any key: `uv run pytest -q` should report all tests passing. This
   checks the dataset, the corpus retrieval for all six sample queries, and the
   agent loop with a scripted stand-in model.
2. With model access: in the console chat or the Gradio UI, ask
   `How risky is lowering checkout-service's payment timeout from 5000 ms to 500 ms?`
   The answer should give a risk rating, cite INC-2201, list what it could not
   confirm, and end with "This is advisory only. The decision to ship requires
   a human."

| If you see | It means | Fix |
|---|---|---|
| `DefaultCredentialsError: Your default credentials were not found` | Option B is active but `gcloud` isn't logged in | Run `gcloud auth application-default login`, or switch to option A |
| `400 INVALID_ARGUMENT ... API key not valid` | Option A key is wrong or missing | Paste a valid key from AI Studio into `GOOGLE_API_KEY` |
| `No API key was provided` in the Gradio chat | `.env` is missing or has no key | Create `.env` from `.env.example` and set one option |
| `Index is empty` in a tool result | The RAG index hasn't been built | Run `uv run python -m cra.ingest` |

To regenerate the Week 1 evidence files in `docs/evidence/`, run
`uv run python scripts/run_evidence.py`. With model access it also records the
system-prompt tests and a prototype run.

After a successful run, record it as described in
[docs/evidence/fresh-clone-run.md](docs/evidence/fresh-clone-run.md).

## Branching

`main` always runs. Each plan task gets its own short-lived branch named
`task/<n>-<slug>` (for example `task/06-synthetic-dataset`), merged into
`main` through a pull request. Claude Code sessions use `claude/*` branches.

## Layout

| Path | Purpose |
|---|---|
| `agent.py` | ADK `root_agent`: system prompt plus the `search_incidents` retrieval tool |
| `app.py` | Gradio chat UI |
| `cra/` | Library code: `rag.py` (chunk, embed, search), `ingest.py`, `chat.py`, `prompts/system_prompt.md` |
| `scripts/` | `build_incident_summaries.py`, `run_evidence.py` |
| `tests/` | Dataset, retrieval, and agent-loop tests (`uv run pytest -q`) |
| `CLAUDE.md` | Project rules for Claude Code sessions (naming, progress tracking) |
| `docs/team.md` | Roles and agreed stack |
| `docs/progress.md` | Weekly progress against the 34-task plan |
| `docs/pr-faq.md` | PR/FAQ (task #3). The 6-pager (task #2) arrives through its own PR. |
| `docs/evidence/` | Evidence of completion (run transcripts, screenshots) |
| `docs/adr/` | Architecture decision records and journal |
| `data/` | Synthetic dataset and golden eval cases; see [data/README.md](data/README.md) |
| `corpus/` | RAG corpus: postmortems, incident summaries, runbooks; see [corpus/README.md](corpus/README.md) |
| `workspace/` (not in repo) | Kanban board and ADK research notes |
