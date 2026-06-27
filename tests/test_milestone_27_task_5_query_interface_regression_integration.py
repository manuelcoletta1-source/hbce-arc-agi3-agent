import json
from pathlib import Path

from hbce_arc_agi3.milestone_27_query_interface_regression_integration import (
    NEXT_STAGE,
    REGRESSION_CASE_COUNT,
    REGRESSION_REVISION,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_ID,
    task_5_signature,
    validate_regression_integration_report,
)


DOC_PATH = Path("docs/milestone-27-task-5-query-interface-regression-integration-v1.md")
TASK_4_DOC_PATH = Path("docs/milestone-27-task-4-query-interface-validation-v1.md")
ARTIFACT_DIR = Path("examples/milestone-27/query-interface-regression-integration-v1")


def test_task_5_doc_declares_regression_integration_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_27_TASK_5_QUERY_INTERFACE_REGRESSION_INTEGRATION_READY=true" in text
    assert f"MILESTONE_27_TASK_5_SOURCE_TASK_ID={SOURCE_TASK_ID}" in text
    assert f"MILESTONE_27_TASK_5_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_27_TASK_5_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_27_TASK_5_REGRESSION_REVISION={REGRESSION_REVISION}" in text
    assert f"MILESTONE_27_TASK_5_REGRESSION_CASE_COUNT={REGRESSION_CASE_COUNT}" in text
    assert "MILESTONE_27_TASK_5_INTEGRATION_STATUS=INTEGRATED" in text
    assert "MILESTONE_27_TASK_5_PASS_COUNT=6" in text
    assert "MILESTONE_27_TASK_5_FAIL_COUNT=0" in text
    assert "MILESTONE_27_TASK_5_LOCAL_ONLY=true" in text
    assert "MILESTONE_27_TASK_5_NETWORK_ACCESS_ALLOWED=false" in text
    assert "MILESTONE_27_TASK_5_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in text
    assert "MILESTONE_27_TASK_5_GENERATED_ARTIFACT_COUNT=5" in text
    assert f"MILESTONE_27_TASK_5_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_5_dependency_keeps_task_4_validation_intact():
    text = TASK_4_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_27_TASK_4_QUERY_INTERFACE_VALIDATION_READY=true" in text
    assert "MILESTONE_27_TASK_4_VALIDATION_STATUS=VALID" in text
    assert "MILESTONE_27_TASK_4_PASS_COUNT=6" in text
    assert "MILESTONE_27_TASK_4_FAIL_COUNT=0" in text
    assert "MILESTONE_27_TASK_4_NEXT_STAGE=MILESTONE_27_TASK_5_QUERY_INTERFACE_REGRESSION_INTEGRATION_V1" in text


def test_task_5_persisted_regression_report_is_integrated():
    report = json.loads((ARTIFACT_DIR / "task-5-regression-integration-report.json").read_text(encoding="utf-8"))

    assert validate_regression_integration_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["regression_revision"] == REGRESSION_REVISION
    assert report["task_5_signature"] == task_5_signature()
    assert report["integration_status"] == "INTEGRATED"
    assert report["regression_case_count"] == REGRESSION_CASE_COUNT
    assert report["pass_count"] == 6
    assert report["fail_count"] == 0


def test_task_5_persisted_manifest_and_case_matrix_match_report():
    report = json.loads((ARTIFACT_DIR / "task-5-regression-integration-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-5-manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((ARTIFACT_DIR / "task-5-regression-cases.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["integration_id"] == report["integration_id"]
    assert manifest["integration_signature"] == report["integration_signature"]
    assert manifest["integration_status"] == "INTEGRATED"
    assert manifest["integration_passed"] is True
    assert manifest["generated_artifact_count"] == 5
    assert cases["task_id"] == TASK_ID
    assert cases["integration_id"] == report["integration_id"]
    assert cases["case_count"] == report["regression_case_count"]
    assert len(cases["case_results"]) == report["regression_case_count"]


def test_task_5_index_contains_canonical_integration_markers():
    index = (ARTIFACT_DIR / "task-5-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_27_TASK_5_QUERY_INTERFACE_REGRESSION_INTEGRATION_READY=true" in index
    assert "INTEGRATION_STATUS=INTEGRATED" in index
    assert "PASS_COUNT=6" in index
    assert "FAIL_COUNT=0" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
