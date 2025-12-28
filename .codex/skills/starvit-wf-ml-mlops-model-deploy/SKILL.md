---
name: starvit-wf-ml-mlops-model-deploy
description: Deploy an ML model safely (Vertex AI aligned)
---

# Deploy an ML model safely (Vertex AI aligned)

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

## Steps
1) Register model with version metadata.
2) Validate inference contract.
3) Deploy to staging endpoint first.
4) Run regression + safety checks:
   - outputs within expected ranges
   - no PHI leakage
5) Rollout:
   - canary traffic split if supported
   - monitor latency/errors/drift
6) Update documentation:
   - model card
   - feature set docs

## Output
Safe model deployment with monitoring.

