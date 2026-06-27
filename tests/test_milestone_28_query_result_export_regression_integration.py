from pathlib import Path
import json

from hbce_arc_agi3.milestone_28_query_result_export_regression_integration import (
    CURRENT_TASK_NUMBER,
    INTEGRATION_CASE_COUNT,
    NEXT_STAGE,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_VALIDATION_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    REGRESSION_INTEGRATION_REVISION,
    build_validation_snapshot,
    run_query_result_export_regression_integration,
    task_5_signature,
    validate_regression_integration_report,
    validate_validation_snapshot,
    write_task_5_artifacts,
)


def test_query_result_export_regression_integration_validation_snapshot_is_stable():
    snapshot = build_validation_snapshot()

    assert validate_validation_snapshot(snapshot)
    assert snapshot["source_validation_task_id"] == SOURCE_VALIDATION_TASK_ID
    assert snapshot["source_next_stage"] == TASK_ID
    assert snapshot["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert snapshot["scope_lock_id"] == SCOPE_LOCK_ID
    assert snapshot["validation_status"] == "VALID"
    assert snapshot["pass_count"] == 6
    assert snapshot["fail_count"] == 0
    assert snapshot["stable_validation"] is True


def test_query_result_export_regression_integration_report_is_valid():
    report = run_query_result_export_regression_integration()

    assert validate_regression_integration_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_VALIDATION_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["regression_integration_revision"] == REGRESSION_INTEGRATION_REVISION
    assert report["task_5_signature"] == task_5_signature()
    assert report["source_validation_status"] == "VALID"
    assert report["source_export_status"] == "READY"
    assert report["integration_status"] == "VALID"
    assert report["integration_case_count"] == INTEGRATION_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["next_stage"] == NEXT_STAGE


def test_query_result_export_regression_integration_cases_cover_chain_and_guards():
    report = run_query_result_export_regression_integration()
    case_ids = {case["case_id"] for case in report["case_results"]}

    assert case_ids == {
        "TASK_4_VALIDATION_REPORT_VALID",
        "TASK_4_RUNTIME_STABILITY_VALID",
        "TASK_4_VALIDATION_ARTIFACT_SET_PRESENT",
        "TASK_4_VALIDATION_MANIFEST_CONSISTENCY_VALID",
        "TASK_4_VALIDATION_INDEX_MARKERS_VALID",
        "TASK_3_EXPORT_PAYLOAD_GUARDS_STILL_VALID",
        "TASK_BUDGET_AND_TRANSITION_VALID",
    }
    assert all(case["passed"] is True for case in report["case_results"])
    assert all(case["failure_reason"] == "NONE" for case in report["case_results"])


def test_query_result_export_regression_integration_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_5_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_VALIDATION_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["regression_integration_revision"] == REGRESSION_INTEGRATION_REVISION
    assert artifacts["manifest"]["task_5_signature"] == task_5_signature()
    assert artifacts["manifest"]["integration_status"] == "VALID"
    assert artifacts["manifest"]["integration_passed"] is True
    assert artifacts["manifest"]["pass_count"] == 7
    assert artifacts["manifest"]["fail_count"] == 0
    assert artifacts["manifest"]["generated_artifact_count"] == 5

    report_path = Path(tmp_path) / "task-5-regression-integration-report.json"
    markdown_path = Path(tmp_path) / "task-5-regression-integration-report.md"
    cases_path = Path(tmp_path) / "task-5-regression-integration-cases.json"
    manifest_path = Path(tmp_path) / "task-5-manifest.json"
    index_path = Path(tmp_path) / "task-5-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert cases_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_regression_integration_report(report)
    assert "MILESTONE_28_TASK_5_QUERY_RESULT_EXPORT_REGRESSION_INTEGRATION_READY=true" in index_path.read_text(encoding="utf-8")
