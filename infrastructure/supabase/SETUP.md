# 🗄️ Supabase — Schema & Setup

## Setup Inițial
1. Creează cont pe supabase.com
2. Creează un proiect nou: `ai-agency-db`
3. Rulează SQL-ul de mai jos în SQL Editor

---

## Schema Completă (SQL)

```sql
-- CLIENTS
CREATE TABLE clients (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  name TEXT NOT NULL,
  industry TEXT,
  contact_name TEXT,
  contact_email TEXT,
  contact_phone TEXT,
  history JSONB DEFAULT '{}',
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- PROJECTS
CREATE TABLE projects (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  client_id UUID REFERENCES clients(id),
  name TEXT NOT NULL,
  status TEXT DEFAULT 'draft',
  -- status: draft / active / delivered / closed / cancelled
  brief TEXT,
  industry TEXT,
  deadline DATE,
  estimated_hours INTEGER,
  estimated_cost_eur DECIMAL(10,2),
  final_cost_eur DECIMAL(10,2),
  agents_activated JSONB DEFAULT '[]',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- AGENT RUNS (log-ul fiecărui agent per proiect)
CREATE TABLE agent_runs (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  agent_name TEXT NOT NULL,
  input JSONB,
  output JSONB,
  status TEXT DEFAULT 'pending',
  -- status: pending / running / done / error
  error_message TEXT,
  duration_seconds INTEGER,
  created_at TIMESTAMP DEFAULT NOW()
);

-- DOCUMENTS
CREATE TABLE documents (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  type TEXT,
  -- type: sow / proposal / report / handover / sop / code
  title TEXT,
  content TEXT,
  url TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- PRICING MATRIX
CREATE TABLE pricing_matrix (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  service_type TEXT NOT NULL,
  description TEXT,
  base_hours_min INTEGER,
  base_hours_max INTEGER,
  hourly_rate_eur DECIMAL(10,2) DEFAULT 60,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- RUNTIME LLM USAGE
-- Folosit doar pentru automatizări client-side aprobate explicit.
-- MVP-ul intern cu Codex/Claude Code ca operatori nu scrie costuri aici.
CREATE TABLE runtime_llm_usage (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  client_id UUID REFERENCES clients(id),
  provider TEXT,
  model TEXT,
  purpose TEXT,
  input_tokens INTEGER DEFAULT 0,
  output_tokens INTEGER DEFAULT 0,
  estimated_cost_eur DECIMAL(10,4) DEFAULT 0,
  approved_by_ceo BOOLEAN DEFAULT false,
  billed_to_client BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW()
);

-- SEED: pricing matrix inițială
INSERT INTO pricing_matrix (service_type, description, base_hours_min, base_hours_max, hourly_rate_eur) VALUES
('workflow_automation', 'Automatizare workflow simplu', 5, 15, 60),
('api_integration', 'Integrare API externă', 10, 20, 60),
('custom_ai_agent_design', 'Design agent AI + prompturi + SOP, fără runtime API', 8, 20, 70),
('backend_implementation', 'API-uri, DB, webhooks, integrări server-side', 15, 40, 70),
('frontend_implementation', 'UI, formulare, dashboard, stări UX', 15, 35, 60),
('dashboard_ui', 'Dashboard / interfață vizuală', 10, 25, 60),
('database_setup', 'Setup și configurare bază de date', 5, 10, 60),
('qa_delivery', 'Testare, user guide, handover', 6, 16, 55),
('training_handover', 'Training și predare proiect', 3, 8, 50);
```

---

## Variabile de Mediu Necesare

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGci...
SUPABASE_SERVICE_KEY=eyJhbGci...   # doar pe server, niciodată în frontend

# MVP intern: fara chei LLM platite.
# Completeaza doar pentru runtime client-side aprobat si facturat.
CLIENT_RUNTIME_LLM_PROVIDER=
CLIENT_RUNTIME_LLM_API_KEY=
```

---

## Conexiune din Python

```python
from supabase import create_client
import os

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_SERVICE_KEY")
)

# Exemplu: creează proiect nou
def create_project(client_id, name, brief):
    result = supabase.table("projects").insert({
        "client_id": client_id,
        "name": name,
        "brief": brief,
        "status": "draft"
    }).execute()
    return result.data[0]

# Exemplu: loghează run agent
def log_agent_run(project_id, agent_name, input_data, output_data, status):
    supabase.table("agent_runs").insert({
        "project_id": project_id,
        "agent_name": agent_name,
        "input": input_data,
        "output": output_data,
        "status": status
    }).execute()
```
