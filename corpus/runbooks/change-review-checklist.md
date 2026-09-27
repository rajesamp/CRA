---
doc_type: runbook
title: Change review checklist
services: all
source: synthetic
---

# Change review checklist

Use this checklist for every production change before the go/no-go decision.
The decision itself is always made by a human reviewer.

1. Identify the service and the change type (config change, dependency upgrade,
   feature flag rollout, infra change, schema migration).
2. Look up past incidents on the same service and the same change type. Similar
   incidents are the strongest signal of risk. INC-2201 happened because two
   earlier payment-gateway incidents were not consulted.
3. Check current health and freeze-window status with the system-health tool.
   Never assume freeze status.
4. Check the blast radius with the dependency-graph tool: who depends on this
   service, directly and indirectly.
5. Check the team's stored risk settings. A service flagged high-risk stays
   high-risk until the team changes the flag.
6. Check the traffic and event calendar. Peak events (sales, launches,
   promotional emails) multiply the impact of a bad change, as in INC-2201 and
   INC-2325.
7. Record the risk read with its evidence and leave the decision to the
   reviewer.
