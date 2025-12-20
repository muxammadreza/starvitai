# Routing & Domains

## Public Domains

| Service | Dev (Local) | Staging | Production |
|---------|-------------|---------|------------|
| **Clinician UI** | `localhost:3001` | `admin-staging.starvit.ca` | `admin.starvit.ca` |
| **Research UI** | `localhost:3002` | `research-staging.starvit.ca` | `research.starvit.ca` |
| **Patient App** | (Expo) | `app-staging.starvit.ca` | `app.starvit.ca` |
| **API** | `localhost:8000` | `api-staging.starvit.ca` | `api.starvit.ca` |
| **FHIR Server** | `localhost:8103` | `fhir-staging.starvit.ca` | `fhir.starvit.ca` |

## Internal DNS (Docker Network)
Backend services verify JWT tokens from Medplum. To do this, they call the Medplum internal URL if needed (though mostly they verify signatures via cached JWKS).
Frontends proxy `/api/*` requests to the backend API via internal Docker DNS.

- **API**: `http://api:8000` (referenced as `STARVIT_API_INTERNAL_URL`)
- **Medplum**: `http://medplum-server:8103`
- **Graph**: `http://tigergraph:9000` (stub/live)
- **Analytics**: `postgresql://analytics-postgres:5432/...`

## Frontend Routing Strategy
We use **Server-Side Proxying (Pattern A)** to avoid baking API URLs into Docker images.
1. Frontend code calls `/api/...`.
2. Next.js Middleware/Rewrites proxy this to `STARVIT_API_INTERNAL_URL`.
3. This allows the same Docker image to work in Staging and Prod by just changing the `STARVIT_API_INTERNAL_URL` env var.
