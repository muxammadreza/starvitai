# Backend stack and engineering conventions

## What this backend is
Starvit's backend is a **Python 3.13 + FastAPI** modular monolith deployed to **Cloud Run**. It is the policy enforcement point for:
- PHI zone access (FHIR System of Record on GCP Healthcare API)
- derived metrics and protocol engine outputs (clinician-approved)
- auditability and provenance logging
- controlled research access to **de-identified** BigQuery/TigerGraph data

## Non-negotiables
- **No autonomous medical decisions.** All clinically-actionable outputs are flagged for clinician approval and logged.
- **PHI boundary is sacred.** PHI stays in the FHIR store; analytics/ML use de-identified data only.
- **Auditability first.** Inputs -> outputs -> model version -> clinician decision.

## Core libraries
- Web/API: FastAPI
- Models: Pydantic v2
- Settings: pydantic-settings
- HTTP client: httpx
- Retries/backoff: tenacity (or equivalent) for idempotent operations
- Observability: OpenTelemetry (traces) + structured JSON logs
- Quality gates: ruff, pyright/mypy, pytest

## GCP integrations
- Prefer official Google Cloud client libraries and ADC:
  - `google-auth` / `google-auth-httplib2` for credentials
  - Healthcare API: REST via authenticated HTTP client, or `google-api-python-client` where appropriate
  - Pub/Sub: `google-cloud-pubsub`
  - Secret Manager: `google-cloud-secret-manager`
- Do not ship credential files in containers; use Cloud Run service identity.

## High-level module boundaries
- `api/` HTTP, OpenAPI, dependencies
- `services/` application orchestration
- `domain/` pure domain logic
- `integrations/` GCP Healthcare API, Pub/Sub, BigQuery, Vertex AI
- `persistence/` internal state for non-PHI only (feature flags, job state, etc.)

## API contract discipline
- OpenAPI generated from FastAPI is the contract source of truth.
- Typed clients are generated from OpenAPI; do not hand-maintain duplicate TS types.

## Error model
Use a consistent JSON error envelope:
- `error_code` (stable)
- `message` (safe)
- `correlation_id` (request ID / trace link)
- optional `details` for non-sensitive diagnostics

## Testing strategy
- Unit tests for domain/services (fast)
- Integration tests for HTTP routes (FastAPI TestClient/httpx)
- Contract tests for OpenAPI changes (schema snapshot + client regeneration)
