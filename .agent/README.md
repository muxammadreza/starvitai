# Starvit Antigravity Agent Pack

This folder defines **workspace-scoped** Antigravity **Rules** and **Workflows**.

- Rules live in `.agent/rules/` and are treated as persistent constraints the agent should follow.
- Workflows live in `.agent/workflows/` and are invoked with `/` in Antigravity.

## Safety defaults (recommended)
- Use **Planning** mode for non-trivial tasks.
- Set Terminal auto-execution policy to **Off** by default; escalate only when you are confident the workflow is safe.
- Use a strict browser allowlist for documentation domains.
- Treat `.agent/` changes as security-sensitive and protect them via CODEOWNERS + CI.

## Starvit critical boundaries
- PHI is stored only in Medplum (FHIR R4).
- The Research/ML zone is **de-identified** (BigQuery + TigerGraph + Vertex AI).
- UIs never talk directly to TigerGraph; all graph access is via allowlisted Research API endpoints.
- Every recommendation is auditable: inputs -> transforms -> outputs -> versioned artifacts -> clinician decision.

## Workflow conventions
Every workflow file follows:
- What to do
- When to use it
- Inputs/Outputs
- Step-by-step checklist
- Quality gate commands (marked `// turbo`)

## Routing (start here)
- Default entrypoint: `workflows/router.md` (or `/router` in Antigravity).
- If you are Reza orchestrating work: `workflows/98_reza_feature_intake_playbook.md` and `workflows/99_reza_orchestration.md`.
- Graph/TigerGraph work: `workflows/graph/**`.
- ML/AI work: `workflows/ml/**` plus the ML governance rules.

## Integrity
`.agent/` is a behavior boundary. This pack ships with a checksum manifest:

- Generate/update: `.agent/tools/gen_manifest.sh`
- Verify: `.agent/tools/verify_manifest.sh`

Lock `.agent/**` behind CODEOWNERS and reviewed PRs.
