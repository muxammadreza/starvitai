# Starvit Architecture

## Components

### Applications (Frontends)
1. **Patient App (`@starvit/patient`)**: React Native (Expo). Mobile interface for patients to log measurements.
2. **Clinician Dashboard (`@starvit/clinician`)**: Next.js. Web interface for clinicians to monitor patients and protocols.
3. **Research Workbench (`@starvit/research`)**: Next.js. Web interface for researchers to define cohorts and explore data.

### Backend (`services/api`)
- **Framework**: FastAPI (Python).
- **Role**: Single façade for all frontends.
- **Routes**:
  - `/api/patient/*`: Patient logging and data access.
  - `/api/clinician/*`: Clinical monitoring.
  - `/api/research/*`: Analytics and graph queries.

### Data Layer
- **PHI/Clinical Data**: Stored in **Medplum** (FHIR Server).
  - Frontends DO NOT access Medplum directly. All PHI writes go through the Starvit API Façade (`phi_gateway` module).
- **De-identified Research Data**: Stored in **TigerGraph**.
  - No direct access from frontends. Access via Research API.

### Infrastructure
- **Monorepo**: Managed by Turborepo and pnpm workspaces.
- **Deployment**: Coolify (Docker Compose).
  - **Stack 1 (Medplum)**: Medplum Server + Postgres + Redis.
  - **Stack 2 (Starvit)**: API + Clinician + Research.

## Data Flow
Patient App -> Starvit API -> Medplum (FHIR)
Clinician App -> Starvit API -> Medplum (FHIR)
Research App -> Starvit API -> TigerGraph (De-ID) / Medplum (De-ID)

## Shared Packages
- `@starvit/types`: Domain types (TypeScript).
- `@starvit/protocol`: Zod schemas and XState machines for protocol logic.
- `@starvit/api-client`: Typed fetch client for the Starvit API.
- `@starvit/ui`: Shared UI components (minimal).
