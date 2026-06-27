import json
from pathlib import Path

from hbce_arc_agi3.milestone_27_query_interface import (
    NEXT_STAGE,
    QUERY_INTERFACE_REVISION,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    TASK_ID,
    query_closed_milestone_archive_index,
    task_3_signature,
    validate_query_result,
)


DOC_PATH = Path("docs/milestone-27-task-3-query-interface-implementation-v1.md")
TASK_2_DOC_PATH = Path("docs/milestone-27-task-2-objective-selection-and-scope-lock-v1.md")
ARTIFACT_DIR = Path("examples/milestone-27/query-interface-implementation-v1")


def test_task_3_doc_declares_query_interface_ready_and_local_only():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_27_TASK_3_QUERY_INTERFACE_IMPLEMENTATION_READY=true" in text
    assert f"MILESTONE_27_TASK_3_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_27_TASK_3_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert "MILESTONE_27_TASK_3_IMPLEMENTATION_STARTED=true" in text
    assert "MILESTONE_27_TASK_3_QUERY_INTERFACE_IMPLEMENTED=true" in text
    assert "MILESTONE_27_TASK_3_LOCAL_ONLY=true" in text
    assert "MILESTONE_27_TASK_3_NETWORK_ACCESS_ALLOWED=false" in text
    assert "MILESTONE_27_TASK_3_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in text
    assert "MILESTONE_27_TASK_3_GENERATED_ARTIFACT_COUNT=5" in text
    assert f"MILESTONE_27_TASK_3_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_3_dependency_keeps_task_2_scope_lock_intact():
    text = TASK_2_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_27_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert "MILESTONE_27_TASK_2_SELECTED_OBJECTIVE_ID=CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_INTERFACE_LOCAL_ONLY" in text
    assert "MILESTONE_27_TASK_2_SCOPE_LOCKED=true" in text
    assert "MILESTONE_27_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in text
    assert "MILESTONE_27_TASK_2_NEXT_STAGE=MILESTONE_27_TASK_3_QUERY_INTERFACE_IMPLEMENTATION_V1" in text


def test_task_3_generated_manifest_matches_module_contract():
    manifest = json.loads((ARTIFACT_DIR / "task-3-manifest.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert manifest["scope_lock_id"] == SCOPE_LOCK_ID
    assert manifest["query_interface_revision"] == QUERY_INTERFACE_REVISION
    assert manifest["task_3_signature"] == task_3_signature()
    assert manifest["local_only"] is True
    assert manifest["implementation_started"] is True
    assert manifest["query_interface_implemented"] is True
    assert manifest["network_access_allowed"] is False
    assert manifest["deep_recursive_dependency_traversal_allowed"] is False
    assert manifest["generated_artifact_count"] == 5
    assert manifest["next_stage"] == NEXT_STAGE


def test_task_3_primary_and_blocked_query_artifacts_are_valid():
    primary = json.loads((ARTIFACT_DIR / "task-3-query-interface-result.json").read_text(encoding="utf-8"))
    blocked = json.loads((ARTIFACT_DIR / "task-3-query-interface-blocked-result.json").read_text(encoding="utf-8"))

    assert validate_query_result(primary)
    assert validate_query_result(blocked)
    assert primary["query_status"] == "READY"
    assert primary["matched_count"] == 1
    assert primary["records"][0]["milestone_id"] == "MILESTONE_26"
    assert primary["records"][0]["technical_status"] == "PASS"
    assert blocked["query_status"] == "BLOCKED_BY_SCOPE_LOCK"
    assert blocked["blocked"] is True
    assert blocked["records"] == []


def test_task_3_runtime_query_matches_persisted_artifact_signature():
    runtime = query_closed_milestone_archive_index({"milestone_id": "MILESTONE_26", "local_only": True})
    primary = json.loads((ARTIFACT_DIR / "task-3-query-interface-result.json").read_text(encoding="utf-8"))

    assert runtime["query_id"] == primary["query_id"]
    assert runtime["result_signature"] == primary["result_signature"]
    assert runtime["task_3_signature"] == primary["task_3_signature"]
