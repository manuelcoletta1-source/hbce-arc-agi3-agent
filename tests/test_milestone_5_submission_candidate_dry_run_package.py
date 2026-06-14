from pathlib import Path

from hbce_arc_agi3.milestone_5_submission_candidate_dry_run_package import (
    CANDIDATE_KIND,
    EXPECTED_SUBMISSION_FILENAME,
    PACKAGE_GATES,
    PACKAGE_ISSUES,
    PACKAGE_MODE,
    PACKAGE_STATUS,
    PIPELINE_STATUS,
    REQUIRED_PACKAGE_ARTIFACTS,
    SUBMISSION_MODE,
    VALIDATION_STATUS,
    build_package_artifact_statuses,
    build_submission_candidate_dry_run_package,
    render_submission_candidate_dry_run_manifest,
    render_submission_candidate_dry_run_package_markdown,
    run_submission_candidate_dry_run_package_pipeline,
    validate_submission_candidate_dry_run_package,
    write_submission_candidate_dry_run_package_artifacts,
)


def test_submission_candidate_dry_run_package_ready():
    package = build_submission_candidate_dry_run_package()

    assert package.status == PACKAGE_STATUS
    assert package.baseline_commit.startswith("d2f2750")
    assert package.package_mode == PACKAGE_MODE
    assert package.candidate_kind == CANDIDATE_KIND
    assert package.submission_filename == EXPECTED_SUBMISSION_FILENAME
    assert package.submission_mode == SUBMISSION_MODE
    assert package.package_artifact_count == len(REQUIRED_PACKAGE_ARTIFACTS)
    assert package.ready_artifact_count == len(REQUIRED_PACKAGE_ARTIFACTS)
    assert package.package_gate_count == len(PACKAGE_GATES)
    assert package.passed_gate_count == len(PACKAGE_GATES)
    assert package.package_issue_count == 0
    assert package.warning_count == 0
    assert package.candidate_task_count == 3
    assert package.dry_run_package_ready is True
    assert package.ready_for_milestone_5_closure is True
    assert package.ready_for_real_kaggle_submission is False
    assert package.kaggle_submission_sent is False


def test_package_artifact_statuses_are_ready():
    statuses = build_package_artifact_statuses()

    assert len(statuses) == len(REQUIRED_PACKAGE_ARTIFACTS)
    assert all(status.present for status in statuses)
    assert all(status.ready for status in statuses)
    assert all(status.sha256_16 != "MISSING_HASH" for status in statuses)


def test_submission_candidate_dry_run_package_gates_pass():
    package = build_submission_candidate_dry_run_package()

    assert [gate.name for gate in package.package_gates] == list(PACKAGE_GATES)
    assert all(gate.passed for gate in package.package_gates)
    assert all(gate.severity == "PASS" for gate in package.package_gates)


def test_submission_candidate_dry_run_package_issues_inactive():
    package = build_submission_candidate_dry_run_package()

    assert [issue.name for issue in package.package_issues] == list(PACKAGE_ISSUES)
    assert all(issue.active is False for issue in package.package_issues)
    assert all(issue.severity == "BLOCKING" for issue in package.package_issues)


def test_submission_candidate_dry_run_index_is_safe():
    package = build_submission_candidate_dry_run_package()
    index = package.dry_run_index

    assert index["package_mode"] == PACKAGE_MODE
    assert index["artifact_count"] == len(REQUIRED_PACKAGE_ARTIFACTS)
    assert index["ready_artifact_count"] == len(REQUIRED_PACKAGE_ARTIFACTS)
    assert index["contains_archive"] is False
    assert index["contains_upload_step"] is False
    assert index["contains_real_kaggle_submission"] is False


def test_submission_candidate_preview_is_stable():
    package = build_submission_candidate_dry_run_package()
    preview = package.submission_candidate_preview

    assert preview["candidate_kind"] == CANDIDATE_KIND
    assert preview["submission_filename"] == EXPECTED_SUBMISSION_FILENAME
    assert preview["submission_mode"] == SUBMISSION_MODE
    assert preview["task_count"] == 3
    assert preview["kaggle_submission_sent"] is False
    assert preview["task_ids"] == [
        "SMOKE-TASK-IDENTITY-2X2",
        "SMOKE-TASK-COLOR-REMAP-2X2",
        "SMOKE-TASK-OBJECT-FILL-3X3",
    ]


