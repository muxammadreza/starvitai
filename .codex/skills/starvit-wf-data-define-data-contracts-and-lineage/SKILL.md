---
name: starvit-wf-data-define-data-contracts-and-lineage
description: Define/refresh data contracts and lineage for a data product
---

# Define/refresh data contracts and lineage for a data product

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

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

