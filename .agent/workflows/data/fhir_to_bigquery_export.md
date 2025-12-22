---
description: Move FHIR data into the de-identified BigQuery zone (export/stream + de-ID gate)
---

## When to use
- You need fresh research data in BigQuery derived from FHIR resources.

## Steps
1) Identify required FHIR resources/fields:
   - Patient, Observation, Condition, MedicationRequest, etc.
2) Pick the movement pattern:
   - **batch export** for backfills and controlled periodic loads
   - **streaming changes** for near-real-time research when needed
3) Enforce the de-ID gate (mandatory):
   - de-identify in Cloud Healthcare first (`datasets.deidentify` / `fhirStores.deidentify`)
   - export/stream **only** from the de-identified store
   - version the de-ID config and document residual re-identification risk
4) Export/stream to BigQuery:
   - prefer schema type `ANALYTICS_V2`
   - design partitioning/clustering (event time + common cohort keys)
   - use stable pseudo-identifiers (no PHI)
5) Validate and monitor:
   - schema + nullability checks
   - “no identifiers present” assertions
   - row counts vs source sanity checks
   - cost guardrails (bytes scanned, job labels)

Deliverables:
- Pipeline spec + runbook
- BigQuery dataset/table DDL
- De-ID tests + monitoring
