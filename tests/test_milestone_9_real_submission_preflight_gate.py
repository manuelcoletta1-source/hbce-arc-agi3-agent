from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_9_real_submission_preflight_gate import (
    EXPECTED_PREFLIGHT_CASE_COUNT,
    EXPECTED_PREFLIGHT_CHECK_COUNT,
    EXPECTED_PREFLIGHT_FAILURE_COUNT,
    EXPECTED_PREFLIGHT_PASS_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    PREFLIGHT_MODE,
    PREFLIGHT_SCOPE,
    PREFLIGHT_STATUS,
    PREFLIGHT_VERDICT,
    VALIDATION_STATUS,
    build_milestone_9_real_submission_preflight_gate,
    build_preflight_source_summary,
    build_real_submission_preflight_checks,
    build_real_submission_preflight_state,
    evaluate_all_real_submission_preflight_cases,
    evaluate_real_submission_preflight_case,
    render_real_submission_preflight_gate_manifest,
    render_real_submission_preflight_gate_markdown,
    run_milestone_9_real_submission_preflight_gate_pipeline,
    validate_milestone_9_real_submission_preflight_gate,
    write_real_submission_preflight_gate_artifacts,
)


def test_preflight_source_summary_ready():
    summary = build_preflight_source_summary()
    assert summary["local_review_present"] is True
    assert summary["local_review_status"] == "MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_READY"
    assert summary["local_review_id"].startswith("MILESTONE-9-LOCAL-REVIEW-")
    assert summary["candidate_source_path"]
    assert Path(summary["candidate_source_path"]).exists()
    assert summary["candidate_id"].startswith("MILESTONE-8-SUBMISSION-REFRESH-")
    assert summary["candidate_signature"]
    assert summary["candidate_count"] > 0
    assert summary["review_sha256"] != "MISSING_HASH"


def test_preflight_state_ready_but_closed():
    state = build_real_submission_preflight_state()
    assert state["real_submission_preflight_required"] is True
    assert state["real_submission_preflight_ready"] is True
    assert state["real_submission_preflight_completed"] is False
    assert state["preflight_gate_ready"] is True
    assert state["preflight_gate_open"] is False
    assert state["operator_approval_required"] is True
    assert state["operator_approval_granted"] is False
    assert state["manual_upload_allowed"] is False
    assert state["kaggle_authentication_allowed"] is False
    assert state["real_submission_allowed"] is False


def test_preflight_checks_all_pass():
    checks = build_real_submission_preflight_checks()
    assert all(checks.values())


