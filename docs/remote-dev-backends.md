# Remote Dev Backends on Coolify

This guide details how to set up the persistent backing services (Medplum, Postgres, Redis) for development using a managed Coolify instance (VPS). This allows developers to run application code locally (apps & API) while connecting to shared, stable, and persistent data services.

## Prerequisites
- Access to the Starvit Coolify instance.
- A domain setup (e.g., `starvit.ca` with wildcard `*.starvit.ca`).

## Step 1: Create Project & Environment
1. In Coolify, go to **Projects**.
2. Open or create the `starvit` project.
3. Create a new Environment named `dev-remote`.

## Step 2: Configure Environment Variables
In the **Environment** view for `dev-remote`, switch to the **Secrets** (or Environment Variables) tab. Add the following variables. These will be shared across all services in this environment.

### Required Secrets
| Variable | Description | Example Value |
|---|---|---|
| `POSTGRES_PASSWORD` | Password for the internal Medplum Postgres | `generate-secure-password` |
| `MEDPLUM_REDIS_PASSWORD` | Password for internal Redis | `generate-secure-password` |
| `ANALYTICS_PASSWORD` | Password for Analytics Postgres | `generate-secure-password` |
| `MEDPLUM_BASE_URL` | Public URL of the Medplum Server (MUST have trailing slash) | `https://fhir-dev.starvit.ca/` |
| `MEDPLUM_APP_BASE_URL` | Public URL of the Medplum App | `https://medplum-dev.starvit.ca` |
| `MEDPLUM_STORAGE_BASE_URL` | URL base for binary storage | `https://fhir-dev.starvit.ca/binary/` |

**Note**: `MEDPLUM_BASE_URL` MUST end with a trailing slash `/`.

## Step 3: Deploy the Stack
1. In the `dev-remote` environment, click **+ Add Resource**.
2. Select **Docker Compose**.
3. Copy the content from `infra/coolify/dev-backends/docker-compose.yml` in this repo.
4. Paste it into the Coolify editor.
5. Click **Save**.

## Step 4: Configure Domains
After saving, you will see a list of services (`medplum-server`, `medplum-app`, `medplum-postgres`, etc.).
You need to explicitly configure the domains for the public-facing services.

1. **medplum-server**:
   - Go to the service configuration.
   - Set **Domains** to `https://fhir-dev.starvit.ca`.
   - Ensure the internal port is detected as `8103`.
   - Click **Save** & **Restart Service** if needed.

2. **medplum-app**:
   - Go to the service configuration.
   - Set **Domains** to `https://medplum-dev.starvit.ca`.
   - Ensure the internal port is detected as `3000`.
   - Click **Save** & **Restart Service** if needed.

3. **Backend Databases (medplum-postgres, etc.)**:
   - Ensure **Domains** is empty. These should NOT be reachable from the internet.
   - They communicate internally via the Docker network.

## Step 5: Verification
1. Navigate to `https://fhir-dev.starvit.ca/health`. You should see `{"status":"ok"}` (or similar Medplum health response).
2. Navigate to `https://medplum-dev.starvit.ca`. You should see the Medplum login screen.
3. Log in with the default admin credentials (if fresh install) or your configured admin user.

## Connecting Local Dev
Once deployed, local applications can connect to this environment.
See `infra/dev/.env.local.example` and `services/api/.env.example` for local configuration templates.
