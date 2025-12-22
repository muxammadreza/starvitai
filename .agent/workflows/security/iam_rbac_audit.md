---
description: IAM/RBAC audit (least privilege verification)
---

## Steps
1) Enumerate principals:
   - users/groups
   - service accounts
2) Map permissions:
   - GCP IAM roles
   - application RBAC roles
3) Identify risks:
   - broad roles (Owner/Editor)
   - cross-environment access
   - unused principals
4) Apply mitigations:
   - narrow roles
   - add conditions
   - rotate keys and remove stale access
5) Add/confirm audit logs for sensitive actions.

## Output
IAM matrix and a remediation PR list.
