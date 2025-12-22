---
description: Define/refresh data contracts and lineage for a data product
---

1) Define the contract:
   - table/view name
   - owner
   - grain
   - primary keys
   - field list with types + semantics + units
   - partition/clustering strategy
2) Define permitted uses:
   - cohorting, reporting, training, inference
3) Define lineage:
   - source systems (FHIR, pipelines, embeddings)
   - transformation steps and versions
4) Define quality guarantees:
   - tests/assertions and SLAs
5) Publish:
   - docs/data dictionary update
   - add to feature registry if ML-facing

Deliverable:
- A contract doc and lineage map that another engineer can implement from scratch
