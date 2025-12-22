---
description: Release readiness checks (operability, rollback, and verification)
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
