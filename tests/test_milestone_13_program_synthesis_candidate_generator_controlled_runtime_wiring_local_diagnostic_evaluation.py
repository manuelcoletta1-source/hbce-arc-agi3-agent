from pathlib import Path

from hbce_arc_agi3.milestone_13_program_synthesis_candidate_generator_controlled_runtime_wiring_local_diagnostic_evaluation import (
    NEXT_STAGE,
    TASK_NAME,
    build_local_diagnostic_evaluation_record,
    run_local_diagnostic_evaluation,
    score_diagnostic_row,
    validate_local_diagnostic_evaluation_record,
    write_artifacts,
)


def test_score_diagnostic_row_passes_without_runtime_execution():
    row = {
        "candidate_id": "CANDIDATE-1",
        "candidate_family": "color_mapping",
        "candidate_operation": "map",
        "fixture_id": "FIXTURE-1",
        "fixture_family": "color_mapping",
    }

    scored = score_diagnostic_row(row)

    assert scored["diagnostic_pass"] is True
    assert scored["diagnostic_score"] == 1.0
    assert scored["runtime_execution_performed"] is False
    assert scored["real_evaluation_performed"] is False
    assert scored["diagnostic_only"] is True


def test_local_diagnostic_evaluation_has_expected_counts_and_boundaries():
    evaluation = run_local_diagnostic_evaluation()

    assert evaluation["runtime_candidate_count"] == 4
    assert evaluation["candidate_fixture_matrix_count"] == 12
    assert evaluation["diagnostic_case_count"] == 12
    assert evaluation["diagnostic_pass_count"] == 12
    assert evaluation["diagnostic_failure_count"] == 0
    assert evaluation["diagnostic_average_score"] >= 0.5
    assert evaluation["local_diagnostic_evaluation_performed"] is True
    assert evaluation["diagnostic_only"] is True
    assert evaluation["runtime_activation_performed"] is False
    assert evaluation["runtime_execution_performed"] is False
    assert evaluation["real_evaluation_performed"] is False
    assert evaluation["kaggle_submission_sent"] is False


def test_task16_record_is_valid():
    record = build_local_diagnostic_evaluation_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["next_stage"] == NEXT_STAGE
    assert record["source_review_passed"] is True
    assert record["local_diagnostic_evaluation_performed"] is True
    assert record["ready_for_local_diagnostic_evaluation_review"] is True
    assert record["diagnostic_case_count"] == 12
    assert record["diagnostic_pass_count"] == 12
    assert record["diagnostic_failure_count"] == 0
    assert record["runtime_activation_performed"] is False
    assert record["runtime_execution_performed"] is False
    assert record["real_submission_allowed"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert validate_local_diagnostic_evaluation_record(record) == []


def test_task16_validation_fails_if_runtime_execution_performed():
    record = build_local_diagnostic_evaluation_record(baseline_commit="TEST-COMMIT")
    record["runtime_execution_performed"] = True

    issues = validate_local_diagnostic_evaluation_record(record)

    assert "runtime_execution_performed_NOT_FALSE" in issues


def test_task16_validation_fails_if_kaggle_submission_sent():
    record = build_local_diagnostic_evaluation_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_local_diagnostic_evaluation_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_task16_validation_fails_if_diagnostic_failure_count_changes():
    record = build_local_diagnostic_evaluation_record(baseline_commit="TEST-COMMIT")
    record["diagnostic_failure_count"] = 1

    issues = validate_local_diagnostic_evaluation_record(record)

    assert "DIAGNOSTIC_FAILURE_COUNT_MISMATCH" in issues


def test_task16_artifacts_are_written(tmp_path: Path):
    record = build_local_diagnostic_evaluation_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-index-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-manifest-v1.txt" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-v1.md" in written_files
