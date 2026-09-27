# Weekly Progress Tracker — ChangeRiskAdvisor

Tracks CRA against the 34-task core plan in
[abhineer/Sep-Projects · ChangeRiskAdvisor/tasks.md](https://github.com/abhineer/Sep-Projects/blob/main/ChangeRiskAdvisor/tasks.md).
Status is judged only from evidence committed to this repo (the "Evidence of
Completion" column in tasks.md). Refreshed every Sunday before the 8:00 CDT
Beyond Vectors check-in.

Status key: ✅ done · 🟡 partial · ❌ not started

## Snapshot — 2026-09-27 (start of Week 2)

| Week | Dates (check-in Sunday) | Tasks | Done | Partial | Not started |
|---|---|---|---|---|---|
| 1 — Foundations, RAG & UI | Sep 20 – Sep 26 | 11 | 1 | 1 | 9 |
| 2 — Tools, MCP & Memory | Sep 27 – Oct 3 | 7 | 0 | 0 | 7 |
| 3 — Guardrails & Caching | Oct 4 – Oct 10 | 7 | 0 | 0 | 7 |
| 4 — Observability, Evals & Demo | Oct 11 – Oct 17 | 9 | 0 | 0 | 9 |
| **Total** | | **34** | **1** | **1** | **32** |

- Last commit: 2026-09-22 (`4739d5b`). No commits in the 5 days since.
- Week 1 demo goal (Gradio UI giving a RAG-grounded risk assessment, plus
  6-pager and PR/FAQ): **not met**.
- Week 2 tasks all depend on the Week 1 pipeline (#6–#11), so Week 1 closes first.

## Week 1 — Foundations, RAG & UI

Demo goal: live Gradio chat UI returning a RAG-grounded risk assessment citing
past incidents; plus a 6-pager and a PR/FAQ.

| # | Task | Status | Evidence / gap |
|---|---|---|---|
| 1 | Kickoff: roles, requirements read, stack agreed | ✅ | `docs/team.md` has roles, stack, and read confirmation. Nit: persona is "Raj Sam"; requirements.md names **Sameer**. |
| 2 | Amazon-style 6-pager | ❌ | No `docs/6-pager.md`. |
| 3 | PR/FAQ (≥5 FAQs incl. data handling + advisory-only) | ❌ | No `docs/pr-faq.md`. |
| 4 | Repo, branch strategy, .gitignore, README | 🟡 | Repo, `.gitignore`, README exist. Only `main` branch (DoD wants feature branches); no teammate clone-and-run evidence; README spec link `../Sep-Projects/...` is broken on GitHub. |
| 5 | System prompt (advisory only, cite evidence) + 2 test transcripts | ❌ | `agent.py` still has the hello-agent instruction. |
| 6 | Synthetic dataset: incidents, dependency graph, health snapshots | ❌ | No `data/`. Seeds available: `sample_data/change_risk_sample.xlsx`, `change_management_postmortem.pdf` in Sep-Projects. |
| 7 | RAG corpus covering all 6 sample queries | ❌ | No `corpus/`. |
| 8 | Ingestion pipeline (chunk + embed into vector store) | ❌ | — |
| 9 | Retrieval test: checkout-service chunk in top 3 | ❌ | — |
| 10 | Minimal prototype: change → grounded assessment | ❌ | — |
| 11 | Gradio chat UI + shareable link | ❌ | `gradio` not in `pyproject.toml`. |

## Week 2 — Tools, MCP & Memory

Demo goal: same UI checks health/freeze-window and dependency graph, and
remembers the team's high-risk service list across two visits.

| # | Task | Status | Evidence / gap |
|---|---|---|---|
| 12 | Tool specs: `check_system_health`, `get_dependency_graph` | ❌ | No `docs/tools.md`. |
| 13 | Implement system-health tool | ❌ | — |
| 14 | Implement dependency-graph tool | ❌ | — |
| 15 | MCP exposes both tools; full round trip | ❌ | — |
| 16 | Memory schema: high-risk list + freeze-window notes | ❌ | — |
| 17 | Risk-appetite recall across 2 sessions | ❌ | — |
| 18 | Agent-trace panel in Gradio UI | ❌ | — |

## Week 3 — Guardrails & Caching

Demo goal: agent declines to approve and completes the assessment instead;
visible cache-hit speed-up on a repeated dependency-graph query.

| # | Task | Status | Evidence / gap |
|---|---|---|---|
| 19 | Guardrail rules checklist → `docs/guardrails.md` | ❌ | — |
| 20 | Guardrail checks on every assessment | ❌ | — |
| 21 | Test "just approve this" + unsupported-claim probe | ❌ | — |
| 22 | Caching for embeddings + frequent tool queries | ❌ | — |
| 23 | Measure cache hit rate + latency | ❌ | — |
| 24 | Run all 6 sample queries end-to-end; fix bugs | ❌ | — |
| 25 | Advisory + cache hit/miss badges in UI | ❌ | — |

## Week 4 — Observability, Evals & Demo Readiness

Demo goal: full walkthrough with dashboard, before/after eval score, and an
on-demand approval refusal.

| # | Task | Status | Evidence / gap |
|---|---|---|---|
| 26 | Observability: one trace ID per request | ❌ | — |
| 27 | Eval harness from expected-answers table | ❌ | — |
| 28 | Baseline eval run + report | ❌ | — |
| 29 | Error analysis table, top 3 fixes | ❌ | — |
| 30 | Apply fixes, re-run evals, show delta | ❌ | — |
| 31 | Dashboard: tool failure rate, guardrail triggers, high-risk hits | ❌ | — |
| 32 | Edge cases: timeouts, ambiguous "this change", no corpus match | ❌ | — |
| 33 | Demo script (Sameer persona, live queries, memory, scorecard) | ❌ | — |
| 34 | Final rehearsal, deployed build, backup video in README | ❌ | — |

## Catch-up plan (this week)

1. Critical path, in order: #6 dataset → #7 corpus → #8 ingestion → #9
   retrieval → #10 prototype → #11 Gradio. This alone meets the Week 1 demo.
2. In parallel: #5 system prompt (feeds #10).
3. Writing, no code dependency: #2 6-pager, #3 PR/FAQ.
4. Quick fixes: feature-branch workflow, README spec link, persona name.
5. Then Week 2 (#12–#18).

## Other findings

- `docs/adr/index.md` lists ADR-001..006 but none of the six files exist.
- `docs/adr/architecture-journal.md` last entry (2026-09-21) predates the
  repo bootstrap.

## History

| Date | Done | Partial | Not started | Note |
|---|---|---|---|---|
| 2026-09-27 | 1 | 1 | 32 | First snapshot; Week 1 demo goal not met. |
