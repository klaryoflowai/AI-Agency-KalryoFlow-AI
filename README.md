# AI Agency - Suita de Agenti pentru Automatizare IMM-uri

## Viziunea Proiectului
Agenție care oferă servicii de automatizare cu AI pentru companii mici și mijlocii.
Modelul de lucru pentru MVP este **zero API LLM plătit**: Codex și Claude Code sunt operatorii de implementare, iar agenții din `agents/*/SKILL.md` sunt contractele de lucru.

Automatizările client care trebuie să ruleze singure în producție pot folosi API LLM plătit doar ulterior, per client, cu aprobare explicită și cost inclus în ofertă.

---

## Structura Folderelor

```
ai-agency/
├── AGENTS.md                   ← context pentru Codex
├── CLAUDE.md                   ← context pentru Claude Code
├── README.md                   ← overview pentru oameni
├── docs/
│   ├── blueprint.md            ← arhitectura completă a sistemului
│   ├── business-model.md       ← modelul de business & strategie
│   ├── stack-tehnic.md         ← tehnologii folosite & de ce
│   ├── roadmap.md              ← plan de implementare pe faze
│   └── rules/                  ← reguli auto-încărcate per sesiune
│
├── agents/
│   ├── orchestrator/           ← coordonare
│   ├── eval-agent/             ← evaluare proiecte
│   ├── bd-agent/               ← business development
│   ├── backend-agent/          ← API-uri, DB, integrări server-side
│   ├── frontend-agent/         ← UI, dashboard-uri, React/Next.js
│   ├── qa-agent/               ← quality assurance & livrare
│   ├── ops-agent/              ← operațiuni & workflow-uri
│   ├── marketing-agent/        ← conținut & marketing
│   └── client-success-agent/   ← relație post-livrare
│
├── infrastructure/
│   ├── supabase/               ← schema bază de date
│   ├── n8n/                    ← workflow-uri orchestrare
│   └── dashboard/              ← UI vizual
│
├── projects/
│   └── template/               ← template refolosibil per proiect nou
│
└── resources/
    ├── pricing-matrix.md       ← matrice de prețuri servicii
    ├── client-brief-template.md← template brief pentru clienți
    └── freelancer-brief.md     ← brief pentru freelancerul tehnic
```

---

## Status Curent
- [x] Arhitectură definită
- [x] Structură foldere creată
- [x] Prompt-uri și contracte agenți scrise
- [x] Schema Supabase documentată
- [x] Migrații Supabase pregătite local + validator RLS
- [x] Supabase sync dry-run pregătit pentru runner
- [x] Strategie MVP zero API definită
- [x] Execution Runner v0 pentru prompt packets, validare JSON și next-action
- [x] Teste automate + GitHub Actions pentru runner, migrații și guardrails
- [x] Workflow-to-Skill Factory + Client Context Pack
- [x] Primul proiect pilot rulat end-to-end cu QA PASS
- [x] n8n Cloud-safe webhook workflow + validator local
- [x] Dashboard UI MVP local-first în Next.js
- [ ] Infrastructură configurată
- [ ] Dashboard conectat la Supabase live

---

## Tool-uri Folosite
| Rol | Tool |
|-----|------|
| Operatori AI MVP | Codex + Claude Code |
| Runtime LLM producție client | API plătit doar dacă este aprobat și facturat |
| Orchestrare | n8n Cloud pentru taskuri, statusuri, webhook-uri |
| Bază de date | Supabase |
| Dashboard UI | Vercel + Next.js |
| QA browser | Playwright |
| Versionare | Git + GitHub |
| Runner MVP | `python3 execution/agency.py` |
| Sync DB | `python3 execution/agency.py sync-supabase <project_id>` |
| n8n workflow QA | `python3 execution/validate_n8n_workflows.py` |
| CI | GitHub Actions + pytest + Next.js build |
| Competenta interna | Workflow-to-Skill Factory |

Supabase rulează în shared-project mode: obiectele MVP sunt izolate în schema
`agency`, astfel încât putem folosi un proiect Supabase existent fără să atingem
tabelele vechi din `public`.

---

## Principiul de Cost
În MVP, agenția folosește abonamentele Codex/Claude Code pentru analiză, implementare, QA și documentație. Nu se adaugă chei `ANTHROPIC_API_KEY` sau alte chei LLM în proiect decât pentru automatizări client aprobate explicit.
