---
name: starvit-wf-ml-evaluation-and-model-card
description: Evaluate a model and publish a model card (Starvit)
---

# Evaluate a model and publish a model card (Starvit)

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

Use this when:
- training a new model version,
- changing features,
- or changing the evaluation protocol.

## 1) Define evaluation scope
- model version, feature set version, dataset snapshot
- target tasks (risk stratification, response prediction, novelty ranking, etc.)
- intended use and contraindications (clinician approval required)

## 2) Data integrity checks
- point-in-time correctness (no leakage)
- cohort definitions are versioned
- de-identified data only
- label quality and missingness audit

## 3) Metrics (minimum set)
- discrimination (AUC/PR-AUC where applicable)
- calibration (reliability, Brier score)
- stability and drift (train vs eval distributions)
- subgroup checks (only within permitted de-identified constraints)
- uncertainty estimates and confidence calibration if produced

## 4) Error analysis
- top failure modes
- confusion slices (by cohort strata, time windows, data completeness)

## 5) Publish artifacts
- update `docs/ml/templates/model_card_template.md` and commit a completed model card
- attach evaluation report summary and key plots
- record decisions: promote/hold/reject and why

Deliverables:
- evaluation report + model card
- reproducible script/notebook reference
- decision log entry (docs/DECISIONS.md or ADR)

