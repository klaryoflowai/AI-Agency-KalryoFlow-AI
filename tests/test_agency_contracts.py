from __future__ import annotations

import copy

from execution import agency


def validate(agent_name: str, data: dict) -> tuple[list[str], list[str]]:
    return agency.validate_contract(agency.AGENTS[agent_name], data)


VALID_BD_V2 = {
    "schema_version": "bd-agent.v2",
    "document_type": "proposal",
    "lead_qualification": {
        "budget_signal": "green",
        "authority_signal": "green",
        "need_signal": "green",
        "timeline_signal": "yellow",
        "decision_process_signal": "green",
        "fit_signal": "green",
        "recommendation": "MOVE_FORWARD",
    },
    "subject": "Propunere",
    "content": "Draft",
    "cta": "Aprobare CEO",
    "pricing_source": "eval-agent output",
    "discount_applied": False,
    "ceo_approval_required": True,
    "next_followup_days": 3,
    "notes": "ok",
}

VALID_MARKETING_V2 = {
    "schema_version": "marketing-agent.v2",
    "content_type": "case_study",
    "pillar": "dovezi",
    "title": "Studiu de caz",
    "meta_description": "Rezultate validate.",
    "target_keyword": "automatizare procese IMM Romania",
    "target_audience": "IMM operational",
    "content": "Draft",
    "cta": "Programeaza evaluare",
    "distribution_channels": ["LinkedIn"],
    "estimated_reach": "orientativ",
    "metrics_to_track": ["engagement_rate"],
    "data_sources_used": ["project-test"],
    "anonymization_confirmed": True,
    "approval_required": True,
    "notes": "ok",
}

VALID_CLIENT_SUCCESS_V2 = {
    "schema_version": "client-success-agent.v2",
    "communication_type": "report_30d",
    "client_id": "client-test",
    "project_id": "project-test",
    "health_score": 8,
    "health_score_breakdown": {
        "technical": 4,
        "satisfaction": 2,
        "engagement": 1,
        "business_fit": 1,
    },
    "churn_risk": "low",
    "churn_signals": [],
    "content": "Draft",
    "upsell_opportunities": [],
    "escalation_required": False,
    "escalation_reason": "",
    "action_required_from_ceo": "aproba mesajul",
    "next_touchpoint_days": 60,
    "notes": "ok",
}


def test_business_agent_v2_contracts_accept_valid_outputs() -> None:
    for agent_name, payload in (
        ("bd-agent", VALID_BD_V2),
        ("marketing-agent", VALID_MARKETING_V2),
        ("client-success-agent", VALID_CLIENT_SUCCESS_V2),
    ):
        errors, warnings = validate(agent_name, payload)
        assert errors == []
        assert warnings == []


def test_bd_agent_rejects_missing_ceo_approval() -> None:
    payload = copy.deepcopy(VALID_BD_V2)
    payload["ceo_approval_required"] = False

    errors, _warnings = validate("bd-agent", payload)

    assert "BD outputs require ceo_approval_required=true before external use." in errors


def test_marketing_case_study_requires_anonymization() -> None:
    payload = copy.deepcopy(VALID_MARKETING_V2)
    payload["anonymization_confirmed"] = False

    errors, _warnings = validate("marketing-agent", payload)

    assert "case_study content requires anonymization_confirmed=true." in errors


def test_client_success_low_health_requires_escalation() -> None:
    payload = copy.deepcopy(VALID_CLIENT_SUCCESS_V2)
    payload["health_score"] = 4
    payload["health_score_breakdown"] = {
        "technical": 1,
        "satisfaction": 1,
        "engagement": 1,
        "business_fit": 1,
    }
    payload["churn_risk"] = "high"

    errors, _warnings = validate("client-success-agent", payload)

    assert "health_score <= 4 requires escalation_required=true." in errors
    assert "high/critical churn_risk requires escalation_required=true." in errors


def test_qa_contract_enforces_delivery_gate() -> None:
    payload = {
        "schema_version": "qa-agent.v1",
        "qa_score": 6.5,
        "status": "NEEDS_FIXES",
        "backend_tests": [],
        "frontend_tests": [],
        "e2e_tests": [],
        "sow_coverage": {"percentage": 80},
        "bugs_found": [],
        "delivery_checklist": [],
        "user_guide": "",
        "handover_notes": "",
    }

    errors, _warnings = validate("qa-agent", payload)

    assert "qa_score must be >= 7 for delivery." in errors
    assert "status must be APPROVED or APPROVED_WITH_NOTES for delivery." in errors
    assert "sow_coverage.percentage must be 100 for delivery." in errors
