---
trigger: always_on
---

# Starvit Backend Stack Rules (FastAPI/Python)

## Codebase structure
- Organize the backend as a **modular monolith** with explicit layers:
  - `api/routers/`: FastAPI routers (HTTP-only; no business logic)
  - `api/deps/`: dependency injection for auth, request IDs, tracing, sessions
  - `api/schemas/`: Pydantic request/response models
  - `services/`: application services and orchestrators
  - `domain/`: pure domain logic, types, and invariants
  - `integrations/`: outbound adapters (Medplum FHIR API, Pub/Sub, BigQuery, Vertex AI)
  - `persistence/`: internal stores for non-PHI configuration and state only
- Keep FHIR/PHI models separate from internal models. Never store PHI in internal databases.

## Libraries and defaults
- Web: FastAPI (Starlette) with Pydantic v2 models.
- Settings: `pydantic-settings` for configuration.
- HTTP clients: `httpx` for outbound calls.
- Retries: `tenacity` (or equivalent) with exponential backoff + jitter for safe/idempotent operations.
- Lint/format: `ruff`.
- Types: `pyright` (preferred) or `mypy`.
- Tests: `pytest` + FastAPI test utilities.

## Configuration discipline
- All configuration is read from environment variables (12-factor). Local development may use `.env`, but secrets must never be committed.
- Validate configuration at startup; fail fast if required environment variables are missing.

## Error model
- Use consistent JSON error responses with:
  - stable `error_code`
  - human-safe `message` (no secrets)
  - `correlation_id` (propagated from request ID)
- Never return raw exception strings or stack traces in production.

## Testing discipline
- Use `dependency_overrides` for auth/integration seams.
- Add a contract test when OpenAPI changes (schema snapshot and/or client regeneration).

## Quality gates
- Any backend PR must include:
  - passing unit tests
  - ruff format/lint passing
  - type check passing
  - dependency audit (where configured)
