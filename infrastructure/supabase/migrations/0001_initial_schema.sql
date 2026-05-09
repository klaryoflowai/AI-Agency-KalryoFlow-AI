-- AI Agency / KlaryoFlow AI
-- Initial Supabase schema for the zero-API MVP.
--
-- This migration is intentionally backend/operator oriented:
-- - no public anon/authenticated access by default;
-- - RLS enabled on every public table;
-- - runtime LLM usage is tracked only when approved and billed per client.

create schema if not exists extensions;
create extension if not exists pgcrypto with schema extensions;

create table if not exists public.clients (
  id uuid primary key default extensions.gen_random_uuid(),
  name text not null,
  industry text,
  contact_name text,
  contact_email text,
  contact_phone text,
  history jsonb not null default '{}'::jsonb,
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  constraint clients_contact_email_format
    check (contact_email is null or position('@' in contact_email) > 1)
);

create table if not exists public.projects (
  id uuid primary key default extensions.gen_random_uuid(),
  client_id uuid references public.clients(id) on delete set null,
  name text not null,
  status text not null default 'draft',
  brief text,
  industry text,
  deadline date,
  estimated_hours integer,
  estimated_cost_eur numeric(10,2),
  final_cost_eur numeric(10,2),
  agents_activated jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  constraint projects_status_valid
    check (status in ('draft', 'active', 'delivered', 'closed', 'cancelled')),
  constraint projects_estimated_hours_non_negative
    check (estimated_hours is null or estimated_hours >= 0),
  constraint projects_costs_non_negative
    check (
      (estimated_cost_eur is null or estimated_cost_eur >= 0)
      and (final_cost_eur is null or final_cost_eur >= 0)
    )
);

create table if not exists public.agent_runs (
  id uuid primary key default extensions.gen_random_uuid(),
  project_id uuid not null references public.projects(id) on delete cascade,
  agent_name text not null,
  operator text,
  input jsonb not null default '{}'::jsonb,
  output jsonb not null default '{}'::jsonb,
  output_path text,
  prompt_packet_path text,
  status text not null default 'pending',
  qa_score numeric(3,1),
  error_message text,
  duration_seconds integer,
  prepared_at timestamptz,
  started_at timestamptz,
  completed_at timestamptz,
  validated_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  constraint agent_runs_agent_name_valid
    check (
      agent_name in (
        'orchestrator',
        'eval-agent',
        'bd-agent',
        'backend-agent',
        'frontend-agent',
        'ops-agent',
        'qa-agent',
        'marketing-agent',
        'client-success-agent'
      )
    ),
  constraint agent_runs_status_valid
    check (status in ('pending', 'prepared', 'running', 'waiting_for_operator', 'done', 'validated', 'error', 'blocked')),
  constraint agent_runs_operator_valid
    check (operator is null or operator in ('codex', 'claude-code', 'ceo', 'qa-operator', 'other')),
  constraint agent_runs_duration_non_negative
    check (duration_seconds is null or duration_seconds >= 0),
  constraint agent_runs_qa_score_range
    check (qa_score is null or (qa_score >= 0 and qa_score <= 10))
);

create table if not exists public.agent_run_events (
  id uuid primary key default extensions.gen_random_uuid(),
  agent_run_id uuid references public.agent_runs(id) on delete cascade,
  project_id uuid not null references public.projects(id) on delete cascade,
  agent_name text,
  event_type text not null,
  event_payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),

  constraint agent_run_events_event_type_not_blank
    check (length(trim(event_type)) > 0)
);

create table if not exists public.documents (
  id uuid primary key default extensions.gen_random_uuid(),
  project_id uuid references public.projects(id) on delete cascade,
  type text not null,
  title text,
  content text,
  url text,
  source_agent text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),

  constraint documents_type_valid
    check (type in ('sow', 'proposal', 'report', 'handover', 'sop', 'code', 'qa_report', 'user_guide', 'workflow', 'other'))
);

create table if not exists public.pricing_matrix (
  id uuid primary key default extensions.gen_random_uuid(),
  service_type text not null unique,
  description text,
  base_hours_min integer,
  base_hours_max integer,
  hourly_rate_eur numeric(10,2) not null default 60,
  updated_at timestamptz not null default now(),

  constraint pricing_matrix_hours_non_negative
    check (
      (base_hours_min is null or base_hours_min >= 0)
      and (base_hours_max is null or base_hours_max >= 0)
      and (base_hours_min is null or base_hours_max is null or base_hours_min <= base_hours_max)
    ),
  constraint pricing_matrix_rate_positive
    check (hourly_rate_eur > 0)
);

create table if not exists public.runtime_llm_usage (
  id uuid primary key default extensions.gen_random_uuid(),
  project_id uuid references public.projects(id) on delete cascade,
  client_id uuid references public.clients(id) on delete set null,
  usage_type text not null default 'estimate',
  provider text,
  model text,
  purpose text,
  input_tokens integer not null default 0,
  output_tokens integer not null default 0,
  estimated_cost_eur numeric(10,4) not null default 0,
  approved_by_ceo boolean not null default false,
  approved_by text,
  approved_at timestamptz,
  approval_reference text,
  billed_to_client boolean not null default false,
  created_at timestamptz not null default now(),

  constraint runtime_llm_usage_type_valid
    check (usage_type in ('estimate', 'actual')),
  constraint runtime_llm_usage_tokens_non_negative
    check (input_tokens >= 0 and output_tokens >= 0),
  constraint runtime_llm_usage_cost_non_negative
    check (estimated_cost_eur >= 0),
  constraint runtime_llm_usage_actual_requires_approval
    check (usage_type = 'estimate' or approved_by_ceo = true),
  constraint runtime_llm_usage_approval_consistency
    check (
      approved_by_ceo = false
      or (approved_at is not null and length(trim(coalesce(approval_reference, ''))) > 0)
    )
);

