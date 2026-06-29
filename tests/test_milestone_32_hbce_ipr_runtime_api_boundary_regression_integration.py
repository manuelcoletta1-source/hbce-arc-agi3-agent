from hbce_arc_agi3.milestone_32_hbce_ipr_runtime_api_boundary_regression_integration import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    REGRESSION_CASE_COUNT,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_VALIDATION_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    run_milestone_32_boundary_regression_integration,
    task_5_signature,
    validate_milestone_32_boundary_regression_integration_report,
    write_task_5_artifacts,
)


def test_milestone_32_boundary_regression_integration_report_is_valid():
    report = run_milestone_32_boundary_regression_integration()

    assert validate_milestone_32_boundary_regression_integration_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_validation_task_id"] == SOURCE_VALIDATION_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["task_5_signature"] == task_5_signature()
    assert report["source_validation_status"] == "VALID"
    assert report["source_validation_passed"] is True
    assert report["integration_status"] == "VALID"
    assert report["integration_case_count"] == REGRESSION_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["integration_passed"] is True
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_32_boundary_regression_preserves_legal_boundary():
    report = run_milestone_32_boundary_regression_integration()

    assert report["opc_technical_proof_receipt_only"] is True
    assert report["legal_certification"] is False
    assert report["ipr_card_internal_operational_identity_certificate"] is True
    assert report["ipr_card_official_public_identity_document"] is False
    assert report["explicit_legal_boundary_required"] is True


def test_milestone_32_boundary_regression_cases_are_all_passed():
    report = run_milestone_32_boundary_regression_integration()

    assert len(report["integration_cases"]) == REGRESSION_CASE_COUNT
    assert all(case["passed"] is True for case in report["integration_cases"])
    assert all(case["failure_reason"] == "NONE" for case in report["integration_cases"])


def test_milestone_32_boundary_regression_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_5_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_validation_task_id"] == SOURCE_VALIDATION_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["task_5_signature"] == task_5_signature()
    assert artifacts["manifest"]["integration_status"] == "VALID"
    assert artifacts["manifest"]["integration_passed"] is True
    assert artifacts["manifest"]["integration_case_count"] == REGRESSION_CASE_COUNT
    assert artifacts["manifest"]["pass_count"] == REQUIRED_PASS_COUNT
    assert artifacts["manifest"]["fail_count"] == REQUIRED_FAIL_COUNT
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE


def test_milestone_32_boundary_regression_rejects_mutated_report():
    report = run_milestone_32_boundary_regression_integration()
    report["legal_certification"] = True

    assert not validate_milestone_32_boundary_regression_integration_report(report)
