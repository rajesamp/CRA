# ChangeRiskAdvisor: 6-Pager

- **Author:** Raj Sam (DevOps engineer)
- **Persona note for reviewers:** this memo uses Raj Sam as the customer persona
  in place of the persona name in requirements.md. The persona's role, daily
  workload, goals, and constraints are unchanged from the spec.
- **Status:** Draft 1, to be rewritten by the author before team review
  (guide: [learning/6-pager-first-principles.md](learning/6-pager-first-principles.md))
- **Task:** #2 in [Sep-Projects/ChangeRiskAdvisor/tasks.md](https://github.com/abhineer/Sep-Projects/blob/main/ChangeRiskAdvisor/tasks.md).
  Definition of done: a narrative document (no slides or bullet-only sections);
  every section from the standard format present and specific to
  ChangeRiskAdvisor, not generic; reviewed and agreed on by the whole team.

## Introduction

ChangeRiskAdvisor (CRA) is an assistant that gives the engineer reviewing a
production change an evidence-backed risk read before they decide whether it
ships. It brings together the four things a careful reviewer checks by hand:
similar past incidents, the service's current health, whether a freeze window
is active, and which services depend on the one being changed. It also applies
the risk settings the team has agreed on. CRA advises and never decides. This
memo describes the problem CRA addresses, the engineer it serves, how it works,
what it will and will not do, the risks we see, and how we will measure
success over the four-week build. We are asking reviewers to agree on the scope
and non-goals in this memo, and on the success metrics we will be held to at
the demo in mid-October.

## Problem

On 14 February 2026, a change to checkout-service lowered the timeout on its
calls to payment-gateway from 5,000 ms to 500 ms. Reviewers rated it a
low-risk config tweak, so it skipped load testing at production traffic. It
deployed at 14:02 UTC. At 14:10 a promotional email tripled traffic, and the
shorter timeout turned slow payment responses into failures. Checkout success
dropped 42% for 38 minutes. About 1,150 checkout attempts failed or stalled
before the change was rolled back at 14:40. That incident is INC-2201, a SEV1.

The warning signs were already on record. payment-gateway had failed twice in
the six months before: INC-1987, a config change in September 2025 (SEV2), and
INC-2055, a dependency upgrade in November 2025 (SEV1). Neither came up in the
review. Nobody reviewing the change had them in front of them, and nothing put
them there. The postmortem's action items say it plainly: checkout-service and
payment-gateway should have been flagged as high-risk.

The history kept repeating after the postmortem. payment-gateway had two more
change-related incidents: INC-2214, a client library mismatch after a
dependency upgrade in March 2026 (SEV2), and INC-2318, a rate limit lowered
below peak traffic in August 2026 (SEV1). That is five incidents on one
dependency path in twelve months, and each review started without the ones
before it.

The pattern holds beyond one service. Of the twelve change-related incidents
on record, four came from config changes, and all four were SEV1 or SEV2. Two
were SEV1. A config change can look like a one-value edit, which is exactly why
it gets waved through without anyone checking what happened the last time.

The cost is not only the outages. On a release-day spike, a reviewer has two
bad options. They can stop and dig through the incident tracker for every
change, reading postmortems and matching root causes, and slow the whole
release down. Or they can ship on memory and hope nothing like this has broken
before. Most spike days, memory wins, because the release has to go out. Either
way something loses: speed, or safety.

The history that would stop a risky change exists. It just isn't in front of
the reviewer when they decide.

## Customer

Our customer is Raj Sam, a DevOps engineer at a mid-size SaaS company. Raj Sam
reviews proposed production changes across eight services, from
checkout-service and payment-gateway to the web and mobile frontends: config
updates, dependency upgrades, feature-flag rollouts, infra changes, and schema
migrations. Some days bring a handful of changes. Release days bring a spike,
and that is when the risky ones get through. Raj Sam knows some of these
services deeply and others only by name.

For every change, Raj Sam has to answer one question: will this hurt us, and
should it ship now? Their first stop is the dashboards. Is the service healthy?
Is anything already degraded or alerting? That check is quick, and it catches
problems that exist today. It says nothing about what went wrong the last time
someone made a change like this one.

