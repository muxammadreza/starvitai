---
description: Add a new field to a pipeline dataset and propagate safely
---

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
