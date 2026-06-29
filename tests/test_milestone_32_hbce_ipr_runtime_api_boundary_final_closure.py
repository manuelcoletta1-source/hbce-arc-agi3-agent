from hbce_arc_agi3.milestone_32_hbce_ipr_runtime_api_boundary_final_closure import (
    CLOSURE_CASE_COUNT,
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_REGRESSION_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    run_milestone_32_boundary_final_closure,
    task_6_signature,
    validate_milestone_32_boundary_final_closure_report,
    write_task_6_artifacts,
)


def test_milestone_32_boundary_final_closure_report_is_valid():
    report = run_milestone_32_boundary_final_closure()

    assert validate_milestone_32_boundary_final_closure_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_regression_task_id"] == SOURCE_REGRESSION_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["task_6_signature"] == task_6_signature()
    assert report["closure_status"] == "CLOSED"
    assert report["closure_case_count"] == CLOSURE_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["closure_passed"] is True
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_32_boundary_final_closure_preserves_legal_boundary():
    report = run_milestone_32_boundary_final_closure()

    assert report["opc_technical_proof_receipt_only"] is True
    assert report["legal_certification"] is False
    assert report["ipr_card_internal_operational_identity_certificate"] is True
    assert report["ipr_card_official_public_identity_document"] is False
    assert report["explicit_legal_boundary_required"] is True


def test_milestone_32_boundary_final_closure_cases_are_all_passed():
    report = run_milestone_32_boundary_final_closure()

    assert len(report["closure_cases"]) == CLOSURE_CASE_COUNT
    assert all(case["passed"] is True for case in report["closure_cases"])
    assert all(case["failure_reason"] == "NONE" for case in report["closure_cases"])


def test_milestone_32_boundary_final_closure_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_6_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_regression_task_id"] == SOURCE_REGRESSION_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["task_6_signature"] == task_6_signature()
    assert artifacts["manifest"]["closure_status"] == "CLOSED"
    assert artifacts["manifest"]["closure_passed"] is True
    assert artifacts["manifest"]["closure_case_count"] == CLOSURE_CASE_COUNT
    assert artifacts["manifest"]["pass_count"] == REQUIRED_PASS_COUNT
    assert artifacts["manifest"]["fail_count"] == REQUIRED_FAIL_COUNT
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE


def test_milestone_32_boundary_final_closure_rejects_mutated_report():
    report = run_milestone_32_boundary_final_closure()
    report["legal_certification"] = True

    assert not validate_milestone_32_boundary_final_closure_report(report)
