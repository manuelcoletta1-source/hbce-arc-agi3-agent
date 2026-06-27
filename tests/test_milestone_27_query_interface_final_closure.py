from pathlib import Path
import json

from hbce_arc_agi3.milestone_27_query_interface_final_closure import (
    CLOSURE_CASE_COUNT,
    FINAL_CLOSURE_REVISION,
    FINAL_TASK_NUMBER,
    NEXT_STAGE,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    run_query_interface_final_closure,
    task_6_signature,
    validate_final_closure_report,
    write_task_6_artifacts,
)


def test_query_interface_final_closure_report_is_closed():
    report = run_query_interface_final_closure()

    assert validate_final_closure_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["final_closure_revision"] == FINAL_CLOSURE_REVISION
    assert report["task_6_signature"] == task_6_signature()
    assert report["closure_status"] == "CLOSED"
    assert report["technical_status"] == "PASS"
    assert report["process_status"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert report["closure_case_count"] == CLOSURE_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["final_task_number"] == FINAL_TASK_NUMBER
    assert report["task_7_used"] is False
    assert report["task_8_used"] is False
    assert report["milestone_closed"] is True
    assert report["ready_for_next_milestone"] is True
    assert report["next_stage"] == NEXT_STAGE


def test_query_interface_final_closure_cases_cover_chain_scope_artifacts_budget_and_next_stage():
    report = run_query_interface_final_closure()
    case_ids = {case["case_id"] for case in report["case_results"]}

    assert case_ids == {
        "TASK_1_TO_5_DOCUMENT_CHAIN_VALID",
        "SCOPE_LOCK_CONSISTENT_ACROSS_TASK_2_TO_6",
        "TASK_3_QUERY_INTERFACE_ARTIFACT_READY",
        "TASK_4_VALIDATION_ARTIFACT_AND_RUNTIME_VALID",
        "TASK_5_REGRESSION_ARTIFACT_AND_RUNTIME_INTEGRATED",
        "TASK_BUDGET_CLOSED_AT_TASK_6_WITH_TASK_7_AND_8_UNUSED",
        "NEXT_MILESTONE_READY",
    }

    assert all(case["passed"] is True for case in report["case_results"])
    assert all(case["failure_reason"] == "NONE" for case in report["case_results"])


def test_query_interface_final_closure_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_6_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["final_closure_revision"] == FINAL_CLOSURE_REVISION
    assert artifacts["manifest"]["task_6_signature"] == task_6_signature()
    assert artifacts["manifest"]["closure_status"] == "CLOSED"
    assert artifacts["manifest"]["closure_passed"] is True
    assert artifacts["manifest"]["task_budget_max"] == 8
    assert artifacts["manifest"]["final_task_number"] == 6
    assert artifacts["manifest"]["task_7_used"] is False
    assert artifacts["manifest"]["task_8_used"] is False
    assert artifacts["manifest"]["generated_artifact_count"] == 5

    report_path = Path(tmp_path) / "task-6-final-closure-report.json"
    markdown_path = Path(tmp_path) / "task-6-final-closure-report.md"
    closure_index_path = Path(tmp_path) / "task-6-closure-index.json"
    manifest_path = Path(tmp_path) / "task-6-manifest.json"
    index_path = Path(tmp_path) / "task-6-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert closure_index_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_final_closure_report(report)
    assert "MILESTONE_27_TASK_6_QUERY_INTERFACE_FINAL_CLOSURE_READY=true" in index_path.read_text(encoding="utf-8")
