---
description: Bootstrap a new FastAPI feature module with correct layering, tests, and docs
---

1) Identify the new capability and map it to a domain boundary (protocol engine, PHI gateway, research API, ETL worker).
2) Create or update the module skeleton:
   - `domain/<feature>/` (types, invariants, pure logic)
   - `services/<feature>/` (orchestrator)
   - `api/schemas/<feature>.py` (Pydantic IO)
   - `api/routers/<feature>.py` (router; thin HTTP)
3) Wire dependencies through `api/deps/`:
   - authN/authZ dependency
   - request ID / correlation dependency
   - integration adapters (FHIR, Pub/Sub, BigQuery) via interfaces
4) Add tests:
   - unit tests for domain + services
   - integration test for the router using dependency overrides
5) Update relevant docs:
   - `docs/backend/STACK.md` if new patterns/libraries were introduced
   - `docs/backend/SECURITY.md` if threat surface changed
6) Quality gates:
   // turbo
   - Run `poetry run ruff format`
   // turbo
   - Run `poetry run ruff check`
   // turbo
   - Run `poetry run pytest -q`
7) Deliver: PR-ready diff + test output + short ADR note if a new dependency or cross-cutting pattern was introduced.
