---
description: Data governance + de-ID pipeline change workflow
---

Use this when adding or modifying any pipeline involving **FHIR → de-ID → BigQuery → TigerGraph** (or any analytics/feature table).

## 1) Classify the data fields
- Direct identifiers (PHI)
- Quasi-identifiers (re-identification risk)
- Clinical content (sensitive even if not identifying)
- Operational telemetry

## 2) Define lineage (must be explicit)
- Source FHIR resources and fields
- Transformation steps and versions (code hash + config version)
- De-identification method and configuration
- Destination schema:
  - BigQuery tables/views + partitioning
  - TigerGraph vertices/edges + keys

## 3) Choose the de-ID method and validate
- Confirm direct identifiers are removed/masked **before** leaving PHI zone.
- Add automated assertions for “no identifiers present” on the de-ID output.
- Document residual re-identification risks and assumptions.

## 4) Access controls (fail closed)
- BigQuery:
  - dataset/table IAM
  - row-level security policies when needed for cohort isolation
  - policy tags + column-level access control / masking for sensitive quasi-identifiers
- TigerGraph:
  - backend Research API allowlisted queries only
  - no direct UI access to graph DB

## 5) Retention and deletion
- Define retention class and purge strategy for the derived data product.
- Ensure exports/snapshots are not retained indefinitely.

Deliverables:
- Data contract + lineage notes
- De-ID tests + acceptance criteria
- IAM/RLS/policy-tag diffs (PR)
- Runbook: replay/backfill and rollback steps
