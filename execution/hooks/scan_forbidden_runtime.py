#!/usr/bin/env python3
import json
import os
import re
import sys


try:
    payload = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_input = payload.get("tool_input", {})
path = tool_input.get("file_path") or tool_input.get("path") or ""
if not path or not os.path.isfile(path):
    sys.exit(0)

base = os.path.basename(path)
if base == ".env.example" or path.endswith(os.path.join("projects", "template", ".env.project")):
    sys.exit(0)

try:
    with open(path, "r", encoding="utf-8", errors="ignore") as handle:
        content = handle.read()
except Exception:
    sys.exit(0)

patterns = [
    r"ANTHROPIC_API_KEY\s*=",
    r"OPENAI_API_KEY\s*=",
    r"from\s+anthropic\s+import",
    r"import\s+anthropic",
    r"from\s+openai\s+import",
    r"import\s+openai",
    r"@anthropic-ai/sdk",
]

if any(re.search(pattern, content) for pattern in patterns):
    print(json.dumps({
        "systemMessage": (
            "Potential paid LLM runtime was added. MVP policy requires explicit CEO approval "
            "and client-side billing before LLM API keys or SDKs are introduced."
        )
    }))

