"""Milestone #23 Task 2 objective selection and scope lock validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_23_objective_scope_lock import (
    build_milestone_23_objective_scope_lock,
    validate_milestone_23_objective_scope_lock,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-23-task-2-objective-selection-and-scope-lock-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_23_objective_scope_lock.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_23_objective_scope_lock.py"
MANIFEST = ROOT / "examples" / "milestone-23" / "objective-selection-and-scope-lock-v1" / "task-2-manifest.json"
INDEX = ROOT / "examples" / "milestone-23" / "objective-selection-and-scope-lock-v1" / "task-2-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-23" / "objective-selection-and-scope-lock-v1" / "task-2-objective-scope-lock.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-23" / "objective-selection-and-scope-lock-v1" / "task-2-objective-scope-lock.md"
TASK_1_DOC = ROOT / "docs" / "milestone-23-task-1-governed-opening-with-task-budget-v1.md"


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

    assert "MILESTONE_23_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in task1
    assert "MILESTONE_23_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT=true" in task1
    assert "MILESTONE_23_TASK_1_SCOPE_LOCK_REQUIRED_NEXT=true" in task1
    assert "MILESTONE_23_TASK_1_IMPLEMENTATION_STARTED=false" in task1
    assert "MILESTONE_23_TASK_1_NEXT_STAGE=MILESTONE_23_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1" in task1


def test_task_2_scope_lock_contract() -> None:
    lock = build_milestone_23_objective_scope_lock()

    assert lock.valid is True
    assert lock.lock_ok is True
    assert lock.scope_lock_id == "MILESTONE_23_SCOPE_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY"
    assert lock.selected_objective_id == "CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY"
    assert lock.task_budget_max == 8
    assert lock.current_task_number == 2
    assert lock.recommended_closure_task_number == 6
    assert len(lock.objective_candidates) == 3
    assert lock.rejected_objective_count == 2
    assert len(lock.scope_constraints) == 12
    assert validate_milestone_23_objective_scope_lock(lock) == ()


def test_task_2_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_23_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert "MILESTONE_23_TASK_2_SCOPE_LOCK_ID=MILESTONE_23_SCOPE_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY" in text
    assert "MILESTONE_23_TASK_2_SELECTED_OBJECTIVE_ID=CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY" in text
    assert "MILESTONE_23_TASK_2_TASK_BUDGET_MIN=4" in text
    assert "MILESTONE_23_TASK_2_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_23_TASK_2_CURRENT_TASK_NUMBER=2" in text
    assert "MILESTONE_23_TASK_2_OBJECTIVE_SELECTED=true" in text
    assert "MILESTONE_23_TASK_2_SCOPE_LOCKED=true" in text
    assert "MILESTONE_23_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in text
    assert "MILESTONE_23_TASK_2_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_23_TASK_2_REGISTRY_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_23_TASK_2_FAST_SNAPSHOT_DEPENDENCY_MODE_REQUIRED=true" in text
    assert "MILESTONE_23_TASK_2_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_FORBIDDEN=true" in text
    assert "MILESTONE_23_TASK_2_NEXT_STAGE=MILESTONE_23_TASK_3_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_IMPLEMENTATION_V1" in text


def test_task_2_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_23_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert manifest["scopeLockId"] == "MILESTONE_23_SCOPE_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY"
    assert manifest["selectedObjectiveId"] == "CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY"
    assert manifest["taskBudgetMin"] == 4
    assert manifest["taskBudgetMax"] == 8
    assert manifest["currentTaskNumber"] == 2
    assert manifest["objectiveSelected"] is True
    assert manifest["scopeLocked"] is True
    assert manifest["implementationAllowedNext"] is True
    assert manifest["implementationStarted"] is False
    assert artifact["valid"] is True
    assert artifact["lockOk"] is True
    assert artifact["issues"] == []
