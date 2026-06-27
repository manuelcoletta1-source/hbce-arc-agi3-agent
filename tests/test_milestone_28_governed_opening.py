from pathlib import Path
import json

from hbce_arc_agi3.milestone_28_governed_opening import (
    CURRENT_TASK_NUMBER,
    MILESTONE_ID,
    NEXT_STAGE,
    OPENING_REVISION,
    PROCESS_STATUS,
    SOURCE_MILESTONE_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    build_source_closure_snapshot,
    run_governed_opening,
    task_1_signature,
    validate_governed_opening_report,
    validate_source_closure_snapshot,
    write_task_1_artifacts,
)


def test_milestone_28_source_closure_snapshot_validates_milestone_27_closure():
    snapshot = build_source_closure_snapshot()

    assert validate_source_closure_snapshot(snapshot)
    assert snapshot["source_milestone_id"] == "MILESTONE_27"
    assert snapshot["source_final_status"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert snapshot["source_technical_status"] == "PASS"
    assert snapshot["source_final_task_number"] == 6
    assert snapshot["source_task_7_used"] is False
    assert snapshot["source_task_8_used"] is False
    assert snapshot["source_milestone_closed"] is True
    assert snapshot["source_ready_for_next_milestone"] is True


def test_milestone_28_governed_opening_report_is_ready_and_budgeted():
    report = run_governed_opening()

    assert validate_governed_opening_report(report)
    assert report["task_id"] == TASK_ID
    assert report["milestone_id"] == MILESTONE_ID
    assert report["source_milestone_id"] == SOURCE_MILESTONE_ID
    assert report["opening_revision"] == OPENING_REVISION
    assert report["task_1_signature"] == task_1_signature()
    assert report["opening_status"] == "OPEN"
    assert report["technical_status"] == "PASS"
    assert report["process_status"] == PROCESS_STATUS
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["implementation_started"] is False
    assert report["implementation_allowed_at_task_1"] is False
    assert report["objective_selection_required_next"] is True
    assert report["scope_lock_required_next"] is True
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_28_opening_blocks_implementation_until_task_2_scope_lock():
    report = run_governed_opening()

    assert report["implementation_started"] is False
    assert report["implementation_allowed_at_task_1"] is False
    assert report["objective_selection_required_next"] is True
    assert report["scope_lock_required_next"] is True
    assert report["ready_for_objective_selection"] is True
    assert report["ready_for_scope_lock"] is True
    assert report["deep_recursive_dependency_traversal_allowed"] is False


def test_milestone_28_governed_opening_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_1_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["milestone_id"] == MILESTONE_ID
    assert artifacts["manifest"]["source_milestone_id"] == SOURCE_MILESTONE_ID
    assert artifacts["manifest"]["opening_revision"] == OPENING_REVISION
    assert artifacts["manifest"]["task_1_signature"] == task_1_signature()
    assert artifacts["manifest"]["opening_status"] == "OPEN"
    assert artifacts["manifest"]["opening_ready"] is True
    assert artifacts["manifest"]["task_budget_max"] == 8
    assert artifacts["manifest"]["current_task_number"] == 1
    assert artifacts["manifest"]["implementation_started"] is False
    assert artifacts["manifest"]["implementation_allowed_at_task_1"] is False
    assert artifacts["manifest"]["objective_selection_required_next"] is True
    assert artifacts["manifest"]["scope_lock_required_next"] is True
    assert artifacts["manifest"]["generated_artifact_count"] == 4

    report_path = Path(tmp_path) / "task-1-governed-opening.json"
    markdown_path = Path(tmp_path) / "task-1-governed-opening.md"
    manifest_path = Path(tmp_path) / "task-1-manifest.json"
    index_path = Path(tmp_path) / "task-1-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_governed_opening_report(report)
    assert "MILESTONE_28_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in index_path.read_text(encoding="utf-8")
