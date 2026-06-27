from pathlib import Path
import json

from hbce_arc_agi3.milestone_28_query_result_export_validation import (
    CURRENT_TASK_NUMBER,
    NEXT_STAGE,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    VALIDATION_CASE_COUNT,
    VALIDATION_REVISION,
    run_query_result_export_validation,
    task_4_signature,
    validate_validation_report,
    write_task_4_artifacts,
)


def test_query_result_export_validation_report_is_valid():
    report = run_query_result_export_validation()

    assert validate_validation_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["validation_revision"] == VALIDATION_REVISION
    assert report["task_4_signature"] == task_4_signature()
    assert report["source_export_status"] == "READY"
    assert report["source_exported_record_count"] == 1
    assert report["validation_status"] == "VALID"
    assert report["validation_case_count"] == VALIDATION_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["next_stage"] == NEXT_STAGE


def test_query_result_export_validation_cases_cover_payload_runtime_artifacts_and_scope():
    report = run_query_result_export_validation()
    case_ids = {case["case_id"] for case in report["case_results"]}

    assert case_ids == {
        "PERSISTED_EXPORT_PAYLOAD_VALID",
        "RUNTIME_EXPORT_STABILITY_VALID",
        "EXPORT_MANIFEST_CONSISTENCY_VALID",
        "EXPORT_INDEX_CONSISTENCY_VALID",
        "MARKDOWN_AND_TEXT_INDEX_CONSISTENCY_VALID",
        "SCOPE_AUTHORITY_GUARDS_VALID",
    }
    assert all(case["passed"] is True for case in report["case_results"])
    assert all(case["failure_reason"] == "NONE" for case in report["case_results"])


def test_query_result_export_validation_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_4_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["validation_revision"] == VALIDATION_REVISION
    assert artifacts["manifest"]["task_4_signature"] == task_4_signature()
    assert artifacts["manifest"]["validation_status"] == "VALID"
    assert artifacts["manifest"]["validation_passed"] is True
    assert artifacts["manifest"]["pass_count"] == 6
    assert artifacts["manifest"]["fail_count"] == 0
    assert artifacts["manifest"]["generated_artifact_count"] == 5

    report_path = Path(tmp_path) / "task-4-validation-report.json"
    markdown_path = Path(tmp_path) / "task-4-validation-report.md"
    cases_path = Path(tmp_path) / "task-4-validation-cases.json"
    manifest_path = Path(tmp_path) / "task-4-manifest.json"
    index_path = Path(tmp_path) / "task-4-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert cases_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_validation_report(report)
    assert "MILESTONE_28_TASK_4_QUERY_RESULT_EXPORT_VALIDATION_READY=true" in index_path.read_text(encoding="utf-8")
