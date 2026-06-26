"""Tests for Milestone #25 evidence bundle implementation."""

from __future__ import annotations

from hbce_arc_agi3.milestone_25_evidence_bundle import (
    EVIDENCE_BUNDLE_IMPLEMENTED,
    FAST_SOURCE_SCOPE_LOCK_SNAPSHOT,
    NEXT_STAGE,
    READY_FOR_VALIDATION_ARTIFACTS,
    SELECTED_OBJECTIVE_ID,
    TASK_ID,
    build_closed_milestone_snapshot_query_result_evidence_bundle,
    build_fast_source_scope_lock_snapshot,
    generate_local_public_safe_evidence_manifest,
    summarize_evidence_bundle_integrity,
    validate_evidence_bundle_boundary,
)


def test_fast_source_scope_lock_snapshot_contract() -> None:
    source = build_fast_source_scope_lock_snapshot()

    assert source["taskId"] == "MILESTONE_25_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert source["milestoneId"] == "MILESTONE_25"
    assert source["selectedObjectiveId"] == "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"
    assert source["scopeLocked"] is True
    assert source["implementationAllowedNext"] is True
    assert source["implementationStarted"] is False
    assert source["valid"] is True


def test_evidence_bundle_contract() -> None:
    bundle = build_closed_milestone_snapshot_query_result_evidence_bundle()

    assert TASK_ID == "MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_IMPLEMENTATION_V1"
    assert SELECTED_OBJECTIVE_ID == "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"
    assert NEXT_STAGE == "MILESTONE_25_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert EVIDENCE_BUNDLE_IMPLEMENTED is True
    assert READY_FOR_VALIDATION_ARTIFACTS is True
    assert FAST_SOURCE_SCOPE_LOCK_SNAPSHOT is True
    assert bundle.current_task_number == 3
    assert bundle.task_budget_max == 8
    assert bundle.remaining_budget_after_current_task == 5
    assert bundle.query_result_item_count == 3
    assert bundle.registered_milestone_ids == ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22")
    assert bundle.missing_snapshot_found is False
    assert bundle.invalid_query_result_found is False
    assert bundle.task8_used_found is False
    assert bundle.bundle_ok is True
    assert bundle.valid is True
    assert validate_evidence_bundle_boundary(bundle) == ()


def test_evidence_manifest_and_integrity_summary() -> None:
    bundle = build_closed_milestone_snapshot_query_result_evidence_bundle()
    manifest = generate_local_public_safe_evidence_manifest(bundle)
    summary = summarize_evidence_bundle_integrity(bundle)

    assert manifest["bundleId"] == bundle.bundle_id
    assert manifest["queryResultItemCount"] == 3
    assert manifest["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert manifest["localOnly"] is True
    assert manifest["publicSafe"] is True
    assert manifest["legalCertification"] is False
    assert manifest["valid"] is True
    assert manifest["manifestId"].startswith("MILESTONE-25-EVIDENCE-MANIFEST-")

    assert summary["bundleId"] == bundle.bundle_id
    assert summary["valid"] is True
    assert summary["missingSnapshotFound"] is False
    assert summary["invalidQueryResultFound"] is False
    assert summary["task8UsedFound"] is False
    assert summary["implementationCompleted"] is True
    assert summary["readyForValidationArtifacts"] is True
    assert summary["issues"] == []


def test_evidence_bundle_public_payload() -> None:
    payload = build_closed_milestone_snapshot_query_result_evidence_bundle().to_public_dict()

    assert payload["taskId"] == "MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_IMPLEMENTATION_V1"
    assert payload["milestoneId"] == "MILESTONE_25"
    assert payload["selectedObjectiveId"] == "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"
    assert payload["nextStage"] == "MILESTONE_25_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert payload["evidenceBundleImplemented"] is True
    assert payload["evidenceBundleValid"] is True
    assert payload["manifestGenerated"] is True
    assert payload["boundaryReportValid"] is True
    assert payload["integritySummaryValid"] is True
    assert payload["implementationStarted"] is True
    assert payload["implementationCompleted"] is True
    assert payload["readyForValidationArtifacts"] is True
    assert payload["queryResultItemCount"] == 3
    assert payload["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert payload["missingSnapshotFound"] is False
    assert payload["invalidQueryResultFound"] is False
    assert payload["task8UsedFound"] is False
    assert payload["fastSourceScopeLockSnapshot"] is True
    assert payload["deepRecursiveDependencyTraversalAllowed"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["bundleOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["bundleId"].startswith("MILESTONE-25-EVIDENCE-BUNDLE-")
