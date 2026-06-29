import json
from pathlib import Path

from hbce_arc_agi3.milestone_32_objective_scope_lock import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    SCOPE_LOCK_CASE_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_OPENING_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_2_signature,
    validate_milestone_32_objective_scope_lock_report,
)


DOC_PATH = Path("docs/milestone-32-task-2-objective-selection-and-scope-lock-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-32-task-1-governed-opening-with-task-budget-v1.md")
ARTIFACT_DIR = Path("examples/milestone-32/objective-selection-and-scope-lock-v1")


def test_task_2_doc_declares_objective_scope_lock_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert f"MILESTONE_32_TASK_2_TASK_ID={TASK_ID}" in text
    assert f"MILESTONE_32_TASK_2_SOURCE_OPENING_TASK_ID={SOURCE_OPENING_TASK_ID}" in text
    assert f"MILESTONE_32_TASK_2_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert "MILESTONE_32_TASK_2_SELECTED_OBJECTIVE_STATUS=SELECTED_AND_SCOPE_LOCKED" in text
    assert f"MILESTONE_32_TASK_2_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert "MILESTONE_32_TASK_2_OPC_TECHNICAL_PROOF_RECEIPT_ONLY=true" in text
    assert "MILESTONE_32_TASK_2_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_32_TASK_2_IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE=true" in text
    assert "MILESTONE_32_TASK_2_IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT=false" in text
    assert "MILESTONE_32_TASK_2_SCOPE_LOCK_STATUS=LOCKED" in text
    assert f"MILESTONE_32_TASK_2_SCOPE_LOCK_CASE_COUNT={SCOPE_LOCK_CASE_COUNT}" in text
    assert "MILESTONE_32_TASK_2_PASS_COUNT=10" in text
    assert "MILESTONE_32_TASK_2_FAIL_COUNT=0" in text
    assert "MILESTONE_32_TASK_2_SCOPE_LOCK_PASSED=true" in text
    assert f"MILESTONE_32_TASK_2_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_32_TASK_2_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert f"MILESTONE_32_TASK_2_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_32_TASK_2_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_2_dependency_keeps_task_1_opening_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in text
    assert "MILESTONE_32_TASK_1_OPENING_STATUS=READY" in text
    assert "MILESTONE_32_TASK_1_OPENING_PASSED=true" in text
    assert "MILESTONE_32_TASK_1_NEXT_STAGE=MILESTONE_32_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1" in text


def test_task_2_persisted_scope_lock_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-2-objective-scope-lock-report.json").read_text(encoding="utf-8"))

    assert validate_milestone_32_objective_scope_lock_report(report)
    assert report["task_id"] == TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["task_2_signature"] == task_2_signature()
    assert report["scope_lock_status"] == "LOCKED"
    assert report["scope_lock_case_count"] == SCOPE_LOCK_CASE_COUNT
    assert report["pass_count"] == 10
    assert report["fail_count"] == 0
    assert report["scope_lock_passed"] is True
    assert report["next_stage"] == NEXT_STAGE


def test_task_2_persisted_manifest_and_cases_match_report():
    report = json.loads((ARTIFACT_DIR / "task-2-objective-scope-lock-report.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-2-manifest.json").read_text(encoding="utf-8"))
    cases = json.loads((ARTIFACT_DIR / "task-2-objective-scope-lock-cases.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert manifest["scope_lock_id"] == SCOPE_LOCK_ID
    assert manifest["scope_lock_instance_id"] == report["scope_lock_instance_id"]
    assert manifest["scope_lock_signature"] == report["scope_lock_signature"]
    assert manifest["scope_lock_status"] == "LOCKED"
    assert manifest["scope_lock_passed"] is True
    assert cases["task_id"] == TASK_ID
    assert cases["scope_lock_instance_id"] == report["scope_lock_instance_id"]
    assert cases["scope_lock_status"] == "LOCKED"
    assert len(cases["scope_lock_cases"]) == report["scope_lock_case_count"]


def test_task_2_index_contains_canonical_scope_lock_markers():
    index = (ARTIFACT_DIR / "task-2-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_32_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in index
    assert f"TASK_ID={TASK_ID}" in index
    assert f"SOURCE_OPENING_TASK_ID={SOURCE_OPENING_TASK_ID}" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert "OPC_TECHNICAL_PROOF_RECEIPT_ONLY=true" in index
    assert "LEGAL_CERTIFICATION=false" in index
    assert "IPR_CARD_INTERNAL_OPERATIONAL_IDENTITY_CERTIFICATE=true" in index
    assert "IPR_CARD_OFFICIAL_PUBLIC_IDENTITY_DOCUMENT=false" in index
    assert "SCOPE_LOCK_STATUS=LOCKED" in index
    assert "PASS_COUNT=10" in index
    assert "FAIL_COUNT=0" in index
    assert "SCOPE_LOCK_PASSED=true" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