That second check, past incident history, is the one that gets skipped. Finding
the right postmortems means searching the incident tracker, reading root causes,
and matching them to the change in front of you. On a spike day there is no time
for that, so Raj Sam falls back on memory. Memory only covers the incidents
Raj Sam was around for. Nobody is on call for every incident on every service.
INC-2201 is what that gap looks like: the history that would have flagged the
change existed, and nobody reviewing it had it in front of them.

Raj Sam also carries context no tool has. The biggest is peak events: a sale, a
launch, or a marketing push that is about to multiply traffic. INC-2201 turned
from a quiet config change into a SEV1 because a promotional email tripled
traffic eight minutes after deploy. Raj Sam knows when those pushes are coming.
A tool doesn't.

What Raj Sam wants is simple. Paste in a change and get a fast risk read that
cites similar past incidents and the current state of the system. Get flagged
when a change touches a service the team has marked high-risk or lands in a
freeze window. Let safe changes move faster because the evidence shows why
they're safe, and give risky ones the second look they need.

What Raj Sam will not give up is the decision. The tool advises; Raj Sam and
the team make the go/no-go call. Their reason is rubber-stamping: the moment a
bot can approve a change, people stop reading the change. An advisor keeps the
reviewer reading. It puts the evidence in front of them and leaves the call
with the person who knows about Friday's peak event.

## Solution

CRA meets Raj Sam at the point of decision. Here is what one review looks like.
Raj Sam receives a change that lowers checkout-service's payment timeout to
500 ms, and types into CRA: "How risky is this change to the checkout-service
config?"

CRA answers in one response. It reports that this change closely matches
INC-2201, where the same kind of timeout reduction on checkout-service caused a
SEV1 outage under promotional traffic, and INC-2289, where a retry timeout set
too low failed under load in July. It checks checkout-service's live status
and reports that the service is healthy and no freeze window is active. It
looks up the dependency graph and notes that checkout-service calls
payment-gateway, which is currently degraded, and that order-service,
web-frontend, and mobile-frontend all sit downstream and would feel an outage.
It reminds Raj Sam that the team has flagged checkout-service as always
high-risk. It closes by recommending a load test at three times baseline
traffic before release, citing the INC-2201 postmortem, and by stating that the
decision to ship requires a human. Every claim in the response points to its
source, and a trace panel under the answer shows which checks CRA ran and which
incidents it retrieved.

Four capabilities make this possible.

**Retrieval over past incidents.** CRA searches a corpus of change-related
postmortems, runbooks, and incident summaries for the incidents most similar to
the proposed change, by service and by type of change. It cites them by ID and
root cause. If nothing similar exists, it says so rather than stretching an
unrelated incident to fit.

**Live checks.** Two tools report the current state of the system. The
system-health tool returns a service's status, any active incidents, and
whether a freeze window is in force. The dependency-graph tool returns the
services a given service depends on and the services that depend on it. CRA
never infers health, freeze status, or dependencies from service names; it
states only what a tool returned during that request, and if a tool fails it
labels that part of the answer unconfirmed.

**Team memory.** Raj Sam can tell CRA once that "checkout-service is always
high-risk for our team," and CRA applies that setting in every later session
without being reminded. Stored settings stay in place until the team changes
them. CRA never downgrades them on its own judgement, even when the evidence
for a particular change looks mild.

**Guardrails.** A check runs on every response before Raj Sam sees it. It
confirms that the response contains no approval, block, merge, or deploy
decision, that every risk claim carries a citation, and that every statement
about health, freeze windows, or dependencies matches a tool result. A
response that fails is corrected or marked unconfirmed, and the event is
logged. If Raj Sam asks CRA to "just approve this change," it declines,
explains that approval is a human step, and offers to finish the risk
assessment instead.

CRA is built with Google's Agent Development Kit on `gemini-2.5-flash`, with a
ChromaDB vector store for the incident corpus, an MCP server for the two live
tools, a SQLite session store for team memory, and a Gradio chat interface. The
reasoning behind each choice is recorded in [docs/adr/](adr/index.md).

## Goals & Non-Goals

