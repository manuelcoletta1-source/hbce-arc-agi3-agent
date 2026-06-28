import json
from pathlib import Path

from hbce_arc_agi3.milestone_31_verified_operator_session_gate_validation import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SESSION_GATE_MODE_ID,
    SOURCE_SCOPE_TASK_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    VALIDATION_CASE_COUNT,
    VALIDATION_REVISION,
    task_4_signature,
    validate_verified_operator_session_gate_validation_report,
)


DOC_PATH = Path("docs/milestone-31-task-4-verified-operator-authorization-session-gate-validation-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-31-task-3-verified-operator-authorization-session-gate-implementation-v1.md")
ARTIFACT_DIR = Path("examples/milestone-31/verified-operator-authorization-session-gate-validation-v1")


def test_task_4_doc_declares_verified_operator_session_gate_validation_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_31_TASK_4_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_VALIDATION_READY=true" in text
    assert f"MILESTONE_31_TASK_4_TASK_ID={TASK_ID}" in text
    assert f"MILESTONE_31_TASK_4_SOURCE_TASK_ID={SOURCE_TASK_ID}" in text
    assert f"MILESTONE_31_TASK_4_SOURCE_SCOPE_TASK_ID={SOURCE_SCOPE_TASK_ID}" in text
    assert f"MILESTONE_31_TASK_4_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_31_TASK_4_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_31_TASK_4_VALIDATION_REVISION={VALIDATION_REVISION}" in text
    assert "MILESTONE_31_TASK_4_SOURCE_IMPLEMENTATION_STATUS=READY" in text
    assert "MILESTONE_31_TASK_4_SOURCE_IMPLEMENTATION_STARTED=true" in text
    assert "MILESTONE_31_TASK_4_SOURCE_IMPLEMENTATION_COMPLETE=true" in text
    assert f"MILESTONE_31_TASK_4_SOURCE_SESSION_GATE_MODE_ID={SESSION_GATE_MODE_ID}" in text
    assert "MILESTONE_31_TASK_4_SOURCE_SESSION_CASE_COUNT=9" in text
    assert "MILESTONE_31_TASK_4_SOURCE_RUNTIME_CASES_VALID=true" in text
    assert "MILESTONE_31_TASK_4_SOURCE_PASS_COUNT=9" in text
    assert "MILESTONE_31_TASK_4_SOURCE_FAIL_COUNT=0" in text
    assert "MILESTONE_31_TASK_4_SOURCE_PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_4_SOURCE_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_4_SOURCE_EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_4_SOURCE_SESSION_AUTHORIZATION_WITHOUT_VALID_AUTHORIZATION_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_4_SOURCE_SESSION_AUTHORIZATION_WITHOUT_CONTEXT_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_4_SOURCE_SESSION_AUTHORIZATION_WITHOUT_VERIFICATION_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_4_VALIDATION_STATUS=VALID" in text
    assert f"MILESTONE_31_TASK_4_VALIDATION_CASE_COUNT={VALIDATION_CASE_COUNT}" in text
    assert "MILESTONE_31_TASK_4_PASS_COUNT=10" in text
    assert "MILESTONE_31_TASK_4_FAIL_COUNT=0" in text
    assert "MILESTONE_31_TASK_4_VALIDATION_PASSED=true" in text
    assert f"MILESTONE_31_TASK_4_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_31_TASK_4_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert f"MILESTONE_31_TASK_4_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_31_TASK_4_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_4_dependency_keeps_task_3_session_gate_implementation_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_31_TASK_3_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_IMPLEMENTATION_READY=true" in text
    assert f"MILESTONE_31_TASK_3_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_31_TASK_3_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert "MILESTONE_31_TASK_3_IMPLEMENTATION_STATUS=READY" in text
    assert "MILESTONE_31_TASK_3_IMPLEMENTATION_STARTED=true" in text
    assert "MILESTONE_31_TASK_3_IMPLEMENTATION_COMPLETE=true" in text
    assert f"MILESTONE_31_TASK_3_SESSION_GATE_MODE_ID={SESSION_GATE_MODE_ID}" in text
    assert "MILESTONE_31_TASK_3_SESSION_CASE_COUNT=9" in text
    assert "MILESTONE_31_TASK_3_PASS_COUNT=9" in text
    assert "MILESTONE_31_TASK_3_FAIL_COUNT=0" in text
    assert "MILESTONE_31_TASK_3_RUNTIME_CASES_VALID=true" in text
    assert "MILESTONE_31_TASK_3_PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_3_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_3_EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_3_NEXT_STAGE=MILESTONE_31_TASK_4_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_VALIDATION_V1" in text


