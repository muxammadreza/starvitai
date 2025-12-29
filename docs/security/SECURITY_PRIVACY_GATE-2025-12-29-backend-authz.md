# Security/Privacy Gate — Backend authz + Medplum role mapping (2025-12-29)

## 1) Data classification
- Touches PHI boundary (FHIR access via Medplum).
- PHI remains in Medplum; no PHI stored in app databases.

## 2) Medplum controls
- Access control: AccessPolicy + ProjectMembership required and mapped to Starvit roles.
- Compartment-based scoping is enforced in Medplum policies (patient/self, clinician scope, backend scope).
- Auditability: Medplum AuditEvent is the canonical audit trail (verify retention in ops).
- Binary/attachments: No change; still gated by Medplum `securityContext`.

## 3) Threat model delta
- New risk: role mapping depends on AccessPolicy IDs/names and `/auth/me` availability.
- Mitigation: explicit env mapping + deny-by-default if role is unmapped.

## 4) App security baseline
- Input validation remains in place.
- Role-based checks enforced at API boundary.
- Errors avoid returning PHI.

## 5) Logging/telemetry
- No PHI added to logs; tokens are not logged.

## 6) Dependencies
- No new third-party dependencies.

## Decision
Approved with mitigations:
- Configure policy ID/name mappings per environment.
- Monitor `/auth/me` latency and failure rates.
