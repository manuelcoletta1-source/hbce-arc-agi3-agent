from pathlib import Path

from hbce_arc_agi3.milestone_6_submission_candidate_final_audit import (
    AUDIT_GATES,
    AUDIT_ISSUES,
    AUDIT_MODE,
    AUDIT_SCOPE,
    AUDIT_STATUS,
    AUDIT_VERDICT,
    BASELINE_COMMIT,
    EXPECTED_AUDITED_SOURCE_COUNT,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_6_submission_candidate_final_audit,
    render_submission_candidate_final_audit_manifest,
    render_submission_candidate_final_audit_markdown,
    run_milestone_6_submission_candidate_final_audit_pipeline,
    validate_milestone_6_submission_candidate_final_audit,
    write_submission_candidate_final_audit_artifacts,
)


def test_submission_candidate_final_audit_ready():
    audit = build_milestone_6_submission_candidate_final_audit()
    assert audit["status"] == AUDIT_STATUS
    assert audit["baseline_commit"] == BASELINE_COMMIT
    assert audit["audit_mode"] == AUDIT_MODE
    assert audit["audit_scope"] == AUDIT_SCOPE
    assert audit["audit_verdict"] == AUDIT_VERDICT
    assert audit["audited_source_count"] == EXPECTED_AUDITED_SOURCE_COUNT
    assert audit["ready_source_count"] == EXPECTED_AUDITED_SOURCE_COUNT
    assert audit["source_hash_count"] == EXPECTED_AUDITED_SOURCE_COUNT
    assert audit["audit_gate_count"] == len(AUDIT_GATES)
    assert audit["passed_gate_count"] == len(AUDIT_GATES)
    assert audit["audit_issue_count"] == 0
    assert audit["audit_ready"] is True
    assert audit["audit_locked"] is True


def test_submission_candidate_final_audit_blocks_real_submission():
    audit = build_milestone_6_submission_candidate_final_audit()
    assert audit["solver_improvement_required"] is True
    assert audit["competitive_claim_absent"] is True
    assert audit["manual_upload_required"] is True
    assert audit["manual_execution_performed"] is False
    assert audit["real_submission_allowed"] is False
    assert audit["ready_for_real_kaggle_submission"] is False
    assert audit["real_submission_created"] is False
    assert audit["kaggle_submission_sent"] is False
    assert audit["upload_performed"] is False
    assert audit["kaggle_authentication_performed"] is False


def test_audited_sources_are_ready_and_hashed():
    audit = build_milestone_6_submission_candidate_final_audit()
    sources = audit["audited_sources"]
    assert len(sources) == EXPECTED_AUDITED_SOURCE_COUNT
    assert all(item["present"] is True for item in sources)
    assert all(item["ready"] is True for item in sources)
    assert all(item["sha256"] != "MISSING_HASH" for item in sources)
    assert all(item["sha256_16"] != "MISSING_HASH" for item in sources)


def test_audit_record_is_conservative():
    record = build_milestone_6_submission_candidate_final_audit()["audit_record"]
    assert record["audit_ready"] is True
    assert record["audit_locked"] is True
    assert record["integrity_verified"] is True
    assert record["integrity_locked"] is True
    assert record["freeze_ready"] is True
    assert record["freeze_locked"] is True
    assert record["precheck_passed"] is True
    assert record["operator_approval_granted"] is True
    assert record["solver_improvement_required"] is True
    assert record["competitive_claim_absent"] is True
    assert record["real_submission_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_audit_gates_pass():
    audit = build_milestone_6_submission_candidate_final_audit()
    assert [item["name"] for item in audit["audit_gates"]] == list(AUDIT_GATES)
    assert all(item["passed"] is True for item in audit["audit_gates"])
    assert all(item["severity"] == "PASS" for item in audit["audit_gates"])


def test_audit_issues_inactive():
    audit = build_milestone_6_submission_candidate_final_audit()
    assert [item["name"] for item in audit["audit_issues"]] == list(AUDIT_ISSUES)
    assert all(item["active"] is False for item in audit["audit_issues"])


def test_audit_boundary_intact():
    boundary = build_milestone_6_submission_candidate_final_audit()["boundary"]
    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_audit_validation_passes():
    audit = build_milestone_6_submission_candidate_final_audit()
    validation = validate_milestone_6_submission_candidate_final_audit(audit)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_audit_pipeline_ready():
    payload = run_milestone_6_submission_candidate_final_audit_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["audit_status"] == AUDIT_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["audit_mode"] == AUDIT_MODE
    assert payload["audit_verdict"] == AUDIT_VERDICT
    assert payload["audited_source_count"] == EXPECTED_AUDITED_SOURCE_COUNT
    assert payload["ready_source_count"] == EXPECTED_AUDITED_SOURCE_COUNT
    assert payload["source_hash_count"] == EXPECTED_AUDITED_SOURCE_COUNT
    assert payload["audit_gate_count"] == len(AUDIT_GATES)
    assert payload["passed_gate_count"] == len(AUDIT_GATES)
    assert payload["audit_issue_count"] == 0
    assert payload["audit_ready"] is True
    assert payload["kaggle_submission_sent"] is False


def test_audit_markdown_contains_markers():
    markdown = render_submission_candidate_final_audit_markdown(
        build_milestone_6_submission_candidate_final_audit()
    )
    assert "ARC_AGI3_MILESTONE_6_SUBMISSION_CANDIDATE_FINAL_AUDIT_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_SUBMISSION_CANDIDATE_FINAL_AUDIT_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_AUDIT_MODE=SUBMISSION_CANDIDATE_FINAL_AUDIT_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_6_SOLVER_IMPROVEMENT_REQUIRED=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_COMPETITIVE_CLAIM_ABSENT=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_audit_manifest_contains_sources_and_boundary():
    manifest = render_submission_candidate_final_audit_manifest(
        build_milestone_6_submission_candidate_final_audit()
    )
    assert "ARC AGI3 MILESTONE 6 SUBMISSION CANDIDATE FINAL AUDIT MANIFEST v1" in manifest
    assert "audit_mode=SUBMISSION_CANDIDATE_FINAL_AUDIT_ONLY_NO_UPLOAD" in manifest
    assert "audit_ready=True" in manifest
    assert "audit_locked=True" in manifest
    assert "solver_improvement_required=True" in manifest
    assert "competitive_claim_absent=True" in manifest
    assert "AUDITED_SOURCES" in manifest
    assert "sha256=" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest


def test_audit_writes_artifacts(tmp_path: Path):
    audit = build_milestone_6_submission_candidate_final_audit()
    paths = write_submission_candidate_final_audit_artifacts(audit, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_6_SUBMISSION_CANDIDATE_FINAL_AUDIT_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_6_SUBMISSION_CANDIDATE_FINAL_AUDIT_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "FINAL_AUDIT_PASS_REAL_SUBMISSION_STILL_BLOCKED_PENDING_SOLVER_IMPROVEMENT" in Path(paths["index_path"]).read_text(encoding="utf-8")
