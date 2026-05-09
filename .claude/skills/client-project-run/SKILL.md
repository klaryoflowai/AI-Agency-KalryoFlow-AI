---
name: client-project-run
description: Run a client project through the MVP operator workflow from brief to QA using the local project template and agent contracts.
---

# Client Project Run

Use when the user asks to run a new or existing client project.

## Workflow
1. Read `projects/<project_id>/PROJECT.md`.
2. Run Eval Agent first using `agents/eval-agent/SKILL.md`.
3. Save outputs to `projects/<project_id>/outputs/eval-agent/`.
4. Ask CEO approval if the SOW, price, scope, or runtime API cost is not approved yet.
5. Route execution:
   - Backend tasks → `backend-agent`.
   - Frontend/UI tasks → `frontend-agent`.
   - Process/SOP tasks → `ops-agent`.
   - Commercial docs → `bd-agent`.
6. Run QA Agent last.
7. Do not mark delivery complete unless QA score is at least 7/10 and SOW coverage is 100%.

## Rules
- MVP uses Codex/Claude Code as operators.
- Do not add LLM API SDKs or keys.
- Runtime API client-side requires explicit CEO approval and cost estimate.

