# Release readiness: measurement ingestion + derived GKI

Date: 2025-12-29
Scope: patient measurement endpoints and FHIR Observation mapping.

## Preconditions
- Tests green (unit + integration).
- Security/privacy gate completed.

## Rollout strategy
- Staged rollout (dev → staging → prod).
- No feature flags required; endpoints are patient-scoped.

## Migration safety
- No database migrations.
- No backfill required.

## Observability
- Ensure request/response logging excludes PHI payloads.
- Monitor 4xx/5xx rates on:
  - POST /api/patient/measurements
  - GET /api/patient/measurements/recent
  - GET /api/patient/measurements/gki

## Runbooks
- Mapping spec and failure checks in `docs/backend/MEASUREMENT_MAPPING.md`.

## Post-deploy verification
1) Submit a synthetic measurement in staging and confirm four Observations + one Provenance created.
2) Query recent measurements and GKI trend in staging.
3) Verify Medplum AuditEvent entries for creation.
