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
uv run adk run .               # console chat (type exit to quit)
uv run adk web --port 8000 .   # browser UI at http://127.0.0.1:8000
```

## Check it works

Type `hello` in the console chat. Until the RAG pipeline and tools are wired
in (tasks #5–#11), the agent replies with one short sentence saying it is not
yet connected to tools. Any reply from the model means setup is complete.

| If you see | It means | Fix |
|---|---|---|
| `DefaultCredentialsError: Your default credentials were not found` | Option B is active but `gcloud` isn't logged in | Run `gcloud auth application-default login`, or switch to option A |
| `400 INVALID_ARGUMENT ... API key not valid` | Option A key is wrong or missing | Paste a valid key from AI Studio into `GOOGLE_API_KEY` |

After a successful run, record it as described in
[docs/evidence/fresh-clone-run.md](docs/evidence/fresh-clone-run.md).

## Branching

`main` always runs. Each plan task gets its own short-lived branch named
`task/<n>-<slug>` (for example `task/06-synthetic-dataset`), merged into
`main` through a pull request. Claude Code sessions use `claude/*` branches.

## Layout

| Path | Purpose |
|---|---|
| `agent.py` | ADK `root_agent` (hello agent until tasks #5–#11 wire RAG and tools) |
| `CLAUDE.md` | Project rules for Claude Code sessions (naming, progress tracking) |
| `docs/team.md` | Roles and agreed stack |
| `docs/progress.md` | Weekly progress against the 34-task plan |
| `docs/pr-faq.md` | PR/FAQ (task #3). The 6-pager (task #2) arrives through its own PR. |
| `docs/evidence/` | Evidence of completion (run transcripts, screenshots) |
| `docs/adr/` | Architecture decision records and journal |
| `data/` | Synthetic dataset and golden eval cases; see [data/README.md](data/README.md) |
| `corpus/` | RAG corpus (task #7) |
| `workspace/` (not in repo) | Kanban board and ADK research notes |
