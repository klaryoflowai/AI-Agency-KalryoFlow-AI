#!/usr/bin/env python3
import json
import os
import sys


def respond(decision: str, message: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {"permissionDecision": decision},
        "systemMessage": message,
    }))


try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_input = payload.get("tool_input", {})
path = tool_input.get("file_path") or tool_input.get("path") or ""
if not path:
    sys.exit(0)

path = os.path.abspath(path)
base = os.path.basename(path)
parts = set(path.split(os.sep))

allowed_secret_templates = {
    ".env.example",
}

if base.startswith(".env") and base not in allowed_secret_templates:
    if path.endswith(os.path.join("projects", "template", ".env.project")):
        sys.exit(0)
    respond("deny", "Blocked edit to environment/secret file. Use .env.example or a template instead.")
    sys.exit(0)

if base in {"credentials.json", "token.json", "secrets.yaml", "secrets.yml"}:
    respond("deny", f"Blocked edit to sensitive secret file: {base}.")
    sys.exit(0)

if base in {"AGENTS.md", "CLAUDE.md"} or ("agents" in parts and base == "SKILL.md") or ("docs" in parts and "rules" in parts):
    respond("ask", "This file controls project behavior. Confirm the change is intentional and approved.")
    sys.exit(0)

