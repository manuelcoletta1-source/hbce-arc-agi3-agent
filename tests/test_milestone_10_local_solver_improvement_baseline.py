from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_10_local_solver_improvement_baseline import (
    BASELINE_MODE,
    BASELINE_SCOPE,
    BASELINE_STATUS,
    BASELINE_VERDICT,
    EXPECTED_BASELINE_CASE_COUNT,
    EXPECTED_BASELINE_CHECK_COUNT,
    EXPECTED_BASELINE_FAILURE_COUNT,
    EXPECTED_BASELINE_PASS_COUNT,
    EXPECTED_LOCAL_STAGE_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_10_baseline_checks,
    build_milestone_10_local_solver_baseline_state,
    build_milestone_10_local_solver_improvement_baseline,
    build_milestone_10_source_summary,
    evaluate_all_milestone_10_baseline_cases,
    evaluate_milestone_10_baseline_case,
    render_milestone_10_baseline_manifest,
    render_milestone_10_baseline_markdown,
    run_milestone_10_local_solver_improvement_baseline_pipeline,
    validate_milestone_10_local_solver_improvement_baseline,
    write_milestone_10_baseline_artifacts,
)


def test_milestone_10_source_summary_reads_milestone_9_closure():
    summary = build_milestone_10_source_summary()
    assert summary["milestone_9_closure_present"] is True
    assert summary["milestone_9_closure_status"] == "MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_READY"
    assert summary["milestone_9_closure_id"].startswith("MILESTONE-9-BLOCKED-CLOSURE-")
    assert summary["milestone_9_closed"] is True
    assert summary["milestone_9_closure_type"] == "REAL_SUBMISSION_BLOCKED"
    assert summary["real_submission_decision"] == "NOT_AUTHORIZED"
    assert summary["operator_approval_granted"] is False
    assert summary["real_submission_allowed"] is False
    assert summary["kaggle_submission_sent"] is False
    assert Path(summary["candidate_source_path"]).exists()
    assert summary["candidate_id"].startswith("MILESTONE-8-SUBMISSION-REFRESH-")
    assert summary["candidate_signature"]


def test_milestone_10_state_is_local_only_and_fail_closed():
    state = build_milestone_10_local_solver_baseline_state()
    assert state["milestone_10_open"] is True
    assert state["local_solver_improvement_cycle_created"] is True
    assert state["local_solver_improvement_cycle_ready"] is True
    assert state["local_solver_improvement_cycle_locked_to_local_only"] is True
    assert state["real_submission_boundary_status"] == "BLOCKED"
    assert state["real_submission_decision"] == "NOT_AUTHORIZED"
    assert state["real_submission_allowed"] is False
    assert state["kaggle_authentication_allowed"] is False
    assert state["manual_upload_allowed"] is False
    assert state["fail_closed_required"] is True
    assert state["fail_closed_active"] is True
    assert state["local_improvement_stage_count"] == EXPECTED_LOCAL_STAGE_COUNT


def test_milestone_10_checks_all_pass():
    checks = build_milestone_10_baseline_checks()
    assert all(checks.values())


def test_each_milestone_10_baseline_case_passes():
    case_ids = [
        "m10_baseline_m9_closure_source_ready_v1",
        "m10_baseline_submission_still_blocked_v1",
        "m10_baseline_operator_approval_absent_v1",
        "m10_baseline_kaggle_actions_absent_v1",
        "m10_baseline_local_solver_cycle_ready_v1",
        "m10_baseline_local_stage_plan_ready_v1",
        "m10_baseline_next_stage_valid_v1",
        "m10_baseline_fail_closed_preserved_v1",
        "m10_baseline_no_private_core_exposure_v1",
        "m10_baseline_no_legal_certification_v1",
    ]
    for case_id in case_ids:
        result = evaluate_milestone_10_baseline_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_milestone_10_baseline_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_milestone_10_baseline_case("missing_milestone_10_case")


