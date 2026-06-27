from pathlib import Path
import json

from hbce_arc_agi3.milestone_27_query_interface_regression_integration import (
    NEXT_STAGE,
    REGRESSION_CASE_COUNT,
    REGRESSION_REVISION,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_ID,
    run_query_interface_regression_integration,
    task_5_signature,
    validate_regression_integration_report,
    write_task_5_artifacts,
)


def test_query_interface_regression_integration_report_is_integrated():
    report = run_query_interface_regression_integration()

    assert validate_regression_integration_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["regression_revision"] == REGRESSION_REVISION
    assert report["task_5_signature"] == task_5_signature()
    assert report["integration_status"] == "INTEGRATED"
    assert report["regression_case_count"] == REGRESSION_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_query_interface_regression_cases_cover_stability_artifact_and_scope_guard():
    report = run_query_interface_regression_integration()
    case_ids = {case["case_id"] for case in report["case_results"]}

    assert case_ids == {
        "TASK_4_VALIDATION_REPORT_ARTIFACT_VALID",
        "TASK_3_PRIMARY_QUERY_RUNTIME_STABLE",
        "TASK_3_BLOCKED_QUERY_RUNTIME_STABLE",
        "TASK_4_RUNTIME_VALIDATION_REPORT_STABLE",
        "TASK_4_CASE_MATRIX_INTEGRATED",
        "SCOPE_LOCK_REGRESSION_GUARD_BLOCKS_FORBIDDEN_OPERATIONS",
    }

    assert all(case["passed"] is True for case in report["case_results"])
    assert all(case["failure_reason"] == "NONE" for case in report["case_results"])


def test_query_interface_regression_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_5_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["regression_revision"] == REGRESSION_REVISION
    assert artifacts["manifest"]["task_5_signature"] == task_5_signature()
    assert artifacts["manifest"]["integration_status"] == "INTEGRATED"
    assert artifacts["manifest"]["integration_passed"] is True
    assert artifacts["manifest"]["generated_artifact_count"] == 5

    report_path = Path(tmp_path) / "task-5-regression-integration-report.json"
    markdown_path = Path(tmp_path) / "task-5-regression-integration-report.md"
    cases_path = Path(tmp_path) / "task-5-regression-cases.json"
    manifest_path = Path(tmp_path) / "task-5-manifest.json"
    index_path = Path(tmp_path) / "task-5-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert cases_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_regression_integration_report(report)
    assert "MILESTONE_27_TASK_5_QUERY_INTERFACE_REGRESSION_INTEGRATION_READY=true" in index_path.read_text(encoding="utf-8")
