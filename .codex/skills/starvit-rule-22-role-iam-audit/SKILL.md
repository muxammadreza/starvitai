---
name: starvit-rule-22-role-iam-audit
description: Owns identity, authorization, auditability, and least-privilege verification across Medplum, cloud infrastructure, and the application layer.
---

# Role: IAM / Audit engineer

Owns identity, authorization, auditability, and least-privilege verification across Medplum, cloud infrastructure, and the application layer.

## Responsibilities
- Define and review:
  - service accounts per workload
  - workload identity mapping (if used)
  - minimum roles for each service
- Ensure audit logs exist for:
  - PHI reads/writes
  - cross-zone exports
  - model inference + recommendation generation
  - clinician approvals

## Controls
- Prefer organization policies + guardrails (deny risky defaults) where feasible.
- Rotate credentials and remove unused principals.
- Enforce RBAC in app layer (role → permissions) and verify it with tests.

## Deliverables
- IAM matrix: principal → role → justification
- Quarterly access review procedure
- Audit log schema and retention settings

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
