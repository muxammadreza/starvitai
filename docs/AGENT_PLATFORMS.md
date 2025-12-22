# Starvit agent-pack compatibility (Codex, Copilot, Claude Code, Cursor, Windsurf, Aider, Gemini CLI)

The Starvit agent-pack is authored for Antigravity IDE (rules + workflows in `.agent/`). Many other agentic platforms can still follow the pack **without modifying `.agent/` content** by loading a small set of **high-level instruction files** and then executing the Router procedure.

This document explains how to achieve that across common platforms.

## 1) Universal pattern

Regardless of tool:

1. Ensure the platform loads a root-level instruction file (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or Copilot instruction files).
2. That file must instruct the agent to:
   - read `docs/AGENTS.md`
   - run the Router (`docs/ROUTER.md` + `.agent/router/router_map.yml`)
   - emulate selected `.agent/workflows/*` as step-by-step runbooks

If your platform supports directory-scoped instruction files, you may optionally add smaller overrides in subdirectories, but keep the Router logic centralized in `docs/ROUTER.md`.

## 2) OpenAI Codex (CLI / IDE)

Codex natively reads `AGENTS.md` files before doing work and supports layered instructions (`AGENTS.override.md`, root → subdirectories). Use a **root-level `AGENTS.md`** that points Codex to `docs/AGENTS.md` and the Router procedure.

Codex also supports a *global* instructions file under your Codex home directory (e.g., `~/.codex/AGENTS.md`). Treat that as personal defaults; Starvit’s repo-level rules should live in this repo.

Operational verification (recommended): run a Codex command that asks it to list the instruction sources it loaded, ensuring `AGENTS.md` is included.

## 3) GitHub Copilot (coding agent + chat)

Copilot supports repository-wide instructions via `.github/copilot-instructions.md` and path-specific instructions via `.github/instructions/*.instructions.md`. Copilot also supports `AGENTS.md` instruction files, with the nearest file intended to take precedence.

Practical setup:

- Prefer a root-level `AGENTS.md` that routes to `docs/AGENTS.md` + Router.
- Optionally add `.github/copilot-instructions.md` as a thin shim that points to the same.
- Avoid conflicting guidance across multiple instruction sources; Copilot’s behavior in conflicts can be non-deterministic.

If your team already uses Copilot instruction files, keep them as thin redirects back to `docs/AGENTS.md` and the Router contract, rather than duplicating content.

## 4) Cursor

Cursor’s supported configuration is **project rules** stored in `.cursor/rules` (preferred), with `.cursorrules` as a deprecated legacy mechanism.

Cursor rules support multiple activation modes (always-on, auto-attached to globs, agent-requested, manual). Treat Starvit’s routing/safety guidance as “always-on”, and optionally create additional auto-attached rules for high-risk areas (e.g., anything under `services/` or `docs/clinical/`).

Recommended approach (without copying the entire `.agent/` pack into Cursor rules):

- Create one Always-on Cursor rule that says:
  - Read `docs/AGENTS.md`.
  - Follow `docs/ROUTER.md` and `.agent/router/router_map.yml`.
  - Treat `.agent/workflows/*` as runbooks.

If you later decide to fully port Antigravity rules into Cursor `.mdc` format, do it as a separate, explicit conversion project.

## 5) Windsurf

Windsurf’s Cascade supports `AGENTS.md` discovery (root and subdirectories) and also has its own rules system under `.windsurf/rules`.

Recommended approach:

- Use root-level `AGENTS.md` as the primary instruction entry.
- Keep the Router in `docs/ROUTER.md`.

## 6) Claude Code

Claude Code supports instruction “memory” via `CLAUDE.md` files (with a discoverable hierarchy) and settings via `.claude/settings.json`.

Recommended approach:

- Create a root-level `CLAUDE.md` that points to `docs/AGENTS.md` and the Router.
- Add `.claude/settings.json` deny rules in your main repo (outside this pack) to prevent the tool from reading secrets/PHI artifacts.

Tip: keep `CLAUDE.md` short, and put detailed guidance into `docs/AGENTS.md` so it can be shared across platforms.

## 7) Aider

Aider can be configured to read a project instructions file (commonly `AGENTS.md`) via `.aider.conf.yml`.

Example:

```yaml
read: AGENTS.md
```

## 8) Gemini CLI

Gemini CLI can be configured to use `AGENTS.md` as the context/instructions file (via `.gemini/settings.json`).

Example:

```json
{ "contextFileName": "AGENTS.md" }
```

---

## Appendix: What we do NOT do here

This agent-pack does **not** auto-generate tool-specific rule files (e.g., `.cursor/rules/*.mdc`, `.windsurf/rules/*.md`, `.github/instructions/*.instructions.md`) because those formats vary and should be adopted explicitly in the target environment.

Instead, we ship:

- `AGENTS.md` (repo root) — the primary entrypoint for Codex/Windsurf/Copilot and other agents.
- `CLAUDE.md` (repo root) — a compatibility shim for Claude Code and tools that recognize it.
- `GEMINI.md` (repo root) — a compatibility shim for Gemini-oriented tooling and some Copilot deployments.

Each shim is intentionally short and tells the agent to open `docs/AGENTS.md` and then run the Router procedure.

If you choose to add additional platform-specific instruction files in your main repository, keep them thin and redirect to the same Router contract:

- `.github/copilot-instructions.md` → “Read `docs/AGENTS.md`, then run the Router.”
- `.cursor/rules/00_starvit_always.mdc` → same guidance, Cursor rule format.
- `.windsurf/rules/starvit_always.md` → same guidance, Windsurf rule format.

This avoids divergence between tool-specific copies of the instruction set.

- portable instruction docs (`docs/AGENTS.md`, `docs/ROUTER.md`, `docs/DEVELOPMENT_OPERATING_MODEL.md`)
- a small set of root-level shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) that point agents back to the canonical docs

## Validation checklist (use this when adopting a new agent platform)

1. Ask the agent: “List the instruction files you loaded from this repo.”
2. Ask the agent: “Summarize the Starvit non-negotiables.” (PHI boundary, clinician approval, one backend, auditability, TigerGraph isolation)
3. Give a small, low-risk task (tier0/1), run the Router, and verify it:
   - outputs a Dispatch Plan
   - selects at least one critic pass
   - references concrete `.agent/workflows/*` paths
4. Give a medium change (tier2) and verify it runs the security/privacy gate.

## Common failure modes

- The platform does not automatically discover `docs/AGENTS.md` because it only reads root-level instruction files.
  - Fix: ensure `AGENTS.md` exists at the repository root (shim file).
- The agent “skips” `.agent/rules/*`.
  - Fix: require the agent to open and summarize the relevant rule files and treat them as constraints.
- Conflicting instruction sources (e.g., Copilot has both `.github/copilot-instructions.md` and path-specific `.instructions.md`).
  - Fix: keep all platform-specific files as thin redirects; do not duplicate detailed instructions.
