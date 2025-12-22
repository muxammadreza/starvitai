---
description: Protocol engine change (schema/state machine/derived metric)
---

Use this workflow for any change that could alter clinician-facing protocol behavior.

Steps:
1) Define the change precisely:
   - what state(s)/transition(s)/threshold(s) changes
   - what inputs are required (FHIR Observations, QuestionnaireResponses, etc.)
   - intended effect and non-goals
2) Safety framing:
   - confirm outputs remain “clinician approval required”
   - identify potential harms (false positives, false negatives, alert fatigue)
3) Independently reviewable basis:
   - update the plain-language rationale shown in clinician UI
   - ensure provenance is displayed (protocol version, last updated)
4) Versioning + migration:
   - bump protocol schema/version
   - write migration/compat notes for existing CarePlans
   - define rollback path
5) Implementation:
   - implement validator and state machine updates server-side
   - add unit tests for edge cases and unit conversions
   - add scenario tests using representative patient timelines (synthetic)
6) Gates:
   - run clinical safety review workflow
   - run security/privacy gate
   - ensure audit logging for protocol approvals/overrides
7) Docs:
   - update `docs/DECISIONS.md` and any protocol documentation
   - update evidence mapping if rationale is evidence-derived

Deliverables:
- ADR entry + protocol changelog
- Tests + scenario validations
- UI provenance/rationale updates
