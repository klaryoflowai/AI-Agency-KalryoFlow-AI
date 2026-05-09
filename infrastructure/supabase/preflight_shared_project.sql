-- AI Agency / KlaryoFlow AI
-- Shared-project preflight for running inside an existing Supabase project.
--
-- This script is read-only. Run it in Supabase SQL Editor before applying the
-- migrations. It shows whether the isolated `agency` schema already exists and
-- confirms that similarly named tables in `public` will not be touched.

with expected_tables(table_name) as (
  values
    ('clients'),
    ('projects'),
    ('agent_runs'),
    ('agent_run_events'),
    ('documents'),
    ('pricing_matrix'),
    ('runtime_llm_usage')
),
matches as (
  select
    table_schema,
    table_name
  from information_schema.tables
  where table_type = 'BASE TABLE'
    and table_schema in ('agency', 'public')
    and table_name in (select table_name from expected_tables)
)
select
  case
    when exists (select 1 from matches where table_schema = 'agency')
      then 'REVIEW_AGENCY_SCHEMA_ALREADY_HAS_TABLES'
    else 'OK_AGENCY_SCHEMA_CLEAR'
  end as agency_schema_status,
  coalesce(
    jsonb_agg(
      jsonb_build_object('schema', table_schema, 'table', table_name)
      order by table_schema, table_name
    ) filter (where table_schema is not null),
    '[]'::jsonb
  ) as matching_tables
from matches;

with wanted(schema_name) as (
  values ('agency')
)
select
  w.schema_name,
  (n.oid is not null) as schema_exists,
  count(c.oid) as object_count,
  coalesce(
    jsonb_agg(
      jsonb_build_object('type', c.relkind, 'name', c.relname)
      order by c.relname
    ) filter (where c.oid is not null),
    '[]'::jsonb
  ) as agency_objects
from wanted w
left join pg_namespace n
  on n.nspname = w.schema_name
left join pg_class c
  on c.relnamespace = n.oid
 and c.relkind in ('r', 'p', 'v', 'm', 'S', 'f')
group by w.schema_name, n.oid;
