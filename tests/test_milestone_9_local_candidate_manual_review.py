from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_9_local_candidate_manual_review import (
    EXPECTED_REVIEW_CASE_COUNT,
    EXPECTED_REVIEW_CHECK_COUNT,
    EXPECTED_REVIEW_FAILURE_COUNT,
    EXPECTED_REVIEW_PASS_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    REVIEW_MODE,
    REVIEW_SCOPE,
    REVIEW_STATUS,
    REVIEW_VERDICT,
    VALIDATION_STATUS,
    build_candidate_source_summary,
    build_local_candidate_manual_review_checks,
    build_manual_review_state,
    build_milestone_9_local_candidate_manual_review,
    evaluate_all_local_candidate_manual_review_cases,
    evaluate_local_candidate_manual_review_case,
    render_local_candidate_manual_review_manifest,
    render_local_candidate_manual_review_markdown,
    resolve_candidate_source_path,
    run_milestone_9_local_candidate_manual_review_pipeline,
    validate_milestone_9_local_candidate_manual_review,
    write_local_candidate_manual_review_artifacts,
)


def test_candidate_source_resolves_to_existing_file():
    path = resolve_candidate_source_path()
    assert path.exists()
    assert "candidate" in path.name.lower()


def test_candidate_source_summary_ready():
    summary = build_candidate_source_summary()
    assert summary["present"] is True
    assert summary["candidate_id"] != "MISSING_CANDIDATE_ID"
    assert summary["signature"]
    assert summary["candidate_count"] > 0
    assert summary["sha256"] != "MISSING_HASH"
    assert summary["sha256_16"] != "MISSING_HASH"


def test_manual_review_state_is_ready_but_not_completed():
    state = build_manual_review_state()
    assert state["local_candidate_manual_review_required"] is True
    assert state["local_candidate_manual_review_ready"] is True
    assert state["local_candidate_manual_review_completed"] is False
    assert state["operator_approval_required"] is True
    assert state["operator_approval_granted"] is False
    assert state["operator_approval_received"] is False
    assert state["manual_upload_allowed"] is False


def test_local_candidate_manual_review_checks_all_pass():
    checks = build_local_candidate_manual_review_checks()
    assert all(checks.values())


def test_each_local_candidate_manual_review_case_passes():
    case_ids = [
        "review_operator_declaration_package_source_ready_v1",
        "review_local_candidate_source_ready_v1",
        "review_candidate_artifacts_available_v1",
        "review_candidate_payload_signature_present_v1",
        "review_declarations_still_empty_v1",
        "review_operator_approval_not_granted_v1",
        "review_real_submission_blocked_v1",
        "review_no_upload_no_auth_v1",
        "review_no_score_or_leaderboard_claim_v1",
        "review_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_local_candidate_manual_review_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_local_candidate_manual_review_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_local_candidate_manual_review_case("missing_review_case")


def test_all_local_candidate_manual_review_cases_pass():
    results = evaluate_all_local_candidate_manual_review_cases()
    assert len(results) == EXPECTED_REVIEW_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_local_candidate_manual_review_record_ready():
    review = build_milestone_9_local_candidate_manual_review()
    assert review["status"] == REVIEW_STATUS
    assert review["review_mode"] == REVIEW_MODE
    assert review["review_scope"] == REVIEW_SCOPE
    assert review["review_verdict"] == REVIEW_VERDICT
    assert review["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert review["review_ready"] is True
    assert review["review_locked"] is True
    assert review["local_candidate_manual_review_created"] is True
    assert review["local_candidate_manual_review_ready"] is True
    assert review["local_candidate_manual_review_completed"] is False
    assert review["review_check_count"] == EXPECTED_REVIEW_CHECK_COUNT
    assert review["review_case_count"] == EXPECTED_REVIEW_CASE_COUNT
    assert review["review_pass_count"] == EXPECTED_REVIEW_PASS_COUNT
    assert review["review_failure_count"] == EXPECTED_REVIEW_FAILURE_COUNT
    assert review["candidate_count"] > 0
    assert review["passed_gate_count"] == review["review_gate_count"]
    assert review["review_issue_count"] == 0


def test_declaration_package_source_is_present_and_hashed():
    source = build_milestone_9_local_candidate_manual_review()["declaration_package_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_READY"
    assert source["package_id"].startswith("MILESTONE-9-DECLARATION-PACKAGE-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_local_candidate_review_keeps_submission_blocked():
    review = build_milestone_9_local_candidate_manual_review()
    assert review["operator_approval_required"] is True
    assert review["operator_approval_granted"] is False
    assert review["operator_approval_received"] is False
    assert review["manual_upload_allowed"] is False
    assert review["real_submission_created"] is False
    assert review["real_submission_allowed"] is False
    assert review["ready_for_real_kaggle_submission"] is False
    assert review["kaggle_submission_sent"] is False
    assert review["upload_performed"] is False
    assert review["kaggle_authentication_performed"] is False


def test_local_candidate_review_gates_and_issues_are_clean():
    review = build_milestone_9_local_candidate_manual_review()
    assert all(item["passed"] is True for item in review["review_gates"])
    assert all(item["active"] is False for item in review["review_issues"])


def test_local_candidate_review_validation_and_pipeline_pass():
    review = build_milestone_9_local_candidate_manual_review()
    validation = validate_milestone_9_local_candidate_manual_review(review)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_9_local_candidate_manual_review_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["review_status"] == REVIEW_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["review_ready"] is True
    assert payload["review_pass_count"] == 10
    assert payload["review_failure_count"] == 0


def test_local_candidate_review_markdown_and_manifest_contain_markers():
    review = build_milestone_9_local_candidate_manual_review()
    markdown = render_local_candidate_manual_review_markdown(review)
    manifest = render_local_candidate_manual_review_manifest(review)
    assert "ARC_AGI3_MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_LOCAL_CANDIDATE_REVIEW_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_COMPLETED=false" in markdown
    assert "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GRANTED=false" in markdown
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "REVIEW_CHECKS" in manifest
    assert "REVIEW_RESULTS" in manifest
    assert "review_real_submission_blocked_v1" in manifest


def test_local_candidate_review_writes_artifacts(tmp_path: Path):
    review = build_milestone_9_local_candidate_manual_review()
    paths = write_local_candidate_manual_review_artifacts(review, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "LOCAL_CANDIDATE_MANUAL_REVIEW_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_local_candidate_review_metadata_safe():
    metadata = build_milestone_9_local_candidate_manual_review()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_local_candidate_review_index_is_conservative():
    index = build_milestone_9_local_candidate_manual_review()["review_index"]
    assert index["review_ready"] is True
    assert index["review_locked"] is True
    assert index["local_candidate_manual_review_created"] is True
    assert index["local_candidate_manual_review_completed"] is False
    assert index["operator_approval_required"] is True
    assert index["operator_approval_granted"] is False
    assert index["operator_approval_received"] is False
    assert index["manual_upload_allowed"] is False
    assert index["real_submission_allowed"] is False
    assert index["ready_for_real_kaggle_submission"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["upload_performed"] is False
    assert index["kaggle_authentication_performed"] is False
