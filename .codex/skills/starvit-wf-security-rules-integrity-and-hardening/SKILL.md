---
name: starvit-wf-security-rules-integrity-and-hardening
description: Hardening checklist for rule/workflow packs and automation
---

# Hardening checklist for rule/workflow packs and automation

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

## Objective
Prevent tampering, reduce risky automation, and make agent behavior reviewable.

## Checklist
1) Review permissions:
   - agent tooling must use allowlists
   - prevent write access to PHI resources unless explicitly required
2) Repository hardening:
   - CODEOWNERS for `.codex/`
   - required reviews for security-sensitive paths
3) Integrity:
   - maintain `.codex/manifest.sha256`
   - CI verifies manifest
4) Supply chain:
   - SBOM generation for deployables
   - provenance/attestations where feasible
5) Secrets hygiene:
   - secret scanning
   - no secrets in PRs, logs, or docs

## Output
A short security note describing what was hardened.

