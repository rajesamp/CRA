---
doc_type: runbook
title: High-risk services and team risk settings
services: all
source: synthetic
---

# High-risk services and team risk settings

The team keeps a list of services it treats as high-risk, plus notes on its
freeze-window policy. CRA stores these settings in team memory and applies
them in every session without being reminded.

Setting or clearing a flag: anyone on the team can ask in chat, for example
"Remember that checkout-service is always high-risk for our team." CRA repeats
the change back and saves it only after explicit confirmation. Every downgrade
(clearing a high-risk flag) is logged.

CRA never changes a stored setting on its own judgement. When the evidence for
a change looks mild but the service is flagged high-risk, CRA still flags it and
reports both facts. The INC-2201 postmortem recommended flagging
checkout-service and payment-gateway as high-risk; the flags only take effect
once the team sets them.
