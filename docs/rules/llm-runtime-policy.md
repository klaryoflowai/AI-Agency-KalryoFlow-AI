# Regula: LLM Runtime Policy

## MVP Intern
- Codex și Claude Code sunt operatori de lucru.
- Nu se folosesc chei `ANTHROPIC_API_KEY`, `OPENAI_API_KEY` sau SDK-uri LLM în codul MVP.
- Scripturile care au nevoie de LLM scriu promptul în `.tmp/` sau în `agent_runs.input`, apoi se opresc.

## Runtime Client-Side
API LLM plătit este permis doar dacă:
- CEO aprobă explicit;
- costul estimat este inclus în ofertă/retainer;
- cheia stă doar în backend/secrets manager;
- există limită de cost, retry policy și fallback uman;
- QA Agent validează înainte de livrare.

## Interzis
- Chei LLM în Git.
- Chei LLM în frontend.
- Automatizări unattended fără cost cap.
- Promisiuni comerciale despre autonomie completă fără validare QA.

