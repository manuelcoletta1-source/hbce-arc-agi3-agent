"""Milestone #27 Task 2 objective selection and scope lock validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_27_objective_scope_lock import (
    build_milestone_27_objective_scope_lock,
    validate_milestone_27_objective_scope_lock,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "milestone-27-task-2-objective-selection-and-scope-lock-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_27_objective_scope_lock.py"
REPORT = ROOT / "examples" / "milestone-27" / "objective-selection-and-scope-lock-v1" / "task-2-objective-scope-lock.json"
MANIFEST = ROOT / "examples" / "milestone-27" / "objective-selection-and-scope-lock-v1" / "task-2-manifest.json"
SOURCE_DOC = ROOT / "docs" / "milestone-27-task-1-governed-opening-with-task-budget-v1.md"


def test_task_2_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert REPORT.exists()
    assert MANIFEST.exists()
    assert SOURCE_DOC.exists()


def test_task_2_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")
    assert "MILESTONE_27_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in source
    assert "MILESTONE_27_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT=true" in source
    assert "MILESTONE_27_TASK_1_SCOPE_LOCK_REQUIRED_NEXT=true" in source
    assert "MILESTONE_27_TASK_1_IMPLEMENTATION_STARTED=false" in source
    assert "MILESTONE_27_TASK_1_IMPLEMENTATION_ALLOWED_AT_TASK_1=false" in source
    assert "MILESTONE_27_TASK_1_NEXT_STAGE=MILESTONE_27_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1" in source


def test_task_2_scope_lock_contract() -> None:
    lock = build_milestone_27_objective_scope_lock()
    assert lock.valid is True
    assert lock.lock_ok is True
    assert lock.selected_objective_id == "CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_INTERFACE_LOCAL_ONLY"
    assert lock.scope_lock_id == "MILESTONE_27_SCOPE_CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_INTERFACE_LOCAL_ONLY"
    assert lock.current_task_number == 2
    assert lock.task_budget_max == 8
    assert lock.remaining_budget_after_current_task == 6
    assert len(lock.allowed_operations) == 4
    assert len(lock.forbidden_operations) == 9
    assert len(lock.scope_checks) == 13
    assert len(lock.generated_artifacts) == 4
    assert validate_milestone_27_objective_scope_lock(lock) == ()


def test_task_2_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_27_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert "MILESTONE_27_TASK_2_SELECTED_OBJECTIVE_ID=CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_INTERFACE_LOCAL_ONLY" in text
    assert "MILESTONE_27_TASK_2_SCOPE_LOCK_ID=MILESTONE_27_SCOPE_CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_INTERFACE_LOCAL_ONLY" in text
    assert "MILESTONE_27_TASK_2_OBJECTIVE_SELECTED=true" in text
    assert "MILESTONE_27_TASK_2_SCOPE_LOCKED=true" in text
    assert "MILESTONE_27_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in text
    assert "MILESTONE_27_TASK_2_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_27_TASK_2_QUERY_INTERFACE_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_27_TASK_2_CURRENT_TASK_NUMBER=2" in text
    assert "MILESTONE_27_TASK_2_ALLOWED_OPERATION_COUNT=4" in text
    assert "MILESTONE_27_TASK_2_FORBIDDEN_OPERATION_COUNT=9" in text
    assert "MILESTONE_27_TASK_2_SCOPE_CHECK_COUNT=13" in text
    assert "MILESTONE_27_TASK_2_FAST_SOURCE_OPENING_SNAPSHOT=true" in text
    assert "MILESTONE_27_TASK_2_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in text
    assert "MILESTONE_27_TASK_2_NEXT_STAGE=MILESTONE_27_TASK_3_QUERY_INTERFACE_IMPLEMENTATION_V1" in text


def test_task_2_artifacts() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert report["valid"] is True
    assert report["lockOk"] is True
    assert report["issues"] == []
    assert report["selectedObjectiveId"] == "CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_INTERFACE_LOCAL_ONLY"
    assert report["scopeLockId"] == "MILESTONE_27_SCOPE_CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_INTERFACE_LOCAL_ONLY"
    assert report["objectiveSelected"] is True
    assert report["scopeLocked"] is True
    assert report["implementationAllowedNext"] is True
    assert report["implementationStarted"] is False
    assert report["queryInterfaceImplementationStarted"] is False
    assert report["nextStage"] == "MILESTONE_27_TASK_3_QUERY_INTERFACE_IMPLEMENTATION_V1"

    assert manifest["taskId"] == "MILESTONE_27_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert manifest["selectedObjectiveId"] == "CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_INTERFACE_LOCAL_ONLY"
    assert manifest["scopeLocked"] is True
    assert manifest["implementationAllowedNext"] is True
    assert manifest["nextStage"] == "MILESTONE_27_TASK_3_QUERY_INTERFACE_IMPLEMENTATION_V1"
