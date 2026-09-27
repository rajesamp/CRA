# The Amazon 6-Pager, From First Principles

A study guide for task #2 of the ChangeRiskAdvisor plan. Read it once end to
end (about 20 minutes), then keep the outline and checklist open while you
write `docs/6-pager.md` section by section.

## What a 6-pager is

A 6-pager is a narrative memo of at most six pages, written in full sentences
and paragraphs, that replaces a slide deck as the input to a decision meeting.
It started in June 2004, when Jeff Bezos ended PowerPoint presentations at
Amazon's senior-team (S-team) meetings in favour of short written memos; the
standard length later settled at six pages. His email explained why a good
memo is harder to write than a 20-page deck:

> "...the narrative structure of a good memo forces better thought and better
> understanding of what's more important than what, and how things are related."

Supporting data goes in an appendix, which has no page limit. The meeting
starts with everyone reading the memo in silence, and discussion only begins
once everyone has finished.

## The first principles

Each principle below says what the format does, why it works, and what it
means for the CRA 6-pager.

### Writing is thinking

Slides let you place two ideas next to each other without saying how they
connect. Sentences don't. To write "because", "so", or "unless", you have to
know the causal link. A memo that is hard to write is usually hard because the
thinking isn't finished yet, and the writing exposes that before a reader does.

**For CRA:** If you can't write one paragraph explaining *why* retrieving past
postmortems changes a reviewer's decision, the RAG design isn't justified yet.

### Narrative connects; bullets fragment

Bullets drop the connective tissue: the reasons, the trade-offs, the order of
cause and effect. A reader of bullets fills those gaps with their own
assumptions, and different readers fill them differently. Prose carries one
chain of reasoning from the author to every reader.

**For CRA:** The course definition of done rules out bullet-only sections. Tables
are fine for data, but every section needs paragraphs that say what the data
means.

### Silent reading creates shared context

In a presentation the room moves at the presenter's speed, and charisma
competes with content. In a reading meeting everyone reads at their own pace,
annotates, and arrives at the discussion with the same full context. The author
doesn't present. The document has to stand on its own.

**For CRA:** Write for a Beyond Vectors mentor who has never seen the repo. Define
terms like "freeze window" and "blast radius" the first time they appear.

### The page limit forces priorities

Six pages is roughly 3,000 words. The limit forces you to decide what matters
most and cut the rest, or move it to the appendix. What you leave out shows the
reader your judgement as much as what you keep.

**For CRA:** The model choice, vector store, and framework comparison belong in
the appendix or the decision records, not the main body. The body is about Raj
Sam's problem and how CRA changes their day.

### Data replaces adjectives

Words like "significantly", "most", "often", and "robust" (Amazon calls them
weasel words) sound informative but can't be checked. A number with a comparison
and a source can be.

**Weak:** "Config changes to critical services are often risky and have caused
significant outages."

**Strong:** "Four of the ten change-related incidents since February hit
checkout-service. The worst, INC-2201, was a timeout config change reviewed as
low-risk; it cut checkout success by 42% for 38 minutes and failed about 1,150
checkout attempts."

The strong version is checkable, specific, and it makes the argument on its
own.

### Start from the customer, not the technology

Amazon calls this working backwards: begin with a specific customer and their
problem, then describe the experience that solves it, and only then the
technology. Memos that open with architecture tend to solve problems nobody has.

**For CRA:** Open with Raj Sam reviewing a dozen changes a day, not with "a RAG
agent built on Google ADK". The stack earns one paragraph near the end of the
solution section.

### Seek truth, not approval

A good memo invites the reader to find holes. It states risks, unknowns, and
non-goals plainly, because a flaw found in the meeting is cheap and a flaw found
in production is not. Non-goals matter as much as goals, because they stop
scope creep and set expectations.

**For CRA:** "CRA never approves, blocks, merges, or deploys a change" is your most
important non-goal. Say it explicitly, and explain why Raj Sam insists on it.

## How the reading meeting runs

1. The author shares the memo at the start of the meeting (or shortly before).
2. Everyone reads in silence for 20 to 30 minutes and writes comments in the
   margins.
3. Discussion goes through the questions and comments, usually page by page.
   The author listens and answers, and doesn't re-present the memo.
4. The meeting ends with a decision, or with a list of what must change before
   a decision.

For the cohort, that means the 6-pager must be understandable by a reviewer who
reads it cold during the Sunday check-in.

## The CRA 6-pager outline

This follows the sections tasks.md requires, plus a short introduction and an
appendix. The word budgets add up to about 3,000 words for the main body.

| Section | Words | Question it answers |
|---|---|---|
| Introduction (write it last) | ~150 | What is this memo about, and what do you want from the reader? |
| Problem | ~450 | What goes wrong today, how often, and what does it cost? |
| Customer | ~400 | Who exactly has this problem, and what does their day look like? |
| Solution | ~750 | What does Raj Sam experience with CRA, step by step? |
| Goals and non-goals | ~400 | What will CRA do, and what will it deliberately never do? |
| Key risks and mitigations | ~450 | What could make this fail or cause harm, and what do we do about it? |
| Success metrics | ~400 | How will we know it works, with which numbers and targets? |
| Appendix | no limit | Data, dependency graph, glossary, open questions |

