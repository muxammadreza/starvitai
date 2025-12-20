# Starvit Monorepo

Clinical-grade platform for metabolic therapy support.

## Getting Started

### Prerequisites
- Node.js 22
- pnpm 10.26
- Docker & Docker Compose
- Python 3.13+ (for backend local dev without Docker)

### Installation
```bash
pnpm install
```

### Development
Start all services (Frontends + API) in development mode:
```bash
pnpm dev
```
- Medplum App: http://localhost:3000
- Clinician App: http://localhost:3001
- Research App: http://localhost:3002
- Patient App: Expo dev server (press `w` for web, or scan QR)
- API: http://localhost:8000/docs

### Local Infrastructure (Medplum)
To run the FHIR backend (Medplum) locally:
```bash
docker compose -f infra/dev/docker-compose.yml up -d
```
This spins up:
- Medplum Server (http://localhost:8103)
- Medplum App (http://localhost:3000)
- Postgres & Redis

**Note:** If running everything together via `infra/dev/docker-compose.yml`, it includes the Starvit API and Medplum. It does NOT include the Next.js apps by default (run those via `pnpm dev` for better DX).

### Deployment (Coolify)

1. **Deploy Medplum Stack**:
   - Use `infra/coolify/medplum/docker-compose.yml`.
   - Configure secrets in Coolify.
   - Domain: `fhir.starvit.ca` (8103), `medplum.starvit.ca` (3000).

2. **Deploy Starvit Stack**:
   - Use `infra/coolify/starvit/docker-compose.yml`.
   - Connects to Medplum via URL.
   - Domain: `api.starvit.ca` (8000), `clinician.starvit.ca` (3000), `research.starvit.ca` (3000, assign distinct domain/port mappings in Coolify).
   - Patient App: `app.starvit.ca` (hosted via Expo or web build).
