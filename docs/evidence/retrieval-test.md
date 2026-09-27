# Evidence: retrieval test (task #9)

Query: "How risky is this change to the checkout-service config?" · top 3 · run 2026-09-27 06:40 UTC

Definition of done: relevant past-incident chunk(s) appear in the top-3 results.
Relevant here means a checkout-service config-change incident: INC-2201, INC-2289.

| Rank | Score | Source | Incident | Judgment |
|---|---|---|---|---|
| 1 | 0.528 | `corpus/postmortems/INC-2201.md` | INC-2201 | relevant |
| 2 | 0.497 | `corpus/runbooks/high-risk-services-policy.md` | — | supporting |
| 3 | 0.468 | `corpus/postmortems/INC-2201.md` | INC-2201 | relevant |

**Result: CORRECT.** A relevant incident chunk is in the top 3.

Top relevant chunk:

```
Postmortem INC-2201: checkout-service payment timeout outage [INC-2201 | checkout-service | Config change | SEV1]
## Root cause

The timeout change was classified as a low-risk config tweak and was not load
tested at production traffic levels. The change review did not flag
checkout-service's dependency on payment-gateway as high-risk, even though two
earlier incidents involved the same dependency: INC-1987 (config change, SEV2,
2025-09-02) and INC-2055 (dependency upgrade, SEV1, 2025-11-19).
```

The same check runs for all six sample queries in `tests/test_cra.py`.
