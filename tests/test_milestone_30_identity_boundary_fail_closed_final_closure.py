from pathlib import Path
import json

from hbce_arc_agi3.milestone_30_identity_boundary_fail_closed_final_closure import (
    CLOSURE_STATUS,
    FINAL_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    MILESTONE_ID,
    NEXT_STAGE,
    PROCESS_STATUS,
    READY_FOR_NEXT_MILESTONE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_7_UNUSED,
    TASK_8_UNUSED,
    TASK_BUDGET_MAX,
    TASK_ID,
    TECHNICAL_STATUS,
    build_integration_snapshot,
    run_identity_boundary_fail_closed_final_closure,
    task_6_signature,
    validate_final_closure_report,
    validate_integration_snapshot,
    write_task_6_artifacts,
)


def test_milestone_30_final_closure_integration_snapshot_is_valid():
    snapshot = build_integration_snapshot()

    assert validate_integration_snapshot(snapshot)
    assert snapshot["source_task_id"] == SOURCE_TASK_ID
    assert snapshot["source_next_stage"] == TASK_ID
    assert snapshot["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert snapshot["scope_lock_id"] == SCOPE_LOCK_ID
    assert snapshot["source_validation_status"] == "VALID"
    assert snapshot["source_validation_passed"] is True
    assert snapshot["source_private_core_access_allowed_without_verified_manuel"] is False
    assert snapshot["source_unverified_manuel_assumption_allowed"] is False
    assert snapshot["source_external_command_authority_allowed"] is False
    assert snapshot["integration_status"] == "VALID"
    assert snapshot["integration_case_count"] == 9
    assert snapshot["pass_count"] == 9
    assert snapshot["fail_count"] == 0
    assert snapshot["integration_passed"] is True
    assert snapshot["stable_integration"] is True


def test_milestone_30_final_closure_report_is_valid():
    report = run_identity_boundary_fail_closed_final_closure()

    assert validate_final_closure_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["milestone_id"] == MILESTONE_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["task_6_signature"] == task_6_signature()
    assert report["source_integration_status"] == "VALID"
    assert report["source_integration_passed"] is True
    assert report["closure_status"] == CLOSURE_STATUS
    assert report["technical_status"] == TECHNICAL_STATUS
    assert report["process_status"] == PROCESS_STATUS
    assert report["milestone_closed"] is True
    assert report["ready_for_next_milestone"] == READY_FOR_NEXT_MILESTONE
    assert report["implementation_complete"] is True
    assert report["validation_complete"] is True
    assert report["regression_integration_complete"] is True
    assert report["pass_count"] == report["required_pass_count"]
    assert report["fail_count"] == 0
    assert report["closure_passed"] is True
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["final_task_number"] == FINAL_TASK_NUMBER
    assert report["task_7_unused"] == TASK_7_UNUSED
    assert report["task_8_unused"] == TASK_8_UNUSED
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_30_final_closure_cases_cover_required_surface():
    report = run_identity_boundary_fail_closed_final_closure()
    case_ids = {case["case_id"] for case in report["closure_cases"]}

    assert case_ids == {
        "MILESTONE_30_TASK_CHAIN_REPORTS_VALID",
        "TASK_5_REGRESSION_INTEGRATION_REPORT_VALID",
        "TASK_5_REGRESSION_INTEGRATION_RUNTIME_STABILITY_VALID",
        "TASK_5_REGRESSION_INTEGRATION_ARTIFACT_SET_PRESENT",
        "TASK_5_REGRESSION_INTEGRATION_MANIFEST_CONSISTENCY_VALID",
        "TASK_5_REGRESSION_INTEGRATION_CASE_SET_VALID",
        "MILESTONE_30_FAIL_CLOSED_GUARDRAIL_FINAL_STATE_VALID",
        "MILESTONE_30_TASK_BUDGET_FINAL_STATE_VALID",
        "MILESTONE_30_FINAL_TRANSITION_VALID",
        "MILESTONE_30_STATUS_CLOSURE_VALID",
        "MILESTONE_30_SIGNATURE_CHAIN_VALID",
        "MILESTONE_30_GENERATED_ARTIFACT_COUNT_VALID",
    }
    assert all(case["passed"] is True for case in report["closure_cases"])
    assert all(case["failure_reason"] == "NONE" for case in report["closure_cases"])


def test_milestone_30_final_closure_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_6_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["milestone_id"] == MILESTONE_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["task_6_signature"] == task_6_signature()
    assert artifacts["manifest"]["closure_status"] == "CLOSED"
    assert artifacts["manifest"]["technical_status"] == "PASS"
    assert artifacts["manifest"]["process_status"] == PROCESS_STATUS
    assert artifacts["manifest"]["milestone_closed"] is True
    assert artifacts["manifest"]["ready_for_next_milestone"] is True
    assert artifacts["manifest"]["closure_passed"] is True
    assert artifacts["manifest"]["pass_count"] == artifacts["manifest"]["closure_case_count"]
    assert artifacts["manifest"]["fail_count"] == 0
    assert artifacts["manifest"]["generated_artifact_count"] == 5
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE

    report_path = Path(tmp_path) / "task-6-final-closure-report.json"
    markdown_path = Path(tmp_path) / "task-6-final-closure-report.md"
    cases_path = Path(tmp_path) / "task-6-closure-cases.json"
    manifest_path = Path(tmp_path) / "task-6-manifest.json"
    index_path = Path(tmp_path) / "task-6-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert cases_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_final_closure_report(report)
    assert "MILESTONE_30_TASK_6_IDENTITY_BOUNDARY_FAIL_CLOSED_FINAL_CLOSURE_READY=true" in index_path.read_text(encoding="utf-8")
