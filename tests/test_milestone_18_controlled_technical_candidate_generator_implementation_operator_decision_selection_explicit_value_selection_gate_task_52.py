from __future__ import annotations

import json

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_value_gate import (
    allowed_operator_decision_values,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_selection_actual_operator_decision_value_record_review_task_51 import (
    build_candidate_generator_implementation_operator_decision_selection_actual_operator_decision_value_record_review,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_gate_task_52 import (
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_gate,
    build_operator_decision_selection_explicit_value_selection_gate_items,
    write_artifacts,
)


def test_task_52_ready_valid_created() -> None:
    data = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_gate()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["operator_decision_selection_explicit_value_selection_gate_ready"] is True
    assert data["operator_decision_selection_explicit_value_selection_gate_created"] is True
    assert data["operator_decision_selection_explicit_value_selection_gate_locked"] is True
    assert data["operator_decision_selection_explicit_value_selection_gate_open"] is False
    assert data["operator_decision_selection_explicit_value_selection_gate_review_required"] is True
    assert data["operator_decision_selection_explicit_value_selection_gate_passed"] is False
    assert data["operator_decision_selection_actual_operator_decision_value_record_confirmed"] is True
    assert data["operator_decision_selection_actual_operator_decision_value_record_review_confirmed"] is True
    assert data["operator_decision_selection_authorization_required"] is True
    assert data["operator_decision_selection_authorization_received"] is False
    assert data["operator_decision_selection_authorized"] is False
    assert data["explicit_operator_authorization_received"] is False
    assert data["operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert data["operator_decision_value_selected"] is False
    assert data["operator_decision_selection_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION"
    assert data["implementation_code_authorized"] is False
    assert data["implementation_allowed_now"] is False
    assert data["blocking_issue_count"] == 0


def test_task_52_preserves_task_51_baseline() -> None:
    source = build_candidate_generator_implementation_operator_decision_selection_actual_operator_decision_value_record_review()
    data = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_gate()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "1f7df38"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "016D54580650E8E1"
    assert (
        data["source_operator_decision_selection_actual_operator_decision_value_record_review_signature"]
        == source["signature"]
        == PREVIOUS_SIGNATURE
    )
    assert data["source_operator_decision_selection_actual_operator_decision_value_record_review_validation"].endswith("_VALID")
    assert source["operator_decision_selection_actual_operator_decision_value_record_review_passed"] is True
    assert source["operator_decision_selection_explicit_value_selection_gate_required"] is True
    assert source["operator_decision_selection_explicit_value_selection_gate_allowed_next"] is True


def test_task_52_gate_items_created_pending_review_no_code() -> None:
    source = build_candidate_generator_implementation_operator_decision_selection_actual_operator_decision_value_record_review()
    items = build_operator_decision_selection_explicit_value_selection_gate_items(source)

    assert len(items) == 6
    assert all(
        item["gate_status"]
        == "OPERATOR_DECISION_SELECTION_EXPLICIT_VALUE_SELECTION_GATE_CREATED_PENDING_REVIEW"
        for item in items
    )
    assert all(item["allowed_operator_decision_values"] == allowed_operator_decision_values() for item in items)
    assert all(item["operator_decision_selection_explicit_value_selection_gate_created"] is True for item in items)
    assert all(item["operator_decision_selection_explicit_value_selection_gate_review_required"] is True for item in items)
    assert all(item["operator_decision_selection_explicit_value_selection_gate_open"] is False for item in items)
    assert all(item["operator_decision_selection_actual_operator_decision_value_record_confirmed"] is True for item in items)
    assert all(item["operator_decision_selection_actual_operator_decision_value_record_review_confirmed"] is True for item in items)
    assert all(item["operator_decision_selection_authorization_required"] is True for item in items)
    assert not any(item["operator_decision_selection_authorization_received"] for item in items)
    assert not any(item["operator_decision_selection_authorized"] for item in items)
    assert all(item["operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION" for item in items)
    assert not any(item["operator_decision_value_selected"] for item in items)
    assert all(item["operator_decision_selection_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION" for item in items)
    assert not any(item["explicit_operator_authorization_received"] for item in items)
    assert not any(item["implementation_code_authorized"] for item in items)
    assert not any(item["runtime_execution_authorized"] for item in items)
    assert not any(item["real_submission_authorized"] for item in items)
    assert not any(item["blocking_issue"] for item in items)


def test_task_52_boundary_blocks_code_runtime_submission() -> None:
    controls = build_boundary_controls()

    assert controls["operator_decision_selection_explicit_value_selection_gate_only"] is True
    assert controls["operator_decision_selection_explicit_value_selection_gate_created"] is True
    assert controls["operator_decision_selection_explicit_value_selection_gate_review_required"] is True
    assert controls["operator_decision_selection_actual_operator_decision_value_record_confirmed"] is True
    assert controls["operator_decision_selection_actual_operator_decision_value_record_review_confirmed"] is True
    assert controls["operator_decision_selection_authorization_required"] is True
    assert controls["operator_decision_selection_authorization_received"] is False
    assert controls["operator_decision_selection_authorized"] is False
    assert controls["explicit_operator_authorization_received"] is False
    assert controls["operator_decision_value_pending"] is True
    assert controls["implementation_code_authorized"] is False
    assert controls["candidate_generator_modified"] is False
    assert controls["runtime_execution_allowed"] is False
    assert controls["real_submission_allowed"] is False
    assert controls["submission_artifact_created"] is False
    assert controls["kaggle_submission_sent"] is False
    assert controls["private_core_exposure"] is False
    assert controls["legal_certification"] is False
    assert controls["fail_closed_active"] is True


def test_task_52_acceptance_and_signature() -> None:
    first = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_gate()
    second = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_gate()

    assert first["acceptance_gate_count"] > 113
    assert first["acceptance_gate_failure_count"] == 0
    assert first["acceptance_gate_failures"] == []
    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["operator_decision_selection_explicit_value_selection_gate_id"].endswith(first["signature"])


def test_task_52_artifacts_are_written(tmp_path) -> None:
    paths = write_artifacts(
        artifact_dir=tmp_path / "examples" / "task-52",
        docs_path=tmp_path / "docs" / "task-52.md",
    )

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    markdown = paths["markdown"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert "operator_decision_selection_explicit_value_selection_gate_only=true" in manifest
    assert "operator_decision_selection_explicit_value_selection_gate_created=true" in manifest
    assert "operator_decision_selection_explicit_value_selection_gate_review_required=true" in manifest
    assert "operator_decision_selection_authorization_received=false" in manifest
    assert "operator_decision_selection_authorized=false" in manifest
    assert "explicit_operator_authorization_received=false" in manifest
    assert "operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION" in manifest
    assert "operator_decision_selection_value=PENDING_EXPLICIT_OPERATOR_DECISION_SELECTION" in manifest
    assert "implementation_code_authorized=false" in manifest
    assert "Controlled Technical Candidate Generator Implementation Operator Decision Selection Explicit Value Selection Gate v1" in markdown
