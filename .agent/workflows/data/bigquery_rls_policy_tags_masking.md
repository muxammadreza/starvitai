---
description: Implement BigQuery row-level security + policy tags + masking
---

Use this when adding fine-grained controls to a dataset/table.

1) Decide what needs protection:
   - cohort isolation (RLS)
   - quasi-identifiers (policy tags + column access control)
   - sensitive columns (masking policies)
2) Implement controls:
   - RLS: `CREATE ROW ACCESS POLICY ... FILTER USING (...)`
   - Policy tags: assign tags to columns and enforce access control on taxonomy
   - Masking: create data masking policies where appropriate
3) Verify:
   - authorized user can query allowed data
   - unauthorized user receives access denied or masked results
   - validate that dataset IAM alone does not over-grant access
4) Document:
   - access matrix update
   - verification queries + screenshots/logs if needed

Deliverables:
- DDL/policy definitions
- Verification evidence
- Updated governance docs
