"""Milestone #21 Task 6 milestone closure validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_21_closure import (
    build_milestone_21_closure,
    validate_milestone_21_closure,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-21-task-6-milestone-closure-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_21_closure.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_21_closure.py"
MANIFEST = ROOT / "examples" / "milestone-21" / "milestone-closure-v1" / "task-6-manifest.json"
INDEX = ROOT / "examples" / "milestone-21" / "milestone-closure-v1" / "task-6-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-21" / "milestone-closure-v1" / "task-6-milestone-closure.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-21" / "milestone-closure-v1" / "task-6-milestone-closure.md"
TASK_5_DOC = ROOT / "docs" / "milestone-21-task-5-integration-regression-v1.md"
TASK_4_DOC = ROOT / "docs" / "milestone-21-task-4-validation-and-artifacts-v1.md"
TASK_3_DOC = ROOT / "docs" / "milestone-21-task-3-scoped-operator-decision-handoff-implementation-v1.md"
TASK_2_DOC = ROOT / "docs" / "milestone-21-task-2-objective-selection-and-scope-lock-v1.md"
TASK_1_DOC = ROOT / "docs" / "milestone-21-task-1-governed-opening-with-task-budget-v1.md"
M20_CLOSURE = ROOT / "docs" / "milestone-20-task-7-milestone-closure-v1.md"


def test_task_6_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert TASK_5_DOC.exists()
    assert TASK_4_DOC.exists()
    assert TASK_3_DOC.exists()
    assert TASK_2_DOC.exists()
    assert TASK_1_DOC.exists()
    assert M20_CLOSURE.exists()


def test_task_6_dependencies_are_present() -> None:
    task5 = TASK_5_DOC.read_text(encoding="utf-8")
    task4 = TASK_4_DOC.read_text(encoding="utf-8")
    task3 = TASK_3_DOC.read_text(encoding="utf-8")
    task2 = TASK_2_DOC.read_text(encoding="utf-8")
    task1 = TASK_1_DOC.read_text(encoding="utf-8")
    milestone20 = M20_CLOSURE.read_text(encoding="utf-8")

    assert "MILESTONE_21_TASK_5_READY_FOR_MILESTONE_CLOSURE=true" in task5
    assert "MILESTONE_21_TASK_5_NEXT_STAGE=MILESTONE_21_TASK_6_MILESTONE_CLOSURE_V1" in task5
    assert "MILESTONE_21_TASK_4_ARTIFACTS_READY_FOR_INTEGRATION_REGRESSION=true" in task4
    assert "MILESTONE_21_TASK_3_HANDOFF_PACKAGE_CREATED=true" in task3
    assert "MILESTONE_21_TASK_2_SCOPE_LOCKED=true" in task2
    assert "MILESTONE_21_TASK_1_TASK_BUDGET_MAX=8" in task1
    assert "MILESTONE_20_TASK_7_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8" in milestone20
    assert "MILESTONE_20_TASK_7_TASK_8_USED=false" in milestone20


def test_task_6_closure_contract() -> None:
    closure = build_milestone_21_closure()

    assert closure.valid is True
    assert closure.closure_ok is True
    assert closure.task_budget_max == 8
    assert closure.final_task_number == 6
    assert closure.completed_task_count == 6
    assert closure.remaining_budget_after_closure == 2
    assert closure.reserve_task_number == 7
    assert closure.emergency_only_task_number == 8
    assert len(closure.closure_checks) == 10
    assert validate_milestone_21_closure(closure) == ()


def test_task_6_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_21_TASK_6_MILESTONE_CLOSURE_READY=true" in text
    assert "MILESTONE_21_TASK_6_TECHNICAL_STATUS=PASS" in text
    assert "MILESTONE_21_TASK_6_PROCESS_STATUS=GOVERNED_WITHIN_TASK_BUDGET" in text
    assert "MILESTONE_21_TASK_6_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6" in text
    assert "MILESTONE_21_TASK_6_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_21_TASK_6_FINAL_TASK_NUMBER=6" in text
    assert "MILESTONE_21_TASK_6_COMPLETED_TASK_COUNT=6" in text
    assert "MILESTONE_21_TASK_6_TASK_7_USED=false" in text
    assert "MILESTONE_21_TASK_6_TASK_8_USED=false" in text
    assert "MILESTONE_21_TASK_6_RESERVE_UNUSED=true" in text
    assert "MILESTONE_21_TASK_6_EMERGENCY_RESERVE_UNUSED=true" in text
    assert "MILESTONE_21_TASK_6_CLOSURE_COMPLETED=true" in text
    assert "MILESTONE_21_TASK_6_NO_RECURSIVE_META_LAYER=true" in text
    assert "MILESTONE_21_TASK_6_NEXT_STAGE=MILESTONE_21_CLOSED_NO_TASK_7_OR_8_USED" in text


def test_task_6_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_21_TASK_6_MILESTONE_CLOSURE_V1"
    assert manifest["technicalStatus"] == "PASS"
    assert manifest["processStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
    assert manifest["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert manifest["taskBudgetMax"] == 8
    assert manifest["finalTaskNumber"] == 6
    assert manifest["completedTaskCount"] == 6
    assert manifest["task7Used"] is False
    assert manifest["task8Used"] is False
    assert manifest["reserveUnused"] is True
    assert manifest["emergencyReserveUnused"] is True
    assert artifact["valid"] is True
    assert artifact["closureOk"] is True
    assert artifact["issues"] == []
