from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_10_submission_preparation_closure import (
    CLOSURE_MODE,
    CLOSURE_SCOPE,
    CLOSURE_STATUS,
    CLOSURE_VERDICT,
    EXPECTED_CANDIDATE_PACKAGE_ID,
    EXPECTED_CLOSURE_CASE_COUNT,
    EXPECTED_CLOSURE_CHECK_COUNT,
    EXPECTED_CLOSURE_CRITERION_COUNT,
    EXPECTED_CLOSURE_FAILURE_COUNT,
    EXPECTED_CLOSURE_PASS_COUNT,
    EXPECTED_REBUILT_CANDIDATE_ID,
    EXPECTED_REVIEW_ID,
    EXPECTED_SELECTED_CANDIDATE_ID,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_closure_decision,
    build_closure_scorecard,
    build_closure_state,
    build_milestone_10_submission_preparation_closure,
    build_submission_preparation_closure_checks,
    build_submission_preparation_closure_source_summary,
    evaluate_all_submission_preparation_closure_cases,
    evaluate_submission_preparation_closure_case,
    render_submission_preparation_closure_manifest,
    render_submission_preparation_closure_markdown,
    run_milestone_10_submission_preparation_closure_pipeline,
    validate_milestone_10_submission_preparation_closure,
    write_submission_preparation_closure_artifacts,
)