### Introduction (~150 words, write it last)

State what CRA is in one sentence, who it's for, and what the memo asks of the
reader (for example: agree on the scope and the success metrics for the 4-week
build). You can only write this well once the other sections exist.

### Problem (~450 words)

Describe what goes wrong today and what it costs, without mentioning CRA.

- **Evidence to use:** the sample dataset has 10 change-related incidents from
  February to September 2026 across 6 services: 3 SEV1, 4 SEV2, 3 SEV3.
  checkout-service had 4 of them. The INC-2201 postmortem shows the core
  failure: a config change was classified as low-risk, and two earlier incidents
  on the same dependency were not surfaced during review.
- **Trap:** describing the missing solution ("there is no RAG tool") instead of
  the problem ("reviewers can't recall past incidents on the service they're
  changing").

### Customer (~400 words)

Make Raj Sam concrete. They are a DevOps engineer at a mid-size SaaS company
who reviews about a dozen proposed changes a day, across services they don't
all know deeply. Describe what they do today to judge a change, where that
breaks down, and what they refuse to give up (the go/no-go decision stays with
them and the team).

- **Trap:** writing about "DevOps teams" in general. Specific beats broad.

### Solution (~750 words)

Walk through one real example from Raj Sam's side of the screen. For instance:
they paste "lower checkout-service payment timeout to 500 ms". CRA returns a
risk read that cites INC-2201 and INC-2289, reports checkout-service's current
health and freeze status, lists who depends on it (order-service, web-frontend,
mobile-frontend), flags that the team marked checkout-service high-risk, and
ends with the reminder that the decision is Raj Sam's.

Then explain the four capabilities that make that possible (search over past
incidents, live health and dependency tools, team memory, guardrails) in one
paragraph each. Keep the stack to one short paragraph and link the decision
records.

- **Trap:** leading with architecture diagrams or framework names.

### Goals and non-goals (~400 words)

Goals are outcomes, not activities. "Every assessment cites at least one
retrieved incident or live tool result" is a goal. "Build a RAG pipeline" is an
activity.

Non-goals to state and justify: CRA never approves, blocks, merges, or deploys;
no live CI/CD or production integration in this build (static dataset); it does
not replace the team's change review, it prepares it.

### Key risks and mitigations (~450 words)

For each risk, say how likely it is, what happens if it occurs, and what the
mitigation is. Candidates from requirements.md:

- Fabricated evidence or freeze status → every claim must come from a retrieved
  document or a live tool call, or be labelled unconfirmed.
- Tool failure or timeout → degrade gracefully and say so ("I couldn't confirm
  the freeze calendar; treat this as unconfirmed").
- Over-trust in the tool → every output restates that a human decision is
  required.
- Stored risk settings silently overridden → high-risk flags stay until the
  team changes them.
- Sensitive content in postmortems → synthetic data only for this build.

**Trap:** a list of risks with no mitigation or no sense of which ones matter
most.

### Success metrics (~400 words)

Give each metric a target and a way to measure it. Separate what the build
controls (input metrics) from the outcome it's meant to move (output metrics).

- **Input examples:** all 6 sample queries pass the eval; 100% of assessments
  cite evidence; 0 approval statements across the refusal and red-team probes;
  the high-risk flag is recalled in 100% of second-session tests.
- **Output hypothesis:** time for Raj Sam to reach an evidence-backed risk read
  drops from minutes of manual digging to one query. Say how you'd measure it
  (timed runs on the sample changes).
- **Trap:** vanity metrics ("users love it") or metrics with no target.

### Appendix (no limit)

The incident table, the dependency graph, current health and freeze status,
a glossary (freeze window, blast radius, SEV levels), open questions, and links
to the decision records.

## Self-review checklist

Run this on every section before asking for review, and on the full memo before
marking task #2 done.

- [ ] Every required section is present and written as prose, not bullets only.
- [ ] Every section is specific to CRA; none of it could be pasted into another
      project's memo.
- [ ] Every claim has a number or a source; no weasel words (significantly,
      many, most, nearly, very, robust, seamless, best-in-class).
- [ ] Raj Sam is the only persona name used.
- [ ] The advisory-only rule appears in the solution, the non-goals, and the
      risks.
- [ ] Each paragraph opens with its point.
- [ ] The main body is about 3,000 words or less; supporting data is in the
      appendix.
- [ ] A reader with no context could explain CRA back in three sentences.
- [ ] It reads in 20 minutes or less.
- [ ] Reviewed and agreed (course evidence): reviewer sign-off recorded at the
      bottom of the memo.

## How we'll write it: section by section

1. Write order: **Customer → Problem → Solution → Goals and non-goals → Success
   metrics → Risks and mitigations → Introduction → Appendix.** Customer comes
   first because every other section depends on knowing exactly whose problem
   you're solving.
2. You draft one section in `docs/6-pager.md` (or paste it into the chat).
3. I review it against this checklist and the course definition of done, with
   line-level comments.
4. You revise, then we move to the next section.
