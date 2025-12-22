---
trigger: always_on
---

## Documentation is a deliverable

- Update docs/runbooks/ADRs in the same PR as code changes that alter behavior or contracts.
- Treat docs as **auditable artifacts** in a clinical product:
  - clear purpose, intended user, assumptions, and limitations
  - “what changed” and “why” for any protocol/model behavior changes
  - copy/pastable commands with expected outputs (no secrets)
- Keep a single source of truth:
  - architecture: `docs/ARCHITECTURE.md`
  - decisions/ADRs: `docs/DECISIONS.md`
  - agent rules: `.agent/rules/**`
  - agent workflows/runbooks: `.agent/workflows/**`

## Required doc updates (when relevant)

- New endpoint or contract change → update API docs + examples + error cases.
- New metric/derived feature → update formula, units, validation, provenance.
- New pipeline → update lineage diagram + retention + de-ID checkpoints.
- New operational behavior → update SLOs, alerts, dashboards, rollback.
