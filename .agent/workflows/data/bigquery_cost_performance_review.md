---
description: BigQuery cost and performance review for a dataset or workload
---

1) Identify top cost drivers:
   - most expensive queries/jobs by bytes processed
   - scheduled queries and pipeline jobs
2) Quick wins:
   - enforce partition filters and clustering
   - materialize expensive views into tables (incremental if possible)
   - remove unnecessary columns early (projection pushdown)
3) Structural improvements:
   - redesign table partitioning strategy (event time vs ingestion time)
   - denormalize selectively for repeated joins
   - precompute common cohort filters
4) Governance:
   - require job labels for ownership/cost attribution
   - set quotas or max bytes billed for unsafe workloads where possible
5) Report:
   - before/after bytes scanned + runtime
   - change plan and risk assessment

Deliverable:
- Cost/perf report + PR(s) to implement changes
