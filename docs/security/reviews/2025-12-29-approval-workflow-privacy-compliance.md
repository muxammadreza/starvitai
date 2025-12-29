# Privacy/compliance review: clinician approval workflow

Date: 2025-12-29
Reviewer role: Privacy + compliance
Scope: plan definitions (protocol schema), clinician approval Tasks, decision provenance, audit logging.

## Data inventory
- Collected fields: protocol ID/version/title, recommendation text, rationale, decision status, clinician signature metadata, patient reference.
- Storage location: Medplum FHIR R4 (PlanDefinition, Task, Provenance, AuditEvent).
- Access: Clinician role (patient compartment), backend service role (service policy).

## Boundary enforcement
- PHI remains in Medplum (Task/Provenance/AuditEvent).
- No analytics/de-ID export in this change.

## De-identification
- Not applicable in this change.

## Telemetry
- No PHI logged; responses return IDs and metadata only.
- Correlation IDs only (opaque) in logs.

## Retention
- Decisions are clinical artifacts and should follow Medplum retention policy.

## Decision
Approved with mitigations:
- Confirm AccessPolicies include Task/Provenance/AuditEvent access scoped to clinician + patient compartments.
- Ensure recommendation/rationale fields remain within clinician-facing systems only.
