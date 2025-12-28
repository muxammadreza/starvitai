---
name: starvit-rule-19-api-contracts-openapi
description: Starvit API Contract + Typed Client Rules
---

# Starvit API Contract + Typed Client Rules

## Contract source of truth

- Backend is **FastAPI**; OpenAPI schema is authoritative.
- Frontend does not hand-write request/response types for backend endpoints.

## Client generation (preferred)

- Use **Orval** to generate:
  - TypeScript models
  - HTTP client functions
  - Optional React Query hooks
  - Optional MSW mocks (for UI development without backend)

## Versioning + change management

- Any API change must include:
  - updated OpenAPI schema (automatic from FastAPI, but verify)
  - regenerated clients
  - backward-compat notes (breaking change vs additive)
  - integration tests for critical endpoints

## Safety

- Never expose internal/admin endpoints in generated clients unless they are intended for the given app surface.
- Enforce allowlists of endpoints per app when feasible (e.g., clinician vs research).

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
