from pathlib import Path
import json

from hbce_arc_agi3.milestone_29_objective_scope_lock import (
    CURRENT_TASK_NUMBER,
    FORBIDDEN_OPERATIONS,
    GENERATED_ARTIFACT_COUNT,
    IMPLEMENTATION_ALLOWED_AT_TASK_2,
    IMPLEMENTATION_ALLOWED_NEXT,
    IMPLEMENTATION_STARTED,
    LOCAL_ONLY,
    NEXT_STAGE,
    SCOPE_LOCK_ID,
    SCOPE_LOCK_REVISION,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    ALLOWED_INPUTS,
    build_objective_scope_lock_report,
    build_source_opening_snapshot,
    objective_candidates,
    task_2_signature,
    validate_objective_scope_lock_report,
    validate_source_opening_snapshot,
    write_task_2_artifacts,
)


def test_milestone_29_source_opening_snapshot_is_valid():
    snapshot = build_source_opening_snapshot()

    assert validate_source_opening_snapshot(snapshot)
    assert snapshot["source_task_id"] == SOURCE_TASK_ID
    assert snapshot["opening_status"] == "OPEN"
    assert snapshot["technical_status"] == "PASS"
    assert snapshot["process_status"] == "GOVERNED_OPENING_WITH_TASK_BUDGET_MAX_8"
    assert snapshot["source_dependency_valid"] is True
    assert snapshot["task_budget_max"] == 8
    assert snapshot["source_current_task_number"] == 1
    assert snapshot["implementation_started"] is False
    assert snapshot["implementation_allowed_at_task_1"] is False
    assert snapshot["objective_selection_required_next"] is True
    assert snapshot["scope_lock_required_next"] is True
    assert snapshot["source_next_stage"] == TASK_ID


def test_milestone_29_objective_candidates_have_single_selected_local_candidate():
    candidates = objective_candidates()
    selected = [candidate for candidate in candidates if candidate["selected"]]

    assert len(candidates) == 4
    assert len(selected) == 1
    assert selected[0]["objective_id"] == SELECTED_OBJECTIVE_ID
    assert selected[0]["local_only"] is True
    assert any(candidate["local_only"] is False for candidate in candidates)


def test_milestone_29_objective_scope_lock_report_is_valid():
    report = build_objective_scope_lock_report()

    assert validate_objective_scope_lock_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["scope_lock_revision"] == SCOPE_LOCK_REVISION
    assert report["task_2_signature"] == task_2_signature()
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["objective_selection_ready"] is True
    assert report["scope_locked"] is True
    assert report["implementation_started"] is IMPLEMENTATION_STARTED is False
    assert report["implementation_allowed_at_task_2"] is IMPLEMENTATION_ALLOWED_AT_TASK_2 is False
    assert report["implementation_allowed_next"] is IMPLEMENTATION_ALLOWED_NEXT is True
    assert report["scope_guard"]["local_only"] is LOCAL_ONLY is True
    assert report["scope_guard"]["network_access_allowed"] is False
    assert report["scope_guard"]["shell_execution_allowed"] is False
    assert report["scope_guard"]["repository_mutation_allowed"] is False
    assert report["scope_guard"]["remote_registry_lookup_allowed"] is False
    assert report["scope_guard"]["deep_recursive_dependency_traversal_allowed"] is False
    assert report["scope_guard"]["external_model_call_allowed"] is False
    assert len(report["scope_guard"]["allowed_inputs"]) == len(ALLOWED_INPUTS) == 6
    assert len(report["scope_guard"]["forbidden_operations"]) == len(FORBIDDEN_OPERATIONS) == 8
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_29_objective_scope_lock_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_2_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["task_2_signature"] == task_2_signature()
    assert artifacts["manifest"]["objective_selection_ready"] is True
    assert artifacts["manifest"]["scope_locked"] is True
    assert artifacts["manifest"]["implementation_started"] is False
    assert artifacts["manifest"]["implementation_allowed_at_task_2"] is False
    assert artifacts["manifest"]["implementation_allowed_next"] is True
    assert artifacts["manifest"]["local_only"] is True
    assert artifacts["manifest"]["generated_artifact_count"] == 5
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE

    candidates_path = Path(tmp_path) / "task-2-objective-candidates.json"
    report_path = Path(tmp_path) / "task-2-objective-scope-lock.json"
    markdown_path = Path(tmp_path) / "task-2-objective-scope-lock.md"
    manifest_path = Path(tmp_path) / "task-2-manifest.json"
    index_path = Path(tmp_path) / "task-2-index.txt"

    assert candidates_path.exists()
    assert report_path.exists()
    assert markdown_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_objective_scope_lock_report(report)
    assert "MILESTONE_29_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in index_path.read_text(encoding="utf-8")
