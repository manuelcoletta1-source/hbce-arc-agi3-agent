"""Milestone #26 Task 3 archive index implementation validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_26_archive_index import (
    build_evidence_bundle_archive_index,
    validate_milestone_26_archive_index,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "milestone-26-task-3-archive-index-implementation-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_26_archive_index.py"
MANIFEST = ROOT / "examples" / "milestone-26" / "archive-index-implementation-v1" / "task-3-manifest.json"
REPORT = ROOT / "examples" / "milestone-26" / "archive-index-implementation-v1" / "task-3-archive-index.json"
ARCHIVE_MANIFEST = ROOT / "examples" / "milestone-26" / "archive-index-implementation-v1" / "task-3-archive-manifest.json"
BOUNDARY = ROOT / "examples" / "milestone-26" / "archive-index-implementation-v1" / "task-3-boundary-report.json"
INTEGRITY = ROOT / "examples" / "milestone-26" / "archive-index-implementation-v1" / "task-3-integrity-summary.json"
SOURCE_DOC = ROOT / "docs" / "milestone-26-task-2-objective-selection-and-scope-lock-v1.md"


def test_task_3_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MANIFEST.exists()
    assert REPORT.exists()
    assert ARCHIVE_MANIFEST.exists()
    assert BOUNDARY.exists()
    assert INTEGRITY.exists()
    assert SOURCE_DOC.exists()


def test_task_3_dependency_is_present() -> None:
    source = SOURCE_DOC.read_text(encoding="utf-8")
    assert "MILESTONE_26_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in source
    assert "MILESTONE_26_TASK_2_SELECTED_OBJECTIVE_ID=CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_ARCHIVE_INDEX_LOCAL_ONLY" in source
    assert "MILESTONE_26_TASK_2_SCOPE_LOCKED=true" in source
    assert "MILESTONE_26_TASK_2_IMPLEMENTATION_ALLOWED_NEXT=true" in source
    assert "MILESTONE_26_TASK_2_NEXT_STAGE=MILESTONE_26_TASK_3_ARCHIVE_INDEX_IMPLEMENTATION_V1" in source


def test_task_3_archive_index_contract() -> None:
    index = build_evidence_bundle_archive_index()
    assert index.valid is True
    assert index.archive_ok is True
    assert index.current_task_number == 3
    assert index.task_budget_max == 8
    assert index.remaining_budget_after_current_task == 5
    assert len(index.archive_items) == 3
    assert index.archived_milestone_ids == ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22")
    assert index.missing_archive_item_found is False
    assert index.invalid_archive_item_found is False
    assert index.task_8_used_found is False
    assert validate_milestone_26_archive_index(index) == ()


def test_task_3_doc_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_26_TASK_3_ARCHIVE_INDEX_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_26_TASK_3_ARCHIVE_INDEX_IMPLEMENTED=true" in text
    assert "MILESTONE_26_TASK_3_ARCHIVE_INDEX_VALID=true" in text
    assert "MILESTONE_26_TASK_3_ARCHIVE_MANIFEST_GENERATED=true" in text
    assert "MILESTONE_26_TASK_3_BOUNDARY_REPORT_VALID=true" in text
    assert "MILESTONE_26_TASK_3_INTEGRITY_SUMMARY_VALID=true" in text
    assert "MILESTONE_26_TASK_3_IMPLEMENTATION_COMPLETED=true" in text
    assert "MILESTONE_26_TASK_3_ARCHIVE_ITEM_COUNT=3" in text
    assert "MILESTONE_26_TASK_3_ARCHIVED_MILESTONE_IDS=MILESTONE_20,MILESTONE_21,MILESTONE_22" in text
    assert "MILESTONE_26_TASK_3_MISSING_ARCHIVE_ITEM_FOUND=false" in text
    assert "MILESTONE_26_TASK_3_INVALID_ARCHIVE_ITEM_FOUND=false" in text
    assert "MILESTONE_26_TASK_3_TASK_8_USED_FOUND=false" in text
    assert "MILESTONE_26_TASK_3_FAST_SOURCE_SCOPE_LOCK_SNAPSHOT=true" in text
    assert "MILESTONE_26_TASK_3_NEXT_STAGE=MILESTONE_26_TASK_4_VALIDATION_AND_ARTIFACTS_V1" in text


def test_task_3_manifest_and_artifacts() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    archive_manifest = json.loads(ARCHIVE_MANIFEST.read_text(encoding="utf-8"))
    boundary = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    integrity = json.loads(INTEGRITY.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_26_TASK_3_ARCHIVE_INDEX_IMPLEMENTATION_V1"
    assert manifest["archiveIndexImplemented"] is True
    assert manifest["archiveIndexValid"] is True
    assert manifest["archiveManifestGenerated"] is True
    assert manifest["boundaryReportValid"] is True
    assert manifest["integritySummaryValid"] is True
    assert manifest["implementationCompleted"] is True
    assert manifest["archiveItemCount"] == 3
    assert manifest["archivedMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert manifest["nextStage"] == "MILESTONE_26_TASK_4_VALIDATION_AND_ARTIFACTS_V1"

    assert report["valid"] is True
    assert report["archiveOk"] is True
    assert report["issues"] == []
    assert archive_manifest["valid"] is True
    assert boundary["valid"] is True
    assert boundary["issues"] == []
    assert integrity["valid"] is True
    assert integrity["issues"] == []
