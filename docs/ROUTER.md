# Starvit Router (portable routing contract)

The **Router** is the entrypoint that converts a request (“add X”) into an auditable execution plan that selects the correct specialists, workflows, and safety gates.

In Antigravity IDE, the Router is an executable workflow (`.agent/workflows/router.md`, slash command `/router`). In other agentic platforms, you must **emulate** the Router using the same inputs and outputs.

## Router inputs

Always read, in this order:

1. `docs/AGENTS.md` (portable non-negotiables)
2. `.agent/router/router_map.yml` (domain routing + risk tiers)
3. The relevant existing docs for the area being changed (e.g., `docs/frontend/*`, `docs/backend/*`, `docs/data/*`, `docs/graph/*`, `docs/ml/*`, `docs/clinical/*`)

## Router outputs

The Router must emit a **Dispatch Plan** that contains:

1. **Classification**
   - primary domain(s)
   - affected components (paths)
2. **Risk tier** (tier0–tier3)
3. **Lead role** + required supporting roles
4. **Mandatory gates** (at minimum: security/privacy gate + at least one critic)
5. **Selected workflows** (explicit `.agent/workflows/...` paths)
6. **Deliverables** (what will change; how correctness will be proven)
7. **Stop conditions** (when to ask the human for a decision)

## Universal router procedure

If your platform does not support “workflows” as first-class objects, treat each referenced workflow file as a **step-by-step runbook**.

1. **Summarize the request** in 1–3 sentences.
2. **Classify** the request using `.agent/router/router_map.yml`.
3. **Assign risk tier**:
   - tier0: docs-only, no behavioral change
   - tier1: localized code change, low blast radius
   - tier2: cross-cutting or security/infra/data-plane change
   - tier3: clinical-facing logic, PHI boundary risk, ML model behavior, or anything regulator-relevant
4. **Select workflows**:
   - pick the primary specialist workflow(s)
   - add mandatory gates
   - add tests + observability workflows when applicable
5. **Execute** workflows in order:
   - design → implement → verify → critic → release readiness
6. **Finish** only when:
   - tests pass (or an explicit exception is documented)
   - security/privacy checks are satisfied
   - the critic pass has been addressed

## When not to route

If the user request is a pure question (no implied repo changes), do not run the Router. Answer normally, but still respect safety constraints.

## Maintenance

Routing logic is maintained in:

- `.agent/router/router_map.yml`

When new workflows or roles are added, update the router map accordingly.
