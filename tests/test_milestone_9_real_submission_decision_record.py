from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_9_real_submission_decision_record import (
    DECISION_MODE,
    DECISION_SCOPE,
    DECISION_STATUS,
    DECISION_VERDICT,
    EXPECTED_ACCEPTED_DECLARATION_COUNT,
    EXPECTED_DECISION_CASE_COUNT,
    EXPECTED_DECISION_CHECK_COUNT,
    EXPECTED_DECISION_FAILURE_COUNT,
    EXPECTED_DECISION_PASS_COUNT,
    EXPECTED_PROVIDED_DECLARATION_COUNT,
    EXPECTED_REQUIRED_DECLARATION_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_decision_source_summary,
    build_milestone_9_real_submission_decision_record,
    build_real_submission_decision_checks,
    build_real_submission_decision_state,
    evaluate_all_real_submission_decision_cases,
    evaluate_real_submission_decision_case,
    render_real_submission_decision_record_manifest,
    render_real_submission_decision_record_markdown,
    run_milestone_9_real_submission_decision_record_pipeline,
    validate_milestone_9_real_submission_decision_record,
    write_real_submission_decision_record_artifacts,
)


def test_decision_source_summary_ready():
    summary = build_decision_source_summary()
    assert summary["approval_gate_present"] is True
    assert summary["approval_gate_status"] == "MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_READY"
    assert summary["approval_id"].startswith("MILESTONE-9-APPROVAL-GATE-")
    assert summary["approval_ready"] is True
    assert summary["approval_locked"] is True
    assert summary["operator_approval_gate_ready"] is True
    assert summary["operator_approval_gate_open"] is False
    assert Path(summary["candidate_source_path"]).exists()
    assert summary["candidate_id"].startswith("MILESTONE-8-SUBMISSION-REFRESH-")
    assert summary["candidate_signature"]
    assert summary["candidate_count"] > 0
    assert summary["required_declaration_count"] == EXPECTED_REQUIRED_DECLARATION_COUNT
    assert summary["provided_declaration_count"] == EXPECTED_PROVIDED_DECLARATION_COUNT
    assert summary["accepted_declaration_count"] == EXPECTED_ACCEPTED_DECLARATION_COUNT


def test_decision_state_records_not_authorized():
    state = build_real_submission_decision_state()
    assert state["real_submission_decision_record_required"] is True
    assert state["real_submission_decision_record_created"] is True
    assert state["real_submission_decision_record_ready"] is True
    assert state["real_submission_decision_record_locked"] is True
    assert state["real_submission_decision"] == "NOT_AUTHORIZED"
    assert state["real_submission_decision_reason"] == "OPERATOR_APPROVAL_NOT_GRANTED"
    assert state["real_submission_decision_verdict"] == "SUBMISSION_BLOCKED_OPERATOR_APPROVAL_ABSENT"
    assert state["operator_approval_required"] is True
    assert state["operator_approval_granted"] is False
    assert state["manual_upload_decision"] == "BLOCKED"
    assert state["kaggle_authentication_decision"] == "BLOCKED"
    assert state["real_submission_allowed"] is False


def test_decision_checks_all_pass():
    checks = build_real_submission_decision_checks()
    assert all(checks.values())


