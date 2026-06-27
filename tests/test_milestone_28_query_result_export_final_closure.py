from pathlib import Path
import json

from hbce_arc_agi3.milestone_28_query_result_export_final_closure import (
    CLOSURE_CASE_COUNT,
    CURRENT_TASK_NUMBER,
    FINAL_TASK_NUMBER,
    NEXT_STAGE,
    PROCESS_STATUS,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    build_regression_integration_snapshot,
    run_query_result_export_final_closure,
    task_6_signature,
    validate_final_closure_report,
    validate_regression_integration_snapshot,
    write_task_6_artifacts,
)


def test_query_result_export_final_closure_integration_snapshot_is_stable():
    snapshot = build_regression_integration_snapshot()

    assert validate_regression_integration_snapshot(snapshot)
    assert snapshot["source_task_id"] == SOURCE_TASK_ID
    assert snapshot["source_next_stage"] == TASK_ID
    assert snapshot["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert snapshot["scope_lock_id"] == SCOPE_LOCK_ID
    assert snapshot["source_validation_status"] == "VALID"
    assert snapshot["source_export_status"] == "READY"
    assert snapshot["integration_status"] == "VALID"
    assert snapshot["pass_count"] == 7
    assert snapshot["fail_count"] == 0
    assert snapshot["stable_integration"] is True


def test_query_result_export_final_closure_report_is_valid():
    report = run_query_result_export_final_closure()

    assert validate_final_closure_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["task_6_signature"] == task_6_signature()
    assert report["source_integration_status"] == "VALID"
    assert report["source_validation_status"] == "VALID"
    assert report["source_export_status"] == "READY"
    assert report["closure_status"] == "CLOSED"
    assert report["technical_status"] == "PASS"
    assert report["process_status"] == PROCESS_STATUS
    assert report["closure_case_count"] == CLOSURE_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["final_task_number"] == FINAL_TASK_NUMBER
    assert report["task_7_used"] is False
    assert report["task_8_used"] is False
    assert report["milestone_closed"] is True
    assert report["ready_for_next_milestone"] is True
    assert report["next_stage"] == NEXT_STAGE


def test_query_result_export_final_closure_cases_cover_chain_budget_and_transition():
    report = run_query_result_export_final_closure()
    case_ids = {case["case_id"] for case in report["case_results"]}

    assert case_ids == {
        "TASK_5_REGRESSION_INTEGRATION_REPORT_VALID",
        "TASK_5_RUNTIME_STABILITY_VALID",
        "TASK_5_ARTIFACT_SET_PRESENT",
        "TASK_5_MANIFEST_CONSISTENCY_VALID",
        "TASK_5_INDEX_MARKERS_VALID",
        "TASK_BUDGET_FINALIZATION_VALID",
        "FINAL_CLOSURE_TRANSITION_VALID",
        "QUERY_RESULT_EXPORT_CHAIN_STATUS_VALID",
    }
    assert all(case["passed"] is True for case in report["case_results"])
    assert all(case["failure_reason"] == "NONE" for case in report["case_results"])


def test_query_result_export_final_closure_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_6_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["task_6_signature"] == task_6_signature()
    assert artifacts["manifest"]["closure_status"] == "CLOSED"
    assert artifacts["manifest"]["technical_status"] == "PASS"
    assert artifacts["manifest"]["process_status"] == PROCESS_STATUS
    assert artifacts["manifest"]["closure_passed"] is True
    assert artifacts["manifest"]["pass_count"] == 8
    assert artifacts["manifest"]["fail_count"] == 0
    assert artifacts["manifest"]["final_task_number"] == 6
    assert artifacts["manifest"]["task_7_used"] is False
    assert artifacts["manifest"]["task_8_used"] is False
    assert artifacts["manifest"]["generated_artifact_count"] == 5

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
    assert validate_final_closure_report(report)
    assert "MILESTONE_28_TASK_6_QUERY_RESULT_EXPORT_FINAL_CLOSURE_READY=true" in index_path.read_text(encoding="utf-8")
