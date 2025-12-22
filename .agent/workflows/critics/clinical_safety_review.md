---
description: Clinical safety review for protocol-related and metabolic-therapy changes (KMT / monitoring / decision support)
---

Use this workflow whenever a change could:
- add or alter protocol engine logic,
- change how glucose/ketones or derived metrics are calculated or displayed,
- add “suggestions” or “recommendations” for clinicians,
- change safety/contraindication gates,
- or expose research/ML outputs to clinicians.

## Inputs

- PR/RFC/ADR and the exact diff (or proposed schema change)
- Which user surfaces are affected (clinician web, patient mobile, research workbench)
- Any new claims being implied (explicitly or via UX)

## Review checklist

### 1) Scope and framing
- Does the feature remain **clinician-supervised**?
- Is it clearly **monitoring/visualization** versus **recommendation**?
- If recommendation-like, is the **basis independently reviewable** (evidence card + provenance) and gated by clinician sign-off?

### 2) Safety gates (non-bypassable)
- Confirm gates exist for the “stop and escalate” categories in `docs/clinical/SAFETY_RED_FLAGS.md`.
- Verify there is no pathway (UI or API) that can bypass clinician approval.
- Confirm override behavior is logged and requires a reason.

### 3) Unit correctness and calculational integrity
- Verify glucose and BHB units are explicit and consistent (mmol/L end-to-end).
- Verify any conversion logic is tested (including edge cases like missing ketones).
- Verify derived metrics (e.g., GKI) are computed server-side, versioned, and logged.

### 4) Host fragility / cachexia safeguards
- Confirm the platform does not incentivize “chasing GKI” or weight loss.
- Confirm cachexia risk is treated as a red-flag gate and is visible to clinicians.

### 5) Adverse event and escalation UX
- Ensure clinician dashboard includes clear warning states.
- Ensure patient app phrasing avoids prescriptive medical guidance.
- Ensure escalation pathways are defined (what triggers a clinician review, what is recorded).

### 6) Auditability
- Confirm the audit trail captures:
  - inputs (source + timestamp)
  - transforms/derived metrics + version
  - gate outcomes
  - clinician decision (approve/override) + reason
  - model/protocol version identifiers

### 7) Evidence hygiene
- Any clinical claim must have an evidence card (`workflows/clinical/evidence_card.md`).
- Ensure uncertainty and applicability constraints are displayed in clinician-facing views.

## Output

- **Required fixes** list (blocking)
- **Nice-to-haves** list (non-blocking)
- Safety sign-off checklist with reviewer name/role and version identifiers
