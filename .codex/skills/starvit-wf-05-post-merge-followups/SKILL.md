---
name: starvit-wf-05-post-merge-followups
description: Prevent drift after code merges.
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

---

**Codex usage notes:**
- Use this workflow skill to execute the step sequence as written.
- Produce the specified deliverables explicitly (plans, ADRs, checklists, etc.).
