---
description: Add structured logging + traces + metrics (OpenTelemetry-first)
---

## Goal
Make every critical path observable without leaking PHI.

## Steps
1) Define what to measure:
   - request lifecycle (route, latency, status)
   - business events (protocol suggestion, approval, export)
   - data pipeline health
2) Instrument traces:
   - span naming consistent
   - semantic attributes (low cardinality)
3) Emit structured logs:
   - include `trace_id` / `span_id` correlation fields
   - redact sensitive fields at the logger boundary
4) Metrics:
   - counters for errors
   - histograms for latency
   - gauges for saturation/backlog
5) Dashboards + alerts aligned to SLOs.

## Output
- updated instrumentation
- dashboard and alert definitions
