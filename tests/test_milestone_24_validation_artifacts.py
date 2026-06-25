"""Tests for Milestone #24 validation artifacts."""

from __future__ import annotations

from hbce_arc_agi3.milestone_24_validation_artifacts import (
    NEXT_STAGE,
    REVISION,
    TASK_ID,
    VALIDATION_ARTIFACTS_CREATED,
    VALIDATION_ARTIFACTS_READY,
    build_boundary_report,
    build_milestone_24_validation_artifacts,
    build_query_evidence,
    validate_milestone_24_validation_artifacts,
)


def test_validation_artifacts_contract() -> None:
    validation = build_milestone_24_validation_artifacts(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_24_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert REVISION == "MILESTONE_24_VALIDATION_AND_ARTIFACTS_v1"
    assert NEXT_STAGE == "MILESTONE_24_TASK_5_INTEGRATION_REGRESSION_V1"
    assert VALIDATION_ARTIFACTS_READY is True
    assert VALIDATION_ARTIFACTS_CREATED is True
    assert validation.task_budget_min == 4
    assert validation.task_budget_max == 8
    assert validation.current_task_number == 4
    assert validation.recommended_closure_task_number == 6
    assert len(validation.validation_cases) == 12
    assert len(validation.generated_artifacts) == 6
    assert validation.validation_ok is True
    assert validation.valid is True
    assert validate_milestone_24_validation_artifacts(validation) == ()


def test_query_evidence_contract() -> None:
    evidence = build_query_evidence()

    assert evidence["valid"] is True
    assert evidence["snapshotCount"] == 3
    assert evidence["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert evidence["m20Found"] is True
    assert evidence["m20Task7Used"] is True
    assert evidence["m20Task8Used"] is False
    assert evidence["m22Found"] is True
    assert evidence["m22Task8Used"] is False
    assert evidence["missingSnapshotFound"] is False
    assert evidence["missingSnapshotValid"] is False
    assert evidence["summaryM22Found"] is True
    assert "MILESTONE_22 closed" in evidence["summaryM22Text"]
    assert evidence["localOnly"] is True
    assert evidence["readOnly"] is True
    assert evidence["legalCertification"] is False


def test_boundary_report_contract() -> None:
    boundary = build_boundary_report()

    assert boundary["valid"] is True
    assert boundary["validBoundaryCount"] == 3
    assert boundary["validBoundaryPassCount"] == 3
    assert boundary["brokenBoundaryValid"] is False
    assert "TASK_8_USED" in boundary["brokenBoundaryIssues"]
    assert boundary["requiredFieldCount"] == 10
    assert boundary["localOnly"] is True
    assert boundary["readOnly"] is True
    assert boundary["legalCertification"] is False


def test_validation_artifacts_public_payload() -> None:
    payload = build_milestone_24_validation_artifacts().to_public_dict()

    assert payload["taskId"] == "MILESTONE_24_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert payload["milestoneId"] == "MILESTONE_24"
    assert payload["sourceImplementationValid"] is True
    assert payload["sourceImplementationOk"] is True
    assert payload["sourceQueryInterfaceImplemented"] is True
    assert payload["sourceQueryInterfaceReadOnly"] is True
    assert payload["sourceSnapshotCount"] == 3
    assert payload["sourceRegisteredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert payload["sourceMissingSnapshotFound"] is False
    assert payload["nextStage"] == "MILESTONE_24_TASK_5_INTEGRATION_REGRESSION_V1"
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 4
    assert payload["validationCaseCount"] == 12
    assert payload["generatedArtifactCount"] == 6
    assert payload["queryEvidence"]["valid"] is True
    assert payload["boundaryReport"]["valid"] is True
    assert payload["validationArtifactsReady"] is True
    assert payload["validationArtifactsCreated"] is True
    assert payload["queryInterfaceValidated"] is True
    assert payload["queryOperationsValidated"] is True
    assert payload["boundaryValidated"] is True
    assert payload["readyForIntegrationRegression"] is True
    assert payload["localOnly"] is True
    assert payload["readOnly"] is True
    assert payload["deepRecursiveDependencyTraversalAllowed"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["validationOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["validationId"].startswith("MILESTONE-24-VALIDATION-")
