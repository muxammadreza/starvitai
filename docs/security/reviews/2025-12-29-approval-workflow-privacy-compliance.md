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

---

# Privacy/compliance review: de-identification pipeline scaffold

Date: 2025-12-29  
Reviewer role: Privacy + compliance  
Scope: synthetic-only de-id transformer scaffold, boundary contract, schema proposal.

## Data inventory
- Collected fields: synthetic Observation-like fields (code, value, effective time) and pseudonymous patient key.
- Storage location: none in stub; proposed BigQuery `analytics.deid_observations` (de-ID zone).
- Access: stub only; production access to be governed by dataset IAM + policy tags.

## Boundary enforcement
- PHI remains in Medplum; stub has no Medplum/BigQuery IO.
- Stub requires `APP_ENV` in `dev|test|local` and `STARVIT_MODE=stub`.

## De-identification
- Allowlisted fields only; direct identifiers are not emitted.
- Pseudonymous `patient_key` derived within transformer boundary.

## Telemetry
- Log only `run_id`, counts, and version metadata.
- No PHI in logs/traces.

## Retention
- Stub does not persist data.
- Production retention to follow de-ID dataset retention policy.

## Decision
Approved with mitigations:
- Formalize DLP policy + policy tags before any production export.
- Require access policy review before enabling Medplum → BigQuery IO.
