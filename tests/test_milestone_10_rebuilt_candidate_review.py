from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_10_rebuilt_candidate_review import (
    EXPECTED_CANDIDATE_PACKAGE_ID,
    EXPECTED_REBUILT_CANDIDATE_ID,
    EXPECTED_REVIEW_CASE_COUNT,
    EXPECTED_REVIEW_CHECK_COUNT,
    EXPECTED_REVIEW_CRITERION_COUNT,
    EXPECTED_REVIEW_FAILURE_COUNT,
    EXPECTED_REVIEW_PASS_COUNT,
    EXPECTED_SELECTED_CANDIDATE_ID,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    REVIEW_MODE,
    REVIEW_SCOPE,
    REVIEW_STATUS,
    REVIEW_VERDICT,
    VALIDATION_STATUS,
    build_milestone_10_rebuilt_candidate_review,
    build_rebuilt_candidate_review_checks,
    build_rebuilt_candidate_review_scorecard,
    build_rebuilt_candidate_review_source_summary,
    build_review_decision,
    build_review_state,
    evaluate_all_rebuilt_candidate_review_cases,
    evaluate_rebuilt_candidate_review_case,
    render_rebuilt_candidate_review_manifest,
    render_rebuilt_candidate_review_markdown,
    run_milestone_10_rebuilt_candidate_review_pipeline,
    validate_milestone_10_rebuilt_candidate_review,
    write_rebuilt_candidate_review_artifacts,
)


