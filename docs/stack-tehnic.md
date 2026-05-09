# Stack Tehnic

## Decizie Principală
MVP-ul folosește **Codex + Claude Code ca operatori**, nu API LLM plătit ca runtime intern.

Această alegere reduce costul, păstrează controlul uman și permite validarea modelului de business înainte să construim automatizare complet unattended.

---

## Stack MVP

| Layer | Tool | De ce |
|-------|------|-------|
| AI Operator | Codex | Implementare, debugging, QA tehnic, dashboard |
| AI Reviewer/Operator | Claude Code | Review, prompturi, documentație, analiză paralelă |
| Orchestrare | n8n Cloud | Statusuri, webhook-uri, handoff între agenți |
| DB/Memory | Supabase | Proiecte, clienți, agent runs, documente |
| Dashboard | Next.js + Vercel | UI rapid, ieftin, ușor de extins |
| UI kit | Tailwind + shadcn/ui | Componente B2B rapide și coerente |
| QA | Playwright + pytest + Vitest | Verificare reală înainte de livrare |
| Versionare | Git + GitHub | Audit, rollback, colaborare |

---

## Politica Modelului

### Codex
- Default: model Codex pentru implementare și lucru în repo.
- Reasoning `medium`: taskuri obișnuite.
- Reasoning `high/xhigh`: arhitectură, debugging greu, review critic, securitate.
- Model mic/rapid: scanări repetitive, cleanup docs, checklisturi.

### Claude Code
- Folosit pentru review, documentație, business copy, prompt refinement și validare independentă.
- Nu editează aceleași fișiere simultan cu Codex fără ownership clar.
- Nu folosește API key runtime în proiectul MVP.

---

## Când Folosim API LLM Plătit

Doar pentru automatizări client care trebuie să ruleze singure în producție:
- triere emailuri/leaduri;
- clasificare documente;
- suport clienți automatizat;
- rapoarte generate periodic;
- extragere date din conversații sau documente.

Condiții obligatorii:
1. CEO aprobă explicit.
2. Costul estimat este inclus în ofertă.
3. Cheia este în backend/secrets manager, niciodată în frontend sau Git.
4. Există limită de cost și fallback uman.
5. QA Agent validează scenariile de eroare.

