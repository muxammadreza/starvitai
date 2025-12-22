---
description: Model risk and evaluation review (clinical-facing ML / novelty discovery)
---

Use this workflow for any ML output that could influence clinician decisions, protocol logic, or patient safety.

Treat the review as SaMD/CDS-adjacent risk management, not a generic ML checklist.

## Inputs

- model card draft + intended use statement
- dataset datasheet(s) + feature list + lineage
- evaluation report + slice results
- deployment/inference contract + monitoring plan

## Review checklist

### 1) Intended use and harm analysis
- What decision(s) might this influence?
- Failure modes: false positives, false negatives, “automation bias,” subgroup harms.
- Decide the required human-in-the-loop controls and UI constraints.

### 2) Data boundary integrity
- Confirm **de-identified training data** only.
- Confirm PHI never enters TigerGraph/ML features.
- Check for leakage risks (target leakage, label leakage, post-outcome features, future knowledge).

### 3) Clinical association and validity framing
- Does the model output reflect a clinically meaningful association?
- Are endpoints defined and measured reproducibly?
- Is external validation planned or performed?

### 4) Evaluation rigor
- Prefer time-aware splits (avoid temporal leakage).
- Calibration assessment where probability outputs exist.
- Subgroup performance (sex, age bands, cancer subtype/stage if available, treatment context).
- Robustness to missingness and measurement noise.

### 5) Transparency and “independently reviewable basis”
- For clinician-facing outputs, require:
  - top contributing factors/features (as appropriate)
  - provenance links (evidence cards, cohort definitions)
  - uncertainty/confidence + caveats

### 6) Operational controls
- Versioning: model version, feature set version, dataset snapshot version.
- Rollback strategy and canary plan.
- Monitoring: drift, data quality, outcome tracking, alerting.

### 7) Regulatory alignment (risk framing)
- Review `docs/clinical/REGULATORY_SAMD_CDS.md`.
- Ensure documentation aligns with GMLP principles and AI reporting norms (CONSORT-AI / SPIRIT-AI where relevant).

## Output

- Verdict: **approve / approve with conditions / reject**
- Required mitigations with owners
- Monitoring and change-control requirements
