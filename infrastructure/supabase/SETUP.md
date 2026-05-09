# Supabase - Schema & Setup

Acest folder contine schema DB versionata pentru MVP-ul zero-API.
Schema ruleaza in **shared-project mode**: toate obiectele KlaryoFlow sunt in
schema Postgres izolata `agency`, nu in `public`.

Migrations sunt in:

```text
infrastructure/supabase/migrations/0001_initial_schema.sql
infrastructure/supabase/migrations/0002_local_sync_keys.sql
infrastructure/supabase/preflight_shared_project.sql
```

Nu am aplicat migrarea pe un proiect Supabase live. Totul este pregatit local, fara costuri si fara chei secrete.

## Ce Contine Schema

- `agency.clients` - clienti, contacte, istoric si note.
- `agency.projects` - proiecte client, status, estimari, agenti activati.
- `agency.agent_runs` - fiecare rulare de agent per proiect.
- `agency.agent_run_events` - timeline granular pentru pregatire, validare si erori.
- `agency.documents` - SOW, propuneri, rapoarte, SOP-uri, user guides.
- `agency.pricing_matrix` - rate si estimari standard.
- `agency.runtime_llm_usage` - doar pentru runtime LLM client-side aprobat explicit si facturat.
- chei locale de sync: `agency.projects.local_project_id`, `agency.agent_runs.local_run_key`, `agency.documents.local_document_key`.

## Reguli de Securitate

- RLS este activat pe toate tabelele din schema `agency`.
- `anon` si `authenticated` nu primesc acces direct la tabele in MVP.
- Backend-ul/server-side foloseste `service_role`, niciodata frontend-ul.
- `service_role` nu se comite in repo si nu se expune in `NEXT_PUBLIC_*`.
- Runtime LLM platit este blocat prin proces: `actual` usage cere aprobare CEO, `approved_at` si `approval_reference`.
- In proiecte Supabase partajate, schema veche din `public` ramane neatinsa.

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
SUPABASE_SCHEMA=agency \
SUPABASE_SERVICE_KEY=eyJ... \
python3 execution/agency.py sync-supabase 2026-05_Restaurant_Demo --apply
```

Ce sincronizeaza:

- `agency.projects` prin `local_project_id`;
- `agency.agent_runs` prin `local_run_key`;
- `agency.documents` prin `local_document_key`.

Nu sincronizeaza secrete si nu trimite runtime LLM API calls.

## Aplicare Intr-un Proiect Supabase Existent

1. Ruleaza preflight-ul read-only in SQL Editor:

```sql
-- copiaza continutul din:
-- infrastructure/supabase/preflight_shared_project.sql
```

2. Daca `agency_schema_status` este `OK_AGENCY_SCHEMA_CLEAR`, aplica migrațiile.
   Daca vezi tabele deja existente in `agency`, opreste-te si verifica manual.

3. Pentru sync prin REST runner, mergi in Supabase Dashboard -> Project Settings
   -> Data API si adauga `agency` in lista de exposed schemas. Pastreaza granturile
   doar pentru `service_role`; nu acorda acces `anon` sau `authenticated` in MVP.

4. Ruleaza un dry-run local:

```bash
python3 execution/agency.py sync-supabase 2026-05_Restaurant_Demo
```

5. Abia dupa verificare ruleaza `--apply` cu variabilele locale setate.

## Aplicare Cand Cream Proiectul Supabase Nou

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
SUPABASE_SCHEMA=agency
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
    result = supabase.schema("agency").table("projects").insert({
        "client_id": client_id,
        "name": name,
        "brief": brief,
        "status": "draft",
    }).execute()
    return result.data[0]


def log_agent_run(project_id, agent_name, input_data, output_data, status):
    result = supabase.schema("agency").table("agent_runs").insert({
        "project_id": project_id,
        "agent_name": agent_name,
        "input": input_data,
        "output": output_data,
        "status": status,
    }).execute()
    return result.data[0]
```
