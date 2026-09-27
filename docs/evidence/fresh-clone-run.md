# Evidence: fresh clone runs from the README alone (task #4)

Definition of done (tasks.md #4): repo exists remotely with main + feature
branches; README lets a fresh clone run the project. Evidence: a teammate
clones the repo and runs it successfully from the README alone.

## 1. Clean-room run (Claude Code, 2026-09-27)

A new clone into an empty folder, following [README.md](../../README.md)
exactly, on commit `0c6eaf8` (branch `claude/wizardly-keller-xabzlr`).
No real API key or GCP login was available, so a placeholder key was used.
That proves every step up to the model call; the teammate run in part 2
completes the last step with a real key.

| Step | Command | Result |
|---|---|---|
| Clone | `git clone https://github.com/rajesamp/CRA.git && cd CRA` | ✅ |
| Install | `uv sync` | ✅ Python 3.13.12 venv, 48 packages |
| Configure | `cp .env.example .env`, option A | ✅ (placeholder key) |
| CLI | `uv run adk --version` | ✅ `adk, version 2.9.2` |
| Console chat | `uv run adk run .`, type `hello` | ✅ Request reached the Gemini API, which rejected the placeholder key (`400 INVALID_ARGUMENT: API key not valid`), as expected |
| Web UI | `uv run adk web --port 8000 .` | ✅ Server started; `GET /dev-ui/` returned HTTP 200 |

### README gaps found and fixed before this run

| Gap in the previous README | Fix (commit `0c6eaf8`) |
|---|---|
| Only Vertex AI was documented, so anyone without access to the owner's GCP project hit `DefaultCredentialsError` on the first message | Added option A, a Gemini API key, which needs no GCP access |
| Said uv installs Python 3.13, but uv used the machine's Python 3.11 | Pinned `3.13` in `.python-version` |
| Spec link was a relative path that 404s on GitHub | Absolute link to Sep-Projects |
| No way to tell whether setup worked | Added "Check it works" with expected output and fixes for both setup errors |

## 2. Teammate run (pending, after PR #1 merges)

Run this only after [rajesamp/CRA#1](https://github.com/rajesamp/CRA/pull/1)
has merged, so the clone of `main` has the updated README. The teammate
follows the README from a new clone with their own API key (or Vertex AI
access), types `hello`, and gets a one-sentence reply from the model. They
then add a row below in a follow-up commit and comment on PR #1 with a
screenshot or pasted output (comments still work after merge).

| Name | Date | OS | Option (A or B) | Result | PR comment link |
|---|---|---|---|---|---|
| _teammate_ | | | | _pending_ | |
