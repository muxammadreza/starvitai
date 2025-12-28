---
name: starvit-wf-data-dataflow-streaming-pipeline-pubsub-bigquery
description: Build a Dataflow/Beam pipeline from Pub/Sub to BigQuery (de-identified)
---

# Build a Dataflow/Beam pipeline from Pub/Sub to BigQuery (de-identified)

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

## Steps
1) Define message contract:
   - schema, versioning, idempotency key
   - classification: must be de-identified
2) Pub/Sub design:
   - topic and subscription names
   - retention and DLQ topic for poison messages
3) Dataflow design:
   - parse/validate
   - dedupe (stateful or deterministic key)
   - windowing/watermarks if event-time matters
   - write to BigQuery using an appropriate method (streaming insert or Storage Write API)
4) Observability:
   - metrics: throughput, lag, error rate, DLQ rate
   - structured logs with correlation IDs
5) Operations:
   - deploy procedure (dev → stage → prod)
   - rollback plan
   - replay/backfill plan from Pub/Sub retention or archived raw logs

Deliverables:
- Pipeline code skeleton + config
- Message contract doc
- Runbook + alerting

