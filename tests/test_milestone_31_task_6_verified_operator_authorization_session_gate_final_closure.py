import json
from pathlib import Path

from hbce_arc_agi3.milestone_31_verified_operator_session_gate_final_closure import (
    CLOSURE_CASE_COUNT,
    CURRENT_TASK_NUMBER,
    FINAL_CLOSURE_REVISION,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SESSION_GATE_MODE_ID,
    SOURCE_REGRESSION_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_6_signature,
    validate_verified_operator_session_gate_final_closure_report,
)


DOC_PATH = Path("docs/milestone-31-task-6-verified-operator-authorization-session-gate-final-closure-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-31-task-5-verified-operator-authorization-session-gate-regression-integration-v1.md")
ARTIFACT_DIR = Path("examples/milestone-31/verified-operator-authorization-session-gate-final-closure-v1")


def test_task_6_doc_declares_session_gate_final_closure_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_31_TASK_6_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_FINAL_CLOSURE_READY=true" in text
    assert f"MILESTONE_31_TASK_6_TASK_ID={TASK_ID}" in text
    assert f"MILESTONE_31_TASK_6_SOURCE_REGRESSION_TASK_ID={SOURCE_REGRESSION_TASK_ID}" in text
    assert f"MILESTONE_31_TASK_6_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_31_TASK_6_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_31_TASK_6_SESSION_GATE_MODE_ID={SESSION_GATE_MODE_ID}" in text
    assert f"MILESTONE_31_TASK_6_FINAL_CLOSURE_REVISION={FINAL_CLOSURE_REVISION}" in text
    assert "MILESTONE_31_TASK_6_SOURCE_INTEGRATION_STATUS=VALID" in text
    assert "MILESTONE_31_TASK_6_SOURCE_INTEGRATION_PASSED=true" in text
    assert "MILESTONE_31_TASK_6_SOURCE_INTEGRATION_CASE_COUNT=10" in text
    assert "MILESTONE_31_TASK_6_SOURCE_PASS_COUNT=10" in text
    assert "MILESTONE_31_TASK_6_SOURCE_FAIL_COUNT=0" in text
    assert "MILESTONE_31_TASK_6_CLOSURE_STATUS=CLOSED" in text
    assert f"MILESTONE_31_TASK_6_CLOSURE_CASE_COUNT={CLOSURE_CASE_COUNT}" in text
    assert "MILESTONE_31_TASK_6_PASS_COUNT=12" in text
    assert "MILESTONE_31_TASK_6_FAIL_COUNT=0" in text
    assert "MILESTONE_31_TASK_6_CLOSURE_PASSED=true" in text
    assert f"MILESTONE_31_TASK_6_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_31_TASK_6_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert f"MILESTONE_31_TASK_6_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_31_TASK_6_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_6_dependency_keeps_task_5_regression_integration_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_31_TASK_5_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_REGRESSION_INTEGRATION_READY=true" in text
    assert f"MILESTONE_31_TASK_5_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_31_TASK_5_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_31_TASK_5_SOURCE_SESSION_GATE_MODE_ID={SESSION_GATE_MODE_ID}" in text
    assert "MILESTONE_31_TASK_5_INTEGRATION_STATUS=VALID" in text
    assert "MILESTONE_31_TASK_5_INTEGRATION_CASE_COUNT=10" in text
    assert "MILESTONE_31_TASK_5_PASS_COUNT=10" in text
    assert "MILESTONE_31_TASK_5_FAIL_COUNT=0" in text
    assert "MILESTONE_31_TASK_5_INTEGRATION_PASSED=true" in text
    assert "MILESTONE_31_TASK_5_NEXT_STAGE=MILESTONE_31_TASK_6_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_FINAL_CLOSURE_V1" in text


def test_task_6_persisted_final_closure_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-6-final-closure-report.json").read_text(encoding="utf-8"))

    assert validate_verified_operator_session_gate_final_closure_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_regression_task_id"] == SOURCE_REGRESSION_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["session_gate_mode_id"] == SESSION_GATE_MODE_ID
    assert report["final_closure_revision"] == FINAL_CLOSURE_REVISION
    assert report["task_6_signature"] == task_6_signature()
    assert report["source_integration_status"] == "VALID"
    assert report["source_integration_passed"] is True
    assert report["closure_status"] == "CLOSED"
    assert report["closure_case_count"] == CLOSURE_CASE_COUNT
    assert report["pass_count"] == 12
    assert report["fail_count"] == 0
    assert report["closure_passed"] is True
    assert report["next_stage"] == NEXT_STAGE


def test_task_6_persisted_manifest_and_cases_match_report():
    report = json.loads((ARTIFACT_DIR / "task-6-final-closure-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-6-manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((ARTIFACT_DIR / "task-6-final-closure-cases.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["source_regression_task_id"] == SOURCE_REGRESSION_TASK_ID
    assert manifest["closure_id"] == report["closure_id"]
    assert manifest["closure_signature"] == report["closure_signature"]
    assert manifest["source_integration_id"] == report["source_integration_id"]
    assert manifest["source_integration_signature"] == report["source_integration_signature"]
    assert manifest["closure_status"] == "CLOSED"
    assert manifest["closure_passed"] is True
    assert cases["task_id"] == TASK_ID
    assert cases["closure_id"] == report["closure_id"]
    assert cases["closure_status"] == "CLOSED"
    assert cases["closure_case_count"] == report["closure_case_count"]
    assert len(cases["closure_cases"]) == report["closure_case_count"]


def test_task_6_index_contains_canonical_final_closure_markers():
    index = (ARTIFACT_DIR / "task-6-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_31_TASK_6_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_FINAL_CLOSURE_READY=true" in index
    assert f"TASK_ID={TASK_ID}" in index
    assert f"SOURCE_REGRESSION_TASK_ID={SOURCE_REGRESSION_TASK_ID}" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert f"SESSION_GATE_MODE_ID={SESSION_GATE_MODE_ID}" in index
    assert f"FINAL_CLOSURE_REVISION={FINAL_CLOSURE_REVISION}" in index
    assert "SOURCE_INTEGRATION_STATUS=VALID" in index
    assert "SOURCE_INTEGRATION_PASSED=true" in index
    assert "SOURCE_INTEGRATION_CASE_COUNT=10" in index
    assert "SOURCE_PASS_COUNT=10" in index
    assert "SOURCE_FAIL_COUNT=0" in index
    assert "CLOSURE_STATUS=CLOSED" in index
    assert "CLOSURE_CASE_COUNT=12" in index
    assert "PASS_COUNT=12" in index
    assert "FAIL_COUNT=0" in index
    assert "CLOSURE_PASSED=true" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
