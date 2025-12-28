---
name: starvit-rule-21-frontend-stack-mobile
description: This is the baseline for `apps/patient-mobile`.
---

# Starvit Frontend Stack (Mobile / Patient App)

This is the baseline for `apps/patient-mobile`.

## Baseline stack (approved)

- Framework: **React Native (Expo) + TypeScript**
- Navigation: React Navigation
- Styling: prefer `nativewind` (Tailwind-style) OR a minimal token system aligned with web CSS variables (choose one; document it).
- Forms: React Hook Form + Zod
- Server state: TanStack Query (React Native supported)
- Offline posture:
  - queue writes locally when offline
  - reconcile with server when online
  - show sync status clearly

## Clinical logging constraints

- Measurement entry must enforce units and ranges.
- Derived metrics are computed server-side for auditability (client may preview but backend is source-of-truth).
- No PHI in analytics events; telemetry must be privacy-reviewed.

## Security

- Do not store tokens in plaintext on device.
- Use platform secure storage for session secrets (Keychain/Keystore) if needed.

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
