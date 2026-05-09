# Blueprint - Arhitectura Completă a Sistemului

## Principiul de Bază

Suita funcționează ca o **companie virtuală** activată per proiect.
Fiecare agent are rol fix, skill pre-setat și comunică prin Orchestrator.

Pentru MVP, agenții nu rulează ca API LLM autonome. Codex și Claude Code sunt operatorii care citesc contractele agenților, execută taskurile și salvează output-urile. Runtime-ul LLM plătit se activează doar pentru automatizări client care trebuie să funcționeze singure în producție.

---

## Diagrama Sistemului - MVP Zero API

```
┌─────────────────────────────────────────────────────┐
│                  DASHBOARD (Vercel)                 │
│         Proiecte, agenți, status, livrabile         │
└───────────────────────┬─────────────────────────────┘
                        │ HTTP/Webhook
┌───────────────────────▼─────────────────────────────┐
│              ORCHESTRATOR (n8n Cloud)                │
│     Creează taskuri → rutează → colectează status    │
└──┬──────┬──────┬─────────┬──────────┬──────┬────────┘
   │      │      │         │          │      │
   ▼      ▼      ▼         ▼          ▼      ▼
 [BD]  [EVAL] [BACKEND] [FRONTEND]  [OPS]  [QA]  [CS]
        CONTRACTE DE LUCRU EXECUTATE DE CODEX/CLAUDE CODE
┌─────────────────────────────────────────────────────┐
│              SUPABASE (Creierul de date)             │
│   Proiecte │ Agent runs │ Documents │ Logs          │
└─────────────────────────────────────────────────────┘
```

---

## Anatomia unui Agent

```
AGENT = Role Prompt      (identitate + responsabilități)
      + Input Contract   (ce primește)
      + Allowed Tools    (ce poate folosi operatorul)
      + Output Schema    (JSON stabil, versionat)
      + Write Boundary   (unde are voie să scrie)
      + QA Gate          (cum este validat)
```

---

## Fluxul per Proiect Nou

```
1. CEO completează brieful în Dashboard sau în projects/<id>/PROJECT.md
2. Se creează project_id unic în Supabase și folder local de proiect
3. Orchestratorul primește project_id + brief
4. Eval Agent analizează → returnează plan JSON + SOW draft
5. CEO aprobă scope-ul și costul
6. Orchestratorul activează Backend, Frontend, Ops, BD etc. după plan
7. `execution/agency.py` generează prompt packet-uri pentru operatorii Codex/Claude Code
8. Codex/Claude Code execută agenții ca operatori, nu ca API runtime
9. Runner-ul validează JSON-urile de output și loghează local în `.tmp/agency/`
10. Output-urile se salvează în Supabase și în projects/<id>/outputs/
11. QA Agent verifică tot înainte de livrare
12. Client Success Agent preia follow-up la 7/30/90 zile
```

---

## Orchestrator + 8 Agenți Operaționali

| # | Agent | Rol Principal |
|---|-------|---------------|
| 0 | Orchestrator | Rutează taskuri între agenți |
| 1 | Eval Agent | Analizează brief, estimează, aprobă |
| 2 | BD Agent | Leads, propuneri comerciale, pricing |
| 3 | Backend Agent | API-uri, DB, integrări, automatizări server-side |
| 4 | Frontend Agent | UI, dashboard-uri, componente React/Next.js |
| 5 | Ops Agent | Workflow-uri interne client, SOP-uri |
| 6 | QA Agent | Testare, verificare, livrare |
| 7 | Marketing Agent | Conținut agenție + conținut clienți |
| 8 | Client Success Agent | Follow-up, upsell, feedback |

Notă: Orchestratorul coordonează, dar nu livrează direct lucrări client. Execuția tehnică este separată în `backend-agent`, `frontend-agent` și `qa-agent`.

---

## Stack Tehnic

| Layer | Tool | Rol |
|-------|------|-----|
| AI Operator MVP | Codex + Claude Code | Analiză, implementare, QA, documentație |
| Runtime LLM client | API plătit opțional | Doar pentru automatizări unattended aprobate și facturate |
| Orchestrare | n8n Cloud | Logica de rutare, statusuri, webhook-uri |
| Date | Supabase | Memoria sistemului și jurnal de execuție |
| UI | Next.js pe Vercel | Dashboard vizual |
| QA | Playwright, pytest, Vitest | Verificare livrabile |
| Versionare | Git + GitHub | Control cod și audit |

---

## Schema Bază de Date (Supabase)

Schema completă se află în `infrastructure/supabase/SETUP.md`. Entitățile principale:

```sql
clients
projects
agent_runs
agent_run_events
documents
pricing_matrix
runtime_llm_usage -- doar pentru faza cu API client-side
```

---

## Cost Lunar Estimat (Bootstrap)

| Serviciu | Cost/lună MVP |
|----------|---------------|
| Codex / Claude Code | abonamente existente |
| API LLM pentru runtime client | 0€ în MVP, apoi per client aprobat |
| n8n Cloud | ~20€ |
| Supabase | 0-25€ |
| Vercel | 0€ |
| **TOTAL operațional MVP** | **~20-45€ + abonamentele AI existente** |

---

## Regula Runtime LLM

Folosim API plătit numai când automatizarea clientului trebuie să ruleze singură fără operator uman. Înainte de orice cheie LLM runtime:

1. CEO aprobă explicit.
2. Costul lunar estimat este inclus în propunerea clientului.
3. Cheia stă doar în backend/secrets manager.
4. `agent_runs` loghează input/output sumar, status, cost estimat și erori.
5. QA Agent validează că există fallback uman și limită de cost.
