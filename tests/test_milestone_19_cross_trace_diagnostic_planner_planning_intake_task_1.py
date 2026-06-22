from __future__ import annotations

import json

from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_planning_intake_task_1 import (
    PREVIOUS_MILESTONE_CLOSURE_COMMIT,
    PREVIOUS_MILESTONE_CLOSURE_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_cross_trace_diagnostic_planner_planning_intake,
    build_feature_families,
    build_pipeline_model,
    build_required_output_fields,
    build_test_plan,
    write_artifacts,
)


def test_task_1_ready_valid_planning_only() -> None:
    data = build_cross_trace_diagnostic_planner_planning_intake()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["planning_artifact_ready"] is True
    assert data["implementation_status"] == "PLANNING_ALLOWED_IMPLEMENTATION_BLOCKED_RUNTIME_BLOCKED_EVALUATION_BLOCKED_SUBMISSION_BLOCKED"
    assert data["previous_milestone_closure_commit"] == PREVIOUS_MILESTONE_CLOSURE_COMMIT == "287d1d9"
    assert data["previous_milestone_closure_signature"] == PREVIOUS_MILESTONE_CLOSURE_SIGNATURE == "811221A25BFEB5AF"
    assert data["acceptance_gate_failure_count"] == 0


def test_task_1_pipeline_feature_output_models() -> None:
    data = build_cross_trace_diagnostic_planner_planning_intake()

    assert data["pipeline_model"] == build_pipeline_model()
    assert data["feature_families"] == build_feature_families()
    assert data["required_output_fields"] == build_required_output_fields()

    assert "cross_trace_diagnostic_planner" in data["pipeline_model"]
    assert "contradiction" in data["feature_families"]
    assert "verificationStatus" in data["required_output_fields"]
    assert "boundary" in data["required_output_fields"]


def test_task_1_test_plan_is_declared() -> None:
    tests = build_test_plan()

    assert len(tests) == 6
    assert [test["test_id"] for test in tests] == [
        "CTDP-T1",
        "CTDP-T2",
        "CTDP-T3",
        "CTDP-T4",
        "CTDP-T5",
        "CTDP-T6",
    ]


def test_task_1_boundary_blocks_implementation_runtime_eval_submission() -> None:
    controls = build_boundary_controls()

    assert controls["planning_only"] is True
    assert controls["implementation_authorized"] is False
    assert controls["runtime_activation_authorized"] is False
    assert controls["runtime_activation_performed"] is False
    assert controls["runtime_solver_modified"] is False
    assert controls["candidate_generator_modified"] is False
    assert controls["ranker_modified"] is False
    assert controls["verifier_modified"] is False
    assert controls["real_evaluation_authorized"] is False
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


def test_task_1_acceptance_and_signature_are_deterministic() -> None:
    first = build_cross_trace_diagnostic_planner_planning_intake()
    second = build_cross_trace_diagnostic_planner_planning_intake()

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["planning_intake_id"].endswith(first["signature"])
    assert first["acceptance_gate_count"] > 49
    assert first["acceptance_gate_failure_count"] == 0
    assert first["acceptance_gate_failures"] == []


def test_task_1_artifacts_are_written(tmp_path) -> None:
    paths = write_artifacts(
        artifact_dir=tmp_path / "examples" / "milestone-19" / "task-1",
        docs_path=tmp_path / "docs" / "task-1.md",
        index_path=tmp_path / "docs" / "milestone-19-index.md",
    )

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    docs = paths["docs"].read_text(encoding="utf-8")
    milestone_index = paths["milestone_index"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert "planning_only=true" in manifest
    assert "implementation_authorized=false" in manifest
    assert "runtime_solver_modified=false" in manifest
    assert "real_evaluation_performed=false" in manifest
    assert "kaggle_submission_sent=false" in manifest
    assert "operator_approval_required=true" in manifest
    assert "Cross-Trace Diagnostic Planner Planning Intake v1" in docs
    assert "Milestone 19" in milestone_index