Our goals are stated as outcomes we can check at the demo. First, every risk
assessment CRA produces cites at least one retrieved incident or live tool
result for each claim it makes; an assessment without evidence is flagged as
unconfirmed, never guessed. Second, CRA answers all six sample queries in
requirements.md with the expected behaviour, including correct freeze-window
status and the correct dependency list for payment-gateway. Third, a high-risk
setting stated in one session is applied, unprompted, in the next. Fourth, CRA
refuses every request to approve a change, direct or indirect, and offers the
assessment instead. Fifth, when a tool fails, CRA degrades gracefully and says
what it could not confirm.

Our non-goals matter as much. CRA will never approve, block, merge, or deploy a
change. That is the product's defining rule, not a limitation we plan to lift:
the approval step stays an explicit human action in the demo and in any future
version, because the people who ship a change are accountable for it and hold
context CRA does not.

CRA will not integrate with live CI/CD pipelines, source control, or production
monitoring in this build. requirements.md asks for a static or lightly
simulated dataset, and a fixed dataset lets us test CRA's answers against known
facts. Connecting real systems is a later decision that would bring access
control and data-handling questions this build does not need to answer.

CRA will not replace the team's change review. It prepares the reviewer; it
does not remove them. We also will not use real incident records or customer
data. The core dataset is synthetic, and any real public postmortems added to
the corpus are summarised, linked to their source, and never presented as the
team's own history (see ADR-007).

## Key Risks & Mitigations

The most serious risk is fabricated evidence: CRA citing an incident that does
not exist, or stating a freeze status or dependency it did not check. It is
likely without controls, because language models fill gaps fluently, and the
impact is high, because a reviewer who trusts a false "no freeze" could ship
into a freeze window. We mitigate it in three layers: the system prompt
requires a source for every claim, the guardrail check compares every health,
freeze, and dependency statement against the tool results from the same
request, and the golden eval tests it with a request that has no evidence
behind it.

The second risk is over-trust. Even an accurate advisor can train reviewers to
stop thinking and accept its recommendation, and the risk grows as the tool
proves useful. We mitigate it by design rather than by policy: every answer
states that a human decision is required, CRA never produces an approve or
reject verdict, and the evidence is always shown alongside the recommendation
so the reviewer can disagree with it.

The third risk is silent tool failure. If the health or dependency check times
out and CRA answers anyway, the assessment rests on nothing. This will happen at
some point, and the impact is high. CRA labels any unanswered check as
unconfirmed, for example "I couldn't confirm the freeze calendar right now;
treat freeze status as unconfirmed," and every failure is logged and counted on
the observability dashboard so we can see how often it happens.

The fourth risk is that stored team settings are overridden. If CRA decided on
its own that checkout-service no longer looked high-risk, it would erase a
decision the team made after INC-2201. The likelihood is moderate and the
impact is high, because the flag exists precisely for the changes that look
safe. CRA treats stored settings as fixed until the team changes them, and when
the evidence and a setting disagree it reports both and leaves the choice to
the team.

The fifth risk is data exposure. Real postmortems can contain names, customer
details, and credentials. This build avoids the risk by using synthetic data
and summarised public postmortems only. Before any real rollout, postmortems
would need redaction before indexing and access controls matching the incident
tracker.

## Success Metrics

We separate the measures this build controls from the outcome it is meant to
change. The controllable measures are scored against the golden eval in
`data/golden_eval.json`, which encodes the expected behaviour for each of the
six sample queries in requirements.md.

The first measure is the eval pass rate: all six sample queries pass, scored
automatically, with a baseline recorded before our Week 4 error analysis and a
second score recorded after the fixes. The second is citation coverage: 100%
of risk assessments cite at least one retrieved incident or live tool result,
measured across every eval run. The third is refusal accuracy: zero approval,
block, merge, or deploy statements across the direct approval request and the
indirect red-team phrasings we test in Week 3. The fourth is memory recall: in
100% of two-session tests, a high-risk flag stated in session one is applied
unprompted in session two. The fifth is graceful degradation: every simulated
tool failure produces an "unconfirmed" label rather than a guess, and the
observability dashboard reports the tool-failure rate.

The outcome we want is faster, better-informed reviews for Raj Sam. Our
hypothesis is that the time to reach an evidence-backed risk read on a change
drops from several manual lookups across four sources to a single question. We
will test it with timed runs on the sample changes, comparing a manual check of
the four sources with a CRA query for the same change, and report the result at
the demo. We will treat the hypothesis as unproven until those numbers exist.

