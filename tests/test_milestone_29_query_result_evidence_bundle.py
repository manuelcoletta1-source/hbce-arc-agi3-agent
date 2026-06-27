from pathlib import Path
import json

from hbce_arc_agi3.milestone_29_query_result_evidence_bundle import (
    CURRENT_TASK_NUMBER,
    EVIDENCE_BUNDLE_REVISION,
    EVIDENCE_ITEM_COUNT,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    build_query_result_evidence_bundle,
    build_scope_lock_snapshot,
    build_evidence_items,
    task_3_signature,
    validate_evidence_items,
    validate_query_result_evidence_bundle,
    validate_scope_lock_snapshot,
    write_task_3_artifacts,
)


def test_milestone_29_evidence_bundle_scope_lock_snapshot_is_valid():
    snapshot = build_scope_lock_snapshot()

    assert validate_scope_lock_snapshot(snapshot)
    assert snapshot["source_task_id"] == SOURCE_TASK_ID
    assert snapshot["source_next_stage"] == TASK_ID
    assert snapshot["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert snapshot["scope_lock_id"] == SCOPE_LOCK_ID
    assert snapshot["objective_selection_ready"] is True
    assert snapshot["scope_locked"] is True
    assert snapshot["implementation_allowed_next"] is True
    assert snapshot["local_only"] is True
    assert snapshot["network_access_allowed"] is False
    assert snapshot["shell_execution_allowed"] is False


def test_milestone_29_evidence_items_are_local_and_hash_verified():
    items = build_evidence_items()

    assert len(items) == EVIDENCE_ITEM_COUNT
    assert validate_evidence_items(items)
    assert all(Path(item["path"]).exists() for item in items)
    assert all(item["local_only"] is True for item in items)
    assert all(len(item["sha256"]) == 64 for item in items)


def test_milestone_29_query_result_evidence_bundle_is_valid():
    bundle = build_query_result_evidence_bundle()

    assert validate_query_result_evidence_bundle(bundle)
    assert bundle["task_id"] == TASK_ID
    assert bundle["source_task_id"] == SOURCE_TASK_ID
    assert bundle["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert bundle["scope_lock_id"] == SCOPE_LOCK_ID
    assert bundle["evidence_bundle_revision"] == EVIDENCE_BUNDLE_REVISION
    assert bundle["task_3_signature"] == task_3_signature()
    assert bundle["implementation_status"] == "READY"
    assert bundle["implementation_started"] is True
    assert bundle["implementation_complete"] is True
    assert bundle["scope_lock_valid"] is True
    assert bundle["source_chain_valid"] is True
    assert bundle["evidence_valid"] is True
    assert bundle["evidence_item_count"] == EVIDENCE_ITEM_COUNT
    assert bundle["local_only"] is True
    assert bundle["network_access_allowed"] is False
    assert bundle["shell_execution_allowed"] is False
    assert bundle["repository_mutation_allowed"] is False
    assert bundle["remote_registry_lookup_allowed"] is False
    assert bundle["deep_recursive_dependency_traversal_allowed"] is False
    assert bundle["external_model_call_allowed"] is False
    assert bundle["task_budget_max"] == TASK_BUDGET_MAX
    assert bundle["current_task_number"] == CURRENT_TASK_NUMBER
    assert bundle["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert bundle["next_stage"] == NEXT_STAGE


def test_milestone_29_query_result_evidence_bundle_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_3_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["task_3_signature"] == task_3_signature()
    assert artifacts["manifest"]["implementation_status"] == "READY"
    assert artifacts["manifest"]["implementation_started"] is True
    assert artifacts["manifest"]["implementation_complete"] is True
    assert artifacts["manifest"]["scope_lock_valid"] is True
    assert artifacts["manifest"]["source_chain_valid"] is True
    assert artifacts["manifest"]["evidence_valid"] is True
    assert artifacts["manifest"]["evidence_item_count"] == EVIDENCE_ITEM_COUNT
    assert artifacts["manifest"]["generated_artifact_count"] == 5
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE

    bundle_path = Path(tmp_path) / "task-3-evidence-bundle.json"
    markdown_path = Path(tmp_path) / "task-3-evidence-bundle.md"
    evidence_index_path = Path(tmp_path) / "task-3-evidence-index.json"
    manifest_path = Path(tmp_path) / "task-3-manifest.json"
    index_path = Path(tmp_path) / "task-3-index.txt"

    assert bundle_path.exists()
    assert markdown_path.exists()
    assert evidence_index_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
    assert validate_query_result_evidence_bundle(bundle)
    assert "MILESTONE_29_TASK_3_QUERY_RESULT_EVIDENCE_BUNDLE_IMPLEMENTATION_READY=true" in index_path.read_text(encoding="utf-8")
