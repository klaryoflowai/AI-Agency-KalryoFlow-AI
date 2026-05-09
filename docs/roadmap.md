# Roadmap de Implementare

## Săptămâna 1-2: Fundația MVP Zero API
- [x] Aliniere arhitectură: Codex/Claude Code ca operatori, nu API runtime intern
- [x] Execuția tehnică este separată în `backend-agent` + `frontend-agent` + `qa-agent`
- [x] Inițializare Git + GitHub pentru versionare
- [x] Execution Runner v0 pentru prompt packets, validare JSON și next-action
- [x] Migrare Supabase initiala pregatita local + validator fara conectare live
- [x] Runner Supabase sync dry-run pregatit, live doar cu `--apply`
- [x] Teste automate + GitHub Actions pentru runner, migrații și guardrails
- [x] Workflow-to-Skill Factory documentat + Client Context Pack per proiect
- [x] n8n webhook workflow pregatit offline + validator local
- [x] Dashboard MVP local-first in Next.js
- [ ] Creare cont Supabase și rulare schema DB
- [ ] Creare cont n8n Cloud și primul webhook de test
- [x] Configurare dashboard minim sau flux local pe `projects/template`

## Săptămâna 3-4: Primii Agenți Operaționali
- [x] Eval Agent funcțional ca workflow manual/semi-manual
- [x] BD Agent funcțional pentru propuneri aprobate de CEO
- [x] Backend Agent + Frontend Agent rulați pe proiect fictiv
- [x] QA Agent validează output-urile înainte de livrare
- [x] Date salvate corect în folderul proiectului
- [ ] Date salvate corect în Supabase live

## Luna 2: Dashboard + Orchestrare
- [x] UI Dashboard construit în Next.js
- [ ] Conectare dashboard la Supabase
- [ ] Orchestrator n8n creează `agent_runs` și statusuri
- [ ] Ops Agent generează SOP-uri și workflow designs
- [ ] Client Success Agent adăugat pentru follow-up 7/30/90 zile

## Luna 3: Primul Client Real
- [ ] Primul proiect real rulat prin sistem
- [ ] Costurile și timpul de livrare măsurate
- [ ] Gaps documentate în `docs/rules/` sau `agents/*/memory/`
- [ ] Decizie: ce componente merită runtime API plătit

## Luna 4-6: Automatizări Client-Side
- [ ] Pentru fiecare client, runtime API doar cu aprobare explicită
- [ ] Cost LLM estimat inclus în ofertă și monitorizat
- [ ] Marketing Agent activ pe studii de caz
- [ ] 3-5 proiecte gestionate simultan
- [ ] Primele retainere semnate
