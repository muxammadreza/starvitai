---
description: Add a backend API endpoint safely
---

Add a backend endpoint safely.

1) Contract-first:
   - define request/response schema (Pydantic)
   - define endpoint classification (patient / clinician / research)
   - define error model and status codes
2) Security:
   - implement authN and authZ (object + property level)
   - add rate limiting / abuse controls for public surfaces
3) Implementation:
   - router is thin; call a service-layer function
   - use integration adapters (FHIR, Pub/Sub, BigQuery) behind interfaces
4) Auditability:
   - emit an audit event (and/or FHIR Provenance if PHI workflow relevant)
   - include correlation_id in logs, never PHI
5) Tests:
   - unit tests for service/domain logic
   - integration test for route using dependency overrides
6) Contract propagation:
   - ensure OpenAPI is correct
   - regenerate typed client if applicable
7) Quality gates:
   // turbo
   - Run `poetry run pytest -q`

Deliver: PR-ready diff + test evidence + audit event example + OpenAPI/client updates.