def test_submission_candidate_dry_run_package_validation_passes():
    package = build_submission_candidate_dry_run_package()
    validation = validate_submission_candidate_dry_run_package(package)

    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_submission_candidate_dry_run_package_pipeline_ready():
    payload = run_submission_candidate_dry_run_package_pipeline()

    assert payload["status"] == PIPELINE_STATUS
    assert payload["package_status"] == PACKAGE_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["package_artifact_count"] == len(REQUIRED_PACKAGE_ARTIFACTS)
    assert payload["ready_artifact_count"] == len(REQUIRED_PACKAGE_ARTIFACTS)
    assert payload["package_gate_count"] == len(PACKAGE_GATES)
    assert payload["passed_gate_count"] == len(PACKAGE_GATES)
    assert payload["package_issue_count"] == 0
    assert payload["warning_count"] == 0
    assert payload["candidate_task_count"] == 3
    assert payload["dry_run_package_ready"] is True
    assert payload["ready_for_real_kaggle_submission"] is False
    assert payload["kaggle_submission_sent"] is False


def test_submission_candidate_dry_run_markdown_contains_markers():
    package = build_submission_candidate_dry_run_package()
    markdown = render_submission_candidate_dry_run_package_markdown(package)

    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_DRY_RUN_PACKAGE_MODE=LOCAL_DRY_RUN_PACKAGE_ONLY_NO_ARCHIVE_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_5_PACKAGE_ARTIFACT_COUNT=5" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_ARTIFACT_COUNT=5" in markdown
    assert "ARC_AGI3_MILESTONE_5_PACKAGE_GATE_COUNT=16" in markdown
    assert "ARC_AGI3_MILESTONE_5_PACKAGE_ISSUE_COUNT=0" in markdown
    assert "ARC_AGI3_MILESTONE_5_DRY_RUN_PACKAGE_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_FOR_REAL_KAGGLE_SUBMISSION=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_submission_candidate_dry_run_manifest_contains_boundary():
    package = build_submission_candidate_dry_run_package()
    manifest = render_submission_candidate_dry_run_manifest(package)

    assert "ARC AGI3 SUBMISSION CANDIDATE DRY-RUN PACKAGE MANIFEST v1" in manifest
    assert "package_mode=LOCAL_DRY_RUN_PACKAGE_ONLY_NO_ARCHIVE_NO_UPLOAD" in manifest
    assert "submission_filename=submission.json" in manifest
    assert "package_issue_count=0" in manifest
    assert "dry_run_package_ready=True" in manifest
    assert "ready_for_real_kaggle_submission=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "external_api_dependency=false" in manifest
    assert "private_core_exposure=false" in manifest
    assert "legal_certification=false" in manifest


def test_submission_candidate_dry_run_package_writes_artifacts(tmp_path: Path):
    package = build_submission_candidate_dry_run_package()
    paths = write_submission_candidate_dry_run_package_artifacts(
        package,
        output_dir=str(tmp_path),
    )

    json_path = Path(paths["json_path"])
    markdown_path = Path(paths["markdown_path"])
    manifest_path = Path(paths["manifest_path"])
    index_path = Path(paths["index_path"])
    preview_path = Path(paths["preview_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()
    assert preview_path.exists()
    assert "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_READY" in json_path.read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_V1_READY=true" in markdown_path.read_text(encoding="utf-8")
    assert "ARC AGI3 SUBMISSION CANDIDATE DRY-RUN PACKAGE MANIFEST v1" in manifest_path.read_text(encoding="utf-8")
    assert "LOCAL_DRY_RUN_PACKAGE_ONLY_NO_ARCHIVE_NO_UPLOAD" in index_path.read_text(encoding="utf-8")
    assert "LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY" in preview_path.read_text(encoding="utf-8")


def test_submission_candidate_dry_run_boundary_is_intact():
    package = build_submission_candidate_dry_run_package()
    boundary = package.boundary

    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False
