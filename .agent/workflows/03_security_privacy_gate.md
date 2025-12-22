---
description: Security and privacy gate (mandatory for medium/high risk changes)
---

## When to use
Run for any change that touches: PHI boundary, auth/RBAC, external integrations, data export, ML/agent actions, or pipeline cross-zone movement.

## Checklist
1) Data classification: does this touch PHI? If yes, how is it contained?
2) Threat model delta:
   - what new attacker paths exist?
   - what new assets are exposed?
3) App security baseline:
   - input validation
   - access control
   - secure error handling
4) Logging/telemetry:
   - confirm no PHI
   - confirm trace/log correlation is safe
5) Dependency changes:
   - run supply-chain intake for new deps
6) Decide: approve, approve-with-mitigations, or block.

## Output
A short written security decision note (1–2 pages max) with required mitigations.
