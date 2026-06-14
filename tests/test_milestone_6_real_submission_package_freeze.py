from pathlib import Path

from hbce_arc_agi3.milestone_6_real_submission_package_freeze import (
    BASELINE_COMMIT,
    FREEZE_GATES,
    FREEZE_ISSUES,
    FREEZE_MODE,
    FREEZE_SCOPE,
    FREEZE_STATUS,
    FREEZE_VERDICT,
    FROZEN_ARTIFACT_NAMES,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_6_real_submission_package_freeze,
    render_real_submission_package_freeze_manifest,
    render_real_submission_package_freeze_markdown,
    run_milestone_6_real_submission_package_freeze_pipeline,
    validate_milestone_6_real_submission_package_freeze,
    write_real_submission_package_freeze_artifacts,
)


def test_real_submission_package_freeze_ready():
    freeze = build_milestone_6_real_submission_package_freeze()
    assert freeze["status"] == FREEZE_STATUS
    assert freeze["baseline_commit"] == BASELINE_COMMIT
    assert freeze["freeze_mode"] == FREEZE_MODE
    assert freeze["freeze_scope"] == FREEZE_SCOPE
    assert freeze["freeze_verdict"] == FREEZE_VERDICT
    assert freeze["frozen_artifact_count"] == len(FROZEN_ARTIFACT_NAMES)
    assert freeze["ready_artifact_count"] == len(FROZEN_ARTIFACT_NAMES)
    assert freeze["freeze_gate_count"] == len(FREEZE_GATES)
    assert freeze["passed_gate_count"] == len(FREEZE_GATES)
    assert freeze["freeze_issue_count"] == 0
    assert freeze["freeze_ready"] is True
    assert freeze["freeze_locked"] is True


def test_real_submission_package_freeze_does_not_submit():
    freeze = build_milestone_6_real_submission_package_freeze()
    assert freeze["manual_execution_performed"] is False
    assert freeze["real_submission_allowed"] is False
    assert freeze["ready_for_real_kaggle_submission"] is False
    assert freeze["real_submission_created"] is False
    assert freeze["kaggle_submission_sent"] is False
    assert freeze["upload_performed"] is False
    assert freeze["kaggle_authentication_performed"] is False


def test_frozen_artifacts_are_ready_and_hashed():
    freeze = build_milestone_6_real_submission_package_freeze()
    assert [item["name"] for item in freeze["frozen_artifacts"]] == list(FROZEN_ARTIFACT_NAMES)
    assert all(item["present"] is True for item in freeze["frozen_artifacts"])
    assert all(item["ready"] is True for item in freeze["frozen_artifacts"])
    assert all(item["sha256"] != "MISSING_HASH" for item in freeze["frozen_artifacts"])
    assert all(item["sha256_16"] != "MISSING_HASH" for item in freeze["frozen_artifacts"])


def test_freeze_record_is_conservative():
    record = build_milestone_6_real_submission_package_freeze()["freeze_record"]
    assert record["freeze_record_ready"] is True
    assert record["freeze_locked"] is True
    assert record["manual_execution_gate_ready"] is True
    assert record["manual_execution_performed"] is False
    assert record["precheck_passed"] is True
    assert record["real_submission_allowed"] is False
    assert record["ready_for_real_kaggle_submission"] is False
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_freeze_gates_pass():
    freeze = build_milestone_6_real_submission_package_freeze()
    assert [item["name"] for item in freeze["freeze_gates"]] == list(FREEZE_GATES)
    assert all(item["passed"] is True for item in freeze["freeze_gates"])
    assert all(item["severity"] == "PASS" for item in freeze["freeze_gates"])


def test_freeze_issues_inactive():
    freeze = build_milestone_6_real_submission_package_freeze()
    assert [item["name"] for item in freeze["freeze_issues"]] == list(FREEZE_ISSUES)
    assert all(item["active"] is False for item in freeze["freeze_issues"])


def test_freeze_boundary_intact():
    boundary = build_milestone_6_real_submission_package_freeze()["boundary"]
    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_freeze_validation_passes():
    freeze = build_milestone_6_real_submission_package_freeze()
    validation = validate_milestone_6_real_submission_package_freeze(freeze)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_freeze_pipeline_ready():
    payload = run_milestone_6_real_submission_package_freeze_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["freeze_status"] == FREEZE_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["freeze_mode"] == FREEZE_MODE
    assert payload["freeze_verdict"] == FREEZE_VERDICT
    assert payload["frozen_artifact_count"] == len(FROZEN_ARTIFACT_NAMES)
    assert payload["ready_artifact_count"] == len(FROZEN_ARTIFACT_NAMES)
    assert payload["freeze_gate_count"] == len(FREEZE_GATES)
    assert payload["passed_gate_count"] == len(FREEZE_GATES)
    assert payload["freeze_issue_count"] == 0
    assert payload["freeze_ready"] is True
    assert payload["freeze_locked"] is True
    assert payload["kaggle_submission_sent"] is False


def test_freeze_markdown_contains_markers():
    markdown = render_real_submission_package_freeze_markdown(build_milestone_6_real_submission_package_freeze())
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_PACKAGE_FREEZE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_PACKAGE_FREEZE_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_FREEZE_MODE=REAL_SUBMISSION_PACKAGE_FREEZE_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_6_FREEZE_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_FREEZE_LOCKED=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_freeze_manifest_contains_hashes_and_boundary():
    manifest = render_real_submission_package_freeze_manifest(build_milestone_6_real_submission_package_freeze())
    assert "ARC AGI3 MILESTONE 6 REAL SUBMISSION PACKAGE FREEZE MANIFEST v1" in manifest
    assert "freeze_mode=REAL_SUBMISSION_PACKAGE_FREEZE_ONLY_NO_UPLOAD" in manifest
    assert "freeze_ready=True" in manifest
    assert "freeze_locked=True" in manifest
    assert "FROZEN_ARTIFACTS" in manifest
    assert "sha256=" in manifest
    assert "real_submission_allowed=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest
    assert "external_api_dependency=false" in manifest
    assert "private_core_exposure=false" in manifest
    assert "legal_certification=false" in manifest


def test_freeze_writes_artifacts(tmp_path: Path):
    freeze = build_milestone_6_real_submission_package_freeze()
    paths = write_real_submission_package_freeze_artifacts(freeze, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_6_REAL_SUBMISSION_PACKAGE_FREEZE_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_PACKAGE_FREEZE_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "REAL_SUBMISSION_PACKAGE_FROZEN_FOR_MANUAL_REVIEW_NO_SUBMISSION" in Path(paths["index_path"]).read_text(encoding="utf-8")
