---
description: Quick entrypoint for routing work to the right workflow(s)
---

# Routing entrypoint (use this when you are unsure)

**Default move:** run the Router.
- `.agent/workflows/router.md`

The Router will:
- interpret the ask
- pick the smallest set of workflows that cover planning → build → gates → release
- apply always-on gates (security/privacy + release readiness)

## Fast lanes
Use these when you already know what you’re doing:

### A) Standard feature change
1) `.agent/workflows/00_triage_and_plan.md`
2) `.agent/workflows/02_implement_with_tests.md`
3) `.agent/workflows/03_security_privacy_gate.md`
4) `.agent/workflows/04_release_readiness.md`

### B) Dataflow / pipelines
- `.agent/workflows/data/add_pipeline_field.md`
- `.agent/workflows/03_security_privacy_gate.md`

### C) FHIR adapter / PHI boundary
- `.agent/workflows/backend/add_healthcare_fhir_adapter_operation.md`
- `.agent/workflows/03_security_privacy_gate.md`

### D) RBAC / authorization
- `.agent/workflows/frontend/add_rbac_guard.md`
- `.agent/workflows/security/iam_rbac_audit.md`

### E) Graph / ML research surface
- `.agent/workflows/graph/research_api_allowlist_change.md`
- `.agent/workflows/ml/inference_contract_check.md`

## Stop conditions
If any path might cross the PHI boundary or expand permissions, run:
- `.agent/workflows/critics/threat_model.md`
- `.agent/workflows/security/privacy_compliance_review.md`
