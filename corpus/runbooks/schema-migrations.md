---
doc_type: runbook
title: Schema migration runbook
services: all
source: synthetic
---

# Schema migration runbook

Schema changes must stay backward compatible until every caller has moved.

Past incidents: INC-2270 (backward-incompatible column drop in
inventory-service), INC-2071 (order status column made non-nullable before the
backfill finished).

Before release: use expand-and-contract migrations, finish backfills before
adding constraints, and drop columns only after no caller reads them.
