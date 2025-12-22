---
description: Triage the request, clarify scope, and produce an implementation plan
---

## When to use
Use this before any non-trivial implementation, especially when the change touches PHI, auth, data pipelines, or ML/graph layers.

## Inputs
- user request / ticket
- relevant internal docs (architecture, security, data, clinical)

## Outputs
- problem statement + success criteria
- scope boundaries (in/out)
- risk tier (low/medium/high)
- execution plan broken into PR-sized steps

## Steps
1) Restate the goal as an acceptance-testable outcome.
2) Identify impacted surfaces:
   - UI (clinician/research/patient)
   - backend module
   - PHI zone vs de-ID zone
   - pipelines/ML/graph
3) Identify key risks and required gates:
   - security/privacy gate
   - data migration/backfill
   - clinical safety review
4) Propose an implementation plan:
   - interfaces first (schemas/contracts)
   - tests to write
   - roll-out strategy
5) Produce a "Definition of Done" checklist.
