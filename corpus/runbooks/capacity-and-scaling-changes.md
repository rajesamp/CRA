---
doc_type: runbook
title: Capacity and scaling changes
services: all
source: synthetic
---

# Capacity and scaling changes

Connection pools, autoscaling thresholds, replica counts, and cache TTLs
should be sized for peak load, not averages.

Past incidents: INC-2255 (auth-service connection pool reduced too far,
SEV1), INC-2325 (checkout autoscaling threshold raised before a sale),
INC-2139 (notification queue consumers cut from 6 to 2), INC-2229 (CDN cache
TTL raised, stale prices).

Before release: check peak metrics and the event calendar. Avoid capacity
reductions on checkout and auth in the days before a known peak.
