# Threat model — Backend authz + Medplum role mapping (2025-12-29)

## Dataflow (high level)
- Actors: patient app, clinician app, research app, backend service.
- Trust boundaries: public clients → Starvit API → Medplum API.
- Data stores: Medplum FHIR (PHI), de-ID stores (BigQuery/TigerGraph).

## Key threats (STRIDE + LINDDUN)
1) **Elevation of privilege**: incorrect role mapping → unintended PHI access.
2) **Information disclosure**: PHI endpoints accessible to research role.
3) **Spoofing**: forged tokens accepted by backend.
4) **Denial of service**: `/auth/me` dependency becomes a bottleneck.

## Mitigations
- Enforce JWKS validation, issuer, and audience for tokens.
- Resolve role via AccessPolicy; deny if unmapped.
- Explicit role allowlists on every PHI endpoint.
- Configure policy IDs/names per environment; avoid ambiguous mapping.

## Test cases (top risks)
- Research role → PHI endpoint → expect 403.
- Clinician role → patient-only endpoint → expect 403.
- Patient role → clinician endpoint → expect 403.
- Invalid/missing token → expect 401.
