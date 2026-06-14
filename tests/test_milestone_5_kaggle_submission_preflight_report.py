from pathlib import Path

from hbce_arc_agi3.milestone_5_kaggle_submission_preflight_report import (
    BLOCKING_ISSUE_NAMES,
    PREFLIGHT_GATES,
    REPORT_STATUS,
    PIPELINE_STATUS,
    REQUIRED_PREFLIGHT_SOURCES,
    VALIDATION_STATUS,
    build_blocking_issues,
    build_kaggle_submission_preflight_report,
    build_preflight_gates,
    build_preflight_source_statuses,
    render_kaggle_submission_preflight_manifest,
    render_kaggle_submission_preflight_report_markdown,
    run_kaggle_submission_preflight_report_pipeline,
    validate_kaggle_submission_preflight_report,
    write_kaggle_submission_preflight_report_artifacts,
)


def test_kaggle_submission_preflight_report_ready():
    report = build_kaggle_submission_preflight_report()

    assert report.status == REPORT_STATUS
    assert report.baseline_commit.startswith("9c3c7e2")
    assert report.required_source_count == len(REQUIRED_PREFLIGHT_SOURCES)
    assert report.ready_source_count == len(REQUIRED_PREFLIGHT_SOURCES)
    assert report.preflight_gate_count == len(PREFLIGHT_GATES)
    assert report.passed_gate_count == len(PREFLIGHT_GATES)
    assert report.blocking_issue_count == 0
    assert report.warning_count == 0
    assert report.ready_for_local_submission_smoke_test is True
    assert report.ready_for_submission_candidate_format_report is True
    assert report.ready_for_real_kaggle_submission is False
    assert report.kaggle_submission_sent is False


def test_preflight_source_statuses_are_ready():
    statuses = build_preflight_source_statuses()

    assert len(statuses) == len(REQUIRED_PREFLIGHT_SOURCES)
    assert all(status.present for status in statuses)
    assert all(status.ready for status in statuses)


def test_preflight_gates_pass():
    report = build_kaggle_submission_preflight_report()

    assert [gate.name for gate in report.preflight_gates] == list(PREFLIGHT_GATES)
    assert all(gate.passed for gate in report.preflight_gates)
    assert all(gate.severity == "PASS" for gate in report.preflight_gates)


def test_preflight_blocking_issues_are_inactive():
    report = build_kaggle_submission_preflight_report()

    assert [issue.name for issue in report.blocking_issues] == list(BLOCKING_ISSUE_NAMES)
    assert all(issue.active is False for issue in report.blocking_issues)
    assert all(issue.severity == "BLOCKING" for issue in report.blocking_issues)


def test_kaggle_submission_preflight_report_validation_passes():
    report = build_kaggle_submission_preflight_report()
    validation = validate_kaggle_submission_preflight_report(report)

    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_kaggle_submission_preflight_report_pipeline_ready():
    payload = run_kaggle_submission_preflight_report_pipeline()

    assert payload["status"] == PIPELINE_STATUS
    assert payload["report_status"] == REPORT_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["required_source_count"] == len(REQUIRED_PREFLIGHT_SOURCES)
    assert payload["ready_source_count"] == len(REQUIRED_PREFLIGHT_SOURCES)
    assert payload["blocking_issue_count"] == 0
    assert payload["warning_count"] == 0
    assert payload["ready_for_local_submission_smoke_test"] is True
    assert payload["ready_for_real_kaggle_submission"] is False
    assert payload["kaggle_submission_sent"] is False


def test_kaggle_submission_preflight_report_markdown_contains_markers():
    report = build_kaggle_submission_preflight_report()
    markdown = render_kaggle_submission_preflight_report_markdown(report)

    assert "ARC_AGI3_MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_PREFLIGHT_REQUIRED_SOURCE_COUNT=5" in markdown
    assert "ARC_AGI3_MILESTONE_5_PREFLIGHT_READY_SOURCE_COUNT=5" in markdown
    assert "ARC_AGI3_MILESTONE_5_PREFLIGHT_GATE_COUNT=12" in markdown
    assert "ARC_AGI3_MILESTONE_5_PREFLIGHT_BLOCKING_ISSUE_COUNT=0" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_FOR_LOCAL_SUBMISSION_SMOKE_TEST=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_FOR_REAL_KAGGLE_SUBMISSION=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_kaggle_submission_preflight_manifest_contains_boundary():
    report = build_kaggle_submission_preflight_report()
    manifest = render_kaggle_submission_preflight_manifest(report)

    assert "ARC AGI3 KAGGLE SUBMISSION PREFLIGHT REPORT MANIFEST v1" in manifest
    assert "ready_for_local_submission_smoke_test=True" in manifest
    assert "ready_for_real_kaggle_submission=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "blocking_issue_count=0" in manifest
    assert "external_api_dependency=false" in manifest
    assert "private_core_exposure=false" in manifest
    assert "legal_certification=false" in manifest


def test_kaggle_submission_preflight_report_writes_artifacts(tmp_path: Path):
    report = build_kaggle_submission_preflight_report()
    paths = write_kaggle_submission_preflight_report_artifacts(
        report,
        output_dir=str(tmp_path),
    )

    json_path = Path(paths["json_path"])
    markdown_path = Path(paths["markdown_path"])
    manifest_path = Path(paths["manifest_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert manifest_path.exists()
    assert "MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_READY" in json_path.read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_V1_READY=true" in markdown_path.read_text(encoding="utf-8")
    assert "ARC AGI3 KAGGLE SUBMISSION PREFLIGHT REPORT MANIFEST v1" in manifest_path.read_text(encoding="utf-8")
