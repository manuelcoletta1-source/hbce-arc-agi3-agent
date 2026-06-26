"""Tests for Milestone #25 validation and artifacts."""

from __future__ import annotations

from hbce_arc_agi3.milestone_25_validation_artifacts import (
    FAST_SOURCE_EVIDENCE_BUNDLE_SNAPSHOT,
    NEXT_STAGE,
    READY_FOR_INTEGRATION_REGRESSION,
    TASK_ID,
    VALIDATION_ARTIFACTS_CREATED,
    build_fast_source_evidence_bundle_snapshot,
    build_milestone_25_validation_artifacts,
    validate_milestone_25_validation_artifacts,
)


def test_fast_source_evidence_bundle_snapshot_contract() -> None:
    source = build_fast_source_evidence_bundle_snapshot()

    assert source["taskId"] == "MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_IMPLEMENTATION_V1"
    assert source["milestoneId"] == "MILESTONE_25"
    assert source["evidenceBundleImplemented"] is True
    assert source["evidenceBundleValid"] is True
    assert source["manifestGenerated"] is True
    assert source["boundaryReportValid"] is True
    assert source["integritySummaryValid"] is True
    assert source["queryResultItemCount"] == 3
    assert source["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert source["missingSnapshotFound"] is False
    assert source["invalidQueryResultFound"] is False
    assert source["task8UsedFound"] is False
    assert source["valid"] is True
    assert source["bundleOk"] is True
    assert source["issues"] == []


def test_validation_artifacts_contract() -> None:
    validation = build_milestone_25_validation_artifacts()

    assert TASK_ID == "MILESTONE_25_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert NEXT_STAGE == "MILESTONE_25_TASK_5_INTEGRATION_REGRESSION_V1"
    assert VALIDATION_ARTIFACTS_CREATED is True
    assert READY_FOR_INTEGRATION_REGRESSION is True
    assert FAST_SOURCE_EVIDENCE_BUNDLE_SNAPSHOT is True
    assert validation.task_budget_max == 8
    assert validation.current_task_number == 4
    assert validation.remaining_budget_after_current_task == 4
    assert len(validation.validation_cases) == 12
    assert len(validation.generated_artifacts) == 6
    assert validation.validation_ok is True
    assert validation.valid is True
    assert validate_milestone_25_validation_artifacts(validation) == ()


def test_validation_artifacts_public_payload() -> None:
    payload = build_milestone_25_validation_artifacts().to_public_dict()

    assert payload["taskId"] == "MILESTONE_25_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert payload["milestoneId"] == "MILESTONE_25"
    assert payload["sourceTaskId"] == "MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_IMPLEMENTATION_V1"
    assert payload["nextStage"] == "MILESTONE_25_TASK_5_INTEGRATION_REGRESSION_V1"
    assert payload["sourceEvidenceBundleValid"] is True
    assert payload["sourceEvidenceBundleOk"] is True
    assert payload["sourceEvidenceBundleIssues"] == []
    assert payload["evidenceBundleValidated"] is True
    assert payload["evidenceManifestValidated"] is True
    assert payload["boundaryReportValidated"] is True
    assert payload["integritySummaryValidated"] is True
    assert payload["validationArtifactsCreated"] is True
    assert payload["readyForIntegrationRegression"] is True
    assert payload["queryResultItemCount"] == 3
    assert payload["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert payload["missingSnapshotFound"] is False
    assert payload["invalidQueryResultFound"] is False
    assert payload["task8UsedFound"] is False
    assert payload["validationCaseCount"] == 12
    assert payload["generatedArtifactCount"] == 6
    assert payload["fastSourceEvidenceBundleSnapshot"] is True
    assert payload["deepRecursiveDependencyTraversalAllowed"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["validationOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["validationId"].startswith("MILESTONE-25-VALIDATION-")
