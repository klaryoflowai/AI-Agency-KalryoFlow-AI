# Codex + Claude Code Operating Model

## Roluri

### Codex
Operator principal pentru backend și integrare:
- modificări în repo;
- backend Python/TypeScript;
- API-uri, DB, Supabase, n8n, webhooks;
- debugging server-side;
- teste backend;
- integrare finală și verificare Git.

### Claude Code
Operator principal pentru frontend și reviewer:
- frontend React/Next.js;
- dashboard UI, componente, formulare, states;
- copy UX și documentație client;
- audit de skill-uri;
- verificare independentă.

## Regula de Ownership
Nu două unelte editează același fișier în paralel.

Default pentru proiectele client:
- Backend Agent output → Codex.
- Frontend Agent output → Claude Code.
- QA Agent output → rulează ultimul; poate fi executat de Codex sau Claude Code, dar trebuie să fie independent de implementatorul principal.

Ownership pe directoare:
- Codex: `infrastructure/`, `execution/`, backend app, Supabase, n8n, `projects/<id>/outputs/backend-agent/`.
- Claude Code: frontend app, UI docs, `projects/<id>/outputs/frontend-agent/`.
- Read-only pentru amândoi fără aprobare: `agents/*/SKILL.md`, `docs/rules/*`.
- Modificări arhitecturale în `AGENTS.md`, `CLAUDE.md`, `docs/blueprint.md` se fac doar cu aprobare explicită.

Dacă trebuie schimbat ownership-ul pentru un proiect, se notează în `projects/<id>/PROJECT.md` înainte de lucru.

## Task Brief pentru Operatori

Fiecare task non-trivial trebuie sa includa:

- `project_id`;
- agentul responsabil;
- owner pe fisiere;
- output asteptat;
- comanda de validare;
- context pack relevant;
- QA evidence cerut.

Template: `resources/templates/operator-task-brief.md`.

Regula practica: Codex/Claude Code sunt operatori, nu doar chat-uri. Un task bun catre operator seamana cu un ticket de lucru: clar, limitat, verificabil.

## Modele și Efort
- Codex reasoning `medium`: lucru normal.
- Codex reasoning `high/xhigh`: arhitectură, securitate, buguri dificile.
- Claude Code: folosit pentru review și sinteză, nu pentru runtime client.
- Claude Haiku subagents: scanări read-only simple (`repo-drift-scanner`, `secret-runtime-scanner`, `project-inventory-reporter`).
- Claude Sonnet subagents: review/QA mai greu (`skill-contract-reviewer`, `delivery-qa-reviewer`).

## Runtime Client
Automatizările client care trebuie să ruleze fără operator pot folosi API LLM doar după aprobare. Aceasta este o fază separată de MVP.

## Workflow-to-Skill Factory

Cand un workflow client a fost rulat cu succes si QA score >= 7, il putem transforma intr-un skill candidate folosind:

- `resources/templates/workflow-capture-template.md`;
- `resources/templates/skill-candidate-template.md`;
- `resources/templates/qa-evidence-checklist.md`.

Nu se creeaza sau modifica `SKILL.md` fara aprobare explicita. Pana atunci, skill candidate ramane document operational.

## Guardrails Claude Code
Project settings în `.claude/settings.json` activează:
- deny pentru `git push`, `rm -rf /`, chei LLM și instalări SDK LLM în MVP;
- ask pentru editări în `AGENTS.md`, `CLAUDE.md`, `agents/*/SKILL.md` și `docs/rules/*`;
- hook PreToolUse pentru fișiere sensibile;
- hook PostToolUse care avertizează dacă apare runtime LLM plătit în cod.
