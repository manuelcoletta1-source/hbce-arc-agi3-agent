from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_10_local_error_pattern_audit import (
    AUDIT_MODE,
    AUDIT_SCOPE,
    AUDIT_STATUS,
    AUDIT_VERDICT,
    EXPECTED_AUDIT_CASE_COUNT,
    EXPECTED_AUDIT_CHECK_COUNT,
    EXPECTED_AUDIT_FAILURE_COUNT,
    EXPECTED_AUDIT_PASS_COUNT,
    EXPECTED_ERROR_PATTERN_COUNT,
    EXPECTED_SOLVER_TARGET_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_local_error_audit_source_summary,
    build_local_error_pattern_audit_checks,
    build_local_error_pattern_audit_state,
    build_local_error_pattern_catalog,
    build_milestone_10_local_error_pattern_audit,
    evaluate_all_local_error_pattern_audit_cases,
    evaluate_local_error_pattern_audit_case,
    render_local_error_pattern_audit_manifest,
    render_local_error_pattern_audit_markdown,
    run_milestone_10_local_error_pattern_audit_pipeline,
    validate_milestone_10_local_error_pattern_audit,
    write_local_error_pattern_audit_artifacts,
)


def test_audit_source_summary_reads_milestone_10_baseline():
    summary = build_local_error_audit_source_summary()
    assert summary["baseline_present"] is True
    assert summary["baseline_status"] == "MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_BASELINE_V1_READY"
    assert summary["baseline_id"].startswith("MILESTONE-10-LOCAL-SOLVER-BASELINE-")
    assert summary["baseline_ready"] is True
    assert summary["baseline_locked"] is True
    assert summary["next_allowed_stage"] == "MILESTONE_10_TASK_2_LOCAL_ERROR_PATTERN_AUDIT_V1"
    assert summary["milestone_10_open"] is True
    assert summary["local_solver_improvement_cycle_ready"] is True
    assert summary["real_submission_decision"] == "NOT_AUTHORIZED"
    assert summary["real_submission_allowed"] is False
    assert summary["fail_closed_active"] is True
    assert Path(summary["candidate_source_path"]).exists()
    assert summary["candidate_id"].startswith("MILESTONE-8-SUBMISSION-REFRESH-")


def test_error_pattern_catalog_is_local_only():
    patterns = build_local_error_pattern_catalog()
    assert len(patterns) == EXPECTED_ERROR_PATTERN_COUNT
    assert len({pattern["patch_target"] for pattern in patterns}) == EXPECTED_SOLVER_TARGET_COUNT
    assert all(pattern["local_only"] is True for pattern in patterns)
    assert all(pattern["requires_external_api"] is False for pattern in patterns)
    assert all(pattern["requires_kaggle_upload"] is False for pattern in patterns)
    assert all(pattern["ready_for_patch_plan"] is True for pattern in patterns)
    families = {pattern["family"] for pattern in patterns}
    assert "color_mapping" in families
    assert "object_model" in families
    assert "shape_symmetry" in families
    assert "cross_family_composition" in families
    assert "candidate_ranker" in families
    assert "traceability" in families


def test_audit_state_keeps_fail_closed_active():
    state = build_local_error_pattern_audit_state()
    assert state["local_error_pattern_audit_required"] is True
    assert state["local_error_pattern_audit_created"] is True
    assert state["local_error_pattern_audit_ready"] is True
    assert state["local_error_pattern_audit_locked"] is True
    assert state["audit_mode"] == AUDIT_MODE
    assert state["audit_scope"] == AUDIT_SCOPE
    assert state["audit_verdict"] == AUDIT_VERDICT
    assert state["real_submission_decision"] == "NOT_AUTHORIZED"
    assert state["real_submission_allowed"] is False
    assert state["fail_closed_required"] is True
    assert state["fail_closed_active"] is True


def test_local_error_pattern_audit_checks_all_pass():
    checks = build_local_error_pattern_audit_checks()
    assert all(checks.values())


