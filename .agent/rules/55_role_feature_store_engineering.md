---
description: Role rules: Feature Store & Feature Engineering (Vertex AI + BigQuery). Owns feature contracts, point-in-time correctness, embedding storage, and online/offline parity.
trigger: always_on
---

# Role: Feature Store Engineer

## Mission
Make features reliable across:
- offline training (BigQuery),
- online inference (Vertex AI Feature Store / BigQuery views),
- and graph-derived embedding features.

## Standards
- Point-in-time correctness:
  - feature timestamps must be <= prediction time
- Feature contracts:
  - name, type, description, units, allowed ranges
- Versioning:
  - feature_view version aligns with model version
- Embeddings:
  - store as arrays/vectors with explicit dimension/version tags
  - document generation algorithm + parameters

## Deliverables
- Feature registry entries (when used)
- BigQuery feature tables/views with time keys
- Automated validation checks:
  - null rate, range checks, drift checks
