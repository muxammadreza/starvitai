# Starvit agent guidance (portable across agentic platforms)

This repository ships an **agent pack** designed for Antigravity IDE and compatible tooling. Some platforms will not automatically load `.agent/rules/*` or understand `.agent/workflows/*`. This document provides a **portable operating contract** so that Codex, Copilot, Claude Code, Cursor, Windsurf, Aider, Gemini CLI, and similar tools can still execute Starvit work correctly.

## Source of truth

- **Operational rules + role rules:** `.agent/rules/`
- **Playbooks (“workflows”):** `.agent/workflows/`
- **Routing map (how to pick the right playbooks):** `.agent/router/router_map.yml`
- **Human-facing overview:** `docs/ROUTER.md` and `docs/DEVELOPMENT_OPERATING_MODEL.md`

If your platform does not have a native “rules/workflows” concept, treat these files as:

- **Rules** = non-negotiable constraints to include *up-front* in the agent’s system/prefix context.
- **Workflows** = runbooks to execute step-by-step.

## Non-negotiables (Starvit)

1. **No autonomous medical decisions.** Agents may draft suggestions; clinicians approve. Everything must be auditable.
2. **PHI boundary is sacred.** PHI lives only in **Medplum FHIR store (FHIR R4)**. Research/ML layers use **de-identified data only**.
   - Medplum admin/config changes MUST be performed via the configured **Medplum MCP server**.
   - Implementation MUST be compatible with **Medplum v5.0.10+** (avoid deprecated APIs).
3. **One backend for MVP (modular monolith).** Multiple UIs are permitted; multiple backends are not.
4. **Every recommendation is audit-able.** Inputs → outputs → model version → clinician decision must be traceable.
5. **TigerGraph lives only in the de-identified zone.** UI never talks to TigerGraph directly; access is via allowlisted Research API queries.

## Universal execution contract (what every agent must do)

### A) Always start by routing

If the user request implies **any repo change** (code, infra, docs, configs), the agent must run the Router procedure:

1. Read `docs/ROUTER.md`.
2. Read `.agent/router/router_map.yml`.
3. Produce a **Dispatch Plan** (domain, risk tier, required gates, selected workflows, deliverables).
4. Execute the selected workflows (or emulate them if your platform cannot “run workflows”).

### B) Always run gates before finalizing

At minimum:

- `.agent/workflows/03_security_privacy_gate.md`
- at least one critic pass in `.agent/workflows/critics/*`

Higher risk changes must also include: threat modeling, observability checks, test strategy updates, and release readiness.

### C) If your platform cannot load `.agent/rules/*`

Do not ignore them. Instead:

1. Open the relevant rules in `.agent/rules/` (security, privacy, clinical scope, etc.).
2. Summarize them into a short “Constraints” section.
3. Use that Constraints section as the invariant policy for the work.

## Starvit’s main domains

- **Frontend:** Next.js + design system + accessibility baseline
- **Backend:** FastAPI services (Cloud Run optional) + Medplum FHIR integration
- **Data:** de-ID pipeline, analytics tables, governance, quality
- **Graph:** TigerGraph in de-identified zone + allowlisted query surface
- **ML/AI:** Vertex AI training/serving, model registry, evaluation, novelty seeking, clinical guardrails
- **Ops/SRE:** observability, CI/CD, SLOs, reliability and change management
- **Clinical research & regulatory:** evidence ingestion, safety/red flags, SaMD/CDS posture

## Platform interoperability

## Codex (VS Code) — Agent Skills integration

This repo also ships a **Codex-native skills pack** under:

- `.codex/skills/`

Codex loads each subdirectory containing a `SKILL.md` as a Skill. Each Starvit **rule** and **workflow** from the Antigravity pack has been re-published as a Codex Skill, plus two helpers:

- `$starvit-router` — routes tasks to the correct workflow + role/rule skills.
- `$starvit-skillpack-index` — catalog of available Starvit skills.

### How to use (practical)

1. Open the Starvit repo in VS Code with the Codex extension enabled.
2. Ensure `.codex/skills/` is present at the repository root (or in the service subfolder you work in).
3. Restart the Codex extension/session so it indexes skills.
4. Start with:
   - `$starvit-router`
   - `$starvit-rule-00-nonnegotiables`
   - one workflow skill (e.g., `$starvit-wf-00-triage-and-plan`)
   - then the relevant role/rule skills.

Codex supports explicit skill invocation with `$skill-name`, and may also choose skills implicitly when your request matches a skill’s description.



Different agent tools load “project instructions” differently. To keep Starvit behavior consistent across tools:

1. Treat **this** document as the canonical overview.
2. Use `docs/AGENT_PLATFORMS.md` for tool-specific setup patterns.
3. When available, prefer a **root-level** instruction file (AGENTS.md / CLAUDE.md / GEMINI.md / Copilot instruction files) that tells the agent to load this doc and then follow the router.
