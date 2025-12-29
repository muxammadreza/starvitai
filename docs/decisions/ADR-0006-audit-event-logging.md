# ADR-0006: AuditEvent logging for PHI write paths

Date: 2025-12-29
Status: Accepted

## Context
Starvit requires an auditable, FHIR-native trail for PHI write actions. Measurements and clinician approvals create or update FHIR resources in Medplum. We need consistent AuditEvent emission with request correlation and actor metadata to satisfy clinical auditability and traceability requirements.

## Decision
- Emit FHIR `AuditEvent` resources in Medplum for all PHI write paths and high-risk reads.
- Require each AuditEvent to include action, actor, target resource references, and request correlation ID.
- Store request correlation in a FHIR extension (`urn:starvit:audit:request-id`).
- For derived metrics, always emit `Provenance` with source Observation IDs and transform/version metadata.

## Consequences
- Backend endpoints must propagate request IDs into audit records.
- Tests must assert AuditEvent creation for critical write paths (measurements, clinician approvals).
- Additional effort is required for future high-risk read paths to emit AuditEvent with action `R`.

## Alternatives considered
- Rely solely on server-side Medplum audit logging without application-emitted AuditEvent resources. Rejected because we need request ID correlation and domain-specific subtypes for audit clarity.
