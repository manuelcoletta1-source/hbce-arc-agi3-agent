from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_9_real_submission_blocked_closure import (
    CLOSURE_MODE,
    CLOSURE_SCOPE,
    CLOSURE_STATUS,
    CLOSURE_VERDICT,
    EXPECTED_ACCEPTED_DECLARATION_COUNT,
    EXPECTED_CLOSURE_CASE_COUNT,
    EXPECTED_CLOSURE_CHECK_COUNT,
    EXPECTED_CLOSURE_FAILURE_COUNT,
    EXPECTED_CLOSURE_PASS_COUNT,
    EXPECTED_PROVIDED_DECLARATION_COUNT,
    EXPECTED_REQUIRED_DECLARATION_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_closure_source_summary,
    build_milestone_9_real_submission_blocked_closure,
    build_real_submission_blocked_closure_checks,
    build_real_submission_blocked_closure_state,
    evaluate_all_real_submission_blocked_closure_cases,
    evaluate_real_submission_blocked_closure_case,
    render_real_submission_blocked_closure_manifest,
    render_real_submission_blocked_closure_markdown,
    run_milestone_9_real_submission_blocked_closure_pipeline,
    validate_milestone_9_real_submission_blocked_closure,
    write_real_submission_blocked_closure_artifacts,
)


def test_closure_source_summary_ready():
    summary = build_closure_source_summary()
    assert summary["decision_record_present"] is True
    assert summary["decision_record_status"] == "MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_READY"
    assert summary["decision_id"].startswith("MILESTONE-9-DECISION-RECORD-")
    assert summary["decision_ready"] is True
    assert summary["decision_locked"] is True
    assert summary["real_submission_decision_record_ready"] is True
    assert summary["real_submission_decision"] == "NOT_AUTHORIZED"
    assert summary["real_submission_decision_reason"] == "OPERATOR_APPROVAL_NOT_GRANTED"
    assert Path(summary["candidate_source_path"]).exists()
    assert summary["candidate_id"].startswith("MILESTONE-8-SUBMISSION-REFRESH-")
    assert summary["candidate_signature"]
    assert summary["candidate_count"] > 0
    assert summary["required_declaration_count"] == EXPECTED_REQUIRED_DECLARATION_COUNT
    assert summary["provided_declaration_count"] == EXPECTED_PROVIDED_DECLARATION_COUNT
    assert summary["accepted_declaration_count"] == EXPECTED_ACCEPTED_DECLARATION_COUNT


def test_closure_state_records_blocked_closure():
    state = build_real_submission_blocked_closure_state()
    assert state["real_submission_blocked_closure_required"] is True
    assert state["real_submission_blocked_closure_created"] is True
    assert state["real_submission_blocked_closure_ready"] is True
    assert state["real_submission_blocked_closure_locked"] is True
    assert state["milestone_9_closed"] is True
    assert state["milestone_9_closure_type"] == "REAL_SUBMISSION_BLOCKED"
    assert state["milestone_9_closure_reason"] == "OPERATOR_APPROVAL_NOT_GRANTED"
    assert state["milestone_9_closure_verdict"] == "CLOSED_WITH_REAL_SUBMISSION_BLOCKED"
    assert state["real_submission_decision"] == "NOT_AUTHORIZED"
    assert state["manual_upload_decision"] == "BLOCKED"
    assert state["kaggle_authentication_decision"] == "BLOCKED"
    assert state["real_submission_allowed"] is False


def test_closure_checks_all_pass():
    checks = build_real_submission_blocked_closure_checks()
    assert all(checks.values())


