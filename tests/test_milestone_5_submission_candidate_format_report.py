from pathlib import Path

from hbce_arc_agi3.milestone_5_submission_candidate_format_report import (
    EXPECTED_CANDIDATE_KIND,
    EXPECTED_SUBMISSION_FILENAME,
    EXPECTED_SUBMISSION_MODE,
    FORMAT_GATES,
    FORMAT_ISSUES,
    PIPELINE_STATUS,
    REPORT_STATUS,
    VALIDATION_STATUS,
    build_candidate_task_format_statuses,
    build_submission_candidate_format_report,
    is_valid_candidate_task,
    is_valid_grid,
    render_submission_candidate_format_manifest,
    render_submission_candidate_format_report_markdown,
    run_submission_candidate_format_report_pipeline,
    validate_submission_candidate_format_report,
    write_submission_candidate_format_report_artifacts,
)


def test_submission_candidate_format_report_ready():
    report = build_submission_candidate_format_report()

    assert report.status == REPORT_STATUS
    assert report.baseline_commit.startswith("47d47d2")
    assert report.candidate_kind == EXPECTED_CANDIDATE_KIND
    assert report.submission_filename == EXPECTED_SUBMISSION_FILENAME
    assert report.submission_mode == EXPECTED_SUBMISSION_MODE
    assert report.candidate_task_count == 3
    assert report.valid_task_count == 3
    assert report.format_gate_count == len(FORMAT_GATES)
    assert report.passed_gate_count == len(FORMAT_GATES)
    assert report.format_issue_count == 0
    assert report.warning_count == 0
    assert report.ready_for_submission_candidate_dry_run is True
    assert report.ready_for_milestone_5_closure is True
    assert report.ready_for_real_kaggle_submission is False
    assert report.kaggle_submission_sent is False


def test_candidate_grid_validator_accepts_valid_grid():
    assert is_valid_grid([[0, 1], [2, 3]]) is True
    assert is_valid_grid([[9]]) is True


def test_candidate_grid_validator_rejects_invalid_grid():
    assert is_valid_grid([]) is False
    assert is_valid_grid([[]]) is False
    assert is_valid_grid([[1], [1, 2]]) is False
    assert is_valid_grid([[10]]) is False
    assert is_valid_grid([[True]]) is False
    assert is_valid_grid("not-a-grid") is False


def test_candidate_task_validator_accepts_valid_task():
    task = {
        "task_id": "TASK-1",
        "attempt_1": [[1, 2], [3, 4]],
        "attempt_2": [[1, 2], [3, 4]],
    }

    assert is_valid_candidate_task(task) is True


def test_candidate_task_validator_rejects_invalid_task():
    assert is_valid_candidate_task({"task_id": "", "attempt_1": [[1]], "attempt_2": [[1]]}) is False
    assert is_valid_candidate_task({"task_id": "TASK-1", "attempt_1": [[1]]}) is False
    assert is_valid_candidate_task({"task_id": "TASK-1", "attempt_1": [[1]], "attempt_2": [[99]]}) is False


def test_candidate_task_format_statuses_are_valid():
    report = build_submission_candidate_format_report()

    assert len(report.task_format_statuses) == 3
    assert all(status.valid for status in report.task_format_statuses)
    assert all(status.has_task_id for status in report.task_format_statuses)
    assert all(status.has_attempt_1 for status in report.task_format_statuses)
    assert all(status.has_attempt_2 for status in report.task_format_statuses)


def test_submission_candidate_format_report_validation_passes():
    report = build_submission_candidate_format_report()
    validation = validate_submission_candidate_format_report(report)

    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_submission_candidate_format_report_pipeline_ready():
    payload = run_submission_candidate_format_report_pipeline()

    assert payload["status"] == PIPELINE_STATUS
    assert payload["report_status"] == REPORT_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["candidate_task_count"] == 3
    assert payload["valid_task_count"] == 3
    assert payload["format_gate_count"] == len(FORMAT_GATES)
    assert payload["passed_gate_count"] == len(FORMAT_GATES)
    assert payload["format_issue_count"] == 0
    assert payload["warning_count"] == 0
    assert payload["ready_for_submission_candidate_dry_run"] is True
    assert payload["ready_for_real_kaggle_submission"] is False
    assert payload["kaggle_submission_sent"] is False


def test_submission_candidate_format_report_markdown_contains_markers():
    report = build_submission_candidate_format_report()
    markdown = render_submission_candidate_format_report_markdown(report)

    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_FILENAME=submission.json" in markdown
    assert "ARC_AGI3_MILESTONE_5_CANDIDATE_KIND=LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY" in markdown
    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_MODE=LOCAL_SMOKE_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_5_CANDIDATE_TASK_COUNT=3" in markdown
    assert "ARC_AGI3_MILESTONE_5_VALID_TASK_COUNT=3" in markdown
    assert "ARC_AGI3_MILESTONE_5_FORMAT_GATE_COUNT=14" in markdown
    assert "ARC_AGI3_MILESTONE_5_FORMAT_ISSUE_COUNT=0" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_FOR_SUBMISSION_CANDIDATE_DRY_RUN=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_FOR_REAL_KAGGLE_SUBMISSION=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_submission_candidate_format_manifest_contains_boundary():
    report = build_submission_candidate_format_report()
    manifest = render_submission_candidate_format_manifest(report)

    assert "ARC AGI3 SUBMISSION CANDIDATE FORMAT REPORT MANIFEST v1" in manifest
    assert "submission_filename=submission.json" in manifest
    assert "submission_mode=LOCAL_SMOKE_ONLY_NO_UPLOAD" in manifest
    assert "candidate_task_count=3" in manifest
    assert "valid_task_count=3" in manifest
    assert "format_issue_count=0" in manifest
    assert "ready_for_submission_candidate_dry_run=True" in manifest
    assert "ready_for_real_kaggle_submission=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "external_api_dependency=false" in manifest
    assert "private_core_exposure=false" in manifest
    assert "legal_certification=false" in manifest


def test_submission_candidate_format_report_writes_artifacts(tmp_path: Path):
    report = build_submission_candidate_format_report()
    paths = write_submission_candidate_format_report_artifacts(
        report,
        output_dir=str(tmp_path),
    )

    json_path = Path(paths["json_path"])
    markdown_path = Path(paths["markdown_path"])
    manifest_path = Path(paths["manifest_path"])
    preview_path = Path(paths["preview_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert manifest_path.exists()
    assert preview_path.exists()
    assert "MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_READY" in json_path.read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_V1_READY=true" in markdown_path.read_text(encoding="utf-8")
    assert "ARC AGI3 SUBMISSION CANDIDATE FORMAT REPORT MANIFEST v1" in manifest_path.read_text(encoding="utf-8")
    assert "LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY" in preview_path.read_text(encoding="utf-8")


def test_build_candidate_task_format_statuses_handles_bad_tasks():
    statuses = build_candidate_task_format_statuses(
        {
            "tasks": [
                {"task_id": "", "attempt_1": [[1]], "attempt_2": [[1]]},
                {"task_id": "TASK-2", "attempt_1": [[1]]},
            ]
        }
    )

    assert len(statuses) == 2
    assert statuses[0].valid is False
    assert statuses[1].valid is False
