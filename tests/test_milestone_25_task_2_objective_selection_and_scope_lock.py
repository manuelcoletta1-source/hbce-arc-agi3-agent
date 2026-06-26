"""Milestone #25 Task 2 objective selection and scope lock validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_25_objective_scope_lock import (
    build_milestone_25_objective_scope_lock,
    validate_milestone_25_objective_scope_lock,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "milestone-25-task-2-objective-selection-and-scope-lock-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_25_objective_scope_lock.py"
MANIFEST = ROOT / "examples" / "milestone-25" / "objective-selection-and-scope-lock-v1" / "task-2-manifest.json"
JSON_ARTIFACT = ROOT / "examples" / "milestone-25" / "objective-selection-and-scope-lock-v1" / "task-2-objective-scope-lock.json"
SOURCE_DOC = ROOT / "docs" / "milestone-25-task-1-governed-opening-with-task-budget-v1.md"


def test_task_2_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MANIFEST.exists()
    assert JSON_ARTIFACT.exists()
    assert SOURCE_DOC.exists()


def test_task_2_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")
    assert "MILESTONE_25_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in source
    assert "MILESTONE_25_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT=true" in source
    assert "MILESTONE_25_TASK_1_SCOPE_LOCK_REQUIRED_NEXT=true" in source
    assert "MILESTONE_25_TASK_1_IMPLEMENTATION_STARTED=false" in source
    assert "MILESTONE_25_TASK_1_NEXT_STAGE=MILESTONE_25_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1" in source


def test_task_2_lock_contract() -> None:
    lock = build_milestone_25_objective_scope_lock()
    assert lock.valid is True
    assert lock.lock_ok is True
    assert lock.selected_objective_id == "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"
    assert lock.scope_lock_id == "MILESTONE_25_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"
    assert lock.current_task_number == 2
    assert lock.task_budget_max == 8
    assert lock.remaining_budget_after_current_task == 6
    assert validate_milestone_25_objective_scope_lock(lock) == ()


def test_task_2_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_25_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert "MILESTONE_25_TASK_2_SELECTED_OBJECTIVE_ID=CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY" in text
    assert "MILESTONE_25_TASK_2_SCOPE_LOCK_ID=MILESTONE_25_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY" in text
    assert "MILESTONE_25_TASK_2_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_25_TASK_2_CURRENT_TASK_NUMBER=2" in text
    assert "MILESTONE_25_TASK_2_OBJECTIVE_SELECTED=true" in text
    assert "MILESTONE_25_TASK_2_SCOPE_LOCKED=true" in text
    assert "MILESTONE_25_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in text
    assert "MILESTONE_25_TASK_2_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_25_TASK_2_FAST_SOURCE_OPENING_SNAPSHOT=true" in text
    assert "MILESTONE_25_TASK_2_NEXT_STAGE=MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_IMPLEMENTATION_V1" in text


def test_task_2_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_25_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert manifest["selectedObjectiveId"] == "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"
    assert manifest["scopeLockId"] == "MILESTONE_25_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"
    assert manifest["objectiveSelected"] is True
    assert manifest["scopeLocked"] is True
    assert manifest["implementationStarted"] is False
    assert artifact["valid"] is True
    assert artifact["lockOk"] is True
    assert artifact["issues"] == []
