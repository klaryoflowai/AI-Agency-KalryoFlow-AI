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


def test_supabase_rest_client_targets_custom_schema(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class FakeResponse:
        def __enter__(self) -> "FakeResponse":
            return self

        def __exit__(self, *args: object) -> None:
            return None

        def read(self) -> bytes:
            return b'[{"id":"project-id"}]'

    def fake_urlopen(req, timeout: int) -> FakeResponse:
        captured["url"] = req.full_url
        captured["headers"] = dict(req.header_items())
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setattr(agency.request, "urlopen", fake_urlopen)

    result = agency.SupabaseRestClient(
        "https://demo.supabase.co",
        "service-key",
        schema="agency",
    ).upsert("projects", {"local_project_id": "demo"}, "local_project_id")

    headers = {key.lower(): value for key, value in captured["headers"].items()}
    assert result == [{"id": "project-id"}]
    assert captured["url"] == "https://demo.supabase.co/rest/v1/projects?on_conflict=local_project_id"
    assert headers["accept-profile"] == "agency"
    assert headers["content-profile"] == "agency"
    assert headers["prefer"] == "resolution=merge-duplicates,return=representation"
