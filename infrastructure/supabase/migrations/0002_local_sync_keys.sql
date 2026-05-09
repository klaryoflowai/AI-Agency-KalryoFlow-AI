-- Add stable local keys used by the zero-API runner when syncing folder-based
-- project state into Supabase. These keys let the runner upsert safely without
-- knowing Supabase-generated UUIDs in advance.

alter table public.projects
  add column if not exists local_project_id text;

create unique index if not exists projects_local_project_id_key
  on public.projects (local_project_id);

alter table public.projects
  drop constraint if exists projects_status_valid;

alter table public.projects
  add constraint projects_status_valid
  check (status in ('draft', 'active', 'pilot_ready', 'delivered', 'closed', 'cancelled'));

alter table public.agent_runs
  add column if not exists local_run_key text;

create unique index if not exists agent_runs_local_run_key_key
  on public.agent_runs (local_run_key);

alter table public.documents
  add column if not exists local_document_key text;

create unique index if not exists documents_local_document_key_key
  on public.documents (local_document_key);
