---
trigger: always_on
---

## Clinical informatics & safety (Starvit)

You are working on a clinician-supervised system that can *suggest* protocol actions and analytics, but cannot make autonomous medical decisions.

### Non-negotiables
- Protocol logic is **server-side**, **versioned**, and **auditable**.
- UI can *edit/visualize* protocol schemas/state machines; it must not introduce hidden behavior.
- Any output that could influence care MUST be labeled **“clinician approval required”** and treated as non-binding.

### “Independently reviewable basis” requirement
For any clinical-facing suggestion (rule-based or ML-based), ensure a clinician can independently review the basis:
- show required inputs (what data was used, time windows, units)
- show the applied logic in plain language (rules, thresholds, state transitions)
- show provenance (protocol version, model version, feature set version, last-updated timestamp)
- surface limitations/uncertainty and contraindications as *flags*, not directives.

### Data semantics
- Use FHIR R4 correctly for PHI (Observation/Condition/MedicationRequest/CarePlan/etc.).
- Avoid leaking identifiers into de-identified zones; ensure de-ID happens *before* any analytics/graph loading.
- Derived metrics (e.g., GKI) must clearly state units, formula, and source observations.

### Change control
- Any protocol schema change requires:
  - an ADR entry (what/why/risks)
  - migration/compat plan (existing CarePlans/QuestionnaireResponses)
  - tests and clinical safety review (edge cases, unit conversions, false positives/negatives)
  - rollback path.
