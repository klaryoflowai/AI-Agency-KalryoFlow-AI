---
name: agent-skill-lint
description: Lint agent SKILL.md files for schema, boundaries, forbidden SDKs, and handoff clarity.
---

# Agent Skill Lint

Use before changing any `agents/*/SKILL.md`.

## Checks
- Agent role is narrow and does not invade another agent.
- Technical delivery is split across backend, frontend, and QA.
- Output format includes `"schema_version": "<agent>.v1"`.
- Contract section exists:
  - Input
  - Output
  - Write boundary
  - Forbidden
  - QA gate
- No SDK LLM runtime in MVP.
- QA Agent is final delivery gate.

## Output
Return:
- PASS/FAIL.
- Blocking findings.
- Suggested patch summary.

