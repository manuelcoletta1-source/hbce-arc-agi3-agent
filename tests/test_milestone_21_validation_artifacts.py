"""Tests for Milestone #21 validation and artifacts."""

from __future__ import annotations

from hbce_arc_agi3.milestone_21_validation_artifacts import (
    NEXT_STAGE,
    REVISION,
    TASK_ID,
    VALIDATION_ARTIFACTS_READY,
    build_handoff_validation_artifacts,
    validate_handoff_validation_artifacts,
)


def test_validation_artifacts_contract() -> None:
    artifacts = build_handoff_validation_artifacts(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_21_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert REVISION == "MILESTONE_21_VALIDATION_AND_ARTIFACTS_v1"
    assert NEXT_STAGE == "MILESTONE_21_TASK_5_INTEGRATION_REGRESSION_V1"
    assert VALIDATION_ARTIFACTS_READY is True
    assert artifacts.task_budget_max == 8
    assert artifacts.current_task_number == 4
    assert artifacts.recommended_closure_task_number == 6
    assert artifacts.reserve_task_number == 7
    assert artifacts.emergency_only_task_number == 8
    assert len(artifacts.validation_checks) == 8
    assert len(artifacts.artifact_names) == 4
    assert len(artifacts.carried_boundary_markers) == 7
    assert artifacts.validation_ok is True
    assert artifacts.valid is True
    assert validate_handoff_validation_artifacts(artifacts) == ()


def test_validation_artifacts_public_payload() -> None:
    payload = build_handoff_validation_artifacts().to_public_dict()

    assert payload["taskId"] == "MILESTONE_21_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert payload["milestoneId"] == "MILESTONE_21"
    assert payload["nextStage"] == "MILESTONE_21_TASK_5_INTEGRATION_REGRESSION_V1"
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 4
    assert payload["remainingBudgetAfterCurrentTask"] == 4
    assert payload["recommendedClosureTaskNumber"] == 6
    assert payload["sourceHandoffKind"] == "LOCAL_ONLY_OPERATOR_DECISION_HANDOFF_PACKAGE"
    assert payload["sourceHandoffScopeId"] == "MILESTONE_21_SCOPE_OPERATOR_DECISION_HANDOFF_LOCAL_ONLY"
    assert payload["sourceMilestone20FinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8"
    assert payload["sourceMilestone20Task8Used"] is False
    assert payload["scopeLocked"] is True
    assert payload["milestone20Task8Used"] is False
    assert payload["milestone20EmergencyReserveUnused"] is True
    assert payload["validationCheckCount"] == 8
    assert payload["artifactNameCount"] == 4
    assert payload["carriedBoundaryMarkerCount"] == 7
    assert payload["validationArtifactsReady"] is True
    assert payload["handoffPackageValidated"] is True
    assert payload["validationArtifactsCreated"] is True
    assert payload["artifactsLocalOnly"] is True
    assert payload["artifactsDeterministic"] is True
    assert payload["artifactsPublicSafe"] is True
    assert payload["artifactsReadyForIntegrationRegression"] is True
    assert payload["noRecursiveMetaLayer"] is True
    assert payload["milestone20Task8Required"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["rawRequestBodyPersisted"] is False
    assert payload["secretPersisted"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True
    assert payload["validationOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["validationArtifactId"].startswith("MILESTONE-21-VALIDATION-ARTIFACTS-")


def test_validation_artifacts_boundary_markers_are_explicit() -> None:
    artifacts = build_handoff_validation_artifacts()

    assert "runtimeSolverModified=false" in artifacts.carried_boundary_markers
    assert "runtimeWiringAllowed=false" in artifacts.carried_boundary_markers
    assert "kaggleSubmissionSent=false" in artifacts.carried_boundary_markers
    assert "rawRequestBodyPersisted=false" in artifacts.carried_boundary_markers
    assert "secretPersisted=false" in artifacts.carried_boundary_markers
    assert "legalCertification=false" in artifacts.carried_boundary_markers
    assert "failClosedActive=true" in artifacts.carried_boundary_markers
