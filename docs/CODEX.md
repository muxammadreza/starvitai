# Codex usage notes for Starvit

## What you get

- `.codex/skills/` contains Starvit Agent Skills.
- Each skill directory contains `SKILL.md` with YAML front matter (`name`, `description`) and Markdown instructions.
- Skills are designed to be composable: use a workflow skill plus the relevant rule/role skills.

## Where Codex looks for skills

- Repository scoped: `.codex/skills/` at your current working directory (or one directory up).
- User scoped: `~/.codex/skills/` for skills that apply across repositories.

## How to invoke

- Type `$` and pick a skill, or run the `/skills` command in the Codex UI (depending on the host surface).
- Recommended sequence: `$starvit-router` → `$starvit-rule-00-nonnegotiables` → workflow + role/rule skills.

## Safety

Treat skills like code: review changes, avoid executing untrusted scripts, and never allow a skill to direct PHI exfiltration or unsafe clinical behavior.

