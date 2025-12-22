---
description: Deploy backend to Cloud Run with safety checks (tests, config validation, rollout verification)
---

1) Confirm target environment (dev/stage/prod) and the Cloud Run service name.
2) Ensure config is present:
   - required env vars and Secret Manager bindings
   - service identity (user-managed service account)
3) Run local verification:
   // turbo
   - Run `poetry run ruff check`
   // turbo
   - Run `poetry run pytest -q`
4) Build the container and push to registry (platform-specific; do NOT auto-run deploy commands without explicit confirmation).
5) Deploy a new revision to Cloud Run.
6) Post-deploy verification:
   - call `/healthz` and `/readyz`
   - verify logs show startup without secrets
   - run a small canary request path
7) Rollback plan:
   - identify the previous stable revision and how to revert traffic.

Deliver: deployment checklist + commands used + verification evidence.
