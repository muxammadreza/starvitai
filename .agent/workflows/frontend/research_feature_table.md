---
description: Build a research feature exploration table with provenance (virtualized)
---

Goal: make large de-identified feature tables usable and fast.

Steps:

1) Define columns and provenance:
   - feature name, definition, units, missingness, distribution summary
   - dataset version + ETL run id
2) Implement TanStack Table + virtualization (see table workflow).
3) Add exploration affordances:
   - quick filters (missingness threshold, correlation threshold)
   - pin/save feature set (de-identified only)
4) Add export guardrails:
   - exports must be reviewed; avoid row-level dumps unless explicitly allowed
5) Tests:
   - sorting/filtering correctness
   - performance sanity on large row counts
Deliver:
- table screen + tests + provenance banner
