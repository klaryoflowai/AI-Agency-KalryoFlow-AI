#!/usr/bin/env python3
"""Local checks for Supabase migration files.

The validator is intentionally conservative. It does not connect to Supabase,
spend API credits, or require Docker. It catches the mistakes that matter most
for this MVP: missing core tables, missing RLS, accidental public grants, and
runtime LLM/API drift.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS_DIR = ROOT / "infrastructure" / "supabase" / "migrations"

REQUIRED_TABLES = (
    "clients",
    "projects",
    "agent_runs",
    "agent_run_events",
    "documents",
    "pricing_matrix",
    "runtime_llm_usage",
)

REQUIRED_SYNC_COLUMNS = (
    "local_project_id",
    "local_run_key",
    "local_document_key",
)

FORBIDDEN_PATTERNS = {
    "paid Anthropic runtime": r"\banthropic\b|ANTHROPIC_API_KEY",
    "paid OpenAI runtime": r"\bopenai\b|OPENAI_API_KEY",
    "service key exposure": r"SUPABASE_SERVICE_KEY|SUPABASE_SERVICE_ROLE_KEY",
    "unsafe security definer": r"\bsecurity\s+definer\b",
}


@dataclass
class CheckResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def normalize(sql: str) -> str:
    return re.sub(r"\s+", " ", sql.lower())


def migration_files() -> list[Path]:
    return sorted(MIGRATIONS_DIR.glob("*.sql"))


def has_table(sql: str, table: str) -> bool:
    pattern = rf"create\s+table\s+(if\s+not\s+exists\s+)?public\.{re.escape(table)}\b"
    return bool(re.search(pattern, sql, re.IGNORECASE))


def has_rls(sql: str, table: str) -> bool:
    pattern = rf"alter\s+table\s+public\.{re.escape(table)}\s+enable\s+row\s+level\s+security"
    return bool(re.search(pattern, sql, re.IGNORECASE))


def has_service_policy(sql: str, table: str) -> bool:
    pattern = rf"create\s+policy\s+.*?\s+on\s+public\.{re.escape(table)}\s+for\s+all\s+to\s+service_role"
    return bool(re.search(pattern, sql, re.IGNORECASE | re.DOTALL))


def has_public_grant(sql: str, table: str) -> bool:
    pattern = rf"grant\s+(select|insert|update|delete|all).*?\s+on\s+table\s+public\.{re.escape(table)}\s+to\s+(anon|authenticated)"
    return bool(re.search(pattern, sql, re.IGNORECASE | re.DOTALL))


def check_sql(sql: str) -> CheckResult:
    errors: list[str] = []
    warnings: list[str] = []

    if not sql.strip():
        errors.append("No SQL content found in migrations.")
        return CheckResult(errors, warnings)

    for label, pattern in FORBIDDEN_PATTERNS.items():
        if re.search(pattern, sql, re.IGNORECASE):
            errors.append(f"Forbidden pattern found: {label}")

    for table in REQUIRED_TABLES:
        if not has_table(sql, table):
            errors.append(f"Missing required table: public.{table}")
        if not has_rls(sql, table):
            errors.append(f"Missing RLS enable statement for public.{table}")
        if not has_service_policy(sql, table):
            errors.append(f"Missing service_role full-access policy for public.{table}")
        if has_public_grant(sql, table):
            errors.append(f"Unexpected anon/authenticated grant for public.{table}")

    normalized = normalize(sql)
    for column in REQUIRED_SYNC_COLUMNS:
        if column not in normalized:
            errors.append(f"Missing local sync column/index: {column}")
    if "runtime_llm_usage_actual_requires_approval" not in normalized:
        errors.append("Missing runtime LLM approval constraint.")
    if "runtime_llm_usage_approval_consistency" not in normalized:
        errors.append("Missing runtime LLM approval reference constraint.")
    if "agent_runs_qa_score_range" not in normalized:
        warnings.append("No explicit QA score range constraint found.")
    if "revoke all on table" not in normalized:
        warnings.append("No explicit table revokes found for anon/authenticated roles.")

    return CheckResult(errors, warnings)


def main() -> int:
    files = migration_files()
    if not files:
        print(f"FAIL: no migration files found in {MIGRATIONS_DIR.relative_to(ROOT)}")
        return 1

    combined_sql = "\n\n".join(path.read_text(encoding="utf-8") for path in files)
    result = check_sql(combined_sql)

    print("Supabase migration validation")
    print(f"Files: {', '.join(str(path.relative_to(ROOT)) for path in files)}")
    print(f"Status: {'PASS' if result.ok else 'FAIL'}")

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"- {error}")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"- {warning}")

    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
