# Development Operating Model (Starvit)

This is the practical “how we build” guide for Starvit when using **agentic coding tools** (Antigravity, Codex, Copilot coding agent, Cursor Agent, Windsurf Cascade, Claude Code, Aider, ...).

The pack’s core promise is: **a consistent, auditable change process**, regardless of which tool executes it.

## 1) Default execution posture

- Use the **Router** for any work that implies repository changes.
- Prefer **small, testable diffs** over “big bang” changes.
- Default to **explicit human approval** for risky commands, infrastructure changes, security-sensitive edits, and anything touching PHI boundaries.

## 2) The standard change loop (tier1–tier3)

This is the canonical sequence. In Antigravity, these are workflows; in other platforms, treat them as runbooks.

1. **Triage & plan** → `.agent/workflows/00_triage_and_plan.md`
2. **Design if cross-cutting** → `.agent/workflows/01_change_design_rfc_adr.md`
3. **Implement with tests** → `.agent/workflows/02_implement_with_tests.md`
4. **Security & privacy gate** → `.agent/workflows/03_security_privacy_gate.md`
5. **Release readiness** → `.agent/workflows/04_release_readiness.md`
6. **Post-merge follow-ups** → `.agent/workflows/05_post_merge_followups.md`

For tier0 (docs-only), you can skip directly to critic + release readiness.

## 3) When to involve which specialists

Use this as routing intuition (the Router will make it explicit):

- **UI change:** UI/UX + Frontend + Accessibility QA (+ Backend if API/contract changes)
- **New clinical metric/protocol behavior:** Protocol Engine + Clinical Safety + Backend + QA
- **New de-ID feature table / analytics:** Data Engineering + Data Governance + Security/Privacy
- **Any ML:** ML Engineering + MLOps + Model Risk + Clinical Safety
- **Any graph:** Graph Engineer + Query Allowlist Owner + Data Governance + Security/Privacy
- **Any infra/deploy:** SRE + Release/Change + Security + FinOps

## 4) What the human operator must provide

Agents can draft and implement, but you (human) must:

- confirm scope and priorities when tradeoffs are required (safety vs speed vs cost)
- approve risky commands and production-like operations
- provide secrets via your own secure mechanism (agents should never invent or hardcode them)
- accept the final diff and ensure it aligns with clinical intent and compliance constraints

## 5) Science-to-product discipline

For anything that could be interpreted as “clinical guidance”:

- require **provenance** (where evidence came from; what level; limitations)
- express outputs as **clinician-supervised flags**, not directives
- include escalation paths and patient-safety red flags (see `docs/clinical/SAFETY_RED_FLAGS.md`)

## 6) Practical “how do I use this day-to-day?”

When you want to add a feature or change behavior:

1. Write a one-paragraph request (what, why, constraints, what good looks like).
2. Trigger the Router (or ask the agent: “Run the Router and produce a Dispatch Plan”).
3. Read the Dispatch Plan and adjust anything you disagree with.
4. Let the agent execute workflows sequentially (or in parallel if your platform supports multi-agent dispatch).
5. Require a critic pass before you merge.

If the agent does not follow the Router, stop and re-run it explicitly.
