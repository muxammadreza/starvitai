---
description: FinOps cost review (cloud + data + ML)
---

Objective: reduce unit cost and prevent surprise spend while preserving reliability, security, and auditability.

Inputs:
- Recent changes (PRs) and planned roadmap items
- Current architecture docs (`docs/ARCHITECTURE.md`)
- Current SLOs and expected load
- Current cloud billing exports (if available)

Steps:
1) Identify cost drivers by surface:
   - BigQuery (bytes scanned, storage, scheduled queries)
   - Vertex AI (deployed endpoints, batch jobs, monitoring, feature store)
   - Cloud Run / networking (requests, egress)
   - Storage (GCS, logs, artifacts)
2) Add hard guardrails:
   - BigQuery: enforce maximum-bytes-billed for interactive queries; require partitions for large tables; prefer clustered tables where appropriate.
   - Vertex AI: ensure endpoints are not left deployed when idle; prefer batch inference for offline workloads.
   - Cloud Run: set sane autoscaling/concurrency defaults and per-environment limits.
3) Add visibility:
   - Create/verify budgets and alerting thresholds.
   - Publish “top spenders” runbook: where to look, how to remediate.
4) Produce a remediation plan:
   - quick wins (largest spenders)
   - medium-term refactors (data model / query patterns)
   - long-term architectural moves (reduce duplication, cache, fewer hops)

Deliverables:
- Cost review note: “current top drivers + proposed guardrails”
- PR(s) implementing guardrails (query caps, budgets, runbooks)
- A simple KPI: cost-per-active-user and/or cost-per-1k events (pick one per environment)
