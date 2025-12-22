---
trigger: always_on
---

# GCP Identity and Secrets Rules (Backend)

## Cloud Run service identity
- Use a **user-managed service account** as the Cloud Run service identity.
- Grant least-privilege IAM roles required for specific API calls (Healthcare API, Secret Manager, Pub/Sub, BigQuery, Vertex AI, etc.).
- Avoid the default Compute Engine service account unless an explicit ADR approves it.

## Credentials in Cloud Run
- Do **not** set `GOOGLE_APPLICATION_CREDENTIALS` in Cloud Run services, jobs, or worker pools.
- Use Application Default Credentials via the metadata server (Cloud Client Libraries) under the configured service identity.

## Secret handling
- Secrets must come from **Secret Manager** (environment variables or mounted volumes).
- Do not log secret values. Do not echo secrets in terminal output or CI logs.
- Any new secret requires:
  - an owner and rotation plan
  - least-privilege access policy
  - non-production safe defaults

## Healthcare API request headers
- If adding custom headers for audit/debugging, ensure they never contain PHI.
- Prefer correlation-only headers (request ID, trace ID, environment, component name).
