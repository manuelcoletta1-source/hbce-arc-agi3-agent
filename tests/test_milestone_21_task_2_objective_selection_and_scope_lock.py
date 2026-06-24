"""Milestone #21 Task 2 objective selection and scope lock validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_21_objective_scope_lock import (
    build_milestone_21_objective_scope_lock,
    validate_milestone_21_objective_scope_lock,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-21-task-2-objective-selection-and-scope-lock-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_21_objective_scope_lock.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_21_objective_scope_lock.py"
MANIFEST = ROOT / "examples" / "milestone-21" / "objective-selection-and-scope-lock-v1" / "task-2-manifest.json"
INDEX = ROOT / "examples" / "milestone-21" / "objective-selection-and-scope-lock-v1" / "task-2-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-21" / "objective-selection-and-scope-lock-v1" / "task-2-objective-scope-lock.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-21" / "objective-selection-and-scope-lock-v1" / "task-2-objective-scope-lock.md"
TASK_1_DOC = ROOT / "docs" / "milestone-21-task-1-governed-opening-with-task-budget-v1.md"
M20_CLOSURE = ROOT / "docs" / "milestone-20-task-7-milestone-closure-v1.md"


def test_task_2_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert TASK_1_DOC.exists()
    assert M20_CLOSURE.exists()


def test_task_2_dependencies_are_present() -> None:
    task1 = TASK_1_DOC.read_text(encoding="utf-8")
    milestone20 = M20_CLOSURE.read_text(encoding="utf-8")

    assert "MILESTONE_21_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in task1
    assert "MILESTONE_21_TASK_1_NEXT_STAGE=MILESTONE_21_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1" in task1
    assert "MILESTONE_20_TASK_7_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8" in milestone20
    assert "MILESTONE_20_TASK_7_TASK_8_USED=false" in milestone20


def test_task_2_scope_lock_contract() -> None:
    lock = build_milestone_21_objective_scope_lock()

    assert lock.valid is True
    assert lock.scope_lock_ok is True
    assert lock.task_budget_max == 8
    assert lock.current_task_number == 2
    assert lock.recommended_closure_task_number == 6
    assert lock.reserve_task_number == 7
    assert lock.emergency_only_task_number == 8
    assert len(lock.in_scope_items) == 5
    assert len(lock.out_of_scope_items) == 10
    assert validate_milestone_21_objective_scope_lock(lock) == ()


def test_task_2_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_21_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert "MILESTONE_21_TASK_2_SCOPE_LOCK_ID=MILESTONE_21_SCOPE_OPERATOR_DECISION_HANDOFF_LOCAL_ONLY" in text
    assert "MILESTONE_21_TASK_2_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_21_TASK_2_CURRENT_TASK_NUMBER=2" in text
    assert "MILESTONE_21_TASK_2_OBJECTIVE_SELECTED=true" in text
    assert "MILESTONE_21_TASK_2_SCOPE_LOCKED=true" in text
    assert "MILESTONE_21_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in text
    assert "MILESTONE_21_TASK_2_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_21_TASK_2_IN_SCOPE_ITEM_COUNT=5" in text
    assert "MILESTONE_21_TASK_2_OUT_OF_SCOPE_ITEM_COUNT=10" in text
    assert "MILESTONE_21_TASK_2_MILESTONE_20_TASK_8_REQUIRED=false" in text
    assert "MILESTONE_21_TASK_2_NEXT_STAGE=MILESTONE_21_TASK_3_SCOPED_OPERATOR_DECISION_HANDOFF_IMPLEMENTATION_V1" in text


def test_task_2_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_21_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert manifest["scopeLockId"] == "MILESTONE_21_SCOPE_OPERATOR_DECISION_HANDOFF_LOCAL_ONLY"
    assert manifest["taskBudgetMax"] == 8
    assert manifest["currentTaskNumber"] == 2
    assert manifest["objectiveSelected"] is True
    assert manifest["scopeLocked"] is True
    assert manifest["implementationAllowedNext"] is True
    assert manifest["implementationStarted"] is False
    assert manifest["inScopeItemCount"] == 5
    assert manifest["outOfScopeItemCount"] == 10
    assert artifact["valid"] is True
    assert artifact["scopeLockOk"] is True
    assert artifact["issues"] == []
