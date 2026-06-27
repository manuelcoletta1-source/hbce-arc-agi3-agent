from pathlib import Path
import json

from hbce_arc_agi3.milestone_28_objective_scope_lock import (
    CURRENT_TASK_NUMBER,
    FORBIDDEN_OPERATIONS,
    MILESTONE_ID,
    NEXT_STAGE,
    OBJECTIVE_SELECTION_REVISION,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    build_objective_candidates,
    build_source_opening_snapshot,
    run_objective_scope_lock,
    task_2_signature,
    validate_objective_scope_lock_report,
    validate_source_opening_snapshot,
    write_task_2_artifacts,
)


def test_milestone_28_task_2_source_opening_snapshot_is_valid():
    snapshot = build_source_opening_snapshot()

    assert validate_source_opening_snapshot(snapshot)
    assert snapshot["source_task_id"] == SOURCE_TASK_ID
    assert snapshot["source_milestone_id"] == MILESTONE_ID
    assert snapshot["source_opening_status"] == "OPEN"
    assert snapshot["source_technical_status"] == "PASS"
    assert snapshot["source_task_budget_max"] == 8
    assert snapshot["source_current_task_number"] == 1
    assert snapshot["source_implementation_started"] is False
    assert snapshot["source_objective_selection_required_next"] is True
    assert snapshot["source_scope_lock_required_next"] is True


def test_milestone_28_task_2_selects_exactly_one_local_only_objective():
    candidates = build_objective_candidates()
    selected = [candidate for candidate in candidates if candidate.selected]

    assert len(candidates) == 3
    assert len(selected) == 1
    assert selected[0].objective_id == SELECTED_OBJECTIVE_ID
    assert selected[0].local_only is True
    assert selected[0].implementation_allowed_next is True
    assert all(candidate.objective_id for candidate in candidates)


def test_milestone_28_task_2_scope_lock_report_is_ready():
    report = run_objective_scope_lock()

    assert validate_objective_scope_lock_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["milestone_id"] == MILESTONE_ID
    assert report["objective_selection_revision"] == OBJECTIVE_SELECTION_REVISION
    assert report["task_2_signature"] == task_2_signature()
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["objective_selection_ready"] is True
    assert report["scope_locked"] is True
    assert report["implementation_started"] is False
    assert report["implementation_allowed_next"] is True
    assert report["implementation_allowed_at_task_2"] is False
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_28_task_2_scope_blocks_forbidden_operations():
    report = run_objective_scope_lock()

    assert report["local_only"] is True
    assert report["network_access_allowed"] is False
    assert report["shell_execution_allowed"] is False
    assert report["repository_mutation_allowed"] is False
    assert report["remote_registry_lookup_allowed"] is False
    assert report["deep_recursive_dependency_traversal_allowed"] is False
    assert report["external_model_call_allowed"] is False
    assert tuple(report["forbidden_operations"]) == FORBIDDEN_OPERATIONS
    assert "NETWORK_ACCESS" in report["forbidden_operations"]
    assert "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL" in report["forbidden_operations"]


def test_milestone_28_task_2_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_2_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["scope_ready"] is True
    assert artifacts["manifest"]["generated_artifact_count"] == 5

    report_path = Path(tmp_path) / "task-2-objective-scope-lock.json"
    markdown_path = Path(tmp_path) / "task-2-objective-scope-lock.md"
    candidates_path = Path(tmp_path) / "task-2-objective-candidates.json"
    manifest_path = Path(tmp_path) / "task-2-manifest.json"
    index_path = Path(tmp_path) / "task-2-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert candidates_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_objective_scope_lock_report(report)
    assert "MILESTONE_28_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in index_path.read_text(encoding="utf-8")
