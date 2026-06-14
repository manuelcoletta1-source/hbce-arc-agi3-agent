from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_9_operator_declaration_package import (
    EXPECTED_ACCEPTED_DECLARATION_COUNT,
    EXPECTED_DECLARATION_COUNT,
    EXPECTED_DECLARATION_TEMPLATE_COUNT,
    EXPECTED_PACKAGE_CASE_COUNT,
    EXPECTED_PACKAGE_FAILURE_COUNT,
    EXPECTED_PACKAGE_PASS_COUNT,
    EXPECTED_PROVIDED_DECLARATION_COUNT,
    EXPECTED_REJECTED_DECLARATION_COUNT,
    NEXT_ALLOWED_STAGE,
    PACKAGE_MODE,
    PACKAGE_SCOPE,
    PACKAGE_STATUS,
    PACKAGE_VERDICT,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_declaration_checks,
    build_milestone_9_operator_declaration_package,
    build_operator_declaration_state,
    evaluate_all_operator_declaration_package_cases,
    evaluate_operator_declaration_package_case,
    render_operator_declaration_package_manifest,
    render_operator_declaration_package_markdown,
    run_milestone_9_operator_declaration_package_pipeline,
    validate_milestone_9_operator_declaration_package,
    write_operator_declaration_package_artifacts,
)


def test_operator_declaration_state_templates_ready_but_unapproved():
    state = build_operator_declaration_state()
    assert state["declaration_package_ready"] is True
    assert state["declaration_template_count"] == EXPECTED_DECLARATION_TEMPLATE_COUNT
    assert state["required_declaration_count"] == EXPECTED_DECLARATION_COUNT
    assert state["provided_declaration_count"] == EXPECTED_PROVIDED_DECLARATION_COUNT
    assert state["accepted_declaration_count"] == EXPECTED_ACCEPTED_DECLARATION_COUNT
    assert state["rejected_declaration_count"] == EXPECTED_REJECTED_DECLARATION_COUNT
    assert state["operator_approval_required"] is True
    assert state["operator_approval_granted"] is False
    assert state["operator_approval_received"] is False


def test_declaration_checks_all_pass():
    checks = build_declaration_checks()
    assert all(checks.values())


def test_each_operator_declaration_package_case_passes():
    case_ids = [
        "declaration_governance_plan_source_ready_v1",
        "declaration_template_set_complete_v1",
        "declaration_required_count_valid_v1",
        "declaration_no_operator_submission_yet_v1",
        "declaration_no_accepted_declarations_yet_v1",
        "declaration_approval_not_granted_v1",
        "declaration_real_submission_blocked_v1",
        "declaration_no_upload_no_auth_v1",
        "declaration_no_score_or_leaderboard_claim_v1",
        "declaration_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_operator_declaration_package_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_operator_declaration_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_operator_declaration_package_case("missing_declaration_case")


def test_all_operator_declaration_package_cases_pass():
    results = evaluate_all_operator_declaration_package_cases()
    assert len(results) == EXPECTED_PACKAGE_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_operator_declaration_package_record_ready():
    package = build_milestone_9_operator_declaration_package()
    assert package["status"] == PACKAGE_STATUS
    assert package["package_mode"] == PACKAGE_MODE
    assert package["package_scope"] == PACKAGE_SCOPE
    assert package["package_verdict"] == PACKAGE_VERDICT
    assert package["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert package["package_ready"] is True
    assert package["package_locked"] is True
    assert package["declaration_package_created"] is True
    assert package["declaration_template_count"] == EXPECTED_DECLARATION_TEMPLATE_COUNT
    assert package["required_declaration_count"] == EXPECTED_DECLARATION_COUNT
    assert package["package_case_count"] == EXPECTED_PACKAGE_CASE_COUNT
    assert package["package_pass_count"] == EXPECTED_PACKAGE_PASS_COUNT
    assert package["package_failure_count"] == EXPECTED_PACKAGE_FAILURE_COUNT
    assert package["passed_gate_count"] == package["package_gate_count"]
    assert package["package_issue_count"] == 0


def test_governance_plan_source_is_present_and_hashed():
    source = build_milestone_9_operator_declaration_package()["governance_plan_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_READY"
    assert source["plan_id"].startswith("MILESTONE-9-GOVERNANCE-PLAN-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_declaration_templates_are_unique_and_match_required():
    package = build_milestone_9_operator_declaration_package()
    templates = package["declaration_templates"]
    ids = [item["declaration_id"] for item in templates]
    required = package["operator_declaration_state"]["required_declarations"]
    assert len(templates) == EXPECTED_DECLARATION_TEMPLATE_COUNT
    assert len(ids) == len(set(ids))
    assert sorted(ids) == sorted(required)
    assert all(item["required_response"] == "explicit_yes" for item in templates)


def test_operator_declaration_package_keeps_submission_blocked():
    package = build_milestone_9_operator_declaration_package()
    assert package["operator_approval_required"] is True
    assert package["operator_approval_granted"] is False
    assert package["operator_approval_received"] is False
    assert package["real_submission_created"] is False
    assert package["real_submission_allowed"] is False
    assert package["ready_for_real_kaggle_submission"] is False
    assert package["kaggle_submission_sent"] is False
    assert package["upload_performed"] is False
    assert package["kaggle_authentication_performed"] is False


def test_operator_declaration_package_gates_and_issues_are_clean():
    package = build_milestone_9_operator_declaration_package()
    assert all(item["passed"] is True for item in package["package_gates"])
    assert all(item["active"] is False for item in package["package_issues"])


def test_operator_declaration_validation_and_pipeline_pass():
    package = build_milestone_9_operator_declaration_package()
    validation = validate_milestone_9_operator_declaration_package(package)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_9_operator_declaration_package_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["package_status"] == PACKAGE_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["package_ready"] is True
    assert payload["package_pass_count"] == 10
    assert payload["package_failure_count"] == 0


def test_operator_declaration_markdown_and_manifest_contain_markers():
    package = build_milestone_9_operator_declaration_package()
    markdown = render_operator_declaration_package_markdown(package)
    manifest = render_operator_declaration_package_manifest(package)
    assert "ARC_AGI3_MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_DECLARATION_PACKAGE_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GRANTED=false" in markdown
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "DECLARATION_TEMPLATES" in manifest
    assert "PACKAGE_RESULTS" in manifest
    assert "declaration_real_submission_blocked_v1" in manifest


def test_operator_declaration_writes_artifacts(tmp_path: Path):
    package = build_milestone_9_operator_declaration_package()
    paths = write_operator_declaration_package_artifacts(package, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "OPERATOR_DECLARATION_PACKAGE_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_operator_declaration_metadata_safe():
    metadata = build_milestone_9_operator_declaration_package()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_operator_declaration_index_is_conservative():
    index = build_milestone_9_operator_declaration_package()["package_index"]
    assert index["package_ready"] is True
    assert index["package_locked"] is True
    assert index["declaration_package_created"] is True
    assert index["operator_approval_required"] is True
    assert index["operator_approval_granted"] is False
    assert index["operator_approval_received"] is False
    assert index["real_submission_allowed"] is False
    assert index["ready_for_real_kaggle_submission"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["upload_performed"] is False
    assert index["kaggle_authentication_performed"] is False
