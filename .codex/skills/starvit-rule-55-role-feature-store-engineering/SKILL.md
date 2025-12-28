---
name: starvit-rule-55-role-feature-store-engineering
description: Role -> Feature Store Engineer
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

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
