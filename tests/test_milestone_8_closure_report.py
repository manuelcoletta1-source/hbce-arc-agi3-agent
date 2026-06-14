from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_8_closure_report import (
    CLOSURE_MODE,
    CLOSURE_SCOPE,
    CLOSURE_STATUS,
    CLOSURE_VERDICT,
    EXPECTED_ACCEPTED_DECLARATION_COUNT,
    EXPECTED_CLOSED_TASK_COUNT,
    EXPECTED_CLOSURE_CASE_COUNT,
    EXPECTED_CLOSURE_FAILURE_COUNT,
    EXPECTED_CLOSURE_PASS_COUNT,
    EXPECTED_PROVIDED_DECLARATION_COUNT,
    EXPECTED_REQUIRED_DECLARATION_COUNT,
    EXPECTED_SOURCE_COMMIT_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_closure_checks,
    build_milestone_8_closure_report,
    evaluate_all_closure_cases,
    evaluate_closure_case,
    render_milestone_8_closure_report_manifest,
    render_milestone_8_closure_report_markdown,
    run_milestone_8_closure_report_pipeline,
    validate_milestone_8_closure_report,
    write_milestone_8_closure_report_artifacts,
)


def test_closure_checks_all_pass():
    checks = build_closure_checks()
    assert all(checks.values())


def test_each_closure_case_passes():
    case_ids = [
        "closure_decision_layer_source_ready_v2",
        "closure_task_chain_complete_v2",
        "closure_manual_review_package_ready_v2",
        "closure_operator_approval_contract_preserved_v2",
        "closure_real_submission_still_blocked_v2",
        "closure_no_upload_no_auth_v2",
        "closure_no_score_or_leaderboard_claim_v2",
        "closure_artifact_package_ready_v2",
        "closure_milestone_closed_state_valid_v2",
        "closure_next_stage_valid_v2",
    ]
    for case_id in case_ids:
        result = evaluate_closure_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_closure_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_closure_case("missing_closure_case")


def test_all_closure_cases_pass():
    results = evaluate_all_closure_cases()
    assert len(results) == EXPECTED_CLOSURE_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_closure_record_ready():
    closure = build_milestone_8_closure_report()
    assert closure["status"] == CLOSURE_STATUS
    assert closure["closure_mode"] == CLOSURE_MODE
    assert closure["closure_scope"] == CLOSURE_SCOPE
    assert closure["closure_verdict"] == CLOSURE_VERDICT
    assert closure["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert closure["milestone_8_closed"] is True
    assert closure["closed_task_count"] == EXPECTED_CLOSED_TASK_COUNT
    assert closure["source_commit_count"] == EXPECTED_SOURCE_COMMIT_COUNT
    assert closure["closure_case_count"] == EXPECTED_CLOSURE_CASE_COUNT
    assert closure["closure_pass_count"] == EXPECTED_CLOSURE_PASS_COUNT
    assert closure["closure_failure_count"] == EXPECTED_CLOSURE_FAILURE_COUNT
    assert closure["passed_gate_count"] == closure["closure_gate_count"]
    assert closure["closure_issue_count"] == 0
    assert closure["closure_ready"] is True


def test_closure_chain_commits_are_complete():
    closure = build_milestone_8_closure_report()
    commits = [item["commit"] for item in closure["source_commits"]]
    assert commits == [
        "69af006",
        "4a93654",
        "1df6919",
        "3ea3687",
        "537b277",
        "c68ab45",
        "0e7e086",
        "cb52cd2",
        "db17554",
    ]


def test_decision_layer_source_is_present_and_hashed():
    source = build_milestone_8_closure_report()["decision_layer_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_8_RELEASE_DECISION_LAYER_V2_READY"
    assert source["decision_id"].startswith("MILESTONE-8-RELEASE-DECISION-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_closure_preserves_operator_approval_contract():
    closure = build_milestone_8_closure_report()
    assert closure["operator_approval_required"] is True
    assert closure["operator_approval_granted"] is False
    assert closure["operator_approval_received"] is False
    assert closure["required_declaration_count"] == EXPECTED_REQUIRED_DECLARATION_COUNT
    assert closure["provided_declaration_count"] == EXPECTED_PROVIDED_DECLARATION_COUNT
    assert closure["accepted_declaration_count"] == EXPECTED_ACCEPTED_DECLARATION_COUNT
    assert closure["approval_contract_preserved"] is True


def test_closure_keeps_submission_blocked():
    closure = build_milestone_8_closure_report()
    assert closure["package_ready_for_manual_review"] is True
    assert closure["real_submission_created"] is False
    assert closure["real_submission_allowed"] is False
    assert closure["ready_for_real_kaggle_submission"] is False
    assert closure["kaggle_submission_sent"] is False
    assert closure["upload_performed"] is False
    assert closure["kaggle_authentication_performed"] is False
    assert closure["score_claim_absent"] is True
    assert closure["public_leaderboard_claim_absent"] is True


def test_closure_gates_and_issues_are_clean():
    closure = build_milestone_8_closure_report()
    assert all(item["passed"] is True for item in closure["closure_gates"])
    assert all(item["active"] is False for item in closure["closure_issues"])


def test_closure_validation_and_pipeline_pass():
    closure = build_milestone_8_closure_report()
    validation = validate_milestone_8_closure_report(closure)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_8_closure_report_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["closure_status"] == CLOSURE_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["closure_ready"] is True
    assert payload["milestone_8_closed"] is True
    assert payload["closure_pass_count"] == 10
    assert payload["closure_failure_count"] == 0


def test_closure_markdown_and_manifest_contain_markers():
    closure = build_milestone_8_closure_report()
    markdown = render_milestone_8_closure_report_markdown(closure)
    manifest = render_milestone_8_closure_report_manifest(closure)
    assert "ARC_AGI3_MILESTONE_8_CLOSURE_REPORT_V2_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_CLOSURE_REPORT_V2_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_CLOSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_CLOSED_TASK_COUNT=9" in markdown
    assert "ARC_AGI3_MILESTONE_8_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "SOURCE_COMMITS" in manifest
    assert "CLOSURE_RESULTS" in manifest
    assert "closure_real_submission_still_blocked_v2" in manifest


def test_closure_writes_artifacts(tmp_path: Path):
    closure = build_milestone_8_closure_report()
    paths = write_milestone_8_closure_report_artifacts(closure, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_8_CLOSURE_REPORT_V2_READY" in Path(paths["json_path"]).read_text(
        encoding="utf-8"
    )
    assert "ARC_AGI3_MILESTONE_8_CLOSURE_REPORT_V2_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "MILESTONE_8_CLOSED_PACKAGE_READY_FOR_MANUAL_REVIEW_REAL_SUBMISSION_BLOCKED" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_closure_metadata_safe():
    metadata = build_milestone_8_closure_report()["metadata"]
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
    index = build_milestone_8_closure_report()["closure_index"]
    assert index["milestone_8_closed"] is True
    assert index["closure_ready"] is True
    assert index["closure_locked"] is True
    assert index["closure_pass_count"] == 10
    assert index["closure_failure_count"] == 0
    assert index["package_ready_for_manual_review"] is True
    assert index["operator_approval_required"] is True
    assert index["operator_approval_granted"] is False
    assert index["real_submission_allowed"] is False
    assert index["ready_for_real_kaggle_submission"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["upload_performed"] is False
    assert index["kaggle_authentication_performed"] is False
