# Datasets and features (Starvit)

## Non-negotiable
All training/evaluation data must be **de-identified**.

## Dataset versioning
Every dataset snapshot has:
- `dataset_version` (semantic)
- source table/view versions
- extraction time
- label definition + horizon
- cohort definition

## Feature versioning
Every feature set has:
- `feature_version`
- point-in-time correctness rules
- units and conversion rules
- missingness strategy

## Graph-derived features
Store:
- embeddings (vector + dimension + algo version)
- similarity scores (with algorithm + params)
- community/centrality metrics

## Templates
Use:
- `docs/ml/templates/dataset_datasheet_template.md`
- `docs/ml/templates/model_card_template.md`
