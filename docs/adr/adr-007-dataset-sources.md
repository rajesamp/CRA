# ADR-007: Dataset sources for ChangeRiskAdvisor

- **Status:** Proposed
- **Date:** 2026-09-27
- **Decision-makers:** Raj Sam (DevOps engineer)

## Context

Tasks #6 and #7 need a dataset (incidents, dependency graph, health snapshots)
and a RAG corpus (postmortems, runbooks, incident summaries). requirements.md
asks for "a static or lightly simulated dataset". The golden eval
(`data/golden_eval.json`) depends on exact facts: checkout-service is Healthy
with no freeze, the freeze set is auth-service and mobile-frontend, and the
payment-gateway dependency chain is fixed. Open-source and crawled datasets
were considered as a way to add realism.

## Decision

- **Keep the core dataset synthetic.** `incidents.json`, `dependencies.json`
  and `health.json` stay synthetic and are extended by hand, so every service
  has at least two incidents (task #6 asks for "multiple past incidents each").
- **Enrich only the RAG corpus with real public postmortems.** Add 5–10 real
  outages caused by changes (config changes, dependency upgrades, feature
  flags, infra changes), summarised in our own words with a link to the source.
- **Keep real and synthetic data separate.** Real-world summaries are tagged
  `source: public_postmortem` and never get `INC-xxxx` IDs. The agent must
  never present another company's outage as the team's own history.
- **Don't use web crawls or model-training datasets.**

## Alternatives considered

The candidate sources below were listed from memory and have not been checked.
Confirm names, availability and licences before relying on any of them.

| Option | Pros | Cons |
|---|---|---|
| Web crawls (Common Crawl and similar) | Huge volume | Noisy, unclear licences, no ground truth; the eval can't be checked against it |
| Ops log and trace datasets (Loghub, cluster traces) | Real telemetry | CRA reasons over change descriptions, not logs; out of scope |
| Microservice fault benchmarks (TrainTicket, DeathStarBench) | Realistic dependency graphs and faults | Would replace the course's service graph and break the golden eval facts |
| Public postmortem collections (danluu/post-mortems, cloud-provider incident reports) | Real change-caused failures; better retrieval realism | Copyright on blog posts, so summarise and link rather than copy |
| Synthetic core plus summarised public postmortems (chosen) | Eval facts stay stable; the corpus gains realism; licences stay clean | Manual curation, about 1–2 hours |

## Consequences

- Positive: the golden eval stays deterministic, the corpus shows retrieval
  across varied real failure patterns, and the data-handling FAQ (#7) remains
  true: no production data or customer data.
- Negative / accepted trade-offs: the real postmortems are summaries rather
  than full text, and dataset growth is manual.
- Reversible? Yes. Public entries are tagged and can be removed without
  touching the core data.

## Follow-ups

- Task #6: add incidents so every service has at least two.
- Task #7: shortlist public postmortems, check each licence, then write
  summaries with source links.
- Once public postmortems are in the corpus, update the data-handling FAQ (#7)
  and `data/README.md` to mention the `public_postmortem` source.

## Links

- requirements.md §4 Constraints: [Sep-Projects/ChangeRiskAdvisor/requirements.md](https://github.com/abhineer/Sep-Projects/blob/main/ChangeRiskAdvisor/requirements.md)
- Dataset provenance: [data/README.md](../../data/README.md)
- Golden eval: [data/golden_eval.json](../../data/golden_eval.json)
