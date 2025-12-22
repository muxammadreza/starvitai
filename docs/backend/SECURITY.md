# Backend security

## Threat model (minimum)
- Broken object level authorization / tenant boundary breaks
- Broken property level authorization / mass assignment
- Excessive data exposure (returning more than needed)
- SSRF via URL fetches / metadata server access
- Credential leakage via logs

## Authorization rules
- AuthZ is enforced server-side on every request.
- Do object-level checks (tenant/patient/cohort) and property-level checks (field-level updates/reads).

## Input handling
- Validate schemas, size limits, and allowed values.
- Do not bind raw JSON to ORM/entities.

## Secrets
- Use Secret Manager. No secrets in repo.

## Logging
- Never log PHI.
- Include correlation IDs.
