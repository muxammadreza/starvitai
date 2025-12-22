# Starvit architecture (high level)

Starvit is a clinician-supervised metabolic-therapy support platform with strict PHI controls.

## Zones
### PHI system of record
- Google Cloud Healthcare API (FHIR R4)
- Strict RBAC + audit logging

### De-identified research zone
- BigQuery: analytics + feature tables
- TigerGraph: relationship mining, embeddings, link discovery
- Vertex AI: training/serving (models must be auditable and approval-required)

See `docs/decisions/ADR-0003-bigquery-role.md` for the BigQuery↔TigerGraph division of labor and data movement patterns.

## Invariants
- One backend for MVP (modular monolith).
- UIs never talk to TigerGraph directly.
- Every recommendation is auditable: inputs -> transforms -> outputs -> versions -> clinician decision.
