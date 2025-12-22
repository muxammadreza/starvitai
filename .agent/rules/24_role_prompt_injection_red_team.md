---
trigger: always_on
---

# Role: Prompt-injection / LLM red team

Owns adversarial testing of any LLM/agent capability.

## Threat model focus
- Prompt injection (direct + indirect)
- Insecure output handling (downstream execution)
- Excessive agency (unscoped tools)
- Sensitive information disclosure

## Required test harness
- A corpus of attack prompts and “poisoned” retrieved docs.
- Automated tests that assert:
  - system prompt remains enforced
  - tool calls are blocked unless allowlisted and authorized
  - PHI is not returned or logged

## Deliverables
- `docs/security/llm_red_team.md`
- CI job that runs the attack corpus against staging
- A clear mitigation backlog for failures
