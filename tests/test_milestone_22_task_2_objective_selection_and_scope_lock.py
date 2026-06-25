"""Milestone #22 Task 2 objective selection and scope lock validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_22_objective_scope_lock import (
    build_milestone_22_objective_scope_lock,
    validate_milestone_22_objective_scope_lock,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-22-task-2-objective-selection-and-scope-lock-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_22_objective_scope_lock.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_22_objective_scope_lock.py"
MANIFEST = ROOT / "examples" / "milestone-22" / "objective-selection-and-scope-lock-v1" / "task-2-manifest.json"
INDEX = ROOT / "examples" / "milestone-22" / "objective-selection-and-scope-lock-v1" / "task-2-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-22" / "objective-selection-and-scope-lock-v1" / "task-2-objective-scope-lock.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-22" / "objective-selection-and-scope-lock-v1" / "task-2-objective-scope-lock.md"
TASK_1_DOC = ROOT / "docs" / "milestone-22-task-1-governed-opening-with-task-budget-v1.md"


def test_task_2_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert TASK_1_DOC.exists()


def test_task_2_dependency_is_present() -> None:
    task1 = TASK_1_DOC.read_text(encoding="utf-8")

    assert "MILESTONE_22_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in task1
    assert "MILESTONE_22_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT=true" in task1
    assert "MILESTONE_22_TASK_1_SCOPE_LOCK_REQUIRED_NEXT=true" in task1
    assert "MILESTONE_22_TASK_1_IMPLEMENTATION_STARTED=false" in task1
    assert "MILESTONE_22_TASK_1_NEXT_STAGE=MILESTONE_22_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1" in task1


def test_task_2_scope_lock_contract() -> None:
    scope = build_milestone_22_objective_scope_lock()

    assert scope.valid is True
    assert scope.scope_lock_ok is True
    assert scope.scope_lock_id == "MILESTONE_22_SCOPE_FAST_SNAPSHOT_DEPENDENCY_GUARD_LOCAL_ONLY"
    assert scope.task_budget_max == 8
    assert scope.current_task_number == 2
    assert scope.recommended_closure_task_number == 6
    assert len(scope.allowed_implementation_targets) == 4
    assert len(scope.forbidden_targets) == 10
    assert len(scope.scope_checks) == 10
    assert validate_milestone_22_objective_scope_lock(scope) == ()


def test_task_2_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_22_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert "MILESTONE_22_TASK_2_SCOPE_LOCK_ID=MILESTONE_22_SCOPE_FAST_SNAPSHOT_DEPENDENCY_GUARD_LOCAL_ONLY" in text
    assert "MILESTONE_22_TASK_2_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_22_TASK_2_CURRENT_TASK_NUMBER=2" in text
    assert "MILESTONE_22_TASK_2_OBJECTIVE_SELECTION_READY=true" in text
    assert "MILESTONE_22_TASK_2_SCOPE_LOCKED=true" in text
    assert "MILESTONE_22_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in text
    assert "MILESTONE_22_TASK_2_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_22_TASK_2_FAST_SNAPSHOT_PATTERN_REQUIRED=true" in text
    assert "MILESTONE_22_TASK_2_DEEP_RECURSIVE_SERIALIZATION_FORBIDDEN=true" in text
    assert "MILESTONE_22_TASK_2_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_22_TASK_2_NEXT_STAGE=MILESTONE_22_TASK_3_FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTATION_V1" in text


def test_task_2_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_22_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert manifest["scopeLockId"] == "MILESTONE_22_SCOPE_FAST_SNAPSHOT_DEPENDENCY_GUARD_LOCAL_ONLY"
    assert manifest["taskBudgetMax"] == 8
    assert manifest["currentTaskNumber"] == 2
    assert manifest["scopeLocked"] is True
    assert manifest["implementationAllowedNext"] is True
    assert manifest["implementationStarted"] is False
    assert manifest["fastSnapshotPatternRequired"] is True
    assert manifest["deepRecursiveSerializationForbidden"] is True
    assert artifact["valid"] is True
    assert artifact["scopeLockOk"] is True
    assert artifact["issues"] == []
