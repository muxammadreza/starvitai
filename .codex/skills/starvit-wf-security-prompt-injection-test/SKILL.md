---
name: starvit-wf-security-prompt-injection-test
description: Run prompt-injection and agent misuse tests
---

# Run prompt-injection and agent misuse tests

When invoked, follow this workflow as written. Use the Router and relevant role/rule skills as needed, and run the Security/Privacy Gate for tier2+ changes.

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

