# Release readiness: clinician approval workflow (2025-12-29)

## Preconditions
- Tests green (pytest).
- Security/privacy gate completed.

## Rollout strategy
- Standard deployment; no data migration.
- Monitor Task creation and approval error rates.

## Migration safety
- No schema migrations.
- No backfill required.

## Observability
- AuditEvent + Provenance emitted for proposal and decisions.
- Request IDs used for correlation.

## Access policy note
- Medplum AccessPolicy criteria do not allow chained dot notation (e.g., `Task?for:Patient.general-practitioner=%profile`).
- Current ClinicianPolicy scopes Tasks by `owner` and Provenance/AuditEvent by `agent`.
- Backend-created tasks must set `owner` to the clinician profile to appear in clinician queues (`Task?owner=%profile`).

## Runbooks
- Add troubleshooting notes for Task approval failures (Medplum write errors).

## Post-deploy verification
1) Create PlanDefinition → verify exists in Medplum.
2) Propose Task → verify Task status `requested`.
3) Approve Task → verify Task `completed` + Provenance + AuditEvent.
