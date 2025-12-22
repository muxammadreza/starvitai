---
trigger: always_on
---

# Backend Security and Authorization Rules

## Authorization model
- Enforce authorization at two levels:
  1) object-level: tenant, patient, cohort, protocol ownership
  2) property-level: which fields can be read/updated (prevent mass assignment)
- Never rely on the frontend to enforce authZ.

## Input handling
- Validate all inputs (schema, size limits, allowed enums, terminology codes).
- Never bind raw request JSON directly into internal objects or ORM models.

## OWASP API security
- Default-deny: return only the minimum properties required for the endpoint.
- Never expose internal IDs, IAM info, or debug diagnostics on public endpoints.

## Logging and errors
- No PHI in logs.
- Errors must be deterministic and safe; no stack traces in responses.

## Abuse prevention
- Rate limit unauthenticated or internet-facing endpoints.
- Apply SSRF controls for any endpoint that fetches URLs: allowlist domains, enforce timeouts, block link-local/metadata IP ranges.
