import json
from pathlib import Path

from hbce_arc_agi3.milestone_31_verified_operator_session_gate import (
    GENERATED_ARTIFACT_COUNT,
    IMPLEMENTATION_REVISION,
    NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SESSION_CASE_COUNT,
    SESSION_GATE_MODE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_3_signature,
    validate_verified_operator_session_gate_implementation_report,
)


DOC_PATH = Path("docs/milestone-31-task-3-verified-operator-authorization-session-gate-implementation-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-31-task-2-objective-selection-and-scope-lock-v1.md")
ARTIFACT_DIR = Path("examples/milestone-31/verified-operator-authorization-session-gate-implementation-v1")


def test_task_3_doc_declares_verified_operator_session_gate_implementation_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_31_TASK_3_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_IMPLEMENTATION_READY=true" in text
    assert f"MILESTONE_31_TASK_3_TASK_ID={TASK_ID}" in text
    assert f"MILESTONE_31_TASK_3_SOURCE_TASK_ID={SOURCE_TASK_ID}" in text
    assert f"MILESTONE_31_TASK_3_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_31_TASK_3_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_31_TASK_3_IMPLEMENTATION_REVISION={IMPLEMENTATION_REVISION}" in text
    assert "MILESTONE_31_TASK_3_SOURCE_DEPENDENCY_VALID=true" in text
    assert "MILESTONE_31_TASK_3_SCOPE_RULES_VALID=true" in text
    assert "MILESTONE_31_TASK_3_IMPLEMENTATION_STATUS=READY" in text
    assert "MILESTONE_31_TASK_3_IMPLEMENTATION_STARTED=true" in text
    assert "MILESTONE_31_TASK_3_IMPLEMENTATION_COMPLETE=true" in text
    assert f"MILESTONE_31_TASK_3_SESSION_GATE_MODE_ID={SESSION_GATE_MODE_ID}" in text
    assert f"MILESTONE_31_TASK_3_SESSION_CASE_COUNT={SESSION_CASE_COUNT}" in text
    assert "MILESTONE_31_TASK_3_PASS_COUNT=9" in text
    assert "MILESTONE_31_TASK_3_FAIL_COUNT=0" in text
    assert "MILESTONE_31_TASK_3_RUNTIME_CASES_VALID=true" in text
    assert "MILESTONE_31_TASK_3_PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_3_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_3_EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_3_SESSION_AUTHORIZATION_WITHOUT_VALID_AUTHORIZATION_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_3_SESSION_AUTHORIZATION_WITHOUT_CONTEXT_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_3_SESSION_AUTHORIZATION_WITHOUT_VERIFICATION_ALLOWED=false" in text
    assert f"MILESTONE_31_TASK_3_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_31_TASK_3_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_31_TASK_3_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_3_dependency_keeps_task_2_scope_lock_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_31_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert f"MILESTONE_31_TASK_2_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert "MILESTONE_31_TASK_2_SELECTED_OBJECTIVE_STATUS=SELECTED_AND_SCOPE_LOCKED" in text
    assert f"MILESTONE_31_TASK_2_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert "MILESTONE_31_TASK_2_SCOPE_LOCKED=true" in text
    assert "MILESTONE_31_TASK_2_SCOPE_RULES_VALID=true" in text
    assert f"MILESTONE_31_TASK_2_SESSION_GATE_MODE_ID={SESSION_GATE_MODE_ID}" in text
    assert "MILESTONE_31_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in text
    assert "MILESTONE_31_TASK_2_PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_2_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_2_EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_2_NEXT_STAGE=MILESTONE_31_TASK_3_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_IMPLEMENTATION_V1" in text


def test_task_3_persisted_session_gate_implementation_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-3-session-gate-implementation.json").read_text(encoding="utf-8"))

    assert validate_verified_operator_session_gate_implementation_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["implementation_revision"] == IMPLEMENTATION_REVISION
    assert report["task_3_signature"] == task_3_signature()
    assert report["implementation_status"] == "READY"
    assert report["implementation_started"] is True
    assert report["implementation_complete"] is True
    assert report["session_gate_mode_id"] == SESSION_GATE_MODE_ID
    assert report["session_case_count"] == SESSION_CASE_COUNT
    assert report["pass_count"] == 9
    assert report["fail_count"] == 0
    assert report["runtime_cases_valid"] is True
    assert report["next_stage"] == NEXT_STAGE


def test_task_3_persisted_manifest_cases_and_matrix_match_report():
    report = json.loads((ARTIFACT_DIR / "task-3-session-gate-implementation.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-3-manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((ARTIFACT_DIR / "task-3-runtime-cases.json").read_text(encoding="utf-8"))
    matrix = json.loads((ARTIFACT_DIR / "task-3-decision-matrix.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["source_task_id"] == SOURCE_TASK_ID
    assert manifest["implementation_id"] == report["implementation_id"]
    assert manifest["implementation_signature"] == report["implementation_signature"]
    assert manifest["implementation_status"] == "READY"
    assert manifest["implementation_started"] is True
    assert manifest["implementation_complete"] is True
    assert cases["task_id"] == TASK_ID
    assert cases["implementation_id"] == report["implementation_id"]
    assert cases["session_case_count"] == SESSION_CASE_COUNT
    assert cases["pass_count"] == 9
    assert cases["fail_count"] == 0
    assert matrix["task_id"] == TASK_ID
    assert matrix["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert matrix["scope_lock_id"] == SCOPE_LOCK_ID
    assert matrix["session_gate_mode_id"] == SESSION_GATE_MODE_ID
    assert matrix["hard_denials"]["private_core_access_without_verified_manuel_allowed"] is False
    assert matrix["hard_denials"]["unverified_manuel_assumption_allowed"] is False
    assert matrix["hard_denials"]["external_command_authority_allowed"] is False


def test_task_3_index_contains_canonical_implementation_markers():
    index = (ARTIFACT_DIR / "task-3-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_31_TASK_3_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_IMPLEMENTATION_READY=true" in index
    assert f"TASK_ID={TASK_ID}" in index
    assert f"SOURCE_TASK_ID={SOURCE_TASK_ID}" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert f"IMPLEMENTATION_REVISION={IMPLEMENTATION_REVISION}" in index
    assert "SOURCE_DEPENDENCY_VALID=true" in index
    assert "SCOPE_RULES_VALID=true" in index
    assert "IMPLEMENTATION_STATUS=READY" in index
    assert "IMPLEMENTATION_STARTED=true" in index
    assert "IMPLEMENTATION_COMPLETE=true" in index
    assert f"SESSION_GATE_MODE_ID={SESSION_GATE_MODE_ID}" in index
    assert "SESSION_CASE_COUNT=9" in index
    assert "PASS_COUNT=9" in index
    assert "FAIL_COUNT=0" in index
    assert "RUNTIME_CASES_VALID=true" in index
    assert "PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED=false" in index
    assert "UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in index
    assert "EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in index
    assert "SESSION_AUTHORIZATION_WITHOUT_VALID_AUTHORIZATION_ALLOWED=false" in index
    assert "SESSION_AUTHORIZATION_WITHOUT_CONTEXT_ALLOWED=false" in index
    assert "SESSION_AUTHORIZATION_WITHOUT_VERIFICATION_ALLOWED=false" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
