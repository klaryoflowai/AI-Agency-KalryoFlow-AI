from __future__ import annotations

import json
from pathlib import Path

from execution import agency


def write_project(root: Path, project_id: str, active_lines: list[str]) -> None:
    project_dir = root / "projects" / project_id
    project_dir.mkdir(parents=True)
    project_dir.joinpath("PROJECT.md").write_text(
        "# PROJECT: Test\n\n## Agenți Activați\n" + "\n".join(active_lines) + "\n",
        encoding="utf-8",
    )


def patch_runner_paths(monkeypatch, root: Path) -> None:
    monkeypatch.setattr(agency, "ROOT", root)
    monkeypatch.setattr(agency, "PROJECTS_DIR", root / "projects")
    monkeypatch.setattr(agency, "TMP_RUNS_DIR", root / ".tmp" / "agency")


def test_next_action_prepares_first_active_agent(monkeypatch, tmp_path: Path) -> None:
    patch_runner_paths(monkeypatch, tmp_path)
    write_project(
        tmp_path,
        "demo",
        [
            "- [x] eval-agent           -> `outputs/eval-agent/`",
            "- [x] qa-agent             -> `outputs/qa-agent/`",
        ],
    )

    action = agency.next_action("demo")

    assert action.kind == "prepare_agent"
    assert action.agent == "eval-agent"
    assert action.command == "python3 execution/agency.py prepare eval-agent demo"


def test_next_action_validates_ready_output(monkeypatch, tmp_path: Path) -> None:
    patch_runner_paths(monkeypatch, tmp_path)
    write_project(
        tmp_path,
        "demo",
        [
            "- [x] eval-agent           -> `outputs/eval-agent/`",
            "- [x] qa-agent             -> `outputs/qa-agent/`",
        ],
    )
    output_dir = tmp_path / "projects" / "demo" / "outputs" / "eval-agent"
    output_dir.mkdir(parents=True)
    output_dir.joinpath("evaluation.json").write_text("{}", encoding="utf-8")

    action = agency.next_action("demo")

    assert action.kind == "validate_output"
    assert action.agent == "eval-agent"
    assert action.command == "python3 execution/agency.py validate eval-agent demo"


def test_next_action_blocks_delivery_without_qa(monkeypatch, tmp_path: Path) -> None:
    patch_runner_paths(monkeypatch, tmp_path)
    write_project(
        tmp_path,
        "demo",
        ["- [x] eval-agent           -> `outputs/eval-agent/`"],
    )
    output_dir = tmp_path / "projects" / "demo" / "outputs" / "eval-agent"
    output_dir.mkdir(parents=True)
    output_dir.joinpath("validation-report.json").write_text(
        json.dumps({"status": "PASS"}),
        encoding="utf-8",
    )

    action = agency.next_action("demo")

    assert action.kind == "qa_not_active"
    assert action.status == "BLOCKED"
    assert action.agent == "qa-agent"
