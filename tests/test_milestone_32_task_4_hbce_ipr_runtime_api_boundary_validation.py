import json
from pathlib import Path

from hbce_arc_agi3.milestone_32_hbce_ipr_runtime_api_boundary_validation import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_IMPLEMENTATION_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    VALIDATION_CASE_COUNT,
    VALIDATION_REVISION,
    task_4_signature,
    validate_milestone_32_boundary_validation_report,
)


DOC_PATH = Path("docs/milestone-32-task-4-hbce-ipr-runtime-api-v1-operational-identity-and-proof-layer-boundary-validation-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-32-task-3-hbce-ipr-runtime-api-v1-operational-identity-and-proof-layer-boundary-implementation-v1.md")
ARTIFACT_DIR = Path("examples/milestone-32/hbce-ipr-runtime-api-v1-operational-identity-proof-layer-boundary-validation-v1")


def test_task_4_doc_declares_boundary_validation_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_4_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_VALIDATION_READY=true" in text
    assert f"MILESTONE_32_TASK_4_TASK_ID={TASK_ID}" in text
    assert f"MILESTONE_32_TASK_4_SOURCE_IMPLEMENTATION_TASK_ID={SOURCE_IMPLEMENTATION_TASK_ID}" in text
    assert f"MILESTONE_32_TASK_4_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_32_TASK_4_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_32_TASK_4_VALIDATION_REVISION={VALIDATION_REVISION}" in text
    assert "MILESTONE_32_TASK_4_VALIDATION_STATUS=VALID" in text
    assert f"MILESTONE_32_TASK_4_VALIDATION_CASE_COUNT={VALIDATION_CASE_COUNT}" in text
    assert "MILESTONE_32_TASK_4_PASS_COUNT=12" in text
    assert "MILESTONE_32_TASK_4_FAIL_COUNT=0" in text
    assert "MILESTONE_32_TASK_4_VALIDATION_PASSED=true" in text
    assert "MILESTONE_32_TASK_4_OPC_TECHNICAL_PROOF_RECEIPT_ONLY=true" in text
    assert "MILESTONE_32_TASK_4_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_32_TASK_4_IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT=false" in text
    assert f"MILESTONE_32_TASK_4_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_32_TASK_4_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert f"MILESTONE_32_TASK_4_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_32_TASK_4_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_4_dependency_keeps_task_3_implementation_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_3_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_32_TASK_3_IMPLEMENTATION_STATUS=READY" in text
    assert "MILESTONE_32_TASK_3_PASS_COUNT=11" in text
    assert "MILESTONE_32_TASK_3_FAIL_COUNT=0" in text
    assert "MILESTONE_32_TASK_3_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_32_TASK_3_NEXT_STAGE=MILESTONE_32_TASK_4_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_VALIDATION_V1" in text


def test_task_4_persisted_validation_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-4-boundary-validation-report.json").read_text(encoding="utf-8"))

    assert validate_milestone_32_boundary_validation_report(report)
    assert report["task_id"] == TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["task_4_signature"] == task_4_signature()
    assert report["validation_status"] == "VALID"
    assert report["validation_case_count"] == VALIDATION_CASE_COUNT
    assert report["pass_count"] == 12
    assert report["fail_count"] == 0
    assert report["validation_passed"] is True
    assert report["next_stage"] == NEXT_STAGE


def test_task_4_persisted_manifest_and_cases_match_report():
    report = json.loads((ARTIFACT_DIR / "task-4-boundary-validation-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-4-manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((ARTIFACT_DIR / "task-4-boundary-validation-cases.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert manifest["scope_lock_id"] == SCOPE_LOCK_ID
    assert manifest["validation_id"] == report["validation_id"]
    assert manifest["validation_signature"] == report["validation_signature"]
    assert manifest["validation_status"] == "VALID"
    assert manifest["validation_passed"] is True
    assert cases["task_id"] == TASK_ID
    assert cases["validation_id"] == report["validation_id"]
    assert cases["validation_status"] == "VALID"
    assert len(cases["validation_cases"]) == report["validation_case_count"]


def test_task_4_index_contains_canonical_validation_markers():
    index = (ARTIFACT_DIR / "task-4-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_4_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_VALIDATION_READY=true" in index
    assert f"TASK_ID={TASK_ID}" in index
    assert f"SOURCE_IMPLEMENTATION_TASK_ID={SOURCE_IMPLEMENTATION_TASK_ID}" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert "VALIDATION_STATUS=VALID" in index
    assert "VALIDATION_CASE_COUNT=12" in index
    assert "PASS_COUNT=12" in index
    assert "FAIL_COUNT=0" in index
    assert "VALIDATION_PASSED=true" in index
    assert "OPC_TECHNICAL_PROOF_RECEIPT_ONLY=true" in index
    assert "LEGAL_CERTIFICATION=false" in index
    assert "IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT=false" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
