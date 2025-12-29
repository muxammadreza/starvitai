# Security/Privacy Gate: Measurement Observations + derived GKI

Date: 2025-12-29
Scope: patient measurement endpoints, FHIR Observation writes/reads, derived metric computation.

## Checklist
1) Data classification
- PHI: yes (raw glucose/ketones/weight + derived GKI).
- PHI stays in Medplum: yes.

2) Medplum controls
- AccessPolicy/ProjectMembership required: yes (patient/clinician/backend service).
- Compartment scoping: patient uses profile compartment; clinician scoped via compartment policies.
- Auditability: Medplum AuditEvent expected for CRUD; Provenance written for derived metric.
- Binary/attachments: not used.

3) Threat model delta
- New attacker paths: measurement endpoints for patient role; potential misuse via forged patientId.
- New egress: none.
- SSRF: none.

4) App security baseline
- Input validation: schema + unit validation + timezone requirement.
- Access control: patient role only for endpoints; patientId bound to token in live mode.
- Error handling: 4xx with no PHI payloads.

5) Logging/telemetry
- Confirm no PHI in logs or traces.

6) Dependency changes
- None.

## Decision
Approved with mitigations:
- Add monitoring alert on spikes in measurement POST errors (4xx/5xx) once observability dashboard exists.
