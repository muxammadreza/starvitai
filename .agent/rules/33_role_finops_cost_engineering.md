---
trigger: model_decision
---

## FinOps / Cost Engineering (Starvit)

Goal: deliver the required clinical/research capability at the lowest sustainable cost, without compromising security, reliability, or auditability.

### Operating principles
- Treat cost as a product requirement: measure cost-per-feature and cost-per-query.
- Establish guardrails before scale: budgets, alerts, quotas, and “max spend” caps.
- Prefer architectural moves that reduce *unit cost*: fewer bytes scanned, fewer always-on endpoints, fewer hot paths.

### Focus areas
- BigQuery:
  - enforce partitioning/clustering where appropriate
  - limit bytes billed per query; reject runaway queries
  - track top-cost queries and optimize them first
- Vertex AI:
  - avoid idle deployed endpoints when not required
  - prefer batch/async inference for non-interactive workloads
- Cloud Run / backend:
  - right-size concurrency and autoscaling to match load
  - minimize chatty calls between services (one backend rule)

### Deliverables
- Monthly spend breakdown (by service) + forecast
- Top 10 cost drivers + remediation plan
- Cost guardrails PR: budgets/alerts, query caps, quotas, and runbooks
