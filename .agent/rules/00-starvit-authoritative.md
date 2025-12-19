---
trigger: always_on
---

# Starvit — Antigravity Rules (Authoritative)

## A) What Starvit is (1 sentence)
Starvit is a clinician-supervised metabolic-therapy support platform (oncology first; diabetes/metabolic disease later) with strict PHI controls and a de-identified research/ML layer.

## B) Non-negotiables (agents must obey)
1) **No autonomous medical decisions.** The system can suggest, but clinicians approve and actions are logged.
2) **PHI boundary is sacred.** PHI stays in FHIR/Medplum + controlled storage; research/ML uses de-identified data only.
3) **One backend for MVP (modular monolith).** Multiple UIs, not multiple backends.
4) **Every recommendation is audit-able.** Inputs → outputs → model version → clinician decision.

## C) Product surfaces (3 UIs, 1 platform backend)
1) **Patient app (mobile)**: logging measurements, adherence, symptoms; sensor integrations later.
2) **Clinician dashboard (web)**: monitor cohorts/patients, review glucose/ketones/GKI trends, edit protocols visually (React Flow), approve suggestions.
3) **Research workbench (web + notebooks later)**: de-identified cohorting, feature engineering, graph exploration, model evaluation.

## D) Enterprise-style architecture (how the pieces connect)
### D1) “System of record” for PHI: Medplum (FHIR)
- PHI is represented as **FHIR resources** (Patient, Observation, Condition, CarePlan, QuestionnaireResponse, etc.). FHIR is the interoperability standard for exchanging healthcare data.
- Medplum supports SMART-on-FHIR and OAuth2-based auth patterns; treat it as the PHI “truth” layer.
- Medplum server config via env vars uses `MEDPLUM_*` + nested prefixes like `MEDPLUM_DATABASE_HOST`, `MEDPLUM_REDIS_HOST` (NOT double-underscore casing).
- Medplum `baseUrl` must be a fully-qualified URL **with a trailing slash**.

### D2) De-identified zone (research/ML)
- De-identified analytics uses **PostgreSQL (OMOP schema)** for cohorting/stats.
- **TigerGraph** is the designated Graph DB for complex relationship discovery (no Neo4j).
- ETL into OMOP is a formal “thing”; plan for it rather than inventing random tables forever.

### D3) Graph layer placement (NO direct UI access)
- Graph DB (TigerGraph) lives **only** in the de-identified zone.
- Frontends never talk to graph DB directly. All graph access goes through `services/api` (Research API) which enforces:
  - allowlisted queries
  - de-ID constraints
  - provenance logging

TigerGraph is used:
- Auth + tokens/JWT handling must follow TigerGraph’s API auth model; note plaintext tokens are being deprecated in favor of OIDC JWT in newer versions.

## E) Clinical protocol engine rules (domain logic)
- Protocol logic is **server-side** and versioned. UI only edits a schema/state-machine definition.
- Required derived metric for MVP: **GKI** (glucose/ketones in mmol/L).
- The metabolic therapy knowledge base is stored in `docs/research/` and must be treated as “modeling references,” not as patient advice.

## F) AI/ML rules (safe-by-design)
- Training is offline on **de-identified** datasets.
- Inference is behind the backend API and must return:
  - model version
  - feature set version
  - uncertainty/confidence
  - short rationale
  - “clinician approval required” flag
- No self-modifying protocols in production.

## G) Repo conventions (monorepo discipline)
- Monorepo uses Turborepo; Turborepo runs tasks from package scripts and orchestrates via `turbo.json`.
- Turborepo task outputs must be correct for caching to work; package-level overrides are allowed via per-package `turbo.json` that `extends` root config.
- Apps go in `apps/*`, shared libs in `packages/*`, backend in `services/*`, infra in `infra/*`.
- Python version: **3.13** mandatory for all backend and ML services.
- Python dependency management: **Poetry**.

## H) Security + ops guardrails (agent execution safety)
- Never print secrets (.env, tokens, keys) into chat or commits.
- Never run destructive shell commands (rm -rf, wipe volumes, delete databases) unless explicitly instructed and scoped to a narrow path.
- All PHI endpoints require RBAC + audit logging.

## I) Definition of Done (agent work is not “done” unless)
- PHI/de-ID boundary is respected
- RBAC enforced at API level
- audit trail exists for clinician actions and model outputs
- minimal tests exist + builds run under Turborepo
- docs updated (even a short note)