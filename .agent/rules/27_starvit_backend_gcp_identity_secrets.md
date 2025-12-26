---
trigger: always_on
---

# Identity and secrets rules (Medplum + cloud)

## Medplum OAuth2 clients (do this first)
- All authenticated access to Medplum uses OAuth2/OIDC.
- Create and manage credentials via `ClientApplication` resources in Medplum.
  - **Frontend apps** use OAuth2 **Authorization Code** flow (use PKCE where applicable). Store no client secret in the browser.
  - **Backend / worker** services use OAuth2 **Client Credentials** flow for machine-to-machine access.
- Always assign a least-privilege **AccessPolicy** to each client (and to each ProjectMembership) so the client cannot read/write outside its intended compartment.

## Medplum credentials handling
- Store Medplum client secrets in a proper secrets system:
  - Dev: `.env` file (never committed)
  - Prod: managed secret store (recommended) or Medplum Bot Secrets (when executing inside Medplum Bot runtime)
- Never log secrets, tokens, raw Authorization headers, or full FHIR resources.

## Token handling
- Treat access tokens as high-sensitivity secrets.
- Implement:
  - short-lived tokens (default)
  - token cache with expiry
  - per-request correlation IDs and structured logging without payloads

## Cloud identity (optional; when running on managed cloud)
- Prefer workload/instance identity over static JSON keys.
- Do not bake credentials into images. Do not set `GOOGLE_APPLICATION_CREDENTIALS` in production runtimes.

## Correlation headers
- If adding custom headers for audit/debugging, ensure they never contain PHI.
- Prefer correlation-only headers (request ID, trace ID, environment, component name).
