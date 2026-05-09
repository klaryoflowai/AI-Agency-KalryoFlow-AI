#!/usr/bin/env python3
"""Static validator for n8n workflow JSON files.

The checks are intentionally conservative for n8n Cloud:
- no Execute Command nodes;
- no credentials or obvious secrets in exported JSON;
- every workflow must expose a Webhook and a Respond to Webhook node;
- orchestrator workflow must document the supported project events.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS_DIR = ROOT / "infrastructure" / "n8n" / "workflows"

FORBIDDEN_NODE_TYPES = {
    "n8n-nodes-base.executeCommand",
}

FORBIDDEN_PATTERNS = {
    "Supabase service key": r"SUPABASE_SERVICE_KEY|SUPABASE_SERVICE_ROLE_KEY|service_role",
    "OpenAI key": r"OPENAI_API_KEY|sk-[A-Za-z0-9_-]{20,}",
    "Anthropic key": r"ANTHROPIC_API_KEY|sk-ant-[A-Za-z0-9_-]{20,}",
    "Authorization header": r"authorization\s*[:=]",
    "Bearer token": r"bearer\s+[A-Za-z0-9._-]{20,}",
}

REQUIRED_EVENTS = {
    "project.created",
    "agent.prepared",
    "agent.output_submitted",
    "agent.validated",
    "qa.approved",
    "delivery.ready",
}


@dataclass
class WorkflowCheck:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def workflow_files() -> list[Path]:
    return sorted(WORKFLOWS_DIR.glob("*.json"))


def load_workflow(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("workflow JSON must be an object")
    return data


def check_workflow(path: Path) -> WorkflowCheck:
    errors: list[str] = []
    warnings: list[str] = []
    raw = path.read_text(encoding="utf-8")

    for label, pattern in FORBIDDEN_PATTERNS.items():
        if re.search(pattern, raw, re.IGNORECASE):
            errors.append(f"{path.name}: forbidden secret pattern found: {label}")

    try:
        data = load_workflow(path)
    except (json.JSONDecodeError, ValueError) as exc:
        return WorkflowCheck([f"{path.name}: invalid JSON: {exc}"], warnings)

    nodes = data.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        errors.append(f"{path.name}: workflow must contain nodes")
        return WorkflowCheck(errors, warnings)

    node_names = {str(node.get("name", "")) for node in nodes if isinstance(node, dict)}
    node_types = {str(node.get("type", "")) for node in nodes if isinstance(node, dict)}

    forbidden = sorted(node_types.intersection(FORBIDDEN_NODE_TYPES))
    for node_type in forbidden:
        errors.append(f"{path.name}: forbidden n8n Cloud node type: {node_type}")

    if "n8n-nodes-base.webhook" not in node_types:
        errors.append(f"{path.name}: missing Webhook node")
    if "n8n-nodes-base.respondToWebhook" not in node_types:
        errors.append(f"{path.name}: missing Respond to Webhook node")
    if "credentials" in raw.lower():
        errors.append(f"{path.name}: exported workflow must not contain credentials")

    connections = data.get("connections")
    if not isinstance(connections, dict) or not connections:
        errors.append(f"{path.name}: workflow must contain node connections")
    else:
        for source_name in connections:
            if source_name not in node_names:
                errors.append(f"{path.name}: connection source does not match a node: {source_name}")

    missing_events = sorted(event for event in REQUIRED_EVENTS if event not in raw)
    if missing_events:
        errors.append(f"{path.name}: missing supported events: {', '.join(missing_events)}")

    if data.get("active") is True:
        warnings.append(f"{path.name}: workflow is marked active in exported JSON")

    return WorkflowCheck(errors, warnings)


def main() -> int:
    files = workflow_files()
    if not files:
        print(f"FAIL: no n8n workflows found in {WORKFLOWS_DIR.relative_to(ROOT)}")
        return 1

    all_errors: list[str] = []
    all_warnings: list[str] = []
    for path in files:
        result = check_workflow(path)
        all_errors.extend(result.errors)
        all_warnings.extend(result.warnings)

    print("n8n workflow validation")
    print(f"Files: {', '.join(str(path.relative_to(ROOT)) for path in files)}")
    print(f"Status: {'PASS' if not all_errors else 'FAIL'}")

    if all_errors:
        print("\nErrors:")
        for error in all_errors:
            print(f"- {error}")

    if all_warnings:
        print("\nWarnings:")
        for warning in all_warnings:
            print(f"- {warning}")

    return 0 if not all_errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
