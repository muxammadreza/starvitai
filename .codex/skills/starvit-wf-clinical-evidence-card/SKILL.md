---
name: starvit-wf-clinical-evidence-card
description: Produce an evidence card for a specific metabolic-therapy claim (claim -> citations -> confidence -> applicability -> implementation implications).
---

# Produce an evidence card for a specific metabolic-therapy claim (claim -> citations -> confidence -> applicability -> implementation implications)

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

# Workflow: Evidence card

## Inputs

- Claim statement (one sentence).
- Intended product impact (protocol gate? clinician dashboard info? ML feature?).

## Steps

1) **Decompose the claim**
   - Mechanism claim vs outcome claim vs safety claim.

2) **Collect evidence**
   - Prioritize: systematic reviews/meta-analyses → RCTs → cohorts → case series → mechanism.
   - Record search strategy and inclusion/exclusion (lightweight PRISMA).

3) **Assess quality and applicability**
   - Population, cancer type, stage, concurrent therapy.
   - Contraindications and red flags.
   - Identify plausible counterexamples / tumor-subtype caveats.

4) **Produce implementation notes**
   - What can be safely turned into a *monitoring* feature?
   - What requires clinician override?
   - What should remain “research-only”?

## Output format

- Title
- Claim
- Evidence table (citation, design, n, effect direction)
- Confidence grade (A–D)
- Applicability constraints
- Safety gates triggered
- Engineering implications

