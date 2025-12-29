# Medplum configuration checklist (Starvit)

This document is a runbook-style checklist for configuring Medplum so Starvit can rely on it as the PHI system of record.

## Starvit dev endpoints
- API: https://api.medplum.starvit.ca
- App: https://app.medplum.starvit.ca/
- FHIR base (expected): https://api.medplum.starvit.ca/fhir/R4
  - Verify with: `GET /fhir/R4/metadata` (should return a CapabilityStatement)

## Required Medplum server settings
1) Base URLs
- Set `baseUrl` to the public API base URL.
- Set `appBaseUrl` to the public app URL.

2) Auditability
- Enable server-side persistence of AuditEvents (so read/write actions are traceable).
- Decide whether AuditEvents are additionally emitted to logs and whether they should be redacted.

3) Email/SMS (optional)
- For prod, configure email delivery for user onboarding and password reset.

4) Secrets
- Use Medplum Project Settings/secrets for integration keys (preferred for bots).
- Never commit secrets to the repo.

5) Version compatibility
- Starvit assumes **Medplum v5.0.10+**.
- Do not use deprecated APIs and SDK patterns (see `docs/backend/MEDPLUM_V5_COMPAT.md`).

6) Administrative changes
- All Medplum admin/config changes for Starvit MUST be performed via the configured **Medplum MCP server** (see `docs/backend/MEDPLUM_MCP_SERVER.md`).

## Required Medplum project setup
- Create Projects per environment (`dev`, `stage`, `prod`).
- Create ClientApplications:
  - `starvit-backend` (machine access)
  - `starvit-clinician-web` (human access)
  - `starvit-patient-mobile` (human access)
- Define and apply AccessPolicies (see `docs/security/access-policies/`).

### Project feature flags (recommended for MVP)
Enable on the Starvit project as needed:
- `bots` (server-side workflows)
- `cron` (scheduled bots)
- `transaction-bundles` (FHIR transaction bundles; beta; requires retry logic)

### Project/system settings (recommended)
- `redactAuditEvents`: consider enabling in production to reduce PHI in logs while preserving traceability.
- Rate limit settings (`rateLimit`, `authRateLimit`) should be configured per environment.

## Starvit-side integration guardrails
- Never log FHIR resources or raw payloads.
- Store “approvals” and clinical workflow artifacts in FHIR where feasible (Task/Provenance).
- If any non-PHI event log is stored outside FHIR, it must not contain patient identifiers or clinical values.

## Backend role mapping (required)
Starvit resolves roles via Medplum ProjectMembership + AccessPolicy. Configure:
- `MEDPLUM_AUTH_ME_URL` (e.g., `https://api.medplum.starvit.ca/auth/me`)
- AccessPolicy identifiers (names or IDs, comma-separated):
  - `MEDPLUM_POLICY_PATIENT`
  - `MEDPLUM_POLICY_CLINICIAN`
  - `MEDPLUM_POLICY_RESEARCH`
  - `MEDPLUM_POLICY_BACKEND_SERVICE`

These should map to the AccessPolicies applied to ProjectMemberships for patient/clinician/research/backend principals.
