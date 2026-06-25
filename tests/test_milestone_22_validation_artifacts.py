"""Tests for Milestone #22 validation artifacts."""

from __future__ import annotations

from hbce_arc_agi3.milestone_22_validation_artifacts import (
    NEXT_STAGE,
    REVISION,
    TASK_ID,
    VALIDATION_ARTIFACTS_CREATED,
    VALIDATION_ARTIFACTS_READY,
    build_milestone_22_validation_artifacts,
    validate_milestone_22_validation_artifacts,
)


def test_validation_artifacts_contract() -> None:
    artifacts = build_milestone_22_validation_artifacts(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_22_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert REVISION == "MILESTONE_22_VALIDATION_AND_ARTIFACTS_v1"
    assert NEXT_STAGE == "MILESTONE_22_TASK_5_INTEGRATION_REGRESSION_V1"
    assert VALIDATION_ARTIFACTS_READY is True
    assert VALIDATION_ARTIFACTS_CREATED is True
    assert artifacts.task_budget_max == 8
    assert artifacts.current_task_number == 4
    assert artifacts.recommended_closure_task_number == 6
    assert artifacts.reserve_task_number == 7
    assert artifacts.emergency_only_task_number == 8
    assert len(artifacts.validation_cases) == 10
    assert len(artifacts.generated_artifacts) == 4
    assert artifacts.validation_ok is True
    assert artifacts.valid is True
    assert validate_milestone_22_validation_artifacts(artifacts) == ()


def test_validation_artifacts_public_payload() -> None:
    payload = build_milestone_22_validation_artifacts().to_public_dict()

    assert payload["taskId"] == "MILESTONE_22_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert payload["milestoneId"] == "MILESTONE_22"
    assert payload["nextStage"] == "MILESTONE_22_TASK_5_INTEGRATION_REGRESSION_V1"
    assert payload["sourceGuardValid"] is True
    assert payload["sourceGuardSnapshotCount"] == 2
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 4
    assert payload["remainingBudgetAfterCurrentTask"] == 4
    assert payload["recommendedClosureTaskNumber"] == 6
    assert payload["validationCaseCount"] == 10
    assert payload["generatedArtifactCount"] == 4
    assert payload["detectedForbiddenTraversalSampleCount"] == 3
    assert payload["m21Task7Used"] is False
    assert payload["m21Task8Used"] is False
    assert payload["m20FinalTaskNumber"] == 7
    assert payload["m20Task7Used"] is True
    assert payload["m20Task8Used"] is False
    assert payload["requiredSnapshotFieldCount"] == 8
    assert payload["forbiddenRuntimeTraversalTokenCount"] == 5
    assert payload["validationArtifactsReady"] is True
    assert payload["validationArtifactsCreated"] is True
    assert payload["guardValidated"] is True
    assert payload["snapshotEvidenceValidated"] is True
    assert payload["forbiddenTraversalDetectionValidated"] is True
    assert payload["readyForIntegrationRegression"] is True
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["kaggleAuthenticationAllowed"] is False
    assert payload["kaggleUploadAllowed"] is False
    assert payload["rawRequestBodyPersisted"] is False
    assert payload["secretPersisted"] is False
    assert payload["legalCertification"] is False
    assert payload["historicalMilestoneRewrite"] is False
    assert payload["failClosedActive"] is True
    assert payload["validationOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["validationArtifactId"].startswith("MILESTONE-22-VALIDATION-ARTIFACTS-")


def test_validation_cases_are_explicit() -> None:
    artifacts = build_milestone_22_validation_artifacts()

    assert "guard_contract_valid" in artifacts.validation_cases
    assert "milestone_20_task7_snapshot_valid" in artifacts.validation_cases
    assert "forbidden_runtime_traversal_detection_valid" in artifacts.validation_cases
    assert "runtime_boundaries_unchanged" in artifacts.validation_cases
    assert "ready_for_integration_regression" in artifacts.validation_cases
