from pathlib import Path
import json

from hbce_arc_agi3.milestone_29_governed_opening import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    IMPLEMENTATION_ALLOWED_AT_TASK_1,
    IMPLEMENTATION_STARTED,
    MILESTONE_ID,
    NEXT_STAGE,
    OBJECTIVE_SELECTION_REQUIRED_NEXT,
    OPENING_REVISION,
    SCOPE_LOCK_REQUIRED_NEXT,
    SOURCE_MILESTONE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    build_governed_opening_report,
    build_source_closure_snapshot,
    task_1_signature,
    validate_governed_opening_report,
    validate_source_closure_snapshot,
    write_task_1_artifacts,
)


def test_milestone_29_source_closure_snapshot_is_valid():
    snapshot = build_source_closure_snapshot()

    assert validate_source_closure_snapshot(snapshot)
    assert snapshot["source_task_id"] == SOURCE_TASK_ID
    assert snapshot["source_milestone_id"] == SOURCE_MILESTONE_ID
    assert snapshot["source_closure_status"] == "CLOSED"
    assert snapshot["source_technical_status"] == "PASS"
    assert snapshot["source_task_budget_max"] == 8
    assert snapshot["source_final_task_number"] == 6
    assert snapshot["source_task_7_used"] is False
    assert snapshot["source_task_8_used"] is False
    assert snapshot["source_milestone_closed"] is True
    assert snapshot["source_ready_for_next_milestone"] is True
    assert snapshot["source_next_stage"] == TASK_ID


def test_milestone_29_governed_opening_report_is_valid():
    report = build_governed_opening_report()

    assert validate_governed_opening_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["milestone_id"] == MILESTONE_ID
    assert report["source_milestone_id"] == SOURCE_MILESTONE_ID
    assert report["opening_revision"] == OPENING_REVISION
    assert report["task_1_signature"] == task_1_signature()
    assert report["opening_status"] == "OPEN"
    assert report["technical_status"] == "PASS"
    assert report["process_status"] == "GOVERNED_OPENING_WITH_TASK_BUDGET_MAX_8"
    assert report["source_dependency_valid"] is True
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["implementation_started"] is IMPLEMENTATION_STARTED is False
    assert report["implementation_allowed_at_task_1"] is IMPLEMENTATION_ALLOWED_AT_TASK_1 is False
    assert report["objective_selection_required_next"] is OBJECTIVE_SELECTION_REQUIRED_NEXT is True
    assert report["scope_lock_required_next"] is SCOPE_LOCK_REQUIRED_NEXT is True
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_29_governed_opening_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_1_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["milestone_id"] == MILESTONE_ID
    assert artifacts["manifest"]["opening_revision"] == OPENING_REVISION
    assert artifacts["manifest"]["task_1_signature"] == task_1_signature()
    assert artifacts["manifest"]["opening_status"] == "OPEN"
    assert artifacts["manifest"]["technical_status"] == "PASS"
    assert artifacts["manifest"]["process_status"] == "GOVERNED_OPENING_WITH_TASK_BUDGET_MAX_8"
    assert artifacts["manifest"]["task_budget_max"] == 8
    assert artifacts["manifest"]["current_task_number"] == 1
    assert artifacts["manifest"]["implementation_started"] is False
    assert artifacts["manifest"]["implementation_allowed_at_task_1"] is False
    assert artifacts["manifest"]["objective_selection_required_next"] is True
    assert artifacts["manifest"]["scope_lock_required_next"] is True
    assert artifacts["manifest"]["generated_artifact_count"] == 5
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE

    report_path = Path(tmp_path) / "task-1-governed-opening.json"
    markdown_path = Path(tmp_path) / "task-1-governed-opening.md"
    snapshot_path = Path(tmp_path) / "task-1-source-closure-snapshot.json"
    manifest_path = Path(tmp_path) / "task-1-manifest.json"
    index_path = Path(tmp_path) / "task-1-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert snapshot_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_governed_opening_report(report)
    assert "MILESTONE_29_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in index_path.read_text(encoding="utf-8")
