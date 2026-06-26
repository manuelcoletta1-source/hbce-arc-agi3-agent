"""Milestone #25 Task 6 milestone closure validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_25_closure import (
    build_milestone_25_closure,
    validate_milestone_25_closure,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "milestone-25-task-6-milestone-closure-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_25_closure.py"
MANIFEST = ROOT / "examples" / "milestone-25" / "milestone-closure-v1" / "task-6-manifest.json"
REPORT = ROOT / "examples" / "milestone-25" / "milestone-closure-v1" / "task-6-milestone-closure.json"
SUMMARY = ROOT / "examples" / "milestone-25" / "milestone-closure-v1" / "task-6-final-summary.json"
SOURCE_DOC = ROOT / "docs" / "milestone-25-task-5-integration-regression-v1.md"


def test_task_6_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MANIFEST.exists()
    assert REPORT.exists()
    assert SUMMARY.exists()
    assert SOURCE_DOC.exists()


def test_task_6_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")
    assert "MILESTONE_25_TASK_5_INTEGRATION_REGRESSION_READY=true" in source
    assert "MILESTONE_25_TASK_5_TASK_CHAIN_VALIDATED=true" in source
    assert "MILESTONE_25_TASK_5_NO_MUTATION_REGRESSION_VALIDATED=true" in source
    assert "MILESTONE_25_TASK_5_READY_FOR_MILESTONE_CLOSURE=true" in source
    assert "MILESTONE_25_TASK_5_NEXT_STAGE=MILESTONE_25_TASK_6_MILESTONE_CLOSURE_V1" in source


def test_task_6_closure_contract() -> None:
    closure = build_milestone_25_closure()
    assert closure.valid is True
    assert closure.closure_ok is True
    assert closure.final_status == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert closure.technical_status == "PASS"
    assert closure.process_status == "GOVERNED_WITHIN_TASK_BUDGET"
    assert closure.final_task_number == 6
    assert closure.completed_task_count == 6
    assert validate_milestone_25_closure(closure) == ()


def test_task_6_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_25_TASK_6_MILESTONE_CLOSURE_READY=true" in text
    assert "MILESTONE_25_TASK_6_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6" in text
    assert "MILESTONE_25_TASK_6_TECHNICAL_STATUS=PASS" in text
    assert "MILESTONE_25_TASK_6_PROCESS_STATUS=GOVERNED_WITHIN_TASK_BUDGET" in text
    assert "MILESTONE_25_TASK_6_FINAL_TASK_NUMBER=6" in text
    assert "MILESTONE_25_TASK_6_COMPLETED_TASK_COUNT=6" in text
    assert "MILESTONE_25_TASK_6_TASK_7_USED=false" in text
    assert "MILESTONE_25_TASK_6_TASK_8_USED=false" in text
    assert "MILESTONE_25_TASK_6_NO_TASK_7_OR_8_USED=true" in text
    assert "MILESTONE_25_TASK_6_MILESTONE_CLOSED=true" in text
    assert "MILESTONE_25_TASK_6_READY_FOR_NEXT_MILESTONE=true" in text
    assert "MILESTONE_25_TASK_6_FAST_SOURCE_INTEGRATION_SNAPSHOT=true" in text
    assert "MILESTONE_25_TASK_6_NEXT_STAGE=MILESTONE_25_CLOSED_NO_TASK_7_OR_8_USED" in text


def test_task_6_manifest_and_artifacts() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_25_TASK_6_MILESTONE_CLOSURE_V1"
    assert manifest["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert manifest["technicalStatus"] == "PASS"
    assert manifest["processStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
    assert manifest["finalTaskNumber"] == 6
    assert manifest["completedTaskCount"] == 6
    assert manifest["task7Used"] is False
    assert manifest["task8Used"] is False
    assert manifest["milestoneClosed"] is True
    assert manifest["readyForNextMilestone"] is True
    assert manifest["nextStage"] == "MILESTONE_25_CLOSED_NO_TASK_7_OR_8_USED"

    assert report["valid"] is True
    assert report["closureOk"] is True
    assert report["issues"] == []
    assert report["milestoneClosed"] is True

    assert summary["valid"] is True
    assert summary["milestoneClosed"] is True
    assert summary["readyForNextMilestone"] is True
    assert summary["issues"] == []
