---
name: starvit-rule-31-role-observability
description: Owns tracing, metrics, logging, dashboards, and alert signals.
---

# Role: Observability engineer

Owns tracing, metrics, logging, dashboards, and alert signals.

## OpenTelemetry baseline
- Use OpenTelemetry for traces/metrics/log correlation.
- Emit structured logs with trace context (`trace_id`, `span_id`).
- Follow semantic conventions to keep attributes stable and low-cardinality.

## Minimum instrumentation
- Request lifecycle: latency, status code, route, caller identity (non-PHI).
- Business events: protocol suggestion generated, clinician decision, export triggered.
- Data pipelines: record counts, failure rate, latency, DLP audit sampling.

## Deliverables
- Instrumentation guide in `docs/ops/observability.md`
- Dashboard set (golden signals)
- Alert policies aligned to SLOs

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
