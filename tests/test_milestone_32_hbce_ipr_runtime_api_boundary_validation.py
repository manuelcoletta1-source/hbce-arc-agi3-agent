from hbce_arc_agi3.milestone_32_hbce_ipr_runtime_api_boundary_validation import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_IMPLEMENTATION_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    VALIDATION_CASE_COUNT,
    run_milestone_32_boundary_validation,
    task_4_signature,
    validate_milestone_32_boundary_validation_report,
    write_task_4_artifacts,
)


def test_milestone_32_boundary_validation_report_is_valid():
    report = run_milestone_32_boundary_validation()

    assert validate_milestone_32_boundary_validation_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_implementation_task_id"] == SOURCE_IMPLEMENTATION_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["task_4_signature"] == task_4_signature()
    assert report["validation_status"] == "VALID"
    assert report["validation_case_count"] == VALIDATION_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["validation_passed"] is True
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_32_boundary_validation_blocks_missing_links():
    report = run_milestone_32_boundary_validation()

    assert len(report["blocked_validation_results"]) == 6
    assert all(result["validator_passed"] is False for result in report["blocked_validation_results"])
    assert all(result["status"] == "BLOCKED" for result in report["blocked_validation_results"])


def test_milestone_32_boundary_validation_preserves_legal_flags():
    report = run_milestone_32_boundary_validation()

    assert report["opc_technical_proof_receipt_only"] is True
    assert report["legal_certification"] is False
    assert report["ipr_card_internal_operational_identity_certificate"] is True
    assert report["ipr_card_official_public_identity_document"] is False
    assert report["explicit_legal_boundary_required"] is True


def test_milestone_32_boundary_validation_cases_are_all_passed():
    report = run_milestone_32_boundary_validation()

    assert len(report["validation_cases"]) == VALIDATION_CASE_COUNT
    assert all(case["passed"] is True for case in report["validation_cases"])
    assert all(case["failure_reason"] == "NONE" for case in report["validation_cases"])


def test_milestone_32_boundary_validation_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_4_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_implementation_task_id"] == SOURCE_IMPLEMENTATION_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["task_4_signature"] == task_4_signature()
    assert artifacts["manifest"]["validation_status"] == "VALID"
    assert artifacts["manifest"]["validation_passed"] is True
    assert artifacts["manifest"]["validation_case_count"] == VALIDATION_CASE_COUNT
    assert artifacts["manifest"]["pass_count"] == REQUIRED_PASS_COUNT
    assert artifacts["manifest"]["fail_count"] == REQUIRED_FAIL_COUNT
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE


def test_milestone_32_boundary_validation_rejects_mutated_report():
    report = run_milestone_32_boundary_validation()
    report["legal_certification"] = True

    assert not validate_milestone_32_boundary_validation_report(report)
