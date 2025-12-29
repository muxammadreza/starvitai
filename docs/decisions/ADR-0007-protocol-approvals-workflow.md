# ADR-0007: Versioned ProtocolDefinitions + clinician approval workflow

Date: 2025-12-29
Status: Accepted

## Context
Starvit must ensure all protocol-driven recommendations remain clinician-supervised. We need a versioned protocol schema (with explicit approval-required steps) and an auditable, FHIR-native workflow for proposed actions, clinician review, and approval/rejection. This must avoid any autonomous treatment execution and provide immutable decision logs.

## Decision
- Use FHIR `PlanDefinition` as the versioned schema container for protocol steps (Medplum does not support `ProtocolDefinition` in this environment).
- Require each protocol definition to include at least one `approvalRequired` step via an explicit extension.
- Represent protocol recommendations as FHIR `Task` resources with `intent=proposal` and `status=requested`.
- Record clinician decisions via Task status transitions (`completed` for approve, `rejected` for reject) and FHIR `Provenance` with signature metadata and decision extensions.
- Emit FHIR `AuditEvent` records for proposal creation and clinician decisions.
- Provide API endpoints for propose → queue → approve/reject → decision log; no automated execution of treatment decisions.

## Consequences
- Clinician approvals are fully auditable in FHIR with task status, provenance, and audit trail.
- Protocol version changes are explicit and tied to recommendation tasks via `instantiatesCanonical`.
- Additional integration tests are required to validate approval workflow and audit emission.

## Alternatives considered
- Custom database tables for protocol and approvals. Rejected because it would duplicate PHI workflows outside Medplum and reduce FHIR-native auditability.
- Storing approvals solely as AuditEvent without Task/Provenance. Rejected because Task provides an explicit clinical workflow artifact and state transitions.
