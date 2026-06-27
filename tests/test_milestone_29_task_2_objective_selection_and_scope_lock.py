import json
from pathlib import Path

from hbce_arc_agi3.milestone_29_objective_scope_lock import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    SCOPE_LOCK_ID,
    SCOPE_LOCK_REVISION,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_2_signature,
    validate_objective_scope_lock_report,
)


DOC_PATH = Path("docs/milestone-29-task-2-objective-selection-and-scope-lock-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-29-task-1-governed-opening-with-task-budget-v1.md")
ARTIFACT_DIR = Path("examples/milestone-29/objective-selection-and-scope-lock-v1")


def test_task_2_doc_declares_milestone_29_scope_lock_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_29_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert f"MILESTONE_29_TASK_2_SOURCE_TASK_ID={SOURCE_TASK_ID}" in text
    assert f"MILESTONE_29_TASK_2_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_29_TASK_2_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_29_TASK_2_SCOPE_LOCK_REVISION={SCOPE_LOCK_REVISION}" in text
    assert "MILESTONE_29_TASK_2_OBJECTIVE_SELECTION_READY=true" in text
    assert "MILESTONE_29_TASK_2_SCOPE_LOCKED=true" in text
    assert "MILESTONE_29_TASK_2_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_29_TASK_2_IMPLEMENTATION_ALLOWED_AT_TASK_2=false" in text
    assert "MILESTONE_29_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in text
    assert "MILESTONE_29_TASK_2_LOCAL_ONLY=true" in text
    assert "MILESTONE_29_TASK_2_NETWORK_ACCESS_ALLOWED=false" in text
    assert "MILESTONE_29_TASK_2_SHELL_EXECUTION_ALLOWED=false" in text
    assert "MILESTONE_29_TASK_2_ALLOWED_INPUT_COUNT=6" in text
    assert "MILESTONE_29_TASK_2_FORBIDDEN_OPERATION_COUNT=8" in text
    assert f"MILESTONE_29_TASK_2_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_29_TASK_2_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_29_TASK_2_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert f"MILESTONE_29_TASK_2_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_2_dependency_keeps_milestone_29_task_1_opening_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_29_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in text
    assert "MILESTONE_29_TASK_1_OPENING_STATUS=OPEN" in text
    assert "MILESTONE_29_TASK_1_TECHNICAL_STATUS=PASS" in text
    assert "MILESTONE_29_TASK_1_PROCESS_STATUS=GOVERNED_OPENING_WITH_TASK_BUDGET_MAX_8" in text
    assert "MILESTONE_29_TASK_1_SOURCE_DEPENDENCY_VALID=true" in text
    assert "MILESTONE_29_TASK_1_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_29_TASK_1_IMPLEMENTATION_ALLOWED_AT_TASK_1=false" in text
    assert "MILESTONE_29_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT=true" in text
    assert "MILESTONE_29_TASK_1_SCOPE_LOCK_REQUIRED_NEXT=true" in text
    assert "MILESTONE_29_TASK_1_NEXT_STAGE=MILESTONE_29_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1" in text


def test_task_2_persisted_objective_scope_lock_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-2-objective-scope-lock.json").read_text(encoding="utf-8"))

    assert validate_objective_scope_lock_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["scope_lock_revision"] == SCOPE_LOCK_REVISION
    assert report["task_2_signature"] == task_2_signature()
    assert report["objective_selection_ready"] is True
    assert report["scope_locked"] is True
    assert report["implementation_started"] is False
    assert report["implementation_allowed_at_task_2"] is False
    assert report["implementation_allowed_next"] is True
    assert report["scope_guard"]["local_only"] is True
    assert report["scope_guard"]["network_access_allowed"] is False
    assert report["scope_guard"]["shell_execution_allowed"] is False
    assert report["next_stage"] == NEXT_STAGE


def test_task_2_persisted_manifest_and_candidates_match_report():
    report = json.loads((ARTIFACT_DIR / "task-2-objective-scope-lock.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-2-manifest.json").read_text(encoding="utf-8"))
    candidates = json.loads((ARTIFACT_DIR / "task-2-objective-candidates.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["selected_objective_id"] == report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert manifest["scope_lock_id"] == report["scope_lock_id"] == SCOPE_LOCK_ID
    assert manifest["scope_lock_signature"] == report["scope_lock_signature"]
    assert manifest["objective_selection_ready"] is True
    assert manifest["scope_locked"] is True
    assert manifest["implementation_allowed_next"] is True
    assert manifest["generated_artifact_count"] == 5
    assert candidates["task_id"] == TASK_ID
    assert len(candidates["candidates"]) == 4
    assert len([candidate for candidate in candidates["candidates"] if candidate["selected"]]) == 1


def test_task_2_index_contains_canonical_scope_lock_markers():
    index = (ARTIFACT_DIR / "task-2-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_29_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in index
    assert f"SOURCE_TASK_ID={SOURCE_TASK_ID}" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert "OBJECTIVE_SELECTION_READY=true" in index
    assert "SCOPE_LOCKED=true" in index
    assert "IMPLEMENTATION_STARTED=false" in index
    assert "IMPLEMENTATION_ALLOWED_AT_TASK_2=false" in index
    assert "IMPLEMENTATION_ALLOWED_NEXT=true" in index
    assert "LOCAL_ONLY=true" in index
    assert "NETWORK_ACCESS_ALLOWED=false" in index
    assert "SHELL_EXECUTION_ALLOWED=false" in index
    assert "REPOSITORY_MUTATION_ALLOWED=false" in index
    assert "REMOTE_REGISTRY_LOOKUP_ALLOWED=false" in index
    assert "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in index
    assert "EXTERNAL_MODEL_CALL_ALLOWED=false" in index
    assert "ALLOWED_INPUT_COUNT=6" in index
    assert "FORBIDDEN_OPERATION_COUNT=8" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
