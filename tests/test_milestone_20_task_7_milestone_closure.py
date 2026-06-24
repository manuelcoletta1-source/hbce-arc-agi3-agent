"""Milestone #20 Task 7 milestone closure validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_20_closure import (
    build_milestone_20_closure,
    validate_milestone_20_closure,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-20-task-7-milestone-closure-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_20_closure.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_20_closure.py"
MANIFEST = ROOT / "examples" / "milestone-20" / "milestone-closure-v1" / "task-7-manifest.json"
INDEX = ROOT / "examples" / "milestone-20" / "milestone-closure-v1" / "task-7-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-20" / "milestone-closure-v1" / "task-7-milestone-closure.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-20" / "milestone-closure-v1" / "task-7-milestone-closure.md"
TASK_6_DOC = ROOT / "docs" / "milestone-20-task-6-validation-and-integration-v1.md"
TASK_5_DOC = ROOT / "docs" / "milestone-20-task-5-governed-execution-budget-alignment-v1.md"
M19_GUARD = ROOT / "docs" / "milestone-19-task-142-final-closure-and-recursion-guard-v1.md"


def test_task_7_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert TASK_6_DOC.exists()
    assert TASK_5_DOC.exists()
    assert M19_GUARD.exists()


def test_task_7_dependencies_are_present() -> None:
    task6 = TASK_6_DOC.read_text(encoding="utf-8")
    task5 = TASK_5_DOC.read_text(encoding="utf-8")
    guard = M19_GUARD.read_text(encoding="utf-8")

    assert "MILESTONE_20_TASK_6_VALIDATION_AND_INTEGRATION_READY=true" in task6
    assert "MILESTONE_20_TASK_6_NEXT_STAGE=MILESTONE_20_TASK_7_MILESTONE_CLOSURE_V1" in task6
    assert "MILESTONE_20_TASK_5_GOVERNED_EXECUTION_BUDGET_ALIGNMENT_READY=true" in task5
    assert "MILESTONE_20_TASK_5_TASK_BUDGET_MAX=8" in task5
    assert "MILESTONE_19_TASK_142_MILESTONE_19_FINAL_STATUS=CLOSED_WITH_PROCESS_CORRECTION" in guard
    assert "MILESTONE_19_TASK_142_MILESTONE_19_CONTINUE_RECURSIVE_TASKS=false" in guard


def test_task_7_closure_contract() -> None:
    closure = build_milestone_20_closure()

    assert closure.valid is True
    assert closure.closure_ok is True
    assert closure.task_budget_max == 8
    assert closure.final_task_number == 7
    assert closure.completed_task_count == 7
    assert closure.emergency_reserve_task_number == 8
    assert closure.emergency_only_task_label == "MILESTONE_20_TASK_8_EMERGENCY_RESERVE_ONLY_UNUSED"
    assert validate_milestone_20_closure(closure) == ()


def test_task_7_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_20_TASK_7_MILESTONE_CLOSURE_READY=true" in text
    assert "MILESTONE_20_TASK_7_TECHNICAL_STATUS=PASS" in text
    assert "MILESTONE_20_TASK_7_PROCESS_STATUS=GOVERNED_WITHIN_TASK_BUDGET" in text
    assert "MILESTONE_20_TASK_7_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8" in text
    assert "MILESTONE_20_TASK_7_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_20_TASK_7_FINAL_TASK_NUMBER=7" in text
    assert "MILESTONE_20_TASK_7_COMPLETED_TASK_COUNT=7" in text
    assert "MILESTONE_20_TASK_7_TASK_8_USED=false" in text
    assert "MILESTONE_20_TASK_7_EMERGENCY_RESERVE_UNUSED=true" in text
    assert "MILESTONE_20_TASK_7_NO_RECURSIVE_META_LAYER=true" in text
    assert "MILESTONE_20_TASK_7_REOPEN_MILESTONE_19_REQUIRED=false" in text
    assert "MILESTONE_20_TASK_7_REWRITE_MILESTONE_19_REQUIRED=false" in text
    assert "MILESTONE_20_TASK_7_NEXT_STAGE=MILESTONE_20_CLOSED_NO_TASK_8_USED" in text


def test_task_7_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_20_TASK_7_MILESTONE_CLOSURE_V1"
    assert manifest["technicalStatus"] == "PASS"
    assert manifest["processStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
    assert manifest["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8"
    assert manifest["taskBudgetMax"] == 8
    assert manifest["finalTaskNumber"] == 7
    assert manifest["completedTaskCount"] == 7
    assert manifest["task8Used"] is False
    assert manifest["emergencyReserveUnused"] is True
    assert artifact["valid"] is True
    assert artifact["closureOk"] is True
    assert artifact["issues"] == []
