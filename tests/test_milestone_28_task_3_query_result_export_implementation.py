import json
from pathlib import Path

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
    task_3_signature,
    validate_export_payload,
)


DOC_PATH = Path("docs/milestone-28-task-3-query-result-export-implementation-v1.md")
SOURCE_TASK_2_DOC_PATH = Path("docs/milestone-28-task-2-objective-selection-and-scope-lock-v1.md")
ARTIFACT_DIR = Path("examples/milestone-28/query-result-export-implementation-v1")


def test_task_3_doc_declares_query_result_export_implementation_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_28_TASK_3_QUERY_RESULT_EXPORT_IMPLEMENTATION_READY=true" in text
    assert f"MILESTONE_28_TASK_3_SOURCE_TASK_ID={SOURCE_TASK_ID}" in text
    assert f"MILESTONE_28_TASK_3_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_28_TASK_3_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_28_TASK_3_EXPORT_REVISION={EXPORT_REVISION}" in text
    assert "MILESTONE_28_TASK_3_IMPLEMENTATION_STARTED=true" in text
    assert "MILESTONE_28_TASK_3_IMPLEMENTATION_COMPLETE=true" in text
    assert "MILESTONE_28_TASK_3_LOCAL_ONLY=true" in text
    assert "MILESTONE_28_TASK_3_NETWORK_ACCESS_ALLOWED=false" in text
    assert "MILESTONE_28_TASK_3_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in text
    assert f"MILESTONE_28_TASK_3_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_28_TASK_3_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_28_TASK_3_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert f"MILESTONE_28_TASK_3_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_3_dependency_keeps_task_2_scope_lock_intact():
    text = SOURCE_TASK_2_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_28_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert f"MILESTONE_28_TASK_2_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_28_TASK_2_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert "MILESTONE_28_TASK_2_SCOPE_LOCKED=true" in text
    assert "MILESTONE_28_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in text
    assert "MILESTONE_28_TASK_2_LOCAL_ONLY=true" in text
    assert "MILESTONE_28_TASK_2_NEXT_STAGE=MILESTONE_28_TASK_3_QUERY_RESULT_EXPORT_IMPLEMENTATION_V1" in text


def test_task_3_persisted_export_payload_is_valid():
    payload = json.loads((ARTIFACT_DIR / "task-3-query-result-export.json").read_text(encoding="utf-8"))

    assert validate_export_payload(payload)
    assert payload["task_id"] == TASK_ID
    assert payload["source_task_id"] == SOURCE_TASK_ID
    assert payload["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert payload["scope_lock_id"] == SCOPE_LOCK_ID
    assert payload["export_revision"] == EXPORT_REVISION
    assert payload["task_3_signature"] == task_3_signature()
    assert payload["export_status"] == "READY"
    assert payload["exported_record_count"] >= 1
    assert payload["next_stage"] == NEXT_STAGE


def test_task_3_persisted_manifest_and_export_index_match_payload():
    payload = json.loads((ARTIFACT_DIR / "task-3-query-result-export.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-3-manifest.json").read_text(encoding="utf-8"))
    export_index = json.loads((ARTIFACT_DIR / "task-3-export-index.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["export_id"] == payload["export_id"]
    assert manifest["export_signature"] == payload["export_signature"]
    assert manifest["export_status"] == "READY"
    assert manifest["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert export_index["task_id"] == TASK_ID
    assert export_index["export_id"] == payload["export_id"]
    assert export_index["export_signature"] == payload["export_signature"]
    assert export_index["exported_record_count"] == payload["exported_record_count"]
    assert len(export_index["exported_records"]) == payload["exported_record_count"]


def test_task_3_index_contains_canonical_export_markers():
    index = (ARTIFACT_DIR / "task-3-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_28_TASK_3_QUERY_RESULT_EXPORT_IMPLEMENTATION_READY=true" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert "EXPORT_STATUS=READY" in index
    assert "IMPLEMENTATION_STARTED=true" in index
    assert "IMPLEMENTATION_COMPLETE=true" in index
    assert "LOCAL_ONLY=true" in index
    assert "NETWORK_ACCESS_ALLOWED=false" in index
    assert "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in index
    assert f"GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
