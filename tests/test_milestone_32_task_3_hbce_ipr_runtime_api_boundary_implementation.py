import json
from pathlib import Path

from hbce_arc_agi3.milestone_32_hbce_ipr_runtime_api_boundary import (
    BOUNDARY_MODE_ID,
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    IMPLEMENTATION_CASE_COUNT,
    IMPLEMENTATION_REVISION,
    NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_SCOPE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_3_signature,
    validate_milestone_32_boundary_implementation_report,
)


DOC_PATH = Path("docs/milestone-32-task-3-hbce-ipr-runtime-api-v1-operational-identity-and-proof-layer-boundary-implementation-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-32-task-2-objective-selection-and-scope-lock-v1.md")
ARTIFACT_DIR = Path("examples/milestone-32/hbce-ipr-runtime-api-v1-operational-identity-proof-layer-boundary-implementation-v1")


def test_task_3_doc_declares_boundary_implementation_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_3_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_IMPLEMENTATION_READY=true" in text
    assert f"MILESTONE_32_TASK_3_TASK_ID={TASK_ID}" in text
    assert f"MILESTONE_32_TASK_3_SOURCE_SCOPE_TASK_ID={SOURCE_SCOPE_TASK_ID}" in text
    assert f"MILESTONE_32_TASK_3_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_32_TASK_3_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_32_TASK_3_IMPLEMENTATION_REVISION={IMPLEMENTATION_REVISION}" in text
    assert f"MILESTONE_32_TASK_3_BOUNDARY_MODE_ID={BOUNDARY_MODE_ID}" in text
    assert "MILESTONE_32_TASK_3_IMPLEMENTATION_STATUS=READY" in text
    assert f"MILESTONE_32_TASK_3_IMPLEMENTATION_CASE_COUNT={IMPLEMENTATION_CASE_COUNT}" in text
    assert "MILESTONE_32_TASK_3_PASS_COUNT=11" in text
    assert "MILESTONE_32_TASK_3_FAIL_COUNT=0" in text
    assert "MILESTONE_32_TASK_3_IMPLEMENTATION_PASSED=true" in text
    assert "MILESTONE_32_TASK_3_OPC_TECHNICAL_PROOF_RECEIPT_ONLY=true" in text
    assert "MILESTONE_32_TASK_3_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_32_TASK_3_IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE=true" in text
    assert "MILESTONE_32_TASK_3_IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT=false" in text
    assert f"MILESTONE_32_TASK_3_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_32_TASK_3_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert f"MILESTONE_32_TASK_3_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_32_TASK_3_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_3_dependency_keeps_task_2_scope_lock_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert f"MILESTONE_32_TASK_2_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_32_TASK_2_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert "MILESTONE_32_TASK_2_SCOPE_LOCK_STATUS=LOCKED" in text
    assert "MILESTONE_32_TASK_2_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_32_TASK_2_IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT=false" in text
    assert "MILESTONE_32_TASK_2_NEXT_STAGE=MILESTONE_32_TASK_3_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_IMPLEMENTATION_V1" in text


def test_task_3_persisted_implementation_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-3-boundary-implementation-report.json").read_text(encoding="utf-8"))

    assert validate_milestone_32_boundary_implementation_report(report)
    assert report["task_id"] == TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["boundary_mode_id"] == BOUNDARY_MODE_ID
    assert report["task_3_signature"] == task_3_signature()
    assert report["implementation_status"] == "READY"
    assert report["implementation_case_count"] == IMPLEMENTATION_CASE_COUNT
    assert report["pass_count"] == 11
    assert report["fail_count"] == 0
    assert report["implementation_passed"] is True
    assert report["next_stage"] == NEXT_STAGE


def test_task_3_persisted_manifest_and_cases_match_report():
    report = json.loads((ARTIFACT_DIR / "task-3-boundary-implementation-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-3-manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((ARTIFACT_DIR / "task-3-boundary-implementation-cases.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert manifest["scope_lock_id"] == SCOPE_LOCK_ID
    assert manifest["implementation_id"] == report["implementation_id"]
    assert manifest["implementation_signature"] == report["implementation_signature"]
    assert manifest["implementation_status"] == "READY"
    assert manifest["implementation_passed"] is True
    assert cases["task_id"] == TASK_ID
    assert cases["implementation_id"] == report["implementation_id"]
    assert cases["implementation_status"] == "READY"
    assert len(cases["implementation_cases"]) == report["implementation_case_count"]


def test_task_3_index_contains_canonical_implementation_markers():
    index = (ARTIFACT_DIR / "task-3-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_3_HBCE_IPR_RUNTIME_API_V1_OPERATIONAL_IDENTITY_AND_PROOF_LAYER_BOUNDARY_IMPLEMENTATION_READY=true" in index
    assert f"TASK_ID={TASK_ID}" in index
    assert f"SOURCE_SCOPE_TASK_ID={SOURCE_SCOPE_TASK_ID}" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert f"BOUNDARY_MODE_ID={BOUNDARY_MODE_ID}" in index
    assert "IMPLEMENTATION_STATUS=READY" in index
    assert "PASS_COUNT=11" in index
    assert "FAIL_COUNT=0" in index
    assert "IMPLEMENTATION_PASSED=true" in index
    assert "OPC_TECHNICAL_PROOF_RECEIPT_ONLY=true" in index
    assert "LEGAL_CERTIFICATION=false" in index
    assert "IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT=false" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
