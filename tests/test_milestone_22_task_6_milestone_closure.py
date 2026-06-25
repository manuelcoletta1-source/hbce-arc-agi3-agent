"""Milestone #22 Task 6 milestone closure validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_22_closure import (
    build_milestone_22_closure,
    validate_milestone_22_closure,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-22-task-6-milestone-closure-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_22_closure.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_22_closure.py"
MANIFEST = ROOT / "examples" / "milestone-22" / "milestone-closure-v1" / "task-6-manifest.json"
INDEX = ROOT / "examples" / "milestone-22" / "milestone-closure-v1" / "task-6-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-22" / "milestone-closure-v1" / "task-6-milestone-closure.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-22" / "milestone-closure-v1" / "task-6-milestone-closure.md"
TASK_5_DOC = ROOT / "docs" / "milestone-22-task-5-integration-regression-v1.md"


def test_task_6_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert TASK_5_DOC.exists()


def test_task_6_dependency_is_present() -> None:
    task5 = TASK_5_DOC.read_text(encoding="utf-8")

    assert "MILESTONE_22_TASK_5_INTEGRATION_REGRESSION_READY=true" in task5
    assert "MILESTONE_22_TASK_5_READY_FOR_MILESTONE_CLOSURE=true" in task5
    assert "MILESTONE_22_TASK_5_M20_TASK_7_USED=true" in task5
    assert "MILESTONE_22_TASK_5_M20_TASK_8_USED=false" in task5
    assert "MILESTONE_22_TASK_5_NEXT_STAGE=MILESTONE_22_TASK_6_MILESTONE_CLOSURE_V1" in task5


def test_task_6_closure_contract() -> None:
    closure = build_milestone_22_closure()

    assert closure.valid is True
    assert closure.closure_ok is True
    assert closure.final_status == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert closure.technical_status == "PASS"
    assert closure.process_status == "GOVERNED_WITHIN_TASK_BUDGET"
    assert closure.task_budget_max == 8
    assert closure.final_task_number == 6
    assert len(closure.completed_task_ids) == 6
    assert len(closure.closure_checks) == 12
    assert validate_milestone_22_closure(closure) == ()


def test_task_6_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_22_TASK_6_MILESTONE_CLOSURE_READY=true" in text
    assert "MILESTONE_22_TASK_6_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6" in text
    assert "MILESTONE_22_TASK_6_TECHNICAL_STATUS=PASS" in text
    assert "MILESTONE_22_TASK_6_PROCESS_STATUS=GOVERNED_WITHIN_TASK_BUDGET" in text
    assert "MILESTONE_22_TASK_6_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_22_TASK_6_FINAL_TASK_NUMBER=6" in text
    assert "MILESTONE_22_TASK_6_COMPLETED_TASK_COUNT=6" in text
    assert "MILESTONE_22_TASK_6_TASK_7_USED=false" in text
    assert "MILESTONE_22_TASK_6_TASK_8_USED=false" in text
    assert "MILESTONE_22_TASK_6_RESERVE_UNUSED=true" in text
    assert "MILESTONE_22_TASK_6_EMERGENCY_RESERVE_UNUSED=true" in text
    assert "MILESTONE_22_TASK_6_MILESTONE_CLOSED=true" in text
    assert "MILESTONE_22_TASK_6_M20_FINAL_TASK_NUMBER=7" in text
    assert "MILESTONE_22_TASK_6_M20_TASK_7_USED=true" in text
    assert "MILESTONE_22_TASK_6_M20_TASK_8_USED=false" in text
    assert "MILESTONE_22_TASK_6_NEXT_STAGE=MILESTONE_22_CLOSED_NO_TASK_7_OR_8_USED" in text


def test_task_6_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_22_TASK_6_MILESTONE_CLOSURE_V1"
    assert manifest["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert manifest["technicalStatus"] == "PASS"
    assert manifest["processStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
    assert manifest["taskBudgetMax"] == 8
    assert manifest["finalTaskNumber"] == 6
    assert manifest["completedTaskCount"] == 6
    assert manifest["task7Used"] is False
    assert manifest["task8Used"] is False
    assert manifest["reserveUnused"] is True
    assert manifest["emergencyReserveUnused"] is True
    assert manifest["milestoneClosed"] is True
    assert manifest["m20FinalTaskNumber"] == 7
    assert manifest["m20Task7Used"] is True
    assert manifest["m20Task8Used"] is False
    assert artifact["valid"] is True
    assert artifact["closureOk"] is True
    assert artifact["issues"] == []
