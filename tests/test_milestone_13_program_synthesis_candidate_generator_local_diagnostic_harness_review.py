from pathlib import Path

from hbce_arc_agi3.milestone_13_program_synthesis_candidate_generator_local_diagnostic_harness_review import (
    NEXT_STAGE,
    REVIEW_VERDICT,
    TASK_NAME,
    TASK_VERDICT,
    build_harness_review_report,
    build_local_diagnostic_harness_review_record,
    review_candidate_fixture_matrix,
    validate_local_diagnostic_harness_review_record,
    write_artifacts,
)


def _matrix_row(index: int):
    return {
        "fixture_id": f"DIAG-FIXTURE-{index:03d}",
        "fixture_name": f"fixture_{index}",
        "required_family": "primitive_sequence_candidates",
        "matching_candidate_count": 1,
        "observation_passed": True,
        "runtime_execution_performed": False,
        "real_evaluation_performed": False,
        "public_safe": True,
    }


def test_local_diagnostic_harness_review_record_is_valid():
    record = build_local_diagnostic_harness_review_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["review_verdict"] == REVIEW_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["source_harness_ready"] is True
    assert record["source_harness_shape_ok"] is True
    assert record["local_diagnostic_harness_review_ready"] is True
    assert record["local_diagnostic_harness_review_valid"] is True
    assert record["local_diagnostic_harness_review_passed"] is True
    assert record["runtime_wiring_plan_authorized"] is True
    assert record["candidate_count"] == 12
    assert record["candidate_family_count"] == 7
    assert record["diagnostic_fixture_count"] == 4
    assert record["candidate_fixture_matrix_count"] == 4
    assert record["blocking_issue_count"] == 0
    assert record["runtime_execution_performed"] is False
    assert record["candidate_generator_wiring_authorized"] is False
    assert record["runtime_wiring_authorized"] is False
    assert record["runtime_solver_modified"] is False
    assert record["candidate_generator_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert validate_local_diagnostic_harness_review_record(record) == []


def test_review_candidate_fixture_matrix_passes_for_good_matrix():
    matrix = [_matrix_row(index) for index in range(1, 5)]
    review = review_candidate_fixture_matrix(matrix)

    assert review["candidate_fixture_matrix_count"] == 4
    assert review["fixture_ids_unique"] is True
    assert review["all_observations_passed"] is True
    assert review["all_matching_counts_positive"] is True
    assert review["all_runtime_execution_blocked"] is True
    assert review["all_real_evaluation_blocked"] is True
    assert review["all_public_safe"] is True


def test_review_candidate_fixture_matrix_detects_runtime_execution():
    matrix = [_matrix_row(index) for index in range(1, 5)]
    matrix[0]["runtime_execution_performed"] = True

    review = review_candidate_fixture_matrix(matrix)

    assert review["all_runtime_execution_blocked"] is False


def test_harness_review_report_passes_for_good_source_record():
    source_record = {
        "local_diagnostic_harness_ready": True,
        "local_diagnostic_harness_passed": True,
        "candidate_count": 12,
        "candidate_family_count": 7,
        "diagnostic_fixture_count": 4,
        "candidate_fixture_matrix": [_matrix_row(index) for index in range(1, 5)],
        "blocking_issue_count": 0,
        "runtime_execution_performed": False,
        "candidate_generator_wiring_authorized": False,
        "runtime_wiring_authorized": False,
        "runtime_solver_modified": False,
        "candidate_generator_modified": False,
        "ranker_runtime_modified": False,
        "real_evaluation_performed": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_upload_allowed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    report = build_harness_review_report(source_record)

    assert report["review_passed"] is True
    assert report["blocking_issue_count"] == 0
    assert report["recommended_next_stage"] == NEXT_STAGE


def test_harness_review_report_fails_for_bad_source_record():
    source_record = {
        "local_diagnostic_harness_ready": True,
        "local_diagnostic_harness_passed": True,
        "candidate_count": 12,
        "candidate_family_count": 7,
        "diagnostic_fixture_count": 4,
        "candidate_fixture_matrix": [_matrix_row(index) for index in range(1, 5)],
        "blocking_issue_count": 0,
        "runtime_execution_performed": True,
        "candidate_generator_wiring_authorized": False,
        "runtime_wiring_authorized": False,
        "runtime_solver_modified": False,
        "candidate_generator_modified": False,
        "ranker_runtime_modified": False,
        "real_evaluation_performed": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_upload_allowed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    report = build_harness_review_report(source_record)

    assert report["review_passed"] is False
    assert "runtime_execution_performed_false" in report["blocking_issues"]


def test_local_diagnostic_harness_review_fails_if_runtime_wiring_mutated():
    record = build_local_diagnostic_harness_review_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_authorized"] = True

    issues = validate_local_diagnostic_harness_review_record(record)

    assert "runtime_wiring_authorized_NOT_FALSE" in issues


def test_local_diagnostic_harness_review_artifacts_are_written(tmp_path: Path):
    record = build_local_diagnostic_harness_review_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-review-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-review-index-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-review-manifest-v1.txt" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-review-v1.md" in written_files
