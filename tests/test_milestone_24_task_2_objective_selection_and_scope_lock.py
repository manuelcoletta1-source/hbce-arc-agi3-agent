"""Milestone #24 Task 2 objective selection and scope lock validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_24_objective_scope_lock import (
    build_milestone_24_objective_scope_lock,
    validate_milestone_24_objective_scope_lock,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-24-task-2-objective-selection-and-scope-lock-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_24_objective_scope_lock.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_24_objective_scope_lock.py"
MANIFEST = ROOT / "examples" / "milestone-24" / "objective-selection-and-scope-lock-v1" / "task-2-manifest.json"
INDEX = ROOT / "examples" / "milestone-24" / "objective-selection-and-scope-lock-v1" / "task-2-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-24" / "objective-selection-and-scope-lock-v1" / "task-2-objective-scope-lock.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-24" / "objective-selection-and-scope-lock-v1" / "task-2-objective-scope-lock.md"
SOURCE_DOC = ROOT / "docs" / "milestone-24-task-1-governed-opening-with-task-budget-v1.md"


def test_task_2_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert SOURCE_DOC.exists()


def test_task_2_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")

    assert "MILESTONE_24_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in source
    assert "MILESTONE_24_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT=true" in source
    assert "MILESTONE_24_TASK_1_SCOPE_LOCK_REQUIRED_NEXT=true" in source
    assert "MILESTONE_24_TASK_1_IMPLEMENTATION_STARTED=false" in source
    assert "MILESTONE_24_TASK_1_NEXT_STAGE=MILESTONE_24_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1" in source


def test_task_2_scope_lock_contract() -> None:
    scope_lock = build_milestone_24_objective_scope_lock()

    assert scope_lock.valid is True
    assert scope_lock.lock_ok is True
    assert scope_lock.scope_lock_id == "MILESTONE_24_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY"
    assert scope_lock.selected_objective_id == "CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY"
    assert scope_lock.task_budget_max == 8
    assert scope_lock.current_task_number == 2
    assert len(scope_lock.allowed_query_operations) == 4
    assert len(scope_lock.forbidden_operations) == 5
    assert validate_milestone_24_objective_scope_lock(scope_lock) == ()


def test_task_2_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_24_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert "MILESTONE_24_TASK_2_SCOPE_LOCK_ID=MILESTONE_24_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY" in text
    assert "MILESTONE_24_TASK_2_SELECTED_OBJECTIVE_ID=CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY" in text
    assert "MILESTONE_24_TASK_2_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_24_TASK_2_CURRENT_TASK_NUMBER=2" in text
    assert "MILESTONE_24_TASK_2_OBJECTIVE_SELECTED=true" in text
    assert "MILESTONE_24_TASK_2_SCOPE_LOCKED=true" in text
    assert "MILESTONE_24_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in text
    assert "MILESTONE_24_TASK_2_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_24_TASK_2_QUERY_INTERFACE_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_24_TASK_2_FAST_SOURCE_OPENING_SNAPSHOT=true" in text
    assert "MILESTONE_24_TASK_2_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_FORBIDDEN=true" in text
    assert "MILESTONE_24_TASK_2_NEXT_STAGE=MILESTONE_24_TASK_3_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_IMPLEMENTATION_V1" in text


def test_task_2_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_24_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert manifest["scopeLockId"] == "MILESTONE_24_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY"
    assert manifest["selectedObjectiveId"] == "CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY"
    assert manifest["objectiveSelected"] is True
    assert manifest["scopeLocked"] is True
    assert manifest["implementationAllowedNext"] is True
    assert manifest["implementationStarted"] is False
    assert manifest["queryInterfaceImplementationStarted"] is False
    assert manifest["fastSourceOpeningSnapshot"] is True
    assert artifact["valid"] is True
    assert artifact["lockOk"] is True
    assert artifact["scopeLockId"] == "MILESTONE_24_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY"
    assert artifact["selectedObjectiveId"] == "CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY"
    assert artifact["fastSourceOpeningSnapshot"] is True
    assert artifact["issues"] == []
