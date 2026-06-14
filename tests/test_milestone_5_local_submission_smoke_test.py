from pathlib import Path

from hbce_arc_agi3.milestone_5_local_submission_smoke_test import (
    CANDIDATE_KIND,
    EXPECTED_SUBMISSION_FILENAME,
    PIPELINE_STATUS,
    SMOKE_CASES,
    SMOKE_MODE,
    SMOKE_STATUS,
    VALIDATION_STATUS,
    build_local_smoke_cases,
    build_local_submission_candidate,
    build_local_submission_smoke_test,
    render_local_submission_smoke_manifest,
    render_local_submission_smoke_test_markdown,
    run_local_submission_smoke_test_pipeline,
    validate_local_submission_smoke_test,
    write_local_submission_smoke_test_artifacts,
)


def test_local_submission_smoke_test_ready():
    smoke_test = build_local_submission_smoke_test()

    assert smoke_test.status == SMOKE_STATUS
    assert smoke_test.baseline_commit.startswith("3c56cd7")
    assert smoke_test.smoke_mode == SMOKE_MODE
    assert smoke_test.candidate_kind == CANDIDATE_KIND
    assert smoke_test.expected_submission_filename == EXPECTED_SUBMISSION_FILENAME
    assert smoke_test.smoke_case_count == len(SMOKE_CASES)
    assert smoke_test.smoke_case_passed_count == len(SMOKE_CASES)
    assert smoke_test.candidate_task_count == len(SMOKE_CASES)
    assert smoke_test.ready_for_submission_candidate_format_report is True
    assert smoke_test.ready_for_real_kaggle_submission is False
    assert smoke_test.kaggle_submission_sent is False


def test_local_smoke_cases_pass():
    cases = build_local_smoke_cases()

    assert len(cases) == len(SMOKE_CASES)
    assert all(case.passed for case in cases)
    assert all(case.predicted_output_grid == case.expected_output_grid for case in cases)


def test_local_submission_candidate_is_smoke_only():
    cases = build_local_smoke_cases()
    candidate = build_local_submission_candidate(cases)

    assert candidate["candidate_kind"] == CANDIDATE_KIND
    assert candidate["submission_filename"] == EXPECTED_SUBMISSION_FILENAME
    assert candidate["submission_mode"] == SMOKE_MODE
    assert candidate["kaggle_submission_sent"] is False
    assert len(candidate["tasks"]) == len(SMOKE_CASES)
    assert candidate["metadata"]["external_api_dependency"] is False
    assert candidate["metadata"]["contains_api_keys"] is False
    assert candidate["metadata"]["private_core_exposure"] is False
    assert candidate["metadata"]["legal_certification"] is False


def test_local_submission_smoke_test_validation_passes():
    smoke_test = build_local_submission_smoke_test()
    validation = validate_local_submission_smoke_test(smoke_test)

    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_local_submission_smoke_test_pipeline_ready():
    payload = run_local_submission_smoke_test_pipeline()

    assert payload["status"] == PIPELINE_STATUS
    assert payload["smoke_status"] == SMOKE_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["smoke_case_count"] == len(SMOKE_CASES)
    assert payload["smoke_case_passed_count"] == len(SMOKE_CASES)
    assert payload["candidate_task_count"] == len(SMOKE_CASES)
    assert payload["ready_for_submission_candidate_format_report"] is True
    assert payload["ready_for_real_kaggle_submission"] is False
    assert payload["kaggle_submission_sent"] is False


def test_local_submission_smoke_test_markdown_contains_markers():
    smoke_test = build_local_submission_smoke_test()
    markdown = render_local_submission_smoke_test_markdown(smoke_test)

    assert "ARC_AGI3_MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_LOCAL_SMOKE_ONLY_NO_UPLOAD=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_EXPECTED_SUBMISSION_FILENAME=submission.json" in markdown
    assert "ARC_AGI3_MILESTONE_5_SMOKE_CASE_COUNT=3" in markdown
    assert "ARC_AGI3_MILESTONE_5_SMOKE_CASE_PASSED_COUNT=3" in markdown
    assert "ARC_AGI3_MILESTONE_5_CANDIDATE_TASK_COUNT=3" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_FOR_SUBMISSION_CANDIDATE_FORMAT_REPORT=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_FOR_REAL_KAGGLE_SUBMISSION=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_local_submission_smoke_manifest_contains_boundary():
    smoke_test = build_local_submission_smoke_test()
    manifest = render_local_submission_smoke_manifest(smoke_test)

    assert "ARC AGI3 LOCAL SUBMISSION SMOKE TEST MANIFEST v1" in manifest
    assert "smoke_mode=LOCAL_SMOKE_ONLY_NO_UPLOAD" in manifest
    assert "expected_submission_filename=submission.json" in manifest
    assert "ready_for_submission_candidate_format_report=True" in manifest
    assert "ready_for_real_kaggle_submission=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "external_api_dependency=false" in manifest
    assert "private_core_exposure=false" in manifest
    assert "legal_certification=false" in manifest


def test_local_submission_smoke_test_writes_artifacts(tmp_path: Path):
    smoke_test = build_local_submission_smoke_test()
    paths = write_local_submission_smoke_test_artifacts(
        smoke_test,
        output_dir=str(tmp_path),
    )

    json_path = Path(paths["json_path"])
    markdown_path = Path(paths["markdown_path"])
    manifest_path = Path(paths["manifest_path"])
    candidate_path = Path(paths["candidate_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert manifest_path.exists()
    assert candidate_path.exists()
    assert "MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_READY" in json_path.read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_V1_READY=true" in markdown_path.read_text(encoding="utf-8")
    assert "ARC AGI3 LOCAL SUBMISSION SMOKE TEST MANIFEST v1" in manifest_path.read_text(encoding="utf-8")
    assert "LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY" in candidate_path.read_text(encoding="utf-8")


def test_local_submission_candidate_tasks_are_stable():
    smoke_test = build_local_submission_smoke_test()
    task_ids = [task["task_id"] for task in smoke_test.local_submission_candidate["tasks"]]

    assert task_ids == [
        "SMOKE-TASK-IDENTITY-2X2",
        "SMOKE-TASK-COLOR-REMAP-2X2",
        "SMOKE-TASK-OBJECT-FILL-3X3",
    ]
