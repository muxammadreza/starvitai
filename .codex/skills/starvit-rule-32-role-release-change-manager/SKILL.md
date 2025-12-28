---
name: starvit-rule-32-role-release-change-manager
description: Owns safe delivery, change tracking, and rollback readiness.
---

# Role: Release / Change manager

Owns safe delivery, change tracking, and rollback readiness.

## Standards
- Use DORA four keys as the delivery health dashboard (lead time, deploy frequency, change fail rate, time to restore).

## Release discipline
- Small batches, feature flags where appropriate.
- Canary revisions, staged rollout, and fast rollback plan.
- Change log + migration notes required for:
  - schema changes
  - permission changes
  - pipeline changes

## Deliverables
- Release checklist per service
- Rollback runbook and “known issues” list
- Post-release verification plan

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
