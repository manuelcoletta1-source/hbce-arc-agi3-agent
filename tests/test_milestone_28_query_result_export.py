from pathlib import Path
import json

from hbce_arc_agi3.milestone_28_query_result_export import (
    CURRENT_TASK_NUMBER,
    EXPORT_REVISION,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    build_export_payload,
    build_scope_lock_snapshot,
    task_3_signature,
    validate_export_payload,
    validate_scope_lock_snapshot,
    write_task_3_artifacts,
)


def test_query_result_export_scope_lock_snapshot_is_valid_and_stable():
    snapshot = build_scope_lock_snapshot()

    assert validate_scope_lock_snapshot(snapshot)
    assert snapshot["source_task_id"] == SOURCE_TASK_ID
    assert snapshot["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert snapshot["scope_lock_id"] == SCOPE_LOCK_ID
    assert snapshot["runtime_valid"] is True
    assert snapshot["persisted_valid"] is True
    assert snapshot["stable_scope_lock"] is True


def test_query_result_export_payload_is_ready_and_local_only():
    payload = build_export_payload()

    assert validate_export_payload(payload)
    assert payload["task_id"] == TASK_ID
    assert payload["source_task_id"] == SOURCE_TASK_ID
    assert payload["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert payload["scope_lock_id"] == SCOPE_LOCK_ID
    assert payload["export_revision"] == EXPORT_REVISION
    assert payload["task_3_signature"] == task_3_signature()
    assert payload["export_status"] == "READY"
    assert payload["exported_record_count"] >= 1
    assert payload["local_only"] is True
    assert payload["implementation_complete"] is True
    assert payload["network_access_allowed"] is False
    assert payload["deep_recursive_dependency_traversal_allowed"] is False
    assert payload["task_budget_max"] == TASK_BUDGET_MAX
    assert payload["current_task_number"] == CURRENT_TASK_NUMBER
    assert payload["next_stage"] == NEXT_STAGE


def test_query_result_export_payload_preserves_milestone_26_closed_record():
    payload = build_export_payload()
    records = payload["exported_records"]

    assert records
    assert records[0]["milestone_id"] == "MILESTONE_26"
    assert records[0]["archive_status"] == "CLOSED"
    assert records[0]["technical_status"] == "PASS"
    assert records[0]["final_task_number"] == 6
    assert payload["source_primary_query_id"].startswith("MILESTONE-27-QUERY-")


def test_query_result_export_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_3_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["export_revision"] == EXPORT_REVISION
    assert artifacts["manifest"]["task_3_signature"] == task_3_signature()
    assert artifacts["manifest"]["export_status"] == "READY"
    assert artifacts["manifest"]["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT

    export_path = Path(tmp_path) / "task-3-query-result-export.json"
    markdown_path = Path(tmp_path) / "task-3-query-result-export.md"
    export_index_path = Path(tmp_path) / "task-3-export-index.json"
    manifest_path = Path(tmp_path) / "task-3-manifest.json"
    index_path = Path(tmp_path) / "task-3-index.txt"

    assert export_path.exists()
    assert markdown_path.exists()
    assert export_index_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    payload = json.loads(export_path.read_text(encoding="utf-8"))
    assert validate_export_payload(payload)
    assert "MILESTONE_28_TASK_3_QUERY_RESULT_EXPORT_IMPLEMENTATION_READY=true" in index_path.read_text(encoding="utf-8")
