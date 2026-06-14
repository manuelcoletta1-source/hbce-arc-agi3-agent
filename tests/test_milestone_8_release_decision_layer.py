from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_8_release_decision_layer import (
    DECISION_MODE,
    DECISION_SCOPE,
    DECISION_STATUS,
    DECISION_VERDICT,
    EXPECTED_ACCEPTED_DECLARATION_COUNT,
    EXPECTED_CLOSED_TASK_COUNT,
    EXPECTED_DECISION_CASE_COUNT,
    EXPECTED_DECISION_FAILURE_COUNT,
    EXPECTED_DECISION_PASS_COUNT,
    EXPECTED_PROVIDED_DECLARATION_COUNT,
    EXPECTED_REQUIRED_DECLARATION_COUNT,
    EXPECTED_SOURCE_COMMIT_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_decision_checks,
    build_milestone_8_release_decision_layer,
    build_operator_approval_state,
    evaluate_all_release_decision_cases,
    evaluate_release_decision_case,
    render_release_decision_layer_manifest,
    render_release_decision_layer_markdown,
    run_milestone_8_release_decision_layer_pipeline,
    validate_milestone_8_release_decision_layer,
    write_release_decision_layer_artifacts,
)


def test_operator_approval_state_requires_manual_approval_but_has_none():
    approval = build_operator_approval_state()
    assert approval["operator_approval_required"] is True
    assert approval["operator_approval_granted"] is False
    assert approval["operator_approval_received"] is False
    assert approval["required_declaration_count"] == EXPECTED_REQUIRED_DECLARATION_COUNT
    assert approval["provided_declaration_count"] == EXPECTED_PROVIDED_DECLARATION_COUNT
    assert approval["accepted_declaration_count"] == EXPECTED_ACCEPTED_DECLARATION_COUNT
    assert len(set(approval["required_declarations"])) == EXPECTED_REQUIRED_DECLARATION_COUNT


def test_decision_checks_all_pass():
    checks = build_decision_checks()
    assert all(checks.values())


def test_each_release_decision_case_passes():
    case_ids = [
        "decision_final_refresh_source_ready_v2",
        "decision_package_ready_for_manual_review_v2",
        "decision_chain_task_1_to_8_complete_v2",
        "decision_required_declarations_defined_v2",
        "decision_no_operator_approval_provided_v2",
        "decision_real_submission_blocked_v2",
        "decision_no_upload_no_auth_v2",
        "decision_no_score_or_leaderboard_claim_v2",
        "decision_manual_review_package_ready_v2",
        "decision_next_stage_closure_valid_v2",
    ]
    for case_id in case_ids:
        result = evaluate_release_decision_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_release_decision_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_release_decision_case("missing_release_decision_case")


def test_all_release_decision_cases_pass():
    results = evaluate_all_release_decision_cases()
    assert len(results) == EXPECTED_DECISION_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_release_decision_record_ready():
    decision = build_milestone_8_release_decision_layer()
    assert decision["status"] == DECISION_STATUS
    assert decision["decision_mode"] == DECISION_MODE
    assert decision["decision_scope"] == DECISION_SCOPE
    assert decision["decision_verdict"] == DECISION_VERDICT
    assert decision["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert decision["closed_task_count"] == EXPECTED_CLOSED_TASK_COUNT
    assert decision["source_commit_count"] == EXPECTED_SOURCE_COMMIT_COUNT
    assert decision["decision_case_count"] == EXPECTED_DECISION_CASE_COUNT
    assert decision["decision_pass_count"] == EXPECTED_DECISION_PASS_COUNT
    assert decision["decision_failure_count"] == EXPECTED_DECISION_FAILURE_COUNT
    assert decision["passed_gate_count"] == decision["decision_gate_count"]
    assert decision["decision_issue_count"] == 0
    assert decision["decision_ready"] is True


def test_release_decision_chain_commits_are_complete():
    decision = build_milestone_8_release_decision_layer()
    commits = [item["commit"] for item in decision["source_commits"]]
    assert commits == ["69af006", "4a93654", "1df6919", "3ea3687", "537b277", "c68ab45", "0e7e086", "cb52cd2"]


def test_final_refresh_source_is_present_and_hashed():
    source = build_milestone_8_release_decision_layer()["final_refresh_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_8_FINAL_COMPETITIVE_READINESS_REFRESH_V2_READY"
    assert source["final_id"].startswith("MILESTONE-8-FINAL-READINESS-REFRESH-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_release_decision_keeps_submission_blocked():
    decision = build_milestone_8_release_decision_layer()
    assert decision["package_ready_for_manual_review"] is True
    assert decision["operator_approval_required"] is True
    assert decision["operator_approval_granted"] is False
    assert decision["operator_approval_received"] is False
    assert decision["real_submission_created"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["ready_for_real_kaggle_submission"] is False
    assert decision["kaggle_submission_sent"] is False
    assert decision["upload_performed"] is False
    assert decision["kaggle_authentication_performed"] is False


def test_decision_gates_and_issues_are_clean():
    decision = build_milestone_8_release_decision_layer()
    assert all(item["passed"] is True for item in decision["decision_gates"])
    assert all(item["active"] is False for item in decision["decision_issues"])


def test_release_decision_validation_and_pipeline_pass():
    decision = build_milestone_8_release_decision_layer()
    validation = validate_milestone_8_release_decision_layer(decision)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_8_release_decision_layer_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["decision_status"] == DECISION_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["decision_ready"] is True
    assert payload["decision_pass_count"] == 10
    assert payload["decision_failure_count"] == 0


def test_release_decision_markdown_and_manifest_contain_markers():
    decision = build_milestone_8_release_decision_layer()
    markdown = render_release_decision_layer_markdown(decision)
    manifest = render_release_decision_layer_manifest(decision)
    assert "ARC_AGI3_MILESTONE_8_RELEASE_DECISION_LAYER_V2_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_RELEASE_DECISION_LAYER_V2_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_OPERATOR_APPROVAL_REQUIRED=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_OPERATOR_APPROVAL_GRANTED=false" in markdown
    assert "ARC_AGI3_MILESTONE_8_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "REQUIRED_OPERATOR_DECLARATIONS" in manifest
    assert "DECISION_RESULTS" in manifest
    assert "decision_real_submission_blocked_v2" in manifest


def test_release_decision_writes_artifacts(tmp_path: Path):
    decision = build_milestone_8_release_decision_layer()
    paths = write_release_decision_layer_artifacts(decision, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_8_RELEASE_DECISION_LAYER_V2_READY" in Path(paths["json_path"]).read_text(
        encoding="utf-8"
    )
    assert "ARC_AGI3_MILESTONE_8_RELEASE_DECISION_LAYER_V2_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "RELEASE_DECISION_LAYER_READY_MANUAL_APPROVAL_REQUIRED_REAL_SUBMISSION_BLOCKED" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_release_decision_metadata_safe():
    metadata = build_milestone_8_release_decision_layer()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_release_decision_index_is_conservative():
    index = build_milestone_8_release_decision_layer()["decision_index"]
    assert index["decision_ready"] is True
    assert index["decision_locked"] is True
    assert index["package_ready_for_manual_review"] is True
    assert index["operator_approval_required"] is True
    assert index["operator_approval_granted"] is False
    assert index["real_submission_allowed"] is False
    assert index["ready_for_real_kaggle_submission"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["upload_performed"] is False
    assert index["kaggle_authentication_performed"] is False
