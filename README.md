# Starvit Monorepo

Clinical-grade platform for metabolic therapy support.

## Quick Start (Local Development)

### Prerequisites
- Node.js 22 + pnpm 10.26
- Python 3.13 + Poetry
- Docker (optional, for analytics DB)

### 1. Install Dependencies
```bash
pnpm install
cd services/api && poetry install
```

### 2. Configure Environment
```bash
# Copy env templates
cp .env.example .env.local
cp services/api/.env.example services/api/.env
```

Edit the `.env` files with your managed service credentials:
- **TigerGraph**: Sign up at [tgcloud.io](https://tgcloud.io/)

### 3. Run Everything

**Option A: Stub Mode (No external services needed)**
```bash
# Terminal 1: Backend API (stub mode - fake data)
pnpm dev:api

# Terminal 2: Frontend apps
pnpm dev
```

**Option B: With Analytics DB**
```bash
# Start local Postgres for analytics
pnpm dev:db

# Then run API and frontends as above
```

### Access Points
| Service | URL |
|---------|-----|
| Clinician Dashboard | http://localhost:3001 |
| Research Workbench | http://localhost:3002 |
| API Docs | http://localhost:8000/docs |
| Patient App | `cd apps/patient && pnpm start` |

---

## Architecture

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Patient App │  │ Clinician   │  │ Research    │
│ (Expo)      │  │ (Next.js)   │  │ (Next.js)   │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┼────────────────┘
                        ▼
              ┌─────────────────┐
              │  Starvit API    │
              │  (FastAPI)      │
              └────────┬────────┘
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ GCP     │ │ TigerGraph  │ │ Analytics   │
│ (PHI/FHIR)  │ │ (De-ID)     │ │ (OMOP)      │
└─────────────┘ └─────────────┘ └─────────────┘
```

## Key Commands

```bash
pnpm dev          # Run all frontends
pnpm dev:api      # Run backend API
pnpm dev:db       # Start analytics DB
pnpm build        # Build all apps
pnpm lint         # Lint all code
```

## Security Notes
- **Logs**: Never log PHI or tokens
- **Mode**: Use `STARVIT_MODE=stub` for local dev
