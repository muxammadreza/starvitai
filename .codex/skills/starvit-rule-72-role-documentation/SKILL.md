---
name: starvit-rule-72-role-documentation
description: Update docs/runbooks/ADRs in the same PR as code changes that alter behavior or contracts. - Treat docs as **auditable artifacts** in a clinical product -> clear purpose, intended user, assumptions, and limitations - “what changed” and “why” for any protocol/model behavior changes - copy/pastable commands with expected outputs (no secrets) - Keep a single source of truth -> architecture -> `docs/ARCHITECTURE.md` -> decisions/ADRs -> `docs/DECISIONS.md` -> agent rules:...
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
  - agent rules: `.codex/rules/**`
  - agent workflows/runbooks: `.codex/workflows/**`

## Required doc updates (when relevant)

- New endpoint or contract change → update API docs + examples + error cases.
- New metric/derived feature → update formula, units, validation, provenance.
- New pipeline → update lineage diagram + retention + de-ID checkpoints.
- New operational behavior → update SLOs, alerts, dashboards, rollback.

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
