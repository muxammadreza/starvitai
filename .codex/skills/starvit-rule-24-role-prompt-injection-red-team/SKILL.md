---
name: starvit-rule-24-role-prompt-injection-red-team
description: Owns adversarial testing of any LLM/agent capability.
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

---

**Codex usage notes:**
- Apply this skill whenever the current task matches the scope.
- If a decision or output could affect PHI, clinical safety, or security posture, cross-check `$starvit-rule-00-nonnegotiables` and `$starvit-wf-03-security-privacy-gate`.
