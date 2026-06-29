import json
from pathlib import Path

from hbce_arc_agi3.milestone_33_governed_opening import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    MILESTONE_ID,
    NEXT_STAGE,
    OPENING_CASE_COUNT,
    OPENING_REVISION,
    SOURCE_CLOSURE_TASK_ID,
    SOURCE_MILESTONE_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_1_signature,
    validate_milestone_33_governed_opening_report,
)


DOC_PATH = Path("docs/milestone-33-task-1-governed-opening-with-task-budget-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-32-task-6-hbce-ipr-runtime-api-v1-operational-identity-and-proof-layer-boundary-final-closure-v1.md")
ARTIFACT_DIR = Path("examples/milestone-33/governed-opening-with-task-budget-v1")


def test_task_1_doc_declares_milestone_33_governed_opening_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_33_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in text
    assert f"MILESTONE_33_TASK_1_TASK_ID={TASK_ID}" in text
    assert f"MILESTONE_33_TASK_1_MILESTONE_ID={MILESTONE_ID}" in text
    assert f"MILESTONE_33_TASK_1_SOURCE_MILESTONE_ID={SOURCE_MILESTONE_ID}" in text
    assert f"MILESTONE_33_TASK_1_SOURCE_CLOSURE_TASK_ID={SOURCE_CLOSURE_TASK_ID}" in text
    assert f"MILESTONE_33_TASK_1_OPENING_REVISION={OPENING_REVISION}" in text
    assert "MILESTONE_33_TASK_1_SOURCE_CLOSURE_STATUS=CLOSED" in text
    assert "MILESTONE_33_TASK_1_SOURCE_CLOSURE_PASSED=true" in text
    assert "MILESTONE_33_TASK_1_OPENING_STATUS=READY" in text
    assert "MILESTONE_33_TASK_1_OBJECTIVE_SELECTION_STATUS=PENDING_TASK_2_SCOPE_LOCK" in text
    assert f"MILESTONE_33_TASK_1_OPENING_CASE_COUNT={OPENING_CASE_COUNT}" in text
    assert "MILESTONE_33_TASK_1_PASS_COUNT=8" in text
    assert "MILESTONE_33_TASK_1_FAIL_COUNT=0" in text
    assert "MILESTONE_33_TASK_1_OPENING_PASSED=true" in text
    assert f"MILESTONE_33_TASK_1_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_33_TASK_1_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert f"MILESTONE_33_TASK_1_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_33_TASK_1_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_1_dependency_keeps_milestone_32_final_closure_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_6_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_FINAL_CLOSURE_READY=true" in text
    assert "MILESTONE_32_TASK_6_CLOSURE_STATUS=CLOSED" in text
    assert "MILESTONE_32_TASK_6_PASS_COUNT=12" in text
    assert "MILESTONE_32_TASK_6_FAIL_COUNT=0" in text
    assert "MILESTONE_32_TASK_6_CLOSURE_PASSED=true" in text
    assert "MILESTONE_32_TASK_6_NEXT_STAGE=MILESTONE_33_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1" in text


def test_task_1_persisted_governed_opening_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-1-governed-opening-report.json").read_text(encoding="utf-8"))

    assert validate_milestone_33_governed_opening_report(report)
    assert report["task_id"] == TASK_ID
    assert report["milestone_id"] == MILESTONE_ID
    assert report["source_milestone_id"] == SOURCE_MILESTONE_ID
    assert report["source_closure_task_id"] == SOURCE_CLOSURE_TASK_ID
    assert report["opening_revision"] == OPENING_REVISION
    assert report["task_1_signature"] == task_1_signature()
    assert report["source_closure_status"] == "CLOSED"
    assert report["source_closure_passed"] is True
    assert report["opening_status"] == "READY"
    assert report["opening_case_count"] == OPENING_CASE_COUNT
    assert report["pass_count"] == 8
    assert report["fail_count"] == 0
    assert report["opening_passed"] is True
    assert report["next_stage"] == NEXT_STAGE


def test_task_1_persisted_manifest_and_cases_match_report():
    report = json.loads((ARTIFACT_DIR / "task-1-governed-opening-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-1-manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((ARTIFACT_DIR / "task-1-governed-opening-cases.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["milestone_id"] == MILESTONE_ID
    assert manifest["source_milestone_id"] == SOURCE_MILESTONE_ID
    assert manifest["source_closure_task_id"] == SOURCE_CLOSURE_TASK_ID
    assert manifest["opening_id"] == report["opening_id"]
    assert manifest["opening_signature"] == report["opening_signature"]
    assert manifest["opening_status"] == "READY"
    assert manifest["opening_passed"] is True
    assert cases["task_id"] == TASK_ID
    assert cases["opening_id"] == report["opening_id"]
    assert cases["opening_status"] == "READY"
    assert cases["opening_case_count"] == report["opening_case_count"]


def test_task_1_index_contains_canonical_opening_markers():
    index = (ARTIFACT_DIR / "task-1-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_33_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in index
    assert f"TASK_ID={TASK_ID}" in index
    assert f"MILESTONE_ID={MILESTONE_ID}" in index
    assert f"SOURCE_MILESTONE_ID={SOURCE_MILESTONE_ID}" in index
    assert f"SOURCE_CLOSURE_TASK_ID={SOURCE_CLOSURE_TASK_ID}" in index
    assert "SOURCE_CLOSURE_STATUS=CLOSED" in index
    assert "SOURCE_CLOSURE_PASSED=true" in index
    assert f"OPENING_REVISION={OPENING_REVISION}" in index
    assert "OPENING_STATUS=READY" in index
    assert "OBJECTIVE_SELECTION_STATUS=PENDING_TASK_2_SCOPE_LOCK" in index
    assert "OPENING_CASE_COUNT=8" in index
    assert "PASS_COUNT=8" in index
    assert "FAIL_COUNT=0" in index
    assert "OPENING_PASSED=true" in index
    assert f"TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
