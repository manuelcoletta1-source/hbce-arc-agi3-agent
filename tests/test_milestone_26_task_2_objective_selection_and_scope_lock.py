"""Milestone #26 Task 2 objective selection and scope lock validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_26_objective_scope_lock import (
    build_milestone_26_objective_scope_lock,
    validate_milestone_26_objective_scope_lock,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "milestone-26-task-2-objective-selection-and-scope-lock-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_26_objective_scope_lock.py"
MANIFEST = ROOT / "examples" / "milestone-26" / "objective-selection-and-scope-lock-v1" / "task-2-manifest.json"
REPORT = ROOT / "examples" / "milestone-26" / "objective-selection-and-scope-lock-v1" / "task-2-objective-scope-lock.json"
SOURCE_DOC = ROOT / "docs" / "milestone-26-task-1-governed-opening-with-task-budget-v1.md"


def test_task_2_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MANIFEST.exists()
    assert REPORT.exists()
    assert SOURCE_DOC.exists()


def test_task_2_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")
    assert "MILESTONE_26_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in source
    assert "MILESTONE_26_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT=true" in source
    assert "MILESTONE_26_TASK_1_SCOPE_LOCK_REQUIRED_NEXT=true" in source
    assert "MILESTONE_26_TASK_1_IMPLEMENTATION_STARTED=false" in source
    assert "MILESTONE_26_TASK_1_NEXT_STAGE=MILESTONE_26_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1" in source


def test_task_2_scope_lock_contract() -> None:
    lock = build_milestone_26_objective_scope_lock()
    assert lock.valid is True
    assert lock.lock_ok is True
    assert lock.selected_objective_id == "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_ARCHIVE_INDEX_LOCAL_ONLY"
    assert lock.current_task_number == 2
    assert lock.task_budget_max == 8
    assert lock.remaining_budget_after_current_task == 6
    assert validate_milestone_26_objective_scope_lock(lock) == ()


def test_task_2_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_26_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert "MILESTONE_26_TASK_2_SELECTED_OBJECTIVE_ID=CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_ARCHIVE_INDEX_LOCAL_ONLY" in text
    assert "MILESTONE_26_TASK_2_SCOPE_LOCKED=true" in text
    assert "MILESTONE_26_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in text
    assert "MILESTONE_26_TASK_2_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_26_TASK_2_ALLOWED_OPERATION_COUNT=4" in text
    assert "MILESTONE_26_TASK_2_FORBIDDEN_OPERATION_COUNT=9" in text
    assert "MILESTONE_26_TASK_2_CURRENT_TASK_NUMBER=2" in text
    assert "MILESTONE_26_TASK_2_FAST_SOURCE_OPENING_SNAPSHOT=true" in text
    assert "MILESTONE_26_TASK_2_NEXT_STAGE=MILESTONE_26_TASK_3_ARCHIVE_INDEX_IMPLEMENTATION_V1" in text


def test_task_2_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    report = json.loads(REPORT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_26_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert manifest["selectedObjectiveId"] == "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_ARCHIVE_INDEX_LOCAL_ONLY"
    assert manifest["objectiveSelected"] is True
    assert manifest["scopeLocked"] is True
    assert manifest["implementationAllowedNext"] is True
    assert manifest["implementationStarted"] is False
    assert manifest["allowedOperationCount"] == 4
    assert manifest["forbiddenOperationCount"] == 9
    assert manifest["nextStage"] == "MILESTONE_26_TASK_3_ARCHIVE_INDEX_IMPLEMENTATION_V1"

    assert report["valid"] is True
    assert report["lockOk"] is True
    assert report["issues"] == []
