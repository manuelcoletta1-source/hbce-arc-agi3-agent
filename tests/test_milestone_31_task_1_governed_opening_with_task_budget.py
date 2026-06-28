import json
from pathlib import Path

from hbce_arc_agi3.milestone_31_governed_opening import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    MILESTONE_ID,
    NEXT_STAGE,
    OPENING_REVISION,
    PROCESS_STATUS,
    PROPOSED_OPERATOR_SEED_ID,
    PROPOSED_OPERATOR_SEED_STATUS,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_1_signature,
    validate_governed_opening_report,
)


DOC_PATH = Path("docs/milestone-31-task-1-governed-opening-with-task-budget-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-30-task-6-identity-boundary-fail-closed-final-closure-v1.md")
ARTIFACT_DIR = Path("examples/milestone-31/governed-opening-with-task-budget-v1")


def test_task_1_doc_declares_milestone_31_governed_opening_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_31_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in text
    assert f"MILESTONE_31_TASK_1_MILESTONE_ID={MILESTONE_ID}" in text
    assert f"MILESTONE_31_TASK_1_TASK_ID={TASK_ID}" in text
    assert f"MILESTONE_31_TASK_1_SOURCE_TASK_ID={SOURCE_TASK_ID}" in text
    assert f"MILESTONE_31_TASK_1_OPENING_REVISION={OPENING_REVISION}" in text
    assert "MILESTONE_31_TASK_1_OPENING_STATUS=OPEN" in text
    assert "MILESTONE_31_TASK_1_TECHNICAL_STATUS=PASS" in text
    assert f"MILESTONE_31_TASK_1_PROCESS_STATUS={PROCESS_STATUS}" in text
    assert "MILESTONE_31_TASK_1_SOURCE_DEPENDENCY_VALID=true" in text
    assert "MILESTONE_31_TASK_1_SOURCE_MILESTONE_CLOSED=true" in text
    assert "MILESTONE_31_TASK_1_SOURCE_READY_FOR_NEXT_MILESTONE=true" in text
    assert "MILESTONE_31_TASK_1_PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL=false" in text
    assert "MILESTONE_31_TASK_1_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_1_EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in text
    assert "MILESTONE_31_TASK_1_FAIL_CLOSED_DEFAULT=true" in text
    assert f"MILESTONE_31_TASK_1_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_31_TASK_1_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert "MILESTONE_31_TASK_1_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_31_TASK_1_IMPLEMENTATION_ALLOWED_AT_TASK_1=false" in text
    assert "MILESTONE_31_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT=true" in text
    assert "MILESTONE_31_TASK_1_SCOPE_LOCK_REQUIRED_NEXT=true" in text
    assert f"MILESTONE_31_TASK_1_PROPOSED_OPERATOR_SEED_ID={PROPOSED_OPERATOR_SEED_ID}" in text
    assert f"MILESTONE_31_TASK_1_PROPOSED_OPERATOR_SEED_STATUS={PROPOSED_OPERATOR_SEED_STATUS}" in text
    assert f"MILESTONE_31_TASK_1_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_31_TASK_1_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_1_dependency_keeps_milestone_30_final_closure_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_30_TASK_6_IDENTITY_BOUNDARY_FAIL_CLOSED_FINAL_CLOSURE_READY=true" in text
    assert "MILESTONE_30_TASK_6_CLOSURE_STATUS=CLOSED" in text
    assert "MILESTONE_30_TASK_6_TECHNICAL_STATUS=PASS" in text
    assert "MILESTONE_30_TASK_6_MILESTONE_CLOSED=true" in text
    assert "MILESTONE_30_TASK_6_READY_FOR_NEXT_MILESTONE=true" in text
    assert "MILESTONE_30_TASK_6_SOURCE_PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL=false" in text
    assert "MILESTONE_30_TASK_6_SOURCE_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in text
    assert "MILESTONE_30_TASK_6_SOURCE_EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in text
    assert "MILESTONE_30_TASK_6_TASK_7_UNUSED=true" in text
    assert "MILESTONE_30_TASK_6_TASK_8_UNUSED=true" in text
    assert "MILESTONE_30_TASK_6_NEXT_STAGE=MILESTONE_31_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1" in text


