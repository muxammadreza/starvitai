# API contracts & client generation (Starvit)

The backend OpenAPI schema is the single source of truth. Frontends must never hand-roll ad-hoc request shapes.

## Why
- Fewer integration bugs.
- Faster refactors with compile-time failures.
- A clean surface for contract tests.

## Workflow
1) **Backend changes merge with OpenAPI update**
   - confirm schema changes are intentional and reviewed
2) **Regenerate clients**
   - use Orval (or project-standard generator)
   - produce types + clients (+ optional React Query hooks)
3) **Contract guard in CI**
   - CI fails if OpenAPI changed and clients were not regenerated
4) **Breaking change protocol**
   - version endpoints or add fields compatibly
   - coordinate backend + frontend PRs

## Contract testing
- Provider tests assert the server matches OpenAPI.
- Consumer tests exercise the **real client code** with mocked provider responses.

## Outputs
- generated types/models
- generated client functions
- optional React Query hooks
- optional MSW mocks for UI dev
