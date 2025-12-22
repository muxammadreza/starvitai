---
description: Run prompt-injection and agent misuse tests
---

## Goal
Demonstrate resilience to prompt injection and excessive agency.

## Steps
1) Assemble test corpus:
   - direct prompt injection attempts
   - indirect injection via retrieved docs
2) Run tests against staging:
   - ensure system instructions remain enforced
   - ensure tool calls require explicit authorization
3) Validate sensitive data boundaries:
   - ensure no PHI is returned or logged
4) Record outcomes:
   - failures become issues with mitigation plan

## Output
A red-team report + CI test results.
