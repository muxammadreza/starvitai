# Model registry conventions (Starvit)

## Versioning
- Use semantic versioning for the model artifact.
- Labels must include:
  - dataset_version
  - feature_version
  - graph_snapshot_id (if used)
  - git_sha
  - training_pipeline_run_id

## Required attachments
- model card (markdown)
- evaluation summary (metrics + slices)
- monitoring plan (drift, quality)

## Release process
- register -> shadow/canary -> promote
- rollback plan required
