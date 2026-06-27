import json
from pathlib import Path

from hbce_arc_agi3.milestone_28_objective_scope_lock import (
    CURRENT_TASK_NUMBER,
    NEXT_STAGE,
    OBJECTIVE_SELECTION_REVISION,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_2_signature,
    validate_objective_scope_lock_report,
)


DOC_PATH = Path("docs/milestone-28-task-2-objective-selection-and-scope-lock-v1.md")
SOURCE_TASK_1_DOC_PATH = Path("docs/milestone-28-task-1-governed-opening-with-task-budget-v1.md")
ARTIFACT_DIR = Path("examples/milestone-28/objective-selection-and-scope-lock-v1")


def test_task_2_doc_declares_objective_selection_and_scope_lock_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_28_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert f"MILESTONE_28_TASK_2_SOURCE_TASK_ID={SOURCE_TASK_ID}" in text
    assert f"MILESTONE_28_TASK_2_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_28_TASK_2_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_28_TASK_2_OBJECTIVE_SELECTION_REVISION={OBJECTIVE_SELECTION_REVISION}" in text
    assert "MILESTONE_28_TASK_2_OBJECTIVE_SELECTION_READY=true" in text
    assert "MILESTONE_28_TASK_2_SCOPE_LOCKED=true" in text
    assert "MILESTONE_28_TASK_2_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_28_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in text
    assert "MILESTONE_28_TASK_2_IMPLEMENTATION_ALLOWED_AT_TASK_2=false" in text
    assert "MILESTONE_28_TASK_2_LOCAL_ONLY=true" in text
    assert "MILESTONE_28_TASK_2_NETWORK_ACCESS_ALLOWED=false" in text
    assert "MILESTONE_28_TASK_2_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in text
    assert f"MILESTONE_28_TASK_2_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_28_TASK_2_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert f"MILESTONE_28_TASK_2_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_2_dependency_keeps_task_1_governed_opening_intact():
    text = SOURCE_TASK_1_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_28_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in text
    assert "MILESTONE_28_TASK_1_OPENING_STATUS=OPEN" in text
    assert "MILESTONE_28_TASK_1_TECHNICAL_STATUS=PASS" in text
    assert "MILESTONE_28_TASK_1_PROCESS_STATUS=GOVERNED_OPENING_WITH_TASK_BUDGET_MAX_8" in text
    assert "MILESTONE_28_TASK_1_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_28_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT=true" in text
    assert "MILESTONE_28_TASK_1_SCOPE_LOCK_REQUIRED_NEXT=true" in text
    assert "MILESTONE_28_TASK_1_NEXT_STAGE=MILESTONE_28_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1" in text


def test_task_2_persisted_scope_lock_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-2-objective-scope-lock.json").read_text(encoding="utf-8"))

    assert validate_objective_scope_lock_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["task_2_signature"] == task_2_signature()
    assert report["objective_selection_ready"] is True
    assert report["scope_locked"] is True
    assert report["implementation_allowed_next"] is True
    assert report["implementation_started"] is False
    assert report["next_stage"] == NEXT_STAGE


def test_task_2_persisted_manifest_and_candidates_match_report():
    report = json.loads((ARTIFACT_DIR / "task-2-objective-scope-lock.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-2-manifest.json").read_text(encoding="utf-8"))
    candidates = json.loads((ARTIFACT_DIR / "task-2-objective-candidates.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["scope_lock_artifact_id"] == report["scope_lock_artifact_id"]
    assert manifest["scope_lock_signature"] == report["scope_lock_signature"]
    assert manifest["scope_ready"] is True
    assert candidates["task_id"] == TASK_ID
    assert candidates["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert candidates["candidate_count"] == report["candidate_count"]
    assert len(candidates["objective_candidates"]) == report["candidate_count"]


def test_task_2_index_contains_canonical_scope_lock_markers():
    index = (ARTIFACT_DIR / "task-2-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_28_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert "OBJECTIVE_SELECTION_READY=true" in index
    assert "SCOPE_LOCKED=true" in index
    assert "IMPLEMENTATION_STARTED=false" in index
    assert "IMPLEMENTATION_ALLOWED_NEXT=true" in index
    assert "IMPLEMENTATION_ALLOWED_AT_TASK_2=false" in index
    assert "LOCAL_ONLY=true" in index
    assert "NETWORK_ACCESS_ALLOWED=false" in index
    assert "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in index
    assert "FORBIDDEN_OPERATION_COUNT=8" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
