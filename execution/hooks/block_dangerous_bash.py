#!/usr/bin/env python3
import json
import re
import sys


def deny(message: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {"permissionDecision": "deny"},
        "systemMessage": message,
    }))


def ask(message: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {"permissionDecision": "ask"},
        "systemMessage": message,
    }))


try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)

command = payload.get("tool_input", {}).get("command", "")
normalized = " ".join(command.split())

deny_patterns = [
    (r"\brm\s+-rf\s+/(?:\s|$)", "Blocked destructive rm -rf outside the workspace."),
    (r"\bgit\s+push\b", "Blocked git push. Remote pushes require explicit user approval."),
    (r"\bANTHROPIC_API_KEY\s*=", "Blocked adding Anthropic runtime API key in MVP."),
    (r"\bOPENAI_API_KEY\s*=", "Blocked adding OpenAI runtime API key in MVP."),
    (r"\bpip(?:3)?\s+install\b.*\banthropic\b", "Blocked Anthropic SDK install in MVP."),
    (r"\b(?:npm|pnpm|yarn|bun)\s+.*\b@anthropic-ai/sdk\b", "Blocked Anthropic SDK install in MVP."),
    (r"\bpip(?:3)?\s+install\b.*\bopenai\b", "Blocked OpenAI SDK install in MVP."),
]

for pattern, message in deny_patterns:
    if re.search(pattern, normalized):
        deny(message)
        sys.exit(0)

if re.search(r"\bgit\s+commit\b", normalized):
    ask("Creating commits is allowed only when the user explicitly asks for a commit.")
    sys.exit(0)

