from pathlib import Path

from hbce_arc_agi3.milestone_14_local_solver_controlled_runtime_integration_implementation_plan import (
    IMPLEMENTATION_PLAN_VERDICT,
    NEXT_STAGE,
    TASK_NAME,
    build_implementation_plan_gate_map,
    build_implementation_plan_record,
    review_source_plan_review_artifact,
    validate_implementation_plan_record,
    write_artifacts,
)


def test_source_plan_review_artifact_passes():
    review = review_source_plan_review_artifact()

    assert review["source_plan_review_artifact_present"] is True
    assert review["source_plan_review_artifact_parseable"] is True
    assert review["source_plan_review_valid"] is True


def test_implementation_plan_gate_map_passes():
    source = review_source_plan_review_artifact()["source_record"]
    gates = build_implementation_plan_gate_map(source)

    assert len(gates) == 15
    assert all(gates.values())


def test_implementation_plan_record_is_valid():
    record = build_implementation_plan_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["implementation_plan_verdict"] == IMPLEMENTATION_PLAN_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["implementation_plan_passed"] is True
    assert record["ready_for_implementation_plan_review"] is True
    assert record["target_module_count"] == 5
    assert record["implementation_step_count"] == 10
    assert record["integration_contract_count"] == 8
    assert record["regression_test_count"] == 8
    assert record["rollback_item_count"] == 5
    assert record["review_gate_count"] == 11
    assert record["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert record["implementation_plan_only"] is True
    assert record["runtime_activation_performed"] is False
    assert record["runtime_execution_performed"] is False
    assert record["implementation_performed"] is False
    assert record["real_submission_allowed"] is False
    assert validate_implementation_plan_record(record) == []


def test_validation_fails_if_implementation_plan_not_passed():
    record = build_implementation_plan_record(baseline_commit="TEST-COMMIT")
    record["implementation_plan_passed"] = False

    issues = validate_implementation_plan_record(record)

    assert "implementation_plan_passed_NOT_TRUE" in issues


def test_validation_fails_if_runtime_execution_performed():
    record = build_implementation_plan_record(baseline_commit="TEST-COMMIT")
    record["runtime_execution_performed"] = True

    issues = validate_implementation_plan_record(record)

    assert "runtime_execution_performed_NOT_FALSE" in issues


def test_validation_fails_if_implementation_performed():
    record = build_implementation_plan_record(baseline_commit="TEST-COMMIT")
    record["implementation_performed"] = True

    issues = validate_implementation_plan_record(record)

    assert "implementation_performed_NOT_FALSE" in issues


def test_validation_fails_if_submission_sent():
    record = build_implementation_plan_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_implementation_plan_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_validation_fails_if_kaggle_score_semantics_removed():
    record = build_implementation_plan_record(baseline_commit="TEST-COMMIT")
    record["kaggle_score_semantics"] = "KAGGLE_SCORE"

    issues = validate_implementation_plan_record(record)

    assert "KAGGLE_SCORE_SEMANTICS_MISMATCH" in issues


def test_implementation_plan_artifacts_are_written(tmp_path: Path):
    record = build_implementation_plan_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-14-local-solver-controlled-runtime-integration-implementation-plan-v1.json" in written_files
    assert "milestone-14-local-solver-controlled-runtime-integration-implementation-plan-index-v1.json" in written_files
    assert "milestone-14-local-solver-controlled-runtime-integration-implementation-plan-manifest-v1.txt" in written_files
    assert "milestone-14-local-solver-controlled-runtime-integration-implementation-plan-v1.md" in written_files