def test_task_4_persisted_session_gate_validation_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-4-validation-report.json").read_text(encoding="utf-8"))

    assert validate_verified_operator_session_gate_validation_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["source_scope_task_id"] == SOURCE_SCOPE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["validation_revision"] == VALIDATION_REVISION
    assert report["task_4_signature"] == task_4_signature()
    assert report["source_implementation_status"] == "READY"
    assert report["source_implementation_started"] is True
    assert report["source_implementation_complete"] is True
    assert report["source_session_gate_mode_id"] == SESSION_GATE_MODE_ID
    assert report["source_session_case_count"] == 9
    assert report["source_runtime_cases_valid"] is True
    assert report["validation_status"] == "VALID"
    assert report["validation_case_count"] == VALIDATION_CASE_COUNT
    assert report["pass_count"] == 10
    assert report["fail_count"] == 0
    assert report["validation_passed"] is True
    assert report["next_stage"] == NEXT_STAGE


def test_task_4_persisted_manifest_and_cases_match_report():
    report = json.loads((ARTIFACT_DIR / "task-4-validation-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-4-manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((ARTIFACT_DIR / "task-4-validation-cases.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["source_task_id"] == SOURCE_TASK_ID
    assert manifest["source_scope_task_id"] == SOURCE_SCOPE_TASK_ID
    assert manifest["validation_id"] == report["validation_id"]
    assert manifest["validation_signature"] == report["validation_signature"]
    assert manifest["source_implementation_id"] == report["source_implementation_id"]
    assert manifest["source_implementation_signature"] == report["source_implementation_signature"]
    assert manifest["validation_status"] == "VALID"
    assert manifest["validation_passed"] is True
    assert cases["task_id"] == TASK_ID
    assert cases["validation_id"] == report["validation_id"]
    assert cases["validation_status"] == "VALID"
    assert cases["validation_case_count"] == report["validation_case_count"]
    assert len(cases["validation_cases"]) == report["validation_case_count"]


def test_task_4_index_contains_canonical_validation_markers():
    index = (ARTIFACT_DIR / "task-4-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_31_TASK_4_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_VALIDATION_READY=true" in index
    assert f"TASK_ID={TASK_ID}" in index
    assert f"SOURCE_TASK_ID={SOURCE_TASK_ID}" in index
    assert f"SOURCE_SCOPE_TASK_ID={SOURCE_SCOPE_TASK_ID}" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert f"VALIDATION_REVISION={VALIDATION_REVISION}" in index
    assert "SOURCE_IMPLEMENTATION_STATUS=READY" in index
    assert "SOURCE_IMPLEMENTATION_STARTED=true" in index
    assert "SOURCE_IMPLEMENTATION_COMPLETE=true" in index
    assert f"SOURCE_SESSION_GATE_MODE_ID={SESSION_GATE_MODE_ID}" in index
    assert "SOURCE_SESSION_CASE_COUNT=9" in index
    assert "SOURCE_RUNTIME_CASES_VALID=true" in index
    assert "SOURCE_PASS_COUNT=9" in index
    assert "SOURCE_FAIL_COUNT=0" in index
    assert "SOURCE_PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED=false" in index
    assert "SOURCE_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in index
    assert "SOURCE_EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in index
    assert "SOURCE_SESSION_AUTHORIZATION_WITHOUT_VALID_AUTHORIZATION_ALLOWED=false" in index
    assert "SOURCE_SESSION_AUTHORIZATION_WITHOUT_CONTEXT_ALLOWED=false" in index
    assert "SOURCE_SESSION_AUTHORIZATION_WITHOUT_VERIFICATION_ALLOWED=false" in index
    assert "VALIDATION_STATUS=VALID" in index
    assert "VALIDATION_CASE_COUNT=10" in index
    assert "PASS_COUNT=10" in index
    assert "FAIL_COUNT=0" in index
    assert "VALIDATION_PASSED=true" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
