# 🤖 CLAUDE.md — AI Agency / Suită Agenți pentru Automatizare IMM-uri

> Acest fișier este citit automat de Claude Code și Claude Cowork la fiecare sesiune.
> Conține tot contextul, regulile și arhitectura proiectului. NU modifica fără aprobare explicită.

---

## 🎯 Project Context

**Ce construim:** O agenție care automatizează procesele IMM-urilor folosind o suită de 8 agenți specializați, executați în MVP de Codex și Claude Code ca operatori. Fiecare client primește un proiect custom în care agenții relevanți sunt activați și executați în ordine de către un Orchestrator central.

**Cine conduce:** CEO non-tehnic — toate deciziile de business sunt ale lui. Claude Code gestionează implementarea tehnică.

**Obiectivul principal:** Sistem funcțional end-to-end: brief client → agenți execută → livrabil → client mulțumit.

---

## 🚨 Guardrails Critice (CITEȘTE PRIMUL)

- **NICIODATĂ** nu cheltui API credits fără să întrebi utilizatorul mai întâi
- **NICIODATĂ** nu suprascrie sau șterge un SKILL.md fără aprobare explicită
- **NICIODATĂ** `sudo` sau `rm -rf` în afara workspace-ului proiectului
- **NICIODATĂ** nu comite secrete (`.env`, `credentials.json`, `token.json`)
- **NICIODATĂ** nu push la remote fără permisiune explicită
- **NICIODATĂ** un script Python nu importă `anthropic`, `openai` sau alt SDK LLM în MVP — toate taskurile LLM trec prin Codex/Claude Code ca operatori, nu prin API plătit
- Runtime LLM API plătit se activează doar pentru automatizări client-side aprobate explicit și facturate clientului
- Orice output livrat clientului TREBUIE validat de QA Agent (scor ≥ 7/10)
- Un agent nu invadează niciodată rolul altui agent — respectă granițele din SKILL.md

---

## 🏗️ Arhitectura — 3 Layere

LLM-ul e stochastic. Business logica e deterministă. Le separăm strict.

### Layer 1: Skills (CE să facă)
- `agents/<name>/SKILL.md` — descrie rolul, system prompt, tools, output format, edge cases
- `agents/<name>/src/` — cod Python doar pentru I/O (HTTP, fișiere, DB). NICIODATĂ nu apelează LLM direct.
- Dacă un script are nevoie de LLM → scrie promptul în `.tmp/` sau `agent_runs.input`, iese, Codex/Claude Code îl preia în chat

### Layer 2: Orchestration (DECIZIA)
- Orchestratorul (n8n) rutează taskurile, statusurile și handoff-urile între agenți
- Claude Code în main-chat ia deciziile arhitecturale când lucrează ca operator principal
- Ownership implicit: Codex execută Backend Agent output; Claude Code execută Frontend Agent output; QA Agent rulează ultimul și independent
- Codex poate fi folosit ca operator paralel/reviewer când ownership-ul fișierelor este clar
- Toate taskurile LLM interne se fac pe abonamentele Codex/Claude Code — $0 API paid în MVP

### Layer 3: Shared Utilities
- `infrastructure/` — Supabase schema, n8n config, dashboard setup
- `resources/` — pricing matrix, templates, brief freelancer
- `execution/` — scripturi comune reutilizabile între agenți

---

## 📁 Structura Proiectului

```
ai-agency/
├── CLAUDE.md                    ← ești aici — context complet proiect
├── README.md                    ← overview pentru oameni
├── .env                         ← secrete — NICIODATĂ nu comite
├── .tmp/                        ← fișiere intermediare — regenerabile, nu comite
├── .gitignore                   ← include .env și .tmp/
│
├── agents/                      ← un folder per agent
│   ├── orchestrator/
│   │   ├── SKILL.md             ← rolul + system prompt + tools
│   │   └── src/                 ← cod I/O Python
│   ├── eval-agent/
│   ├── bd-agent/
│   ├── backend-agent/
│   ├── frontend-agent/
│   ├── ops-agent/
│   ├── qa-agent/
│   ├── marketing-agent/
│   └── client-success-agent/
│
├── docs/                        ← decizii arhitecturale & documentație
│   ├── blueprint.md
│   ├── business-model.md
│   ├── stack-tehnic.md
│   ├── codex-claude-operating-model.md
│   ├── roadmap.md
│   └── rules/                   ← reguli auto-încărcate per sesiune
│
├── infrastructure/
│   ├── supabase/SETUP.md        ← schema DB + cod conexiune
│   ├── n8n/                     ← workflow-uri orchestrare
│   └── dashboard/               ← config UI
│
├── projects/                    ← proiecte reale
│   └── template/PROJECT.md
│
├── resources/
│   ├── pricing-matrix.md
│   ├── client-brief-template.md
│   └── freelancer-brief.md
│
└── artefacts/                   ← fișiere grele generate (JSON >100KB, exports)
```

---

## ⚙️ Workflow — Cum Lucrăm

### Plan înainte de Cod (OBLIGATORIU)
Research e de 10-100x mai ieftin decât codul. Pentru orice task nebanal:
1. **Mod Plan** — read-only, zero risc, tokeni puțini
2. Ducem planul la aprobare — ieftin
3. Abia apoi execuție — costisitor
4. Cerință neclară → întotdeauna începem cu planul, nu cu codul

### Regula Scrap & Redo
După 2-3 încercări eșuate pe același fix:
1. STOP — se acumulează cod murdar
2. Revenim la stare curată, facem cea mai bună soluție într-o singură trecere
3. Contextul știe deja ce nu funcționează — folosește-l

