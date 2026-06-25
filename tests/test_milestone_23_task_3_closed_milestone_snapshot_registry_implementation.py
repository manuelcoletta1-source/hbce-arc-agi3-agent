"""Milestone #23 Task 3 closed milestone snapshot registry validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_23_closed_milestone_snapshot_registry import (
    build_milestone_23_closed_milestone_snapshot_registry_implementation,
    validate_milestone_23_closed_milestone_snapshot_registry_implementation,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-23-task-3-closed-milestone-snapshot-registry-implementation-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_23_closed_milestone_snapshot_registry.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_23_closed_milestone_snapshot_registry.py"
MANIFEST = ROOT / "examples" / "milestone-23" / "closed-milestone-snapshot-registry-implementation-v1" / "task-3-manifest.json"
INDEX = ROOT / "examples" / "milestone-23" / "closed-milestone-snapshot-registry-implementation-v1" / "task-3-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-23" / "closed-milestone-snapshot-registry-implementation-v1" / "task-3-closed-milestone-snapshot-registry.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-23" / "closed-milestone-snapshot-registry-implementation-v1" / "task-3-closed-milestone-snapshot-registry.md"
TASK_2_DOC = ROOT / "docs" / "milestone-23-task-2-objective-selection-and-scope-lock-v1.md"


def test_task_3_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert TASK_2_DOC.exists()


def test_task_3_dependency_is_present() -> None:
    task2 = TASK_2_DOC.read_text(encoding="utf-8")

    assert "MILESTONE_23_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in task2
    assert "MILESTONE_23_TASK_2_SCOPE_LOCKED=true" in task2
    assert "MILESTONE_23_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in task2
    assert "MILESTONE_23_TASK_2_REGISTRY_IMPLEMENTATION_STARTED=false" in task2
    assert "MILESTONE_23_TASK_2_NEXT_STAGE=MILESTONE_23_TASK_3_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_IMPLEMENTATION_V1" in task2


def test_task_3_registry_implementation_contract() -> None:
    implementation = build_milestone_23_closed_milestone_snapshot_registry_implementation()

    assert implementation.valid is True
    assert implementation.implementation_ok is True
    assert implementation.task_budget_max == 8
    assert implementation.current_task_number == 3
    assert implementation.registry.valid is True
    assert implementation.registry.snapshot_count == 3
    assert implementation.registry.contains("MILESTONE_22") is True
    assert validate_milestone_23_closed_milestone_snapshot_registry_implementation(implementation) == ()


def test_task_3_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_23_TASK_3_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_23_TASK_3_SCOPE_LOCK_ID=MILESTONE_23_SCOPE_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY" in text
    assert "MILESTONE_23_TASK_3_SELECTED_OBJECTIVE_ID=CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY" in text
    assert "MILESTONE_23_TASK_3_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_23_TASK_3_CURRENT_TASK_NUMBER=3" in text
    assert "MILESTONE_23_TASK_3_REGISTRY_IMPLEMENTED=true" in text
    assert "MILESTONE_23_TASK_3_REGISTRY_LOOKUP_READY=true" in text
    assert "MILESTONE_23_TASK_3_REGISTRY_SNAPSHOT_COUNT=3" in text
    assert "MILESTONE_23_TASK_3_REGISTERED_MILESTONE_IDS=MILESTONE_20,MILESTONE_21,MILESTONE_22" in text
    assert "MILESTONE_23_TASK_3_READY_FOR_VALIDATION_ARTIFACTS=true" in text
    assert "MILESTONE_23_TASK_3_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in text
    assert "MILESTONE_23_TASK_3_NEXT_STAGE=MILESTONE_23_TASK_4_VALIDATION_AND_ARTIFACTS_V1" in text


def test_task_3_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_23_TASK_3_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_IMPLEMENTATION_V1"
    assert manifest["registryImplemented"] is True
    assert manifest["registryLookupReady"] is True
    assert manifest["registrySnapshotCount"] == 3
    assert manifest["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert manifest["readyForValidationArtifacts"] is True
    assert manifest["deepRecursiveDependencyTraversalAllowed"] is False
    assert artifact["valid"] is True
    assert artifact["implementationOk"] is True
    assert artifact["registryValid"] is True
    assert artifact["registrySnapshotCount"] == 3
    assert artifact["issues"] == []
