import json
from pathlib import Path

from hbce_arc_agi3.milestone_32_hbce_ipr_runtime_api_boundary_regression_integration import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    REGRESSION_CASE_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_VALIDATION_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_5_signature,
    validate_milestone_32_boundary_regression_integration_report,
)


DOC_PATH = Path("docs/milestone-32-task-5-hbce-ipr-runtime-api-v1-operational-identity-and-proof-layer-boundary-regression-integration-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-32-task-4-hbce-ipr-runtime-api-v1-operational-identity-and-proof-layer-boundary-validation-v1.md")
ARTIFACT_DIR = Path("examples/milestone-32/hbce-ipr-runtime-api-v1-operational-identity-proof-layer-boundary-regression-integration-v1")


def test_task_5_doc_declares_boundary_regression_integration_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_5_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_REGRESSION_INTEGRATION_READY=true" in text
    assert f"MILESTONE_32_TASK_5_TASK_ID={TASK_ID}" in text
    assert f"MILESTONE_32_TASK_5_SOURCE_VALIDATION_TASK_ID={SOURCE_VALIDATION_TASK_ID}" in text
    assert f"MILESTONE_32_TASK_5_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_32_TASK_5_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert "MILESTONE_32_TASK_5_SOURCE_VALIDATION_STATUS=VALID" in text
    assert "MILESTONE_32_TASK_5_INTEGRATION_STATUS=VALID" in text
    assert f"MILESTONE_32_TASK_5_INTEGRATION_CASE_COUNT={REGRESSION_CASE_COUNT}" in text
    assert "MILESTONE_32_TASK_5_PASS_COUNT=12" in text
    assert "MILESTONE_32_TASK_5_FAIL_COUNT=0" in text
    assert "MILESTONE_32_TASK_5_INTEGRATION_PASSED=true" in text
    assert "MILESTONE_32_TASK_5_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_32_TASK_5_IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT=false" in text
    assert f"MILESTONE_32_TASK_5_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_32_TASK_5_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert f"MILESTONE_32_TASK_5_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_32_TASK_5_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_5_dependency_keeps_task_4_validation_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_4_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_VALIDATION_READY=true" in text
    assert "MILESTONE_32_TASK_4_VALIDATION_STATUS=VALID" in text
    assert "MILESTONE_32_TASK_4_PASS_COUNT=12" in text
    assert "MILESTONE_32_TASK_4_FAIL_COUNT=0" in text
    assert "MILESTONE_32_TASK_4_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_32_TASK_4_NEXT_STAGE=MILESTONE_32_TASK_5_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_REGRESSION_INTEGRATION_V1" in text


def test_task_5_persisted_regression_integration_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-5-boundary-regression-integration-report.json").read_text(encoding="utf-8"))

    assert validate_milestone_32_boundary_regression_integration_report(report)
    assert report["task_id"] == TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["task_5_signature"] == task_5_signature()
    assert report["integration_status"] == "VALID"
    assert report["integration_case_count"] == REGRESSION_CASE_COUNT
    assert report["pass_count"] == 12
    assert report["fail_count"] == 0
    assert report["integration_passed"] is True
    assert report["next_stage"] == NEXT_STAGE


def test_task_5_persisted_manifest_and_cases_match_report():
    report = json.loads((ARTIFACT_DIR / "task-5-boundary-regression-integration-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-5-manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((ARTIFACT_DIR / "task-5-boundary-regression-integration-cases.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert manifest["scope_lock_id"] == SCOPE_LOCK_ID
    assert manifest["integration_id"] == report["integration_id"]
    assert manifest["integration_signature"] == report["integration_signature"]
    assert manifest["integration_status"] == "VALID"
    assert manifest["integration_passed"] is True
    assert cases["task_id"] == TASK_ID
    assert cases["integration_id"] == report["integration_id"]
    assert cases["integration_status"] == "VALID"
    assert len(cases["integration_cases"]) == report["integration_case_count"]


def test_task_5_index_contains_canonical_regression_markers():
    index = (ARTIFACT_DIR / "task-5-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_5_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_REGRESSION_INTEGRATION_READY=true" in index
    assert f"TASK_ID={TASK_ID}" in index
    assert f"SOURCE_VALIDATION_TASK_ID={SOURCE_VALIDATION_TASK_ID}" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert "INTEGRATION_STATUS=VALID" in index
    assert "INTEGRATION_CASE_COUNT=12" in index
    assert "PASS_COUNT=12" in index
    assert "FAIL_COUNT=0" in index
    assert "INTEGRATION_PASSED=true" in index
    assert "LEGAL_CERTIFICATION=false" in index
    assert "IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT=false" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
