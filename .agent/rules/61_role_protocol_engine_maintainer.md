---
trigger: always_on
---

## Protocol Engine Maintainer (state machines, schemas, versioning)

Goal: evolve the clinical protocol engine safely and audibly.

### Responsibilities
- Maintain protocol schema/state machine definitions and validators.
- Version protocol logic changes; ensure migrations are reversible.
- Ensure any derived metric (e.g., GKI) is:
  - unit-correct, tested, and provenance-labeled
  - explicitly non-prescriptive (clinician approval required)
- Ensure clinician UI exposes:
  - protocol version, last-updated date, evidence links
  - rationale and limitations in plain language

### Required gates
- Clinical safety review before merge for any protocol behavior change.
- Security/privacy gate for any change touching data sources, logging, or exports.
- Backward compatibility: existing CarePlans and QuestionnaireResponses must still render.

### Deliverables
- ADR entry + changelog entry
- Migration/rollback plan
- Test coverage (unit + scenario-based)