def test_task_1_persisted_governed_opening_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-1-governed-opening.json").read_text(encoding="utf-8"))

    assert validate_governed_opening_report(report)
    assert report["milestone_id"] == MILESTONE_ID
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["opening_revision"] == OPENING_REVISION
    assert report["task_1_signature"] == task_1_signature()
    assert report["opening_status"] == "OPEN"
    assert report["technical_status"] == "PASS"
    assert report["process_status"] == PROCESS_STATUS
    assert report["source_dependency_valid"] is True
    assert report["task_budget_max"] == 8
    assert report["current_task_number"] == 1
    assert report["implementation_started"] is False
    assert report["implementation_allowed_at_task_1"] is False
    assert report["objective_selection_required_next"] is True
    assert report["scope_lock_required_next"] is True
    assert report["proposed_operator_seed_status"] == "CANDIDATE_ONLY_NOT_LOCKED"
    assert report["next_stage"] == NEXT_STAGE


def test_task_1_persisted_manifest_and_seed_match_report():
    report = json.loads((ARTIFACT_DIR / "task-1-governed-opening.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-1-manifest.json").read_text(encoding="utf-8"))
    seed = json.loads((ARTIFACT_DIR / "task-1-proposed-operator-seed.json").read_text(encoding="utf-8"))

    assert manifest["milestone_id"] == MILESTONE_ID
    assert manifest["task_id"] == TASK_ID
    assert manifest["source_task_id"] == SOURCE_TASK_ID
    assert manifest["opening_id"] == report["opening_id"]
    assert manifest["opening_signature"] == report["opening_signature"]
    assert manifest["opening_status"] == "OPEN"
    assert manifest["technical_status"] == "PASS"
    assert manifest["source_dependency_valid"] is True
    assert seed["proposed_operator_seed_id"] == report["proposed_operator_seed_id"]
    assert seed["proposed_operator_seed_status"] == report["proposed_operator_seed_status"]
    assert seed["candidate_only"] is True
    assert seed["selected"] is False
    assert seed["scope_locked"] is False
    assert seed["implementation_started"] is False


def test_task_1_index_contains_canonical_governed_opening_markers():
    index = (ARTIFACT_DIR / "task-1-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_31_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in index
    assert f"MILESTONE_ID={MILESTONE_ID}" in index
    assert f"TASK_ID={TASK_ID}" in index
    assert f"SOURCE_TASK_ID={SOURCE_TASK_ID}" in index
    assert f"OPENING_REVISION={OPENING_REVISION}" in index
    assert "OPENING_STATUS=OPEN" in index
    assert "TECHNICAL_STATUS=PASS" in index
    assert f"PROCESS_STATUS={PROCESS_STATUS}" in index
    assert "SOURCE_DEPENDENCY_VALID=true" in index
    assert "SOURCE_MILESTONE_CLOSED=true" in index
    assert "SOURCE_READY_FOR_NEXT_MILESTONE=true" in index
    assert "PRIVATE_CORE_ACCESS_ALLOWED_WITHOUT_VERIFIED_MANUEL=false" in index
    assert "UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED=false" in index
    assert "EXTERNAL_COMMAND_AUTHORITY_ALLOWED=false" in index
    assert "FAIL_CLOSED_DEFAULT=true" in index
    assert "TASK_BUDGET_MAX=8" in index
    assert "CURRENT_TASK_NUMBER=1" in index
    assert "IMPLEMENTATION_STARTED=false" in index
    assert "IMPLEMENTATION_ALLOWED_AT_TASK_1=false" in index
    assert "OBJECTIVE_SELECTION_REQUIRED_NEXT=true" in index
    assert "SCOPE_LOCK_REQUIRED_NEXT=true" in index
    assert f"PROPOSED_OPERATOR_SEED_ID={PROPOSED_OPERATOR_SEED_ID}" in index
    assert "PROPOSED_OPERATOR_SEED_STATUS=CANDIDATE_ONLY_NOT_LOCKED" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
