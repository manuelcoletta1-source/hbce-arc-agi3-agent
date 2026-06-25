"""Milestone #23 Task 1 governed opening validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_23_governed_opening import (
    build_milestone_23_governed_opening,
    validate_milestone_23_governed_opening,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-23-task-1-governed-opening-with-task-budget-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_23_governed_opening.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_23_governed_opening.py"
MANIFEST = ROOT / "examples" / "milestone-23" / "governed-opening-with-task-budget-v1" / "task-1-manifest.json"
INDEX = ROOT / "examples" / "milestone-23" / "governed-opening-with-task-budget-v1" / "task-1-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-23" / "governed-opening-with-task-budget-v1" / "task-1-governed-opening.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-23" / "governed-opening-with-task-budget-v1" / "task-1-governed-opening.md"
SOURCE_DOC = ROOT / "docs" / "milestone-22-task-6-milestone-closure-v1.md"


def test_task_1_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert SOURCE_DOC.exists()


def test_task_1_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")

    assert "MILESTONE_22_TASK_6_MILESTONE_CLOSURE_READY=true" in source
    assert "MILESTONE_22_TASK_6_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6" in source
    assert "MILESTONE_22_TASK_6_TASK_7_USED=false" in source
    assert "MILESTONE_22_TASK_6_TASK_8_USED=false" in source
    assert "MILESTONE_22_TASK_6_MILESTONE_CLOSED=true" in source


def test_task_1_governed_opening_contract() -> None:
    opening = build_milestone_23_governed_opening()

    assert opening.valid is True
    assert opening.opening_ok is True
    assert opening.task_budget_min == 4
    assert opening.task_budget_max == 8
    assert opening.current_task_number == 1
    assert opening.recommended_closure_task_number == 6
    assert opening.source_snapshot.valid is True
    assert validate_milestone_23_governed_opening(opening) == ()


def test_task_1_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_23_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in text
    assert "MILESTONE_23_TASK_1_SOURCE_MILESTONE_ID=MILESTONE_22" in text
    assert "MILESTONE_23_TASK_1_SOURCE_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6" in text
    assert "MILESTONE_23_TASK_1_SOURCE_TASK_7_USED=false" in text
    assert "MILESTONE_23_TASK_1_SOURCE_TASK_8_USED=false" in text
    assert "MILESTONE_23_TASK_1_TASK_BUDGET_MIN=4" in text
    assert "MILESTONE_23_TASK_1_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_23_TASK_1_CURRENT_TASK_NUMBER=1" in text
    assert "MILESTONE_23_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT=true" in text
    assert "MILESTONE_23_TASK_1_SCOPE_LOCK_REQUIRED_NEXT=true" in text
    assert "MILESTONE_23_TASK_1_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_23_TASK_1_FAST_SNAPSHOT_DEPENDENCY_MODE=true" in text
    assert "MILESTONE_23_TASK_1_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in text
    assert "MILESTONE_23_TASK_1_NEXT_STAGE=MILESTONE_23_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1" in text


def test_task_1_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_23_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
    assert manifest["sourceMilestoneId"] == "MILESTONE_22"
    assert manifest["sourceFinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert manifest["sourceTask7Used"] is False
    assert manifest["sourceTask8Used"] is False
    assert manifest["taskBudgetMin"] == 4
    assert manifest["taskBudgetMax"] == 8
    assert manifest["currentTaskNumber"] == 1
    assert manifest["objectiveSelectionRequiredNext"] is True
    assert manifest["scopeLockRequiredNext"] is True
    assert manifest["implementationStarted"] is False
    assert artifact["valid"] is True
    assert artifact["openingOk"] is True
    assert artifact["issues"] == []
