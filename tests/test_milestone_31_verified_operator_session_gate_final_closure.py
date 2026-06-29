import json
from pathlib import Path

from hbce_arc_agi3.milestone_31_verified_operator_session_gate_final_closure import (
    CLOSURE_CASE_COUNT,
    CURRENT_TASK_NUMBER,
    FINAL_CLOSURE_REVISION,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SESSION_GATE_MODE_ID,
    SOURCE_REGRESSION_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    run_verified_operator_session_gate_final_closure,
    task_6_signature,
    validate_verified_operator_session_gate_final_closure_report,
    write_task_6_artifacts,
)


def test_milestone_31_session_gate_final_closure_report_is_valid():
    report = run_verified_operator_session_gate_final_closure()

    assert validate_verified_operator_session_gate_final_closure_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_regression_task_id"] == SOURCE_REGRESSION_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["session_gate_mode_id"] == SESSION_GATE_MODE_ID
    assert report["final_closure_revision"] == FINAL_CLOSURE_REVISION
    assert report["task_6_signature"] == task_6_signature()
    assert report["source_integration_status"] == "VALID"
    assert report["source_integration_passed"] is True
    assert report["source_integration_case_count"] == 10
    assert report["source_pass_count"] == 10
    assert report["source_fail_count"] == 0
    assert report["closure_status"] == "CLOSED"
    assert report["closure_case_count"] == CLOSURE_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["closure_passed"] is True
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_31_session_gate_final_closure_cases_are_all_passed():
    report = run_verified_operator_session_gate_final_closure()

    assert len(report["closure_cases"]) == CLOSURE_CASE_COUNT
    assert all(case["passed"] is True for case in report["closure_cases"])
    assert all(case["failure_reason"] == "NONE" for case in report["closure_cases"])
    assert {case["case_id"] for case in report["closure_cases"]} == {
        "TASK_5_REGRESSION_INTEGRATION_REMAINS_VALID",
        "TASK_5_REGRESSION_CASES_REMAIN_VALID",
        "TASK_5_ARTIFACT_SET_REMAINS_PRESENT",
        "TASK_5_TRANSITION_TO_FINAL_CLOSURE_REMAINS_VALID",
        "TASK_4_VALIDATION_CHAIN_REMAINS_VALID",
        "TASK_3_IMPLEMENTATION_CHAIN_REMAINS_VALID",
        "TASK_2_SCOPE_LOCK_CHAIN_REMAINS_VALID",
        "TASK_1_GOVERNED_OPENING_CHAIN_REMAINS_VALID",
        "FAIL_CLOSED_AUTHORIZATION_DENIALS_REMAIN_ENFORCED",
        "TASK_BUDGET_REMAINS_WITHIN_GOVERNED_LIMIT",
        "MILESTONE_31_CLOSURE_ARTIFACT_PLAN_REMAINS_COMPLETE",
        "MILESTONE_31_FINAL_CLOSURE_READY_FOR_NEXT_GOVERNED_OPENING",
    }


def test_milestone_31_session_gate_final_closure_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_6_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_regression_task_id"] == SOURCE_REGRESSION_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["session_gate_mode_id"] == SESSION_GATE_MODE_ID
    assert artifacts["manifest"]["final_closure_revision"] == FINAL_CLOSURE_REVISION
    assert artifacts["manifest"]["task_6_signature"] == task_6_signature()
    assert artifacts["manifest"]["closure_status"] == "CLOSED"
    assert artifacts["manifest"]["closure_passed"] is True
    assert artifacts["manifest"]["closure_case_count"] == CLOSURE_CASE_COUNT
    assert artifacts["manifest"]["pass_count"] == REQUIRED_PASS_COUNT
    assert artifacts["manifest"]["fail_count"] == REQUIRED_FAIL_COUNT
    assert artifacts["manifest"]["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE

    report_path = Path(tmp_path) / "task-6-final-closure-report.json"
    markdown_path = Path(tmp_path) / "task-6-final-closure-report.md"
    cases_path = Path(tmp_path) / "task-6-final-closure-cases.json"
    manifest_path = Path(tmp_path) / "task-6-manifest.json"
    index_path = Path(tmp_path) / "task-6-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert cases_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_verified_operator_session_gate_final_closure_report(report)
    assert "MILESTONE_31_TASK_6_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_FINAL_CLOSURE_READY=true" in index_path.read_text(encoding="utf-8")


def test_milestone_31_session_gate_final_closure_rejects_mutated_report():
    report = run_verified_operator_session_gate_final_closure()
    report["closure_status"] = "OPEN"

    assert not validate_verified_operator_session_gate_final_closure_report(report)
