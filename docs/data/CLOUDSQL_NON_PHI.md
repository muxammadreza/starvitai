# Cloud SQL for Postgres (operational, non-PHI)

## Purpose
Store operational data that must not include PHI:
- workflow state
- protocol and configuration versions
- system bookkeeping and audit metadata (without PHI payload)
- integration state (tokens stored securely, references only)

## Guardrails
- Do not mirror FHIR content into Cloud SQL.
- Encrypt in transit and at rest.
- Backups + point-in-time recovery must be enabled in production.
- Migrations are mandatory and reviewed.

## Operational notes
- connection pooling is required for Cloud Run workloads
- define indexes for hot query paths
- include runbooks for restore verification
