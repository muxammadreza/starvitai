---
description: Incident response (IC + tech lead) and postmortem template
---

Use this workflow when there is user-visible impact, data integrity risk, or suspected security/privacy exposure.

Roles (assign explicitly):
- Incident Commander (IC): coordinates, communicates, delegates, time-boxes.
- Tech Lead (TL): drives technical diagnosis and mitigation.
- Scribe: maintains timeline and decisions.
- Comms Lead (optional): stakeholder updates.

1) Declare the incident
- Start time (UTC), severity (SEV1–SEV3), impacted surfaces (patient app, clinician dashboard, backend, FHIR store, de-ID pipeline).
- Create a single source of truth (incident channel + doc).

2) Stabilize first (time-box 15–30 min)
- Prefer reversible mitigations: feature flags, rate limits, rollback, disable risky exports.
- If PHI exposure suspected: stop egress, rotate credentials (human-approved), preserve logs, notify privacy/compliance path.

3) Diagnose (parallelize safely)
- TL forms hypotheses and assigns investigations:
  - recent deploys, migrations, config changes
  - error budget/SLO burn, golden signals (latency, traffic, errors, saturation)
  - data pipeline failures (DLP/de-ID, BigQuery loads, graph ingest)
- Scribe records:
  - hypothesis → test → result → next step
  - commands executed and by whom (no secrets pasted)

4) Mitigate and verify
- Apply fix/rollback; verify recovery via dashboards + synthetic checks + user journeys.
- Confirm no data corruption (spot checks, checksums, reconciliation queries).

5) Close
- Document end time, customer impact, and current status.
- Create follow-up tickets with owners.

6) Postmortem (blameless) draft
Include:
- Summary and impact
- Timeline (key events)
- Root cause(s) and contributing factors
- Detection and response gaps
- Corrective actions (prevent recurrence) with owners and due dates
- What went well / what didn’t

Deliverables:
- Incident summary + timeline
- Postmortem draft + action items
