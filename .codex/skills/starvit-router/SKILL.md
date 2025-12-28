---
name: starvit-router
description: Route a task to the right Starvit role + workflow skills, then execute with safety and audit constraints.
---

# Starvit Router (Codex)

Use this skill first when the user request is ambiguous, cross-cutting, or risks violating Starvit non-negotiables.

## Routing protocol (high level)

1. Identify **domain**: backend/platform, frontend web, mobile, data/analytics, graph, ML/AI, security/privacy, SRE/ops, clinical/research/regulatory.
2. Identify **risk tier**:
   - **High**: touches PHI, clinical recommendations, authn/authz, secrets, infra, security controls, regulatory/SaMD.
   - **Medium**: product logic, data transforms, integrations, observability.
   - **Low**: docs, refactors, linting, non-production scripts.
3. Select the **workflow skill**:
   - Planning or ambiguous: `$starvit-wf-00-triage-and-plan`
   - Cross-cutting change: `$starvit-wf-01-change-design-rfc-adr`
   - Implementation: `$starvit-wf-02-implement-with-tests`
   - Security/privacy checkpoint: `$starvit-wf-03-security-privacy-gate`
   - Release: `$starvit-wf-04-release-readiness`
   - After merge: `$starvit-wf-05-post-merge-followups`
4. Select the **role / rule skills** that apply:
   - Always include `$starvit-rule-00-nonnegotiables`
   - Then include the relevant role skill(s) (e.g., backend, data, clinical safety) and any topical rules (e.g., Medplum, IAM, audit).

## How to execute in Codex

- In the Codex chat, you can explicitly invoke skills by typing `$` and selecting the skill.
- Apply **router → workflow → role/rules**.
- Produce deliverables explicitly (plan, ADR, threat model, checklists) and keep PHI boundaries intact.

## Reference

- See `references/router_map.yml` for the detailed routing matrix (Antigravity-origin).
