from __future__ import annotations

from execution import validate_n8n_workflows as validator


def test_n8n_workflows_pass_static_validation() -> None:
    files = validator.workflow_files()

    assert files
    for path in files:
        result = validator.check_workflow(path)
        assert result.errors == []


def test_n8n_validator_rejects_execute_command(tmp_path) -> None:
    workflow = tmp_path / "bad.json"
    workflow.write_text(
        """
        {
          "name": "bad",
          "nodes": [
            {"name": "Run Shell", "type": "n8n-nodes-base.executeCommand"}
          ],
          "connections": {}
        }
        """,
        encoding="utf-8",
    )

    result = validator.check_workflow(workflow)

    assert "bad.json: forbidden n8n Cloud node type: n8n-nodes-base.executeCommand" in result.errors


def test_n8n_validator_rejects_credentials(tmp_path) -> None:
    workflow = tmp_path / "bad-creds.json"
    workflow.write_text(
        """
        {
          "name": "bad-creds",
          "nodes": [
            {"name": "Webhook", "type": "n8n-nodes-base.webhook"},
            {"name": "Respond", "type": "n8n-nodes-base.respondToWebhook"}
          ],
          "connections": {"Webhook": {"main": [[{"node": "Respond", "type": "main", "index": 0}]]}},
          "credentials": {"httpHeaderAuth": {"id": "1", "name": "secret"}}
        }
        """,
        encoding="utf-8",
    )

    result = validator.check_workflow(workflow)

    assert "bad-creds.json: exported workflow must not contain credentials" in result.errors
