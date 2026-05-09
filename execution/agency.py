#!/usr/bin/env python3
"""Zero-API execution runner for the AI Agency MVP.

The runner does not call any LLM provider. It prepares operator prompt packets,
creates output folders, and validates JSON outputs produced by Codex/Claude Code.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, parse, request


ROOT = Path(__file__).resolve().parents[1]
PROJECTS_DIR = ROOT / "projects"
TMP_RUNS_DIR = ROOT / ".tmp" / "agency"
DEFAULT_SUPABASE_SCHEMA = "agency"
PIPELINE_ORDER = (
    "orchestrator",
    "eval-agent",
    "bd-agent",
    "backend-agent",
    "frontend-agent",
    "ops-agent",
    "marketing-agent",
    "client-success-agent",
    "qa-agent",
)


@dataclass(frozen=True)
class AgentContract:
    name: str
    schema_version: str
    output_json: str
    owner: str
    required_fields: tuple[str, ...]
    extra_outputs: tuple[str, ...] = ()


@dataclass(frozen=True)
class NextAction:
    kind: str
    agent: str | None
    status: str
    message: str
    command: str | None = None


@dataclass(frozen=True)
class SupabaseSyncPlan:
    project: dict[str, Any]
    agent_runs: tuple[dict[str, Any], ...]
    documents: tuple[dict[str, Any], ...]


AGENTS: dict[str, AgentContract] = {
    "orchestrator": AgentContract(
        name="orchestrator",
        schema_version="orchestrator.v1",
        output_json="orchestration.json",
        owner="Codex or Claude Code",
        required_fields=(
            "schema_version",
            "project_id",
            "agents_activated",
            "execution_order",
            "human_approval_required",
            "estimated_completion",
            "notes",
        ),
    ),
    "eval-agent": AgentContract(
        name="eval-agent",
        schema_version="eval-agent.v1",
        output_json="evaluation.json",
        owner="Codex or Claude Code; CEO approval required",
        required_fields=(
            "schema_version",
            "feasibility",
            "complexity_score",
            "estimated_hours",
            "estimated_cost_eur",
            "timeline_weeks",
            "risks",
            "agents_needed",
            "runtime_llm_needed",
            "runtime_llm_cost_estimate_eur_month",
            "clarifying_questions",
            "sow_draft",
            "recommendation",
            "notes",
        ),
        extra_outputs=("sow.md",),
    ),
    "bd-agent": AgentContract(
        name="bd-agent",
        schema_version="bd-agent.v2",
        output_json="proposal.json",
        owner="Codex or Claude Code; CEO approves before send",
        required_fields=(
            "schema_version",
            "document_type",
            "lead_qualification",
            "subject",
            "content",
            "cta",
            "pricing_source",
            "discount_applied",
            "ceo_approval_required",
            "next_followup_days",
            "notes",
        ),
        extra_outputs=("proposal.md",),
    ),
    "backend-agent": AgentContract(
        name="backend-agent",
        schema_version="backend-agent.v1",
        output_json="implementation-report.json",
        owner="Codex",
        required_fields=(
            "schema_version",
            "task_completed",
            "files",
            "endpoints",
            "env_vars_needed",
            "dependencies",
            "runtime_llm_used",
            "setup_instructions",
            "handoff_to_frontend",
            "notes",
        ),
        extra_outputs=("README.md",),
    ),
    "frontend-agent": AgentContract(
        name="frontend-agent",
        schema_version="frontend-agent.v1",
        output_json="implementation-report.json",
        owner="Claude Code",
        required_fields=(
            "schema_version",
            "task_completed",
            "files",
            "pages",
            "env_vars_needed",
            "dependencies",
            "runtime_llm_used",
            "setup_instructions",
            "handoff_to_qa",
            "notes",
        ),
        extra_outputs=("README.md",),
    ),
    "ops-agent": AgentContract(
        name="ops-agent",
        schema_version="ops-agent.v1",
        output_json="workflow-design.json",
        owner="Codex or Claude Code",
        required_fields=(
            "schema_version",
            "process_map",
            "automation_opportunities",
            "recommended_automations",
            "workflow_design",
            "n8n_workflow_json",
            "sop_document",
            "training_notes",
        ),
        extra_outputs=("sop.md",),
    ),
    "qa-agent": AgentContract(
        name="qa-agent",
        schema_version="qa-agent.v1",
        output_json="qa-report.json",
        owner="Independent QA operator",
        required_fields=(
            "schema_version",
            "qa_score",
            "status",
            "backend_tests",
            "frontend_tests",
            "e2e_tests",
            "sow_coverage",
            "bugs_found",
            "delivery_checklist",
            "user_guide",
            "handover_notes",
        ),
        extra_outputs=("user-guide.md",),
    ),
    "marketing-agent": AgentContract(
        name="marketing-agent",
        schema_version="marketing-agent.v2",
        output_json="content.json",
        owner="Claude Code or Codex; CEO approves before publish",
        required_fields=(
            "schema_version",
            "content_type",
            "pillar",
            "title",
            "meta_description",
            "target_keyword",
            "target_audience",
            "content",
            "cta",
            "distribution_channels",
            "estimated_reach",
            "metrics_to_track",
            "data_sources_used",
            "anonymization_confirmed",
            "approval_required",
            "notes",
        ),
    ),
    "client-success-agent": AgentContract(
        name="client-success-agent",
        schema_version="client-success-agent.v2",
        output_json="client-success.json",
        owner="Claude Code or Codex; CEO approves before send",
        required_fields=(
            "schema_version",
            "communication_type",
            "client_id",
            "project_id",
            "health_score",
            "health_score_breakdown",
            "churn_risk",
            "churn_signals",
            "content",
            "upsell_opportunities",
            "escalation_required",
            "escalation_reason",
            "action_required_from_ceo",
            "next_touchpoint_days",
            "notes",
        ),
    ),
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slug_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def fail(message: str, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"Missing file: {path.relative_to(ROOT)}")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def project_dir(project_id: str) -> Path:
    path = PROJECTS_DIR / project_id
    if not path.is_dir():
        fail(f"Project not found: projects/{project_id}")
    if not (path / "PROJECT.md").is_file():
        fail(f"Project is missing PROJECT.md: projects/{project_id}")
    return path


def contract_for(agent_name: str) -> AgentContract:
    try:
        return AGENTS[agent_name]
    except KeyError:
        names = ", ".join(sorted(AGENTS))
        fail(f"Unknown agent '{agent_name}'. Available agents: {names}")


def output_dir(project_id: str, agent_name: str) -> Path:
    return project_dir(project_id) / "outputs" / agent_name


def output_json_path(project_id: str, contract: AgentContract) -> Path:
    return output_dir(project_id, contract.name) / contract.output_json


def parse_active_agents(project_md: str) -> list[str]:
    active: list[str] = []
    for line in project_md.splitlines():
        match = re.match(r"- \[x\]\s+([a-z-]+)\s+", line.strip())
        if match:
            active.append(match.group(1))
    return active


def first_match(pattern: str, text: str, default: str = "") -> str:
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else default


def extract_brief(project_md: str) -> str:
    match = re.search(r"## Brief Client.*?```(?:\w+)?\n(.*?)\n```", project_md, re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_project_title(project_md: str, project_id: str) -> str:
    title = first_match(r"^# PROJECT:\s+(.+)$", project_md, project_id)
    return title.split("—", 1)[0].strip()


def extract_yaml_value(project_md: str, key: str, default: str = "") -> str:
    pattern = rf"^\s*{re.escape(key)}:\s*(.+?)\s*(?:#.*)?$"
    raw = first_match(pattern, project_md, default)
    return raw.strip().strip('"').strip("'")


def normalize_project_status(status: str) -> str:
    normalized = status.strip().lower().replace("-", "_")
    allowed = {"draft", "active", "pilot_ready", "delivered", "closed", "cancelled"}
    return normalized if normalized in allowed else "draft"


def normalize_agent_run_status(status: str) -> str:
    return {
        "PASS": "validated",
        "FAIL": "error",
        "BAD_REPORT": "error",
        "OUTPUT_READY": "done",
        "PREPARED": "prepared",
        "PENDING": "pending",
    }.get(status, "pending")


def log_event(project_id: str, event: dict[str, Any]) -> None:
    run_dir = TMP_RUNS_DIR / project_id
    run_dir.mkdir(parents=True, exist_ok=True)
    event = {"created_at": now_iso(), **event}
    with (run_dir / "runs.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def prompt_packet(project_id: str, contract: AgentContract) -> str:
    project_path = project_dir(project_id)
    skill_path = ROOT / "agents" / contract.name / "SKILL.md"
    project_md = read_text(project_path / "PROJECT.md")
    context_path = project_path / "CONTEXT.md"
    context_md = context_path.read_text(encoding="utf-8") if context_path.is_file() else "No CONTEXT.md found for this project."
    skill_md = read_text(skill_path)
    pricing_md = read_text(ROOT / "resources" / "pricing-matrix.md")
    owner_doc = read_text(ROOT / "docs" / "codex-claude-operating-model.md")
    required = "\n".join(f"- `{field}`" for field in contract.required_fields)
    extra = "\n".join(f"- `{name}`" for name in contract.extra_outputs) or "- none"

    return f"""# Operator Prompt Packet

