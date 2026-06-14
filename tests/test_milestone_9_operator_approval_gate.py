from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_9_operator_approval_gate import (
    EXPECTED_ACCEPTED_DECLARATION_COUNT,
    EXPECTED_APPROVAL_CASE_COUNT,
    EXPECTED_APPROVAL_CHECK_COUNT,
    EXPECTED_APPROVAL_FAILURE_COUNT,
    EXPECTED_APPROVAL_PASS_COUNT,
    EXPECTED_PROVIDED_DECLARATION_COUNT,
    EXPECTED_REQUIRED_DECLARATION_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    APPROVAL_MODE,
    APPROVAL_SCOPE,
    APPROVAL_STATUS,
    APPROVAL_VERDICT,
    VALIDATION_STATUS,
    build_approval_source_summary,
    build_milestone_9_operator_approval_gate,
    build_operator_approval_gate_checks,
    build_operator_approval_gate_state,
    evaluate_all_operator_approval_gate_cases,
    evaluate_operator_approval_gate_case,
    render_operator_approval_gate_manifest,
    render_operator_approval_gate_markdown,
    run_milestone_9_operator_approval_gate_pipeline,
    validate_milestone_9_operator_approval_gate,
    write_operator_approval_gate_artifacts,
)


def test_approval_source_summary_ready():
    summary = build_approval_source_summary()
    assert summary["preflight_present"] is True
    assert summary["preflight_status"] == "MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_READY"
    assert summary["preflight_id"].startswith("MILESTONE-9-PREFLIGHT-GATE-")
    assert summary["declaration_package_present"] is True
    assert summary["declaration_package_status"] == "MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_READY"
    assert summary["declaration_package_id"].startswith("MILESTONE-9-DECLARATION-PACKAGE-")
    assert Path(summary["candidate_source_path"]).exists()
    assert summary["candidate_id"].startswith("MILESTONE-8-SUBMISSION-REFRESH-")
    assert summary["candidate_signature"]
    assert summary["candidate_count"] > 0
    assert summary["required_declaration_count"] == EXPECTED_REQUIRED_DECLARATION_COUNT
    assert summary["provided_declaration_count"] == EXPECTED_PROVIDED_DECLARATION_COUNT
    assert summary["accepted_declaration_count"] == EXPECTED_ACCEPTED_DECLARATION_COUNT


def test_operator_approval_gate_state_ready_but_closed():
    state = build_operator_approval_gate_state()
    assert state["operator_approval_gate_required"] is True
    assert state["operator_approval_gate_created"] is True
    assert state["operator_approval_gate_ready"] is True
    assert state["operator_approval_gate_open"] is False
    assert state["operator_approval_required"] is True
    assert state["operator_approval_granted"] is False
    assert state["operator_approval_received"] is False
    assert state["explicit_operator_approval_phrase_required"] is True
    assert state["explicit_operator_approval_phrase_received"] is False
    assert state["all_required_declarations_accepted"] is False
    assert state["manual_upload_allowed"] is False
    assert state["kaggle_authentication_allowed"] is False
    assert state["real_submission_allowed"] is False


def test_operator_approval_gate_checks_all_pass():
    checks = build_operator_approval_gate_checks()
    assert all(checks.values())


