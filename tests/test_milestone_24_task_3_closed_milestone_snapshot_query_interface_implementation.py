"""Milestone #24 Task 3 query interface implementation validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_24_closed_milestone_snapshot_query_interface import (
    build_milestone_24_query_interface_implementation,
    get_closed_milestone_snapshot,
    list_closed_milestone_snapshots,
    summarize_closed_milestone_snapshot,
    validate_milestone_24_query_interface_implementation,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-24-task-3-closed-milestone-snapshot-query-interface-implementation-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_24_closed_milestone_snapshot_query_interface.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_24_closed_milestone_snapshot_query_interface.py"
MANIFEST = ROOT / "examples" / "milestone-24" / "closed-milestone-snapshot-query-interface-implementation-v1" / "task-3-manifest.json"
INDEX = ROOT / "examples" / "milestone-24" / "closed-milestone-snapshot-query-interface-implementation-v1" / "task-3-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-24" / "closed-milestone-snapshot-query-interface-implementation-v1" / "task-3-query-interface.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-24" / "closed-milestone-snapshot-query-interface-implementation-v1" / "task-3-query-interface.md"
QUERY_EXAMPLES = ROOT / "examples" / "milestone-24" / "closed-milestone-snapshot-query-interface-implementation-v1" / "task-3-query-examples.json"
SOURCE_DOC = ROOT / "docs" / "milestone-24-task-2-objective-selection-and-scope-lock-v1.md"


def test_task_3_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert QUERY_EXAMPLES.exists()
    assert SOURCE_DOC.exists()


def test_task_3_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")

    assert "MILESTONE_24_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in source
    assert "MILESTONE_24_TASK_2_SELECTED_OBJECTIVE_ID=CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY" in source
    assert "MILESTONE_24_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in source
    assert "MILESTONE_24_TASK_2_FAST_SOURCE_OPENING_SNAPSHOT=true" in source
    assert "MILESTONE_24_TASK_2_NEXT_STAGE=MILESTONE_24_TASK_3_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_IMPLEMENTATION_V1" in source


def test_task_3_query_interface_contract() -> None:
    implementation = build_milestone_24_query_interface_implementation()

    assert implementation.valid is True
    assert implementation.implementation_ok is True
    assert implementation.task_budget_max == 8
    assert implementation.current_task_number == 3
    assert len(implementation.allowed_query_operations) == 4
    assert len(implementation.forbidden_operations) == 5
    assert validate_milestone_24_query_interface_implementation(implementation) == ()


def test_task_3_query_operations() -> None:
    snapshots = list_closed_milestone_snapshots()
    m20 = get_closed_milestone_snapshot("MILESTONE_20")
    missing = get_closed_milestone_snapshot("MILESTONE_999")
    summary = summarize_closed_milestone_snapshot("MILESTONE_22")

    assert len(snapshots) == 3
    assert m20["found"] is True
    assert m20["snapshot"]["task7Used"] is True
    assert m20["snapshot"]["task8Used"] is False
    assert missing["found"] is False
    assert missing["valid"] is False
    assert summary["found"] is True
    assert "MILESTONE_22 closed" in summary["summary"]


def test_task_3_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_24_TASK_3_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_24_TASK_3_SOURCE_SCOPE_LOCK_ID=MILESTONE_24_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY" in text
    assert "MILESTONE_24_TASK_3_QUERY_INTERFACE_IMPLEMENTED=true" in text
    assert "MILESTONE_24_TASK_3_QUERY_INTERFACE_READ_ONLY=true" in text
    assert "MILESTONE_24_TASK_3_SNAPSHOT_COUNT=3" in text
    assert "MILESTONE_24_TASK_3_REGISTERED_MILESTONE_IDS=MILESTONE_20,MILESTONE_21,MILESTONE_22" in text
    assert "MILESTONE_24_TASK_3_M20_TASK_7_USED=true" in text
    assert "MILESTONE_24_TASK_3_M22_TASK_8_USED=false" in text
    assert "MILESTONE_24_TASK_3_MISSING_SNAPSHOT_FOUND=false" in text
    assert "MILESTONE_24_TASK_3_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in text
    assert "MILESTONE_24_TASK_3_NEXT_STAGE=MILESTONE_24_TASK_4_VALIDATION_AND_ARTIFACTS_V1" in text


def test_task_3_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_24_TASK_3_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_IMPLEMENTATION_V1"
    assert manifest["queryInterfaceImplemented"] is True
    assert manifest["queryInterfaceReadOnly"] is True
    assert manifest["snapshotCount"] == 3
    assert manifest["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert artifact["valid"] is True
    assert artifact["implementationOk"] is True
    assert artifact["snapshotCount"] == 3
    assert artifact["missingSnapshotFound"] is False
    assert artifact["issues"] == []
