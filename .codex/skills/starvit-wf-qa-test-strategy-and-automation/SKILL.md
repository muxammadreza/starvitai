---
name: starvit-wf-qa-test-strategy-and-automation
description: Create/refresh the testing strategy and automation plan
---

# Create/refresh the testing strategy and automation plan

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

## Steps
1) Identify critical user journeys and safety-critical flows.
2) Choose test layers:
   - unit (fast)
   - integration (boundaries)
   - contract (API)
   - e2e (smoke)
3) Define coverage targets:
   - PHI boundary
   - RBAC enforcement
   - pipeline correctness
   - model inference contract
4) CI plan:
   - fast tests on PR
   - nightly longer suites
5) Flake management:
   - quarantine policy and remediation ownership.

## Output
`docs/testing/strategy.md` and CI checklist.

