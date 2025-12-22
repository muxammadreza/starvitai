---
description: Universal router for Starvit: classify a request, select workflows, dispatch agents, and enforce gates
---

Use this workflow when you want the agent to automatically decide **which specialists** and **which Starvit workflows** should run, then execute (or propose a multi-agent dispatch plan) safely.

This workflow is designed to be triggered explicitly via `/router` or automatically via the Starvit Router Protocol rule.

## 1) Determine whether routing applies

1. If the user request is *pure Q&A* (no implied repo changes), answer normally and stop.
2. Otherwise continue: this is an implementation request and must be routed.

## 2) Load the routing map

Open and use:
- `.agent/router/router_map.yml`

Treat it as the authoritative index for:
- domain → lead role + supporting roles
- domain → workflows
- mandatory gates + always-on gates
- risk tier definitions

## 3) Extract intent and constraints (no back-and-forth unless necessary)

From the user prompt, extract:
- objective (1 sentence)
- surface(s): mobile, clinician dashboard, research workbench, backend, data, graph, ML, ops, security
- change type: feature, bugfix, refactor, research experiment, migration
- constraints: security/compliance, performance, deadlines, rollout/backfill constraints

If critical information is missing (e.g., “which UI surface?”), proceed with the safest default and ask only *one* follow-up question.

## 4) Choose domains and risk tier

1. Pick all applicable `domains.*` entries from `router_map.yml`.
2. Compute risk tier:
   - Start at tier1.
   - Escalate to tier2 if auth/RBAC, audit, pipelines, TigerGraph queries, deployments, or model inference are involved.
   - Escalate to tier3 if PHI boundary/FHIR access, cross-zone data movement, clinician-affecting model behavior, or security-critical paths are involved.
   - Use the *highest* tier when multiple apply.

## 5) Decide orchestration mode

Single-agent execution is acceptable when:
- one primary domain is involved, and
- the work is small/reversible.

Multi-agent dispatch is recommended when:
- 2+ domains are involved, or
- risk tier is tier2/tier3, or
- the task benefits from parallelism (implementation vs tests vs docs vs critic).

If multi-agent is recommended, create a dispatch plan that includes:
- agent names
- which role rule each agent must follow
- explicit task scopes and deliverables

## 6) Emit the Dispatch Plan (required output contract)

Your response must begin with a **Dispatch Plan** section containing:

- Primary objective (1 sentence)
- Domains selected (bullets)
- Risk tier + rationale (1–2 sentences)
- Lead role + supporting roles (bullets)
- Selected workflows (ordered list of paths)
- Mandatory gates and critics (ordered list)
- Verification plan (tests, QA, observability)
- Deliverables (PR diff, evidence, docs/runbooks)

Then include a **Task Group** breakdown:

- TG0 Design (ADR/RFC, contracts)
- TG1 Implementation (domain workflows)
- TG2 Verification (tests, data quality, instrumentation)
- TG3 Independent critique (threat model / perf / clinical safety as applicable)
- TG4 Release readiness

## 7) Execute or dispatch

### Option A — Single-agent sequence

1. For each workflow in the ordered list, open the workflow file and follow its steps.
2. Always execute mandatory gates and at least one critic workflow before finalizing.

### Option B — Multi-agent dispatch

Provide copy/paste prompts for each agent.

Each prompt MUST include:
- the objective
- the exact workflow(s) to run
- the gate(s) to include
- the evidence expected (tests/logs/screenshots/metrics)

The router agent remains responsible for:
- resolving merge conflicts across parallel work
- ensuring gates/critics were actually executed
- assembling the final PR-ready package (diff + evidence + docs)

## 8) Stop conditions

If a required gate fails (security/privacy, test suite, data quality, model risk), stop and return:
- what failed
- why it matters
- the minimal set of remediation steps

Do not “ship anyway.”

### Domain hint: Clinical Research
Route to **clinical_research** when the user request involves:
- metabolic therapy evidence synthesis, contraindications, safety monitoring
- protocol engine changes linked to clinical reasoning
- trial protocol drafting, endpoints, reporting standards (SPIRIT, PRISMA, CONSORT-AI/SPIRIT-AI)
- regulatory framing for clinical decision support
