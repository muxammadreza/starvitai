# Transformations: dbt and Dataform

## dbt Core (preferred for Starvit)
Use dbt when you need:
- strong testing and CI workflows
- incremental models for large tables
- reproducible docs and a consistent developer experience

Minimum bar per model:
- description
- tests (unique/not_null/relationships/accepted_values) where applicable
- incremental strategy and unique_key documented (if incremental)

## Dataform (allowed)
Use Dataform when:
- BigQuery Studio-native workflow improves team velocity
- repo remains small and compilation limits are not a concern

Minimum bar per workflow:
- assertions for key invariants
- documented schedules and backfill behavior
