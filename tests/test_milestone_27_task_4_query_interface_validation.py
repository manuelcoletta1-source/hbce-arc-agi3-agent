import json
from pathlib import Path

from hbce_arc_agi3.milestone_27_query_interface_validation import (
    NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_ID,
    VALIDATION_CASE_COUNT,
    VALIDATION_REVISION,
    task_4_signature,
    validate_validation_report,
)


DOC_PATH = Path("docs/milestone-27-task-4-query-interface-validation-v1.md")
TASK_3_DOC_PATH = Path("docs/milestone-27-task-3-query-interface-implementation-v1.md")
ARTIFACT_DIR = Path("examples/milestone-27/query-interface-validation-v1")


def test_task_4_doc_declares_validation_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_27_TASK_4_QUERY_INTERFACE_VALIDATION_READY=true" in text
    assert f"MILESTONE_27_TASK_4_SOURCE_TASK_ID={SOURCE_TASK_ID}" in text
    assert f"MILESTONE_27_TASK_4_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_27_TASK_4_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_27_TASK_4_VALIDATION_REVISION={VALIDATION_REVISION}" in text
    assert f"MILESTONE_27_TASK_4_VALIDATION_CASE_COUNT={VALIDATION_CASE_COUNT}" in text
    assert "MILESTONE_27_TASK_4_PASS_COUNT=6" in text
    assert "MILESTONE_27_TASK_4_FAIL_COUNT=0" in text
    assert "MILESTONE_27_TASK_4_LOCAL_ONLY=true" in text
    assert "MILESTONE_27_TASK_4_NETWORK_ACCESS_ALLOWED=false" in text
    assert "MILESTONE_27_TASK_4_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in text
    assert "MILESTONE_27_TASK_4_GENERATED_ARTIFACT_COUNT=5" in text
    assert f"MILESTONE_27_TASK_4_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_4_dependency_keeps_task_3_implementation_intact():
    text = TASK_3_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_27_TASK_3_QUERY_INTERFACE_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_27_TASK_3_QUERY_INTERFACE_IMPLEMENTED=true" in text
    assert "MILESTONE_27_TASK_3_LOCAL_ONLY=true" in text
    assert "MILESTONE_27_TASK_3_NETWORK_ACCESS_ALLOWED=false" in text
    assert "MILESTONE_27_TASK_3_NEXT_STAGE=MILESTONE_27_TASK_4_QUERY_INTERFACE_VALIDATION_V1" in text


def test_task_4_persisted_validation_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-4-validation-report.json").read_text(encoding="utf-8"))

    assert validate_validation_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["validation_revision"] == VALIDATION_REVISION
    assert report["task_4_signature"] == task_4_signature()
    assert report["validation_status"] == "VALID"
    assert report["validation_case_count"] == VALIDATION_CASE_COUNT
    assert report["pass_count"] == 6
    assert report["fail_count"] == 0


def test_task_4_persisted_manifest_and_case_matrix_match_report():
    report = json.loads((ARTIFACT_DIR / "task-4-validation-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-4-manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((ARTIFACT_DIR / "task-4-validation-cases.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["validation_id"] == report["validation_id"]
    assert manifest["validation_signature"] == report["validation_signature"]
    assert manifest["validation_status"] == "VALID"
    assert manifest["validation_passed"] is True
    assert manifest["generated_artifact_count"] == 5
    assert cases["task_id"] == TASK_ID
    assert cases["validation_id"] == report["validation_id"]
    assert cases["case_count"] == report["validation_case_count"]
    assert len(cases["case_results"]) == report["validation_case_count"]


def test_task_4_index_contains_canonical_validation_markers():
    index = (ARTIFACT_DIR / "task-4-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_27_TASK_4_QUERY_INTERFACE_VALIDATION_READY=true" in index
    assert "VALIDATION_STATUS=VALID" in index
    assert "PASS_COUNT=6" in index
    assert "FAIL_COUNT=0" in index
    assert "READY_CASE_COUNT=4" in index
    assert "BLOCKED_CASE_COUNT=2" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
