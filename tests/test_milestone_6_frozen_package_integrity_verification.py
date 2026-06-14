from pathlib import Path

from hbce_arc_agi3.milestone_6_frozen_package_integrity_verification import (
    BASELINE_COMMIT,
    EXPECTED_FROZEN_ARTIFACT_COUNT,
    INTEGRITY_GATES,
    INTEGRITY_ISSUES,
    INTEGRITY_MODE,
    INTEGRITY_SCOPE,
    INTEGRITY_STATUS,
    INTEGRITY_VERDICT,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_6_frozen_package_integrity_verification,
    render_frozen_package_integrity_verification_manifest,
    render_frozen_package_integrity_verification_markdown,
    run_milestone_6_frozen_package_integrity_verification_pipeline,
    validate_milestone_6_frozen_package_integrity_verification,
    write_frozen_package_integrity_verification_artifacts,
)


def test_frozen_package_integrity_verification_ready():
    verification = build_milestone_6_frozen_package_integrity_verification()
    assert verification["status"] == INTEGRITY_STATUS
    assert verification["baseline_commit"] == BASELINE_COMMIT
    assert verification["integrity_mode"] == INTEGRITY_MODE
    assert verification["integrity_scope"] == INTEGRITY_SCOPE
    assert verification["integrity_verdict"] == INTEGRITY_VERDICT
    assert verification["frozen_artifact_count"] == EXPECTED_FROZEN_ARTIFACT_COUNT
    assert verification["verified_artifact_count"] == EXPECTED_FROZEN_ARTIFACT_COUNT
    assert verification["matched_hash_count"] == EXPECTED_FROZEN_ARTIFACT_COUNT
    assert verification["integrity_gate_count"] == len(INTEGRITY_GATES)
    assert verification["passed_gate_count"] == len(INTEGRITY_GATES)
    assert verification["integrity_issue_count"] == 0
    assert verification["integrity_ready"] is True
    assert verification["integrity_verified"] is True
    assert verification["integrity_locked"] is True


def test_frozen_package_integrity_does_not_submit():
    verification = build_milestone_6_frozen_package_integrity_verification()
    assert verification["manual_execution_performed"] is False
    assert verification["real_submission_allowed"] is False
    assert verification["ready_for_real_kaggle_submission"] is False
    assert verification["real_submission_created"] is False
    assert verification["kaggle_submission_sent"] is False
    assert verification["upload_performed"] is False
    assert verification["kaggle_authentication_performed"] is False


def test_artifact_integrity_checks_match_hashes():
    checks = build_milestone_6_frozen_package_integrity_verification()["artifact_integrity_checks"]
    assert len(checks) == EXPECTED_FROZEN_ARTIFACT_COUNT
    assert all(item["present"] is True for item in checks)
    assert all(item["ready"] is True for item in checks)
    assert all(item["recorded_sha256"] != "MISSING_HASH" for item in checks)
    assert all(item["current_sha256"] != "MISSING_HASH" for item in checks)
    assert all(item["hash_match"] is True for item in checks)


def test_integrity_record_is_conservative():
    record = build_milestone_6_frozen_package_integrity_verification()["integrity_record"]
    assert record["integrity_verification_ready"] is True
    assert record["integrity_verified"] is True
    assert record["integrity_locked"] is True
    assert record["freeze_ready"] is True
    assert record["freeze_locked"] is True
    assert record["matched_hash_count"] == EXPECTED_FROZEN_ARTIFACT_COUNT
    assert record["manual_execution_performed"] is False
    assert record["real_submission_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_integrity_gates_pass():
    verification = build_milestone_6_frozen_package_integrity_verification()
    assert [item["name"] for item in verification["integrity_gates"]] == list(INTEGRITY_GATES)
    assert all(item["passed"] is True for item in verification["integrity_gates"])
    assert all(item["severity"] == "PASS" for item in verification["integrity_gates"])


def test_integrity_issues_inactive():
    verification = build_milestone_6_frozen_package_integrity_verification()
    assert [item["name"] for item in verification["integrity_issues"]] == list(INTEGRITY_ISSUES)
    assert all(item["active"] is False for item in verification["integrity_issues"])


def test_integrity_boundary_intact():
    boundary = build_milestone_6_frozen_package_integrity_verification()["boundary"]
    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_integrity_validation_passes():
    verification = build_milestone_6_frozen_package_integrity_verification()
    validation = validate_milestone_6_frozen_package_integrity_verification(verification)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_integrity_pipeline_ready():
    payload = run_milestone_6_frozen_package_integrity_verification_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["integrity_status"] == INTEGRITY_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["integrity_mode"] == INTEGRITY_MODE
    assert payload["integrity_verdict"] == INTEGRITY_VERDICT
    assert payload["frozen_artifact_count"] == EXPECTED_FROZEN_ARTIFACT_COUNT
    assert payload["verified_artifact_count"] == EXPECTED_FROZEN_ARTIFACT_COUNT
    assert payload["matched_hash_count"] == EXPECTED_FROZEN_ARTIFACT_COUNT
    assert payload["integrity_gate_count"] == len(INTEGRITY_GATES)
    assert payload["passed_gate_count"] == len(INTEGRITY_GATES)
    assert payload["integrity_issue_count"] == 0
    assert payload["integrity_ready"] is True
    assert payload["kaggle_submission_sent"] is False


def test_integrity_markdown_contains_markers():
    markdown = render_frozen_package_integrity_verification_markdown(
        build_milestone_6_frozen_package_integrity_verification()
    )
    assert "ARC_AGI3_MILESTONE_6_FROZEN_PACKAGE_INTEGRITY_VERIFICATION_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_FROZEN_PACKAGE_INTEGRITY_VERIFICATION_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_INTEGRITY_MODE=FROZEN_PACKAGE_INTEGRITY_VERIFICATION_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_6_INTEGRITY_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_INTEGRITY_VERIFIED=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_INTEGRITY_LOCKED=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_MATCHED_HASH_COUNT=4" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_integrity_manifest_contains_hash_comparison():
    manifest = render_frozen_package_integrity_verification_manifest(
        build_milestone_6_frozen_package_integrity_verification()
    )
    assert "ARC AGI3 MILESTONE 6 FROZEN PACKAGE INTEGRITY VERIFICATION MANIFEST v1" in manifest
    assert "integrity_mode=FROZEN_PACKAGE_INTEGRITY_VERIFICATION_ONLY_NO_UPLOAD" in manifest
    assert "integrity_ready=True" in manifest
    assert "integrity_verified=True" in manifest
    assert "matched_hash_count=4" in manifest
    assert "ARTIFACT_INTEGRITY_CHECKS" in manifest
    assert "hash_match=True" in manifest
    assert "recorded_sha256=" in manifest
    assert "current_sha256=" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest


def test_integrity_writes_artifacts(tmp_path: Path):
    verification = build_milestone_6_frozen_package_integrity_verification()
    paths = write_frozen_package_integrity_verification_artifacts(verification, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_6_FROZEN_PACKAGE_INTEGRITY_VERIFICATION_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_6_FROZEN_PACKAGE_INTEGRITY_VERIFICATION_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "FROZEN_PACKAGE_INTEGRITY_VERIFIED_NO_SUBMISSION" in Path(paths["index_path"]).read_text(encoding="utf-8")
