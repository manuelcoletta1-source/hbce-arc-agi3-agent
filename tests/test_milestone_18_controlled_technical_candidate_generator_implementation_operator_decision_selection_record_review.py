from __future__ import annotations

import json

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_selection_record import (
    build_candidate_generator_implementation_operator_decision_selection_record,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_selection_record_review import (
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_candidate_generator_implementation_operator_decision_selection_record_review,
    build_operator_decision_selection_record_review_items,
    write_artifacts,
)


def test_task_23_ready_valid_passed() -> None:
    data = build_candidate_generator_implementation_operator_decision_selection_record_review()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["operator_decision_selection_record_review_ready"] is True
    assert data["operator_decision_selection_record_review_passed"] is True
    assert data["operator_decision_selection_record_confirmed"] is True
    assert data["operator_decision_value_gate_required"] is True
    assert data["operator_decision_value_gate_allowed_next"] is True
    assert data["operator_decision_selection_required"] is True
    assert data["operator_decision_selection_received"] is False
    assert data["operator_decision_selection_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION"
    assert data["operator_decision_required"] is True
    assert data["operator_decision_received"] is False
    assert data["operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert data["operator_decision_value_selected"] is False
    assert data["explicit_operator_authorization_received"] is False
    assert data["implementation_authorization_candidate_confirmed"] is True
    assert data["implementation_code_authorized"] is False
    assert data["implementation_allowed_now"] is False
    assert data["blocking_issue_count"] == 0


def test_task_23_preserves_task_22_baseline_and_normalizes_boundary_drift() -> None:
    source = build_candidate_generator_implementation_operator_decision_selection_record()
    data = build_candidate_generator_implementation_operator_decision_selection_record_review()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "6d05b5a"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "A3399FF31AA613A3"
    assert data["source_operator_decision_selection_record_signature"] == source["signature"] == PREVIOUS_SIGNATURE
    assert data["source_operator_decision_selection_record_validation"].endswith("_VALID")
    assert source["boundary_controls"]["operator_decision_selection_value"] is False
    assert data["source_boundary_operator_decision_selection_value"] is False
    assert data["source_boundary_operator_decision_selection_value_drift_detected"] is True
    assert data["normalized_operator_decision_selection_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION"


def test_task_23_review_items_require_value_gate_no_code() -> None:
    source = build_candidate_generator_implementation_operator_decision_selection_record()
    items = build_operator_decision_selection_record_review_items(source)

    assert len(items) == 6
    assert all(
        item["review_decision"] == "CONFIRMED_OPERATOR_DECISION_SELECTION_RECORD_PENDING_VALUE_GATE"
        for item in items
    )
    assert all(item["operator_decision_value_gate_required"] is True for item in items)
    assert all(item["operator_decision_value_gate_allowed_next"] is True for item in items)
    assert all(item["operator_decision_selection_required_confirmed"] is True for item in items)
    assert all(item["operator_decision_selection_received_confirmed_false"] is True for item in items)
    assert all(item["operator_decision_selection_value_pending_confirmed"] is True for item in items)
    assert all(item["operator_decision_required_confirmed"] is True for item in items)
    assert all(item["operator_decision_received_confirmed_false"] is True for item in items)
    assert all(item["operator_decision_value_pending_confirmed"] is True for item in items)
    assert all(item["operator_decision_value_selected_confirmed_false"] is True for item in items)
    assert all(item["explicit_operator_authorization_received_confirmed_false"] is True for item in items)
    assert all(item["implementation_authorization_candidate_confirmed"] is True for item in items)
    assert not any(item["implementation_code_authorized"] for item in items)
    assert not any(item["runtime_execution_authorized"] for item in items)
    assert not any(item["real_submission_authorized"] for item in items)
    assert not any(item["blocking_issue"] for item in items)


def test_task_23_boundary_blocks_code_runtime_submission() -> None:
    controls = build_boundary_controls()

    assert controls["operator_decision_selection_record_review_only"] is True
    assert controls["operator_decision_selection_record_confirmed"] is True
    assert controls["operator_decision_selection_record_review_passed"] is True
    assert controls["operator_decision_value_gate_required"] is True
    assert controls["operator_decision_value_gate_created"] is False
    assert controls["operator_decision_value_gate_allowed_next"] is True
    assert controls["operator_decision_selection_value_normalized"] is True
    assert controls["operator_decision_selection_received"] is False
    assert controls["operator_decision_received"] is False
    assert controls["operator_decision_value_selected"] is False
    assert controls["implementation_code_authorized"] is False
    assert controls["candidate_generator_modified"] is False
    assert controls["runtime_execution_allowed"] is False
    assert controls["real_submission_allowed"] is False
    assert controls["submission_artifact_created"] is False
    assert controls["kaggle_submission_sent"] is False
    assert controls["private_core_exposure"] is False
    assert controls["legal_certification"] is False
    assert controls["fail_closed_active"] is True


def test_task_23_acceptance_and_signature() -> None:
    first = build_candidate_generator_implementation_operator_decision_selection_record_review()
    second = build_candidate_generator_implementation_operator_decision_selection_record_review()

    assert first["acceptance_gate_count"] > 85
    assert first["acceptance_gate_failure_count"] == 0
    assert first["acceptance_gate_failures"] == []
    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["operator_decision_selection_record_review_id"].endswith(first["signature"])


def test_task_23_artifacts_are_written(tmp_path) -> None:
    paths = write_artifacts(
        artifact_dir=tmp_path / "examples" / "task-23",
        docs_path=tmp_path / "docs" / "task-23.md",
    )

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    markdown = paths["markdown"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert "source_boundary_operator_decision_selection_value_drift_detected=True" in manifest
    assert "normalized_operator_decision_selection_value=PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION" in manifest
    assert "operator_decision_value_gate_required=true" in manifest
    assert "operator_decision_selection_received=false" in manifest
    assert "operator_decision_selection_value=PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION" in manifest
    assert "operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION" in manifest
    assert "implementation_code_authorized=false" in manifest
    assert "Controlled Technical Candidate Generator Implementation Operator Decision Selection Record Review v1" in markdown
