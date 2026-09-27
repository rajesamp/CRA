# Data

Synthetic data for ChangeRiskAdvisor. No production systems, real incident
records, or customer data.

| File | Contents | Count |
|---|---|---|
| `incidents.json` | Past change-related incidents: id, service, date, change type, severity, root cause, source | 20 incidents across 8 services |
| `dependencies.json` | Service dependency edges (`service` depends on `depends_on`) | 10 edges across 8 services |
| `health.json` | Current status, freeze-window flag, last incident date per service | 8 services |
| `golden_eval.json` | Expected behaviour for the 6 sample queries in requirements.md | 6 cases |

## Provenance

Each incident carries a `source` field:

- `course_sample`: copied from `sample_data/change_risk_sample.xlsx` in
  [Sep-Projects/ChangeRiskAdvisor](https://github.com/abhineer/Sep-Projects/tree/main/ChangeRiskAdvisor/sample_data)
  (10 incidents). `dependencies.json` and `health.json` come from the same
  workbook, with the freeze flag converted from Yes/No to true/false.
- `postmortem_table+synthetic_root_cause`: INC-1987 and INC-2055. Service,
  date, change type, and severity come from the related-incident table in the
  INC-2201 postmortem. That table has no root causes, so the root causes were
  written as synthetic data.
- `synthetic`: eight incidents written for this project (task #6) so every
  service has at least two. Their dates are consistent with
  `last_incident_date` in `health.json`, and none is a config change, so the
  course sample's config-change pattern is unchanged.

## Summary

| Service | Incidents | Status | Freeze window |
|---|---|---|---|
| checkout-service | 4 | Healthy | No |
| payment-gateway | 4 | Degraded | No |
| auth-service | 2 | Healthy | Yes |
| inventory-service | 2 | Healthy | No |
| notification-service | 2 | Healthy | No |
| order-service | 2 | Healthy | No |
| web-frontend | 2 | Healthy | No |
| mobile-frontend | 2 | Healthy | Yes |

Severity: 4 SEV1, 8 SEV2, 8 SEV3. Change types: 5 dependency upgrades, 5
feature-flag rollouts, 4 config changes, 4 infra changes, 2 schema migrations.
Date range: 2025-09-02 to 2026-09-10. Every service has at least two
incidents, as task #6 requires.
