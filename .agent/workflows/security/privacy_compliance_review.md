---
description: Privacy/compliance review for PHI and de-identified flows
---

## When to use
Any new feature that touches patient data, consent, exports, analytics, or ML training.

## Steps
1) Data inventory:
   - what fields are collected
   - where they are stored
   - who can access
2) Boundary enforcement:
   - PHI zone vs de-ID zone
   - cross-zone transfer controls
3) De-identification:
   - DLP transformations
   - sampling audits and re-identification risk checks
4) Telemetry:
   - verify no PHI in logs/traces
5) Retention:
   - retention windows
   - deletion procedures

## Output
A privacy decision note + required mitigations.