### Subagent-ii — pentru tot ce nu necesită decizie
Orice research, căutare fișiere, citire loguri, test run → poate fi delegat unui subagent/reviewer atunci când utilizatorul cere lucru paralel.
- Subagentul procesează mult context și returnează un summary scurt — economie de context
- Subagent-ii rulează în background — main-chat-ul nu se blochează
- Subagent-ii sunt read-only reporters — modificările le aplică parent agent, nu subagentul

### /clear la Schimbarea Temei
La trecerea de la un agent la altul sau de la o temă la alta — resetează contextul. Altfel răspunsurile devin imprecise pe sesiuni lungi.

---

## 🧠 Auto-Îmbunătățire — 3 Canale

Erorile sunt oportunități. După fiecare sesiune: "ce am învățat, ce salvez?"

### 1. Memory (`agents/*/memory/`)
- Fapte confirmate despre proiect și preferințele utilizatorului
- Context strategic "de ce facem X"
- Resurse externe (dashboards, canale, boards)
- Triggere scriere: corecție explicită / aprobare soluție nestandard / context strategic nou / final sesiune

### 2. Skills (`agents/*/SKILL.md`)
Living documents — se actualizează pe parcurs cu:
- Limitări API și edge cases descoperite
- Secvențe îmbunătățite după utilizare reală
- Lecții învățate după fix-uri
- Nu crea skills noi fără aprobare

### 3. Rules (`docs/rules/`)
Se încarcă automat la fiecare sesiune:
- Erori repetate (2-3x) → regulă nouă ca instanța fresh să o rezolve din prima
- Guardrails noi după incidente
- Workflow patterns validate de utilizator
- Întotdeauna cere aprobare înainte de a modifica rules sau CLAUDE.md

---

## 💰 Cost Control

- Zero API paid pentru LLM intern — toate taskurile LLM prin abonamentele Codex/Claude Code
- Agenți cu cost ridicat: Backend Agent, Frontend Agent, QA Agent și Eval Agent — folosește doar pentru taskuri clare
- Dacă un agent depășește 10 iterații fără output clar → STOP, raportează utilizatorului
- Token budget orientativ per run: Eval ~8k, Backend ~15k, Frontend ~15k, QA ~10k, Ops ~10k, restul ~5k
- Runtime API plătit pentru clienți se estimează separat, se aprobă explicit și se facturează clientului

---

## 🤖 Orchestrator + 8 Agenți

| Agent | Rol | SKILL.md |
|-------|-----|----------|
| Orchestrator | Rutează taskuri, coordonează | `agents/orchestrator/SKILL.md` |
| Eval Agent | Analizează brief, estimează, aprobă | `agents/eval-agent/SKILL.md` |
| BD Agent | Leads, propuneri, pricing | `agents/bd-agent/SKILL.md` |
| Backend Agent | API-uri, DB, integrări server-side | `agents/backend-agent/SKILL.md` |
| Frontend Agent | UI, dashboard-uri, React/Next.js | `agents/frontend-agent/SKILL.md` |
| Ops Agent | Workflow-uri, procese, SOP-uri | `agents/ops-agent/SKILL.md` |
| QA Agent | Testare, verificare, livrare | `agents/qa-agent/SKILL.md` |
| Marketing Agent | Conținut agenție + clienți | `agents/marketing-agent/SKILL.md` |
| Client Success | Follow-up, upsell, feedback | `agents/client-success-agent/SKILL.md` |

**Regula granițelor:** Fiecare agent citește DOAR propriul SKILL.md și scrie DOAR în propriul output. Nu există comunicare directă între agenți — totul trece prin Orchestrator.

---

## 🔧 Operațiuni Comune

### Adaugă Agent Nou
1. Creează `agents/nume-agent/SKILL.md` cu: Rol, System Prompt, Tools, Output Format
2. Creează `agents/nume-agent/src/` pentru cod I/O
3. Actualizează `docs/blueprint.md`
4. Actualizează `agents/orchestrator/SKILL.md` cu noul agent disponibil
5. Cere aprobare înainte de a activa în producție

### Proiect Client Nou
1. Copiază `projects/template/` → `projects/YYYY-MM_NumeClient/`
2. Completează `PROJECT.md`
3. Declanșează Orchestratorul cu `project_id` nou
4. Monitorizează în Dashboard

### Adaugă Integrare Nouă
1. Adaugă tool-ul în SKILL.md-ul agentului relevant
2. Implementează I/O script în `agents/nume-agent/src/`
3. Testează izolat înainte de integrare în workflow

---

## 📊 Status Curent

- [x] Arhitectură definită
- [x] Structură foldere creată
- [x] SKILL.md pentru toți cei 8 agenți
- [x] Schema Supabase documentată
- [x] CLAUDE.md complet și upgradrat
- [x] .gitignore + .env.example setup
- [ ] Implementare backend Python per agent
- [ ] Workflow-uri n8n
- [ ] Dashboard UI
- [ ] Primul proiect pilot

---

## ❓ FAQ pentru Claude Code

**Q: Unde pun codul unui agent?**
A: `agents/nume-agent/src/` — cod Python doar I/O, niciodată LLM direct

**Q: Cum știu ce face un agent?**
A: Citește `agents/nume-agent/SKILL.md` — acolo e tot

**Q: Unde e schema bazei de date?**
A: `infrastructure/supabase/SETUP.md`

**Q: Pot cheltui API credits?**
A: NICIODATĂ fără aprobare explicită a utilizatorului

**Q: Un agent poate apela alt agent direct?**
A: NU — totul trece prin Orchestrator

**Q: Ce fac dacă cerința e neclară?**
A: Plan mode întâi, cer clarificări, abia apoi execuție

**Q: Unde salvez fișiere mari generate?**
A: `artefacts/` — niciodată în `agents/` sau `.tmp/`
