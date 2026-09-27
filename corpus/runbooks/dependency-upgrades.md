---
doc_type: runbook
title: Dependency upgrade runbook
services: all
source: synthetic
---

# Dependency upgrade runbook

Library and client upgrades can change defaults the service relies on
implicitly.

Past incidents: INC-2055 (HTTP client upgrade shrank the connection pool,
SEV1), INC-2214 (client library version mismatch with a caller), INC-2301
(deprecated API broke on upgrade), INC-2098 (ORM upgrade changed transaction
isolation), INC-2112 (build tool upgrade dropped a polyfill).

Before release: read the release notes for changed defaults, pin critical
settings explicitly (pool sizes, timeouts, isolation levels), check which
callers use the old version, and load test upgrades on the payment path.
