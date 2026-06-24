"""Milestone #20 Task 6 validation and integration validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_20_validation_integration import (
    build_milestone_20_validation_integration,
    validate_milestone_20_validation_integration,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-20-task-6-validation-and-integration-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_20_validation_integration.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_20_validation_integration.py"
MANIFEST = ROOT / "examples" / "milestone-20" / "validation-and-integration-v1" / "task-6-manifest.json"
INDEX = ROOT / "examples" / "milestone-20" / "validation-and-integration-v1" / "task-6-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-20" / "validation-and-integration-v1" / "task-6-validation-integration.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-20" / "validation-and-integration-v1" / "task-6-validation-integration.md"
TASK_5_DOC = ROOT / "docs" / "milestone-20-task-5-governed-execution-budget-alignment-v1.md"
M19_GUARD = ROOT / "docs" / "milestone-19-task-142-final-closure-and-recursion-guard-v1.md"


def test_task_6_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert TASK_5_DOC.exists()
    assert M19_GUARD.exists()


def test_task_6_dependencies_are_present() -> None:
    task5 = TASK_5_DOC.read_text(encoding="utf-8")
    guard = M19_GUARD.read_text(encoding="utf-8")

    assert "MILESTONE_20_TASK_5_GOVERNED_EXECUTION_BUDGET_ALIGNMENT_READY=true" in task5
    assert "MILESTONE_20_TASK_5_TASK_BUDGET_MAX=8" in task5
    assert "MILESTONE_20_TASK_5_NEXT_STAGE=MILESTONE_20_TASK_6_VALIDATION_AND_INTEGRATION_V1" in task5
    assert "MILESTONE_19_TASK_142_MILESTONE_19_FINAL_STATUS=CLOSED_WITH_PROCESS_CORRECTION" in guard
    assert "MILESTONE_19_TASK_142_MILESTONE_19_CONTINUE_RECURSIVE_TASKS=false" in guard


def test_task_6_validation_contract() -> None:
    validation = build_milestone_20_validation_integration()

    assert validation.valid is True
    assert validation.task_budget_max == 8
    assert validation.current_task_number == 6
    assert validation.remaining_budget_after_current_task == 2
    assert validation.next_closure_task_number == 7
    assert validation.emergency_reserve_task_number == 8
    assert len(validation.integrated_task_labels) == 6
    assert validation.required_closure_task_label == "MILESTONE_20_TASK_7_MILESTONE_CLOSURE"
    assert validate_milestone_20_validation_integration(validation) == ()


def test_task_6_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_20_TASK_6_VALIDATION_AND_INTEGRATION_READY=true" in text
    assert "MILESTONE_20_TASK_6_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_20_TASK_6_CURRENT_TASK_NUMBER=6" in text
    assert "MILESTONE_20_TASK_6_REMAINING_BUDGET_AFTER_CURRENT_TASK=2" in text
    assert "MILESTONE_20_TASK_6_NEXT_CLOSURE_TASK_NUMBER=7" in text
    assert "MILESTONE_20_TASK_6_EMERGENCY_RESERVE_TASK_NUMBER=8" in text
    assert "MILESTONE_20_TASK_6_INTEGRATED_TASK_COUNT=6" in text
    assert "MILESTONE_20_TASK_6_MILESTONE_19_REMAINS_CLOSED=true" in text
    assert "MILESTONE_20_TASK_6_MILESTONE_20_READY_FOR_CLOSURE=true" in text
    assert "MILESTONE_20_TASK_6_NO_RECURSIVE_META_LAYER=true" in text
    assert "MILESTONE_20_TASK_6_CLOSURE_REQUIRED_NEXT=true" in text
    assert "MILESTONE_20_TASK_6_NEXT_STAGE=MILESTONE_20_TASK_7_MILESTONE_CLOSURE_V1" in text


def test_task_6_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_20_TASK_6_VALIDATION_AND_INTEGRATION_V1"
    assert manifest["taskBudgetMax"] == 8
    assert manifest["currentTaskNumber"] == 6
    assert manifest["remainingBudgetAfterCurrentTask"] == 2
    assert manifest["nextClosureTaskNumber"] == 7
    assert manifest["emergencyReserveTaskNumber"] == 8
    assert manifest["integratedTaskCount"] == 6
    assert manifest["milestone19RemainsClosed"] is True
    assert manifest["milestone20ReadyForClosure"] is True
    assert manifest["closureRequiredNext"] is True
    assert artifact["valid"] is True
    assert artifact["issues"] == []
