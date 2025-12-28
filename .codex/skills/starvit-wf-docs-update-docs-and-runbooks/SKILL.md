---
name: starvit-wf-docs-update-docs-and-runbooks
description: Update documentation and operational runbooks after a change
---

# Update documentation and operational runbooks after a change

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

## When to use
Any time you introduce or change:
- an API contract
- a data schema or pipeline
- a model version or feature set
- an operational behavior (timeouts, retries, permissions)

## Steps
1) Update the relevant `docs/*` pages:
   - architecture overview
   - service docs
   - data contracts
   - clinical protocol docs (if affected)
2) Update runbooks:
   - known failure modes
   - rollback steps
   - dashboards/alerts links
3) Add an ADR if a decision is significant (trade-offs documented).

## Output
PR includes doc updates and a brief "How to operate" section.