def test_each_decision_case_passes():
    case_ids = [
        "decision_approval_gate_source_ready_v1",
        "decision_required_declarations_present_v1",
        "decision_no_declarations_accepted_v1",
        "decision_explicit_operator_approval_absent_v1",
        "decision_operator_approval_not_granted_v1",
        "decision_real_submission_not_authorized_v1",
        "decision_manual_upload_blocked_v1",
        "decision_no_auth_no_upload_v1",
        "decision_no_score_or_leaderboard_claim_v1",
        "decision_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_real_submission_decision_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_decision_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_real_submission_decision_case("missing_decision_case")


def test_all_decision_cases_pass():
    results = evaluate_all_real_submission_decision_cases()
    assert len(results) == EXPECTED_DECISION_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_real_submission_decision_record_ready():
    decision = build_milestone_9_real_submission_decision_record()
    assert decision["status"] == DECISION_STATUS
    assert decision["decision_mode"] == DECISION_MODE
    assert decision["decision_scope"] == DECISION_SCOPE
    assert decision["decision_verdict"] == DECISION_VERDICT
    assert decision["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert decision["decision_ready"] is True
    assert decision["decision_locked"] is True
    assert decision["real_submission_decision_record_created"] is True
    assert decision["real_submission_decision_record_ready"] is True
    assert decision["real_submission_decision_record_locked"] is True
    assert decision["real_submission_decision"] == "NOT_AUTHORIZED"
    assert decision["real_submission_decision_reason"] == "OPERATOR_APPROVAL_NOT_GRANTED"
    assert decision["decision_check_count"] == EXPECTED_DECISION_CHECK_COUNT
    assert decision["decision_case_count"] == EXPECTED_DECISION_CASE_COUNT
    assert decision["decision_pass_count"] == EXPECTED_DECISION_PASS_COUNT
    assert decision["decision_failure_count"] == EXPECTED_DECISION_FAILURE_COUNT
    assert decision["passed_gate_count"] == decision["decision_gate_count"]
    assert decision["decision_issue_count"] == 0


def test_approval_gate_source_is_present_and_hashed():
    source = build_milestone_9_real_submission_decision_record()["approval_gate_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_READY"
    assert source["approval_id"].startswith("MILESTONE-9-APPROVAL-GATE-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_decision_record_keeps_submission_blocked():
    decision = build_milestone_9_real_submission_decision_record()
    assert decision["operator_approval_required"] is True
    assert decision["operator_approval_granted"] is False
    assert decision["operator_approval_received"] is False
    assert decision["explicit_operator_approval_phrase_received"] is False
    assert decision["manual_upload_allowed"] is False
    assert decision["kaggle_authentication_allowed"] is False
    assert decision["real_submission_created"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["ready_for_real_kaggle_submission"] is False
    assert decision["kaggle_submission_sent"] is False
    assert decision["upload_performed"] is False
    assert decision["kaggle_authentication_performed"] is False


def test_decision_gates_and_issues_are_clean():
    decision = build_milestone_9_real_submission_decision_record()
    assert all(item["passed"] is True for item in decision["decision_gates"])
    assert all(item["active"] is False for item in decision["decision_issues"])


def test_decision_validation_and_pipeline_pass():
    decision = build_milestone_9_real_submission_decision_record()
    validation = validate_milestone_9_real_submission_decision_record(decision)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_9_real_submission_decision_record_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["decision_status"] == DECISION_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["decision_ready"] is True
    assert payload["decision_pass_count"] == 10
    assert payload["decision_failure_count"] == 0


def test_decision_markdown_and_manifest_contain_markers():
    decision = build_milestone_9_real_submission_decision_record()
    markdown = render_real_submission_decision_record_markdown(decision)
    manifest = render_real_submission_decision_record_manifest(decision)
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_DECISION=NOT_AUTHORIZED" in markdown
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_DECISION_REASON=OPERATOR_APPROVAL_NOT_GRANTED" in markdown
    assert "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GRANTED=false" in markdown
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "DECISION_CHECKS" in manifest
    assert "DECISION_RESULTS" in manifest
    assert "decision_real_submission_not_authorized_v1" in manifest


def test_decision_writes_artifacts(tmp_path: Path):
    decision = build_milestone_9_real_submission_decision_record()
    paths = write_real_submission_decision_record_artifacts(decision, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "REAL_SUBMISSION_DECISION_RECORDED_NOT_AUTHORIZED_SUBMISSION_BLOCKED" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_decision_metadata_safe():
    metadata = build_milestone_9_real_submission_decision_record()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_decision_index_is_conservative():
    index = build_milestone_9_real_submission_decision_record()["decision_index"]
    assert index["decision_ready"] is True
    assert index["decision_locked"] is True
    assert index["real_submission_decision_record_created"] is True
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
