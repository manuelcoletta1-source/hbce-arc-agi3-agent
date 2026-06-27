import json
from pathlib import Path

from hbce_arc_agi3.milestone_27_query_interface_final_closure import (
    CLOSURE_CASE_COUNT,
    FINAL_CLOSURE_REVISION,
    FINAL_TASK_NUMBER,
    NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_6_signature,
    validate_final_closure_report,
)


DOC_PATH = Path("docs/milestone-27-task-6-query-interface-final-closure-v1.md")
TASK_5_DOC_PATH = Path("docs/milestone-27-task-5-query-interface-regression-integration-v1.md")
ARTIFACT_DIR = Path("examples/milestone-27/query-interface-final-closure-v1")


def test_task_6_doc_declares_final_closure_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_27_TASK_6_QUERY_INTERFACE_FINAL_CLOSURE_READY=true" in text
    assert f"MILESTONE_27_TASK_6_SOURCE_TASK_ID={SOURCE_TASK_ID}" in text
    assert f"MILESTONE_27_TASK_6_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_27_TASK_6_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_27_TASK_6_FINAL_CLOSURE_REVISION={FINAL_CLOSURE_REVISION}" in text
    assert "MILESTONE_27_TASK_6_CLOSURE_STATUS=CLOSED" in text
    assert "MILESTONE_27_TASK_6_TECHNICAL_STATUS=PASS" in text
    assert "MILESTONE_27_TASK_6_PROCESS_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6" in text
    assert f"MILESTONE_27_TASK_6_CLOSURE_CASE_COUNT={CLOSURE_CASE_COUNT}" in text
    assert "MILESTONE_27_TASK_6_PASS_COUNT=7" in text
    assert "MILESTONE_27_TASK_6_FAIL_COUNT=0" in text
    assert f"MILESTONE_27_TASK_6_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_27_TASK_6_FINAL_TASK_NUMBER={FINAL_TASK_NUMBER}" in text
    assert "MILESTONE_27_TASK_6_TASK_7_USED=false" in text
    assert "MILESTONE_27_TASK_6_TASK_8_USED=false" in text
    assert "MILESTONE_27_TASK_6_MILESTONE_CLOSED=true" in text
    assert "MILESTONE_27_TASK_6_READY_FOR_NEXT_MILESTONE=true" in text
    assert "MILESTONE_27_TASK_6_GENERATED_ARTIFACT_COUNT=5" in text
    assert f"MILESTONE_27_TASK_6_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_6_dependency_keeps_task_5_regression_integration_intact():
    text = TASK_5_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_27_TASK_5_QUERY_INTERFACE_REGRESSION_INTEGRATION_READY=true" in text
    assert "MILESTONE_27_TASK_5_INTEGRATION_STATUS=INTEGRATED" in text
    assert "MILESTONE_27_TASK_5_PASS_COUNT=6" in text
    assert "MILESTONE_27_TASK_5_FAIL_COUNT=0" in text
    assert "MILESTONE_27_TASK_5_NEXT_STAGE=MILESTONE_27_TASK_6_QUERY_INTERFACE_FINAL_CLOSURE_V1" in text


def test_task_6_persisted_final_closure_report_is_closed():
    report = json.loads((ARTIFACT_DIR / "task-6-final-closure-report.json").read_text(encoding="utf-8"))

    assert validate_final_closure_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["final_closure_revision"] == FINAL_CLOSURE_REVISION
    assert report["task_6_signature"] == task_6_signature()
    assert report["closure_status"] == "CLOSED"
    assert report["pass_count"] == 7
    assert report["fail_count"] == 0
    assert report["final_task_number"] == 6
    assert report["task_7_used"] is False
    assert report["task_8_used"] is False


def test_task_6_persisted_manifest_and_closure_index_match_report():
    report = json.loads((ARTIFACT_DIR / "task-6-final-closure-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-6-manifest.json").read_text(encoding="utf-8"))
    closure_index = json.loads((ARTIFACT_DIR / "task-6-closure-index.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["closure_id"] == report["closure_id"]
    assert manifest["closure_signature"] == report["closure_signature"]
    assert manifest["closure_status"] == "CLOSED"
    assert manifest["closure_passed"] is True
    assert manifest["generated_artifact_count"] == 5
    assert closure_index["task_id"] == TASK_ID
    assert closure_index["closure_id"] == report["closure_id"]
    assert closure_index["closure_status"] == report["closure_status"]
    assert closure_index["case_count"] == report["closure_case_count"]
    assert len(closure_index["case_results"]) == report["closure_case_count"]


def test_task_6_index_contains_canonical_final_closure_markers():
    index = (ARTIFACT_DIR / "task-6-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_27_TASK_6_QUERY_INTERFACE_FINAL_CLOSURE_READY=true" in index
    assert "CLOSURE_STATUS=CLOSED" in index
    assert "TECHNICAL_STATUS=PASS" in index
    assert "PROCESS_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6" in index
    assert "PASS_COUNT=7" in index
    assert "FAIL_COUNT=0" in index
    assert "FINAL_TASK_NUMBER=6" in index
    assert "TASK_7_USED=false" in index
    assert "TASK_8_USED=false" in index
    assert "MILESTONE_CLOSED=true" in index
    assert "READY_FOR_NEXT_MILESTONE=true" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
