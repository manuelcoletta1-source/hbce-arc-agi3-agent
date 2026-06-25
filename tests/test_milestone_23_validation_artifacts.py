"""Tests for Milestone #23 validation artifacts."""

from __future__ import annotations

from hbce_arc_agi3.milestone_23_validation_artifacts import (
    NEXT_STAGE,
    REVISION,
    TASK_ID,
    VALIDATION_ARTIFACTS_CREATED,
    VALIDATION_ARTIFACTS_READY,
    build_milestone_23_validation_artifacts,
    validate_milestone_23_validation_artifacts,
)


def test_validation_artifacts_contract() -> None:
    artifacts = build_milestone_23_validation_artifacts(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_23_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert REVISION == "MILESTONE_23_VALIDATION_AND_ARTIFACTS_v1"
    assert NEXT_STAGE == "MILESTONE_23_TASK_5_INTEGRATION_REGRESSION_V1"
    assert VALIDATION_ARTIFACTS_READY is True
    assert VALIDATION_ARTIFACTS_CREATED is True
    assert artifacts.task_budget_min == 4
    assert artifacts.task_budget_max == 8
    assert artifacts.current_task_number == 4
    assert artifacts.recommended_closure_task_number == 6
    assert artifacts.reserve_task_number == 7
    assert artifacts.emergency_only_task_number == 8
    assert len(artifacts.validation_cases) == 12
    assert len(artifacts.generated_artifacts) == 4
    assert artifacts.validation_ok is True
    assert artifacts.valid is True
    assert validate_milestone_23_validation_artifacts(artifacts) == ()


def test_validation_artifacts_public_payload() -> None:
    payload = build_milestone_23_validation_artifacts().to_public_dict()

    assert payload["taskId"] == "MILESTONE_23_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert payload["milestoneId"] == "MILESTONE_23"
    assert payload["nextStage"] == "MILESTONE_23_TASK_5_INTEGRATION_REGRESSION_V1"
    assert payload["sourceImplementationValid"] is True
    assert payload["sourceImplementationOk"] is True
    assert payload["registryValid"] is True
    assert payload["registrySnapshotCount"] == 3
    assert payload["registryValidSnapshotCount"] == 3
    assert payload["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert payload["requiredSnapshotFieldCount"] == 10
    assert payload["forbiddenTraversalTokenCount"] == 5
    assert payload["taskBudgetMin"] == 4
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 4
    assert payload["remainingBudgetAfterCurrentTask"] == 4
    assert payload["validationCaseCount"] == 12
    assert payload["generatedArtifactCount"] == 4
    assert payload["validationArtifactsReady"] is True
    assert payload["validationArtifactsCreated"] is True
    assert payload["registryValidated"] is True
    assert payload["lookupValidated"] is True
    assert payload["snapshotEvidenceValidated"] is True
    assert payload["forbiddenTraversalDetectionValidated"] is True
    assert payload["boundaryValidated"] is True
    assert payload["readyForIntegrationRegression"] is True
    assert payload["localOnly"] is True
    assert payload["deterministic"] is True
    assert payload["publicSafe"] is True
    assert payload["fastSnapshotDependencyMode"] is True
    assert payload["deepRecursiveDependencyTraversalAllowed"] is False
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
    assert payload["validationArtifactId"].startswith("MILESTONE-23-VALIDATION-ARTIFACTS-")


def test_validation_cases_are_explicit() -> None:
    artifacts = build_milestone_23_validation_artifacts()

    assert "source_task_3_implementation_valid" in artifacts.validation_cases
    assert "registry_valid" in artifacts.validation_cases
    assert "registry_snapshot_count_3" in artifacts.validation_cases
    assert "milestone_22_snapshot_lookup_valid" in artifacts.validation_cases
    assert "milestone_22_task7_unused_preserved" in artifacts.validation_cases
    assert "milestone_20_task7_used_preserved" in artifacts.validation_cases
    assert "forbidden_traversal_detection_valid" in artifacts.validation_cases
    assert "runtime_boundaries_unchanged" in artifacts.validation_cases