def test_rebuilt_candidate_review_source_summary_reads_rebuild():
    summary = build_rebuilt_candidate_review_source_summary()
    assert summary["submission_candidate_rebuild_present"] is True
    assert summary["rebuild_status"] == "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_READY"
    assert summary["submission_candidate_rebuild_id"].startswith(
        "MILESTONE-10-SUBMISSION-CANDIDATE-REBUILD-"
    )
    assert summary["submission_candidate_rebuild_ready"] is True
    assert summary["submission_candidate_rebuild_locked"] is True
    assert summary["next_allowed_stage"] == "MILESTONE_10_TASK_9_REBUILT_CANDIDATE_REVIEW_V1"
    assert summary["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert summary["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
    assert summary["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID
    assert summary["local_candidate_package_rebuilt"] is True
    assert summary["rebuilt_candidate_payload_created"] is True
    assert summary["payload_kind"] == "LOCAL_REBUILT_CANDIDATE_PACKAGE"
    assert summary["payload_ready_for_review"] is True
    assert summary["trace_ready"] is True
    assert summary["review_handoff_created"] is True
    assert summary["real_submission_candidate_created"] is False
    assert summary["submission_json_created"] is False
    assert summary["upload_package_created"] is False
    assert summary["real_submission_decision"] == "NOT_AUTHORIZED"
    assert summary["real_submission_allowed"] is False
    assert summary["fail_closed_active"] is True


def test_review_scorecard_is_complete_and_passes():
    scorecard = build_rebuilt_candidate_review_scorecard()
    assert len(scorecard) == EXPECTED_REVIEW_CRITERION_COUNT
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_review_decision_passes_local_review_only():
    decision = build_review_decision()
    assert decision["decision"] == "PASS_LOCAL_REBUILT_CANDIDATE_REVIEW"
    assert decision["review_passed"] is True
    assert decision["review_ready"] is True
    assert decision["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert decision["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
    assert decision["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID
    assert decision["submission_preparation_closure_required_next"] is True
    assert decision["real_submission_allowed"] is False
    assert decision["manual_upload_allowed"] is False
    assert decision["kaggle_authentication_allowed"] is False
    assert decision["kaggle_submission_allowed"] is False
    assert decision["submission_json_creation_allowed_now"] is False
    assert decision["upload_package_creation_allowed_now"] is False
    assert decision["operator_approval_required_for_real_submission"] is True
    assert decision["next_allowed_stage"] == NEXT_ALLOWED_STAGE


def test_review_state_is_conservative():
    state = build_review_state()
    assert state["rebuilt_candidate_review_required"] is True
    assert state["rebuilt_candidate_review_created"] is True
    assert state["rebuilt_candidate_review_ready"] is True
    assert state["rebuilt_candidate_review_passed"] is True
    assert state["rebuilt_candidate_review_locked"] is True
    assert state["review_mode"] == REVIEW_MODE
    assert state["review_scope"] == REVIEW_SCOPE
    assert state["review_verdict"] == REVIEW_VERDICT
    assert state["review_scorecard_created"] is True
    assert state["review_scorecard_passed"] is True
    assert state["submission_preparation_closure_required_next"] is True
    assert state["real_submission_candidate_created"] is False
    assert state["submission_json_created"] is False
    assert state["upload_package_created"] is False
    assert state["real_submission_allowed"] is False
    assert state["fail_closed_active"] is True


def test_rebuilt_candidate_review_checks_all_pass():
    checks = build_rebuilt_candidate_review_checks()
    assert all(checks.values())


def test_each_rebuilt_candidate_review_case_passes():
    case_ids = [
        "m10_rebuilt_candidate_review_source_ready_v1",
        "m10_rebuilt_candidate_review_identity_valid_v1",
        "m10_rebuilt_candidate_review_payload_ready_v1",
        "m10_rebuilt_candidate_review_scorecard_ready_v1",
        "m10_rebuilt_candidate_review_trace_ready_v1",
        "m10_rebuilt_candidate_review_boundary_preserved_v1",
        "m10_rebuilt_candidate_review_fail_closed_preserved_v1",
        "m10_rebuilt_candidate_review_real_submission_blocked_v1",
        "m10_rebuilt_candidate_review_closure_required_v1",
        "m10_rebuilt_candidate_review_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_rebuilt_candidate_review_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_rebuilt_candidate_review_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_rebuilt_candidate_review_case("missing_rebuilt_candidate_review_case")


def test_all_rebuilt_candidate_review_cases_pass():
    results = evaluate_all_rebuilt_candidate_review_cases()
    assert len(results) == EXPECTED_REVIEW_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_rebuilt_candidate_review_record_ready():
    review = build_milestone_10_rebuilt_candidate_review()
    assert review["status"] == REVIEW_STATUS
    assert review["review_mode"] == REVIEW_MODE
    assert review["review_scope"] == REVIEW_SCOPE
    assert review["review_verdict"] == REVIEW_VERDICT
    assert review["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert review["rebuilt_candidate_review_ready"] is True
    assert review["rebuilt_candidate_review_locked"] is True
    assert review["rebuilt_candidate_review_created"] is True
    assert review["rebuilt_candidate_review_passed"] is True
    assert review["review_scorecard_created"] is True
    assert review["review_scorecard_passed"] is True
    assert review["review_criterion_count"] == EXPECTED_REVIEW_CRITERION_COUNT
    assert review["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert review["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
    assert review["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID
    assert review["review_check_count"] == EXPECTED_REVIEW_CHECK_COUNT
    assert review["review_case_count"] == EXPECTED_REVIEW_CASE_COUNT
    assert review["review_pass_count"] == EXPECTED_REVIEW_PASS_COUNT
    assert review["review_failure_count"] == EXPECTED_REVIEW_FAILURE_COUNT
    assert review["passed_gate_count"] == review["review_gate_count"]
    assert review["review_issue_count"] == 0


def test_submission_candidate_rebuild_source_is_hashed():
    source = build_milestone_10_rebuilt_candidate_review()["submission_candidate_rebuild_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_READY"
    assert source["submission_candidate_rebuild_id"].startswith(
        "MILESTONE-10-SUBMISSION-CANDIDATE-REBUILD-"
    )
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_rebuilt_candidate_review_keeps_submission_blocked():
    review = build_milestone_10_rebuilt_candidate_review()
    assert review["submission_preparation_closure_required_next"] is True
    assert review["real_submission_candidate_created"] is False
    assert review["submission_json_created"] is False
    assert review["upload_package_created"] is False
    assert review["real_submission_decision"] == "NOT_AUTHORIZED"
    assert review["real_submission_allowed"] is False
    assert review["manual_upload_allowed"] is False
    assert review["kaggle_authentication_allowed"] is False
    assert review["kaggle_submission_sent"] is False
    assert review["fail_closed_required"] is True
    assert review["fail_closed_active"] is True


def test_rebuilt_candidate_review_validation_and_pipeline_pass():
    review = build_milestone_10_rebuilt_candidate_review()
    validation = validate_milestone_10_rebuilt_candidate_review(review)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_10_rebuilt_candidate_review_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["review_status"] == REVIEW_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["rebuilt_candidate_review_ready"] is True
    assert payload["review_pass_count"] == 10
    assert payload["review_failure_count"] == 0


def test_rebuilt_candidate_review_markdown_and_manifest_contain_markers():
    review = build_milestone_10_rebuilt_candidate_review()
    markdown = render_rebuilt_candidate_review_markdown(review)
    manifest = render_rebuilt_candidate_review_manifest(review)
    assert "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_REVIEW_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_REVIEW_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_REVIEW_PASSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_REVIEW_SCORECARD_CREATED=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_REVIEW_SCORECARD_PASSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_REQUIRED_NEXT=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_CANDIDATE_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_JSON_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_UPLOAD_PACKAGE_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_ACTIVE=true" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "REVIEW_SCORECARD" in manifest
    assert "REVIEW_VALIDATION_RESULTS" in manifest
    assert "m10_rebuilt_candidate_review_scorecard_ready_v1" in manifest


def test_rebuilt_candidate_review_writes_artifacts(tmp_path: Path):
    review = build_milestone_10_rebuilt_candidate_review()
    paths = write_rebuilt_candidate_review_artifacts(review, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert "MILESTONE_10_REBUILT_CANDIDATE_REVIEW_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_REVIEW_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "REBUILT_CANDIDATE_REVIEW_PASS_READY_FOR_SUBMISSION_PREPARATION_CLOSURE_REAL_SUBMISSION_BLOCKED" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_rebuilt_candidate_review_metadata_safe():
    metadata = build_milestone_10_rebuilt_candidate_review()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_rebuilt_candidate_review_index_is_conservative():
    index = build_milestone_10_rebuilt_candidate_review()["review_index"]
    assert index["rebuilt_candidate_review_ready"] is True
    assert index["rebuilt_candidate_review_created"] is True
    assert index["rebuilt_candidate_review_passed"] is True
    assert index["review_scorecard_created"] is True
    assert index["review_scorecard_passed"] is True
    assert index["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert index["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
    assert index["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID
    assert index["submission_preparation_closure_required_next"] is True
    assert index["next_allowed_stage"] == "MILESTONE_10_TASK_10_SUBMISSION_PREPARATION_CLOSURE_V1"
    assert index["real_submission_candidate_created"] is False
    assert index["submission_json_created"] is False
    assert index["upload_package_created"] is False
    assert index["real_submission_decision"] == "NOT_AUTHORIZED"
    assert index["real_submission_allowed"] is False
    assert index["fail_closed_required"] is True
    assert index["fail_closed_active"] is True
