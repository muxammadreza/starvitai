---
name: starvit-rule-69-role-patient-safety-monitoring
description: Owns safety signal triage and clinical risk controls for anything that could influence care.
---

# Role: Patient safety monitoring

Owns safety signal triage and clinical risk controls for anything that could influence care.

## Scope
- Protocol suggestion outputs
- Alerts/notifications to clinicians
- Patient-facing guidance copy (even when “non-medical”)

## Requirements
- Every suggestion must include:
  - evidence link (internal citation)
  - uncertainty/confidence label
  - explicit “clinician approval required” flag
- Safety signals:
  - unexpected adverse events
  - abnormal metric patterns
  - user-reported symptoms

## Deliverables
- Safety signal triage workflow + severity rubric
- Audit log fields for safety events

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
