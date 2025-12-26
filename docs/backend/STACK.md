# Backend stack and engineering conventions

## What this backend is
Starvit's backend is a **Python 3.13 + FastAPI** modular monolith (deployment target is environment-dependent: VPS, Cloud Run, etc.). It is the policy enforcement point for:
- integrating with the **Medplum PHI system of record** (FHIR R4)
- derived metrics and protocol-engine outputs (always clinician-approved)
- auditability and provenance logging
- controlled research access to **de-identified** BigQuery/TigerGraph data

## Non-negotiables
- **No autonomous medical decisions.** All clinically-actionable outputs are flagged for clinician approval and logged.
- **PHI boundary is sacred.** PHI stays in the FHIR store; analytics/ML use de-identified data only.
- **Auditability first.** Inputs -> outputs -> model/protocol version -> clinician decision.

## Core libraries
- Web/API: FastAPI
- Models: Pydantic v2
- Settings: pydantic-settings
- HTTP client: httpx
- Retries/backoff: tenacity (or equivalent) for idempotent operations
- Observability: OpenTelemetry (traces) + structured JSON logs
- Quality gates: ruff, pyright/mypy, pytest

## Primary integration: Medplum
- Treat Medplum as the canonical PHI datastore and identity provider.
- Use OAuth2:
  - Authorization Code flow for interactive apps
  - Client Credentials for machine-to-machine workers
- Use AccessPolicy + ProjectMembership as the authorization perimeter.

## Optional cloud integrations (de-identified zone)
- BigQuery / TigerGraph / Vertex AI are de-identified only.
- If using managed cloud services, prefer workload/instance identity and managed secret stores.

## High-level module boundaries
- `api/` HTTP, OpenAPI, dependencies
- `services/` application orchestration
- `domain/` pure domain logic
- `integrations/` Medplum, BigQuery, Vertex AI, TigerGraph, etc.
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

## Medplum runbook
See `docs/backend/MEDPLUM_CONFIGURATION.md`.
