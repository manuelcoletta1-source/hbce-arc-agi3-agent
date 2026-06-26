"""Milestone #25 Task 3 evidence bundle implementation validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_25_evidence_bundle import (
    build_closed_milestone_snapshot_query_result_evidence_bundle,
    generate_local_public_safe_evidence_manifest,
    summarize_evidence_bundle_integrity,
    validate_evidence_bundle_boundary,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "milestone-25-task-3-evidence-bundle-implementation-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_25_evidence_bundle.py"
MANIFEST = ROOT / "examples" / "milestone-25" / "evidence-bundle-implementation-v1" / "task-3-manifest.json"
JSON_ARTIFACT = ROOT / "examples" / "milestone-25" / "evidence-bundle-implementation-v1" / "task-3-evidence-bundle.json"
BOUNDARY = ROOT / "examples" / "milestone-25" / "evidence-bundle-implementation-v1" / "task-3-boundary-report.json"
SUMMARY = ROOT / "examples" / "milestone-25" / "evidence-bundle-implementation-v1" / "task-3-integrity-summary.json"
SOURCE_DOC = ROOT / "docs" / "milestone-25-task-2-objective-selection-and-scope-lock-v1.md"


def test_task_3_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MANIFEST.exists()
    assert JSON_ARTIFACT.exists()
    assert BOUNDARY.exists()
    assert SUMMARY.exists()
    assert SOURCE_DOC.exists()


def test_task_3_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")
    assert "MILESTONE_25_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in source
    assert "MILESTONE_25_TASK_2_SELECTED_OBJECTIVE_ID=CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY" in source
    assert "MILESTONE_25_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in source
    assert "MILESTONE_25_TASK_2_IMPLEMENTATION_STARTED=false" in source
    assert "MILESTONE_25_TASK_2_NEXT_STAGE=MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_IMPLEMENTATION_V1" in source


def test_task_3_bundle_contract() -> None:
    bundle = build_closed_milestone_snapshot_query_result_evidence_bundle()
    manifest = generate_local_public_safe_evidence_manifest(bundle)
    summary = summarize_evidence_bundle_integrity(bundle)

    assert bundle.valid is True
    assert bundle.bundle_ok is True
    assert bundle.query_result_item_count == 3
    assert bundle.registered_milestone_ids == ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22")
    assert validate_evidence_bundle_boundary(bundle) == ()
    assert manifest["valid"] is True
    assert summary["valid"] is True
    assert summary["issues"] == []


def test_task_3_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_IMPLEMENTED=true" in text
    assert "MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_VALID=true" in text
    assert "MILESTONE_25_TASK_3_MANIFEST_GENERATED=true" in text
    assert "MILESTONE_25_TASK_3_BOUNDARY_REPORT_VALID=true" in text
    assert "MILESTONE_25_TASK_3_INTEGRITY_SUMMARY_VALID=true" in text
    assert "MILESTONE_25_TASK_3_IMPLEMENTATION_COMPLETED=true" in text
    assert "MILESTONE_25_TASK_3_QUERY_RESULT_ITEM_COUNT=3" in text
    assert "MILESTONE_25_TASK_3_REGISTERED_MILESTONE_IDS=MILESTONE_20,MILESTONE_21,MILESTONE_22" in text
    assert "MILESTONE_25_TASK_3_FAST_SOURCE_SCOPE_LOCK_SNAPSHOT=true" in text
    assert "MILESTONE_25_TASK_3_NEXT_STAGE=MILESTONE_25_TASK_4_VALIDATION_AND_ARTIFACTS_V1" in text


def test_task_3_manifest_and_artifacts() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))
    boundary = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_IMPLEMENTATION_V1"
    assert manifest["evidenceBundleImplemented"] is True
    assert manifest["queryResultItemCount"] == 3
    assert manifest["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert manifest["nextStage"] == "MILESTONE_25_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert artifact["valid"] is True
    assert artifact["bundleOk"] is True
    assert artifact["issues"] == []
    assert boundary["valid"] is True
    assert boundary["issues"] == []
    assert summary["valid"] is True
    assert summary["issues"] == []
