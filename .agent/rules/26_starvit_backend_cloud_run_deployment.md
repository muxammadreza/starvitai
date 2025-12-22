---
trigger: always_on
---

# Cloud Run Deployment Rules (Starvit Backend)

## Container contract
- Bind the ASGI server to `0.0.0.0:$PORT`.
- Provide two endpoints:
  - `GET /healthz`: liveness. Must not touch downstream dependencies.
  - `GET /readyz`: readiness. May check critical dependencies behind short timeouts.
- Handle `SIGTERM`: stop accepting new work, allow in-flight requests to complete where feasible, and exit cleanly.

## Production server
- Production runs behind a process manager:
  - preferred: **Gunicorn + Uvicorn worker**
  - disallowed: `uvicorn --reload` in any deployed revision
- Do not rely on in-memory state for correctness (Cloud Run scales horizontally).

## Timeouts and limits
- All outbound calls must set explicit timeouts.
- Enforce request body size limits for endpoints that accept uploads or large payloads.

## Scaling and concurrency
- Cloud Run concurrency must be set intentionally; endpoints must be safe under concurrent access.
- Any background processing must be idempotent and resilient to at-least-once delivery.

## Deployment hygiene
- Secrets come from Secret Manager (env vars or mounted volumes); do not bake secrets into images.
- Release changes are versioned, traceable, and reversible.
