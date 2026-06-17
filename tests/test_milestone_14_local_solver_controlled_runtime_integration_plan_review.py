from pathlib import Path

from hbce_arc_agi3.milestone_14_local_solver_controlled_runtime_integration_plan_review import (
    NEXT_STAGE,
    REVIEW_VERDICT,
    TASK_NAME,
    build_plan_review_record,
    build_review_gate_map,
    review_source_planning_artifact,
    validate_plan_review_record,
    write_artifacts,
)


def test_source_planning_artifact_passes():
    review = review_source_planning_artifact()

    assert review["source_planning_artifact_present"] is True
    assert review["source_planning_artifact_parseable"] is True
    assert review["source_planning_artifact_valid"] is True


def test_review_gate_map_passes():
    source = review_source_planning_artifact()["source_record"]
    gates = build_review_gate_map(source)

    assert len(gates) == 22
    assert all(gates.values())


def test_plan_review_record_is_valid():
    record = build_plan_review_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["review_verdict"] == REVIEW_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["plan_review_passed"] is True
    assert record["ready_for_implementation_plan"] is True
    assert record["runtime_candidate_count"] == 4
    assert record["candidate_fixture_matrix_count"] == 12
    assert record["diagnostic_average_score"] == 0.6875
    assert record["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert record["review_only"] is True
    assert record["runtime_activation_performed"] is False
    assert record["runtime_execution_performed"] is False
    assert record["implementation_performed"] is False
    assert record["real_submission_allowed"] is False
    assert validate_plan_review_record(record) == []


def test_plan_review_validation_fails_if_review_not_passed():
    record = build_plan_review_record(baseline_commit="TEST-COMMIT")
    record["plan_review_passed"] = False

    issues = validate_plan_review_record(record)

    assert "plan_review_passed_NOT_TRUE" in issues


def test_plan_review_validation_fails_if_runtime_execution_performed():
    record = build_plan_review_record(baseline_commit="TEST-COMMIT")
    record["runtime_execution_performed"] = True

    issues = validate_plan_review_record(record)

    assert "runtime_execution_performed_NOT_FALSE" in issues


def test_plan_review_validation_fails_if_implementation_performed():
    record = build_plan_review_record(baseline_commit="TEST-COMMIT")
    record["implementation_performed"] = True

    issues = validate_plan_review_record(record)

    assert "implementation_performed_NOT_FALSE" in issues


def test_plan_review_validation_fails_if_submission_sent():
    record = build_plan_review_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_plan_review_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_plan_review_validation_fails_if_kaggle_score_semantics_removed():
    record = build_plan_review_record(baseline_commit="TEST-COMMIT")
    record["kaggle_score_semantics"] = "KAGGLE_SCORE"

    issues = validate_plan_review_record(record)

    assert "KAGGLE_SCORE_SEMANTICS_MISMATCH" in issues


def test_plan_review_artifacts_are_written(tmp_path: Path):
    record = build_plan_review_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-14-local-solver-controlled-runtime-integration-plan-review-v1.json" in written_files
    assert "milestone-14-local-solver-controlled-runtime-integration-plan-review-index-v1.json" in written_files
    assert "milestone-14-local-solver-controlled-runtime-integration-plan-review-manifest-v1.txt" in written_files
    assert "milestone-14-local-solver-controlled-runtime-integration-plan-review-v1.md" in written_files
