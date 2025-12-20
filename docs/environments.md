# Environments & Configuration

This project follows the **12-Factor App** methodology: config is stored in the environment.

## Required Environment Variables

| Variable | Dev (Local) | Staging | Production |
|----------|-------------|---------|------------|
| `APP_ENV` | `dev` | `staging` | `prod` |
| `STARVIT_MODE` | `stub` (default) or `live` | `live` | `live` |
| `MEDPLUM_BASE_URL` | `http://localhost:8103/` | `https://fhir-staging.starvit.ca/` | `https://fhir.starvit.ca/` |
| `MEDPLUM_APP_BASE_URL` | `http://localhost:3000/` | `https://medplum-staging.starvit.ca/` | `https://medplum.starvit.ca/` |
| `MEDPLUM_STORAGE_BASE_URL` | `http://localhost:8103/storage/` | `https://fhir-staging.starvit.ca/storage/` | `https://fhir.starvit.ca/storage/` |
| `MEDPLUM_JWT_ISSUER` | `http://localhost:8103/` | `https://fhir-staging.starvit.ca/` | `https://fhir.starvit.ca/` |
| `MEDPLUM_JWT_AUDIENCE` | `http://localhost:8103/` | `https://fhir-staging.starvit.ca/` | `https://fhir.starvit.ca/` |

### Mode `stub` vs `live`
- **`stub`**: Allowed ONLY in `dev`. The backend may mock specific integrations (like TigerGraph or expensive AI calls) to unblock UI development.
- **`live`**: REQUIRED for `staging` and `prod`. All backing services must be real. Missing credentials or unreachable services will cause 500/503 errors, ensuring we never "fail open" or pretend to succeed.

## Promotion Strategy
We build **single Docker images** for our applications and promote them through environments.
- **Backend**: Configured purely via env vars.
- **Frontends (Next.js)**:
  - We use **Runtime Configuration** where possible (reading env vars during `getServerSideProps` or server components).
  - For public browser-side vars (`NEXT_PUBLIC_*`), we rely on the specific build-time environment or use a runtime config endpoint if strict "one image" purity is required. Current strategy: **Rebuild on promotion** is acceptable for Next.js if strictly needed for `NEXT_PUBLIC_` inlining, OR use server-side proxies to keep the image identical.

## Deployment (Coolify)
In Coolify, you must set these variables in the **Environment Variables** UI for each service.
- **Secrets** (Passwords, Tokens) are masked.
- **Topology**: Staging and Prod share identical `docker-compose.yml` topology, differing only in ingress domains and volume names.
