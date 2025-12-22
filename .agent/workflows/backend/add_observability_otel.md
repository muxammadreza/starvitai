---
description: Add or update OpenTelemetry tracing/log correlation for the backend service
---

1) Identify which components need instrumentation:
   - FastAPI incoming requests
   - outbound HTTP calls (httpx)
   - cloud clients (where possible)
2) Add or update tracing setup:
   - ensure a single tracer provider is configured at startup
   - export to OTLP/Cloud Trace as configured
3) Correlation:
   - inject or propagate a request ID; include it in all logs
   - ensure trace_id/span_id can be surfaced in logs for debugging
4) Add a smoke test:
   - unit test that middleware adds correlation ID header
   - optional integration test that route handler creates a span
5) Update `docs/backend/OBSERVABILITY.md`.

Quality gates:
// turbo
- Run `poetry run pytest -q`
