---
name: starvit-skillpack-index
description: Index of all Starvit Codex skills (rules + workflows) and recommended invocation patterns.
---

# Starvit Codex Skills Pack Index

This repository provides a Codex-native packaging of the Starvit agent pack as **Agent Skills**.

## Recommended starting point
- `$starvit-router` (routing)
- `$starvit-rule-00-nonnegotiables` (always-on constraints)
- Then one workflow skill + the relevant role/rule skills.

## Workflows

- `$starvit-wf-00-triage-and-plan` — Use this before any non-trivial implementation, especially when the change touches PHI, auth, data pipelines, or ML/graph layers.
- `$starvit-wf-01-change-design-rfc-adr` — Before starting:
- `$starvit-wf-02-implement-with-tests` — Ship changes that are correct, reviewable, and safe.
- `$starvit-wf-03-security-privacy-gate` — Run for any change that touches: PHI boundary, auth/RBAC, external integrations, data export, ML/agent actions, or pipeline cross-zone movement.
- `$starvit-wf-04-release-readiness` — Before deploying any backend, UI, pipeline, or ML model change to production.
- `$starvit-wf-05-post-merge-followups` — Prevent drift after code merges.
- `$starvit-wf-98-reza-feature-intake-playbook` — Write: “I want Starvit to …”
- `$starvit-wf-99-reza-orchestration` — Include: - outcome (what done looks like) - where it lives (UI / API / data / graph / ML) - users impacted (patients, clinicians, researchers) - constraints (security/compliance, performance targets, deadlines)
- `$starvit-wf-route` — **Default move:** run the Router. - `$starvit-wf-router`
- `$starvit-wf-router` — 1. If the user request is *pure Q&A* (no implied repo changes), answer normally and stop. 2. Otherwise continue: this is an implementation request and must be routed.

## Rules / Roles

