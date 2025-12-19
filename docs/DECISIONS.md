# Starvit MVP Decisions

## 1. Backend Architecture
**Decision:** Single Modular Monolith (`services/api`) using FastAPI (Python). 
**Rationale:** Avoids premature microservices complexity. Centralizes PHI/De-ID enforcement.
**Constraint:** Must expose strictly separate API surfaces for Patient, Clinician, and Research consumers.

## 2. PHI System of Record
**Decision:** Medplum (FHIR).
**Rationale:** Industry standard for interoperability. Handles complex clinical data modeling (fhir resources) + Auth + RBAC.
**Configuration:**
- Access via `MEDPLUM_BASE_URL` (must have trailing slash).
- Env vars must use standard upper-case format (e.g., `MEDPLUM_DATABASE_HOST`) where supported, or be mapped correctly in the container.

## 3. Research & Analytics Database
**Decision:** TigerGraph (Graph) + PostgreSQL (OMOP/Analytics).
**Rationale:** 
- TigerGraph chosen for multi-hop hypothesis discovery and pathway analysis in the de-identified zone.
- Postgres for standard OMOP cohorting and descriptive stats.
**Access Control:** NO direct frontend access. All queries proxied via `services/api`.

## 4. Frontend Technology
**Decision:**
- Patient: React Native (Expo)
- Clinician: Next.js (Web)
- Research: Next.js (Web)
**Rationale:** Best-in-class tools for respective form factors.

## 5. Deployment
**Decision:** Coolify with Split Stacks.
- **Stack A (Medplum):** Postgres + Redis + Medplum Server + Medplum App.
- **Stack B (Starvit):** API + Frontends.
**Rationale:** Decouples the "infrastructure" (PHI store) from the "product" (Starvit app), allowing independent scaling and maintenance.
