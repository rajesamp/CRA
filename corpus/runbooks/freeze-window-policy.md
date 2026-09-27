---
doc_type: runbook
title: Freeze window policy
services: all
source: synthetic
---

# Freeze window policy

A freeze window is a period when non-emergency changes to a service should
not ship, for example before a peak sales event or during a vendor
maintenance window.

Current freeze status must always come from the system-health tool. Never
state that a freeze is or is not active without a tool result from the same
request. If the tool is unavailable, say: "I couldn't confirm the freeze
calendar right now; treat freeze status as unconfirmed."

If a change targets a service in a freeze window, flag it clearly. Emergency
changes during a freeze still need an explicit human decision; CRA never
grants an exception. If a question about freeze status does not name a service,
ask which service before answering.
