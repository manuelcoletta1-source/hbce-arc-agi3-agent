import json
from pathlib import Path

from hbce_arc_agi3.milestone_29_query_result_evidence_bundle import (
    CURRENT_TASK_NUMBER,
    EVIDENCE_BUNDLE_REVISION,
    EVIDENCE_ITEM_COUNT,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    task_3_signature,
    validate_query_result_evidence_bundle,
)


DOC_PATH = Path("docs/milestone-29-task-3-query-result-evidence-bundle-implementation-v1.md")
SOURCE_DOC_PATH = Path("docs/milestone-29-task-2-objective-selection-and-scope-lock-v1.md")
ARTIFACT_DIR = Path("examples/milestone-29/query-result-evidence-bundle-implementation-v1")


def test_task_3_doc_declares_query_result_evidence_bundle_ready():
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_29_TASK_3_QUERY_RESULT_EVIDENCE_BUNDLE_IMPLEMENTATION_READY=true" in text
    assert f"MILESTONE_29_TASK_3_SOURCE_TASK_ID={SOURCE_TASK_ID}" in text
    assert f"MILESTONE_29_TASK_3_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_29_TASK_3_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert f"MILESTONE_29_TASK_3_EVIDENCE_BUNDLE_REVISION={EVIDENCE_BUNDLE_REVISION}" in text
    assert "MILESTONE_29_TASK_3_IMPLEMENTATION_STATUS=READY" in text
    assert "MILESTONE_29_TASK_3_IMPLEMENTATION_STARTED=true" in text
    assert "MILESTONE_29_TASK_3_IMPLEMENTATION_COMPLETE=true" in text
    assert "MILESTONE_29_TASK_3_SCOPE_LOCK_VALID=true" in text
    assert "MILESTONE_29_TASK_3_SOURCE_CHAIN_VALID=true" in text
    assert "MILESTONE_29_TASK_3_EVIDENCE_VALID=true" in text
    assert f"MILESTONE_29_TASK_3_EVIDENCE_ITEM_COUNT={EVIDENCE_ITEM_COUNT}" in text
    assert "MILESTONE_29_TASK_3_LOCAL_ONLY=true" in text
    assert "MILESTONE_29_TASK_3_NETWORK_ACCESS_ALLOWED=false" in text
    assert "MILESTONE_29_TASK_3_SHELL_EXECUTION_ALLOWED=false" in text
    assert f"MILESTONE_29_TASK_3_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}" in text
    assert f"MILESTONE_29_TASK_3_TASK_BUDGET_MAX={TASK_BUDGET_MAX}" in text
    assert f"MILESTONE_29_TASK_3_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}" in text
    assert f"MILESTONE_29_TASK_3_NEXT_STAGE={NEXT_STAGE}" in text


def test_task_3_dependency_keeps_task_2_scope_lock_intact():
    text = SOURCE_DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_29_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert f"MILESTONE_29_TASK_2_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert f"MILESTONE_29_TASK_2_SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in text
    assert "MILESTONE_29_TASK_2_OBJECTIVE_SELECTION_READY=true" in text
    assert "MILESTONE_29_TASK_2_SCOPE_LOCKED=true" in text
    assert "MILESTONE_29_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in text
    assert "MILESTONE_29_TASK_2_LOCAL_ONLY=true" in text
    assert "MILESTONE_29_TASK_2_NETWORK_ACCESS_ALLOWED=false" in text
    assert "MILESTONE_29_TASK_2_NEXT_STAGE=MILESTONE_29_TASK_3_QUERY_RESULT_EVIDENCE_BUNDLE_IMPLEMENTATION_V1" in text


def test_task_3_persisted_evidence_bundle_is_valid():
    bundle = json.loads((ARTIFACT_DIR / "task-3-evidence-bundle.json").read_text(encoding="utf-8"))

    assert validate_query_result_evidence_bundle(bundle)
    assert bundle["task_id"] == TASK_ID
    assert bundle["source_task_id"] == SOURCE_TASK_ID
    assert bundle["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert bundle["scope_lock_id"] == SCOPE_LOCK_ID
    assert bundle["evidence_bundle_revision"] == EVIDENCE_BUNDLE_REVISION
    assert bundle["task_3_signature"] == task_3_signature()
    assert bundle["implementation_status"] == "READY"
    assert bundle["implementation_started"] is True
    assert bundle["implementation_complete"] is True
    assert bundle["scope_lock_valid"] is True
    assert bundle["source_chain_valid"] is True
    assert bundle["evidence_valid"] is True
    assert bundle["evidence_item_count"] == EVIDENCE_ITEM_COUNT
    assert bundle["next_stage"] == NEXT_STAGE


def test_task_3_persisted_manifest_and_evidence_index_match_bundle():
    bundle = json.loads((ARTIFACT_DIR / "task-3-evidence-bundle.json").read_text(encoding="utf-8"))
    manifest = json.loads((ARTIFACT_DIR / "task-3-manifest.json").read_text(encoding="utf-8"))
    evidence_index = json.loads((ARTIFACT_DIR / "task-3-evidence-index.json").read_text(encoding="utf-8"))

    assert manifest["task_id"] == TASK_ID
    assert manifest["evidence_bundle_id"] == bundle["evidence_bundle_id"]
    assert manifest["evidence_bundle_signature"] == bundle["evidence_bundle_signature"]
    assert manifest["implementation_status"] == "READY"
    assert manifest["implementation_complete"] is True
    assert manifest["generated_artifact_count"] == 5
    assert evidence_index["task_id"] == TASK_ID
    assert evidence_index["evidence_bundle_id"] == bundle["evidence_bundle_id"]
    assert evidence_index["evidence_bundle_signature"] == bundle["evidence_bundle_signature"]
    assert evidence_index["evidence_item_count"] == bundle["evidence_item_count"]
    assert evidence_index["evidence_items"] == bundle["evidence_items"]


def test_task_3_index_contains_canonical_evidence_bundle_markers():
    index = (ARTIFACT_DIR / "task-3-index.txt").read_text(encoding="utf-8")

    assert "MILESTONE_29_TASK_3_QUERY_RESULT_EVIDENCE_BUNDLE_IMPLEMENTATION_READY=true" in index
    assert f"SOURCE_TASK_ID={SOURCE_TASK_ID}" in index
    assert f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in index
    assert f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}" in index
    assert "IMPLEMENTATION_STATUS=READY" in index
    assert "IMPLEMENTATION_STARTED=true" in index
    assert "IMPLEMENTATION_COMPLETE=true" in index
    assert "SCOPE_LOCK_VALID=true" in index
    assert "SOURCE_CHAIN_VALID=true" in index
    assert "EVIDENCE_VALID=true" in index
    assert f"EVIDENCE_ITEM_COUNT={EVIDENCE_ITEM_COUNT}" in index
    assert "LOCAL_ONLY=true" in index
    assert "NETWORK_ACCESS_ALLOWED=false" in index
    assert "SHELL_EXECUTION_ALLOWED=false" in index
    assert "REPOSITORY_MUTATION_ALLOWED=false" in index
    assert "REMOTE_REGISTRY_LOOKUP_ALLOWED=false" in index
    assert "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false" in index
    assert "EXTERNAL_MODEL_CALL_ALLOWED=false" in index
    assert f"NEXT_STAGE={NEXT_STAGE}" in index
