import json
from pathlib import Path

from hbce_arc_agi3.milestone_30_identity_boundary_fail_closed import (
    GENERATED_ARTIFACT_COUNT,
    IMPLEMENTATION_REVISION,
    NEXT_STAGE,
    PRIVATE_MODE_ID,
    PUBLIC_MODE_ID,
    RUNTIME_CASE_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_3_signature,
    validate_identity_boundary_implementation_report,
)


DOC_PATH = Path("docs/milestone-30-task-3-identity-boundary-fail-closed-implementation-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-30-task-2-objective-selection-and-scope-lock-v1.md")
ARTIFACT_DIR = Path("examples/milestone-30/identity-boundary-fail-closed-implementation-v1")


def test_task_3_doc_declares_identity_boundary_implementation_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_30_TASK_3_IDENTITY_BOUNDARY_FAIL_CLOSED_IMPLEMENTATION_READY=true" in text
    assert f"MILESTONE_30_TASK_3_SOURCE_TASK_ID={SOURCE_TASK_ID}" in text
    assert f"MILESTONE_30_TASK_3_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_30_TASK_3_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_30_TASK_3_IMPLEMENTATION_REVISION={IMPLEMENTATION_REVISION}" in text
    assert "MILESTONE_30_TASK_3_IMPLEMENTATION_STATUS=READY" in text
    assert "MILESTONE_30_TASK_3_IMPLEMENTATION_STARTED=true" in text
    assert "MILESTONE_30_TASK_3_IMPLEMENTATION_COMPLETE=true" in text
    assert f"MILESTONE_30_TASK_3_RUNTIME_CASE_COUNT={RUNTIME_CASE_COUNT}" in text
    assert "MILESTONE_30_TASK_3_PASS_COUNT=8" in text
    assert "MILESTONE_30_TASK_3_FAIL_COUNT=0" in text
    assert "MILESTONE_30_TASK_3_RUNTIME_CASES_VALID=true" in text
    assert f"MILESTONE_30_TASK_3_PUBLIC_MODE_ID={PUBLIC_MODE_ID}" in text
    assert f"MILESTONE_30_TASK_3_PRIVATE_MODE_ID={PRIVATE_MODE_ID}" in text
    assert "MILESTONE_30_TASK_3_PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL=false" in text
    assert "MILESTONE_30_TASK_3_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in text
    assert "MILESTONE_30_TASK_3_EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in text
    assert f"MILESTONE_30_TASK_3_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_30_TASK_3_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_30_TASK_3_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_3_dependency_keeps_task_2_scope_lock_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_30_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert f"MILESTONE_30_TASK_2_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_30_TASK_2_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert "MILESTONE_30_TASK_2_SCOPE_LOCKED=true" in text
    assert "MILESTONE_30_TASK_2_SCOPE_RULES_VALID=true" in text
    assert "MILESTONE_30_TASK_2_PUBLIC_MODE_ID=PUBLIC_LIMITED_VERIFYING" in text
    assert "MILESTONE_30_TASK_2_PRIVATE_MODE_ID=PRIVATE_VERIFIED_MANUEL_AUTHORIZED_SCOPE_ONLY" in text
    assert "MILESTONE_30_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in text
    assert "MILESTONE_30_TASK_2_PRIVATE_CORE_EXPOSURE_ALLOWED=false" in text
    assert "MILESTONE_30_TASK_2_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in text
    assert "MILESTONE_30_TASK_2_EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in text
    assert "MILESTONE_30_TASK_2_NEXT_STAGE=MILESTONE_30_TASK_3_IDENTITY_BOUNDARY_FAIL_CLOSED_IMPLEMENTATION_V1" in text


def test_task_3_persisted_identity_boundary_implementation_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-3-identity-boundary-implementation.json").read_text(encoding="utf-8"))

    assert validate_identity_boundary_implementation_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["implementation_revision"] == IMPLEMENTATION_REVISION
    assert report["task_3_signature"] == task_3_signature()
    assert report["implementation_status"] == "READY"
    assert report["implementation_started"] is True
    assert report["implementation_complete"] is True
    assert report["runtime_case_count"] == RUNTIME_CASE_COUNT
    assert report["pass_count"] == 8
    assert report["fail_count"] == 0
    assert report["runtime_cases_valid"] is True
    assert report["private_core_access_allowed_without_verified_manuel"] is False
    assert report["unverified_manuel_assumption_allowed"] is False
    assert report["external_command_authority_allowed"] is False
    assert report["next_stage"] == NEXT_STAGE


def test_task_3_persisted_manifest_cases_and_matrix_match_report():
    report = json.loads((ARTIFACT_DIR / "task-3-identity-boundary-implementation.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-3-manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((ARTIFACT_DIR / "task-3-runtime-cases.json").read_text(encoding="utf-8"))
    matrix = json.loads((ARTIFACT_DIR / "task-3-decision-matrix.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["implementation_id"] == report["implementation_id"]
    assert manifest["implementation_signature"] == report["implementation_signature"]
    assert manifest["implementation_status"] == "READY"
    assert manifest["runtime_cases_valid"] is True
    assert cases["implementation_id"] == report["implementation_id"]
    assert cases["runtime_case_count"] == report["runtime_case_count"]
    assert cases["pass_count"] == report["pass_count"]
    assert cases["fail_count"] == report["fail_count"]
    assert matrix["task_id"] == TASK_ID
    assert matrix["scope_lock_id"] == SCOPE_LOCK_ID
    assert matrix["public_mode_id"] == PUBLIC_MODE_ID
    assert matrix["private_mode_id"] == PRIVATE_MODE_ID
    assert matrix["hard_denials"]["private_core_access_allowed_without_verified_manuel"] is False
    assert matrix["hard_denials"]["unverified_manuel_assumption_allowed"] is False
    assert matrix["hard_denials"]["external_command_authority_allowed"] is False


def test_task_3_index_contains_canonical_identity_boundary_markers():
    index = (ARTIFACT_DIR / "task-3-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_30_TASK_3_IDENTITY_BOUNDARY_FAIL_CLOSED_IMPLEMENTATION_READY=true" in index
    assert f"SOURCE_TASK_ID={SOURCE_TASK_ID}" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert f"IMPLEMENTATION_REVISION={IMPLEMENTATION_REVISION}" in index
    assert "IMPLEMENTATION_STATUS=READY" in index
    assert "IMPLEMENTATION_STARTED=true" in index
    assert "IMPLEMENTATION_COMPLETE=true" in index
    assert "RUNTIME_CASE_COUNT=8" in index
    assert "PASS_COUNT=8" in index
    assert "FAIL_COUNT=0" in index
    assert "RUNTIME_CASES_VALID=true" in index
    assert f"PUBLIC_MODE_ID={PUBLIC_MODE_ID}" in index
    assert f"PRIVATE_MODE_ID={PRIVATE_MODE_ID}" in index
    assert "PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL=false" in index
    assert "UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in index
    assert "EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
