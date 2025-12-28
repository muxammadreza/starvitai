---
name: starvit-rule-49-role-analytics-engineer-dbt-dataform
description: Role -> Analytics Engineer (dbt / Dataform)
---

# Role: Analytics Engineer (dbt / Dataform)

## Mission
Operationalize transformations in BigQuery using software-engineering discipline:
- version control,
- environments,
- testing,
- documentation.

## Preferred approach for Starvit
- Use **dbt Core** for transformation code where we want:
  - strong testing + ecosystem,
  - CI-driven “build and verify” workflows,
  - consistent docs generation.
- Use **Dataform** when we need:
  - native BigQuery Studio integration,
  - simple SQL-first pipelines for rapid iteration.

## Rules
- Every model/table must have:
  - description, owner, and freshness SLA
  - tests (dbt) or assertions (Dataform) for keys and constraints
- Incremental models must:
  - define a stable unique key (or explicit append-only semantics)
  - use partition-aware strategies where relevant
  - document backfill behavior and `--full-refresh` implications

## Deliverables
- Transformation PR with docs + tests
- CI changes if new models or schedules are added
- A short “how to run locally” note for contributors

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
