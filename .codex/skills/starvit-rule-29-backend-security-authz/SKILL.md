---
name: starvit-rule-29-backend-security-authz
description: Backend Security and Authorization Rules
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

## Medplum integration security
- Medplum is the PHI system of record. Do not mirror PHI into Starvit storage.
- For Medplum admin/config changes, use the configured Medplum MCP server.
- Medplum v5+ is strict FHIR; avoid non-standard search modifiers and deprecated Medplum resources (see `$starvit-rule-36-medplum-v5-non-deprecated`).

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
