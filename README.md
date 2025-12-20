# Starvit Monorepo

Clinical-grade platform for metabolic therapy support.

## Getting Started (Day 1)

### Prerequisites
- Node.js 22
- pnpm 10.26
- Docker & Docker Compose
- Python 3.13+ (for backend local dev without Docker)

### 1. Start Infrastructure (Medplum + DBs)
Spins up Medplum Server, App, Postgres, and Redis locally.
```bash
# Copy env template
cp infra/dev/.env.local.example infra/dev/.env.local

# Start services
pnpm dev:infra
```
- Medplum App: http://localhost:3000 (Login: `admin@example.com` / `medplum_admin`)
- Medplum API: http://localhost:8103

### 2. Start Applications (Clinician + Research)
Runs the Next.js apps in development mode.
```bash
pnpm install
pnpm dev
```
- Clinician App: http://localhost:3001
- Research App: http://localhost:3002

### 3. Start Backend (API)
The backend runs in `stub` mode by default for safety.
```bash
cd services/api
cp .env.example .env
poetry install
poetry run uvicorn app.main:app --reload --port 8000
```
- API Docs: http://localhost:8000/docs

## Architecture
- **Apps**: `apps/clinician`, `apps/research`, `apps/patient` (Expo)
- **Backend**: `services/api` (FastAPI modular monolith)
- **Infrastructure**: `infra/coolify` (Docker Compose for deployment)
- **Shared**: `packages/*`

## Security Notes
- **PHI**: Stays in Medplum (FHIR).
- **Logs**: Never log PHI or Tokens.
- **Mode**: `STARVIT_MODE=stub` (default) vs `live`. Live mode requires auth.
