import json
from pathlib import Path

from hbce_arc_agi3.milestone_30_objective_scope_lock import (
    CURRENT_TASK_NUMBER,
    FORBIDDEN_OPERATION_COUNT,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    PUBLIC_MODE_ID,
    PRIVATE_MODE_ID,
    SCOPE_LOCK_ID,
    SCOPE_LOCK_REVISION,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_2_signature,
    validate_objective_scope_lock_report,
)


DOC_PATH = Path("docs/milestone-30-task-2-objective-selection-and-scope-lock-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-30-task-1-governed-opening-with-task-budget-v1.md")
ARTIFACT_DIR = Path("examples/milestone-30/objective-selection-and-scope-lock-v1")


def test_task_2_doc_declares_objective_selection_and_scope_lock_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_30_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert f"MILESTONE_30_TASK_2_SOURCE_TASK_ID={SOURCE_TASK_ID}" in text
    assert f"MILESTONE_30_TASK_2_SCOPE_LOCK_REVISION={SCOPE_LOCK_REVISION}" in text
    assert f"MILESTONE_30_TASK_2_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_30_TASK_2_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert "MILESTONE_30_TASK_2_OBJECTIVE_SELECTION_READY=true" in text
    assert "MILESTONE_30_TASK_2_SCOPE_LOCKED=true" in text
    assert "MILESTONE_30_TASK_2_SOURCE_DEPENDENCY_VALID=true" in text
    assert "MILESTONE_30_TASK_2_SCOPE_RULES_VALID=true" in text
    assert f"MILESTONE_30_TASK_2_PUBLIC_MODE_ID={PUBLIC_MODE_ID}" in text
    assert f"MILESTONE_30_TASK_2_PRIVATE_MODE_ID={PRIVATE_MODE_ID}" in text
    assert "MILESTONE_30_TASK_2_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_30_TASK_2_IMPLEMENTATION_ALLOWED_AT_TASK_2=false" in text
    assert "MILESTONE_30_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in text
    assert "MILESTONE_30_TASK_2_LOCAL_ONLY=true" in text
    assert "MILESTONE_30_TASK_2_NETWORK_ACCESS_ALLOWED=false" in text
    assert "MILESTONE_30_TASK_2_SHELL_EXECUTION_ALLOWED=false" in text
    assert "MILESTONE_30_TASK_2_PRIVATE_CORE_EXPOSURE_ALLOWED=false" in text
    assert "MILESTONE_30_TASK_2_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in text
    assert "MILESTONE_30_TASK_2_EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in text
    assert f"MILESTONE_30_TASK_2_FORBIDDEN_OPERATION_COUNT={FORBIDDEN_OPERATION_COUNT}" in text
    assert f"MILESTONE_30_TASK_2_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_30_TASK_2_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert f"MILESTONE_30_TASK_2_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_30_TASK_2_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_2_dependency_keeps_task_1_opening_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_30_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in text
    assert "MILESTONE_30_TASK_1_OPENING_STATUS=OPEN" in text
    assert "MILESTONE_30_TASK_1_TECHNICAL_STATUS=PASS" in text
    assert "MILESTONE_30_TASK_1_SOURCE_DEPENDENCY_VALID=true" in text
    assert "MILESTONE_30_TASK_1_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_30_TASK_1_IMPLEMENTATION_ALLOWED_AT_TASK_1=false" in text
    assert "MILESTONE_30_TASK_1_PROPOSED_OPERATOR_SEED_ID=JOKER_C2_IDENTITY_BOUNDARY_AND_FAIL_CLOSED_PUBLIC_MODE" in text
    assert "MILESTONE_30_TASK_1_PROPOSED_OPERATOR_SEED_STATUS=CANDIDATE_ONLY_NOT_LOCKED" in text
    assert "MILESTONE_30_TASK_1_NEXT_STAGE=MILESTONE_30_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1" in text


def test_task_2_persisted_scope_lock_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-2-objective-scope-lock.json").read_text(encoding="utf-8"))

    assert validate_objective_scope_lock_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["scope_lock_revision"] == SCOPE_LOCK_REVISION
    assert report["task_2_signature"] == task_2_signature()
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["objective_selection_ready"] is True
    assert report["scope_locked"] is True
    assert report["scope_rules_valid"] is True
    assert report["implementation_started"] is False
    assert report["implementation_allowed_at_task_2"] is False
    assert report["implementation_allowed_next"] is True
    assert report["private_core_exposure_allowed"] is False
    assert report["unverified_manuel_assumption_allowed"] is False
    assert report["external_command_authority_allowed"] is False
    assert report["next_stage"] == NEXT_STAGE


def test_task_2_persisted_manifest_and_policy_matrix_match_report():
    report = json.loads((ARTIFACT_DIR / "task-2-objective-scope-lock.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-2-manifest.json").read_text(encoding="utf-8"))
    matrix = json.loads((ARTIFACT_DIR / "task-2-policy-matrix.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["scope_lock_artifact_id"] == report["scope_lock_artifact_id"]
    assert manifest["scope_lock_signature"] == report["scope_lock_signature"]
    assert manifest["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert manifest["scope_lock_id"] == SCOPE_LOCK_ID
    assert manifest["scope_locked"] is True
    assert manifest["scope_rules_valid"] is True
    assert matrix["task_id"] == TASK_ID
    assert matrix["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert matrix["scope_lock_id"] == SCOPE_LOCK_ID
    assert matrix["runtime_modes"]["public_mode_id"] == PUBLIC_MODE_ID
    assert matrix["runtime_modes"]["private_mode_id"] == PRIVATE_MODE_ID
    assert matrix["guardrails"]["private_core_exposure_allowed"] is False
    assert matrix["guardrails"]["unverified_manuel_assumption_allowed"] is False
    assert matrix["guardrails"]["external_command_authority_allowed"] is False


def test_task_2_index_contains_canonical_scope_lock_markers():
    index = (ARTIFACT_DIR / "task-2-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_30_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in index
    assert f"SOURCE_TASK_ID={SOURCE_TASK_ID}" in index
    assert f"SCOPE_LOCK_REVISION={SCOPE_LOCK_REVISION}" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert "OBJECTIVE_SELECTION_READY=true" in index
    assert "SCOPE_LOCKED=true" in index
    assert "SOURCE_DEPENDENCY_VALID=true" in index
    assert "OPERATOR_SEED_STATUS_AFTER_LOCK=SELECTED_AND_SCOPE_LOCKED" in index
    assert "SCOPE_RULES_VALID=true" in index
    assert f"PUBLIC_MODE_ID={PUBLIC_MODE_ID}" in index
    assert f"PRIVATE_MODE_ID={PRIVATE_MODE_ID}" in index
    assert "IMPLEMENTATION_STARTED=false" in index
    assert "IMPLEMENTATION_ALLOWED_AT_TASK_2=false" in index
    assert "IMPLEMENTATION_ALLOWED_NEXT=true" in index
    assert "LOCAL_ONLY=true" in index
    assert "NETWORK_ACCESS_ALLOWED=false" in index
    assert "SHELL_EXECUTION_ALLOWED=false" in index
    assert "PRIVATE_CORE_EXPOSURE_ALLOWED=false" in index
    assert "UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in index
    assert "EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
