---
description: Write design note and ADR for a change
---

Before starting:
- Confirm the PHI boundary implications (PHI vs de-identified).
- Confirm Antigravity safety posture: terminal auto-execution policy and browser allowlist are appropriate for this task.
- If touching auth/RBAC, PHI boundaries, protocol logic, ML inference, migrations, or deployments: request explicit human review.

Create a short design note and (if architectural) an ADR.

Include:
- Context + problem statement
- Options considered (>=2) with tradeoffs
- Chosen approach + why
- Data contracts (API/FHIR/feature tables)
- Security + PHI boundary analysis
- Rollout/rollback plan
- Testing + observability plan
Output:
- docs/rfcs/<slug>.md (if needed)
- docs/adrs/ADR-<date>-<slug>.md (if needed)
