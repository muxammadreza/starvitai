---
name: starvit-rule-28-backend-async-pubsub-workflows
description: Async Processing Rules (Pub/Sub + Cloud Workflows)
---

# Async Processing Rules (Pub/Sub + Cloud Workflows)

## Delivery semantics
- Assume **at-least-once** delivery for Pub/Sub messages. Handlers must be idempotent.
- Every message handler must:
  - validate payload schema and version
  - enforce authN/authZ (for push endpoints, verify OIDC token)
  - implement dedupe/idempotency keys where applicable
  - set bounded retries; dead-letter on poison messages

## Message contracts
- Define a canonical message envelope:
  - `type`, `version`, `correlation_id`, `occurred_at`, `payload`
- Never include PHI in Pub/Sub message payloads for the de-identified pipeline.

## Workflow orchestration
- Use Cloud Workflows as the orchestrator for multi-step pipelines (FHIR export, DLP, BigQuery load, TigerGraph load).
- Model long-running or failure-prone steps as a saga:
  - explicit retries with backoff
  - clear error routing
  - compensating actions where feasible
- Emit audit events for any state transition that affects PHI access or clinician-facing outputs.

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
