# Brief pentru Freelancer Tehnic

## Contextul Proiectului
Construim o suită de agenți AI pentru o agenție de automatizare IMM-uri.
MVP-ul este **zero API LLM plătit**: Codex și Claude Code sunt operatorii care execută contractele din `agents/*/SKILL.md`.

Freelancerul NU construiește un runtime care apelează Anthropic/OpenAI. Construiește infrastructura de proiect, dashboard, Supabase, n8n și utilitare I/O. Runtime LLM plătit apare doar într-o fază ulterioară, per client, cu aprobare explicită.

---

## Ce Trebuie Construit

### 1. Backend - Utilitare I/O și API Intern
- API pentru proiecte, clienți, agent runs și documente
- Scripturi Python/TypeScript care citesc/scriu în Supabase
- Integrare cu `execution/agency.py` pentru prompt packets și validare JSON
- Zero import `anthropic`, `openai` sau SDK LLM în MVP
- Dacă un pas are nevoie de LLM, scriptul scrie promptul în `.tmp/` sau `agent_runs.input`, apoi operatorul Codex/Claude Code îl execută
- Logging complet în `agent_runs`
- Validare input/output JSON conform contractelor agenților

### 2. Orchestrare - n8n Workflows
- Workflow principal: primește `project_id` și creează pașii de agent
- Sub-workflow per agent pentru status, notificări și handoff
- Webhook endpoint pentru declanșare din Dashboard
- Nu apelează API LLM în MVP

### 3. Dashboard UI (Next.js / React)
Pagini necesare:
- `/dashboard` - overview toate proiectele cu status
- `/projects/new` - formular creare proiect nou
- `/projects/[id]` - detalii proiect, agenți, output-uri, documente
- `/clients` - lista clienți
- `/agent-runs/[id]` - input/output și status pentru un run

Nu e nevoie de:
- Autentificare complexă în prima fază
- Design elaborat de marketing

### 4. QA și Delivery
- Comenzi documentate pentru testare locală
- Playwright pentru fluxurile critice din dashboard
- Validare că niciun secret nu ajunge în frontend sau Git
- Checklist de livrare conectat la QA Agent

---

## Ce Există Deja
- Structura completă de foldere
- `AGENTS.md` și `CLAUDE.md`
- `SKILL.md` per agent
- Schema Supabase în `infrastructure/supabase/SETUP.md`
- Blueprint arhitectură în `docs/blueprint.md`

---

## Stack Obligatoriu MVP
- Python 3.11+ pentru utilitare I/O
- Supabase Python SDK sau client TS
- n8n Cloud pentru orchestrare
- Next.js 14+ pentru dashboard
- Tailwind CSS și shadcn/ui pentru UI
- Playwright pentru QA browser
- Git + GitHub pentru versionare

Interzis în MVP:
- `anthropic`
- `@anthropic-ai/sdk`
- `openai`
- orice cheie LLM runtime în `.env`

---

## Livrabil
- Cod funcțional pentru dashboard + backend I/O
- SQL/migrations documentate
- Workflows n8n exportate ca JSON
- Documentație setup
- Test run cu proiect fictiv

## Timeline & Budget
- Timeline: 2-3 săptămâni
- Budget orientativ: 1.500-2.500€
