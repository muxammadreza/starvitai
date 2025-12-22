---
description: Add or upgrade data quality checks + monitoring for a dataset/pipeline
---

Use this when introducing a new table/view/feature set, or when a pipeline changes semantics.

## 1) Declare the contract
- Dataset/table name + owner
- Grain (one row per what?)
- Primary/unique keys (or explicit append-only)
- Required fields + types
- Units and clinical semantics (if relevant)
- Partition key and expected update cadence (freshness SLA)

## 2) Implement automated checks (minimum bar)
- **Freshness**: latest partition age, ingestion lag
- **Completeness**: row counts and null-rate thresholds for required fields
- **Validity**: accepted values, numeric ranges, regex formats
- **Uniqueness**: key uniqueness or dedupe invariant
- **Relationships**: referential integrity where applicable
- **Schema drift**: fail closed (or alert-only) depending on criticality

Implementation options:
- dbt tests (schema + custom tests) for warehouse tables/views
- Dataform assertions for SQL pipelines
- Streaming pipelines: DLQ + parse-failure counters + duplicate counters

## 3) ML / feature-specific checks (if applicable)
- Point-in-time correctness tests (no feature timestamp after label/prediction time)
- Distribution drift monitoring for key features (mean/std/quantiles + PSI)
- Missingness drift monitoring

## 4) Governance gate
- Confirm data classification and de-ID verification coverage.
- Ensure policy tags / masking are updated if sensitive quasi-identifiers exist.

## 5) Monitoring + runbooks
- Add dashboards: freshness, errors, volumes, drift metrics.
- Add alerts with explicit runbook links.
- Document: rollback, replay/backfill steps, and owner escalation.

Deliverables:
- Test definitions + where they run (CI vs scheduled)
- Alert thresholds + runbook
- Updated docs/data dictionary entries
