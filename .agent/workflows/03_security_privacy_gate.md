---
description: Security and privacy gate (mandatory for medium/high risk changes)
---

## When to use
Run for any change that touches: PHI boundary, auth/RBAC, external integrations, data export, ML/agent actions, or pipeline cross-zone movement.

## Checklist
1) Data classification
   - Does this touch PHI (direct or derived)?
   - Confirm PHI stays in Medplum; confirm any analytics output is de-identified.

2) Medplum controls
   - Access control:
     - AccessPolicy / ProjectMembership rules updated and tested
     - Compartment-based scoping validated (patient/self, clinician scope, backend scope)
   - Auditability:
     - Medplum AuditEvent persistence enabled (or an explicit documented alternative)
     - Starvit creates FHIR-native workflow artifacts for approvals (Task/Provenance/AuditEvent)
   - Binary/attachments:
     - securityContext enforced; no “public file bucket” patterns

3) Threat model delta
   - What new attacker paths exist?
   - Any new network egress? Any SSRF risk?

4) App security baseline
   - input validation
   - access control (object + property level)
   - secure error handling (no PHI in error payloads)

5) Logging/telemetry
   - confirm no PHI in logs/traces
   - confirm trace/log correlation uses opaque IDs

6) Dependency changes
   - run supply-chain intake for new deps

7) Decide
   - approve, approve-with-mitigations, or block.

## Output
A short written security decision note (1–2 pages max) with required mitigations.
