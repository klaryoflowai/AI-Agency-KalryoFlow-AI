---
name: project-audit
description: Audit the AI Agency workspace for architecture drift, missing resources, agent-boundary violations, and MVP zero-API compliance.
---

# Project Audit

Use when the user asks to audit the project, check consistency, or prepare for implementation.

## Workflow
1. Read `AGENTS.md`, `CLAUDE.md`, `README.md`, `docs/blueprint.md`, and `docs/stack-tehnic.md`.
2. Scan for forbidden drift:
   - generic technical agent references;
   - `Claude API`, `Anthropic SDK`, `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`;
   - runtime LLM API without explicit client approval wording.
3. Verify all referenced resources exist.
4. Verify each `agents/*/SKILL.md` has:
   - `schema_version`;
   - Contract Operațional MVP;
   - write boundary;
   - QA gate.
5. Return findings first, then recommended fixes.

Do not modify files unless the user explicitly asks for implementation.

