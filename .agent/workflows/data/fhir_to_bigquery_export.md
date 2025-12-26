---
description: Move FHIR data into the de-identified BigQuery zone (export + de-ID gate)
---

## When to use
- You need fresh research data in BigQuery derived from FHIR resources.

## Default posture
- PHI is sourced from **Medplum FHIR**.
- BigQuery is **de-identified only**.
- De-identification (Cloud DLP or explicitly-approved equivalent) happens **before** any data lands in BigQuery.

## Steps
1) Identify required FHIR resources/fields
   - Observation, Condition, MedicationRequest, etc.
   - Minimize fields; avoid identifiers unless strictly needed in PHI zone.

2) Pick the movement pattern
   - **Batch export (default)**: use FHIR Bulk Data (`$export`) for backfills and scheduled refreshes.
   - **Event-driven (optional)**: use Medplum Subscriptions/Bots to emit de-ID events.

3) Enforce the de-ID gate (mandatory)
   - Export from Medplum to a **PHI staging bucket**.
   - Run Cloud DLP de-ID into a **separate de-ID bucket**.
   - Version and record the de-ID configuration and residual re-identification risk.

4) Load into BigQuery
   - Load de-identified NDJSON/Parquet into normalized resource tables.
   - Apply Starvit’s versioned flattening spec to produce curated fact tables and ML features.
   - Design partitioning/clustering (event time + common cohort keys).
   - Use stable pseudo-identifiers (no PHI).

5) Validate and monitor
   - Schema + nullability checks
   - “No identifiers present” assertions
   - Row counts vs source sanity checks
   - Cost guardrails (bytes scanned, job labels)

Deliverables
- Pipeline spec + runbook
- BigQuery dataset/table DDL
- De-ID tests + monitoring
