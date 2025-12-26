# Backend security

This document covers Starvit backend security posture and how it composes with Medplum.

## Threat model (minimum)
- Broken object-level authorization / tenant boundary breaks
- Broken property-level authorization / mass assignment
- Excessive data exposure (returning more than needed)
- SSRF via URL fetches (credential exfiltration risk)
- Token leakage via logs, analytics, crash dumps
- Insecure webhooks / subscription endpoints

## AuthN
- Primary auth is via **Medplum OAuth2/OIDC**.
- Interactive apps: Authorization Code flow.
- Machine-to-machine: Client Credentials flow.
- Never place Medplum client secrets in frontend code.

## AuthZ
- Medplum AccessPolicy is the first line of defense.
- Starvit backend must not widen access: enforce **server-side authorization** on every request:
  - object-level checks (patient/organization/tenant boundary)
  - property-level checks (which fields may be read/changed)
- Treat all FHIR IDs as sensitive; do not expose broad search capability without guardrails.

## Input handling
- Validate schemas, size limits, and allowed values.
- Do not bind raw JSON into domain entities without explicit mapping.

## Secrets
- Prefer managed secret stores (or Medplum Bot Secrets when running in Bot runtime).
- No secrets in repo; no secrets in CI logs.

## Logging and observability
- Never log PHI or full FHIR resources.
- Strip/redact:
  - Authorization headers
  - request/response bodies
  - identifiers that can be joined back to a person (unless strictly necessary and approved)
- Include correlation IDs and trace IDs.

## Webhooks/subscriptions
- Verify signatures or shared secrets where supported.
- Allowlist source IPs/hosts where possible.
- Use idempotency keys and replay protection.
