from __future__ import annotations

from execution import validate_supabase_migrations as validator


def test_initial_migration_passes_static_validation() -> None:
    sql = "\n\n".join(path.read_text(encoding="utf-8") for path in validator.migration_files())

    result = validator.check_sql(sql)

    assert result.errors == []


def test_validator_rejects_missing_rls() -> None:
    sql = "\n\n".join(path.read_text(encoding="utf-8") for path in validator.migration_files())
    sql = sql.replace("alter table public.clients enable row level security;", "")

    result = validator.check_sql(sql)

    assert "Missing RLS enable statement for public.clients" in result.errors


def test_validator_rejects_runtime_llm_drift() -> None:
    sql = "\n\n".join(path.read_text(encoding="utf-8") for path in validator.migration_files())

    result = validator.check_sql(sql + "\n-- OPENAI_API_KEY=do-not-add\n")

    assert "Forbidden pattern found: paid OpenAI runtime" in result.errors
