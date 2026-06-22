from __future__ import annotations

import json

from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_planning_intake_task_1 import (
    build_feature_families,
    build_pipeline_model,
    build_required_output_fields,
    build_test_plan,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_spec_review_task_2 import (
    build_cross_trace_diagnostic_planner_spec_review,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_implementation_authorization_gate_task_3 import (
    ALLOWED_OPERATOR_DECISION_VALUES,
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_authorization_gate_items,
    build_boundary_controls,
    build_cross_trace_diagnostic_planner_implementation_authorization_gate,
    write_artifacts,
)


def test_task_3_ready_valid_gate_created_but_not_authorized() -> None:
    data = build_cross_trace_diagnostic_planner_implementation_authorization_gate()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["implementation_authorization_gate_ready"] is True
    assert data["implementation_authorization_gate_created"] is True
    assert data["implementation_authorization_gate_review_required"] is True
    assert data["implementation_authorization_gate_passed"] is False
    assert data["implementation_authorized"] is False
    assert data["implementation_authorization_received"] is False
    assert data["implementation_decision_selected"] is False
    assert data["selected_operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert data["operator_approval_required"] is True
    assert data["operator_approval_received"] is False
    assert data["operator_decision_required_for_implementation"] is True
    assert data["operator_decision_received"] is False
    assert data["acceptance_gate_failure_count"] == 0


def test_task_3_preserves_task_2_baseline() -> None:
    source = build_cross_trace_diagnostic_planner_spec_review()
    data = build_cross_trace_diagnostic_planner_implementation_authorization_gate()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "98bfea3"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "E1993A6E809CCEFA"
    assert data["source_spec_review_signature"] == source["signature"] == PREVIOUS_SIGNATURE
    assert source["spec_review_passed"] is True
    assert source["implementation_gate_required"] is True
    assert source["implementation_authorized"] is False


def test_task_3_gate_items_are_created_without_authorization() -> None:
    source = build_cross_trace_diagnostic_planner_spec_review()
    items = build_authorization_gate_items(source)

    assert len(items) == 6
    assert not any(item["blocking_issue"] for item in items)
    assert any(item["gate_area"] == "implementation_scope" for item in items)
    assert any(item["gate_area"] == "runtime_activation" for item in items)
    assert any(item["gate_area"] == "real_evaluation" for item in items)
    assert any(item["gate_area"] == "submission_boundary" for item in items)
    assert any(item["gate_area"] == "external_access_boundary" for item in items)
    assert any(item["gate_area"] == "operator_decision_values" for item in items)
    assert not any(item.get("implementation_authorized", False) for item in items)


def test_task_3_allowed_operator_decision_values_are_declared() -> None:
    data = build_cross_trace_diagnostic_planner_implementation_authorization_gate()

    assert data["allowed_operator_decision_values"] == ALLOWED_OPERATOR_DECISION_VALUES
    assert data["selected_operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert "AUTHORIZE_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_ONLY" in data["allowed_operator_decision_values"]
    assert "DEFER_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_KEEP_PLANNING_ONLY" in data["allowed_operator_decision_values"]


def test_task_3_boundary_blocks_runtime_eval_submission() -> None:
    controls = build_boundary_controls()

    assert controls["implementation_authorization_gate_only"] is True
    assert controls["implementation_authorization_gate_created"] is True
    assert controls["implementation_authorization_gate_review_required"] is True
    assert controls["implementation_authorized"] is False
    assert controls["implementation_authorization_received"] is False
    assert controls["operator_approval_required"] is True
    assert controls["operator_approval_received"] is False
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


def test_task_3_models_remain_unchanged_from_spec() -> None:
    data = build_cross_trace_diagnostic_planner_implementation_authorization_gate()

    assert data["pipeline_model"] == build_pipeline_model()
    assert data["feature_families"] == build_feature_families()
    assert data["required_output_fields"] == build_required_output_fields()
    assert data["test_plan"] == build_test_plan()


def test_task_3_acceptance_and_signature_are_deterministic() -> None:
    first = build_cross_trace_diagnostic_planner_implementation_authorization_gate()
    second = build_cross_trace_diagnostic_planner_implementation_authorization_gate()

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["implementation_authorization_gate_id"].endswith(first["signature"])
    assert first["acceptance_gate_count"] > 73
    assert first["acceptance_gate_failure_count"] == 0
    assert first["acceptance_gate_failures"] == []


def test_task_3_artifacts_are_written(tmp_path) -> None:
    paths = write_artifacts(
        artifact_dir=tmp_path / "examples" / "milestone-19" / "task-3",
        docs_path=tmp_path / "docs" / "task-3.md",
        index_path=tmp_path / "docs" / "milestone-19-index.md",
    )

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    docs = paths["docs"].read_text(encoding="utf-8")
    milestone_index = paths["milestone_index"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert "implementation_authorization_gate_created=true" in manifest
    assert "implementation_authorization_gate_review_required=true" in manifest
    assert "implementation_authorized=false" in manifest
    assert "implementation_authorization_received=false" in manifest
    assert "selected_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION" in manifest
    assert "runtime_solver_modified=false" in manifest
    assert "real_evaluation_authorized=false" in manifest
    assert "kaggle_submission_sent=false" in manifest
    assert "operator_approval_required=true" in manifest
    assert "Implementation Authorization Gate v1" in docs
    assert "Implementation still blocked" in milestone_index