create or replace function public.set_updated_at()
returns trigger
language plpgsql
set search_path = public
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists clients_set_updated_at on public.clients;
create trigger clients_set_updated_at
  before update on public.clients
  for each row execute function public.set_updated_at();

drop trigger if exists projects_set_updated_at on public.projects;
create trigger projects_set_updated_at
  before update on public.projects
  for each row execute function public.set_updated_at();

drop trigger if exists agent_runs_set_updated_at on public.agent_runs;
create trigger agent_runs_set_updated_at
  before update on public.agent_runs
  for each row execute function public.set_updated_at();

drop trigger if exists documents_set_updated_at on public.documents;
create trigger documents_set_updated_at
  before update on public.documents
  for each row execute function public.set_updated_at();

drop trigger if exists pricing_matrix_set_updated_at on public.pricing_matrix;
create trigger pricing_matrix_set_updated_at
  before update on public.pricing_matrix
  for each row execute function public.set_updated_at();

create index if not exists clients_name_idx on public.clients (name);
create index if not exists projects_client_id_idx on public.projects (client_id);
create index if not exists projects_status_idx on public.projects (status);
create index if not exists agent_runs_project_id_idx on public.agent_runs (project_id);
create index if not exists agent_runs_status_idx on public.agent_runs (status);
create index if not exists agent_runs_agent_name_idx on public.agent_runs (agent_name);
create index if not exists agent_run_events_project_id_idx on public.agent_run_events (project_id);
create index if not exists documents_project_id_idx on public.documents (project_id);
create index if not exists runtime_llm_usage_project_id_idx on public.runtime_llm_usage (project_id);
create index if not exists runtime_llm_usage_client_id_idx on public.runtime_llm_usage (client_id);

alter table public.clients enable row level security;
alter table public.projects enable row level security;
alter table public.agent_runs enable row level security;
alter table public.agent_run_events enable row level security;
alter table public.documents enable row level security;
alter table public.pricing_matrix enable row level security;
alter table public.runtime_llm_usage enable row level security;

revoke all on table public.clients from anon, authenticated;
revoke all on table public.projects from anon, authenticated;
revoke all on table public.agent_runs from anon, authenticated;
revoke all on table public.agent_run_events from anon, authenticated;
revoke all on table public.documents from anon, authenticated;
revoke all on table public.pricing_matrix from anon, authenticated;
revoke all on table public.runtime_llm_usage from anon, authenticated;

grant usage on schema public to service_role;
grant all on table public.clients to service_role;
grant all on table public.projects to service_role;
grant all on table public.agent_runs to service_role;
grant all on table public.agent_run_events to service_role;
grant all on table public.documents to service_role;
grant all on table public.pricing_matrix to service_role;
grant all on table public.runtime_llm_usage to service_role;

drop policy if exists "service_role full access clients" on public.clients;
create policy "service_role full access clients"
  on public.clients for all
  to service_role
  using (true)
  with check (true);

drop policy if exists "service_role full access projects" on public.projects;
create policy "service_role full access projects"
  on public.projects for all
  to service_role
  using (true)
  with check (true);

drop policy if exists "service_role full access agent_runs" on public.agent_runs;
create policy "service_role full access agent_runs"
  on public.agent_runs for all
  to service_role
  using (true)
  with check (true);

drop policy if exists "service_role full access agent_run_events" on public.agent_run_events;
create policy "service_role full access agent_run_events"
  on public.agent_run_events for all
  to service_role
  using (true)
  with check (true);

drop policy if exists "service_role full access documents" on public.documents;
create policy "service_role full access documents"
  on public.documents for all
  to service_role
  using (true)
  with check (true);

drop policy if exists "service_role full access pricing_matrix" on public.pricing_matrix;
create policy "service_role full access pricing_matrix"
  on public.pricing_matrix for all
  to service_role
  using (true)
  with check (true);

drop policy if exists "service_role full access runtime_llm_usage" on public.runtime_llm_usage;
create policy "service_role full access runtime_llm_usage"
  on public.runtime_llm_usage for all
  to service_role
  using (true)
  with check (true);

insert into public.pricing_matrix (
  service_type,
  description,
  base_hours_min,
  base_hours_max,
  hourly_rate_eur
) values
  ('workflow_automation', 'Automatizare workflow simplu', 5, 15, 60),
  ('api_integration', 'Integrare API externa', 10, 20, 60),
  ('custom_ai_agent_design', 'Design agent AI + prompturi + SOP, fara runtime API', 8, 20, 70),
  ('backend_implementation', 'API-uri, DB, webhooks, integrari server-side', 15, 40, 70),
  ('frontend_implementation', 'UI, formulare, dashboard, stari UX', 15, 35, 60),
  ('dashboard_ui', 'Dashboard / interfata vizuala', 10, 25, 60),
  ('database_setup', 'Setup si configurare baza de date', 5, 10, 60),
  ('qa_delivery', 'Testare, user guide, handover', 6, 16, 55),
  ('training_handover', 'Training si predare proiect', 3, 8, 50)
on conflict (service_type) do update set
  description = excluded.description,
  base_hours_min = excluded.base_hours_min,
  base_hours_max = excluded.base_hours_max,
  hourly_rate_eur = excluded.hourly_rate_eur,
  updated_at = now();
