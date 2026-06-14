from pathlib import Path

from hbce_arc_agi3.milestone_7_final_competitive_readiness_audit import (
    AUDIT_GATES,
    AUDIT_ISSUES,
    AUDIT_MODE,
    AUDIT_SCOPE,
    AUDIT_STATUS,
    AUDIT_VERDICT,
    BASELINE_COMMIT,
    EXPECTED_AUDIT_CHAIN_COUNT,
    EXPECTED_AUDIT_SECTION_COUNT,
    EXPECTED_BLOCKED_DIMENSION_COUNT,
    EXPECTED_BLOCKER_COUNT,
    EXPECTED_CANDIDATE_FILE_COUNT,
    EXPECTED_LOCAL_MEASUREMENT_COUNT,
    EXPECTED_PASS_DIMENSION_COUNT,
    EXPECTED_READINESS_DIMENSION_COUNT,
    EXPECTED_REBUILD_COMPONENT_COUNT,
    EXPECTED_REGRESSION_FAILURE_COUNT,
    EXPECTED_REGRESSION_PASS_COUNT,
    EXPECTED_SOURCE_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_7_final_competitive_readiness_audit,
    render_final_competitive_readiness_audit_manifest,
    render_final_competitive_readiness_audit_markdown,
    run_milestone_7_final_competitive_readiness_audit_pipeline,
    validate_milestone_7_final_competitive_readiness_audit,
    write_final_competitive_readiness_audit_artifacts,
)


