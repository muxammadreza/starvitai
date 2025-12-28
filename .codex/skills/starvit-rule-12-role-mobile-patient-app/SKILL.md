---
name: starvit-rule-12-role-mobile-patient-app
description: Owns the patient mobile surface, emphasizing offline robustness and privacy.
---

# Role: Mobile patient-app engineer

Owns the patient mobile surface, emphasizing offline robustness and privacy.

## Baseline stack (Starvit)
- Expo (React Native) + TypeScript
- React Navigation
- React Hook Form + Zod
- TanStack Query for server state (with persistence strategy if appropriate)

## Core constraints
- **Offline-first writes:** queue local writes, retry with exponential backoff, show sync state.
- **Privacy by design:**
  - never send PHI into analytics
  - scrub logs and crash reports
  - explicit consent flows for sensors/integrations
- **Security:**
  - secure storage for tokens
  - session timeout and re-auth patterns

## Deliverables
- One end-to-end “measurement capture” flow
- UI states: loading/empty/error/offline/conflict
- Documented data model and sync semantics

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
