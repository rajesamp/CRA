---
doc_type: runbook
title: Timeout and retry changes on the payment path
services: checkout-service, payment-gateway
source: synthetic
---

# Timeout and retry changes on the payment path

Timeout, retry, and rate-limit values on the payment path (checkout-service
calling payment-gateway, payment-gateway calling the card processor) are
behaviour changes, not cleanups.

Past incidents: INC-1987 (card-processor timeout lowered below peak p99),
INC-2201 (checkout payment timeout cut from 5000 ms to 500 ms, SEV1),
INC-2289 (checkout retry timeout too low under load), INC-2318 (rate limit
below peak traffic, SEV1).

Before release: compare the new value with the dependency's peak p99 latency,
not its average. Load test at 3x baseline traffic (INC-2201 action item).
Check the event calendar for promotions. Treat both services as high-risk if
the team has flagged them.
