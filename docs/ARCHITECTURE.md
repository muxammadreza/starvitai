# Starvit architecture (high level)

Starvit is a clinician-supervised metabolic-therapy support platform with strict PHI controls.

## Zones

### PHI system of record (FHIR)
- **Medplum FHIR R4 server** (system of record for all PHI and clinical workflow artifacts)
- Controls we rely on from Medplum:
  - OAuth2/OIDC auth
  - role + compartment access control (AccessPolicy)
  - FHIR-native audit trail (`AuditEvent`) and provenance (`Provenance`)
  - subscriptions + bots for server-side automations

**Important:** self-hosted Medplum on a VPS is acceptable for development with synthetic data; production hosting of real PHI is a separately approved workstream.

### De-identified research zone
- BigQuery: analytics + feature tables (de-identified only)
- TigerGraph: relationship mining, embeddings, link discovery (de-identified only)
- Vertex AI: training/serving (models must be auditable and approval-required)

See `docs/decisions/ADR-0003-bigquery-role.md` for the BigQuery↔TigerGraph division of labor and data movement patterns.

## Invariants
- One backend for MVP (modular monolith).
- UIs never talk to TigerGraph directly.
- Every recommendation is auditable: inputs -> transforms -> outputs -> versions -> clinician decision.
