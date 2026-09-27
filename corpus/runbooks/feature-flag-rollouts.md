---
doc_type: runbook
title: Feature flag rollout runbook
services: all
source: synthetic
---

# Feature flag rollout runbook

Roll out flags in stages (for example 1%, 10%, 50%, 100%) and let the canary
finish before widening.

Past incidents: INC-2233 (checkout flag at 100% before canary finished),
INC-2248 (order-splitting flag enabled in all regions at once), INC-2166
(mobile payment flag without a minimum app-version check), INC-2340 and
INC-2341 (auth token flag and mobile session flag mismatched across regions).

Before release: confirm the canary completed, gate mobile flags on app version,
and coordinate paired flags across services so both sides change together.
