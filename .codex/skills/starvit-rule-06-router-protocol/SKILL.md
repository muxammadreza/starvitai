---
name: starvit-rule-06-router-protocol
description: Starvit uses Antigravity **Rules** (persistent guardrails) and **Workflows** (saved, repeatable playbooks).
---

# Starvit Router Protocol

Starvit uses Antigravity **Rules** (persistent guardrails) and **Workflows** (saved, repeatable playbooks).

- Workspace rules live in `.codex/rules/`.
- Workspace workflows live in `.codex/workflows/` and must be Markdown files that start with YAML frontmatter containing a `description`.

## When this protocol applies

If the user request involves **implementation work** (any code/infra/data/graph/ML change, security/compliance work, deployments, or docs changes that accompany code), the agent MUST route the request before executing.

If the user is asking a **pure question** (explanation, comparison, quick guidance) with no implied repo changes, answer normally.

## Routing-first requirement

1) Read and follow `$starvit-wf-router`.
2) The router MUST:
   - classify the request into impacted surfaces (frontend, mobile, backend, data, graph, ML, ops, security)
   - determine **risk tier** (PHI/auth/data-movement/model-risk)
   - choose the **lead role** and required supporting roles
   - select the exact workflows (file paths) and order of execution
   - list required gates (security/privacy, critic reviews, release readiness)
   - decide whether to run as a single-agent sequence or to propose a multi-agent dispatch plan

## Operating modes (required)

- For Tier 2+ work (anything touching PHI boundaries, auth/RBAC, data pipelines, graph queries, or ML): use **Planning** mode.
- Terminal auto-execution should remain **Off** unless a workflow explicitly marks a safe command with `// turbo` (per workflow conventions).
- If there is any ambiguity that could cause unsafe behavior, the router should proceed with a safe default plan and request only the minimum missing input.

## Output contract

For routed work, the agent response must begin with a short **Dispatch Plan** that includes:

- Primary objective (1 sentence)
- Classified domains (bullet list)
- Risk tier + why
- Selected workflows (ordered list of paths)
- Roles/agents (lead + gates)
- Verification plan (tests, QA, observability)
- Deliverables (PR diff, evidence, docs, runbooks)

This protocol does not replace domain workflows; it forces consistent routing so Starvit stays project-aware, secure, auditable, and coherent.

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
