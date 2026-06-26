"""Tests for Milestone #26 validation artifacts."""

from __future__ import annotations

from hbce_arc_agi3.milestone_26_validation_artifacts import (
    ARCHIVE_INDEX_VALIDATED,
    FAST_SOURCE_ARCHIVE_INDEX_SNAPSHOT,
    NEXT_STAGE,
    READY_FOR_INTEGRATION_REGRESSION,
    TASK_ID,
    build_artifact_manifest,
    build_boundary_validation,
    build_fast_source_archive_index_snapshot,
    build_integrity_validation,
    build_milestone_26_validation_artifacts,
    build_validation_report,
    validate_milestone_26_validation_artifacts,
)


def test_fast_source_archive_index_snapshot_contract() -> None:
    source = build_fast_source_archive_index_snapshot()

    assert source["taskId"] == "MILESTONE_26_TASK_3_ARCHIVE_INDEX_IMPLEMENTATION_V1"
    assert source["milestoneId"] == "MILESTONE_26"
    assert source["archiveIndexImplemented"] is True
    assert source["archiveIndexValid"] is True
    assert source["archiveManifestGenerated"] is True
    assert source["boundaryReportValid"] is True
    assert source["integritySummaryValid"] is True
    assert source["implementationCompleted"] is True
    assert source["readyForValidationArtifacts"] is True
    assert source["archiveItemCount"] == 3
    assert source["archivedMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert source["valid"] is True
    assert source["archiveOk"] is True
    assert source["issues"] == []


def test_validation_artifacts_contract() -> None:
    validation = build_milestone_26_validation_artifacts()

    assert TASK_ID == "MILESTONE_26_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert NEXT_STAGE == "MILESTONE_26_TASK_5_INTEGRATION_REGRESSION_V1"
    assert ARCHIVE_INDEX_VALIDATED is True
    assert READY_FOR_INTEGRATION_REGRESSION is True
    assert FAST_SOURCE_ARCHIVE_INDEX_SNAPSHOT is True
    assert validation.current_task_number == 4
    assert validation.task_budget_max == 8
    assert validation.remaining_budget_after_current_task == 4
    assert len(validation.validation_cases) == 12
    assert len(validation.generated_artifacts) == 6
    assert validation.validation_ok is True
    assert validation.valid is True
    assert validate_milestone_26_validation_artifacts(validation) == ()


def test_validation_artifact_reports() -> None:
    validation = build_milestone_26_validation_artifacts()
    report = build_validation_report(validation)
    manifest = build_artifact_manifest(validation)
    boundary = build_boundary_validation(validation)
    integrity = build_integrity_validation(validation)

    assert report["valid"] is True
    assert report["validationOk"] is True
    assert report["issues"] == []
    assert report["archiveIndexValidated"] is True
    assert report["archiveItemCount"] == 3
    assert report["readyForIntegrationRegression"] is True

    assert manifest["valid"] is True
    assert manifest["validationArtifactsCreated"] is True
    assert manifest["archiveIndexValidated"] is True
    assert manifest["archiveManifestValidated"] is True
    assert manifest["boundaryReportValidated"] is True
    assert manifest["integritySummaryValidated"] is True
    assert manifest["readyForIntegrationRegression"] is True

    assert boundary["valid"] is True
    assert boundary["issues"] == []
    assert boundary["deepRecursiveDependencyTraversalAllowed"] is False
    assert boundary["runtimeSolverModified"] is False
    assert boundary["kaggleSubmissionSent"] is False
    assert boundary["legalCertification"] is False

    assert integrity["valid"] is True
    assert integrity["issues"] == []
    assert integrity["readyForIntegrationRegression"] is True
    assert integrity["archiveItemCount"] == 3
    assert integrity["archivedMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
