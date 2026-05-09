# Execution Runner

`execution/agency.py` este runner-ul zero-API pentru MVP.

Nu apelează Anthropic/OpenAI sau alte API-uri LLM. Creează prompt packets pentru operatorii Codex/Claude Code, pregătește folderele de output și validează JSON-urile produse de agenți.

## Comenzi

Listează agenții cunoscuți:

```bash
python3 execution/agency.py list-agents
```

Pregătește un agent run:

```bash
python3 execution/agency.py prepare eval-agent YYYY-MM_Client
```

Alias:

```bash
python3 execution/agency.py run backend-agent YYYY-MM_Client
```

Promptul pentru operator va fi creat în:

```text
.tmp/agency/<project_id>/<timestamp>_<agent>_prompt.md
```

Prompt packet-ul include acum si `projects/<id>/CONTEXT.md`, daca exista, pentru a pastra memoria clientului in fiecare run.

Validează output-ul JSON produs de agent:

```bash
python3 execution/agency.py validate eval-agent YYYY-MM_Client
```

Vezi statusul proiectului:

```bash
python3 execution/agency.py status YYYY-MM_Client
```

Vezi următorul pas sigur pentru proiect:

```bash
python3 execution/agency.py next YYYY-MM_Client
```

Pregateste sync-ul catre Supabase fara scriere live:

```bash
python3 execution/agency.py sync-supabase YYYY-MM_Client
```

Scrierea live cere explicit `--apply` si env vars server-side:

```bash
SUPABASE_URL=https://xxxxx.supabase.co \
SUPABASE_SERVICE_KEY=... \
python3 execution/agency.py sync-supabase YYYY-MM_Client --apply
```

Cheia `service_role` nu se pune niciodata in frontend sau Git.

Valideaza migrarea Supabase fara conectare live:

```bash
python3 execution/validate_supabase_migrations.py
```

Rulează testele locale:

```bash
PYTHONPATH=.tmp/test-deps python3 -m pytest
```

În CI, GitHub Actions instalează `requirements-dev.txt` și rulează compile, migrații, scan runtime și pytest.

## Ownership Implicit

- `backend-agent` → Codex
- `frontend-agent` → Claude Code
- `qa-agent` → operator independent, ultimul în pipeline

## Output Validat

Runner-ul verifică:
- `schema_version` corect;
- câmpuri obligatorii per agent;
- reguli speciale pentru Eval Agent și QA Agent;
- contractele v2 pentru BD, Marketing și Client Success;
- QA delivery gate: `qa_score >= 7`, status aprobat, SOW coverage 100%.
- Next-action gate: QA nu poate porni până când agenții anteriori activi nu au validare `PASS`.
- Supabase sync dry-run: proiect, agent runs și documente sunt mapate înainte de scriere live.

## Ce Nu Face

- Nu cheltuie API credits.
- Nu trimite emailuri.
- Nu publică conținut.
- Nu scrie în Supabase fără `--apply` și env vars explicite.
- Nu aplică migrații Supabase live; verificarea DB este locală până avem aprobare.
