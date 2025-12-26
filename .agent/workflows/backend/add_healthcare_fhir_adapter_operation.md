---
description: Add a new operation to the Medplum FHIR adapter
---

# Add a Medplum FHIR adapter operation

## When to use
Use this workflow when the Starvit backend needs a new Medplum FHIR interaction, such as:
- create/update an Observation (e.g., GKI)
- query Observations/Conditions/MedicationRequests
- write clinical workflow artifacts (Task, Communication, ServiceRequest)

## Inputs
- Operation name (e.g., `create_gki_observation`)
- Resource types touched
- Auth context:
  - on-behalf-of user (interactive request), or
  - machine-to-machine (client credentials)
- Required constraints (tenant boundary, patient scope)

## Outputs
- New/updated method in the Medplum FHIR adapter
- Unit/integration tests for the operation
- Documentation update (if a new resource type or pattern is introduced)

## Steps
1. **Confirm PHI boundary**
   - Ensure the new operation writes/reads only via Medplum.
   - Confirm no PHI is persisted in Starvit Postgres, logs, analytics, or message queues.

2. **Add/extend adapter interface**
   - Add a strongly-typed method signature.
   - Prefer passing:
     - `patient_id` (FHIR id) and `project_id`/tenant context
     - a minimal request DTO
   - Return the minimal fields required for downstream logic (usually FHIR `id`, `meta.versionId`, and status).

3. **Implement OAuth2 handling**
   - Interactive: accept a bearer token from the caller context (do not re-issue tokens server-side unless explicitly required).
   - Machine: use client credentials to mint short-lived tokens and cache them until expiry.

4. **Implement the FHIR call**
   - Use the canonical FHIR base URL (`<MEDPLUM_BASE_URL>/fhir/R4`).
   - Prefer idempotent patterns:
     - conditional create/update when appropriate
     - optimistic concurrency via ETag / `meta.versionId`
   - For multi-resource writes, prefer a FHIR transaction bundle.

5. **Guardrails**
   - Enforce server-side authorization checks (object-level + property-level) before calling Medplum.
   - Allowlist query parameters for searches; avoid exposing broad `?_query=` patterns.

6. **Tests**
   - Add unit tests for request mapping and validation.
   - Add an integration test stub that can run against a local/dev Medplum:
     - `GET /fhir/R4/metadata` health check
     - create minimal Patient + Observation, verify read-back

7. **Observability**
   - Add tracing spans for the operation with safe attributes only (no payloads).
   - Include correlation id propagation.

## Quality gates
```bash
# // turbo
pnpm lint
pnpm test

# backend (if Python)
poetry run ruff check .
poetry run pytest
```
