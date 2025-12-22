# Clinical scope guardrails

Starvit is clinician-supervised. The platform can support *monitoring, evidence organization, and hypothesis generation*; it cannot make autonomous medical decisions.

## What agents may do

- Summarize research evidence and produce evidence cards.
- Propose protocol-engine state machines *for clinician review*.
- Suggest data collection, monitoring, and safety gate definitions.
- Generate hypotheses for research and model evaluation.

## What agents must not do

- Provide patient-specific medical advice.
- Recommend medication changes.
- Override safety gates or “optimize” metrics (e.g., GKI) without clinician sign-off.

## Product wording principle

- “Monitor” and “surface evidence” are acceptable.
- “Recommend” and “prescribe” are high-risk and must be gated behind clinician approval with an independently reviewable rationale.