As a stretch goal we will also report speed and cost per query, against a
target of under three seconds and under one cent per assessment.

## Appendix

### A. Incident record (`data/incidents.json`)

| ID | Service | Date | Change type | Severity | Root cause |
|---|---|---|---|---|---|
| INC-1987 | payment-gateway | 2025-09-02 | Config change | SEV2 | Card-processor connect timeout lowered below peak p99 latency (synthetic) |
| INC-2055 | payment-gateway | 2025-11-19 | Dependency upgrade | SEV1 | Client upgrade shrank the default connection pool (synthetic) |
| INC-2201 | checkout-service | 2026-02-14 | Config change | SEV1 | Payment timeout misconfigured during release |
| INC-2214 | payment-gateway | 2026-03-03 | Dependency upgrade | SEV2 | Client library version mismatch |
| INC-2233 | checkout-service | 2026-04-22 | Feature flag rollout | SEV2 | Flag enabled for 100% before canary completed |
| INC-2255 | auth-service | 2026-05-10 | Infra change | SEV1 | Connection pool size reduced too aggressively |
| INC-2270 | inventory-service | 2026-06-01 | Schema migration | SEV3 | Backward-incompatible column drop |
| INC-2289 | checkout-service | 2026-07-18 | Config change | SEV2 | Retry timeout set too low under load |
| INC-2301 | notification-service | 2026-07-29 | Dependency upgrade | SEV3 | Deprecated API usage broke on upgrade |
| INC-2318 | payment-gateway | 2026-08-15 | Config change | SEV1 | Rate limit lowered below peak traffic needs |
| INC-2325 | checkout-service | 2026-08-30 | Infra change | SEV2 | Autoscaling threshold changed pre-peak |
| INC-2340 | auth-service | 2026-09-10 | Feature flag rollout | SEV3 | Session token flag mismatch across regions |

INC-1987 and INC-2055 come from the related-incident table in the INC-2201
postmortem; their root causes were written as synthetic data. Provenance for
every record is in `data/README.md`.

### B. Service dependencies and current state

| Service | Depends on | Depended on by | Status | Freeze window |
|---|---|---|---|---|
| checkout-service | payment-gateway, inventory-service, auth-service | order-service | Healthy | No |
| payment-gateway | notification-service | checkout-service | Degraded | No |
| auth-service | — | checkout-service, web-frontend, mobile-frontend | Healthy | Yes |
| inventory-service | — | checkout-service, order-service | Healthy | No |
| order-service | checkout-service, inventory-service | web-frontend, mobile-frontend | Healthy | No |
| notification-service | — | payment-gateway | Healthy | No |
| web-frontend | order-service, auth-service | — | Healthy | No |
| mobile-frontend | order-service, auth-service | — | Healthy | Yes |

### C. Glossary

- **Freeze window:** a period when non-emergency changes to a service are not
  supposed to ship, for example before a peak sales event.
- **Blast radius:** the set of services that would be affected if a change to
  one service failed, found by following the dependency graph downstream.
- **SEV1 / SEV2 / SEV3:** incident severity, from SEV1 (major customer-facing
  outage) to SEV3 (limited impact).
- **Golden eval:** the fixed set of test queries and expected answers used to
  score CRA automatically.

### D. Open questions

1. Should CRA's recommendation include a suggested mitigation (such as "load
   test at 3x baseline"), or only the risk read and evidence?
2. How should the team change a stored high-risk setting: by telling CRA in
   chat, or through a separate reviewed step?
3. Which public postmortems, if any, should join the corpus under ADR-007?

### E. Related documents

- PR/FAQ: `docs/pr-faq.md`
- Requirements: [Sep-Projects/ChangeRiskAdvisor/requirements.md](https://github.com/abhineer/Sep-Projects/blob/main/ChangeRiskAdvisor/requirements.md)
- Golden eval: `data/golden_eval.json`
- Decision records: `docs/adr/`

---

## Review sign-off

Agreement is recorded as an approval on the pull request that adds this file,
plus a row below for each reviewer.

| Name | Role | Decision | Date | Approval link |
|---|---|---|---|---|
| Raj Sam | Author | _pending_ | | |
| _reviewer_ | Team member or mentor | _pending_ | | |
