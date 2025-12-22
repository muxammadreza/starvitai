---
trigger: always_on
---

# Starvit Frontend Stack (Web)

This rule is the **source of truth** for web-frontend tech choices for Starvit.

## Target apps

- `apps/clinician` (Clinician Dashboard)
- `apps/research` (De-identified analytics + graph exploration)
- `packages/ui` (shared design-system components for web)

## Baseline stack (approved)

- Framework: **Next.js (App Router) + TypeScript**
- Styling: **Tailwind CSS** with CSS variables for theming; no CSS-in-JS.
- Component primitives: **Radix UI Primitives** (accessibility-first primitives).
- Design-system distribution: **shadcn/ui** (components are copied into repo; we own the code).
- Icons: `lucide-react`
- Forms: **React Hook Form + Zod** (schema-first validation; no ad-hoc validators).
- Server state: **TanStack Query** for caching, retries, pagination, optimistic updates.
- Tables / lists:
  - `@tanstack/react-table` (headless table)
  - `@tanstack/react-virtual` for virtualization on large cohorts/logs
- Charts: `recharts` for clinical trends and summary charts (prefer simple, readable charts).
- Graph UI (research workbench only): `@xyflow/react` (React Flow) for node-based exploration.

## Contract-first API integration

- Starvit backend is **FastAPI** and publishes OpenAPI.
- Web apps must use **generated clients** from OpenAPI (Orval preferred) to avoid drift.
- All network calls must:
  - be typed
  - use bounded retries/timeouts
  - expose correlation IDs (request id) in logs where available

## Performance + UX constraints

- Default to Server Components for layouts and static pages; use Client Components only where interactivity is needed.
- Large lists must be virtualized (cohorts, audit logs, observations timeline).
- Avoid heavyweight UI libraries that duplicate shadcn/Radix (e.g., do not add MUI/AntD unless a specific missing capability is justified and approved).
- Always implement: loading / empty / error / partial-data states.
- Never rely on implicit caching defaults: specify cache/revalidate behavior explicitly per call site.

## Accessibility + clinical usability

- Follow WCAG 2.2 AA as a baseline.
- Keyboard navigation is non-negotiable for data-heavy screens.
- All clinical metrics must display provenance: measurement source + timestamp + units + calculation rule/version when derived.

## Security posture (web)

- Never store access tokens in `localStorage`/`sessionStorage`.
- Prefer HttpOnly secure cookies or token-in-memory strategies; ensure CSRF posture is defined for cookie-based auth.
- Do not render PHI in research. Only de-identified datasets are allowed.