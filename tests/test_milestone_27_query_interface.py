from pathlib import Path
import json

from hbce_arc_agi3.milestone_27_query_interface import (
    DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
    NETWORK_ACCESS_ALLOWED,
    QUERY_INTERFACE_REVISION,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    TASK_ID,
    build_closed_milestone_archive_index,
    detect_forbidden_operations,
    query_closed_milestone_archive_index,
    render_query_result_markdown,
    task_3_signature,
    validate_query_result,
    write_task_3_artifacts,
)


def test_closed_milestone_archive_index_contains_milestone_26_record():
    records = build_closed_milestone_archive_index()
    milestone_26 = [record for record in records if record.milestone_id == "MILESTONE_26"]

    assert len(milestone_26) == 1
    assert milestone_26[0].archive_status == "CLOSED"
    assert milestone_26[0].technical_status == "PASS"
    assert milestone_26[0].process_status == "GOVERNED_WITHIN_TASK_BUDGET"
    assert milestone_26[0].final_task_number == 6
    assert milestone_26[0].task_budget_max == 8


def test_query_interface_returns_local_only_milestone_26_result():
    result = query_closed_milestone_archive_index({"milestone_id": "MILESTONE_26"})

    assert validate_query_result(result)
    assert result["task_id"] == TASK_ID
    assert result["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert result["scope_lock_id"] == SCOPE_LOCK_ID
    assert result["query_interface_revision"] == QUERY_INTERFACE_REVISION
    assert result["local_only"] is True
    assert result["network_access_allowed"] is False
    assert result["deep_recursive_dependency_traversal_allowed"] is False
    assert result["query_status"] == "READY"
    assert result["matched_count"] == 1
    assert result["records"][0]["milestone_id"] == "MILESTONE_26"
    assert result["records"][0]["closure_marker"] == "MILESTONE_26_CLOSURE_SOURCE_ARTIFACT_VALID"


def test_query_interface_can_suppress_evidence_without_changing_scope():
    result = query_closed_milestone_archive_index(
        {
            "milestone_id": "MILESTONE_26",
            "include_evidence": False,
            "local_only": True,
        }
    )

    assert validate_query_result(result)
    assert result["query_status"] == "READY"
    assert result["matched_count"] == 1
    assert result["records"][0]["evidence_bundle"] == []
    assert result["scope_lock_enforced"] is True


def test_query_interface_blocks_non_local_and_forbidden_operations():
    result = query_closed_milestone_archive_index(
        {
            "milestone_id": "MILESTONE_26",
            "local_only": False,
            "forbidden_operations": ("network_access", "deep_recursive_dependency_traversal"),
        }
    )

    assert validate_query_result(result)
    assert result["query_status"] == "BLOCKED_BY_SCOPE_LOCK"
    assert result["blocked"] is True
    assert result["matched_count"] == 0
    assert "NON_LOCAL_QUERY_REQUESTED" in result["forbidden_operations_detected"]
    assert "NETWORK_ACCESS" in result["forbidden_operations_detected"]
    assert "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL" in result["forbidden_operations_detected"]
    assert detect_forbidden_operations({"local_only": False}) == ("NON_LOCAL_QUERY_REQUESTED",)


def test_query_interface_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_3_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["query_interface_revision"] == QUERY_INTERFACE_REVISION
    assert artifacts["manifest"]["task_3_signature"] == task_3_signature()
    assert artifacts["manifest"]["network_access_allowed"] == NETWORK_ACCESS_ALLOWED
    assert artifacts["manifest"]["deep_recursive_dependency_traversal_allowed"] == DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED
    assert artifacts["manifest"]["generated_artifact_count"] == 5

    result_path = Path(tmp_path) / "task-3-query-interface-result.json"
    blocked_path = Path(tmp_path) / "task-3-query-interface-blocked-result.json"
    manifest_path = Path(tmp_path) / "task-3-manifest.json"
    markdown_path = Path(tmp_path) / "task-3-query-interface-result.md"
    index_path = Path(tmp_path) / "task-3-index.txt"

    assert result_path.exists()
    assert blocked_path.exists()
    assert manifest_path.exists()
    assert markdown_path.exists()
    assert index_path.exists()

    result = json.loads(result_path.read_text(encoding="utf-8"))
    blocked = json.loads(blocked_path.read_text(encoding="utf-8"))
    assert result["query_status"] == "READY"
    assert blocked["query_status"] == "BLOCKED_BY_SCOPE_LOCK"
    assert "MILESTONE_26" in render_query_result_markdown(result)