def test_final_audit_ready():
    audit = build_milestone_7_final_competitive_readiness_audit()
    assert audit["status"] == AUDIT_STATUS
    assert audit["baseline_commit"] == BASELINE_COMMIT
    assert audit["audit_mode"] == AUDIT_MODE
    assert audit["audit_scope"] == AUDIT_SCOPE
    assert audit["audit_verdict"] == AUDIT_VERDICT
    assert audit["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert audit["source_count"] == EXPECTED_SOURCE_COUNT
    assert audit["rebuild_component_count"] == EXPECTED_REBUILD_COMPONENT_COUNT
    assert audit["candidate_file_count"] == EXPECTED_CANDIDATE_FILE_COUNT
    assert audit["audit_chain_count"] == EXPECTED_AUDIT_CHAIN_COUNT
    assert audit["local_measurement_count"] == EXPECTED_LOCAL_MEASUREMENT_COUNT
    assert audit["regression_pass_count"] == EXPECTED_REGRESSION_PASS_COUNT
    assert audit["regression_failure_count"] == EXPECTED_REGRESSION_FAILURE_COUNT
    assert audit["audit_section_count"] == EXPECTED_AUDIT_SECTION_COUNT
    assert audit["readiness_dimension_count"] == EXPECTED_READINESS_DIMENSION_COUNT
    assert audit["blocker_count"] == EXPECTED_BLOCKER_COUNT
    assert audit["pass_dimension_count"] == EXPECTED_PASS_DIMENSION_COUNT
    assert audit["blocked_dimension_count"] == EXPECTED_BLOCKED_DIMENSION_COUNT
    assert audit["audit_gate_count"] == len(AUDIT_GATES)
    assert audit["passed_gate_count"] == len(AUDIT_GATES)
    assert audit["audit_issue_count"] == 0
    assert audit["audit_ready"] is True


def test_final_audit_blocks_real_submission():
    audit = build_milestone_7_final_competitive_readiness_audit()
    assert audit["real_submission_readiness"] == "BLOCKED"
    assert audit["real_submission_decision"] == "NOT_READY"
    assert audit["solver_iteration_required"] is True
    assert audit["real_submission_created"] is False
    assert audit["real_submission_allowed"] is False
    assert audit["ready_for_real_kaggle_submission"] is False
    assert audit["kaggle_submission_sent"] is False
    assert audit["upload_performed"] is False
    assert audit["kaggle_authentication_performed"] is False


def test_readiness_dimensions_have_expected_statuses():
    dimensions = build_milestone_7_final_competitive_readiness_audit()["readiness_dimensions"]
    assert len(dimensions) == EXPECTED_READINESS_DIMENSION_COUNT
    assert sum(1 for item in dimensions if item["status"] == "PASS") == EXPECTED_PASS_DIMENSION_COUNT
    assert sum(1 for item in dimensions if item["status"] == "BLOCKED") == EXPECTED_BLOCKED_DIMENSION_COUNT
    assert any(item["category"] == "REAL_COMPETITIVE_READINESS" and item["blocking"] is True for item in dimensions)


def test_real_submission_blockers_are_active():
    blockers = build_milestone_7_final_competitive_readiness_audit()["real_submission_blockers"]
    assert len(blockers) == EXPECTED_BLOCKER_COUNT
    assert all(item["active"] is True for item in blockers)
    assert {item["blocker_id"] for item in blockers} == {
        "no_real_kaggle_submission_created_v1",
        "no_kaggle_authentication_performed_v1",
        "no_upload_performed_v1",
        "no_numeric_competitive_score_claim_v1",
        "solver_iteration_still_required_v1",
        "operator_final_submission_decision_absent_v1",
    }


def test_final_decision_is_conservative():
    decision = build_milestone_7_final_competitive_readiness_audit()["final_decision"]
    assert decision["local_candidate_chain_integrity"] == "PASS"
    assert decision["local_candidate_rebuild_integrity"] == "PASS"
    assert decision["regression_state"] == "PASS"
    assert decision["score_claim_boundary"] == "PASS"
    assert decision["real_submission_readiness"] == "BLOCKED"
    assert decision["real_submission_decision"] == "NOT_READY"
    assert decision["solver_iteration_required"] is True
    assert decision["next_stage"] == NEXT_ALLOWED_STAGE


def test_candidate_source_is_present_and_hashed():
    source = build_milestone_7_final_competitive_readiness_audit()["candidate_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_7_SUBMISSION_CANDIDATE_REBUILD_READY"
    assert source["candidate_id"].startswith("MILESTONE-7-SUBMISSION-CANDIDATE-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_audit_record_is_conservative():
    record = build_milestone_7_final_competitive_readiness_audit()["audit_record"]
    assert record["audit_ready"] is True
    assert record["audit_locked"] is True
    assert record["candidate_ready"] is True
    assert record["final_competitive_readiness_audit_required"] is True
    assert record["real_submission_created"] is False
    assert record["real_submission_allowed"] is False
    assert record["ready_for_real_kaggle_submission"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["upload_performed"] is False
    assert record["kaggle_authentication_performed"] is False
    assert record["solver_iteration_required"] is True


def test_audit_gates_pass():
    audit = build_milestone_7_final_competitive_readiness_audit()
    assert [item["name"] for item in audit["audit_gates"]] == list(AUDIT_GATES)
    assert all(item["passed"] is True for item in audit["audit_gates"])
    assert all(item["severity"] == "PASS" for item in audit["audit_gates"])


def test_audit_issues_inactive():
    audit = build_milestone_7_final_competitive_readiness_audit()
    assert [item["name"] for item in audit["audit_issues"]] == list(AUDIT_ISSUES)
    assert all(item["active"] is False for item in audit["audit_issues"])


def test_audit_boundary_intact():
    boundary = build_milestone_7_final_competitive_readiness_audit()["boundary"]
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
    audit = build_milestone_7_final_competitive_readiness_audit()
    validation = validate_milestone_7_final_competitive_readiness_audit(audit)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_audit_pipeline_ready():
    payload = run_milestone_7_final_competitive_readiness_audit_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["audit_status"] == AUDIT_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["audit_mode"] == AUDIT_MODE
    assert payload["audit_verdict"] == AUDIT_VERDICT
    assert payload["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert payload["source_count"] == EXPECTED_SOURCE_COUNT
    assert payload["audit_gate_count"] == len(AUDIT_GATES)
    assert payload["passed_gate_count"] == len(AUDIT_GATES)
    assert payload["audit_issue_count"] == 0
    assert payload["audit_ready"] is True
    assert payload["real_submission_readiness"] == "BLOCKED"
    assert payload["real_submission_decision"] == "NOT_READY"
    assert payload["solver_iteration_required"] is True
    assert payload["kaggle_submission_sent"] is False


def test_audit_markdown_contains_markers():
    markdown = render_final_competitive_readiness_audit_markdown(
        build_milestone_7_final_competitive_readiness_audit()
    )
    assert "ARC_AGI3_MILESTONE_7_FINAL_COMPETITIVE_READINESS_AUDIT_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_FINAL_COMPETITIVE_READINESS_AUDIT_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_AUDIT_MODE=FINAL_COMPETITIVE_READINESS_AUDIT_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_READINESS=BLOCKED" in markdown
    assert "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_DECISION=NOT_READY" in markdown
    assert "ARC_AGI3_MILESTONE_7_SOLVER_ITERATION_REQUIRED=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_V2" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_audit_manifest_contains_dimensions_and_blockers():
    manifest = render_final_competitive_readiness_audit_manifest(
        build_milestone_7_final_competitive_readiness_audit()
    )
    assert "ARC AGI3 MILESTONE 7 FINAL COMPETITIVE READINESS AUDIT MANIFEST v1" in manifest
    assert "audit_mode=FINAL_COMPETITIVE_READINESS_AUDIT_ONLY_NO_UPLOAD" in manifest
    assert "audit_ready=True" in manifest
    assert "READINESS_DIMENSIONS" in manifest
    assert "REAL_SUBMISSION_BLOCKERS" in manifest
    assert "real_competitive_readiness_blocked_v1" in manifest
    assert "solver_iteration_still_required_v1 active=True" in manifest
    assert "real_submission_decision=NOT_READY" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest


def test_audit_writes_artifacts(tmp_path: Path):
    audit = build_milestone_7_final_competitive_readiness_audit()
    paths = write_final_competitive_readiness_audit_artifacts(audit, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_7_FINAL_COMPETITIVE_READINESS_AUDIT_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_7_FINAL_COMPETITIVE_READINESS_AUDIT_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "FINAL_COMPETITIVE_READINESS_AUDIT_COMPLETE_REAL_SUBMISSION_NOT_READY_SOLVER_ITERATION_REQUIRED" in Path(paths["index_path"]).read_text(encoding="utf-8")


def test_audit_metadata_safe():
    metadata = build_milestone_7_final_competitive_readiness_audit()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
