# ChangeRiskAdvisor: PR/FAQ

- **Author:** Raj Sam (DevOps engineer)
- **Status:** Draft for team review
- **Persona note for reviewers:** this document uses Raj Sam as the customer
  persona in place of the persona name in requirements.md. The persona's role,
  daily workload, goals, and constraints are unchanged from the spec.
- **Task:** #3 in [Sep-Projects/ChangeRiskAdvisor/tasks.md](https://github.com/abhineer/Sep-Projects/blob/main/ChangeRiskAdvisor/tasks.md).
  Definition of done: press release written from the customer's (Raj Sam's)
  point of view; FAQ has at least 5 questions, including data handling and the
  "advisory only, never auto-approves" guardrail; reviewed and agreed on by the
  whole team.

---

## Press release

### ChangeRiskAdvisor gives DevOps engineers an evidence-backed risk read on any proposed change, in one question

*Engineers who review changes now see similar past incidents, live service
health, freeze windows, and downstream dependents before they decide, and the
decision stays with them.*

**INTERNAL LAUNCH, October 16, 2026.** The platform engineering team today
launched ChangeRiskAdvisor (CRA), an assistant for engineers who review
proposed production changes. An engineer describes a change, and CRA returns a
risk assessment that cites the past incidents it draws on, the current health
and freeze-window status of the service, and the services that depend on it.
CRA only advises. It never approves, blocks, merges, or deploys a change. The
go/no-go call stays with the engineer and their team.

Raj Sam, a DevOps engineer, reviews about a dozen proposed changes a day across
services they don't all know deeply, and the risky ones rarely look risky. In
February, a config change lowered checkout-service's payment-gateway timeout
from 5,000 ms to 500 ms. It was reviewed as a low-risk tweak. Eight minutes
after it deployed, a promotional email tripled traffic; checkout success
dropped 42% for 38 minutes and about 1,150 checkout attempts failed. Two earlier incidents on the
same payment-gateway dependency pointed to exactly this risk, but nobody
reviewing the change had them in front of them. Of the ten change-related
incidents recorded between February and September, four hit checkout-service
and three were SEV1.

With CRA, Raj Sam asks "How risky is this change to the checkout-service
config?" and gets one answer that brings the context together: the past
incidents most like the proposed change, with their IDs and root causes;
whether checkout-service is healthy and whether a freeze window is active right
now; which services sit downstream and would feel an outage; and a flag when the
change touches a service the team has marked high-risk. Every statement in the
assessment points to its source. When CRA can't confirm something, for example
because the freeze calendar didn't respond, it says that point is unconfirmed
instead of guessing.

"I don't want a bot deciding what ships. I want the context I'd have if I'd
been on call for every incident on every service," said Raj Sam. "When I look
at a timeout change on checkout-service now, INC-2201 is right there in the
answer, along with who depends on checkout and whether we're in a freeze. Safe
changes go faster because I can see why they're safe, and risky ones get the
second look they need."

CRA also remembers what the team has decided. Tell it once that
"checkout-service is always high-risk for our team," and it flags
checkout-service in every later session without being reminded. That setting
stays until the team changes it. CRA never quietly downgrades it.

Engineers open CRA in the browser, describe the change in plain language, and
read the assessment. Every answer ends with the same reminder: this is
advisory, and the decision needs a human. A trace panel under each answer shows
which checks CRA ran and which incidents it used, so any engineer can verify
the reasoning before acting on it.

---

## FAQ

### Customer questions

**1. What does CRA do?**

CRA turns a change description into a risk assessment backed by evidence. It
looks up similar past change-related incidents and postmortems, checks the
service's current health and freeze-window status, lists the services that
depend on it, and applies the team's stored risk settings. It explains its
reasoning and cites each source, then leaves the decision to you.

**2. Will CRA approve or block my change?**

No. CRA never approves, blocks, merges, or deploys a change, and every answer
says that a human decision is required. If you ask it to "just approve this
change," it declines, explains that approval is an explicit human step, and
offers to complete the risk assessment instead. The people who ship a change
are accountable for it and hold context CRA doesn't, such as business timing
and customer commitments. An assistant that could approve changes would invite
rubber-stamping, which is the failure CRA exists to prevent.

**3. How do I know the assessment is right?**

Every claim in an assessment is tied to evidence you can check: a retrieved
incident or postmortem (for example "INC-2201, payment timeout misconfigured
during release") or the result of a live check made for that answer (health,
freeze window, or dependency graph). CRA does not give a risk rating it can't
support. If the evidence is thin, it says so and tells you what is missing.