def test_each_preflight_case_passes():
    case_ids = [
        "preflight_local_review_source_ready_v1",
        "preflight_candidate_source_bound_v1",
        "preflight_candidate_signature_bound_v1",
        "preflight_review_cases_passed_v1",
        "preflight_operator_approval_absent_v1",
        "preflight_manual_upload_blocked_v1",
        "preflight_real_submission_blocked_v1",
        "preflight_no_auth_no_external_api_v1",
        "preflight_no_score_or_leaderboard_claim_v1",
        "preflight_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_real_submission_preflight_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_preflight_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_real_submission_preflight_case("missing_preflight_case")


def test_all_preflight_cases_pass():
    results = evaluate_all_real_submission_preflight_cases()
    assert len(results) == EXPECTED_PREFLIGHT_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_preflight_gate_record_ready():
    preflight = build_milestone_9_real_submission_preflight_gate()
    assert preflight["status"] == PREFLIGHT_STATUS
    assert preflight["preflight_mode"] == PREFLIGHT_MODE
    assert preflight["preflight_scope"] == PREFLIGHT_SCOPE
    assert preflight["preflight_verdict"] == PREFLIGHT_VERDICT
    assert preflight["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert preflight["preflight_ready"] is True
    assert preflight["preflight_locked"] is True
    assert preflight["real_submission_preflight_created"] is True
    assert preflight["real_submission_preflight_ready"] is True
    assert preflight["real_submission_preflight_completed"] is False
    assert preflight["preflight_gate_ready"] is True
    assert preflight["preflight_gate_open"] is False
    assert preflight["candidate_count"] > 0
    assert preflight["preflight_check_count"] == EXPECTED_PREFLIGHT_CHECK_COUNT
    assert preflight["preflight_case_count"] == EXPECTED_PREFLIGHT_CASE_COUNT
    assert preflight["preflight_pass_count"] == EXPECTED_PREFLIGHT_PASS_COUNT
    assert preflight["preflight_failure_count"] == EXPECTED_PREFLIGHT_FAILURE_COUNT
    assert preflight["passed_gate_count"] == preflight["preflight_gate_count"]
    assert preflight["preflight_issue_count"] == 0


def test_local_review_source_is_present_and_hashed():
    source = build_milestone_9_real_submission_preflight_gate()["local_review_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_READY"
    assert source["review_id"].startswith("MILESTONE-9-LOCAL-REVIEW-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_preflight_keeps_submission_blocked():
    preflight = build_milestone_9_real_submission_preflight_gate()
    assert preflight["operator_approval_required"] is True
    assert preflight["operator_approval_granted"] is False
    assert preflight["operator_approval_received"] is False
    assert preflight["manual_upload_allowed"] is False
    assert preflight["kaggle_authentication_allowed"] is False
    assert preflight["real_submission_created"] is False
    assert preflight["real_submission_allowed"] is False
    assert preflight["ready_for_real_kaggle_submission"] is False
    assert preflight["kaggle_submission_sent"] is False
    assert preflight["upload_performed"] is False
    assert preflight["kaggle_authentication_performed"] is False


def test_preflight_gates_and_issues_are_clean():
    preflight = build_milestone_9_real_submission_preflight_gate()
    assert all(item["passed"] is True for item in preflight["preflight_gates"])
    assert all(item["active"] is False for item in preflight["preflight_issues"])


def test_preflight_validation_and_pipeline_pass():
    preflight = build_milestone_9_real_submission_preflight_gate()
    validation = validate_milestone_9_real_submission_preflight_gate(preflight)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_9_real_submission_preflight_gate_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["preflight_status"] == PREFLIGHT_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["preflight_ready"] is True
    assert payload["preflight_pass_count"] == 10
    assert payload["preflight_failure_count"] == 0


def test_preflight_markdown_and_manifest_contain_markers():
    preflight = build_milestone_9_real_submission_preflight_gate()
    markdown = render_real_submission_preflight_gate_markdown(preflight)
    manifest = render_real_submission_preflight_gate_manifest(preflight)
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_PREFLIGHT_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_PREFLIGHT_GATE_OPEN=false" in markdown
    assert "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GRANTED=false" in markdown
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "PREFLIGHT_CHECKS" in manifest
    assert "PREFLIGHT_RESULTS" in manifest
    assert "preflight_real_submission_blocked_v1" in manifest


def test_preflight_writes_artifacts(tmp_path: Path):
    preflight = build_milestone_9_real_submission_preflight_gate()
    paths = write_real_submission_preflight_gate_artifacts(preflight, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "REAL_SUBMISSION_PREFLIGHT_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_preflight_metadata_safe():
    metadata = build_milestone_9_real_submission_preflight_gate()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_preflight_index_is_conservative():
    index = build_milestone_9_real_submission_preflight_gate()["preflight_index"]
    assert index["preflight_ready"] is True
    assert index["preflight_locked"] is True
    assert index["real_submission_preflight_created"] is True
    assert index["real_submission_preflight_completed"] is False
    assert index["preflight_gate_open"] is False
    assert index["operator_approval_required"] is True
    assert index["operator_approval_granted"] is False
    assert index["operator_approval_received"] is False
    assert index["manual_upload_allowed"] is False
    assert index["kaggle_authentication_allowed"] is False
    assert index["real_submission_allowed"] is False
    assert index["ready_for_real_kaggle_submission"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["upload_performed"] is False
    assert index["kaggle_authentication_performed"] is False
