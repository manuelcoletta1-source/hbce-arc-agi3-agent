"""Milestone #27 Task 1 governed opening validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_27_governed_opening import (
    build_milestone_27_governed_opening,
    validate_milestone_27_governed_opening,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "milestone-27-task-1-governed-opening-with-task-budget-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_27_governed_opening.py"
REPORT = ROOT / "examples" / "milestone-27" / "governed-opening-with-task-budget-v1" / "task-1-governed-opening.json"
MANIFEST = ROOT / "examples" / "milestone-27" / "governed-opening-with-task-budget-v1" / "task-1-manifest.json"
SOURCE_DOC = ROOT / "docs" / "milestone-26-task-6-milestone-closure-v1.md"


def test_task_1_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert REPORT.exists()
    assert MANIFEST.exists()
    assert SOURCE_DOC.exists()


def test_task_1_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")
    assert "MILESTONE_26_TASK_6_MILESTONE_CLOSURE_READY=true" in source
    assert "MILESTONE_26_TASK_6_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6" in source
    assert "MILESTONE_26_TASK_6_TECHNICAL_STATUS=PASS" in source
    assert "MILESTONE_26_TASK_6_PROCESS_STATUS=GOVERNED_WITHIN_TASK_BUDGET" in source
    assert "MILESTONE_26_TASK_6_TASK_7_USED=false" in source
    assert "MILESTONE_26_TASK_6_TASK_8_USED=false" in source
    assert "MILESTONE_26_TASK_6_MILESTONE_CLOSED=true" in source
    assert "MILESTONE_26_TASK_6_READY_FOR_NEXT_MILESTONE=true" in source


def test_task_1_governed_opening_contract() -> None:
    opening = build_milestone_27_governed_opening()
    assert opening.valid is True
    assert opening.opening_ok is True
    assert opening.current_task_number == 1
    assert opening.task_budget_max == 8
    assert opening.remaining_budget_after_current_task == 7
    assert len(opening.opening_checks) == 16
    assert len(opening.generated_artifacts) == 4
    assert validate_milestone_27_governed_opening(opening) == ()


def test_task_1_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_27_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in text
    assert "MILESTONE_27_TASK_1_SOURCE_MILESTONE_ID=MILESTONE_26" in text
    assert "MILESTONE_27_TASK_1_SOURCE_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6" in text
    assert "MILESTONE_27_TASK_1_SOURCE_TECHNICAL_STATUS=PASS" in text
    assert "MILESTONE_27_TASK_1_SOURCE_PROCESS_STATUS=GOVERNED_WITHIN_TASK_BUDGET" in text
    assert "MILESTONE_27_TASK_1_SOURCE_TASK_7_USED=false" in text
    assert "MILESTONE_27_TASK_1_SOURCE_TASK_8_USED=false" in text
    assert "MILESTONE_27_TASK_1_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_27_TASK_1_CURRENT_TASK_NUMBER=1" in text
    assert "MILESTONE_27_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT=true" in text
    assert "MILESTONE_27_TASK_1_SCOPE_LOCK_REQUIRED_NEXT=true" in text
    assert "MILESTONE_27_TASK_1_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_27_TASK_1_IMPLEMENTATION_ALLOWED_AT_TASK_1=false" in text
    assert "MILESTONE_27_TASK_1_FAST_SOURCE_CLOSURE_SNAPSHOT=true" in text
    assert "MILESTONE_27_TASK_1_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in text
    assert "MILESTONE_27_TASK_1_NEXT_STAGE=MILESTONE_27_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1" in text


def test_task_1_artifacts() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert report["valid"] is True
    assert report["openingOk"] is True
    assert report["issues"] == []
    assert report["sourceMilestoneId"] == "MILESTONE_26"
    assert report["sourceFinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert report["sourceTechnicalStatus"] == "PASS"
    assert report["sourceProcessStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
    assert report["sourceTask7Used"] is False
    assert report["sourceTask8Used"] is False
    assert report["taskBudgetMax"] == 8
    assert report["currentTaskNumber"] == 1
    assert report["objectiveSelectionRequiredNext"] is True
    assert report["scopeLockRequiredNext"] is True
    assert report["implementationStarted"] is False
    assert report["implementationAllowedAtTask1"] is False
    assert report["nextStage"] == "MILESTONE_27_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"

    assert manifest["taskId"] == "MILESTONE_27_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
    assert manifest["sourceMilestoneId"] == "MILESTONE_26"
    assert manifest["sourceFinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert manifest["governedOpeningReady"] is True
    assert manifest["taskBudgetLocked"] is True
    assert manifest["nextStage"] == "MILESTONE_27_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
