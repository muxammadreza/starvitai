---
description: Make a transformation change in BigQuery using dbt or Dataform
---

## 1) Decide the tool (dbt vs Dataform)
- dbt: strong testing ecosystem, CI-first workflow, portable
- Dataform: BigQuery-native integration, SQL-first workflows in BigQuery Studio

## 2) Change design
- Define the target model/table/view
- Partition/clustering plan (if table)
- Backfill behavior (full refresh vs incremental)

## 3) Implement
- Add model SQL + documentation
- Add tests/assertions:
  - unique/not_null/accepted_values/relationships
  - custom clinical checks where relevant

## 4) Validate
- Dry run with limited data (partition filters)
- Compare bytes scanned and runtime pre/post change
- Verify invariants and row counts

## 5) Deploy
- Merge to main with CI gates
- Schedule/trigger (Cloud Build, Composer, Workflows, or Dataform schedule)
- Update docs/data dictionary and lineage map

Deliverables:
- PR with models + tests + docs
- Cost/perf diff notes
- Rollback/backfill instructions
