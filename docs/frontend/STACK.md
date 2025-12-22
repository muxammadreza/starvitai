# Frontend Stack (Starvit)

This document is the canonical reference for frontend libraries and conventions.

## Web apps

Applies to:
- `apps/clinician`
- `apps/research`

Baseline:
- Next.js (App Router) + TypeScript
- Tailwind + CSS variables
- Radix Primitives + shadcn/ui components (in-repo code)
- TanStack Query for server state
- React Hook Form + Zod for forms
- TanStack Table + TanStack Virtual for large datasets
- Recharts for time-series and summary charts
- React Flow for graph exploration (research only)

## Mobile app

Applies to:
- `apps/patient`

Baseline:
- Expo + TypeScript + React Navigation
- React Hook Form + Zod
- TanStack Query
- Offline-first write queue (measurement logging)

## Why this stack

- Accessibility primitives (Radix)
- Repo-owned components (shadcn/ui) for auditability and customizability
- Strong typed contracts via OpenAPI-generated clients
- Proven patterns for large data UIs (TanStack Table/Virtual)
