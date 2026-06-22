from __future__ import annotations

import json

from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_implementation_authorization_gate_task_3 import (
    ALLOWED_OPERATOR_DECISION_VALUES,
    build_cross_trace_diagnostic_planner_implementation_authorization_gate,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_implementation_authorization_gate_review_task_4 import (
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_authorization_gate_review_items,
    build_boundary_controls,
    build_cross_trace_diagnostic_planner_implementation_authorization_gate_review,
    write_artifacts,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_planning_intake_task_1 import (
    build_feature_families,
    build_pipeline_model,
    build_required_output_fields,
    build_test_plan,
)


def test_task_4_ready_valid_gate_review_passed_but_no_authorization() -> None:
    data = build_cross_trace_diagnostic_planner_implementation_authorization_gate_review()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["implementation_authorization_gate_review_ready"] is True
    assert data["implementation_authorization_gate_review_passed"] is True
    assert data["implementation_authorization_gate_confirmed"] is True
    assert data["implementation_operator_decision_record_required"] is True
    assert data["implementation_operator_decision_record_created"] is False
    assert data["implementation_authorization_gate_created"] is True
    assert data["implementation_authorization_gate_passed"] is False
    assert data["implementation_authorized"] is False
    assert data["implementation_authorization_received"] is False
    assert data["implementation_decision_selected"] is False
    assert data["selected_operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert data["selected_operator_decision_value_validated"] is False
    assert data["operator_approval_required"] is True
    assert data["operator_approval_received"] is False
    assert data["operator_decision_required_for_implementation"] is True
    assert data["operator_decision_received"] is False
    assert data["acceptance_gate_failure_count"] == 0


def test_task_4_preserves_task_3_baseline() -> None:
    source = build_cross_trace_diagnostic_planner_implementation_authorization_gate()
    data = build_cross_trace_diagnostic_planner_implementation_authorization_gate_review()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "f0655bc"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "B48C9E344F867523"
    assert data["source_implementation_authorization_gate_signature"] == source["signature"] == PREVIOUS_SIGNATURE
    assert source["implementation_authorization_gate_created"] is True
    assert source["implementation_authorized"] is False
    assert source["operator_decision_received"] is False


def test_task_4_review_items_confirm_gate_without_implementation() -> None:
    source = build_cross_trace_diagnostic_planner_implementation_authorization_gate()
    items = build_authorization_gate_review_items(source)

    assert len(items) == 6
    assert all(
        item["review_status"] == "CONFIRMED_GATE_CREATED_PENDING_OPERATOR_DECISION"
        for item in items
    )
    assert all(
        item["review_effect"] == "IMPLEMENTATION_OPERATOR_DECISION_RECORD_REQUIRED_NO_IMPLEMENTATION"
        for item in items
    )
    assert all(item["allowed_operator_decision_values"] == ALLOWED_OPERATOR_DECISION_VALUES for item in items)
    assert all(item["selected_operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION" for item in items)
    assert not any(item["selected_operator_decision_value_validated"] for item in items)
    assert all(item["implementation_authorization_gate_created"] is True for item in items)
    assert all(item["implementation_authorization_gate_confirmed"] is True for item in items)
    assert not any(item["implementation_authorized"] for item in items)
    assert not any(item["implementation_authorization_received"] for item in items)
    assert not any(item["operator_approval_received"] for item in items)
    assert not any(item["operator_decision_received"] for item in items)
    assert not any(item["runtime_solver_modified"] for item in items)
    assert not any(item["candidate_generator_modified"] for item in items)
    assert not any(item["real_evaluation_performed"] for item in items)
    assert not any(item["kaggle_submission_sent"] for item in items)
    assert not any(item["hidden_label_accessed"] for item in items)
    assert not any(item["private_core_exposure"] for item in items)
    assert all(item["fail_closed_active"] is True for item in items)
    assert not any(item["blocking_issue"] for item in items)


def test_task_4_boundary_blocks_everything_after_review() -> None:
    controls = build_boundary_controls()

    assert controls["implementation_authorization_gate_review_only"] is True
    assert controls["implementation_authorization_gate_confirmed"] is True
    assert controls["implementation_authorization_gate_review_ready"] is True
    assert controls["implementation_authorization_gate_review_passed"] is True
    assert controls["implementation_operator_decision_record_required"] is True
    assert controls["implementation_operator_decision_record_created"] is False
    assert controls["implementation_authorization_gate_created"] is True
    assert controls["implementation_authorization_gate_passed"] is False
    assert controls["implementation_authorized"] is False
    assert controls["implementation_authorization_received"] is False
    assert controls["implementation_decision_selected"] is False
    assert controls["selected_operator_decision_value_validated"] is False
    assert controls["operator_approval_required"] is True
    assert controls["operator_approval_received"] is False
    assert controls["operator_decision_required_for_implementation"] is True
    assert controls["operator_decision_received"] is False
    assert controls["runtime_activation_authorized"] is False
    assert controls["runtime_activation_performed"] is False
    assert controls["runtime_solver_modified"] is False
    assert controls["candidate_generator_modified"] is False
    assert controls["ranker_modified"] is False
    assert controls["verifier_modified"] is False
    assert controls["real_evaluation_authorized"] is False
    assert controls["real_evaluation_performed"] is False
    assert controls["real_submission_authorized"] is False
    assert controls["submission_artifact_created"] is False
    assert controls["kaggle_submission_sent"] is False
    assert controls["internet_during_eval"] is False
    assert controls["external_api_dependency"] is False
    assert controls["hidden_label_accessed"] is False
    assert controls["private_core_exposure"] is False
    assert controls["fail_closed_active"] is True


def test_task_4_models_remain_unchanged() -> None:
    data = build_cross_trace_diagnostic_planner_implementation_authorization_gate_review()

    assert data["pipeline_model"] == build_pipeline_model()
    assert data["feature_families"] == build_feature_families()
    assert data["required_output_fields"] == build_required_output_fields()
    assert data["test_plan"] == build_test_plan()


def test_task_4_acceptance_and_signature_are_deterministic() -> None:
    first = build_cross_trace_diagnostic_planner_implementation_authorization_gate_review()
    second = build_cross_trace_diagnostic_planner_implementation_authorization_gate_review()

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["implementation_authorization_gate_review_id"].endswith(first["signature"])
    assert first["acceptance_gate_count"] > 85
    assert first["acceptance_gate_failure_count"] == 0
    assert first["acceptance_gate_failures"] == []


def test_task_4_artifacts_are_written(tmp_path) -> None:
    paths = write_artifacts(
        artifact_dir=tmp_path / "examples" / "milestone-19" / "task-4",
        docs_path=tmp_path / "docs" / "task-4.md",
        index_path=tmp_path / "docs" / "milestone-19-index.md",
    )

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    docs = paths["docs"].read_text(encoding="utf-8")
    milestone_index = paths["milestone_index"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert "implementation_authorization_gate_review_ready=true" in manifest
    assert "implementation_authorization_gate_review_passed=true" in manifest
    assert "implementation_authorization_gate_confirmed=true" in manifest
    assert "implementation_operator_decision_record_required=true" in manifest
    assert "implementation_authorized=false" in manifest
    assert "selected_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION" in manifest
    assert "runtime_solver_modified=false" in manifest
    assert "real_evaluation_authorized=false" in manifest
    assert "kaggle_submission_sent=false" in manifest
    assert "hidden_label_accessed=false" in manifest
    assert "Implementation Authorization Gate Review v1" in docs
    assert "Implementation operator decision record required" in milestone_index
