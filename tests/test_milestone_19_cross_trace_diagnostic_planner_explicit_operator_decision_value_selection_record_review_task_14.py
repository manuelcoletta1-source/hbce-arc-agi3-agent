from __future__ import annotations

import json

from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_implementation_authorization_gate_task_3 import (
    ALLOWED_OPERATOR_DECISION_VALUES,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_implementation_operator_decision_record_task_5 import (
    SELECTED_OPERATOR_DECISION_VALUE,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_record_task_13 import (
    build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_record,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_record_review_task_14 import (
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_record_review,
    build_explicit_selection_record_review_items,
    write_artifacts,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_planning_intake_task_1 import (
    build_feature_families,
    build_pipeline_model,
    build_required_output_fields,
    build_test_plan,
)


def test_task_14_ready_valid_review_passed_but_no_authorization() -> None:
    data = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_record_review()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["explicit_operator_decision_value_selection_record_review_ready"] is True
    assert data["explicit_operator_decision_value_selection_record_review_passed"] is True
    assert data["explicit_operator_decision_value_selection_record_confirmed"] is True
    assert data["explicit_operator_decision_value_selection_wait_state_required"] is True
    assert data["explicit_operator_decision_value_selection_wait_state_created"] is False
    assert data["explicit_operator_decision_value_selection_record_created"] is True
    assert data["explicit_operator_decision_value_selection_record_locked"] is True
    assert data["explicit_operator_decision_value_selected"] is False
    assert data["explicit_operator_decision_value_validated"] is False
    assert data["explicit_operator_decision_value_authorizing"] is False
    assert data["selected_operator_decision_value"] == SELECTED_OPERATOR_DECISION_VALUE
    assert data["selected_operator_decision_value_validated"] is False
    assert data["selected_operator_decision_value_authorizing"] is False
    assert data["operator_decision_received"] is False
    assert data["implementation_authorized"] is False
    assert data["acceptance_gate_failure_count"] == 0


def test_task_14_preserves_task_13_baseline() -> None:
    source = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_record()
    data = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_record_review()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "2fd42b8"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "218CE1B1080FAE98"
    assert data["source_explicit_operator_decision_value_selection_record_signature"] == source["signature"] == PREVIOUS_SIGNATURE
    assert source["explicit_operator_decision_value_selection_record_created"] is True
    assert source["explicit_operator_decision_value_selection_record_review_required"] is True
    assert source["explicit_operator_decision_value_selection_record_review_created"] is False
    assert source["explicit_operator_decision_value_selected"] is False
    assert source["selected_operator_decision_value"] == SELECTED_OPERATOR_DECISION_VALUE
    assert source["operator_decision_received"] is False
    assert source["implementation_authorized"] is False


def test_task_14_review_items_confirm_no_selection_and_blocked() -> None:
    source = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_record()
    items = build_explicit_selection_record_review_items(source)

    assert len(items) == 6
    assert all(
        item["review_status"] == "CONFIRMED_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_RECORD_NO_VALUE_SELECTED"
        for item in items
    )
    assert all(
        item["review_effect"]
        == "EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_WAIT_STATE_REQUIRED_IMPLEMENTATION_BLOCKED"
        for item in items
    )
    assert all(item["allowed_operator_decision_values"] == ALLOWED_OPERATOR_DECISION_VALUES for item in items)
    assert all(item["selected_operator_decision_value"] == SELECTED_OPERATOR_DECISION_VALUE for item in items)
    assert not any(item["selected_operator_decision_value_validated"] for item in items)
    assert not any(item["selected_operator_decision_value_authorizing"] for item in items)
    assert not any(item["explicit_operator_decision_value_selected"] for item in items)
    assert not any(item["explicit_operator_decision_value_validated"] for item in items)
    assert not any(item["explicit_operator_decision_value_authorizing"] for item in items)
    assert not any(item["implementation_authorized"] for item in items)
    assert not any(item["operator_decision_received"] for item in items)
    assert not any(item["runtime_solver_modified"] for item in items)
    assert not any(item["candidate_generator_modified"] for item in items)
    assert not any(item["real_evaluation_performed"] for item in items)
    assert not any(item["kaggle_submission_sent"] for item in items)
    assert not any(item["hidden_label_accessed"] for item in items)
    assert not any(item["private_core_exposure"] for item in items)
    assert all(item["fail_closed_active"] is True for item in items)
    assert not any(item["blocking_issue"] for item in items)


def test_task_14_boundary_blocks_everything_after_selection_record_review() -> None:
    controls = build_boundary_controls()

    assert controls["explicit_operator_decision_value_selection_record_review_only"] is True
    assert controls["explicit_operator_decision_value_selection_record_confirmed"] is True
    assert controls["explicit_operator_decision_value_selection_record_review_ready"] is True
    assert controls["explicit_operator_decision_value_selection_record_review_passed"] is True
    assert controls["explicit_operator_decision_value_selection_wait_state_required"] is True
    assert controls["explicit_operator_decision_value_selection_wait_state_created"] is False
    assert controls["explicit_operator_decision_value_selection_record_created"] is True
    assert controls["explicit_operator_decision_value_selection_record_locked"] is True
    assert controls["explicit_operator_decision_value_selected"] is False
    assert controls["explicit_operator_decision_value_validated"] is False
    assert controls["explicit_operator_decision_value_authorizing"] is False
    assert controls["selected_operator_decision_value_pending"] is True
    assert controls["selected_operator_decision_value_validated"] is False
    assert controls["selected_operator_decision_value_authorizing"] is False
    assert controls["operator_decision_received"] is False
    assert controls["implementation_authorized"] is False
    assert controls["runtime_activation_authorized"] is False
    assert controls["runtime_solver_modified"] is False
    assert controls["candidate_generator_modified"] is False
    assert controls["real_evaluation_authorized"] is False
    assert controls["real_submission_authorized"] is False
    assert controls["kaggle_submission_sent"] is False
    assert controls["internet_during_eval"] is False
    assert controls["external_api_dependency"] is False
    assert controls["hidden_label_accessed"] is False
    assert controls["private_core_exposure"] is False
    assert controls["fail_closed_active"] is True


def test_task_14_models_remain_unchanged() -> None:
    data = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_record_review()

    assert data["pipeline_model"] == build_pipeline_model()
    assert data["feature_families"] == build_feature_families()
    assert data["required_output_fields"] == build_required_output_fields()
    assert data["test_plan"] == build_test_plan()


def test_task_14_acceptance_and_signature_are_deterministic() -> None:
    first = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_record_review()
    second = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_record_review()

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["explicit_operator_decision_value_selection_record_review_id"].endswith(first["signature"])
    assert first["acceptance_gate_count"] > 205
    assert first["acceptance_gate_failure_count"] == 0
    assert first["acceptance_gate_failures"] == []


def test_task_14_artifacts_are_written(tmp_path) -> None:
    paths = write_artifacts(
        artifact_dir=tmp_path / "examples" / "milestone-19" / "task-14",
        docs_path=tmp_path / "docs" / "task-14.md",
        index_path=tmp_path / "docs" / "milestone-19-index.md",
    )

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    docs = paths["docs"].read_text(encoding="utf-8")
    milestone_index = paths["milestone_index"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert "explicit_operator_decision_value_selection_record_review_ready=true" in manifest
    assert "explicit_operator_decision_value_selection_record_review_passed=true" in manifest
    assert "explicit_operator_decision_value_selection_record_confirmed=true" in manifest
    assert "explicit_operator_decision_value_selection_wait_state_required=true" in manifest
    assert "explicit_operator_decision_value_selection_wait_state_created=false" in manifest
    assert "explicit_operator_decision_value_selection_record_created=true" in manifest
    assert "explicit_operator_decision_value_selected=false" in manifest
    assert "explicit_operator_decision_value_authorizing=false" in manifest
    assert "selected_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION" in manifest
    assert "operator_decision_received=false" in manifest
    assert "implementation_authorized=false" in manifest
    assert "runtime_solver_modified=false" in manifest
    assert "real_evaluation_authorized=false" in manifest
    assert "kaggle_submission_sent=false" in manifest
    assert "hidden_label_accessed=false" in manifest
    assert "Explicit Operator Decision Value Selection Record Review v1" in docs
    assert "Explicit operator decision value selection record reviewed" in milestone_index