def test_each_operator_approval_gate_case_passes():
    case_ids = [
        "approval_preflight_source_ready_v1",
        "approval_declaration_package_source_ready_v1",
        "approval_required_declarations_present_v1",
        "approval_declarations_not_accepted_v1",
        "approval_explicit_operator_approval_absent_v1",
        "approval_gate_ready_but_closed_v1",
        "approval_real_submission_blocked_v1",
        "approval_no_upload_no_auth_v1",
        "approval_no_score_or_leaderboard_claim_v1",
        "approval_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_operator_approval_gate_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_operator_approval_gate_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_operator_approval_gate_case("missing_approval_case")


def test_all_operator_approval_gate_cases_pass():
    results = evaluate_all_operator_approval_gate_cases()
    assert len(results) == EXPECTED_APPROVAL_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_operator_approval_gate_record_ready():
    approval = build_milestone_9_operator_approval_gate()
    assert approval["status"] == APPROVAL_STATUS
    assert approval["approval_mode"] == APPROVAL_MODE
    assert approval["approval_scope"] == APPROVAL_SCOPE
    assert approval["approval_verdict"] == APPROVAL_VERDICT
    assert approval["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert approval["approval_ready"] is True
    assert approval["approval_locked"] is True
    assert approval["operator_approval_gate_created"] is True
    assert approval["operator_approval_gate_ready"] is True
    assert approval["operator_approval_gate_open"] is False
    assert approval["approval_check_count"] == EXPECTED_APPROVAL_CHECK_COUNT
    assert approval["approval_case_count"] == EXPECTED_APPROVAL_CASE_COUNT
    assert approval["approval_pass_count"] == EXPECTED_APPROVAL_PASS_COUNT
    assert approval["approval_failure_count"] == EXPECTED_APPROVAL_FAILURE_COUNT
    assert approval["passed_gate_count"] == approval["approval_gate_count"]
    assert approval["approval_issue_count"] == 0


def test_preflight_and_declaration_sources_are_hashed():
    approval = build_milestone_9_operator_approval_gate()
    preflight_source = approval["preflight_source"]
    declaration_source = approval["declaration_package_source"]
    assert preflight_source["present"] is True
    assert preflight_source["status"] == "MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_READY"
    assert preflight_source["sha256"] != "MISSING_HASH"
    assert preflight_source["sha256_16"] != "MISSING_HASH"
    assert declaration_source["present"] is True
    assert declaration_source["status"] == "MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_READY"
    assert declaration_source["sha256"] != "MISSING_HASH"
    assert declaration_source["sha256_16"] != "MISSING_HASH"


def test_operator_approval_gate_keeps_submission_blocked():
    approval = build_milestone_9_operator_approval_gate()
    assert approval["operator_approval_required"] is True
    assert approval["operator_approval_granted"] is False
    assert approval["operator_approval_received"] is False
    assert approval["explicit_operator_approval_phrase_received"] is False
    assert approval["all_required_declarations_accepted"] is False
    assert approval["manual_upload_allowed"] is False
    assert approval["kaggle_authentication_allowed"] is False
    assert approval["real_submission_created"] is False
    assert approval["real_submission_allowed"] is False
    assert approval["ready_for_real_kaggle_submission"] is False
    assert approval["kaggle_submission_sent"] is False
    assert approval["upload_performed"] is False
    assert approval["kaggle_authentication_performed"] is False


def test_operator_approval_gate_gates_and_issues_are_clean():
    approval = build_milestone_9_operator_approval_gate()
    assert all(item["passed"] is True for item in approval["approval_gates"])
    assert all(item["active"] is False for item in approval["approval_issues"])


def test_operator_approval_gate_validation_and_pipeline_pass():
    approval = build_milestone_9_operator_approval_gate()
    validation = validate_milestone_9_operator_approval_gate(approval)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_9_operator_approval_gate_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["approval_status"] == APPROVAL_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["approval_ready"] is True
    assert payload["approval_pass_count"] == 10
    assert payload["approval_failure_count"] == 0


def test_operator_approval_gate_markdown_and_manifest_contain_markers():
    approval = build_milestone_9_operator_approval_gate()
    markdown = render_operator_approval_gate_markdown(approval)
    manifest = render_operator_approval_gate_manifest(approval)
    assert "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_APPROVAL_GATE_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GATE_OPEN=false" in markdown
    assert "ARC_AGI3_MILESTONE_9_EXPLICIT_OPERATOR_APPROVAL_PHRASE_RECEIVED=false" in markdown
    assert "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GRANTED=false" in markdown
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "APPROVAL_CHECKS" in manifest
    assert "APPROVAL_RESULTS" in manifest
    assert "approval_real_submission_blocked_v1" in manifest


def test_operator_approval_gate_writes_artifacts(tmp_path: Path):
    approval = build_milestone_9_operator_approval_gate()
    paths = write_operator_approval_gate_artifacts(approval, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "OPERATOR_APPROVAL_GATE_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_operator_approval_gate_metadata_safe():
    metadata = build_milestone_9_operator_approval_gate()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_operator_approval_gate_index_is_conservative():
    index = build_milestone_9_operator_approval_gate()["approval_index"]
    assert index["approval_ready"] is True
    assert index["approval_locked"] is True
    assert index["operator_approval_gate_created"] is True
    assert index["operator_approval_gate_open"] is False
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
