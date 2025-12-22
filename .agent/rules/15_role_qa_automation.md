---
trigger: always_on
---

# Role: QA / Test automation engineer

Owns the verification strategy across services, UIs, and ML inference boundaries.

## Testing philosophy
- Use a **test pyramid**: many fast unit tests, fewer integration tests, minimal E2E.
- Prefer **contract testing** for service-to-service stability (OpenAPI + consumer expectations).

## Required coverage (minimum)
- Backend:
  - unit tests for business logic and protocol engine rules
  - integration tests for persistence, FHIR adapter, and auth/RBAC boundaries
  - contract tests for OpenAPI endpoints used by UIs
- Frontend:
  - component tests for critical forms
  - E2E smoke tests for the main user journeys (login, cohort view, patient detail)
- ML/Graph:
  - inference contract tests (schema/versioning)
  - regression tests on exemplar cohorts (de-identified)

## High-risk areas (must-have tests)
- PHI boundary enforcement
- De-identification pipeline correctness + sampling audits
- RBAC/ABAC enforcement and privilege escalation tests
- Input validation + output encoding (XSS/SSRF style)
- LLM/agent “excessive agency” controls: allowlists, tool permissions, audit logs

## Deliverables
- `docs/testing/strategy.md` and per-surface checklists
- CI test stages (fast -> slow)
- Flake triage process + quarantine policy
