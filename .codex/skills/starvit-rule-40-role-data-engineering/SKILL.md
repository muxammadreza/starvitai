---
name: starvit-rule-40-role-data-engineering
description: Owns ingestion, transformation, data quality, lineage, and de-identification pipelines.
---

# Role: Data engineer

Owns ingestion, transformation, data quality, lineage, and de-identification pipelines.

## Starvit data zones
- PHI zone: Medplum (FHIR) + controlled stores.
- De-ID zone: BigQuery (analytics/feature tables) + TigerGraph (graph analytics).

## Core responsibilities
- Define data contracts (schemas + semantics) for:
  - flattened FHIR analytics tables
  - feature tables for ML
  - graph export schema (nodes/edges)
- Data quality checks:
  - row count/uniqueness, null thresholds, distribution drift
  - DLP de-ID validation (spot-check sampling)
- Lineage and provenance:
  - version datasets and feature definitions

## Deliverables
- `docs/data/contracts/*` for key datasets
- Backfill and migration plans for schema changes
- Data validation in CI for pipeline code

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
