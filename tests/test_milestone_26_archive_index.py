"""Tests for Milestone #26 archive index implementation."""

from __future__ import annotations

from hbce_arc_agi3.milestone_26_archive_index import (
    ARCHIVED_MILESTONE_IDS,
    ARCHIVE_INDEX_IMPLEMENTED,
    ARCHIVE_INDEX_VALID,
    ARCHIVE_ITEM_COUNT,
    FAST_SOURCE_SCOPE_LOCK_SNAPSHOT,
    NEXT_STAGE,
    TASK_ID,
    build_evidence_bundle_archive_index,
    build_fast_source_scope_lock_snapshot,
    generate_local_public_safe_archive_manifest,
    summarize_archive_index_integrity,
    validate_archive_index_boundary,
    validate_milestone_26_archive_index,
)


def test_fast_source_scope_lock_snapshot_contract() -> None:
    source = build_fast_source_scope_lock_snapshot()

    assert source["taskId"] == "MILESTONE_26_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert source["milestoneId"] == "MILESTONE_26"
    assert source["selectedObjectiveId"] == "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_ARCHIVE_INDEX_LOCAL_ONLY"
    assert source["scopeLocked"] is True
    assert source["implementationAllowedNext"] is True
    assert source["implementationStarted"] is False
    assert source["archiveIndexImplementationStarted"] is False
    assert source["valid"] is True
    assert source["lockOk"] is True
    assert source["issues"] == []


def test_archive_index_contract() -> None:
    index = build_evidence_bundle_archive_index()

    assert TASK_ID == "MILESTONE_26_TASK_3_ARCHIVE_INDEX_IMPLEMENTATION_V1"
    assert NEXT_STAGE == "MILESTONE_26_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert ARCHIVE_INDEX_IMPLEMENTED is True
    assert ARCHIVE_INDEX_VALID is True
    assert ARCHIVE_ITEM_COUNT == 3
    assert ARCHIVED_MILESTONE_IDS == ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22")
    assert FAST_SOURCE_SCOPE_LOCK_SNAPSHOT is True
    assert index.current_task_number == 3
    assert index.task_budget_max == 8
    assert index.remaining_budget_after_current_task == 5
    assert len(index.archive_items) == 3
    assert index.archived_milestone_ids == ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22")
    assert index.missing_archive_item_found is False
    assert index.invalid_archive_item_found is False
    assert index.task_8_used_found is False
    assert len(index.archive_checks) == 14
    assert len(index.generated_artifacts) == 7
    assert index.archive_ok is True
    assert index.valid is True
    assert validate_milestone_26_archive_index(index) == ()


def test_archive_index_generated_reports() -> None:
    index = build_evidence_bundle_archive_index()
    manifest = generate_local_public_safe_archive_manifest(index)
    boundary = validate_archive_index_boundary(index)
    summary = summarize_archive_index_integrity(index)

    assert manifest["valid"] is True
    assert manifest["archiveItemCount"] == 3
    assert manifest["archivedMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert manifest["localOnly"] is True
    assert manifest["publicSafe"] is True
    assert manifest["legalCertification"] is False

    assert boundary["valid"] is True
    assert boundary["issues"] == []
    assert boundary["deepRecursiveDependencyTraversalAllowed"] is False
    assert boundary["runtimeSolverModified"] is False
    assert boundary["kaggleSubmissionSent"] is False
    assert boundary["legalCertification"] is False

    assert summary["valid"] is True
    assert summary["issues"] == []
    assert summary["archiveIndexImplemented"] is True
    assert summary["archiveIndexValid"] is True
    assert summary["implementationCompleted"] is True
    assert summary["readyForValidationArtifacts"] is True


def test_archive_index_public_payload() -> None:
    payload = build_evidence_bundle_archive_index().to_public_dict()

    assert payload["taskId"] == "MILESTONE_26_TASK_3_ARCHIVE_INDEX_IMPLEMENTATION_V1"
    assert payload["milestoneId"] == "MILESTONE_26"
    assert payload["sourceTaskId"] == "MILESTONE_26_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert payload["nextStage"] == "MILESTONE_26_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert payload["archiveIndexImplemented"] is True
    assert payload["archiveIndexValid"] is True
    assert payload["archiveManifestGenerated"] is True
    assert payload["boundaryReportValid"] is True
    assert payload["integritySummaryValid"] is True
    assert payload["implementationStarted"] is True
    assert payload["implementationCompleted"] is True
    assert payload["readyForValidationArtifacts"] is True
    assert payload["archiveItemCount"] == 3
    assert payload["archivedMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert payload["missingArchiveItemFound"] is False
    assert payload["invalidArchiveItemFound"] is False
    assert payload["task8UsedFound"] is False
    assert payload["currentTaskNumber"] == 3
    assert payload["fastSourceScopeLockSnapshot"] is True
    assert payload["deepRecursiveDependencyTraversalAllowed"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["archiveOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["archiveIndexId"].startswith("MILESTONE-26-ARCHIVE-INDEX-")
