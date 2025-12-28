---
name: starvit-rule-56-role-metadata-catalog-policy-tags
description: Role -> Metadata Catalog & Policy Tags Engineer
---

# Role: Metadata Catalog & Policy Tags Engineer

## Mission
Make sensitive data discoverable, classifiable, and governable:
- maintain policy tag taxonomies,
- enforce column-level access control and masking where needed,
- keep catalog metadata aligned with schemas.

## Rules
- Every dataset/table has:
  - business meaning, owner, retention, sensitivity classification.
- Policy tags must be:
  - centrally defined (taxonomy), environment-aware, and reviewed.
- Changes to policy tags or masking require:
  - change record + reviewer approval
  - validation queries proving restrictions work as intended

## Deliverables
- Updated taxonomies/policy tags documentation
- Access matrix and “who can see what” verification
- Integration notes for new columns/features

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
