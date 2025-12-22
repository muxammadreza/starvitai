---
description: Provision BigQuery datasets + governance (IAM, RLS, policy tags)
---

## When to use
- Creating a new analytics or feature dataset.
- Tightening access controls for de-identified data products.

## Steps
1) Define dataset intent:
   - domain (clinical, protocol, cohort, features, embeddings, ops metrics)
   - environment (dev/stage/prod)
   - owner + on-call
   - retention class
2) Create datasets with naming conventions:
   - `sv_<env>_<domain>`
3) Apply baseline IAM:
   - owners: data admins only
   - writers: pipeline service accounts only
   - readers: allowlisted groups; prefer views for broad access
4) Apply fine-grained security where needed:
   - Row-level security policies for cohort isolation
   - Policy tags + column-level access control for quasi-identifiers
   - Data masking policies for columns that remain sensitive post de-ID
5) Validate:
   - “least privilege” test: random user cannot query protected columns/rows
   - audit log visibility for dataset accesses

Deliverables:
- Terraform/infra changes (or infra PR) for dataset + IAM
- RLS/policy-tag definitions and verification queries
- Updated docs/data governance notes
