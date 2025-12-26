---
trigger: always_on
---

## Backend Platform Engineer Rules

### Architectural constraints
- Enforce modular monolith boundaries (no ad-hoc microservices).
- Treat **PHI as toxic**: PHI may only be persisted in the FHIR System of Record (Medplum). Never copy PHI into analytics stores, caches, or logs.
- De-identified research/ML data only flows **FHIR (Medplum) → DLP de-id → BigQuery → TigerGraph**.

### Starvit backend stack (authoritative)
- Framework: **FastAPI** (OpenAPI is the contract source of truth).
- Runtime: **Python 3.13** + **Poetry**.
- Production server: **Gunicorn + Uvicorn worker** (do not ship `--reload`).
- Observability: **OpenTelemetry** traces + structured logs; include correlation IDs.

### Endpoint quality bar (non-negotiable)
Every endpoint MUST define and implement:
1) authN: how identity is established (JWT/OIDC, service-to-service identity token, etc.)
2) authZ: role + scope checks (object- and property-level), including tenant boundary
3) validation: request schema, units, enums/terminologies, size limits
4) safety: rate limiting / abuse controls for public surfaces
5) auditability: audit event emitted (and/or FHIR Provenance where applicable)
6) errors: consistent error model (no raw stack traces); deterministic status codes
7) tests: unit + integration tests; contract test for OpenAPI changes

### Integration discipline
- Any PHI read/write MUST go through the approved **FHIR integration layer**; no side channels.
- All outbound HTTP calls must be allowlisted and time-bounded to reduce SSRF/exfiltration risk.
- If running on managed cloud, use workload/instance identity; never commit static creds or mount `GOOGLE_APPLICATION_CREDENTIALS` into runtime.

### Change management
- Public contracts MUST be versioned; breaking changes require migration + deprecation plan.
- Prefer idempotent operations; use explicit request/correlation IDs in logs.

### Required reading when making backend changes
- `docs/backend/STACK.md`
- `docs/backend/SECURITY.md`
- `docs/backend/DEPLOYMENT_CLOUD_RUN.md`
- `docs/backend/ASYNC_JOBS_ETL.md`