def test_submission_preparation_closure_source_summary_reads_review():
    summary = build_submission_preparation_closure_source_summary()
    assert summary["review_present"] is True
    assert summary["review_status"] == "MILESTONE_10_REBUILT_CANDIDATE_REVIEW_V1_READY"
    assert summary["rebuilt_candidate_review_id"] == EXPECTED_REVIEW_ID
    assert summary["rebuilt_candidate_review_ready"] is True
    assert summary["rebuilt_candidate_review_locked"] is True
    assert summary["rebuilt_candidate_review_passed"] is True
    assert summary["next_allowed_stage"] == "MILESTONE_10_TASK_10_SUBMISSION_PREPARATION_CLOSURE_V1"
    assert summary["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert summary["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
    assert summary["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID
    assert summary["review_scorecard_created"] is True
    assert summary["review_scorecard_passed"] is True
    assert summary["submission_preparation_closure_required_next"] is True
    assert summary["real_submission_candidate_created"] is False
    assert summary["submission_json_created"] is False
    assert summary["upload_package_created"] is False
    assert summary["real_submission_decision"] == "NOT_AUTHORIZED"
    assert summary["real_submission_allowed"] is False
    assert summary["fail_closed_active"] is True


def test_closure_scorecard_is_complete_and_passes():
    scorecard = build_closure_scorecard()
    assert len(scorecard) == EXPECTED_CLOSURE_CRITERION_COUNT
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_closure_decision_passes_local_closure_only():
    decision = build_closure_decision()
    assert decision["decision"] == "PASS_LOCAL_SUBMISSION_PREPARATION_CLOSURE"
    assert decision["closure_passed"] is True
    assert decision["closure_ready"] is True
    assert decision["milestone_10_closed"] is True
    assert decision["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert decision["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
    assert decision["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID
    assert decision["rebuilt_candidate_review_id"] == EXPECTED_REVIEW_ID
    assert decision["real_submission_allowed"] is False
    assert decision["manual_upload_allowed"] is False
    assert decision["kaggle_authentication_allowed"] is False
    assert decision["kaggle_submission_allowed"] is False
    assert decision["submission_json_creation_allowed_now"] is False
    assert decision["upload_package_creation_allowed_now"] is False
    assert decision["operator_decision_required_for_any_real_submission"] is True
    assert decision["next_allowed_stage"] == NEXT_ALLOWED_STAGE


def test_closure_state_is_conservative():
    state = build_closure_state()
    assert state["submission_preparation_closure_required"] is True
    assert state["submission_preparation_closure_created"] is True
    assert state["submission_preparation_closure_ready"] is True
    assert state["submission_preparation_closure_passed"] is True
    assert state["submission_preparation_closure_locked"] is True
    assert state["closure_mode"] == CLOSURE_MODE
    assert state["closure_scope"] == CLOSURE_SCOPE
    assert state["closure_verdict"] == CLOSURE_VERDICT
    assert state["closure_scorecard_created"] is True
    assert state["closure_scorecard_passed"] is True
    assert state["closure_report_created"] is True
    assert state["closure_manifest_created"] is True
    assert state["closure_index_created"] is True
    assert state["closure_chain_locked"] is True
    assert state["milestone_10_closed"] is True
    assert state["local_package_prepared"] is True
    assert state["local_package_frozen"] is True
    assert state["integrity_verified"] is True
    assert state["final_audit_passed"] is True
    assert state["real_submission_candidate_created"] is False
    assert state["submission_json_created"] is False
    assert state["upload_package_created"] is False
    assert state["real_submission_allowed"] is False
    assert state["fail_closed_active"] is True


def test_submission_preparation_closure_checks_all_pass():
    checks = build_submission_preparation_closure_checks()
    assert all(checks.values())


def test_each_submission_preparation_closure_case_passes():
    case_ids = [
        "m10_submission_preparation_closure_review_source_ready_v1",
        "m10_submission_preparation_closure_identity_locked_v1",
        "m10_submission_preparation_closure_scorecard_passed_v1",
        "m10_submission_preparation_closure_package_frozen_v1",
        "m10_submission_preparation_closure_integrity_verified_v1",
        "m10_submission_preparation_closure_boundary_preserved_v1",
        "m10_submission_preparation_closure_fail_closed_preserved_v1",
        "m10_submission_preparation_closure_real_submission_blocked_v1",
        "m10_submission_preparation_closure_milestone_closed_v1",
        "m10_submission_preparation_closure_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_submission_preparation_closure_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_submission_preparation_closure_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_submission_preparation_closure_case("missing_submission_preparation_closure_case")


def test_all_submission_preparation_closure_cases_pass():
    results = evaluate_all_submission_preparation_closure_cases()
    assert len(results) == EXPECTED_CLOSURE_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_submission_preparation_closure_record_ready():
    closure = build_milestone_10_submission_preparation_closure()
    assert closure["status"] == CLOSURE_STATUS
    assert closure["closure_mode"] == CLOSURE_MODE
    assert closure["closure_scope"] == CLOSURE_SCOPE
    assert closure["closure_verdict"] == CLOSURE_VERDICT
    assert closure["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert closure["submission_preparation_closure_ready"] is True
    assert closure["submission_preparation_closure_locked"] is True
    assert closure["submission_preparation_closure_created"] is True
    assert closure["submission_preparation_closure_passed"] is True
    assert closure["closure_scorecard_created"] is True
    assert closure["closure_scorecard_passed"] is True
    assert closure["closure_criterion_count"] == EXPECTED_CLOSURE_CRITERION_COUNT
    assert closure["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert closure["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
    assert closure["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID
    assert closure["rebuilt_candidate_review_id"] == EXPECTED_REVIEW_ID
    assert closure["closure_check_count"] == EXPECTED_CLOSURE_CHECK_COUNT
    assert closure["closure_case_count"] == EXPECTED_CLOSURE_CASE_COUNT
    assert closure["closure_pass_count"] == EXPECTED_CLOSURE_PASS_COUNT
    assert closure["closure_failure_count"] == EXPECTED_CLOSURE_FAILURE_COUNT
    assert closure["passed_gate_count"] == closure["closure_gate_count"]
    assert closure["closure_issue_count"] == 0


def test_rebuilt_candidate_review_source_is_hashed():
    source = build_milestone_10_submission_preparation_closure()["rebuilt_candidate_review_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_10_REBUILT_CANDIDATE_REVIEW_V1_READY"
    assert source["rebuilt_candidate_review_id"] == EXPECTED_REVIEW_ID
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_submission_preparation_closure_keeps_submission_blocked():
    closure = build_milestone_10_submission_preparation_closure()
    assert closure["milestone_10_closed"] is True
    assert closure["local_package_prepared"] is True
    assert closure["local_package_frozen"] is True
    assert closure["integrity_verified"] is True
    assert closure["final_audit_passed"] is True
    assert closure["real_submission_candidate_created"] is False
    assert closure["submission_json_created"] is False
    assert closure["upload_package_created"] is False
    assert closure["real_submission_decision"] == "NOT_AUTHORIZED"
    assert closure["real_submission_allowed"] is False
    assert closure["manual_upload_allowed"] is False
    assert closure["kaggle_authentication_allowed"] is False
    assert closure["kaggle_submission_sent"] is False
    assert closure["fail_closed_required"] is True
    assert closure["fail_closed_active"] is True


def test_submission_preparation_closure_validation_and_pipeline_pass():
    closure = build_milestone_10_submission_preparation_closure()
    validation = validate_milestone_10_submission_preparation_closure(closure)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_10_submission_preparation_closure_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["closure_status"] == CLOSURE_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["submission_preparation_closure_ready"] is True
    assert payload["closure_pass_count"] == 10
    assert payload["closure_failure_count"] == 0


def test_submission_preparation_closure_markdown_and_manifest_contain_markers():
    closure = build_milestone_10_submission_preparation_closure()
    markdown = render_submission_preparation_closure_markdown(closure)
    manifest = render_submission_preparation_closure_manifest(closure)
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_PASSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_MILESTONE_CLOSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_LOCAL_PACKAGE_PREPARED=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_LOCAL_PACKAGE_FROZEN=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_INTEGRITY_VERIFIED=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_CANDIDATE_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_JSON_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_UPLOAD_PACKAGE_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_ACTIVE=true" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "CLOSURE_SCORECARD" in manifest
    assert "CLOSURE_VALIDATION_RESULTS" in manifest
    assert "m10_submission_preparation_closure_milestone_closed_v1" in manifest


def test_submission_preparation_closure_writes_artifacts(tmp_path: Path):
    closure = build_milestone_10_submission_preparation_closure()
    paths = write_submission_preparation_closure_artifacts(closure, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert Path(paths["report_path"]).exists()
    assert "MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "SUBMISSION_PREPARATION_CLOSURE_PASS_MILESTONE_10_CLOSED_REAL_SUBMISSION_BLOCKED" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_submission_preparation_closure_metadata_safe():
    metadata = build_milestone_10_submission_preparation_closure()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_submission_preparation_closure_index_is_conservative():
    index = build_milestone_10_submission_preparation_closure()["closure_index"]
    assert index["submission_preparation_closure_ready"] is True
    assert index["submission_preparation_closure_created"] is True
    assert index["submission_preparation_closure_passed"] is True
    assert index["closure_scorecard_created"] is True
    assert index["closure_scorecard_passed"] is True
    assert index["milestone_10_closed"] is True
    assert index["local_package_prepared"] is True
    assert index["local_package_frozen"] is True
    assert index["integrity_verified"] is True
    assert index["final_audit_passed"] is True
    assert index["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert index["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
    assert index["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID
    assert index["next_allowed_stage"] == "MILESTONE_10_CLOSED_REAL_SUBMISSION_BLOCKED_OPERATOR_DECISION_REQUIRED"
    assert index["real_submission_candidate_created"] is False
    assert index["submission_json_created"] is False
    assert index["upload_package_created"] is False
    assert index["real_submission_decision"] == "NOT_AUTHORIZED"
    assert index["real_submission_allowed"] is False
    assert index["fail_closed_required"] is True
    assert index["fail_closed_active"] is True
