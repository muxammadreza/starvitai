# Async jobs and ETL orchestration

## Why
Starvit uses asynchronous workflows for:
- de-identification exports and analytics table refreshes
- graph loads
- long-running cohort operations

## Building blocks
- Cloud Workflows: orchestrate multi-step pipelines
- Pub/Sub: eventing and task fan-out

## Pub/Sub handler rules
- Assume at-least-once delivery; implement idempotency.
- Verify authentication for push endpoints (OIDC token).
- Validate message envelope and version.

## Workflow design rules
- Use explicit retries with exponential backoff and jitter.
- Model failure states and compensating actions (saga style)
- Emit audit events on state transitions that matter.
