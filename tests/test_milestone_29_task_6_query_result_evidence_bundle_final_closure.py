import json
from pathlib import Path

from hbce_arc_agi3.milestone_29_query_result_evidence_bundle_final_closure import (
    CLOSURE_CASE_COUNT,
    CURRENT_TASK_NUMBER,
    FINAL_CLOSURE_REVISION,
    FINAL_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    PROCESS_STATUS,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_INTEGRATION_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_6_signature,
    validate_final_closure_report,
)


DOC_PATH = Path("docs/milestone-29-task-6-query-result-evidence-bundle-final-closure-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-29-task-5-query-result-evidence-bundle-regression-integration-v1.md")
ARTIFACT_DIR = Path("examples/milestone-29/query-result-evidence-bundle-final-closure-v1")


def test_task_6_doc_declares_query_result_evidence_bundle_final_closure_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_29_TASK_6_QUERY_RESULT_EVIDENCE_BUNDLE_FINAL_CLOSURE_READY=true" in text
    assert f"MILESTONE_29_TASK_6_SOURCE_TASK_ID={SOURCE_INTEGRATION_TASK_ID}" in text
    assert f"MILESTONE_29_TASK_6_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_29_TASK_6_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_29_TASK_6_FINAL_CLOSURE_REVISION={FINAL_CLOSURE_REVISION}" in text
    assert "MILESTONE_29_TASK_6_SOURCE_INTEGRATION_STATUS=VALID" in text
    assert "MILESTONE_29_TASK_6_SOURCE_VALIDATION_STATUS=VALID" in text
    assert "MILESTONE_29_TASK_6_SOURCE_IMPLEMENTATION_STATUS=READY" in text
    assert "MILESTONE_29_TASK_6_SOURCE_SCOPE_LOCK_VALID=true" in text
    assert "MILESTONE_29_TASK_6_SOURCE_CHAIN_VALID=true" in text
    assert "MILESTONE_29_TASK_6_SOURCE_EVIDENCE_VALID=true" in text
    assert "MILESTONE_29_TASK_6_CLOSURE_STATUS=CLOSED" in text
    assert "MILESTONE_29_TASK_6_TECHNICAL_STATUS=PASS" in text
    assert f"MILESTONE_29_TASK_6_PROCESS_STATUS={PROCESS_STATUS}" in text
    assert f"MILESTONE_29_TASK_6_CLOSURE_CASE_COUNT={CLOSURE_CASE_COUNT}" in text
    assert "MILESTONE_29_TASK_6_PASS_COUNT=8" in text
    assert "MILESTONE_29_TASK_6_FAIL_COUNT=0" in text
    assert f"MILESTONE_29_TASK_6_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_29_TASK_6_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert f"MILESTONE_29_TASK_6_FINAL_TASK_NUMBER={FINAL_TASK_NUMBER}" in text
    assert "MILESTONE_29_TASK_6_TASK_7_USED=false" in text
    assert "MILESTONE_29_TASK_6_TASK_8_USED=false" in text
    assert "MILESTONE_29_TASK_6_MILESTONE_CLOSED=true" in text
    assert "MILESTONE_29_TASK_6_READY_FOR_NEXT_MILESTONE=true" in text
    assert f"MILESTONE_29_TASK_6_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_29_TASK_6_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_6_dependency_keeps_task_5_regression_integration_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_29_TASK_5_QUERY_RESULT_EVIDENCE_BUNDLE_REGRESSION_INTEGRATION_READY=true" in text
    assert f"MILESTONE_29_TASK_5_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_29_TASK_5_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert "MILESTONE_29_TASK_5_SOURCE_VALIDATION_STATUS=VALID" in text
    assert "MILESTONE_29_TASK_5_SOURCE_IMPLEMENTATION_STATUS=READY" in text
    assert "MILESTONE_29_TASK_5_SOURCE_SCOPE_LOCK_VALID=true" in text
    assert "MILESTONE_29_TASK_5_SOURCE_CHAIN_VALID=true" in text
    assert "MILESTONE_29_TASK_5_SOURCE_EVIDENCE_VALID=true" in text
    assert "MILESTONE_29_TASK_5_INTEGRATION_STATUS=VALID" in text
    assert "MILESTONE_29_TASK_5_PASS_COUNT=9" in text
    assert "MILESTONE_29_TASK_5_FAIL_COUNT=0" in text
    assert "MILESTONE_29_TASK_5_NEXT_STAGE=MILESTONE_29_TASK_6_QUERY_RESULT_EVIDENCE_BUNDLE_FINAL_CLOSURE_V1" in text


