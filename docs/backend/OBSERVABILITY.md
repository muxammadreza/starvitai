# Backend observability (Starvit)

## Goals
- Each request is traceable end-to-end with correlation IDs.
- Audit events can be linked back to the initiating request.
- PHI is never written to logs/metrics/traces.

## Signals (golden signals)
- **Latency**: p50/p95/p99 per route.
- **Traffic**: RPS by route and caller type.
- **Errors**: 4xx vs 5xx; top error codes.
- **Saturation**: CPU/memory/concurrency, queue depth.

## Tracing (OpenTelemetry)
- Instrument FastAPI and outbound clients.
- Propagate W3C trace context across boundaries.
- Use stable semantic attributes and avoid high-cardinality labels.

## Logging
- JSON structured logs.
- Include `trace_id` + `span_id` for log/trace correlation.
- Central scrubbing: redact tokens, emails, MRNs, names.

## Audit logging
Audit events are not debug logs.
- include actor identity, action, object, timestamp, rationale
- store in an append-oriented store suitable for review

## Metrics
- service-level SLIs used to compute SLOs.
- pipeline-level metrics for ETL/de-id (counts, failures, lag).

## Runbooks
- every alert must have a runbook with:
  - expected impact
  - diagnosis steps
  - rollback or mitigation steps
