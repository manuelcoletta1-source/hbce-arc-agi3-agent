"""Milestone #21 Task 1 governed opening with task budget validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_21_governed_opening import (
    build_milestone_21_governed_opening,
    validate_milestone_21_governed_opening,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-21-task-1-governed-opening-with-task-budget-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_21_governed_opening.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_21_governed_opening.py"
MANIFEST = ROOT / "examples" / "milestone-21" / "governed-opening-with-task-budget-v1" / "task-1-manifest.json"
INDEX = ROOT / "examples" / "milestone-21" / "governed-opening-with-task-budget-v1" / "task-1-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-21" / "governed-opening-with-task-budget-v1" / "task-1-governed-opening.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-21" / "governed-opening-with-task-budget-v1" / "task-1-governed-opening.md"
M20_CLOSURE = ROOT / "docs" / "milestone-20-task-7-milestone-closure-v1.md"
M19_GUARD = ROOT / "docs" / "milestone-19-task-142-final-closure-and-recursion-guard-v1.md"


def test_task_1_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert M20_CLOSURE.exists()
    assert M19_GUARD.exists()


def test_task_1_dependencies_are_present() -> None:
    milestone_20 = M20_CLOSURE.read_text(encoding="utf-8")
    milestone_19 = M19_GUARD.read_text(encoding="utf-8")

    assert "MILESTONE_20_TASK_7_MILESTONE_CLOSURE_READY=true" in milestone_20
    assert "MILESTONE_20_TASK_7_TASK_8_USED=false" in milestone_20
    assert "MILESTONE_20_TASK_7_NEXT_STAGE=MILESTONE_20_CLOSED_NO_TASK_8_USED" in milestone_20
    assert "MILESTONE_19_TASK_142_FUTURE_BUDGET_POLICY_REQUIRED=true" in milestone_19
    assert "MILESTONE_19_TASK_142_STANDARD_MILESTONE_TASK_MAX=8" in milestone_19


def test_task_1_opening_contract() -> None:
    opening = build_milestone_21_governed_opening()

    assert opening.valid is True
    assert opening.opening_ok is True
    assert opening.task_budget_min == 4
    assert opening.task_budget_max == 8
    assert opening.current_task_number == 1
    assert opening.recommended_closure_task_number == 6
    assert opening.reserve_task_number == 7
    assert opening.emergency_only_task_number == 8
    assert len(opening.planned_task_labels) == 6
    assert validate_milestone_21_governed_opening(opening) == ()


def test_task_1_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_21_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in text
    assert "MILESTONE_21_TASK_1_TASK_BUDGET_MIN=4" in text
    assert "MILESTONE_21_TASK_1_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_21_TASK_1_CURRENT_TASK_NUMBER=1" in text
    assert "MILESTONE_21_TASK_1_RECOMMENDED_CLOSURE_TASK_NUMBER=6" in text
    assert "MILESTONE_21_TASK_1_RESERVE_TASK_NUMBER=7" in text
    assert "MILESTONE_21_TASK_1_EMERGENCY_ONLY_TASK_NUMBER=8" in text
    assert "MILESTONE_21_TASK_1_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_21_TASK_1_SCOPE_LOCK_REQUIRED_NEXT=true" in text
    assert "MILESTONE_21_TASK_1_NO_RECURSIVE_META_LAYER=true" in text
    assert "MILESTONE_21_TASK_1_MILESTONE_20_TASK_8_REQUIRED=false" in text
    assert "MILESTONE_21_TASK_1_NEXT_STAGE=MILESTONE_21_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1" in text


def test_task_1_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_21_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
    assert manifest["taskBudgetMin"] == 4
    assert manifest["taskBudgetMax"] == 8
    assert manifest["currentTaskNumber"] == 1
    assert manifest["recommendedClosureTaskNumber"] == 6
    assert manifest["reserveTaskNumber"] == 7
    assert manifest["emergencyOnlyTaskNumber"] == 8
    assert manifest["implementationStarted"] is False
    assert manifest["scopeLockRequiredNext"] is True
    assert manifest["closureRequired"] is True
    assert manifest["noRecursiveMetaLayer"] is True
    assert artifact["valid"] is True
    assert artifact["openingOk"] is True
    assert artifact["issues"] == []
