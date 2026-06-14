from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_9_manual_submission_governance_plan import (
    EXPECTED_ACCEPTED_DECLARATION_COUNT,
    EXPECTED_GOVERNANCE_PHASE_COUNT,
    EXPECTED_PLAN_CASE_COUNT,
    EXPECTED_PLAN_FAILURE_COUNT,
    EXPECTED_PLAN_PASS_COUNT,
    EXPECTED_PRE_SUBMISSION_GATE_COUNT,
    EXPECTED_PROVIDED_DECLARATION_COUNT,
    EXPECTED_REQUIRED_DECLARATION_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    PLAN_MODE,
    PLAN_SCOPE,
    PLAN_STATUS,
    PLAN_VERDICT,
    VALIDATION_STATUS,
    build_governance_checks,
    build_milestone_9_manual_submission_governance_plan,
    build_operator_approval_state,
    evaluate_all_governance_plan_cases,
    evaluate_governance_plan_case,
    render_manual_submission_governance_plan_manifest,
    render_manual_submission_governance_plan_markdown,
    run_milestone_9_manual_submission_governance_plan_pipeline,
    validate_milestone_9_manual_submission_governance_plan,
    write_manual_submission_governance_plan_artifacts,
)


def test_operator_approval_state_is_required_but_not_granted():
    approval = build_operator_approval_state()
    assert approval["operator_approval_required"] is True
    assert approval["operator_approval_granted"] is False
    assert approval["operator_approval_received"] is False
    assert approval["required_declaration_count"] == EXPECTED_REQUIRED_DECLARATION_COUNT
    assert approval["provided_declaration_count"] == EXPECTED_PROVIDED_DECLARATION_COUNT
    assert approval["accepted_declaration_count"] == EXPECTED_ACCEPTED_DECLARATION_COUNT


def test_governance_checks_all_pass():
    checks = build_governance_checks()
    assert all(checks.values())


def test_each_governance_plan_case_passes():
    case_ids = [
        "governance_milestone_8_closure_source_ready_v1",
        "governance_milestone_9_open_state_valid_v1",
        "governance_phase_plan_defined_v1",
        "governance_required_declarations_defined_v1",
        "governance_pre_submission_gates_defined_v1",
        "governance_no_operator_approval_yet_v1",
        "governance_real_submission_still_blocked_v1",
        "governance_no_upload_no_auth_v1",
        "governance_no_score_or_leaderboard_claim_v1",
        "governance_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_governance_plan_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_governance_plan_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_governance_plan_case("missing_governance_case")


def test_all_governance_plan_cases_pass():
    results = evaluate_all_governance_plan_cases()
    assert len(results) == EXPECTED_PLAN_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_governance_plan_record_ready():
    plan = build_milestone_9_manual_submission_governance_plan()
    assert plan["status"] == PLAN_STATUS
    assert plan["plan_mode"] == PLAN_MODE
    assert plan["plan_scope"] == PLAN_SCOPE
    assert plan["plan_verdict"] == PLAN_VERDICT
    assert plan["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert plan["milestone_9_open"] is True
    assert plan["governance_phase_count"] == EXPECTED_GOVERNANCE_PHASE_COUNT
    assert plan["pre_submission_gate_count"] == EXPECTED_PRE_SUBMISSION_GATE_COUNT
    assert plan["plan_case_count"] == EXPECTED_PLAN_CASE_COUNT
    assert plan["plan_pass_count"] == EXPECTED_PLAN_PASS_COUNT
    assert plan["plan_failure_count"] == EXPECTED_PLAN_FAILURE_COUNT
    assert plan["passed_gate_count"] == plan["plan_gate_count"]
    assert plan["plan_issue_count"] == 0
    assert plan["plan_ready"] is True


def test_milestone_8_closure_source_is_present_and_hashed():
    source = build_milestone_9_manual_submission_governance_plan()["milestone_8_closure_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_8_CLOSURE_REPORT_V2_READY"
    assert source["closure_id"].startswith("MILESTONE-8-CLOSURE-REPORT-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_governance_phases_and_pre_submission_gates_are_complete():
    plan = build_milestone_9_manual_submission_governance_plan()
    assert plan["governance_phases"][0]["status"] == "THIS_TASK_READY"
    assert plan["governance_phases"][1]["name"] == "operator_declaration_package"
    assert plan["pre_submission_gates"][-1] == "final_operator_approval_confirmed"


def test_governance_keeps_submission_blocked():
    plan = build_milestone_9_manual_submission_governance_plan()
    assert plan["operator_approval_required"] is True
    assert plan["operator_approval_granted"] is False
    assert plan["operator_approval_received"] is False
    assert plan["real_submission_created"] is False
    assert plan["real_submission_allowed"] is False
    assert plan["ready_for_real_kaggle_submission"] is False
    assert plan["kaggle_submission_sent"] is False
    assert plan["upload_performed"] is False
    assert plan["kaggle_authentication_performed"] is False


def test_governance_plan_gates_and_issues_are_clean():
    plan = build_milestone_9_manual_submission_governance_plan()
    assert all(item["passed"] is True for item in plan["plan_gates"])
    assert all(item["active"] is False for item in plan["plan_issues"])


def test_governance_validation_and_pipeline_pass():
    plan = build_milestone_9_manual_submission_governance_plan()
    validation = validate_milestone_9_manual_submission_governance_plan(plan)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_9_manual_submission_governance_plan_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["plan_status"] == PLAN_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["milestone_9_open"] is True
    assert payload["plan_ready"] is True
    assert payload["plan_pass_count"] == 10
    assert payload["plan_failure_count"] == 0


def test_governance_markdown_and_manifest_contain_markers():
    plan = build_milestone_9_manual_submission_governance_plan()
    markdown = render_manual_submission_governance_plan_markdown(plan)
    manifest = render_manual_submission_governance_plan_manifest(plan)
    assert "ARC_AGI3_MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_OPEN=true" in markdown
    assert "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GRANTED=false" in markdown
    assert "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "GOVERNANCE_PHASES" in manifest
    assert "REQUIRED_OPERATOR_DECLARATIONS" in manifest
    assert "PRE_SUBMISSION_GATES" in manifest
    assert "PLAN_RESULTS" in manifest


def test_governance_writes_artifacts(tmp_path: Path):
    plan = build_milestone_9_manual_submission_governance_plan()
    paths = write_manual_submission_governance_plan_artifacts(plan, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_9_MANUAL_SUBMISSION_GOVERNANCE_PLAN_V1_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "MILESTONE_9_OPEN_REAL_SUBMISSION_BLOCKED_PENDING_EXPLICIT_OPERATOR_APPROVAL" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_governance_metadata_safe():
    metadata = build_milestone_9_manual_submission_governance_plan()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_governance_index_is_conservative():
    index = build_milestone_9_manual_submission_governance_plan()["plan_index"]
    assert index["milestone_9_open"] is True
    assert index["plan_ready"] is True
    assert index["plan_locked"] is True
    assert index["operator_approval_required"] is True
    assert index["operator_approval_granted"] is False
    assert index["real_submission_allowed"] is False
    assert index["ready_for_real_kaggle_submission"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["upload_performed"] is False
    assert index["kaggle_authentication_performed"] is False
