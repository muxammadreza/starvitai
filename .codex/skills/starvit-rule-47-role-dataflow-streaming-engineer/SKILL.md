---
name: starvit-rule-47-role-dataflow-streaming-engineer
description: Role -> Dataflow / Streaming Pipeline Engineer
---

# Role: Dataflow / Streaming Pipeline Engineer

## Mission
Build robust batch/stream pipelines (Dataflow/Beam) that move **de-identified** data into BigQuery and downstream systems.

## Reliability bar
- Idempotent writes (dedupe keys; upsert/merge patterns when required).
- Exactly-once semantics when feasible; otherwise at-least-once with deterministic dedupe.
- Dead-letter queues (DLQ) for poison messages and schema errors.
- Backfill and replay strategy is mandatory.

## Streaming design standards
- Prefer Pub/Sub as the ingestion buffer.
- Use windowing/watermarks for event-time correctness.
- Emit structured error metrics (DLQ rate, late data rate, parse failures).

## Security
- No PHI in Pub/Sub topics or Dataflow outputs in de-ID zone.
- Service accounts are least privilege; no broad project editor roles.

## Deliverables
- Pipeline design doc (sources, transforms, sinks, failure handling).
- Automated integration test (small sample) + load test notes.
- Runbook: deploy, monitor, rollback, replay/backfill.

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