- `$starvit-rule-00-nonnegotiables` — These constraints override any generic software engineering preference.
- `$starvit-rule-01-security-terminal-browser` — This repo uses a high-automation workflow style. That creates **real** risk: - prompt injection (malicious instructions in issues/docs/webpages), - accidental destructive commands, - secrets leakage, - PHI boundary violations.
- `$starvit-rule-02-engineering-standards` — - Architecture decisions MUST be written as ADRs for any cross-cutting change.
- `$starvit-rule-03-rules-workflows-integrity` — These rules protect the team from “agent drift”, prompt injection, and supply-chain style tampering of the `.codex/` pack.
- `$starvit-rule-04-project-scope-scientific-context` — Starvit is a **clinician‑supervised metabolic‑therapy support platform** (oncology first; diabetes/metabolic disease later) with strict PHI controls and a **de‑identified research/ML layer**.
- `$starvit-rule-04-turbo-mode-safety` — Turbo mode can auto-run terminal steps. In Starvit, turbo is **restricted**.
- `$starvit-rule-06-router-protocol` — Starvit uses Antigravity **Rules** (persistent guardrails) and **Workflows** (saved, repeatable playbooks).
- `$starvit-rule-10-role-backend-platform` — Backend Platform Engineer Rules
- `$starvit-rule-11-role-frontend-clinician-web` — You are responsible for `apps/clinician` and clinician-facing UX.
- `$starvit-rule-12-role-mobile-patient-app` — Owns the patient mobile surface, emphasizing offline robustness and privacy.
- `$starvit-rule-13-role-uiux-design-system` — You own `packages/ui` and the cross-app design language.
- `$starvit-rule-14-role-devex-build` — Owns developer productivity, CI/CD hygiene, and monorepo ergonomics.
- `$starvit-rule-15-role-qa-automation` — Owns the verification strategy across services, UIs, and ML inference boundaries.
- `$starvit-rule-16-role-accessibility-qa` — Owns accessibility verification for web surfaces (clinician dashboard + research workbench) and patient app.
- `$starvit-rule-17-frontend-stack-web` — This rule is the **source of truth** for web-frontend tech choices for Starvit.
- `$starvit-rule-18-design-system-web` — Starvit Design System Rules (Web)
- `$starvit-rule-19-api-contracts-openapi` — Starvit API Contract + Typed Client Rules
- `$starvit-rule-20-role-frontend-research-workbench-web` — You are responsible for `apps/research`, which operates **only on de-identified data**.
- `$starvit-rule-20-role-security` — Owns application security, platform security (cloud/VPS), and LLM/agent security.
- `$starvit-rule-21-frontend-stack-mobile` — This is the baseline for `apps/patient-mobile`.
- `$starvit-rule-21-role-privacy-compliance` — Owns privacy, data minimization, consent semantics, and regulatory alignment.
- `$starvit-rule-22-role-iam-audit` — Owns identity, authorization, auditability, and least-privilege verification across Medplum, cloud infrastructure, and the application layer.
- `$starvit-rule-23-role-supply-chain-security` — Owns dependency integrity, artifact provenance, and safe ingestion of third-party code/models/datasets.
- `$starvit-rule-24-role-prompt-injection-red-team` — Owns adversarial testing of any LLM/agent capability.
- `$starvit-rule-25-backend-stack-fastapi` — Starvit Backend Stack Rules (FastAPI/Python)
- `$starvit-rule-26-backend-cloud-run-deployment` — Cloud Run Deployment Rules (Starvit Backend)
- `$starvit-rule-27-backend-gcp-identity-secrets` — Identity and secrets rules (Medplum + cloud)
- `$starvit-rule-28-backend-async-pubsub-workflows` — Async Processing Rules (Pub/Sub + Cloud Workflows)
- `$starvit-rule-29-backend-security-authz` — Backend Security and Authorization Rules
- `$starvit-rule-30-role-sre` — Owns reliability, operational readiness, and incident learning.
- `$starvit-rule-31-role-observability` — Owns tracing, metrics, logging, dashboards, and alert signals.
- `$starvit-rule-32-role-release-change-manager` — Owns safe delivery, change tracking, and rollback readiness.
- `$starvit-rule-33-role-finops-cost-engineering` — Goal: deliver the required clinical/research capability at the lowest sustainable cost, without compromising security, reliability, or auditability.
- `$starvit-rule-34-role-incident-commander` — Goal: coordinate fast, safe restoration of service with clear communication, then drive learning via postmortems.
- `$starvit-rule-35-medplum-mcp-mandate` — Starvit uses **Medplum as the PHI system of record**. All configuration and administrative changes to the Medplum instance must be performed via the **Medplum MCP server** that the user has already configured in Antigravity.
- `$starvit-rule-36-medplum-v5-non-deprecated` — Starvit must be compatible with **Medplum 5.0.10+**. Do not copy old snippets or SDK patterns.
- `$starvit-rule-40-role-data-engineering` — Owns ingestion, transformation, data quality, lineage, and de-identification pipelines.
- `$starvit-rule-41-role-graph-engineering` — Role: Graph Engineer (TigerGraph)
- `$starvit-rule-42-role-data-quality` — Role: Data Quality Engineer
- `$starvit-rule-43-role-data-governance-steward` — Role: Data Governance Steward
- `$starvit-rule-44-role-tigergraph-platform-engineering` — Role: TigerGraph Platform Engineer
- `$starvit-rule-45-role-data-platform-architect` — Role: Data Platform Architect
- `$starvit-rule-46-role-bigquery-analytics-engineer` — Role: BigQuery Analytics Engineer
- `$starvit-rule-47-role-dataflow-streaming-engineer` — Role: Dataflow / Streaming Pipeline Engineer
- `$starvit-rule-48-role-cloudsql-database-engineer` — Role: Cloud SQL Database Engineer (Operational, non-PHI)
- `$starvit-rule-49-role-analytics-engineer-dbt-dataform` — Role: Analytics Engineer (dbt / Dataform)
- `$starvit-rule-50-role-ml-engineering` — Role: ML Engineer (Starvit)
- `$starvit-rule-51-role-mlops` — Role: MLOps Engineer (Starvit)
- `$starvit-rule-52-role-model-risk-eval` — Role: Model Risk & Evaluation Lead
- `$starvit-rule-53-role-graph-ml-researcher` — Role: Graph-ML Researcher (Link Discovery)
- `$starvit-rule-54-role-novelty-discovery` — Role: Novelty Discovery Lead
- `$starvit-rule-55-role-feature-store-engineering` — Role: Feature Store Engineer
- `$starvit-rule-56-role-metadata-catalog-policy-tags` — Role: Metadata Catalog & Policy Tags Engineer
- `$starvit-rule-57-role-data-reliability-engineer` — Role: Data Reliability Engineer (Data SRE)
- `$starvit-rule-60-role-clinical-informatics-safety` — You are working on a clinician-supervised system that can *suggest* protocol actions and analytics, but cannot make autonomous medical decisions.
- `$starvit-rule-61-role-protocol-engine-maintainer` — Goal: evolve the clinical protocol engine safely and audibly.
- `$starvit-rule-62-role-metabolic-oncology-clinical-lead` — You act as the clinical-science integrator for Starvit’s metabolic therapy layer. Your output must be usable by other engineers to implement *clinician-supervised* protocol logic.
- `$starvit-rule-63-role-oncology-dietitian-kmt` — You focus on implementability and adherence constraints for ketogenic metabolic therapy (KMT) *as a clinician-supervised intervention*. Your outputs feed the clinician dashboard, patient logging UX, and safety gates.
- `$starvit-rule-64-role-clinical-pharmacist-repursposed-drugs` — You evaluate drug–diet and drug–biomarker interactions, especially where standard-of-care oncology care intersects with metabolic interventions.
- `$starvit-rule-65-role-biostatistician-clinical-trialist` — You design evaluation plans that separate signal from bias. You also ensure that Starvit’s research layer can support auditable, publication-grade analyses.
- `$starvit-rule-66-role-regulatory-samd-cds` — You maintain a conservative posture: treat Starvit’s recommendation features as potentially regulated clinical decision support until proven otherwise.
- `$starvit-rule-67-role-ethics-irb-research-governance` — You enforce ethical and governance constraints for research on de-identified data.
- `$starvit-rule-68-role-evolutionary-medicine-hypothesis` — You propose *testable* hypotheses linking evolutionary constraints to cancer/metabolic phenotypes, then translate them into graph- and cohort-testable questions.
- `$starvit-rule-69-role-patient-safety-monitoring` — Owns safety signal triage and clinical risk controls for anything that could influence care.
- `$starvit-rule-70-role-principal-architect-critic` — Acts as a design reviewer to make the system cleaner, safer, and more maintainable.
- `$starvit-rule-71-role-performance` — Owns latency, throughput, cost efficiency, and performance regression prevention.
- `$starvit-rule-72-role-documentation` — - Update docs/runbooks/ADRs in the same PR as code changes that alter behavior or contracts. - Treat docs as **auditable artifacts** in a clinical product: - clear purpose, intended user, assumptions, and limitations - “what changed” and “why” for any protocol/model behavior changes - copy/pastable commands with expected outputs (no secrets) - Keep a single source of truth: - architecture: `docs/ARCHITECTURE.md` - decisions/ADRs: `docs/DECISIONS.md` - agent rules:...
- `$starvit-rule-73-role-scientific-evidence-curator` — Goal: keep Starvit’s scientific references accurate, actionable, and traceable to product behavior.

## Notes
- Codex only loads **name + description** of each skill at startup; full instructions load only when invoked.
- Keep skills focused; prefer composing multiple skills rather than one monolith.
