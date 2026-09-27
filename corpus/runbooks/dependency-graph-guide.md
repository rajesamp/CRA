---
doc_type: runbook
title: Using the dependency graph
services: all
source: synthetic
---

# Using the dependency graph

The dependency graph shows which services a service calls and which
services call it. The blast radius of a change is every service downstream of
the one being changed.

Questions such as "what services depend on payment-gateway?" or "who calls
checkout-service?" must be answered with the dependency-graph tool. Dependencies
must always come from that tool, never from service names or memory. If the tool is unavailable, say the dependency list is
unconfirmed.

Report both directions: what the service depends on, and what depends on it,
directly and through other services. A failure in a service with many
dependents (for example one that sits under both frontends) has a wide blast
radius.
