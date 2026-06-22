from __future__ import annotations

import json

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_value_gate import (
    allowed_operator_decision_values,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_decision_gate_review_task_69 import (
    build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_decision_gate_review,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_task_70 import (
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record,
    build_final_operator_decision_value_record_items,
    write_artifacts,
)


def test_task_70_ready_valid_created() -> None:
    data = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_ready"] is True
    assert data["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_created"] is True
    assert data["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_review_required"] is True
    assert data["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_passed"] is False
    assert data["operator_decision_selection_explicit_value_selection_final_decision_gate_confirmed"] is True
    assert data["operator_decision_selection_explicit_value_selection_final_decision_gate_review_confirmed"] is True
    assert data["selected_operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert data["selected_operator_decision_value_validated"] is False
    assert data["final_operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert data["final_operator_decision_value_selected"] is False
    assert data["final_operator_decision_value_validated"] is False
    assert data["final_operator_decision_value_record_authorized"] is False
    assert data["final_operator_decision_value_record_value_selected"] is False
    assert data["operator_decision_selection_authorization_received"] is False
    assert data["operator_decision_selection_authorized"] is False
    assert data["explicit_operator_authorization_received"] is False
    assert data["implementation_code_authorized"] is False
    assert data["implementation_allowed_now"] is False
    assert data["blocking_issue_count"] == 0


def test_task_70_preserves_task_69_baseline() -> None:
    source = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_decision_gate_review()
    data = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "e700a22"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "D10E154BE4DFD12A"
    assert (
        data["source_operator_decision_selection_explicit_value_selection_final_decision_gate_review_signature"]
        == source["signature"]
        == PREVIOUS_SIGNATURE
    )
    assert source["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_required"] is True
    assert source["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_allowed_next"] is True


def test_task_70_record_items_pending_no_code() -> None:
    source = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_decision_gate_review()
    items = build_final_operator_decision_value_record_items(source)

    assert len(items) == 6
    assert all(
        item["record_status"]
        == "FINAL_OPERATOR_DECISION_VALUE_RECORD_CREATED_PENDING_REVIEW_NO_VALUE_SELECTED"
        for item in items
    )
    assert all(item["allowed_operator_decision_values"] == allowed_operator_decision_values() for item in items)
    assert all(item["selected_operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION" for item in items)
    assert not any(item["selected_operator_decision_value_validated"] for item in items)
    assert all(item["final_operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION" for item in items)
    assert not any(item["final_operator_decision_value_selected"] for item in items)
    assert not any(item["final_operator_decision_value_validated"] for item in items)
    assert all(item["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_created"] is True for item in items)
    assert all(item["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_review_required"] is True for item in items)
    assert not any(item["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_authorized"] for item in items)
    assert not any(item["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_value_selected"] for item in items)
    assert not any(item["operator_decision_selection_authorization_received"] for item in items)
    assert not any(item["operator_decision_selection_authorized"] for item in items)
    assert not any(item["explicit_operator_authorization_received"] for item in items)
    assert not any(item["implementation_code_authorized"] for item in items)
    assert not any(item["runtime_execution_authorized"] for item in items)
    assert not any(item["real_submission_authorized"] for item in items)
    assert not any(item["blocking_issue"] for item in items)


def test_task_70_boundary_blocks_code_runtime_submission() -> None:
    controls = build_boundary_controls()

    assert controls["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_only"] is True
    assert controls["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_created"] is True
    assert controls["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_review_required"] is True
    assert controls["operator_decision_selection_authorization_required"] is True
    assert controls["operator_decision_selection_authorization_received"] is False
    assert controls["operator_decision_selection_authorized"] is False
    assert controls["explicit_operator_authorization_received"] is False
    assert controls["selected_operator_decision_value_pending"] is True
    assert controls["selected_operator_decision_value_validated"] is False
    assert controls["final_operator_decision_value_pending"] is True
    assert controls["final_operator_decision_value_selected"] is False
    assert controls["final_operator_decision_value_validated"] is False
    assert controls["final_operator_decision_value_record_authorized"] is False
    assert controls["final_operator_decision_value_record_value_selected"] is False
    assert controls["implementation_code_authorized"] is False
    assert controls["candidate_generator_modified"] is False
    assert controls["runtime_execution_allowed"] is False
    assert controls["real_submission_allowed"] is False
    assert controls["kaggle_submission_sent"] is False
    assert controls["private_core_exposure"] is False
    assert controls["legal_certification"] is False
    assert controls["fail_closed_active"] is True


def test_task_70_acceptance_and_signature() -> None:
    first = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record()
    second = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record()

    assert first["acceptance_gate_count"] > 149
    assert first["acceptance_gate_failure_count"] == 0
    assert first["acceptance_gate_failures"] == []
    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_id"].endswith(first["signature"])


def test_task_70_artifacts_are_written(tmp_path) -> None:
    paths = write_artifacts(
        artifact_dir=tmp_path / "examples" / "task-70",
        docs_path=tmp_path / "docs" / "task-70.md",
    )

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    markdown = paths["markdown"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert "final_operator_decision_value_record_created=true" in manifest
    assert "final_operator_decision_value_record_review_required=true" in manifest
    assert "selected_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION" in manifest
    assert "selected_operator_decision_value_validated=false" in manifest
    assert "final_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION" in manifest
    assert "final_operator_decision_value_selected=false" in manifest
    assert "final_operator_decision_value_validated=false" in manifest
    assert "final_operator_decision_value_record_authorized=false" in manifest
    assert "final_operator_decision_value_record_value_selected=false" in manifest
    assert "operator_decision_selection_authorization_received=false" in manifest
    assert "operator_decision_selection_authorized=false" in manifest
    assert "explicit_operator_authorization_received=false" in manifest
    assert "implementation_code_authorized=false" in manifest
    assert "Controlled Technical Candidate Generator Implementation Operator Decision Selection Explicit Value Selection Final Operator Decision Value Record v1" in markdown