def test_each_closure_case_passes():
    case_ids = [
        "closure_decision_record_source_ready_v1",
        "closure_decision_not_authorized_v1",
        "closure_declarations_absent_v1",
        "closure_explicit_operator_approval_absent_v1",
        "closure_operator_approval_not_granted_v1",
        "closure_real_submission_blocked_v1",
        "closure_no_upload_no_auth_v1",
        "closure_no_score_or_leaderboard_claim_v1",
        "closure_milestone_9_closed_blocked_v1",
        "closure_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_real_submission_blocked_closure_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_closure_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_real_submission_blocked_closure_case("missing_closure_case")


def test_all_closure_cases_pass():
    results = evaluate_all_real_submission_blocked_closure_cases()
    assert len(results) == EXPECTED_CLOSURE_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_real_submission_blocked_closure_record_ready():
    closure = build_milestone_9_real_submission_blocked_closure()
    assert closure["status"] == CLOSURE_STATUS
    assert closure["closure_mode"] == CLOSURE_MODE
    assert closure["closure_scope"] == CLOSURE_SCOPE
    assert closure["closure_verdict"] == CLOSURE_VERDICT
    assert closure["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert closure["closure_ready"] is True
    assert closure["closure_locked"] is True
    assert closure["real_submission_blocked_closure_created"] is True
    assert closure["real_submission_blocked_closure_ready"] is True
    assert closure["real_submission_blocked_closure_locked"] is True
    assert closure["milestone_9_closed"] is True
    assert closure["milestone_9_closure_type"] == "REAL_SUBMISSION_BLOCKED"
    assert closure["real_submission_decision"] == "NOT_AUTHORIZED"
    assert closure["closure_check_count"] == EXPECTED_CLOSURE_CHECK_COUNT
    assert closure["closure_case_count"] == EXPECTED_CLOSURE_CASE_COUNT
    assert closure["closure_pass_count"] == EXPECTED_CLOSURE_PASS_COUNT
    assert closure["closure_failure_count"] == EXPECTED_CLOSURE_FAILURE_COUNT
    assert closure["passed_gate_count"] == closure["closure_gate_count"]
    assert closure["closure_issue_count"] == 0


def test_decision_record_source_is_present_and_hashed():
    source = build_milestone_9_real_submission_blocked_closure()["decision_record_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_READY"
    assert source["decision_id"].startswith("MILESTONE-9-DECISION-RECORD-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_closure_keeps_submission_blocked():
    closure = build_milestone_9_real_submission_blocked_closure()
    assert closure["operator_approval_required"] is True
    assert closure["operator_approval_granted"] is False
    assert closure["operator_approval_received"] is False
    assert closure["explicit_operator_approval_phrase_received"] is False
    assert closure["manual_upload_allowed"] is False
    assert closure["kaggle_authentication_allowed"] is False
    assert closure["real_submission_created"] is False
    assert closure["real_submission_allowed"] is False
    assert closure["ready_for_real_kaggle_submission"] is False
    assert closure["kaggle_submission_sent"] is False
    assert closure["upload_performed"] is False
    assert closure["kaggle_authentication_performed"] is False


def test_closure_gates_and_issues_are_clean():
    closure = build_milestone_9_real_submission_blocked_closure()
    assert all(item["passed"] is True for item in closure["closure_gates"])
    assert all(item["active"] is False for item in closure["closure_issues"])


def test_closure_validation_and_pipeline_pass():
    closure = build_milestone_9_real_submission_blocked_closure()
    validation = validate_milestone_9_real_submission_blocked_closure(closure)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_9_real_submission_blocked_closure_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["closure_status"] == CLOSURE_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["closure_ready"] is True
    assert payload["closure_pass_count"] == 10
    assert payload["closure_failure_count"] == 0


def test_closure_markdown_and_manifest_contain_markers():
    closure = build_milestone_9_real_submission_blocked_closure()
    markdown = render_real_submission_blocked_closure_markdown(closure)
    manifest = render_real_submission_blocked_closure_manifest(closure)
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_CLOSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_CLOSURE_TYPE=REAL_SUBMISSION_BLOCKED" in markdown
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_DECISION=NOT_AUTHORIZED" in markdown
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "CLOSURE_CHECKS" in manifest
    assert "CLOSURE_RESULTS" in manifest
    assert "closure_milestone_9_closed_blocked_v1" in manifest


def test_closure_writes_artifacts(tmp_path: Path):
    closure = build_milestone_9_real_submission_blocked_closure()
    paths = write_real_submission_blocked_closure_artifacts(closure, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "MILESTONE_9_CLOSED_REAL_SUBMISSION_BLOCKED_NO_KAGGLE_ACTION" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_closure_metadata_safe():
    metadata = build_milestone_9_real_submission_blocked_closure()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_closure_index_is_conservative():
    index = build_milestone_9_real_submission_blocked_closure()["closure_index"]
    assert index["closure_ready"] is True
    assert index["closure_locked"] is True
    assert index["real_submission_blocked_closure_created"] is True
    assert index["milestone_9_closed"] is True
    assert index["milestone_9_closure_type"] == "REAL_SUBMISSION_BLOCKED"
    assert index["real_submission_decision"] == "NOT_AUTHORIZED"
    assert index["real_submission_decision_reason"] == "OPERATOR_APPROVAL_NOT_GRANTED"
    assert index["provided_declaration_count"] == 0
    assert index["accepted_declaration_count"] == 0
    assert index["explicit_operator_approval_phrase_received"] is False
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
