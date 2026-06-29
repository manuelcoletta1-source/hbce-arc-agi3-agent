import json
from pathlib import Path

from hbce_arc_agi3.milestone_33_governed_opening import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    MILESTONE_ID,
    NEXT_STAGE,
    OPENING_CASE_COUNT,
    OPENING_REVISION,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    SOURCE_CLOSURE_TASK_ID,
    SOURCE_MILESTONE_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    run_milestone_33_governed_opening,
    task_1_signature,
    validate_milestone_33_governed_opening_report,
    write_task_1_artifacts,
)


def test_milestone_33_governed_opening_report_is_valid():
    report = run_milestone_33_governed_opening()

    assert validate_milestone_33_governed_opening_report(report)
    assert report["task_id"] == TASK_ID
    assert report["milestone_id"] == MILESTONE_ID
    assert report["source_milestone_id"] == SOURCE_MILESTONE_ID
    assert report["source_closure_task_id"] == SOURCE_CLOSURE_TASK_ID
    assert report["opening_revision"] == OPENING_REVISION
    assert report["task_1_signature"] == task_1_signature()
    assert report["source_closure_status"] == "CLOSED"
    assert report["source_closure_passed"] is True
    assert report["opening_status"] == "READY"
    assert report["objective_selection_status"] == "PENDING_TASK_2_SCOPE_LOCK"
    assert report["opening_case_count"] == OPENING_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["opening_passed"] is True
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_33_governed_opening_cases_are_all_passed():
    report = run_milestone_33_governed_opening()

    assert len(report["opening_cases"]) == OPENING_CASE_COUNT
    assert all(case["passed"] is True for case in report["opening_cases"])
    assert all(case["failure_reason"] == "NONE" for case in report["opening_cases"])


def test_milestone_33_governed_opening_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_1_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["milestone_id"] == MILESTONE_ID
    assert artifacts["manifest"]["source_milestone_id"] == SOURCE_MILESTONE_ID
    assert artifacts["manifest"]["source_closure_task_id"] == SOURCE_CLOSURE_TASK_ID
    assert artifacts["manifest"]["opening_revision"] == OPENING_REVISION
    assert artifacts["manifest"]["task_1_signature"] == task_1_signature()
    assert artifacts["manifest"]["opening_status"] == "READY"
    assert artifacts["manifest"]["opening_passed"] is True
    assert artifacts["manifest"]["opening_case_count"] == OPENING_CASE_COUNT
    assert artifacts["manifest"]["pass_count"] == REQUIRED_PASS_COUNT
    assert artifacts["manifest"]["fail_count"] == REQUIRED_FAIL_COUNT
    assert artifacts["manifest"]["task_budget_max"] == TASK_BUDGET_MAX
    assert artifacts["manifest"]["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE

    report_path = Path(tmp_path) / "task-1-governed-opening-report.json"
    index_path = Path(tmp_path) / "task-1-index.txt"

    assert report_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_milestone_33_governed_opening_report(report)
    assert "MILESTONE_33_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in index_path.read_text(encoding="utf-8")


def test_milestone_33_governed_opening_rejects_mutated_report():
    report = run_milestone_33_governed_opening()
    report["opening_status"] = "INVALID"

    assert not validate_milestone_33_governed_opening_report(report)
