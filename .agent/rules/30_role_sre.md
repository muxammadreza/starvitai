---
trigger: always_on
---

# Role: SRE / Reliability engineer

Owns reliability, operational readiness, and incident learning.

## SLO-first operations
- Define SLIs/SLOs per critical service (API latency, error rate, availability).
- Use error budgets to balance feature velocity and reliability work.

## Incident management
- Runbooks per service: common failures, mitigations, rollback.
- Blameless postmortems with concrete follow-ups.

## Cloud Run specifics (Starvit)
- Handle SIGTERM gracefully; ensure shutdown safety.
- Prefer small, safe deployments: canary revisions, quick rollback.

## Deliverables
- `docs/ops/SLOs.md` + alert thresholds
- Runbook index + on-call rotation notes
- Postmortem template
