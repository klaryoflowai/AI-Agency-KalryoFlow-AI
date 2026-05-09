from __future__ import annotations

from execution import agency


def test_sync_plan_builds_project_agent_runs_and_documents() -> None:
    plan = agency.build_supabase_sync_plan("2026-05_Restaurant_Demo")

    assert plan.project["local_project_id"] == "2026-05_Restaurant_Demo"
    assert plan.project["status"] == "pilot_ready"
    assert plan.project["estimated_hours"] == 48
    assert plan.project["estimated_cost_eur"] == 3360
    assert "qa-agent" == plan.project["agents_activated"][-1]
    assert len(plan.agent_runs) == 8
    assert all(run["status"] == "validated" for run in plan.agent_runs)
    assert any(doc["type"] == "handover" for doc in plan.documents)
    assert any(doc["type"] == "qa_report" for doc in plan.documents)


def test_agent_status_mapping_for_supabase() -> None:
    assert agency.normalize_agent_run_status("PASS") == "validated"
    assert agency.normalize_agent_run_status("OUTPUT_READY") == "done"
    assert agency.normalize_agent_run_status("PREPARED") == "prepared"
    assert agency.normalize_agent_run_status("PENDING") == "pending"
    assert agency.normalize_agent_run_status("FAIL") == "error"


def test_project_status_mapping_for_supabase() -> None:
    assert agency.normalize_project_status("pilot-ready") == "pilot_ready"
    assert agency.normalize_project_status("active") == "active"
    assert agency.normalize_project_status("unknown") == "draft"
