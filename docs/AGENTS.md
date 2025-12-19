# Starvit — Antigravity Agent Rules (Authoritative)

## 0) Prime Directive (non-negotiable)
Starvit is a clinical-grade platform for **metabolic therapy support** (initially oncology; later diabetes/metabolic disease).
Agents MUST optimize for:
1) Patient safety + clinician oversight (no autonomous medical decisions)
2) PHI/PII segregation + auditability
3) Fast MVP delivery via a modular monolith (NOT premature microservices)
4) Reproducible science (de-identified research layer; traceable features)

If any instruction conflicts with safety/PHI boundaries, PHI boundaries win.

---

## 1) What we are building (3 products, 1 backend)
### 1.1 Patient product (mobile)
- Purpose: log measurements + protocol adherence + symptoms; integrate wearables/sensors later.
- Tech: React Native (Expo) preferred for MVP.

### 1.2 Clinician product (web dashboard)
- Purpose: monitor patients, review metrics (glucose, ketones, GKI), adjust protocols, visualize protocol flows (React Flow).
- Tech: Next.js (TypeScript) preferred.

### 1.3 Research product (web + notebooks/workbench)
- Purpose: de-identified exploration, cohort definitions, feature engineering, model eval, causal/graph analytics.
- Tech: Next.js for UI + Python for analysis/training.

### 1.4 Backend rule
We do **NOT** build 3 backends. We build **one** backend platform with:
- multiple API surfaces (patient/clinician/research) via RBAC scopes
- strong domain modules (PHI, protocol engine, analytics, ML)
- asynchronous pipelines for ingest + ETL + training

---

## 2) Enterprise-grade data architecture (PHI boundary + de-ID boundary)
### 2.1 PHI zone (identifiable clinical data)
- Store and exchange PHI using **FHIR resources** (Patient, Observation, Condition, CarePlan, QuestionnaireResponse, etc.).
- Use a FHIR-native backend (Medplum is acceptable) as the “system of record” for PHI.
- All PHI access requires authentication + RBAC + audit logs.

FHIR exists to standardize electronic exchange of healthcare data; use it as the canonical schema for PHI. (FHIR overview and guidance are primary references.)

### 2.2 De-identified zone (research / model training)
- Research database must be **de-identified/pseudonymized** and separated from the PHI zone.
- Use **OMOP CDM** tables for observational analytics and cross-study comparability.
- Graph relationships live here (gene–lab–phenotype–protocol link discovery).

### 2.3 “No direct graph access” rule
Frontends NEVER talk directly to TigerGraph (or any graph DB).
All access goes through the backend’s Research API, which enforces:
- de-ID constraints
- query allowlists / cost controls
- provenance logging (what query, what cohort, what features)

---

## 3) Graph layer choice (TigerGraph placement + why)
### 3.1 Placement
TigerGraph is part of the **De-identified zone** only:
- It stores relationships among de-identified entities (PatientPseudoID, labs, phenotypes, variants, pathways, protocol parameters, outcomes).
- It is queried by backend services (Research API + Feature Store builder), not by UI clients.

### 3.2 When to use the graph vs OMOP tables
- Use OMOP for cohorting, descriptive stats, reproducible observational studies.
- Use graph for:
  - multi-hop hypothesis discovery (A→B→C)
  - similarity search (patient-to-patient, tumor subtype clusters)
  - pathway-level link discovery and feature generation
  - causal adjacency candidates (to be validated)

TigerGraph’s GSQL is designed for scalable graph analytics; prefer it when relationships and traversals are core.

---

## 4) Protocol engine (domain logic, not UI logic)
### 4.1 Clinical concept model (minimum)
- Protocol = versioned plan with states, constraints, and monitoring requirements.
- ProtocolStep = meal rules, fasting windows, supplements, pulses (if applicable), measurement schedule.
- Measurement = glucose, β-OHB ketones, weight, BP/HR, symptoms, labs.
- Derived metric = **GKI** (glucose/ketones in mmol/L).
- Safety constraints = cachexia risk flags, contraindications, thresholds.

### 4.2 “Press–Pulse” is a reference pattern, not a hard-coded dogma
Use the KMT literature as a knowledge base:
- cancer as metabolic/mitochondrial disease framing
- Press–Pulse strategy
- GKI as a key dynamic biomarker
- explicit contraries/risks (e.g., cachexia acceleration in some contexts; ketone-utilizing tumors in some subtypes)

Agents must implement protocol logic as **config + rules**, not scattered if/else in UI.

---

## 5) AI/ML layer (strict boundaries)
### 5.1 MVP AI principle
Start with “AI-assisted recommendations” that are:
- explainable
- reviewable by clinicians
- logged (inputs → outputs)
- safe defaults (do not intensify protocols autonomously)

### 5.2 Training vs inference separation
- Training: offline pipeline on de-identified data (OMOP + graph features).
- Inference: a versioned model service behind the backend API.
- Every model output includes:
  - model version
  - feature set version
  - confidence/uncertainty
  - rationale summary
  - “clinician must approve” flag

---

## 6) Monorepo rules (how we build as an enterprise, even as solo)
### 6.1 Monorepo
Use Turborepo to manage multiple apps/packages in one repo.
- `apps/` contains patient app + clinician dashboard + research UI
- `packages/` contains shared UI, shared types, shared API clients, shared protocol schemas
- `services/` contains backend + workers

Turborepo caching depends on correctly defined task outputs in `turbo.json`.

### 6.2 “Modular monolith” default
Backend stays one deployable (for MVP) with internal modules:
- auth/rbac
- fhir/phi gateway
- protocol-engine
- ingest
- research-api
- feature-store builder
- model-serving adaptor
Workers can be separate processes, but do NOT fragment the domain prematurely.

---

## 7) Antigravity-specific agent safety guardrails (mandatory)
Antigravity can connect agents to enterprise data via MCP servers (e.g., BigQuery, Cloud SQL, Looker).
Because agentic IDEs can execute commands, we enforce the following:

### 7.1 No destructive shell by default
Agents must NOT run or suggest commands that:
- delete files recursively
- wipe drives
- mass-remove directories
- print secrets

Any operation resembling deletion/migration must be:
1) explained
2) scoped to a narrow path
3) require explicit human confirmation

### 7.2 Secret hygiene
- Never read `.env`, credentials, tokens, private keys, or output them into chat.
- Use secret managers / injected runtime secrets only.

### 7.3 MCP usage policy
Agents may use MCP tools for:
- schema inspection
- read-only queries
- safe migrations (with review)
But must prefer **read-only** queries unless explicitly told otherwise.

---

## 8) Coding rules (how agents must write code here)
1) TypeScript for web apps + shared packages.
2) Python 3.13 for ML + analytics + FastAPI backend.
3) Every feature must include:
   - tests (unit at minimum)
   - logging (structured)
   - a clear data contract (types/schema)
4) No direct DB calls from frontends (ever).
5) Feature flags for anything patient-impacting.
6) Migrations must be reversible.
7) Use Poetry for Python dependency management.

---

## 9) “Definition of Done” for any PR generated by an agent
A change is not done unless:
- boundaries (PHI vs de-ID) are respected
- RBAC is enforced at API level
- audit trail exists for clinician actions and model outputs
- docs updated (at least a short note in `/docs/changes/`)
- build + tests pass via Turborepo pipelines

---

## 10) Knowledge base (authoritative internal references)
Agents must treat these as the project’s scientific grounding:
- all research papers in docs/research

(These docs are not clinical advice; they inform protocol modeling + hypothesis space.)
