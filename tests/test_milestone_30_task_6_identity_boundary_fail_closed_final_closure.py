import json
from pathlib import Path

from hbce_arc_agi3.milestone_30_identity_boundary_fail_closed_final_closure import (
    FINAL_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    MILESTONE_ID,
    NEXT_STAGE,
    PROCESS_STATUS,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_6_signature,
    validate_final_closure_report,
)


DOC_PATH = Path("docs/milestone-30-task-6-identity-boundary-fail-closed-final-closure-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-30-task-5-identity-boundary-fail-closed-regression-integration-v1.md")
ARTIFACT_DIR = Path("examples/milestone-30/identity-boundary-fail-closed-final-closure-v1")


def test_task_6_doc_declares_final_closure_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_30_TASK_6_IDENTITY_BOUNDARY_FAIL_CLOSED_FINAL_CLOSURE_READY=true" in text
    assert f"MILESTONE_30_TASK_6_SOURCE_TASK_ID={SOURCE_TASK_ID}" in text
    assert f"MILESTONE_30_TASK_6_MILESTONE_ID={MILESTONE_ID}" in text
    assert f"MILESTONE_30_TASK_6_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_30_TASK_6_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert "MILESTONE_30_TASK_6_CLOSURE_STATUS=CLOSED" in text
    assert "MILESTONE_30_TASK_6_TECHNICAL_STATUS=PASS" in text
    assert f"MILESTONE_30_TASK_6_PROCESS_STATUS={PROCESS_STATUS}" in text
    assert "MILESTONE_30_TASK_6_MILESTONE_CLOSED=true" in text
    assert "MILESTONE_30_TASK_6_READY_FOR_NEXT_MILESTONE=true" in text
    assert "MILESTONE_30_TASK_6_IMPLEMENTATION_COMPLETE=true" in text
    assert "MILESTONE_30_TASK_6_VALIDATION_COMPLETE=true" in text
    assert "MILESTONE_30_TASK_6_REGRESSION_INTEGRATION_COMPLETE=true" in text
    assert "MILESTONE_30_TASK_6_SOURCE_INTEGRATION_STATUS=VALID" in text
    assert "MILESTONE_30_TASK_6_SOURCE_INTEGRATION_PASSED=true" in text
    assert "MILESTONE_30_TASK_6_SOURCE_PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL=false" in text
    assert "MILESTONE_30_TASK_6_SOURCE_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in text
    assert "MILESTONE_30_TASK_6_SOURCE_EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in text
    assert f"MILESTONE_30_TASK_6_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_30_TASK_6_FINAL_TASK_NUMBER={FINAL_TASK_NUMBER}" in text
    assert "MILESTONE_30_TASK_6_TASK_7_UNUSED=true" in text
    assert "MILESTONE_30_TASK_6_TASK_8_UNUSED=true" in text
    assert f"MILESTONE_30_TASK_6_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_30_TASK_6_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_6_dependency_keeps_task_5_regression_integration_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_30_TASK_5_IDENTITY_BOUNDARY_FAIL_CLOSED_REGRESSION_INTEGRATION_READY=true" in text
    assert f"MILESTONE_30_TASK_5_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_30_TASK_5_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert "MILESTONE_30_TASK_5_SOURCE_VALIDATION_STATUS=VALID" in text
    assert "MILESTONE_30_TASK_5_SOURCE_VALIDATION_PASSED=true" in text
    assert "MILESTONE_30_TASK_5_SOURCE_PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL=false" in text
    assert "MILESTONE_30_TASK_5_SOURCE_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in text
    assert "MILESTONE_30_TASK_5_SOURCE_EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in text
    assert "MILESTONE_30_TASK_5_INTEGRATION_STATUS=VALID" in text
    assert "MILESTONE_30_TASK_5_PASS_COUNT=9" in text
    assert "MILESTONE_30_TASK_5_FAIL_COUNT=0" in text
    assert "MILESTONE_30_TASK_5_NEXT_STAGE=MILESTONE_30_TASK_6_IDENTITY_BOUNDARY_FAIL_CLOSED_FINAL_CLOSURE_V1" in text


def test_task_6_persisted_final_closure_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-6-final-closure-report.json").read_text(encoding="utf-8"))

    assert validate_final_closure_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["milestone_id"] == MILESTONE_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["task_6_signature"] == task_6_signature()
    assert report["closure_status"] == "CLOSED"
    assert report["technical_status"] == "PASS"
    assert report["process_status"] == PROCESS_STATUS
    assert report["milestone_closed"] is True
    assert report["ready_for_next_milestone"] is True
    assert report["source_integration_status"] == "VALID"
    assert report["source_integration_passed"] is True
    assert report["pass_count"] == report["required_pass_count"]
    assert report["fail_count"] == 0
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["final_task_number"] == FINAL_TASK_NUMBER
    assert report["next_stage"] == NEXT_STAGE


def test_task_6_persisted_manifest_and_cases_match_report():
    report = json.loads((ARTIFACT_DIR / "task-6-final-closure-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-6-manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((ARTIFACT_DIR / "task-6-closure-cases.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["source_task_id"] == SOURCE_TASK_ID
    assert manifest["milestone_id"] == MILESTONE_ID
    assert manifest["closure_id"] == report["closure_id"]
    assert manifest["closure_signature"] == report["closure_signature"]
    assert manifest["source_integration_id"] == report["source_integration_id"]
    assert manifest["source_integration_signature"] == report["source_integration_signature"]
    assert manifest["closure_status"] == "CLOSED"
    assert manifest["technical_status"] == "PASS"
    assert manifest["process_status"] == PROCESS_STATUS
    assert manifest["milestone_closed"] is True
    assert manifest["ready_for_next_milestone"] is True
    assert cases["task_id"] == TASK_ID
    assert cases["closure_id"] == report["closure_id"]
    assert cases["closure_status"] == "CLOSED"
    assert cases["closure_case_count"] == report["closure_case_count"]
    assert len(cases["closure_cases"]) == report["closure_case_count"]


def test_task_6_index_contains_canonical_final_closure_markers():
    index = (ARTIFACT_DIR / "task-6-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_30_TASK_6_IDENTITY_BOUNDARY_FAIL_CLOSED_FINAL_CLOSURE_READY=true" in index
    assert f"SOURCE_TASK_ID={SOURCE_TASK_ID}" in index
    assert f"MILESTONE_ID={MILESTONE_ID}" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert "SOURCE_INTEGRATION_STATUS=VALID" in index
    assert "SOURCE_INTEGRATION_PASSED=true" in index
    assert "SOURCE_PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL=false" in index
    assert "SOURCE_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in index
    assert "SOURCE_EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in index
    assert "CLOSURE_STATUS=CLOSED" in index
    assert "TECHNICAL_STATUS=PASS" in index
    assert f"PROCESS_STATUS={PROCESS_STATUS}" in index
    assert "MILESTONE_CLOSED=true" in index
    assert "READY_FOR_NEXT_MILESTONE=true" in index
    assert "TASK_7_UNUSED=true" in index
    assert "TASK_8_UNUSED=true" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
