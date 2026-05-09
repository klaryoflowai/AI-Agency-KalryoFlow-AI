from __future__ import annotations

from pathlib import Path

from execution import agency


ROOT = Path(__file__).resolve().parents[1]


def test_workflow_to_skill_factory_artifacts_exist() -> None:
    required = [
        "docs/competencies/workflow-to-skill-factory.md",
        "resources/templates/client-context-pack-template.md",
        "resources/templates/workflow-capture-template.md",
        "resources/templates/qa-evidence-checklist.md",
        "resources/templates/skill-candidate-template.md",
        "resources/templates/operator-task-brief.md",
        "projects/template/CONTEXT.md",
    ]

    for relative_path in required:
        assert ROOT.joinpath(relative_path).is_file()


def test_prompt_packet_includes_client_context_pack() -> None:
    packet = agency.prompt_packet("2026-05_Restaurant_Demo", agency.AGENTS["eval-agent"])

    assert "## Client Context Pack" in packet
    assert "Restaurant Demo" in packet
    assert "MVP zero-API LLM" in packet


def test_factory_doc_keeps_skill_creation_behind_approval() -> None:
    doc = ROOT.joinpath("docs/competencies/workflow-to-skill-factory.md").read_text(encoding="utf-8")

    assert "Nu cream `SKILL.md` din teorie" in doc
    assert "CEO a aprobat transformarea in `SKILL.md`" in doc
