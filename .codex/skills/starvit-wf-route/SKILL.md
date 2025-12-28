---
name: starvit-wf-route
description: Default move -> run the Router -> `$starvit-wf-router`
---

# Routing entrypoint (use this when you are unsure)

**Default move:** run the Router.
- `$starvit-wf-router`

The Router will:
- interpret the ask
- pick the smallest set of workflows that cover planning → build → gates → release
- apply always-on gates (security/privacy + release readiness)

## Fast lanes
Use these when you already know what you’re doing:

### A) Standard feature change
1) `$starvit-wf-00-triage-and-plan`
2) `$starvit-wf-02-implement-with-tests`
3) `$starvit-wf-03-security-privacy-gate`
4) `$starvit-wf-04-release-readiness`

### B) Dataflow / pipelines
- `$starvit-wf-data-add-pipeline-field`
- `$starvit-wf-03-security-privacy-gate`

### C) FHIR adapter / PHI boundary
- `$starvit-wf-backend-add-healthcare-fhir-adapter-operation`
- `$starvit-wf-03-security-privacy-gate`

### D) RBAC / authorization
- `$starvit-wf-frontend-add-rbac-guard`
- `$starvit-wf-security-iam-rbac-audit`

### E) Graph / ML research surface
- `$starvit-wf-graph-research-api-allowlist-change`
- `$starvit-wf-ml-inference-contract-check`

## Stop conditions
If any path might cross the PHI boundary or expand permissions, run:
- `$starvit-wf-critics-threat-model`
- `$starvit-wf-security-privacy-compliance-review`

---

**Codex usage notes:**
- Use this workflow skill to execute the step sequence as written.
- Produce the specified deliverables explicitly (plans, ADRs, checklists, etc.).