**4. What if there's no similar past incident?**

CRA tells you it found no matching incident in the corpus. It doesn't stretch
an unrelated incident to fit or invent one. The assessment then rests on the
live checks and the team's stored settings, and it notes that the lack of
history makes the read less certain.

**5. What happens if a health, freeze-window, or dependency check fails?**

CRA tells you which check failed and treats that part of the assessment as
unconfirmed, for example: "I couldn't confirm the freeze calendar right now;
treat freeze status as unconfirmed." It never fills the gap with a guess. Every
failure is logged and counted, so the team can see how often checks fail and
how CRA handled each one.

**6. How does CRA remember our team's risk settings?**

Tell CRA in plain language, such as "checkout-service is always high-risk for
our team" or "no config changes to auth-service during a freeze." It stores the
setting for your team and applies it automatically in later sessions. You can
ask what it has stored at any time. Settings change only when the team changes
them. CRA never silently downgrades or overrides them.

### Internal questions

**7. What data does CRA use, and how is it handled?**

This build uses synthetic data only: twelve fictional change-related incidents,
plus a dependency graph and health and freeze-window snapshots covering eight
services, along with sample postmortems and runbooks. It uses no
production systems, real incident records, or customer data. Change
descriptions and retrieved excerpts are sent to the language model inside our
own cloud project to produce each answer. The vector index and session history
stay on the machine running CRA, and team memory stores only risk settings
(service flags and freeze-window notes). Secrets and project identifiers stay
in a local environment file that is never committed. Before any real rollout,
postmortems would need names, customer details, and credentials redacted before
indexing, and access would follow the same permissions as the incident tracker.

**8. How are the guardrails enforced, rather than only requested in the prompt?**

The system prompt sets the rules, and a separate check runs on every response
before Raj Sam sees it. The check confirms three things: the response contains
no approval, block, merge, or deploy decision; every risk claim carries a
citation; and every statement about health, freeze windows, or dependencies
matches a tool result from the same request. A response that fails is
corrected or labelled unconfirmed, and the event is logged. We test this with
direct approval requests, indirect phrasings, and requests for a risk rating
when no evidence exists.

**9. Why advisory-only, when auto-approving low-risk changes would save more time?**

Because "low risk" is exactly the label that failed in INC-2201. That change
was classified as a low-risk config tweak and caused a SEV1 outage. If CRA
could approve changes, its mistakes would ship directly to production. As an
advisor, its mistakes are caught by a person who can see the cited evidence and
disagree. The time saving comes from faster, better-informed reviews, not from
removing the reviewer.

**10. What happens when a stored team setting conflicts with the evidence?**

The team's setting wins, and CRA shows the conflict. If checkout-service is
flagged high-risk but no recent incidents match the change, CRA still flags it
as high-risk, reports that it found no matching incidents, and leaves the team
to decide whether to change the setting. It never overrides a stored setting on
its own judgement.

**11. How does CRA handle a vague request such as "is this change safe?"**

It asks which service and what change before assessing anything. A risk read
on an unidentified change would have to be guessed, which the guardrails
forbid. Once the service and change type are clear, it runs the normal
assessment.

**12. How will we know CRA works?**

We score it against the six sample queries in requirements.md, each with an
expected behaviour and a pass/fail result, and record a baseline before fixes
and a score after. Alongside that we track four measures: the share of
assessments that cite evidence (target 100%), approval statements across the
refusal and red-team probes (target 0), recall of stored high-risk flags in a
second session (target 100%), and the tool-check failure rate, including how
each failure was handled.

**13. How does CRA answer "what depends on payment-gateway?"**

It calls the dependency-graph tool and reports what the tool returns. It never
infers dependencies from service names. For payment-gateway, the graph shows
that checkout-service calls it directly, and that order-service, web-frontend
and mobile-frontend depend on it through checkout-service. payment-gateway
itself depends on notification-service. If the tool is unavailable, CRA says
the dependency list is unconfirmed.

---

## Review sign-off

Agreement is recorded as an approval on the pull request that adds this file,
plus a row below for each reviewer.

| Name | Role | Decision | Date | Approval link |
|---|---|---|---|---|
| Raj Sam | Author | Agreed | _pending_ | |
| _reviewer_ | Team member or mentor | _pending_ | | |
