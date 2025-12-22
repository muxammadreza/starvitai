---
description: Post-merge follow-ups to keep the system healthy
---

## Goal
Prevent drift after code merges.

## Steps
1) Verify CI artifacts (images, generated clients, schema outputs) are published as expected.
2) Ensure docs are updated:
   - architecture decision records (if any)
   - runbooks and dashboards
3) Confirm dependency/audit tasks:
   - SBOM/provenance generated if applicable
   - vulnerability scans completed
4) Record a short engineering note:
   - what changed
   - how to roll back
   - how to validate in staging/prod
