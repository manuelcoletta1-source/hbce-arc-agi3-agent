import json
from pathlib import Path

from hbce_arc_agi3.milestone_30_governed_opening import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    OPENING_REVISION,
    PROPOSED_OPERATOR_SEED_ID,
    PROPOSED_OPERATOR_SEED_STATUS,
    SOURCE_MILESTONE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_1_signature,
    validate_governed_opening_report,
)


DOC_PATH = Path("docs/milestone-30-task-1-governed-opening-with-task-budget-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-29-task-6-query-result-evidence-bundle-final-closure-v1.md")
ARTIFACT_DIR = Path("examples/milestone-30/governed-opening-with-task-budget-v1")


def test_task_1_doc_declares_milestone_30_governed_opening_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_30_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in text
    assert f"MILESTONE_30_TASK_1_SOURCE_TASK_ID={SOURCE_TASK_ID}" in text
    assert f"MILESTONE_30_TASK_1_SOURCE_MILESTONE_ID={SOURCE_MILESTONE_ID}" in text
    assert f"MILESTONE_30_TASK_1_OPENING_REVISION={OPENING_REVISION}" in text
    assert "MILESTONE_30_TASK_1_OPENING_STATUS=OPEN" in text
    assert "MILESTONE_30_TASK_1_TECHNICAL_STATUS=PASS" in text
    assert "MILESTONE_30_TASK_1_PROCESS_STATUS=GOVERNED_OPENING_WITH_TASK_BUDGET_MAX_8" in text
    assert "MILESTONE_30_TASK_1_SOURCE_DEPENDENCY_VALID=true" in text
    assert f"MILESTONE_30_TASK_1_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_30_TASK_1_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert "MILESTONE_30_TASK_1_IMPLEMENTATION_STARTED=false" in text
    assert "MILESTONE_30_TASK_1_IMPLEMENTATION_ALLOWED_AT_TASK_1=false" in text
    assert "MILESTONE_30_TASK_1_OBJECTIVE_SELECTION_REQUIRED_NEXT=true" in text
    assert "MILESTONE_30_TASK_1_SCOPE_LOCK_REQUIRED_NEXT=true" in text
    assert f"MILESTONE_30_TASK_1_PROPOSED_OPERATOR_SEED_ID={PROPOSED_OPERATOR_SEED_ID}" in text
    assert f"MILESTONE_30_TASK_1_PROPOSED_OPERATOR_SEED_STATUS={PROPOSED_OPERATOR_SEED_STATUS}" in text
    assert f"MILESTONE_30_TASK_1_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_30_TASK_1_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_1_dependency_keeps_milestone_29_final_closure_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_29_TASK_6_QUERY_RESULT_EVIDENCE_BUNDLE_FINAL_CLOSURE_READY=true" in text
    assert "MILESTONE_29_TASK_6_CLOSURE_STATUS=CLOSED" in text
    assert "MILESTONE_29_TASK_6_TECHNICAL_STATUS=PASS" in text
    assert "MILESTONE_29_TASK_6_PROCESS_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6" in text
    assert "MILESTONE_29_TASK_6_MILESTONE_CLOSED=true" in text
    assert "MILESTONE_29_TASK_6_READY_FOR_NEXT_MILESTONE=true" in text
    assert "MILESTONE_29_TASK_6_NEXT_STAGE=MILESTONE_30_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1" in text


def test_task_1_persisted_governed_opening_report_is_valid():
    report = json.loads((ARTIFACT_DIR / "task-1-governed-opening.json").read_text(encoding="utf-8"))

    assert validate_governed_opening_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["source_milestone_id"] == SOURCE_MILESTONE_ID
    assert report["opening_revision"] == OPENING_REVISION
    assert report["task_1_signature"] == task_1_signature()
    assert report["opening_status"] == "OPEN"
    assert report["technical_status"] == "PASS"
    assert report["source_dependency_valid"] is True
    assert report["implementation_started"] is False
    assert report["implementation_allowed_at_task_1"] is False
    assert report["objective_selection_required_next"] is True
    assert report["scope_lock_required_next"] is True
    assert report["proposed_operator_seed"]["seed_id"] == PROPOSED_OPERATOR_SEED_ID
    assert report["proposed_operator_seed"]["status"] == PROPOSED_OPERATOR_SEED_STATUS
    assert report["next_stage"] == NEXT_STAGE


def test_task_1_persisted_manifest_and_operator_seed_match_report():
    report = json.loads((ARTIFACT_DIR / "task-1-governed-opening.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-1-manifest.json").read_text(encoding="utf-8"))
    seed = json.loads((ARTIFACT_DIR / "task-1-operator-seed.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["opening_id"] == report["opening_id"]
    assert manifest["opening_signature"] == report["opening_signature"]
    assert manifest["opening_status"] == "OPEN"
    assert manifest["technical_status"] == "PASS"
    assert manifest["source_dependency_valid"] is True
    assert manifest["proposed_operator_seed_id"] == PROPOSED_OPERATOR_SEED_ID
    assert manifest["proposed_operator_seed_status"] == PROPOSED_OPERATOR_SEED_STATUS
    assert seed["task_id"] == TASK_ID
    assert seed["proposed_operator_seed"]["seed_id"] == PROPOSED_OPERATOR_SEED_ID
    assert seed["proposed_operator_seed"]["status"] == PROPOSED_OPERATOR_SEED_STATUS
    assert seed["implementation_status"] == "NOT_IMPLEMENTED_IN_TASK_1"
    assert seed["scope_lock_required_next"] is True


def test_task_1_index_contains_canonical_governed_opening_markers():
    index = (ARTIFACT_DIR / "task-1-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_30_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in index
    assert f"SOURCE_TASK_ID={SOURCE_TASK_ID}" in index
    assert f"SOURCE_MILESTONE_ID={SOURCE_MILESTONE_ID}" in index
    assert f"OPENING_REVISION={OPENING_REVISION}" in index
    assert "OPENING_STATUS=OPEN" in index
    assert "TECHNICAL_STATUS=PASS" in index
    assert "PROCESS_STATUS=GOVERNED_OPENING_WITH_TASK_BUDGET_MAX_8" in index
    assert "SOURCE_DEPENDENCY_VALID=true" in index
    assert "TASK_BUDGET_MAX=8" in index
    assert "CURRENT_TASK_NUMBER=1" in index
    assert "IMPLEMENTATION_STARTED=false" in index
    assert "IMPLEMENTATION_ALLOWED_AT_TASK_1=false" in index
    assert "OBJECTIVE_SELECTION_REQUIRED_NEXT=true" in index
    assert "SCOPE_LOCK_REQUIRED_NEXT=true" in index
    assert f"PROPOSED_OPERATOR_SEED_ID={PROPOSED_OPERATOR_SEED_ID}" in index
    assert f"PROPOSED_OPERATOR_SEED_STATUS={PROPOSED_OPERATOR_SEED_STATUS}" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
