# Release readiness: AuditEvent logging (2025-12-29)

## Preconditions
- Tests green (pytest).
- Security/privacy gate completed.

## Rollout strategy
- Standard deployment; no data migration.
- Monitor FHIR write latency and error rates.

## Migration safety
- No schema migrations.
- No backfill required.

## Observability
- Request ID header added for correlation.
- AuditEvents visible in Medplum; verify in staging.

## Runbooks
- Update runbooks if AuditEvent creation errors occur (Medplum write failures).

## Post-deploy verification
1) Create measurement → verify AuditEvent + Provenance present.
2) Update measurement → verify AuditEvent + Provenance present.
3) Clinician approve Task → verify AuditEvent + Provenance present.
