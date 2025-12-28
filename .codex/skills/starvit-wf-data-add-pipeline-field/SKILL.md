---
name: starvit-wf-data-add-pipeline-field
description: Add a new field to a pipeline dataset and propagate safely
---

# Add a new field to a pipeline dataset and propagate safely

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

## Steps
1) Define the field contract:
   - name/type/semantics
   - nullability + defaults
2) Update upstream extraction/transform.
3) Update downstream consumers:
   - BigQuery tables
   - feature tables
   - TigerGraph export schema
4) Backfill plan:
   - how to populate historical rows
5) Data quality checks:
   - null thresholds
   - distribution sanity

## Output
Schema change with backfill and validation.

