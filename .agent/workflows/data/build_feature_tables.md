---
description: Build offline feature tables/views in BigQuery (training + evaluation)
---

Use this when introducing a new model feature set or changing feature semantics.

## 1) Define the feature spec
- Feature name, description, units, allowed ranges
- Source datasets (BigQuery tables / graph embeddings)
- Time keys:
  - feature_time
  - label_time / prediction_time
- Join keys (patient_pseudo_id, cohort_id, encounter_id as applicable)

## 2) Enforce point-in-time correctness
- Features must be computed using data **available at or before** prediction time.
- Backfill logic must not leak future information.
- Document the leakage-prevention mechanism in the feature spec.

## 3) Implement as SQL transformations
Choose one:
- dbt incremental models for large tables
- Dataform workflows for BigQuery-native pipelines

## 4) Validate
- Data quality tests (nulls/ranges/keys)
- Drift baselines for key features
- Reproducibility check: re-run on same snapshot yields same results

## 5) Versioning and registry
- Feature set version must map to:
  - transformation code version (git SHA)
  - upstream dataset versions
  - embedding version (if applicable)

Deliverables:
- Feature spec + docs/ml dataset datasheet update
- BigQuery DDL and transformation code
- Tests + monitoring additions
