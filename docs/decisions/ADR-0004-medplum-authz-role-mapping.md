# ADR-0004: Medplum-authenticated role mapping and backend authz

## Status
Accepted (2025-12-29)

## Context
Starvit uses Medplum as the PHI system of record and identity provider. The backend must:
- authenticate users and services via Medplum OAuth2/OIDC,
- map Starvit roles (patient/clinician/research/backend-service) to Medplum ProjectMembership + AccessPolicy,
- enforce authorization at the API boundary (in addition to Medplum’s own AccessPolicy enforcement),
- avoid PHI duplication outside Medplum.

We also need a clear service-to-service auth flow for backend workers.

## Decision
1) **AuthN source of truth**: Medplum OAuth2/OIDC.
   - Human users: Authorization Code flow (patient/clinician apps).
   - Service accounts: Client Credentials flow (backend service).

2) **Role mapping**: Backend resolves role via **Medplum AccessPolicy** attached to ProjectMembership.
   - The API calls Medplum `/auth/me` with the bearer token to obtain `projectMembership` and `accessPolicy`.
   - AccessPolicy identifiers (name or ID) are mapped to Starvit roles via environment configuration:
     - `MEDPLUM_POLICY_PATIENT`
     - `MEDPLUM_POLICY_CLINICIAN`
     - `MEDPLUM_POLICY_RESEARCH`
     - `MEDPLUM_POLICY_BACKEND_SERVICE`
   - Patient tokens may be inferred by `profile` reference (`Patient/...`) only as a fallback.

3) **API boundary enforcement**:
   - Every PHI endpoint requires a specific role (patient/clinician/backend-service).
   - Research endpoints are de-identified; researcher role is blocked from PHI endpoints.

4) **PHI storage**: All PHI read/write goes through the Medplum FHIR base URL; no PHI is stored in app databases.

## Consequences
- Each request in live mode may call Medplum `/auth/me` to resolve access policy → adds latency but guarantees authoritative role mapping.
- Role mapping is explicit and auditable via AccessPolicy attachments in Medplum.
- Service-to-service access is handled by Medplum client credentials; internal API keys are not required for PHI paths.
- New configuration is required in each environment (policy IDs or names).

## Alternatives considered
1) **JWT-only role claims** (no `/auth/me` call).
   - Rejected: role claims drift from Medplum ProjectMembership changes.
2) **Profile-type only** (Patient vs Practitioner).
   - Rejected: cannot distinguish clinician vs researcher vs backend service.
3) **Internal API key for services**.
   - Rejected: bypasses Medplum policy boundary and reduces auditability.

## Links
- PR: (add link)

## Rollout plan
1) Deploy backend with role mapping enabled.
2) Configure AccessPolicy identifiers per environment.
3) Validate access via integration tests and Medplum audit logs.
