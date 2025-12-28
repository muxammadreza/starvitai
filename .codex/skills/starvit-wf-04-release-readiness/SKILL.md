---
name: starvit-wf-04-release-readiness
description: Before deploying any backend, UI, pipeline, or ML model change to production.
---

## When to use
Before deploying any backend, UI, pipeline, or ML model change to production.

## Preconditions
- tests are green
- security/privacy gate completed for medium/high risk

## Checks
1) Rollout strategy:
   - canary or staged rollout
   - feature flags (if applicable)
   - rollback path is documented and validated
2) Migration safety:
   - DB migrations are reversible where possible
   - backfill plan exists and is tested on staging
3) Observability:
   - dashboards updated
   - alerts aligned with SLOs
4) Runbooks:
   - updated with new failure modes

## Output
Release plan with post-deploy verification steps.

---

**Codex usage notes:**
- Use this workflow skill to execute the step sequence as written.
- Produce the specified deliverables explicitly (plans, ADRs, checklists, etc.).
