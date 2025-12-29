# De-identified pipeline boundary contract (PHI → De-ID → Analytics)

Date: 2025-12-29
Owner: Data Platform
Status: Draft (synthetic-only scaffold)

## Goal
Establish the PHI boundary and define the minimal contract for moving **only de-identified data** from Medplum (PHI zone) into analytics sinks. This document covers the scaffolded stub, not a production pipeline.

## Boundary contract
**PHI zone (Medplum/FHIR)** → **De-ID transformer (controlled service)** → **De-ID analytics sink (BigQuery)**

### PHI zone (source)
- System: Medplum FHIR (system of record).
- Data types: FHIR resources (Observation, Condition, etc.).
- Access: backend service role only; no direct analyst access.

### De-ID transformer (boundary)
- Inputs: in-memory resource payloads only (no direct Medplum IO in the stub).
- Allowed sources: synthetic fixtures only (generated in tests).
- De-ID policy: allowlisted fields only; direct identifiers removed or pseudonymized.
- Controls:
  - `APP_ENV` must be one of `dev|test|local`.
  - `STARVIT_MODE` must be `stub`.
  - Non-synthetic source kinds are rejected.

### Analytics sink (destination)
- Target: BigQuery dataset (de-identified zone).
- No PHI or quasi-identifiers without approved policy tags.
- Access: governed via dataset IAM + policy tags + row-level security as needed.

## Data movement constraints
- Direct identifiers **must not** leave Medplum.
- Pseudonymous keys are derived inside the transformer boundary.
- Logging/tracing must not include PHI; only opaque IDs and run metadata.

## Stub scope (current)
- Synthetic-only transformer for Observation-like fixtures.
- Placeholder allowlist and pseudonymization strategy.
- No external connections (Medplum, BigQuery, TigerGraph) in stub.
- Runbook: `docs/deid/stub-runner.md`.

## Next steps (production readiness)
- Formal DLP/de-identification policy definition.
- Medplum export service with audited access and rate limits.
- BigQuery dataset provisioning with policy tags and RLS.
- Runbooks for backfill, rollback, and retention enforcement.
