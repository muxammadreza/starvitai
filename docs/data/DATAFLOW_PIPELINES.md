# Dataflow / Beam pipelines (de-identified zone)

## When Dataflow is warranted
- streaming ingestion with correctness requirements (windowing/watermarks)
- complex ETL that benefits from Beam transforms
- large backfills where you need robust retries, observability, and DLQs

## Required pipeline features
### Idempotency
- side effects outside the pipeline must be idempotent (retries happen)
- use deterministic keys for dedupe and upserts

### Dead-letter pattern
- branch bad records away from the main path
- store DLQ elements with enough context to diagnose + replay

### Versioning
- pipeline code and transform versions are part of provenance
- keep versions aligned with retention of the data produced

### Schema as code
- schemas live in the repo, reviewed like code
- additive changes preferred; document breaking changes and backfills

### Observability
- explicit metrics: throughput, lag, DLQ rate, parse failures, late-data rate
- logs contain correlation IDs but never PHI

### Runbooks
- deploy, rollback, drain/cancel behavior
- replay/backfill procedure
- DLQ inspection + remediation path
