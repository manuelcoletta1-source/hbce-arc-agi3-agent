from pathlib import Path
import json

from hbce_arc_agi3.milestone_27_query_interface_validation import (
    NEXT_STAGE,
    REQUIRED_BLOCKED_CASE_COUNT,
    REQUIRED_READY_CASE_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_ID,
    VALIDATION_CASE_COUNT,
    VALIDATION_REVISION,
    build_validation_cases,
    run_query_interface_validation,
    task_4_signature,
    validate_case,
    validate_validation_report,
    write_task_4_artifacts,
)


def test_validation_case_set_has_required_ready_and_blocked_cases():
    cases = build_validation_cases()

    assert len(cases) == VALIDATION_CASE_COUNT
    assert sum(1 for case in cases if case.expected_query_status == "READY") == REQUIRED_READY_CASE_COUNT
    assert sum(1 for case in cases if case.expected_query_status == "BLOCKED_BY_SCOPE_LOCK") == REQUIRED_BLOCKED_CASE_COUNT
    assert {case.case_id for case in cases} == {
        "READY_MILESTONE_26_EXACT",
        "READY_CLOSED_PASS_FILTER",
        "READY_SUPPRESS_EVIDENCE",
        "READY_LIMIT_ONE",
        "BLOCK_NON_LOCAL",
        "BLOCK_FORBIDDEN_NETWORK_AND_DEEP_SCAN",
    }


def test_each_validation_case_passes_against_task_3_query_interface():
    for case in build_validation_cases():
        result = validate_case(case)
        assert result["passed"] is True
        assert result["failure_reason"] == "NONE"
        assert result["actual_query_status"] == case.expected_query_status


def test_query_interface_validation_report_is_valid_and_complete():
    report = run_query_interface_validation()

    assert validate_validation_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["validation_revision"] == VALIDATION_REVISION
    assert report["task_4_signature"] == task_4_signature()
    assert report["validation_status"] == "VALID"
    assert report["validation_case_count"] == VALIDATION_CASE_COUNT
    assert report["pass_count"] == VALIDATION_CASE_COUNT
    assert report["fail_count"] == 0
    assert report["ready_case_count"] == REQUIRED_READY_CASE_COUNT
    assert report["blocked_case_count"] == REQUIRED_BLOCKED_CASE_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_query_interface_validation_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_4_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["validation_revision"] == VALIDATION_REVISION
    assert artifacts["manifest"]["task_4_signature"] == task_4_signature()
    assert artifacts["manifest"]["validation_status"] == "VALID"
    assert artifacts["manifest"]["validation_passed"] is True
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
    assert "MILESTONE_27_TASK_4_QUERY_INTERFACE_VALIDATION_READY=true" in index_path.read_text(encoding="utf-8")
