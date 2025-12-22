# Cloud Run deployment (backend)

## Container contract
- Bind to `0.0.0.0:$PORT`.
- Provide `GET /healthz` and `GET /readyz`.
- Handle `SIGTERM` for graceful shutdown.

## Production server command
Preferred pattern:
- Gunicorn with an ASGI worker (Uvicorn worker)

Example:

```bash
gunicorn -k uvicorn.workers.UvicornWorker -w 2 -b 0.0.0.0:$PORT starvit_api.main:app
```

## Secrets and credentials
- Use Secret Manager for secrets.
- Use Cloud Run service identity for Google APIs (do not set `GOOGLE_APPLICATION_CREDENTIALS`).

## Scaling and concurrency
- Ensure code is safe under concurrent requests.
- Do not rely on in-memory state.
