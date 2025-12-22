---
description: Change management and release planning (DORA/SRE aligned)
---

## When to use
For any production release affecting clinical workflows, PHI boundary, data pipelines, or model behavior.

## Steps
1) Change record:
   - what is changing (code/config/data/model)
   - blast radius (which users/services)
   - expected impact
2) Deployment strategy:
   - canary revision
   - feature flag plan
   - rollback trigger criteria
3) Verification plan:
   - synthetic checks
   - real-user monitoring signals
   - data integrity checks (pipelines)
4) Communication:
   - internal announcement (engineering + clinical)
   - incident channel and on-call assignment
5) Metrics tracking:
   - capture DORA four keys inputs (deploy, change, incident)

## Output
A release runbook: steps + go/no-go criteria.
