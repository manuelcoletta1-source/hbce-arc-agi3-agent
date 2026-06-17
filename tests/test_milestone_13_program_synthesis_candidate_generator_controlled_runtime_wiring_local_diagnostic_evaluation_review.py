from pathlib import Path

from hbce_arc_agi3.milestone_13_program_synthesis_candidate_generator_controlled_runtime_wiring_local_diagnostic_evaluation_review import (
    NEXT_STAGE,
    TASK_NAME,
    build_local_diagnostic_evaluation_review_record,
    review_diagnostic_cases,
    review_source_evaluation_artifact,
    validate_local_diagnostic_evaluation_review_record,
    write_artifacts,
)


def test_source_evaluation_artifact_review_passes():
    review = review_source_evaluation_artifact()

    assert review["source_artifact_present"] is True
    assert review["source_artifact_parseable"] is True
    assert review["source_evaluation_passed"] is True


def test_diagnostic_cases_review_passes():
    source = review_source_evaluation_artifact()["source_record"]
    review = review_diagnostic_cases(source)

    assert review["diagnostic_case_count"] == 12
    assert review["diagnostic_pass_count"] == 12
    assert review["diagnostic_failure_count"] == 0
    assert review["diagnostic_average_score"] == 0.6875
    assert review["all_cases_passed"] is True
    assert review["all_cases_diagnostic_only"] is True
    assert review["all_cases_runtime_execution_false"] is True
    assert review["all_cases_real_evaluation_false"] is True


def test_task17_review_record_is_valid():
    record = build_local_diagnostic_evaluation_review_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["next_stage"] == NEXT_STAGE
    assert record["local_diagnostic_evaluation_review_passed"] is True
    assert record["ready_for_local_diagnostic_evaluation_closure"] is True
    assert record["runtime_candidate_count"] == 4
    assert record["candidate_fixture_matrix_count"] == 12
    assert record["diagnostic_case_count"] == 12
    assert record["diagnostic_pass_count"] == 12
    assert record["diagnostic_failure_count"] == 0
    assert record["diagnostic_average_score"] == 0.6875
    assert record["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert record["runtime_activation_performed"] is False
    assert record["runtime_execution_performed"] is False
    assert record["real_submission_allowed"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert validate_local_diagnostic_evaluation_review_record(record) == []


def test_task17_validation_fails_if_runtime_execution_performed():
    record = build_local_diagnostic_evaluation_review_record(baseline_commit="TEST-COMMIT")
    record["runtime_execution_performed"] = True

    issues = validate_local_diagnostic_evaluation_review_record(record)

    assert "runtime_execution_performed_NOT_FALSE" in issues


def test_task17_validation_fails_if_kaggle_submission_sent():
    record = build_local_diagnostic_evaluation_review_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_local_diagnostic_evaluation_review_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_task17_validation_fails_if_score_is_changed():
    record = build_local_diagnostic_evaluation_review_record(baseline_commit="TEST-COMMIT")
    record["diagnostic_average_score"] = 0.1

    issues = validate_local_diagnostic_evaluation_review_record(record)

    assert "DIAGNOSTIC_AVERAGE_SCORE_MISMATCH" in issues


def test_task17_validation_fails_if_kaggle_score_semantics_removed():
    record = build_local_diagnostic_evaluation_review_record(baseline_commit="TEST-COMMIT")
    record["kaggle_score_semantics"] = "KAGGLE_SCORE"

    issues = validate_local_diagnostic_evaluation_review_record(record)

    assert "KAGGLE_SCORE_SEMANTICS_MISMATCH" in issues


def test_task17_artifacts_are_written(tmp_path: Path):
    record = build_local_diagnostic_evaluation_review_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-review-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-review-index-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-review-manifest-v1.txt" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-review-v1.md" in written_files
