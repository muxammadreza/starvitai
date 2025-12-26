# Medplum Bots in Starvit

## Why Bots
Medplum Bots allow server-side logic to run **inside** the PHI boundary:
- compute derived metrics (e.g., GKI) from Observations
- create/update workflow artifacts (Task/Communication) for clinician review
- react to events via FHIR Subscriptions

## Starvit conventions
- Prefer Bots when the computation:
  - requires PHI access
  - should be auditable within the PHI system of record
  - should be event-driven (new Observation triggers)
- Prefer Starvit backend services when:
  - logic is non-PHI (admin, analytics orchestration, de-ID pipeline)
  - the job requires heavy compute or long-running workflows

## Bot implementation conventions
- Bot code: TypeScript.
- Store integration keys as Medplum Project secrets.
- Do not log PHI.

## Event triggering
- Use FHIR `Subscription` resources to trigger Bots on create/update.
- Use idempotency keys (e.g., based on triggering resource id + lastUpdated) to avoid duplicate actions.

## Approval workflow
- Bots may create a `Task` with status `requested` and a payload describing the recommendation.
- Clinician approval should move status to `accepted`/`completed` and record a `Provenance` referencing the Task and relevant Observations.

## Deliverables
- Bot source code under `services/medplum-bots/*` (or equivalent).
- Subscription manifests (FHIR JSON) under `docs/fhir/subscriptions/*`.
- Integration tests in a Medplum dev Project.