## Metadata
- project_id: `{project_id}`
- agent: `{contract.name}`
- recommended_operator: `{contract.owner}`
- generated_at: `{now_iso()}`
- output_json: `projects/{project_id}/outputs/{contract.name}/{contract.output_json}`

## Zero-API MVP Rules
- Do not call Anthropic/OpenAI/provider APIs.
- Do not add paid LLM SDKs or runtime API keys.
- If runtime LLM is needed for the client, flag it explicitly with cost estimate and CEO approval requirement.
- Respect file ownership: Backend Agent output -> Codex, Frontend Agent output -> Claude Code, QA last and independent.
- Do not edit `agents/*/SKILL.md`, `AGENTS.md`, `CLAUDE.md`, or `docs/rules/*` unless explicitly approved.

## Required JSON Fields
{required}

## Extra Expected Outputs
{extra}

## Task
Read the project brief and the agent skill below. Produce the required JSON output and any extra outputs in the exact output folder.

After writing outputs, run:

```bash
python3 execution/agency.py validate {contract.name} {project_id}
```

## Project
```markdown
{project_md}
```

## Client Context Pack
```markdown
{context_md}
```

## Agent Skill
```markdown
{skill_md}
```

## Pricing Matrix
```markdown
{pricing_md}
```

## Codex/Claude Operating Model
```markdown
{owner_doc}
```
"""


def cmd_list_agents(_args: argparse.Namespace) -> int:
    for name in sorted(AGENTS):
        contract = AGENTS[name]
        print(f"{name:22} owner={contract.owner} output={contract.output_json}")
    return 0


def cmd_prepare(args: argparse.Namespace) -> int:
    contract = contract_for(args.agent)
    project_path = project_dir(args.project_id)
    out_dir = output_dir(args.project_id, contract.name)
    out_dir.mkdir(parents=True, exist_ok=True)

    packet = prompt_packet(args.project_id, contract)
    packet_path = TMP_RUNS_DIR / args.project_id / f"{slug_timestamp()}_{contract.name}_prompt.md"
    write_text(packet_path, packet)

    state = {
        "schema_version": "agency-runner.v1",
        "project_id": args.project_id,
        "agent": contract.name,
        "status": "prepared",
        "recommended_operator": contract.owner,
        "prompt_packet": str(packet_path.relative_to(ROOT)),
        "output_json": str(output_json_path(args.project_id, contract).relative_to(ROOT)),
        "prepared_at": now_iso(),
    }
    write_json(out_dir / ".runner-state.json", state)
    log_event(args.project_id, {"event": "prepared", "agent": contract.name, "prompt_packet": state["prompt_packet"]})

    print(f"Prepared {contract.name} for {args.project_id}")
    print(f"Prompt packet: {packet_path.relative_to(ROOT)}")
    print(f"Output folder: {out_dir.relative_to(ROOT)}")
    print(f"Expected JSON: {output_json_path(args.project_id, contract).relative_to(ROOT)}")
    print(f"Recommended operator: {contract.owner}")
    print(f"Project file: {(project_path / 'PROJECT.md').relative_to(ROOT)}")
    return 0


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"Missing output JSON: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as exc:
        fail(f"Invalid JSON in {path.relative_to(ROOT)}: {exc}")


def load_json_or_empty(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    data = load_json(path)
    return data if isinstance(data, dict) else {}


def validate_contract(contract: AgentContract, data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        return ["Output JSON must be an object."], warnings

    for field in contract.required_fields:
        if field not in data:
            errors.append(f"Missing required field: {field}")

    if data.get("schema_version") != contract.schema_version:
        errors.append(f"schema_version must be {contract.schema_version!r}")

    if data.get("runtime_llm_used") is True:
        warnings.append("runtime_llm_used=true; verify CEO approval and client billing before delivery.")

    if contract.name == "eval-agent":
        if data.get("runtime_llm_needed") is True and not data.get("runtime_llm_cost_estimate_eur_month"):
            errors.append("runtime_llm_needed=true requires runtime_llm_cost_estimate_eur_month > 0")
        complexity = data.get("complexity_score")
        if isinstance(complexity, int) and complexity == 5 and data.get("recommendation") == "APPROVE":
            warnings.append("Complexity 5 with APPROVE requires explicit CEO review.")

    if contract.name == "bd-agent":
        allowed_docs = {"qualification_report", "proposal", "email_followup", "pitch", "objection_response"}
        if data.get("document_type") not in allowed_docs:
            errors.append(f"document_type must be one of: {', '.join(sorted(allowed_docs))}")
        qualification = data.get("lead_qualification")
        if not isinstance(qualification, dict):
            errors.append("lead_qualification must be an object.")
        else:
            signal_fields = (
                "budget_signal",
                "authority_signal",
                "need_signal",
                "timeline_signal",
                "decision_process_signal",
                "fit_signal",
            )
            for field in signal_fields:
                if qualification.get(field) not in {"green", "yellow", "red"}:
                    errors.append(f"lead_qualification.{field} must be green, yellow, or red.")
            if qualification.get("recommendation") not in {"MOVE_FORWARD", "NURTURE", "PARK"}:
                errors.append("lead_qualification.recommendation must be MOVE_FORWARD, NURTURE, or PARK.")
        if data.get("discount_applied") is True and data.get("ceo_approval_required") is not True:
            errors.append("discount_applied=true requires ceo_approval_required=true.")
        if data.get("ceo_approval_required") is not True:
            errors.append("BD outputs require ceo_approval_required=true before external use.")

    if contract.name == "marketing-agent":
        allowed_content_types = {
            "blog_seo",
            "linkedin_text",
            "linkedin_carousel",
            "linkedin_opinion",
            "case_study",
            "email_nurture",
            "email_single",
            "ad_copy",
        }
        allowed_pillars = {"educatie", "dovezi", "thought_leadership", "behind_scenes"}
        if data.get("content_type") not in allowed_content_types:
            errors.append(f"content_type must be one of: {', '.join(sorted(allowed_content_types))}")
        if data.get("pillar") not in allowed_pillars:
            errors.append(f"pillar must be one of: {', '.join(sorted(allowed_pillars))}")
        if data.get("approval_required") is not True:
            errors.append("Marketing outputs require approval_required=true before publishing.")
        if data.get("content_type") == "case_study" and data.get("anonymization_confirmed") is not True:
            errors.append("case_study content requires anonymization_confirmed=true.")
        if data.get("content_type") == "blog_seo":
            meta = str(data.get("meta_description", ""))
            if len(meta) > 155:
                warnings.append("meta_description is longer than 155 characters.")
            if not data.get("target_keyword"):
                errors.append("blog_seo content requires target_keyword.")

    if contract.name == "client-success-agent":
        score = data.get("health_score")
        if not isinstance(score, (int, float)) or not 1 <= score <= 10:
            errors.append("health_score must be a number from 1 to 10.")
        breakdown = data.get("health_score_breakdown")
        if not isinstance(breakdown, dict):
            errors.append("health_score_breakdown must be an object.")
        else:
            limits = {"technical": 4, "satisfaction": 3, "engagement": 2, "business_fit": 1}
            for field, maximum in limits.items():
                value = breakdown.get(field)
                if not isinstance(value, (int, float)) or value < 0 or value > maximum:
                    errors.append(f"health_score_breakdown.{field} must be between 0 and {maximum}.")
        if data.get("churn_risk") not in {"none", "low", "medium", "high", "critical"}:
            errors.append("churn_risk must be none, low, medium, high, or critical.")
        if not isinstance(data.get("churn_signals"), list):
            errors.append("churn_signals must be a list.")
        if (isinstance(score, (int, float)) and score <= 4) and data.get("escalation_required") is not True:
            errors.append("health_score <= 4 requires escalation_required=true.")
        if data.get("churn_risk") in {"high", "critical"} and data.get("escalation_required") is not True:
            errors.append("high/critical churn_risk requires escalation_required=true.")
        if data.get("escalation_required") is True and not data.get("escalation_reason"):
            errors.append("escalation_required=true requires escalation_reason.")

    if contract.name == "qa-agent":
        score = data.get("qa_score")
        status = data.get("status")
        coverage = data.get("sow_coverage", {})
        percentage = coverage.get("percentage") if isinstance(coverage, dict) else None
        if not isinstance(score, (int, float)) or score < 7:
            errors.append("qa_score must be >= 7 for delivery.")
        if status not in {"APPROVED", "APPROVED_WITH_NOTES"}:
            errors.append("status must be APPROVED or APPROVED_WITH_NOTES for delivery.")
        if percentage != 100:
            errors.append("sow_coverage.percentage must be 100 for delivery.")

    return errors, warnings


def cmd_validate(args: argparse.Namespace) -> int:
    contract = contract_for(args.agent)
    path = Path(args.file).resolve() if args.file else output_json_path(args.project_id, contract)
    data = load_json(path)
    errors, warnings = validate_contract(contract, data)

    report = {
        "schema_version": "agency-validation.v1",
        "project_id": args.project_id,
        "agent": contract.name,
        "validated_file": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
        "status": "PASS" if not errors else "FAIL",
        "errors": errors,
        "warnings": warnings,
        "validated_at": now_iso(),
    }
    report_path = output_dir(args.project_id, contract.name) / "validation-report.json"
    write_json(report_path, report)
    log_event(args.project_id, {"event": "validated", "agent": contract.name, "status": report["status"]})

    print(f"{report['status']}: {contract.name} output validation")
    if errors:
        print("Errors:")
        for error in errors:
            print(f"- {error}")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    print(f"Report: {report_path.relative_to(ROOT)}")
    return 0 if not errors else 1


def status_for(project_id: str, contract: AgentContract) -> tuple[str, str]:
    json_path = output_json_path(project_id, contract)
    report_path = output_dir(project_id, contract.name) / "validation-report.json"
    if report_path.is_file():
        try:
            status = json.loads(report_path.read_text(encoding="utf-8")).get("status", "UNKNOWN")
            return str(status), str(json_path.relative_to(ROOT))
        except json.JSONDecodeError:
            return "BAD_REPORT", str(report_path.relative_to(ROOT))
    if json_path.is_file():
        return "OUTPUT_READY", str(json_path.relative_to(ROOT))
    state_path = output_dir(project_id, contract.name) / ".runner-state.json"
    if state_path.is_file():
        return "PREPARED", str(json_path.relative_to(ROOT))
    return "PENDING", str(json_path.relative_to(ROOT))


def document_type_for(path: Path) -> str:
    name = path.name.lower()
    if name == "sow.md":
        return "sow"
    if name == "proposal.md":
        return "proposal"
    if name == "sop.md":
        return "sop"
    if name == "user-guide.md":
        return "user_guide"
    if name == "qa-evidence.md":
        return "qa_report"
    if name == "handover.md":
        return "handover"
    if "workflow" in name:
        return "workflow"
    return "report"


def collect_project_documents(project_id: str) -> tuple[dict[str, Any], ...]:
    root = project_dir(project_id)
    documents: list[dict[str, Any]] = []
    for folder in (root / "outputs", root / "delivery", root / "inputs"):
        if not folder.is_dir():
            continue
        for path in sorted(folder.rglob("*.md")):
            relative = path.relative_to(ROOT)
            source_agent = ""
            parts = path.relative_to(root).parts
            if len(parts) >= 3 and parts[0] == "outputs":
                source_agent = parts[1]
            documents.append(
                {
                    "local_document_key": f"{project_id}:{relative}",
                    "type": document_type_for(path),
                    "title": path.stem.replace("-", " ").title(),
                    "content": path.read_text(encoding="utf-8"),
                    "url": str(relative),
                    "source_agent": source_agent or None,
                }
            )
    return tuple(documents)


def build_supabase_sync_plan(project_id: str) -> SupabaseSyncPlan:
    project_path = project_dir(project_id)
    project_md = read_text(project_path / "PROJECT.md")
    active_agents = ordered_active_agents(project_md)
    project_status = first_match(r"^- \*\*status:\*\*\s+(.+)$", project_md, "draft")

    eval_data = load_json_or_empty(output_json_path(project_id, AGENTS["eval-agent"]))
    project_payload = {
        "local_project_id": project_id,
        "name": extract_project_title(project_md, project_id),
        "status": normalize_project_status(project_status),
        "brief": extract_brief(project_md),
        "industry": extract_yaml_value(project_md, "industrie"),
        "deadline": first_match(r"^- \*\*deadline:\*\*\s+(.+)$", project_md) or None,
        "estimated_hours": eval_data.get("estimated_hours"),
        "estimated_cost_eur": eval_data.get("estimated_cost_eur"),
        "agents_activated": active_agents,
    }

    agent_runs: list[dict[str, Any]] = []
    for agent_name in active_agents:
        contract = contract_for(agent_name)
        status, target = status_for(project_id, contract)
        json_path = output_json_path(project_id, contract)
        output_data = load_json_or_empty(json_path)
        state = load_json_or_empty(output_dir(project_id, agent_name) / ".runner-state.json")
        report = load_json_or_empty(output_dir(project_id, agent_name) / "validation-report.json")
        agent_runs.append(
            {
                "local_run_key": f"{project_id}:{agent_name}",
                "agent_name": agent_name,
                "operator": operator_slug(contract.owner),
                "input": {
                    "local_project_id": project_id,
                    "prompt_packet_path": state.get("prompt_packet"),
                    "status_target": target,
                },
                "output": output_data,
                "output_path": str(json_path.relative_to(ROOT)),
                "prompt_packet_path": state.get("prompt_packet"),
                "status": normalize_agent_run_status(status),
                "qa_score": output_data.get("qa_score") if isinstance(output_data.get("qa_score"), (int, float)) else None,
                "error_message": "; ".join(report.get("errors", [])) if report.get("errors") else None,
                "prepared_at": state.get("prepared_at"),
                "validated_at": report.get("validated_at"),
            }
        )

    return SupabaseSyncPlan(
        project=project_payload,
        agent_runs=tuple(agent_runs),
        documents=collect_project_documents(project_id),
    )


def operator_slug(owner: str) -> str:
    lower = owner.lower()
    if "codex" in lower and "claude" not in lower:
        return "codex"
    if "claude" in lower and "codex" not in lower:
        return "claude-code"
    if "independent qa" in lower:
        return "qa-operator"
    return "other"


class SupabaseRestClient:
    def __init__(self, url: str, key: str, schema: str = DEFAULT_SUPABASE_SCHEMA) -> None:
        self.url = url.rstrip("/")
        self.key = key
        self.schema = schema.strip() or DEFAULT_SUPABASE_SCHEMA

    def upsert(self, table: str, payload: dict[str, Any] | list[dict[str, Any]], on_conflict: str) -> Any:
        query = parse.urlencode({"on_conflict": on_conflict})
        endpoint = f"{self.url}/rest/v1/{table}?{query}"
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = request.Request(
            endpoint,
            data=body,
            method="POST",
            headers={
                "apikey": self.key,
                "Authorization": f"Bearer {self.key}",
                "Content-Type": "application/json",
                "Accept-Profile": self.schema,
                "Content-Profile": self.schema,
                "Prefer": "resolution=merge-duplicates,return=representation",
            },
        )
        try:
            with request.urlopen(req, timeout=30) as response:
                raw = response.read().decode("utf-8")
        except error.HTTPError as exc:
            message = exc.read().decode("utf-8", errors="replace")
            fail(
                f"Supabase {self.schema}.{table} upsert failed: HTTP {exc.code}: {message}\n"
                f"Check that schema '{self.schema}' is listed in Supabase Data API exposed schemas "
                "and that the migration grants service_role access."
            )
        return json.loads(raw) if raw else None


def env_supabase_client(schema: str) -> SupabaseRestClient:
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not url or not key:
        fail("SUPABASE_URL and SUPABASE_SERVICE_KEY are required for --apply.")
    return SupabaseRestClient(url, key, schema=schema)


def cmd_status(args: argparse.Namespace) -> int:
    project_path = project_dir(args.project_id)
    project_md = read_text(project_path / "PROJECT.md")
    active = parse_active_agents(project_md)
    active_set = set(active)
    print(f"Project: {args.project_id}")
    print(f"Active agents: {', '.join(active) if active else 'none marked active'}")
    print("")
    print(f"{'Agent':22} {'Active':7} {'Status':14} Output")
    print("-" * 82)
    for name in sorted(AGENTS):
        contract = AGENTS[name]
        status, target = status_for(args.project_id, contract)
        marker = "yes" if name in active_set else "no"
        print(f"{name:22} {marker:7} {status:14} {target}")
    return 0


def ordered_active_agents(project_md: str) -> list[str]:
    active = parse_active_agents(project_md)
    active_set = set(active)
    ordered = [name for name in PIPELINE_ORDER if name in active_set]
    extras = [name for name in active if name not in PIPELINE_ORDER]
    return ordered + extras


def next_action(project_id: str) -> NextAction:
    project_path = project_dir(project_id)
    project_md = read_text(project_path / "PROJECT.md")
    active = ordered_active_agents(project_md)

    if not active:
        return NextAction(
            kind="no_active_agents",
            agent=None,
            status="BLOCKED",
            message="No active agents are checked in PROJECT.md.",
        )

    qa_active = "qa-agent" in active
    qa_index = active.index("qa-agent") if qa_active else len(active)
    agents_before_qa = active[:qa_index]
    blocked_before_qa: list[tuple[str, str]] = []

    for agent_name in active:
        contract = contract_for(agent_name)
        status, target = status_for(project_id, contract)

        if agent_name == "qa-agent" and blocked_before_qa:
            waiting_on = ", ".join(f"{name}={state}" for name, state in blocked_before_qa)
            return NextAction(
                kind="qa_blocked",
                agent="qa-agent",
                status="BLOCKED",
                message=f"QA is blocked until earlier active agents pass validation: {waiting_on}.",
            )

        if status == "PASS":
            continue

        if status == "OUTPUT_READY":
            return NextAction(
                kind="validate_output",
                agent=agent_name,
                status=status,
                message=f"{agent_name} has output ready and needs validation: {target}",
                command=f"python3 execution/agency.py validate {agent_name} {project_id}",
            )

        if status == "PREPARED":
            return NextAction(
                kind="operator_work",
                agent=agent_name,
                status=status,
                message=f"{agent_name} is prepared. Operator should complete the expected output: {target}",
            )

        if status in {"FAIL", "BAD_REPORT"}:
            return NextAction(
                kind="fix_validation",
                agent=agent_name,
                status=status,
                message=f"{agent_name} validation is {status}. Fix the output or report before continuing.",
                command=f"python3 execution/agency.py validate {agent_name} {project_id}",
            )

        if agent_name in agents_before_qa:
            blocked_before_qa.append((agent_name, status))

        return NextAction(
            kind="prepare_agent",
            agent=agent_name,
            status=status,
            message=f"{agent_name} is the next active agent to prepare.",
            command=f"python3 execution/agency.py prepare {agent_name} {project_id}",
        )

    if not qa_active:
        return NextAction(
            kind="qa_not_active",
            agent="qa-agent",
            status="BLOCKED",
            message="All active non-QA agents are complete, but QA Agent is not active. Delivery requires QA validation before client handoff.",
            command=f"Edit projects/{project_id}/PROJECT.md and activate qa-agent before delivery.",
        )

    return NextAction(
        kind="ready",
        agent=None,
        status="READY",
        message="All active agents, including QA, have passed validation. Project is ready for delivery packaging.",
    )


def cmd_next(args: argparse.Namespace) -> int:
    action = next_action(args.project_id)
    print(f"Project: {args.project_id}")
    print(f"Next action: {action.kind}")
    print(f"Status: {action.status}")
    if action.agent:
        print(f"Agent: {action.agent}")
    print(action.message)
    if action.command:
        print(f"Command: {action.command}")
    return 0 if action.status != "BLOCKED" else 2


def cmd_sync_supabase(args: argparse.Namespace) -> int:
    plan = build_supabase_sync_plan(args.project_id)
    print(f"Project: {args.project_id}")
    print(f"Mode: {'apply' if args.apply else 'dry-run'}")
    print(f"Supabase schema: {args.schema}")
    print(f"Project row: {plan.project['local_project_id']} status={plan.project['status']}")
    print(f"Agent runs: {len(plan.agent_runs)}")
    print(f"Documents: {len(plan.documents)}")

    if args.json:
        print(
            json.dumps(
                {
                    "project": plan.project,
                    "agent_runs": list(plan.agent_runs),
                    "documents": list(plan.documents),
                },
                indent=2,
                ensure_ascii=False,
            )
        )

    if not args.apply:
        print("Dry run only. Use --apply with SUPABASE_URL and SUPABASE_SERVICE_KEY to write live.")
        return 0

    client = env_supabase_client(args.schema)
    project_rows = client.upsert("projects", plan.project, "local_project_id")
    if not project_rows:
        fail("Supabase did not return the project row.")
    supabase_project_id = project_rows[0]["id"]

    runs = [dict(row, project_id=supabase_project_id) for row in plan.agent_runs]
    docs = [dict(row, project_id=supabase_project_id) for row in plan.documents]
    if runs:
        client.upsert("agent_runs", runs, "local_run_key")
    if docs:
        client.upsert("documents", docs, "local_document_key")

    print("Supabase sync completed.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agency",
        description="Zero-API execution runner for AI Agency projects.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    list_agents = sub.add_parser("list-agents", help="List known agent contracts.")
    list_agents.set_defaults(func=cmd_list_agents)

    prepare = sub.add_parser("prepare", help="Prepare a prompt packet for an agent run.")
    prepare.add_argument("agent", choices=sorted(AGENTS))
    prepare.add_argument("project_id")
    prepare.set_defaults(func=cmd_prepare)

    run = sub.add_parser("run", help="Alias for prepare; does not call an LLM.")
    run.add_argument("agent", choices=sorted(AGENTS))
    run.add_argument("project_id")
    run.set_defaults(func=cmd_prepare)

    validate = sub.add_parser("validate", help="Validate an agent output JSON file.")
    validate.add_argument("agent", choices=sorted(AGENTS))
    validate.add_argument("project_id")
    validate.add_argument("--file", help="Optional explicit JSON file path.")
    validate.set_defaults(func=cmd_validate)

    status = sub.add_parser("status", help="Show project agent output status.")
    status.add_argument("project_id")
    status.set_defaults(func=cmd_status)

    next_step = sub.add_parser("next", help="Show the next safe action for a project.")
    next_step.add_argument("project_id")
    next_step.set_defaults(func=cmd_next)

    sync = sub.add_parser("sync-supabase", help="Dry-run or apply local project state to Supabase.")
    sync.add_argument("project_id")
    sync.add_argument("--apply", action="store_true", help="Write to Supabase using service-role env vars.")
    sync.add_argument("--json", action="store_true", help="Print the full sync payload.")
    sync.add_argument(
        "--schema",
        default=os.environ.get("SUPABASE_SCHEMA", DEFAULT_SUPABASE_SCHEMA),
        help=f"Supabase PostgREST schema/profile to use (default: {DEFAULT_SUPABASE_SCHEMA}).",
    )
    sync.set_defaults(func=cmd_sync_supabase)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
