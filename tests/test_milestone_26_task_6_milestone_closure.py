"""Milestone #26 Task 6 milestone closure validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_26_closure import (
    build_milestone_26_closure,
    validate_milestone_26_closure,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "milestone-26-task-6-milestone-closure-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_26_closure.py"
REPORT = ROOT / "examples" / "milestone-26" / "milestone-closure-v1" / "task-6-milestone-closure.json"
MANIFEST = ROOT / "examples" / "milestone-26" / "milestone-closure-v1" / "task-6-manifest.json"
SUMMARY = ROOT / "examples" / "milestone-26" / "milestone-closure-v1" / "task-6-final-summary.json"
SOURCE_DOC = ROOT / "docs" / "milestone-26-task-5-integration-regression-v1.md"


def test_task_6_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert REPORT.exists()
    assert MANIFEST.exists()
    assert SUMMARY.exists()
    assert SOURCE_DOC.exists()


def test_task_6_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")
    assert "MILESTONE_26_TASK_5_INTEGRATION_REGRESSION_READY=true" in source
    assert "MILESTONE_26_TASK_5_TASK_CHAIN_VALIDATED=true" in source
    assert "MILESTONE_26_TASK_5_READY_FOR_MILESTONE_CLOSURE=true" in source
    assert "MILESTONE_26_TASK_5_TASK1_VALID=true" in source
    assert "MILESTONE_26_TASK_5_TASK2_VALID=true" in source
    assert "MILESTONE_26_TASK_5_TASK3_VALID=true" in source
    assert "MILESTONE_26_TASK_5_TASK4_VALID=true" in source
    assert "MILESTONE_26_TASK_5_NEXT_STAGE=MILESTONE_26_TASK_6_MILESTONE_CLOSURE_V1" in source


def test_task_6_closure_contract() -> None:
    closure = build_milestone_26_closure()
    assert closure.valid is True
    assert closure.closure_ok is True
    assert len(closure.closure_checks) == 16
    assert len(closure.generated_artifacts) == 5
    assert validate_milestone_26_closure(closure) == ()


def test_task_6_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_26_TASK_6_MILESTONE_CLOSURE_READY=true" in text
    assert "MILESTONE_26_TASK_6_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6" in text
    assert "MILESTONE_26_TASK_6_TECHNICAL_STATUS=PASS" in text
    assert "MILESTONE_26_TASK_6_PROCESS_STATUS=GOVERNED_WITHIN_TASK_BUDGET" in text
    assert "MILESTONE_26_TASK_6_FINAL_TASK_NUMBER=6" in text
    assert "MILESTONE_26_TASK_6_COMPLETED_TASK_COUNT=6" in text
    assert "MILESTONE_26_TASK_6_TASK_7_USED=false" in text
    assert "MILESTONE_26_TASK_6_TASK_8_USED=false" in text
    assert "MILESTONE_26_TASK_6_NO_TASK_7_OR_8_USED=true" in text
    assert "MILESTONE_26_TASK_6_MILESTONE_CLOSED=true" in text
    assert "MILESTONE_26_TASK_6_READY_FOR_NEXT_MILESTONE=true" in text
    assert "MILESTONE_26_TASK_6_TASK5_VALID=true" in text
    assert "MILESTONE_26_TASK_6_ARCHIVE_ITEM_COUNT=3" in text
    assert "MILESTONE_26_TASK_6_ARCHIVED_MILESTONE_IDS=MILESTONE_20,MILESTONE_21,MILESTONE_22" in text
    assert "MILESTONE_26_TASK_6_FAST_SOURCE_INTEGRATION_SNAPSHOT=true" in text
    assert "MILESTONE_26_TASK_6_NEXT_STAGE=MILESTONE_26_CLOSED_NO_TASK_7_OR_8_USED" in text


def test_task_6_artifacts() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))

    assert report["valid"] is True
    assert report["closureOk"] is True
    assert report["issues"] == []
    assert report["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert report["technicalStatus"] == "PASS"
    assert report["processStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
    assert report["task7Used"] is False
    assert report["task8Used"] is False
    assert report["milestoneClosed"] is True
    assert report["readyForNextMilestone"] is True
    assert report["archiveItemCount"] == 3

    assert manifest["taskId"] == "MILESTONE_26_TASK_6_MILESTONE_CLOSURE_V1"
    assert manifest["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert manifest["task7Used"] is False
    assert manifest["task8Used"] is False
    assert manifest["milestoneClosed"] is True
    assert manifest["readyForNextMilestone"] is True
    assert manifest["nextStage"] == "MILESTONE_26_CLOSED_NO_TASK_7_OR_8_USED"

    assert summary["valid"] is True
    assert summary["closureOk"] is True
    assert summary["issues"] == []
    assert summary["milestoneClosed"] is True
