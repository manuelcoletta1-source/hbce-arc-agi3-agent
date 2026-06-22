from __future__ import annotations

import json

from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_planning_intake_task_1 import (
    build_cross_trace_diagnostic_planner_planning_intake,
    build_feature_families,
    build_pipeline_model,
    build_required_output_fields,
    build_test_plan,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_spec_review_task_2 import (
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_cross_trace_diagnostic_planner_spec_review,
    build_spec_review_items,
    write_artifacts,
)


def test_task_2_ready_valid_spec_review_only() -> None:
    data = build_cross_trace_diagnostic_planner_spec_review()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["spec_review_ready"] is True
    assert data["spec_review_passed"] is True
    assert data["planning_intake_confirmed"] is True
    assert data["implementation_gate_required"] is True
    assert data["implementation_gate_created"] is False
    assert data["implementation_authorized"] is False
    assert data["runtime_activation_performed"] is False
    assert data["runtime_solver_modified"] is False
    assert data["real_evaluation_performed"] is False
    assert data["kaggle_submission_sent"] is False
    assert data["operator_approval_required"] is True
    assert data["operator_approval_received"] is False
    assert data["acceptance_gate_failure_count"] == 0


def test_task_2_preserves_task_1_baseline() -> None:
    source = build_cross_trace_diagnostic_planner_planning_intake()
    data = build_cross_trace_diagnostic_planner_spec_review()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "fcbc26d"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "8EEA061B18EC2B9A"
    assert data["source_planning_intake_signature"] == source["signature"] == PREVIOUS_SIGNATURE
    assert source["planning_artifact_ready"] is True
    assert source["boundary_controls"]["implementation_authorized"] is False


def test_task_2_review_items_confirm_spec_components() -> None:
    source = build_cross_trace_diagnostic_planner_planning_intake()
    items = build_spec_review_items(source)

    assert len(items) == 6
    assert all(item["review_status"].startswith("CONFIRMED") for item in items)
    assert not any(item["blocking_issue"] for item in items)

    pipeline_item = next(item for item in items if item["review_area"] == "pipeline_model")
    feature_item = next(item for item in items if item["review_area"] == "feature_families")
    output_item = next(item for item in items if item["review_area"] == "required_output_model")
    test_item = next(item for item in items if item["review_area"] == "test_plan")

    assert pipeline_item["actual"] == build_pipeline_model()
    assert feature_item["actual"] == build_feature_families()
    assert output_item["actual"] == build_required_output_fields()
    assert test_item["actual_test_count"] == 6


def test_task_2_boundary_blocks_implementation_runtime_eval_submission() -> None:
    controls = build_boundary_controls()

    assert controls["spec_review_only"] is True
    assert controls["planning_intake_confirmed"] is True
    assert controls["planning_only"] is True
    assert controls["implementation_authorized"] is False
    assert controls["implementation_gate_required"] is True
    assert controls["implementation_gate_created"] is False
    assert controls["runtime_activation_performed"] is False
    assert controls["runtime_solver_modified"] is False
    assert controls["candidate_generator_modified"] is False
    assert controls["ranker_modified"] is False
    assert controls["verifier_modified"] is False
    assert controls["real_evaluation_performed"] is False
    assert controls["real_submission_authorized"] is False
    assert controls["kaggle_submission_sent"] is False
    assert controls["internet_during_eval"] is False
    assert controls["external_api_dependency"] is False
    assert controls["hidden_label_accessed"] is False
    assert controls["private_core_exposure"] is False
    assert controls["operator_approval_required"] is True
    assert controls["operator_approval_received"] is False
    assert controls["fail_closed_active"] is True


def test_task_2_models_remain_unchanged_from_task_1() -> None:
    data = build_cross_trace_diagnostic_planner_spec_review()

    assert data["pipeline_model"] == build_pipeline_model()
    assert data["feature_families"] == build_feature_families()
    assert data["required_output_fields"] == build_required_output_fields()
    assert data["test_plan"] == build_test_plan()


def test_task_2_acceptance_and_signature_are_deterministic() -> None:
    first = build_cross_trace_diagnostic_planner_spec_review()
    second = build_cross_trace_diagnostic_planner_spec_review()

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["spec_review_id"].endswith(first["signature"])
    assert first["acceptance_gate_count"] > 61
    assert first["acceptance_gate_failure_count"] == 0
    assert first["acceptance_gate_failures"] == []


def test_task_2_artifacts_are_written(tmp_path) -> None:
    paths = write_artifacts(
        artifact_dir=tmp_path / "examples" / "milestone-19" / "task-2",
        docs_path=tmp_path / "docs" / "task-2.md",
        index_path=tmp_path / "docs" / "milestone-19-index.md",
    )

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    docs = paths["docs"].read_text(encoding="utf-8")
    milestone_index = paths["milestone_index"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert "spec_review_passed=true" in manifest
    assert "planning_intake_confirmed=true" in manifest
    assert "planning_only=true" in manifest
    assert "implementation_gate_required=true" in manifest
    assert "implementation_authorized=false" in manifest
    assert "runtime_solver_modified=false" in manifest
    assert "real_evaluation_performed=false" in manifest
    assert "kaggle_submission_sent=false" in manifest
    assert "operator_approval_required=true" in manifest
    assert "Cross-Trace Diagnostic Planner Spec Review v1" in docs
    assert "Spec review passed" in milestone_index