def test_all_milestone_10_baseline_cases_pass():
    results = evaluate_all_milestone_10_baseline_cases()
    assert len(results) == EXPECTED_BASELINE_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_milestone_10_baseline_record_ready():
    baseline = build_milestone_10_local_solver_improvement_baseline()
    assert baseline["status"] == BASELINE_STATUS
    assert baseline["baseline_mode"] == BASELINE_MODE
    assert baseline["baseline_scope"] == BASELINE_SCOPE
    assert baseline["baseline_verdict"] == BASELINE_VERDICT
    assert baseline["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert baseline["baseline_ready"] is True
    assert baseline["baseline_locked"] is True
    assert baseline["milestone_10_open"] is True
    assert baseline["local_solver_improvement_cycle_created"] is True
    assert baseline["local_solver_improvement_cycle_ready"] is True
    assert baseline["local_improvement_stage_count"] == EXPECTED_LOCAL_STAGE_COUNT
    assert baseline["baseline_check_count"] == EXPECTED_BASELINE_CHECK_COUNT
    assert baseline["baseline_case_count"] == EXPECTED_BASELINE_CASE_COUNT
    assert baseline["baseline_pass_count"] == EXPECTED_BASELINE_PASS_COUNT
    assert baseline["baseline_failure_count"] == EXPECTED_BASELINE_FAILURE_COUNT
    assert baseline["passed_gate_count"] == baseline["baseline_gate_count"]
    assert baseline["baseline_issue_count"] == 0


def test_milestone_10_closure_source_is_hashed():
    source = build_milestone_10_local_solver_improvement_baseline()["milestone_9_closure_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_READY"
    assert source["closure_id"].startswith("MILESTONE-9-BLOCKED-CLOSURE-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_milestone_10_keeps_real_submission_blocked():
    baseline = build_milestone_10_local_solver_improvement_baseline()
    assert baseline["real_submission_decision"] == "NOT_AUTHORIZED"
    assert baseline["real_submission_allowed"] is False
    assert baseline["manual_upload_allowed"] is False
    assert baseline["kaggle_authentication_allowed"] is False
    assert baseline["real_submission_created"] is False
    assert baseline["ready_for_real_kaggle_submission"] is False
    assert baseline["kaggle_submission_sent"] is False
    assert baseline["upload_performed"] is False
    assert baseline["kaggle_authentication_performed"] is False
    assert baseline["fail_closed_required"] is True
    assert baseline["fail_closed_active"] is True


def test_milestone_10_validation_and_pipeline_pass():
    baseline = build_milestone_10_local_solver_improvement_baseline()
    validation = validate_milestone_10_local_solver_improvement_baseline(baseline)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_10_local_solver_improvement_baseline_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["baseline_status"] == BASELINE_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["baseline_ready"] is True
    assert payload["baseline_pass_count"] == 10
    assert payload["baseline_failure_count"] == 0


def test_milestone_10_markdown_and_manifest_contain_markers():
    baseline = build_milestone_10_local_solver_improvement_baseline()
    markdown = render_milestone_10_baseline_markdown(baseline)
    manifest = render_milestone_10_baseline_manifest(baseline)
    assert "ARC_AGI3_MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_BASELINE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_OPEN=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_ACTIVE=true" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "LOCAL_IMPROVEMENT_STAGES" in manifest
    assert "BASELINE_RESULTS" in manifest
    assert "m10_baseline_local_solver_cycle_ready_v1" in manifest


def test_milestone_10_writes_artifacts(tmp_path: Path):
    baseline = build_milestone_10_local_solver_improvement_baseline()
    paths = write_milestone_10_baseline_artifacts(baseline, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_BASELINE_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_10_OPEN=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "MILESTONE_10_OPEN_LOCAL_SOLVER_IMPROVEMENT_ONLY_REAL_SUBMISSION_BLOCKED" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_milestone_10_metadata_safe():
    metadata = build_milestone_10_local_solver_improvement_baseline()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_milestone_10_index_is_conservative():
    index = build_milestone_10_local_solver_improvement_baseline()["baseline_index"]
    assert index["baseline_ready"] is True
    assert index["milestone_10_open"] is True
    assert index["local_solver_improvement_cycle_created"] is True
    assert index["local_solver_improvement_cycle_ready"] is True
    assert index["local_improvement_stage_count"] == EXPECTED_LOCAL_STAGE_COUNT
    assert index["next_allowed_stage"] == "MILESTONE_10_TASK_2_LOCAL_ERROR_PATTERN_AUDIT_V1"
    assert index["real_submission_decision"] == "NOT_AUTHORIZED"
    assert index["real_submission_allowed"] is False
    assert index["manual_upload_allowed"] is False
    assert index["kaggle_authentication_allowed"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["fail_closed_required"] is True
    assert index["fail_closed_active"] is True
