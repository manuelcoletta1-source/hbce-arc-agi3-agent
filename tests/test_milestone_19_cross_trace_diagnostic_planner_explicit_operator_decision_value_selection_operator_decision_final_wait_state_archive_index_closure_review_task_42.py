from __future__ import annotations

import json

from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_implementation_authorization_gate_task_3 import (
    ALLOWED_OPERATOR_DECISION_VALUES,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_implementation_operator_decision_record_task_5 import (
    SELECTED_OPERATOR_DECISION_VALUE,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review_task_42 import (
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_archive_index_closure_review_items,
    build_boundary_controls,
    build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review,
    write_artifacts,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_task_41 import (
    build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure,
)


def test_task_42_ready_valid_archive_index_closure_review_passed_without_authorization() -> None:
    data = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review_ready"] is True
    assert data["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review_passed"] is True
    assert data["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_confirmed"] is True
    assert data["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_final_pending_status_required"] is True
    assert data["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_final_pending_status_created"] is False
    assert data["waiting_for_explicit_operator_decision_value"] is True
    assert data["operator_decision_pending_status_active"] is True
    assert data["selected_operator_decision_value"] == SELECTED_OPERATOR_DECISION_VALUE
    assert data["operator_decision_received"] is False
    assert data["implementation_authorized"] is False
    assert data["runtime_solver_modified"] is False
    assert data["real_evaluation_authorized"] is False
    assert data["kaggle_submission_sent"] is False
    assert data["review_item_count"] == len(ALLOWED_OPERATOR_DECISION_VALUES)
    assert data["acceptance_gate_failure_count"] == 0


def test_task_42_preserves_task_41_baseline() -> None:
    source = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure()
    data = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "62bac98"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "93B52C3BCC5E1A48"
    assert data["source_explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_signature"] == source["signature"] == PREVIOUS_SIGNATURE
    assert source["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_created"] is True
    assert source["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review_required"] is True
    assert source["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review_created"] is False
    assert source["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_active"] is False
    assert source["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closed"] is True
    assert source["waiting_for_explicit_operator_decision_value"] is True
    assert source["operator_decision_received"] is False
    assert source["implementation_authorized"] is False


def test_task_42_review_items_confirm_archive_closure_not_selected_and_blocked() -> None:
    source = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure()
    items = build_archive_index_closure_review_items(source)

    assert len(items) == len(ALLOWED_OPERATOR_DECISION_VALUES)
    assert all(item["decision_value"] in ALLOWED_OPERATOR_DECISION_VALUES for item in items)
    assert all(item["review_status"] == "CONFIRMED_FINAL_WAIT_STATE_ARCHIVE_INDEX_CLOSURE_VALUE_AVAILABLE_NOT_SELECTED" for item in items)
    assert all(item["review_effect"] == "ARCHIVE_INDEX_FINAL_PENDING_STATUS_REQUIRED_NO_SELECTION_NO_IMPLEMENTATION_NO_RUNTIME_NO_EVALUATION_NO_SUBMISSION" for item in items)
    assert all(item["selected_operator_decision_value"] == SELECTED_OPERATOR_DECISION_VALUE for item in items)
    assert all(item["waiting_for_explicit_operator_decision_value"] is True for item in items)
    assert all(item["operator_decision_pending_status_active"] is True for item in items)
    assert all(item["operator_decision_final_wait_state_active"] is False for item in items)
    assert all(item["operator_decision_final_wait_state_closed"] is True for item in items)
    assert not any(item["explicit_operator_decision_value_selected"] for item in items)
    assert not any(item["operator_decision_received"] for item in items)
    assert not any(item["implementation_authorized"] for item in items)
    assert not any(item["runtime_solver_modified"] for item in items)
    assert not any(item["candidate_generator_modified"] for item in items)
    assert not any(item["real_evaluation_performed"] for item in items)
    assert not any(item["kaggle_submission_sent"] for item in items)
    assert not any(item["hidden_label_accessed"] for item in items)
    assert not any(item["private_core_exposure"] for item in items)
    assert all(item["fail_closed_active"] is True for item in items)
    assert not any(item["blocking_issue"] for item in items)


def test_task_42_boundary_review_passed_and_final_pending_required_without_runtime() -> None:
    controls = build_boundary_controls()

    assert controls["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review_only"] is True
    assert controls["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review_ready"] is True
    assert controls["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review_passed"] is True
    assert controls["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_confirmed"] is True
    assert controls["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_final_pending_status_required"] is True
    assert controls["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_final_pending_status_created"] is False
    assert controls["waiting_for_explicit_operator_decision_value"] is True
    assert controls["operator_decision_received"] is False
    assert controls["implementation_authorized"] is False
    assert controls["runtime_activation_authorized"] is False
    assert controls["runtime_solver_modified"] is False
    assert controls["candidate_generator_modified"] is False
    assert controls["real_evaluation_authorized"] is False
    assert controls["kaggle_submission_sent"] is False
    assert controls["hidden_label_accessed"] is False
    assert controls["private_core_exposure"] is False
    assert controls["fail_closed_active"] is True


def test_task_42_operator_prompt_options_still_unselected() -> None:
    data = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review()

    assert len(data["operator_prompt_options"]) == len(ALLOWED_OPERATOR_DECISION_VALUES)
    assert tuple(option["decision_value"] for option in data["operator_prompt_options"]) == ALLOWED_OPERATOR_DECISION_VALUES
    assert not any(option["selected"] for option in data["operator_prompt_options"])
    assert not any(option["validated"] for option in data["operator_prompt_options"])
    assert not any(option["authorizing"] for option in data["operator_prompt_options"])


def test_task_42_acceptance_and_signature_are_deterministic() -> None:
    first = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review()
    second = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review()

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review_id"].endswith(first["signature"])
    assert first["acceptance_gate_count"] > 541
    assert first["acceptance_gate_failure_count"] == 0
    assert first["acceptance_gate_failures"] == []


def test_task_42_artifacts_are_written(tmp_path) -> None:
    paths = write_artifacts(
        artifact_dir=tmp_path / "examples" / "milestone-19" / "task-42",
        docs_path=tmp_path / "docs" / "task-42.md",
        index_path=tmp_path / "docs" / "milestone-19-index.md",
    )

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    docs = paths["docs"].read_text(encoding="utf-8")
    milestone_index = paths["milestone_index"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert "explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review_ready=true" in manifest
    assert "explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_review_passed=true" in manifest
    assert "explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_closure_confirmed=true" in manifest
    assert "explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_final_pending_status_required=true" in manifest
    assert "explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_final_pending_status_created=false" in manifest
    assert "waiting_for_explicit_operator_decision_value=true" in manifest
    assert "selected_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION" in manifest
    assert "operator_decision_received=false" in manifest
    assert "implementation_authorized=false" in manifest
    assert "runtime_solver_modified=false" in manifest
    assert "real_evaluation_authorized=false" in manifest
    assert "kaggle_submission_sent=false" in manifest
    assert "hidden_label_accessed=false" in manifest
    assert "Operator Decision Final Wait State Archive Index Closure Review v1" in docs
    assert "Explicit operator decision final wait state archive index final pending status required next" in milestone_index
