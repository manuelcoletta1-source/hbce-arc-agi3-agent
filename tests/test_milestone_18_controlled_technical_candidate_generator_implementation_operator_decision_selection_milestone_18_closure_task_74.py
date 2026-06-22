from __future__ import annotations

import json

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate_review_task_73 import (
    build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate_review,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_selection_milestone_18_closure_task_74 import (
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_candidate_generator_implementation_operator_decision_selection_milestone_18_closure,
    build_closure_items,
    write_artifacts,
)


def test_task_74_ready_valid_closed() -> None:
    data = build_candidate_generator_implementation_operator_decision_selection_milestone_18_closure()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["milestone_18_closure_ready"] is True
    assert data["milestone_18_closure_created"] is True
    assert data["milestone_18_closed"] is True
    assert data["milestone_18_no_further_internal_gate_loop"] is True
    assert data["operator_decision_still_pending"] is True
    assert data["operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert data["operator_decision_value_selected"] is False
    assert data["final_operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert data["final_operator_decision_value_selected"] is False
    assert data["final_operator_decision_value_validated"] is False
    assert data["final_operator_decision_value_gate_authorized"] is False
    assert data["final_operator_decision_value_gate_decision_selected"] is False
    assert data["operator_decision_selection_authorization_received"] is False
    assert data["operator_decision_selection_authorized"] is False
    assert data["explicit_operator_authorization_received"] is False
    assert data["implementation_remains_blocked"] is True
    assert data["implementation_code_authorized"] is False
    assert data["implementation_allowed_now"] is False
    assert data["runtime_execution_allowed"] is False
    assert data["real_evaluation_allowed"] is False
    assert data["real_submission_allowed"] is False
    assert data["kaggle_submission_sent"] is False
    assert data["fail_closed_active"] is True
    assert data["blocking_issue_count"] == 0


def test_task_74_preserves_task_73_baseline() -> None:
    source = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate_review()
    data = build_candidate_generator_implementation_operator_decision_selection_milestone_18_closure()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "9169f60"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "DC5666DE6A691292"
    assert (
        data["source_final_operator_decision_value_gate_review_signature"]
        == source["signature"]
        == PREVIOUS_SIGNATURE
    )
    assert source["final_operator_decision_value_gate_review_passed"] is True
    assert source["milestone_18_closure_required"] is True
    assert source["milestone_18_closure_allowed_next"] is True


def test_task_74_closure_items_close_without_implementation() -> None:
    source = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate_review()
    items = build_closure_items(source)

    assert len(items) == 6
    assert all(
        item["closure_status"]
        == "MILESTONE_18_CLOSED_OPERATOR_DECISION_PENDING_IMPLEMENTATION_BLOCKED"
        for item in items
    )
    assert all(item["operator_decision_still_pending"] is True for item in items)
    assert all(item["implementation_remains_blocked"] is True for item in items)
    assert not any(item["implementation_code_authorized"] for item in items)
    assert not any(item["runtime_execution_allowed"] for item in items)
    assert not any(item["real_evaluation_allowed"] for item in items)
    assert not any(item["real_submission_allowed"] for item in items)
    assert not any(item["submission_artifact_created"] for item in items)
    assert not any(item["kaggle_submission_sent"] for item in items)
    assert not any(item["private_core_exposure"] for item in items)
    assert not any(item["legal_certification"] for item in items)
    assert all(item["fail_closed_active"] is True for item in items)
    assert not any(item["blocking_issue"] for item in items)


def test_task_74_boundary_is_final_fail_closed_closure() -> None:
    controls = build_boundary_controls()

    assert controls["milestone_18_closure_only"] is True
    assert controls["milestone_18_closed"] is True
    assert controls["milestone_18_no_further_internal_gate_loop"] is True
    assert controls["operator_decision_still_pending"] is True
    assert controls["operator_decision_value_still_pending"] is True
    assert controls["operator_decision_selection_still_pending"] is True
    assert controls["implementation_remains_blocked"] is True
    assert controls["implementation_code_authorized"] is False
    assert controls["candidate_generator_modified"] is False
    assert controls["runtime_execution_allowed"] is False
    assert controls["real_evaluation_allowed"] is False
    assert controls["real_submission_allowed"] is False
    assert controls["kaggle_submission_sent"] is False
    assert controls["private_core_exposure"] is False
    assert controls["legal_certification"] is False
    assert controls["fail_closed_active"] is True


def test_task_74_acceptance_and_signature() -> None:
    first = build_candidate_generator_implementation_operator_decision_selection_milestone_18_closure()
    second = build_candidate_generator_implementation_operator_decision_selection_milestone_18_closure()

    assert first["acceptance_gate_count"] > 157
    assert first["acceptance_gate_failure_count"] == 0
    assert first["acceptance_gate_failures"] == []
    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["milestone_18_closure_id"].endswith(first["signature"])


def test_task_74_artifacts_are_written(tmp_path) -> None:
    paths = write_artifacts(
        artifact_dir=tmp_path / "examples" / "task-74",
        docs_path=tmp_path / "docs" / "task-74.md",
    )

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    markdown = paths["markdown"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert "milestone_18_closed=true" in manifest
    assert "milestone_18_no_further_internal_gate_loop=true" in manifest
    assert "operator_decision_still_pending=true" in manifest
    assert "implementation_remains_blocked=true" in manifest
    assert "implementation_code_authorized=false" in manifest
    assert "runtime_execution_allowed=false" in manifest
    assert "real_evaluation_allowed=false" in manifest
    assert "real_submission_allowed=false" in manifest
    assert "kaggle_submission_sent=false" in manifest
    assert "fail_closed_active=true" in manifest
    assert "Milestone 18 Task 74" in markdown
