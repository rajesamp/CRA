# ChangeRiskAdvisor: 6-Pager

- **Author:** Raj Sam (DevOps engineer)
- **Persona note for reviewers:** this memo uses Raj Sam as the customer persona
  in place of the persona name in requirements.md. The persona's role, daily
  workload, goals, and constraints are unchanged from the spec.
- **Status:** Drafting section by section (guide: [learning/6-pager-first-principles.md](learning/6-pager-first-principles.md))
- **Main body budget:** ~3,000 words. Supporting data goes in the appendix.
- **Task:** #2 in [Sep-Projects/ChangeRiskAdvisor/tasks.md](https://github.com/abhineer/Sep-Projects/blob/main/ChangeRiskAdvisor/tasks.md).
  Definition of done: a narrative document (no slides or bullet-only sections);
  every section from the standard format present and specific to
  ChangeRiskAdvisor, not generic; reviewed and agreed on by the whole team.

<!-- Write order: Customer, Problem, Solution, Goals and non-goals, Success
metrics, Risks and mitigations, Introduction, Appendix. Delete each prompt
comment once its section is written. Prose only; tables are for data. -->

## Introduction

<!-- ~150 words. WRITE LAST. One sentence on what CRA is, who it's for, and
what you want from the reader (e.g. agree on scope and success metrics). -->

## Problem

<!-- ~450 words. What goes wrong today, how often, and what it costs, without
mentioning CRA. Use the sample data: 10 change-related incidents Feb to Sep
2026 across 6 services (3 SEV1, 4 SEV2, 3 SEV3); checkout-service had 4.
INC-2201: config change reviewed as low-risk, 42% checkout success drop for
38 minutes, ~1,150 failed attempts, two earlier related incidents not
surfaced. -->

## Customer

<!-- ~400 words. WRITE FIRST. Raj Sam: DevOps engineer at a mid-size SaaS
company, reviews about a dozen changes a day across services they don't all
know deeply. What do they do today to judge a change? Where does it break
down? What will they never hand over (the go/no-go decision)? -->

## Solution

<!-- ~750 words. Walk through one change from Raj Sam's side of the screen
(e.g. "lower checkout-service payment timeout to 500 ms"): cited incidents,
live health and freeze status, dependents, high-risk flag from team memory,
advisory-only reminder. Then one paragraph per capability. Stack in one short
paragraph at the end. -->

## Goals & Non-Goals

<!-- ~400 words. Goals are outcomes, not activities. Non-goals: never approve,
block, merge, or deploy; no live CI/CD integration in this build; supports
the team's change review rather than replacing it. Justify each. -->

## Key Risks & Mitigations

<!-- ~450 words. For each: likelihood, impact, mitigation. Fabricated evidence,
tool failure, over-trust, stored risk settings overridden, sensitive data. -->

## Success Metrics

<!-- ~400 words. Each metric gets a target and a measurement method. Separate
input metrics (eval pass rate, citation rate, zero approvals, memory recall)
from the output hypothesis (time to an evidence-backed risk read). -->

## Appendix

<!-- No limit. Incident table, dependency graph, health and freeze status,
glossary (freeze window, blast radius, SEV levels), open questions, links to
decision records. -->

---

## Review sign-off

Agreement is recorded as an approval on the pull request that adds this file,
plus a row below for each reviewer.

| Name | Role | Decision | Date | Approval link |
|---|---|---|---|---|
| Raj Sam | Author | _pending_ | | |
| _reviewer_ | Team member or mentor | _pending_ | | |
