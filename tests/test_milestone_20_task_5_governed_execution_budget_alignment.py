"""Milestone #20 Task 5 governed execution budget alignment validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_20_governed_execution import (
    build_milestone_20_governed_execution,
    validate_milestone_20_governed_execution,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-20-task-5-governed-execution-budget-alignment-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_20_governed_execution.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_20_governed_execution.py"
MANIFEST = ROOT / "examples" / "milestone-20" / "governed-execution-budget-alignment-v1" / "task-5-manifest.json"
INDEX = ROOT / "examples" / "milestone-20" / "governed-execution-budget-alignment-v1" / "task-5-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-20" / "governed-execution-budget-alignment-v1" / "task-5-governed-execution.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-20" / "governed-execution-budget-alignment-v1" / "task-5-governed-execution.md"
M19_GUARD = ROOT / "docs" / "milestone-19-task-142-final-closure-and-recursion-guard-v1.md"


def test_task_5_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert M19_GUARD.exists()


def test_task_5_milestone_19_guard_dependency() -> None:
    text = M19_GUARD.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_142_FINAL_CLOSURE_AND_RECURSION_GUARD_READY=true" in text
    assert "MILESTONE_19_TASK_142_STANDARD_MILESTONE_TASK_MAX=8" in text
    assert "MILESTONE_19_TASK_142_MAX_REVIEW_DEPTH=1" in text
    assert "MILESTONE_19_TASK_142_MAX_AUTHORIZATION_DEPTH=1" in text
    assert "MILESTONE_19_TASK_142_MAX_FINALIZATION_DEPTH=1" in text


def test_task_5_governed_execution_contract() -> None:
    execution = build_milestone_20_governed_execution()

    assert execution.valid is True
    assert execution.task_budget_max == 8
    assert execution.completed_task_count_at_alignment == 4
    assert execution.current_task_number == 5
    assert execution.recommended_closure_task_number == 7
    assert execution.emergency_reserve_task_count == 1
    assert execution.remaining_budget_after_current_task == 3
    assert validate_milestone_20_governed_execution(execution) == ()


def test_task_5_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_20_TASK_5_GOVERNED_EXECUTION_BUDGET_ALIGNMENT_READY=true" in text
    assert "MILESTONE_20_TASK_5_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_20_TASK_5_COMPLETED_TASK_COUNT_AT_ALIGNMENT=4" in text
    assert "MILESTONE_20_TASK_5_CURRENT_TASK_NUMBER=5" in text
    assert "MILESTONE_20_TASK_5_RECOMMENDED_CLOSURE_TASK_NUMBER=7" in text
    assert "MILESTONE_20_TASK_5_EMERGENCY_RESERVE_TASK_COUNT=1" in text
    assert "MILESTONE_20_TASK_5_NO_RECURSIVE_META_LAYER=true" in text
    assert "MILESTONE_20_TASK_5_MAX_REVIEW_DEPTH=1" in text
    assert "MILESTONE_20_TASK_5_MAX_AUTHORIZATION_DEPTH=1" in text
    assert "MILESTONE_20_TASK_5_MAX_FINALIZATION_DEPTH=1" in text
    assert "MILESTONE_20_TASK_5_CLOSURE_REQUIRED=true" in text
    assert "MILESTONE_20_TASK_5_NEXT_STAGE=MILESTONE_20_TASK_6_VALIDATION_AND_INTEGRATION_V1" in text


def test_task_5_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_20_TASK_5_GOVERNED_EXECUTION_BUDGET_ALIGNMENT_V1"
    assert manifest["taskBudgetMax"] == 8
    assert manifest["completedTaskCountAtAlignment"] == 4
    assert manifest["currentTaskNumber"] == 5
    assert manifest["recommendedClosureTaskNumber"] == 7
    assert manifest["emergencyReserveTaskCount"] == 1
    assert manifest["noRecursiveMetaLayer"] is True
    assert manifest["closureRequired"] is True
    assert artifact["taskBudgetMax"] == 8
    assert artifact["valid"] is True
    assert artifact["issues"] == []
