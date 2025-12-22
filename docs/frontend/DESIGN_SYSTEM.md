# Design System (Starvit)

## Tokens

Use CSS variables (web) as canonical tokens:
- colors (background, foreground, muted, destructive, warning, success, info)
- radii
- spacing scale
- typography scale

## Clinical UI patterns

- Every metric shows: value, unit, timestamp, provenance.
- Derived metric cards show formula + version.
- Alerts use label + icon + color (never color only).

## Component governance

- Shared components live in `packages/ui`.
- New shared component requires:
  - examples
  - a11y notes
  - tests (critical interactions)
