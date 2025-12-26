---
description: IAM/RBAC audit (least privilege verification)
---

## Steps
1) Enumerate principals
   - human users (clinicians, ops, developers)
   - machine identities (service accounts, CI/CD)

2) Map permissions across layers
   - **Medplum**: ProjectMembership roles + AccessPolicy criteria/compartments
   - Cloud/IaaS (if applicable): IAM roles, network access, secrets access
   - Starvit application RBAC (if present)

3) Identify risks
   - broad roles (admin everywhere)
   - cross-environment access
   - stale principals and unrotated secrets
   - policies that allow unconstrained FHIR search/read

4) Apply mitigations
   - narrow AccessPolicies; use compartment-based scoping
   - enforce environment separation (dev/stage/prod)
   - rotate secrets and remove stale access

5) Verify audit coverage
   - Medplum AuditEvent enabled and retained (or streamed) for access/change logging
   - Starvit operational audit events for non-PHI actions

## Output
- IAM/RBAC matrix and a remediation PR list.
