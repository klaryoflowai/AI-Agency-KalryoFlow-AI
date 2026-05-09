# Supabase - Schema & Setup

Acest folder contine schema DB versionata pentru MVP-ul zero-API.

Migrations sunt in:

```text
infrastructure/supabase/migrations/0001_initial_schema.sql
infrastructure/supabase/migrations/0002_local_sync_keys.sql
```

Nu am aplicat migrarea pe un proiect Supabase live. Totul este pregatit local, fara costuri si fara chei secrete.

## Ce Contine Schema

- `clients` - clienti, contacte, istoric si note.
- `projects` - proiecte client, status, estimari, agenti activati.
- `agent_runs` - fiecare rulare de agent per proiect.
- `agent_run_events` - timeline granular pentru pregatire, validare si erori.
- `documents` - SOW, propuneri, rapoarte, SOP-uri, user guides.
- `pricing_matrix` - rate si estimari standard.
- `runtime_llm_usage` - doar pentru runtime LLM client-side aprobat explicit si facturat.
- chei locale de sync: `projects.local_project_id`, `agent_runs.local_run_key`, `documents.local_document_key`.

## Reguli de Securitate

- RLS este activat pe toate tabelele din schema `public`.
- `anon` si `authenticated` nu primesc acces direct la tabele in MVP.
- Backend-ul/server-side foloseste `service_role`, niciodata frontend-ul.
- `service_role` nu se comite in repo si nu se expune in `NEXT_PUBLIC_*`.
- Runtime LLM platit este blocat prin proces: `actual` usage cere aprobare CEO, `approved_at` si `approval_reference`.

## Validare Locala

Ruleaza:

```bash
python3 execution/validate_supabase_migrations.py
```

Validatorul verifica:

- tabelele obligatorii;
- RLS pe fiecare tabela;
- politici `service_role`;
- lipsa granturilor catre `anon`/`authenticated`;
- lipsa driftului catre runtime LLM platit (`anthropic`, `openai`, chei API);
- constrangerile de aprobare pentru `runtime_llm_usage`.
- cheile locale folosite de runner pentru upsert sigur.

## Sync Runner -> Supabase

Dry-run, fara scriere live:

```bash
python3 execution/agency.py sync-supabase 2026-05_Restaurant_Demo
```

Scriere live, doar dupa ce migrațiile sunt aplicate si ai setat variabilele local:

```bash
SUPABASE_URL=https://xxxxx.supabase.co \
SUPABASE_SERVICE_KEY=eyJ... \
python3 execution/agency.py sync-supabase 2026-05_Restaurant_Demo --apply
```

Ce sincronizeaza:

- `projects` prin `local_project_id`;
- `agent_runs` prin `local_run_key`;
- `documents` prin `local_document_key`.

Nu sincronizeaza secrete si nu trimite runtime LLM API calls.

## Aplicare Cand Cream Proiectul Supabase

Preferat, cu Supabase CLI:

```bash
npx supabase --help
npx supabase login
npx supabase link --project-ref <project-ref>
```

CLI-ul Supabase foloseste in mod standard folderul `supabase/migrations`. Cand activam CLI-ul in repo, mutam sau sincronizam migrarea din `infrastructure/supabase/migrations/` in layout-ul standard, apoi rulam:

```bash
npx supabase db push
```

Daca nu folosim CLI, migrarea poate fi rulata manual in SQL Editor din dashboard-ul Supabase. Inainte de productie, facem backup si verificam tabelele/politicile in dashboard.

## Variabile de Mediu

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGci...
SUPABASE_SERVICE_KEY=eyJhbGci...   # doar pe server, niciodata in frontend

# MVP intern: fara chei LLM platite.
# Completeaza doar pentru runtime client-side aprobat si facturat.
CLIENT_RUNTIME_LLM_PROVIDER=
CLIENT_RUNTIME_LLM_API_KEY=
```

## Conectare Python - Exemplu Server-Side

Acest exemplu este pentru backend/operator tools, nu pentru frontend:

```python
from supabase import create_client
import os

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_SERVICE_KEY"],
)


def create_project(client_id, name, brief):
    result = supabase.table("projects").insert({
        "client_id": client_id,
        "name": name,
        "brief": brief,
        "status": "draft",
    }).execute()
    return result.data[0]


def log_agent_run(project_id, agent_name, input_data, output_data, status):
    result = supabase.table("agent_runs").insert({
        "project_id": project_id,
        "agent_name": agent_name,
        "input": input_data,
        "output": output_data,
        "status": status,
    }).execute()
    return result.data[0]
```
