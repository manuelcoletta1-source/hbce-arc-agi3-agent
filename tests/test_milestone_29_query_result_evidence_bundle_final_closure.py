from pathlib import Path
import json

from hbce_arc_agi3.milestone_29_query_result_evidence_bundle_final_closure import (
    CLOSURE_CASE_COUNT,
    CURRENT_TASK_NUMBER,
    FINAL_CLOSURE_REVISION,
    FINAL_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    PROCESS_STATUS,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_INTEGRATION_TASK_ID,
    TASK_7_USED,
    TASK_8_USED,
    TASK_BUDGET_MAX,
    TASK_ID,
    build_integration_snapshot,
    run_query_result_evidence_bundle_final_closure,
    task_6_signature,
    validate_final_closure_report,
    validate_integration_snapshot,
    write_task_6_artifacts,
)


def test_milestone_29_final_closure_integration_snapshot_is_stable():
    snapshot = build_integration_snapshot()

    assert validate_integration_snapshot(snapshot)
    assert snapshot["source_integration_task_id"] == SOURCE_INTEGRATION_TASK_ID
    assert snapshot["source_next_stage"] == TASK_ID
    assert snapshot["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert snapshot["scope_lock_id"] == SCOPE_LOCK_ID
    assert snapshot["source_validation_status"] == "VALID"
    assert snapshot["source_implementation_status"] == "READY"
    assert snapshot["source_scope_lock_valid"] is True
    assert snapshot["source_chain_valid"] is True
    assert snapshot["source_evidence_valid"] is True
    assert snapshot["integration_status"] == "VALID"
    assert snapshot["integration_case_count"] == 9
    assert snapshot["pass_count"] == 9
    assert snapshot["fail_count"] == 0
    assert snapshot["stable_integration"] is True


def test_milestone_29_final_closure_report_is_valid():
    report = run_query_result_evidence_bundle_final_closure()

    assert validate_final_closure_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_INTEGRATION_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["final_closure_revision"] == FINAL_CLOSURE_REVISION
    assert report["task_6_signature"] == task_6_signature()
    assert report["source_integration_status"] == "VALID"
    assert report["source_validation_status"] == "VALID"
    assert report["source_implementation_status"] == "READY"
    assert report["closure_status"] == "CLOSED"
    assert report["technical_status"] == "PASS"
    assert report["process_status"] == PROCESS_STATUS
    assert report["closure_case_count"] == CLOSURE_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["final_task_number"] == FINAL_TASK_NUMBER
    assert report["task_7_used"] is TASK_7_USED is False
    assert report["task_8_used"] is TASK_8_USED is False
    assert report["milestone_closed"] is True
    assert report["ready_for_next_milestone"] is True
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_29_final_closure_cases_cover_final_surface():
    report = run_query_result_evidence_bundle_final_closure()
    case_ids = {case["case_id"] for case in report["case_results"]}

    assert case_ids == {
        "TASK_5_REGRESSION_INTEGRATION_REPORT_VALID",
        "TASK_5_REGRESSION_INTEGRATION_RUNTIME_STABILITY_VALID",
        "TASK_5_REGRESSION_INTEGRATION_ARTIFACT_SET_PRESENT",
        "TASK_5_REGRESSION_INTEGRATION_MANIFEST_CONSISTENCY_VALID",
        "TASK_5_REGRESSION_INTEGRATION_INDEX_MARKERS_VALID",
        "MILESTONE_29_LINEAGE_FROM_OPENING_TO_INTEGRATION_VALID",
        "MILESTONE_29_TASK_BUDGET_AND_FINAL_CLOSURE_VALID",
        "MILESTONE_29_SOURCE_STATUSES_REMAIN_VALID",
    }
    assert all(case["passed"] is True for case in report["case_results"])
    assert all(case["failure_reason"] == "NONE" for case in report["case_results"])


def test_milestone_29_final_closure_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_6_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_INTEGRATION_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["task_6_signature"] == task_6_signature()
    assert artifacts["manifest"]["closure_status"] == "CLOSED"
    assert artifacts["manifest"]["technical_status"] == "PASS"
    assert artifacts["manifest"]["process_status"] == PROCESS_STATUS
    assert artifacts["manifest"]["closure_passed"] is True
    assert artifacts["manifest"]["pass_count"] == 8
    assert artifacts["manifest"]["fail_count"] == 0
    assert artifacts["manifest"]["task_7_used"] is False
    assert artifacts["manifest"]["task_8_used"] is False
    assert artifacts["manifest"]["milestone_closed"] is True
    assert artifacts["manifest"]["ready_for_next_milestone"] is True
    assert artifacts["manifest"]["generated_artifact_count"] == 5
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
    assert validate_final_closure_report(report)
    assert "MILESTONE_29_TASK_6_QUERY_RESULT_EVIDENCE_BUNDLE_FINAL_CLOSURE_READY=true" in index_path.read_text(encoding="utf-8")
