from pathlib import Path

from hbce_arc_agi3.milestone_14_local_solver_controlled_runtime_integration_planning import (
    NEXT_STAGE,
    PLANNING_VERDICT,
    TASK_NAME,
    build_milestone_14_planning_record,
    build_planning_gate_map,
    review_milestone_13_closure_artifact,
    validate_milestone_14_planning_record,
    write_artifacts,
)


def test_milestone_13_closure_artifact_passes():
    review = review_milestone_13_closure_artifact()

    assert review["milestone_13_closure_artifact_present"] is True
    assert review["milestone_13_closure_artifact_parseable"] is True
    assert review["milestone_13_closure_valid"] is True


def test_planning_gate_map_passes():
    source = review_milestone_13_closure_artifact()["source_record"]
    gates = build_planning_gate_map(source)

    assert len(gates) == 15
    assert all(gates.values())


def test_milestone_14_planning_record_is_valid():
    record = build_milestone_14_planning_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["planning_verdict"] == PLANNING_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["milestone_14_opened"] is True
    assert record["milestone_14_planning_ready"] is True
    assert record["ready_for_plan_review"] is True
    assert record["runtime_candidate_count"] == 4
    assert record["candidate_fixture_matrix_count"] == 12
    assert record["diagnostic_average_score"] == 0.6875
    assert record["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert record["planning_only"] is True
    assert record["runtime_activation_performed"] is False
    assert record["runtime_execution_performed"] is False
    assert record["implementation_performed"] is False
    assert record["real_submission_allowed"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert validate_milestone_14_planning_record(record) == []


def test_milestone_14_validation_fails_if_not_opened():
    record = build_milestone_14_planning_record(baseline_commit="TEST-COMMIT")
    record["milestone_14_opened"] = False

    issues = validate_milestone_14_planning_record(record)

    assert "milestone_14_opened_NOT_TRUE" in issues


def test_milestone_14_validation_fails_if_runtime_execution_performed():
    record = build_milestone_14_planning_record(baseline_commit="TEST-COMMIT")
    record["runtime_execution_performed"] = True

    issues = validate_milestone_14_planning_record(record)

    assert "runtime_execution_performed_NOT_FALSE" in issues


def test_milestone_14_validation_fails_if_implementation_performed():
    record = build_milestone_14_planning_record(baseline_commit="TEST-COMMIT")
    record["implementation_performed"] = True

    issues = validate_milestone_14_planning_record(record)

    assert "implementation_performed_NOT_FALSE" in issues


def test_milestone_14_validation_fails_if_submission_sent():
    record = build_milestone_14_planning_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_milestone_14_planning_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_milestone_14_validation_fails_if_kaggle_score_semantics_removed():
    record = build_milestone_14_planning_record(baseline_commit="TEST-COMMIT")
    record["kaggle_score_semantics"] = "KAGGLE_SCORE"

    issues = validate_milestone_14_planning_record(record)

    assert "KAGGLE_SCORE_SEMANTICS_MISMATCH" in issues


def test_milestone_14_artifacts_are_written(tmp_path: Path):
    record = build_milestone_14_planning_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-14-local-solver-controlled-runtime-integration-planning-v1.json" in written_files
    assert "milestone-14-local-solver-controlled-runtime-integration-planning-index-v1.json" in written_files
    assert "milestone-14-local-solver-controlled-runtime-integration-planning-manifest-v1.txt" in written_files
    assert "milestone-14-local-solver-controlled-runtime-integration-planning-v1.md" in written_files
