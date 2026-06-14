from pathlib import Path

from hbce_arc_agi3.milestone_5_kaggle_submission_dry_run_package import (
    DRY_RUN_RELEASE_FILES,
    DRY_RUN_SOURCE_ARTIFACTS,
    PACKAGE_STATUS,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_dry_run_source_artifacts,
    build_kaggle_submission_dry_run_package,
    render_kaggle_submission_dry_run_manifest,
    render_kaggle_submission_dry_run_package_markdown,
    run_kaggle_submission_dry_run_package_pipeline,
    validate_kaggle_submission_dry_run_package,
    write_kaggle_submission_dry_run_package_artifacts,
)


def test_kaggle_submission_dry_run_package_ready():
    package = build_kaggle_submission_dry_run_package()

    assert package.status == PACKAGE_STATUS
    assert package.baseline_commit.startswith("e983e88")
    assert package.package_source_artifact_count == len(DRY_RUN_SOURCE_ARTIFACTS)
    assert package.planned_release_file_count == len(DRY_RUN_RELEASE_FILES)
    assert package.package_mode == "MANIFEST_ONLY_NO_ARCHIVE_NO_UPLOAD"
    assert package.submission_mode == "LOCAL_DRY_RUN_ONLY"
    assert package.real_submission_blocked is True
    assert package.ready_for_submission_entrypoint_contract is True
    assert package.kaggle_submission_sent is False
    assert all(artifact.present for artifact in package.source_artifacts)


def test_kaggle_submission_dry_run_package_validation_passes():
    package = build_kaggle_submission_dry_run_package()
    validation = validate_kaggle_submission_dry_run_package(package)

    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_kaggle_submission_dry_run_package_pipeline_ready():
    payload = run_kaggle_submission_dry_run_package_pipeline()

    assert payload["status"] == PIPELINE_STATUS
    assert payload["package_status"] == PACKAGE_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["package_source_artifact_count"] == len(DRY_RUN_SOURCE_ARTIFACTS)
    assert payload["planned_release_file_count"] == len(DRY_RUN_RELEASE_FILES)
    assert payload["ready_for_submission_entrypoint_contract"] is True
    assert payload["kaggle_submission_sent"] is False


def test_kaggle_submission_dry_run_package_markdown_contains_markers():
    package = build_kaggle_submission_dry_run_package()
    markdown = render_kaggle_submission_dry_run_package_markdown(package)

    assert "ARC_AGI3_MILESTONE_5_KAGGLE_SUBMISSION_DRY_RUN_PACKAGE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_KAGGLE_SUBMISSION_DRY_RUN_PACKAGE_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_LOCAL_DRY_RUN_ONLY=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_REAL_SUBMISSION_BLOCKED=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_READY_FOR_SUBMISSION_ENTRYPOINT_CONTRACT=true" in markdown
    assert "ARC_AGI3_MILESTONE_5_BASELINE_RELEASE_INDEX_COMMIT=e983e88" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_kaggle_submission_dry_run_package_manifest_contains_boundary():
    package = build_kaggle_submission_dry_run_package()
    manifest = render_kaggle_submission_dry_run_manifest(package)

    assert "ARC AGI3 KAGGLE SUBMISSION DRY-RUN MANIFEST v1" in manifest
    assert "submission_mode=LOCAL_DRY_RUN_ONLY" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "real_submission_blocked=True" in manifest
    assert "external_api_dependency=false" in manifest
    assert "private_core_exposure=false" in manifest
    assert "legal_certification=false" in manifest


def test_kaggle_submission_dry_run_package_writes_artifacts(tmp_path: Path):
    package = build_kaggle_submission_dry_run_package()
    paths = write_kaggle_submission_dry_run_package_artifacts(
        package,
        output_dir=str(tmp_path),
    )

    json_path = Path(paths["json_path"])
    markdown_path = Path(paths["markdown_path"])
    manifest_path = Path(paths["manifest_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert manifest_path.exists()
    assert "MILESTONE_5_KAGGLE_SUBMISSION_DRY_RUN_PACKAGE_READY" in json_path.read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_5_KAGGLE_SUBMISSION_DRY_RUN_PACKAGE_V1_READY=true" in markdown_path.read_text(encoding="utf-8")
    assert "ARC AGI3 KAGGLE SUBMISSION DRY-RUN MANIFEST v1" in manifest_path.read_text(encoding="utf-8")


def test_dry_run_source_artifacts_exist():
    artifacts = build_dry_run_source_artifacts()
    missing = [artifact.path for artifact in artifacts if not artifact.present]

    assert missing == []
