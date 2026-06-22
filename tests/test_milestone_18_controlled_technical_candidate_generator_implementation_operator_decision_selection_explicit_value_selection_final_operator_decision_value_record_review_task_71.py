from __future__ import annotations

import json

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_value_gate import (
    allowed_operator_decision_values,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_task_70 import (
    build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_review_task_71 import (
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_review,
    build_final_operator_decision_value_record_review_items,
    write_artifacts,
)


def test_task_71_ready_valid_passed() -> None:
    data = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_review()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["final_operator_decision_value_record_review_ready"] is True
    assert data["final_operator_decision_value_record_review_passed"] is True
    assert data["final_operator_decision_value_record_confirmed"] is True
    assert data["final_operator_decision_value_gate_required"] is True
    assert data["final_operator_decision_value_gate_allowed_next"] is True
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


def test_task_71_preserves_task_70_baseline() -> None:
    source = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record()
    data = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_review()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "b655d6d"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "4374A4A4325D7FAB"
    assert (
        data["source_final_operator_decision_value_record_signature"]
        == source["signature"]
        == PREVIOUS_SIGNATURE
    )
    assert source["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_created"] is True
    assert source["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_review_required"] is True
    assert source["operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_passed"] is False


def test_task_71_review_items_pending_gate_no_code() -> None:
    source = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record()
    items = build_final_operator_decision_value_record_review_items(source)

    assert len(items) == 6
    assert all(
        item["review_decision"]
        == "CONFIRMED_FINAL_OPERATOR_DECISION_VALUE_RECORD_PENDING_FINAL_OPERATOR_DECISION_VALUE_GATE"
        for item in items
    )
    assert all(item["allowed_operator_decision_values_confirmed"] == allowed_operator_decision_values() for item in items)
    assert all(item["selected_operator_decision_value_confirmed"] == "PENDING_EXPLICIT_OPERATOR_DECISION" for item in items)
    assert not any(item["selected_operator_decision_value_validated_confirmed"] for item in items)
    assert all(item["final_operator_decision_value_confirmed"] == "PENDING_EXPLICIT_OPERATOR_DECISION" for item in items)
    assert not any(item["final_operator_decision_value_selected_confirmed"] for item in items)
    assert not any(item["final_operator_decision_value_validated_confirmed"] for item in items)
    assert all(item["final_operator_decision_value_gate_required"] is True for item in items)
    assert all(item["final_operator_decision_value_gate_allowed_next"] is True for item in items)
    assert not any(item["final_operator_decision_value_record_authorized_confirmed"] for item in items)
    assert not any(item["final_operator_decision_value_record_value_selected_confirmed"] for item in items)
    assert not any(item["operator_decision_selection_authorization_received_confirmed"] for item in items)
    assert not any(item["operator_decision_selection_authorized_confirmed"] for item in items)
    assert not any(item["explicit_operator_authorization_received_confirmed"] for item in items)
    assert not any(item["implementation_code_authorized"] for item in items)
    assert not any(item["runtime_execution_authorized"] for item in items)
    assert not any(item["real_submission_authorized"] for item in items)
    assert not any(item["blocking_issue"] for item in items)


def test_task_71_boundary_blocks_code_runtime_submission() -> None:
    controls = build_boundary_controls()

    assert controls["final_operator_decision_value_record_review_only"] is True
    assert controls["final_operator_decision_value_record_confirmed"] is True
    assert controls["final_operator_decision_value_record_review_passed"] is True
    assert controls["final_operator_decision_value_gate_required"] is True
    assert controls["final_operator_decision_value_gate_created"] is False
    assert controls["final_operator_decision_value_gate_allowed_next"] is True
    assert controls["final_operator_decision_value_record_authorized"] is False
    assert controls["final_operator_decision_value_record_value_selected"] is False
    assert controls["final_operator_decision_value_pending"] is True
    assert controls["final_operator_decision_value_selected"] is False
    assert controls["final_operator_decision_value_validated"] is False
    assert controls["operator_decision_selection_authorization_received"] is False
    assert controls["operator_decision_selection_authorized"] is False
    assert controls["explicit_operator_authorization_received"] is False
    assert controls["implementation_code_authorized"] is False
    assert controls["candidate_generator_modified"] is False
    assert controls["runtime_execution_allowed"] is False
    assert controls["real_submission_allowed"] is False
    assert controls["kaggle_submission_sent"] is False
    assert controls["private_core_exposure"] is False
    assert controls["legal_certification"] is False
    assert controls["fail_closed_active"] is True


def test_task_71_acceptance_and_signature() -> None:
    first = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_review()
    second = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_record_review()

    assert first["acceptance_gate_count"] > 151
    assert first["acceptance_gate_failure_count"] == 0
    assert first["acceptance_gate_failures"] == []
    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["final_operator_decision_value_record_review_id"].endswith(first["signature"])


def test_task_71_artifacts_are_written(tmp_path) -> None:
    paths = write_artifacts(
        artifact_dir=tmp_path / "examples" / "task-71",
        docs_path=tmp_path / "docs" / "task-71.md",
    )

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    markdown = paths["markdown"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert "final_operator_decision_value_record_review_ready=true" in manifest
    assert "final_operator_decision_value_record_review_passed=true" in manifest
    assert "final_operator_decision_value_record_confirmed=true" in manifest
    assert "final_operator_decision_value_gate_required=true" in manifest
    assert "final_operator_decision_value_gate_allowed_next=true" in manifest
    assert "selected_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION" in manifest
    assert "selected_operator_decision_value_validated=false" in manifest
    assert "final_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION" in manifest
    assert "final_operator_decision_value_selected=false" in manifest
    assert "final_operator_decision_value_validated=false" in manifest
    assert "final_operator_decision_value_record_authorized=false" in manifest
    assert "implementation_code_authorized=false" in manifest
    assert "Controlled Technical Candidate Generator Implementation Operator Decision Selection Explicit Value Selection Final Operator Decision Value Record Review v1" in markdown
