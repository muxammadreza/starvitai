# Safety and red flags (KMT / metabolic therapy)

This is a clinician-facing *review checklist* and an engineering spec for building non-bypassable safety gates. It is not medical advice.

## “Stop and escalate” categories

Agents must escalate to clinician review when any work item involves:

### A) Fragile host / malnutrition risk
- Suspected or documented **cachexia** (or rapid unintentional weight loss).
- Poor oral intake, severe GI symptoms, dehydration.
- Frailty / inability to maintain adequate protein/energy intake.

Rationale: preclinical evidence suggests host outcomes can worsen even when tumor growth slows; therefore cachexia risk must gate any “optimize metabolic stress” logic. (Ferrer et al., 2023.)

### B) Diabetes / ketoacidosis (DKA) risk
- Type 1 diabetes, history of DKA, brittle glycemic control.
- Insulin/sulfonylurea management or any change requiring titration.

### C) Organ instability
- Significant renal or hepatic impairment, unstable cardiovascular disease.

Note: the evidence on ketogenic diet safety in “fragile populations” is nuanced; use living review updates and do not hard-code assumptions. (Watanabe et al., 2020.)

### D) Active oncology treatment interactions
- Concurrent chemotherapy/radiation; steroid-induced hyperglycemia; drug–diet interaction questions.

### E) Pregnancy/pediatrics/inborn errors
- Pregnancy, pediatrics, or known/suspected inborn errors of metabolism.

## Platform implication (engineering)

- These must be represented as **protocol engine gates** with:
  - explicit trigger criteria
  - a required clinician review step
  - audit logs (who approved, what data was reviewed, what version of logic)

- User-facing wording must avoid prescriptive medical guidance.

## Living review anchors

- Contraindications and safety evidence: Watanabe et al., 2020 (Obesity Reviews).
- Cachexia/host tradeoff: Ferrer et al., 2023 (Cell Metabolism).

## References

- Watanabe M et al. **Scientific evidence underlying contraindications to the ketogenic diet: an update.** *Obesity Reviews.* 2020. (Open access.)
- Ferrer et al. **Ketogenic diet, tumor delay, and cachexia/host-endocrine tradeoffs.** *Cell Metabolism.* 2023. (Open access.)
