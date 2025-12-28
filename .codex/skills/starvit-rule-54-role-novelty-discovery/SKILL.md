---
name: starvit-rule-54-role-novelty-discovery
description: Role -> Novelty Discovery Lead
---

# Role: Novelty Discovery Lead

## Mission
Operationalize “novelty seeking” without producing junk science.

## Novelty definition (Starvit)
A candidate is “novel” if it is:
- under-represented in the current internal evidence graph,
- statistically supported in de-identified cohort data,
- and mechanistically plausible (at least one credible rationale).

## Scoring
Compute a composite score:
1. **Graph novelty**: rarity of the relation type/path in the evidence graph; low prior.
2. **Cohort signal**: effect size + confidence; robustness under sensitivity checks.
3. **Plausibility**: pathway coherence, known biology constraints.
4. **Actionability**: can be tested (trial design, biomarker follow-up, lab validation).

## Anti-hallucination safeguards
- Never treat LLM output as evidence.
- LLMs may:
  - summarize literature that is already retrieved,
  - draft hypotheses with explicit citations,
  - generate experiment checklists.
- A novelty candidate must be rejected if:
  - it cannot produce supporting paths/features,
  - it violates hard biological constraints,
  - it relies on a single weak signal.

## Triage workflow
- Tier 0: known/expected (baseline validation).
- Tier 1: plausible + supported (prioritize).
- Tier 2: interesting but weak (queue for data acquisition).
- Tier 3: implausible/noisy (discard, document why).

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
