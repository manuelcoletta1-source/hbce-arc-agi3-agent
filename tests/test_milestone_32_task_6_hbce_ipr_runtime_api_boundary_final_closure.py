import json
from pathlib import Path

from hbce_arc_agi3.milestone_32_hbce_ipr_runtime_api_boundary_final_closure import (
    CLOSURE_CASE_COUNT,
    CURRENT_TASK_NUMBER,
    FINAL_CLOSURE_REVISION,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_REGRESSION_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_6_signature,
    validate_milestone_32_boundary_final_closure_report,
)


DOC_PATH = Path("docs/milestone-32-task-6-hbce-ipr-runtime-api-v1-operational-identity-and-proof-layer-boundary-final-closure-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-32-task-5-hbce-ipr-runtime-api-v1-operational-identity-and-proof-layer-boundary-regression-integration-v1.md")
ARTIFACT_DIR = Path("examples/milestone-32/hbce-ipr-runtime-api-v1-operational-identity-proof-layer-boundary-final-closure-v1")


def test_task_6_doc_declares_boundary_final_closure_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_6_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_FINAL_CLOSURE_READY=true" in text
    assert f"MILESTONE_32_TASK_6_TASK_ID={TASK_ID}" in text
    assert f"MILESTONE_32_TASK_6_SOURCE_REGRESSION_TASK_ID={SOURCE_REGRESSION_TASK_ID}" in text
    assert f"MILESTONE_32_TASK_6_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_32_TASK_6_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_32_TASK_6_FINAL_CLOSURE_REVISION={FINAL_CLOSURE_REVISION}" in text
    assert "MILESTONE_32_TASK_6_SOURCE_INTEGRATION_STATUS=VALID" in text
    assert "MILESTONE_32_TASK_6_CLOSURE_STATUS=CLOSED" in text
    assert f"MILESTONE_32_TASK_6_CLOSURE_CASE_COUNT={CLOSURE_CASE_COUNT}" in text
    assert "MILESTONE_32_TASK_6_PASS_COUNT=12" in text
    assert "MILESTONE_32_TASK_6_FAIL_COUNT=0" in text
    assert "MILESTONE_32_TASK_6_CLOSURE_PASSED=true" in text
    assert "MILESTONE_32_TASK_6_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_32_TASK_6_IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT=false" in text
    assert f"MILESTONE_32_TASK_6_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_32_TASK_6_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert f"MILESTONE_32_TASK_6_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_32_TASK_6_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_6_dependency_keeps_task_5_regression_integration_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_5_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_REGRESSION_INTEGRATION_READY=true" in text
    assert "MILESTONE_32_TASK_5_INTEGRATION_STATUS=VALID" in text
    assert "MILESTONE_32_TASK_5_PASS_COUNT=12" in text
    assert "MILESTONE_32_TASK_5_FAIL_COUNT=0" in text
    assert "MILESTONE_32_TASK_5_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_32_TASK_5_NEXT_STAGE=MILESTONE_32_TASK_6_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_FINAL_CLOSURE_V1" in text


def test_task_6_persisted_final_closure_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-6-boundary-final-closure-report.json").read_text(encoding="utf-8"))

    assert validate_milestone_32_boundary_final_closure_report(report)
    assert report["task_id"] == TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["task_6_signature"] == task_6_signature()
    assert report["closure_status"] == "CLOSED"
    assert report["closure_case_count"] == CLOSURE_CASE_COUNT
    assert report["pass_count"] == 12
    assert report["fail_count"] == 0
    assert report["closure_passed"] is True
    assert report["next_stage"] == NEXT_STAGE


def test_task_6_persisted_manifest_and_cases_match_report():
    report = json.loads((ARTIFACT_DIR / "task-6-boundary-final-closure-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-6-manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((ARTIFACT_DIR / "task-6-boundary-final-closure-cases.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert manifest["scope_lock_id"] == SCOPE_LOCK_ID
    assert manifest["closure_id"] == report["closure_id"]
    assert manifest["closure_signature"] == report["closure_signature"]
    assert manifest["closure_status"] == "CLOSED"
    assert manifest["closure_passed"] is True
    assert cases["task_id"] == TASK_ID
    assert cases["closure_id"] == report["closure_id"]
    assert cases["closure_status"] == "CLOSED"
    assert len(cases["closure_cases"]) == report["closure_case_count"]


def test_task_6_index_contains_canonical_final_closure_markers():
    index = (ARTIFACT_DIR / "task-6-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_6_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_FINAL_CLOSURE_READY=true" in index
    assert f"TASK_ID={TASK_ID}" in index
    assert f"SOURCE_REGRESSION_TASK_ID={SOURCE_REGRESSION_TASK_ID}" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert "CLOSURE_STATUS=CLOSED" in index
    assert "CLOSURE_CASE_COUNT=12" in index
    assert "PASS_COUNT=12" in index
    assert "FAIL_COUNT=0" in index
    assert "CLOSURE_PASSED=true" in index
    assert "LEGAL_CERTIFICATION=false" in index
    assert "IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT=false" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
