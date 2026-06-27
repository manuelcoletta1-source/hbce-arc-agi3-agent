import json
from pathlib import Path

from hbce_arc_agi3.milestone_28_query_result_export_regression_integration import (
    CURRENT_TASK_NUMBER,
    INTEGRATION_CASE_COUNT,
    NEXT_STAGE,
    REGRESSION_INTEGRATION_REVISION,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_VALIDATION_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_5_signature,
    validate_regression_integration_report,
)


DOC_PATH = Path("docs/milestone-28-task-5-query-result-export-regression-integration-v1.md")
SOURCE_TASK_4_DOC_PATH = Path("docs/milestone-28-task-4-query-result-export-validation-v1.md")
ARTIFACT_DIR = Path("examples/milestone-28/query-result-export-regression-integration-v1")


def test_task_5_doc_declares_query_result_export_regression_integration_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_28_TASK_5_QUERY_RESULT_EXPORT_REGRESSION_INTEGRATION_READY=true" in text
    assert f"MILESTONE_28_TASK_5_SOURCE_TASK_ID={SOURCE_VALIDATION_TASK_ID}" in text
    assert f"MILESTONE_28_TASK_5_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_28_TASK_5_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_28_TASK_5_REGRESSION_INTEGRATION_REVISION={REGRESSION_INTEGRATION_REVISION}" in text
    assert "MILESTONE_28_TASK_5_SOURCE_VALIDATION_STATUS=VALID" in text
    assert "MILESTONE_28_TASK_5_SOURCE_EXPORT_STATUS=READY" in text
    assert "MILESTONE_28_TASK_5_INTEGRATION_STATUS=VALID" in text
    assert f"MILESTONE_28_TASK_5_INTEGRATION_CASE_COUNT={INTEGRATION_CASE_COUNT}" in text
    assert "MILESTONE_28_TASK_5_PASS_COUNT=7" in text
    assert "MILESTONE_28_TASK_5_FAIL_COUNT=0" in text
    assert "MILESTONE_28_TASK_5_GENERATED_ARTIFACT_COUNT=5" in text
    assert f"MILESTONE_28_TASK_5_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_28_TASK_5_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert f"MILESTONE_28_TASK_5_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_5_dependency_keeps_task_4_validation_intact():
    text = SOURCE_TASK_4_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_28_TASK_4_QUERY_RESULT_EXPORT_VALIDATION_READY=true" in text
    assert f"MILESTONE_28_TASK_4_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_28_TASK_4_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert "MILESTONE_28_TASK_4_SOURCE_EXPORT_STATUS=READY" in text
    assert "MILESTONE_28_TASK_4_VALIDATION_STATUS=VALID" in text
    assert "MILESTONE_28_TASK_4_PASS_COUNT=6" in text
    assert "MILESTONE_28_TASK_4_FAIL_COUNT=0" in text
    assert "MILESTONE_28_TASK_4_NEXT_STAGE=MILESTONE_28_TASK_5_QUERY_RESULT_EXPORT_REGRESSION_INTEGRATION_V1" in text


def test_task_5_persisted_regression_integration_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-5-regression-integration-report.json").read_text(encoding="utf-8"))

    assert validate_regression_integration_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_VALIDATION_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["regression_integration_revision"] == REGRESSION_INTEGRATION_REVISION
    assert report["task_5_signature"] == task_5_signature()
    assert report["source_validation_status"] == "VALID"
    assert report["source_export_status"] == "READY"
    assert report["integration_status"] == "VALID"
    assert report["pass_count"] == 7
    assert report["fail_count"] == 0
    assert report["next_stage"] == NEXT_STAGE


def test_task_5_persisted_manifest_and_cases_match_report():
    report = json.loads((ARTIFACT_DIR / "task-5-regression-integration-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-5-manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((ARTIFACT_DIR / "task-5-regression-integration-cases.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["integration_id"] == report["integration_id"]
    assert manifest["integration_signature"] == report["integration_signature"]
    assert manifest["integration_status"] == "VALID"
    assert manifest["integration_passed"] is True
    assert manifest["generated_artifact_count"] == 5
    assert cases["task_id"] == TASK_ID
    assert cases["integration_id"] == report["integration_id"]
    assert cases["integration_status"] == report["integration_status"]
    assert cases["integration_case_count"] == report["integration_case_count"]
    assert len(cases["case_results"]) == report["integration_case_count"]


def test_task_5_index_contains_canonical_regression_integration_markers():
    index = (ARTIFACT_DIR / "task-5-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_28_TASK_5_QUERY_RESULT_EXPORT_REGRESSION_INTEGRATION_READY=true" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert "SOURCE_VALIDATION_STATUS=VALID" in index
    assert "SOURCE_EXPORT_STATUS=READY" in index
    assert "INTEGRATION_STATUS=VALID" in index
    assert "INTEGRATION_CASE_COUNT=7" in index
    assert "PASS_COUNT=7" in index
    assert "FAIL_COUNT=0" in index
    assert "GENERATED_ARTIFACT_COUNT=5" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