def test_task_6_persisted_final_closure_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-6-final-closure-report.json").read_text(encoding="utf-8"))

    assert validate_final_closure_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_INTEGRATION_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["final_closure_revision"] == FINAL_CLOSURE_REVISION
    assert report["task_6_signature"] == task_6_signature()
    assert report["source_integration_status"] == "VALID"
    assert report["source_validation_status"] == "VALID"
    assert report["source_implementation_status"] == "READY"
    assert report["closure_status"] == "CLOSED"
    assert report["technical_status"] == "PASS"
    assert report["process_status"] == PROCESS_STATUS
    assert report["pass_count"] == 8
    assert report["fail_count"] == 0
    assert report["task_7_used"] is False
    assert report["task_8_used"] is False
    assert report["milestone_closed"] is True
    assert report["ready_for_next_milestone"] is True
    assert report["next_stage"] == NEXT_STAGE


def test_task_6_persisted_manifest_and_cases_match_report():
    report = json.loads((ARTIFACT_DIR / "task-6-final-closure-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-6-manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((ARTIFACT_DIR / "task-6-final-closure-cases.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["closure_id"] == report["closure_id"]
    assert manifest["closure_signature"] == report["closure_signature"]
    assert manifest["closure_status"] == "CLOSED"
    assert manifest["technical_status"] == "PASS"
    assert manifest["process_status"] == PROCESS_STATUS
    assert manifest["closure_passed"] is True
    assert manifest["generated_artifact_count"] == 5
    assert cases["task_id"] == TASK_ID
    assert cases["closure_id"] == report["closure_id"]
    assert cases["closure_status"] == report["closure_status"]
    assert cases["closure_case_count"] == report["closure_case_count"]
    assert len(cases["case_results"]) == report["closure_case_count"]


def test_task_6_index_contains_canonical_final_closure_markers():
    index = (ARTIFACT_DIR / "task-6-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_29_TASK_6_QUERY_RESULT_EVIDENCE_BUNDLE_FINAL_CLOSURE_READY=true" in index
    assert f"SOURCE_TASK_ID={SOURCE_INTEGRATION_TASK_ID}" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert "SOURCE_INTEGRATION_STATUS=VALID" in index
    assert "SOURCE_VALIDATION_STATUS=VALID" in index
    assert "SOURCE_IMPLEMENTATION_STATUS=READY" in index
    assert "SOURCE_SCOPE_LOCK_VALID=true" in index
    assert "SOURCE_CHAIN_VALID=true" in index
    assert "SOURCE_EVIDENCE_VALID=true" in index
    assert "CLOSURE_STATUS=CLOSED" in index
    assert "TECHNICAL_STATUS=PASS" in index
    assert f"PROCESS_STATUS={PROCESS_STATUS}" in index
    assert "CLOSURE_CASE_COUNT=8" in index
    assert "PASS_COUNT=8" in index
    assert "FAIL_COUNT=0" in index
    assert "TASK_BUDGET_MAX=8" in index
    assert "CURRENT_TASK_NUMBER=6" in index
    assert "FINAL_TASK_NUMBER=6" in index
    assert "TASK_7_USED=false" in index
    assert "TASK_8_USED=false" in index
    assert "MILESTONE_CLOSED=true" in index
    assert "READY_FOR_NEXT_MILESTONE=true" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