def test_each_local_error_pattern_audit_case_passes():
    case_ids = [
        "m10_error_audit_baseline_source_ready_v1",
        "m10_error_audit_fail_closed_preserved_v1",
        "m10_error_audit_color_mapping_pattern_v1",
        "m10_error_audit_object_model_pattern_v1",
        "m10_error_audit_shape_symmetry_pattern_v1",
        "m10_error_audit_cross_family_pattern_v1",
        "m10_error_audit_ranker_pattern_v1",
        "m10_error_audit_traceability_pattern_v1",
        "m10_error_audit_patch_targets_ready_v1",
        "m10_error_audit_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_local_error_pattern_audit_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_local_error_pattern_audit_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_local_error_pattern_audit_case("missing_audit_case")


def test_all_local_error_pattern_audit_cases_pass():
    results = evaluate_all_local_error_pattern_audit_cases()
    assert len(results) == EXPECTED_AUDIT_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_local_error_pattern_audit_record_ready():
    audit = build_milestone_10_local_error_pattern_audit()
    assert audit["status"] == AUDIT_STATUS
    assert audit["audit_mode"] == AUDIT_MODE
    assert audit["audit_scope"] == AUDIT_SCOPE
    assert audit["audit_verdict"] == AUDIT_VERDICT
    assert audit["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert audit["audit_ready"] is True
    assert audit["audit_locked"] is True
    assert audit["local_error_pattern_audit_created"] is True
    assert audit["local_error_pattern_audit_ready"] is True
    assert audit["local_error_pattern_audit_locked"] is True
    assert audit["error_pattern_count"] == EXPECTED_ERROR_PATTERN_COUNT
    assert audit["solver_target_count"] == EXPECTED_SOLVER_TARGET_COUNT
    assert audit["audit_check_count"] == EXPECTED_AUDIT_CHECK_COUNT
    assert audit["audit_case_count"] == EXPECTED_AUDIT_CASE_COUNT
    assert audit["audit_pass_count"] == EXPECTED_AUDIT_PASS_COUNT
    assert audit["audit_failure_count"] == EXPECTED_AUDIT_FAILURE_COUNT
    assert audit["passed_gate_count"] == audit["audit_gate_count"]
    assert audit["audit_issue_count"] == 0


def test_audit_baseline_source_is_hashed():
    source = build_milestone_10_local_error_pattern_audit()["baseline_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_BASELINE_V1_READY"
    assert source["baseline_id"].startswith("MILESTONE-10-LOCAL-SOLVER-BASELINE-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_audit_keeps_real_submission_blocked():
    audit = build_milestone_10_local_error_pattern_audit()
    assert audit["real_submission_decision"] == "NOT_AUTHORIZED"
    assert audit["real_submission_allowed"] is False
    assert audit["manual_upload_allowed"] is False
    assert audit["kaggle_authentication_allowed"] is False
    assert audit["kaggle_submission_sent"] is False
    assert audit["fail_closed_required"] is True
    assert audit["fail_closed_active"] is True


def test_audit_validation_and_pipeline_pass():
    audit = build_milestone_10_local_error_pattern_audit()
    validation = validate_milestone_10_local_error_pattern_audit(audit)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_10_local_error_pattern_audit_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["audit_status"] == AUDIT_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["audit_ready"] is True
    assert payload["audit_pass_count"] == 10
    assert payload["audit_failure_count"] == 0


def test_audit_markdown_and_manifest_contain_markers():
    audit = build_milestone_10_local_error_pattern_audit()
    markdown = render_local_error_pattern_audit_markdown(audit)
    manifest = render_local_error_pattern_audit_manifest(audit)
    assert "ARC_AGI3_MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_ERROR_AUDIT_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_ERROR_PATTERN_COUNT=6" in markdown
    assert "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_ACTIVE=true" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "ERROR_PATTERNS" in manifest
    assert "AUDIT_RESULTS" in manifest
    assert "m10_error_audit_patch_targets_ready_v1" in manifest


def test_audit_writes_artifacts(tmp_path: Path):
    audit = build_milestone_10_local_error_pattern_audit()
    paths = write_local_error_pattern_audit_artifacts(audit, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_10_ERROR_AUDIT_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "LOCAL_ERROR_PATTERN_AUDIT_READY_FOR_SOLVER_PATCH_PLAN" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_audit_metadata_safe():
    metadata = build_milestone_10_local_error_pattern_audit()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_audit_index_is_conservative():
    index = build_milestone_10_local_error_pattern_audit()["audit_index"]
    assert index["audit_ready"] is True
    assert index["local_error_pattern_audit_created"] is True
    assert index["local_error_pattern_audit_ready"] is True
    assert index["error_pattern_count"] == EXPECTED_ERROR_PATTERN_COUNT
    assert index["solver_target_count"] == EXPECTED_SOLVER_TARGET_COUNT
    assert index["next_allowed_stage"] == "MILESTONE_10_TASK_3_SOLVER_PATCH_PLAN_V1"
    assert index["real_submission_decision"] == "NOT_AUTHORIZED"
    assert index["real_submission_allowed"] is False
    assert index["manual_upload_allowed"] is False
    assert index["kaggle_authentication_allowed"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["fail_closed_required"] is True
    assert index["fail_closed_active"] is True
