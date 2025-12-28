---
name: starvit-rule-18-design-system-web
description: Starvit Design System Rules (Web)
---

# Starvit Design System Rules (Web)

## Design system goals

- High information density without visual clutter (clinical dashboard).
- Consistent components across clinician + research web apps.
- Accessible by default (Radix primitives).
- Minimal bundle overhead (no heavy theming frameworks).

## Implementation

- Use **shadcn/ui** components as the baseline (owned code; customize in-repo).
- Use **Radix Primitives** for behavior and accessibility.
- Styling:
  - Tailwind + CSS variables for tokens (colors, radii, spacing, typography).
  - Keep variants in `class-variance-authority` (CVA) when applicable.
- Component location:
  - Shared primitives in `packages/ui`
  - App-specific composites live in each app (e.g., `ClinicianMetricCard`, `ObservationTimeline`)

## Clinical UI conventions

- Units are mandatory (mmol/L vs mg/dL; convert explicitly and label).
- Date/time must include timezone or be normalized to user's configured TZ.
- Derived metrics must show formula and version (e.g., `GKI v1: glucose(mmol/L)/ketones(mmol/L)`).
- Warning styles: use text + icon + color (never color alone).

## Accessibility checklist per component

- Labeling: programmatic labels for every interactive control.
- Focus: visible focus, focus order matches reading order.
- Keyboard: all interactions possible without mouse.
- ARIA: only when needed; prefer native semantics; Radix provides patterns.

## Documentation

- Every shared component must include:
  - usage example
  - props/variants
  - a11y notes
  - test coverage expectations

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
