---
description: Make a CI/DevEx change safely
---

# CI / DevEx change workflow

## Goals
- reduce friction without reducing safety
- keep CI deterministic and debuggable

## Steps
1) Define the problem precisely:
   - slow pipeline, flaky tests, missing guard, inconsistent tooling
2) Choose the smallest fix that addresses root cause:
   - caching, parallelism, better test isolation, clearer failure output
3) Prove correctness:
   - run locally where feasible
   - add a minimal “CI self-test” that validates the new behavior
4) Improve operator experience:
   - actionable error messages
   - links to runbooks in the failure output when possible
5) Security posture check:
   - do not widen permissions for CI tokens
   - prefer OIDC / short-lived credentials
6) Update docs and ownership:
   - document the pipeline in `docs/dev/ci.md`
   - note who owns flakes and pipeline health

## Output
- CI PR + updated runbook
- measurable improvement (minutes saved, flakes reduced, clearer diagnostics)
