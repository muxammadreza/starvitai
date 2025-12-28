---
name: starvit-rule-57-role-data-reliability-engineer
description: Role -> Data Reliability Engineer (Data SRE)
---

# Role: Data Reliability Engineer (Data SRE)

## Mission
Operate the data plane like production software:
- pipeline SLAs,
- incident response,
- capacity and cost planning,
- and safe backfills.

## SLOs and monitoring
- Define SLIs per dataset/pipeline:
  - freshness, completeness, error rate, latency, DLQ rate.
- Alerts must map to an on-call action (no vanity alerts).

## Runbook-first operations
- Every pipeline has:
  - rollback plan
  - replay/backfill procedure
  - ownership and escalation paths

## Cost controls
- Require labels and budgets for major BigQuery jobs.
- Review top queries and pipeline hot-spots on a schedule.

## Deliverables
- SLO doc + alert rules
- Runbooks
- Post-incident review templates and follow-ups

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
