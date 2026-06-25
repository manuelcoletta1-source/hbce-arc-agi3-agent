"""Tests for Milestone #22 integration regression."""

from __future__ import annotations

from hbce_arc_agi3.milestone_22_integration_regression import (
    INTEGRATION_REGRESSION_EXECUTED,
    INTEGRATION_REGRESSION_READY,
    NEXT_STAGE,
    REVISION,
    TASK_ID,
    build_milestone_22_integration_regression,
    validate_milestone_22_integration_regression,
)


def test_integration_regression_contract() -> None:
    integration = build_milestone_22_integration_regression(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_22_TASK_5_INTEGRATION_REGRESSION_V1"
    assert REVISION == "MILESTONE_22_INTEGRATION_REGRESSION_v1"
    assert NEXT_STAGE == "MILESTONE_22_TASK_6_MILESTONE_CLOSURE_V1"
    assert INTEGRATION_REGRESSION_READY is True
    assert INTEGRATION_REGRESSION_EXECUTED is True
    assert integration.task_budget_max == 8
    assert integration.current_task_number == 5
    assert integration.recommended_closure_task_number == 6
    assert integration.reserve_task_number == 7
    assert integration.emergency_only_task_number == 8
    assert len(integration.integration_cases) == 12
    assert len(integration.generated_artifacts) == 4
    assert integration.integration_ok is True
    assert integration.valid is True
    assert validate_milestone_22_integration_regression(integration) == ()


def test_integration_regression_public_payload() -> None:
    payload = build_milestone_22_integration_regression().to_public_dict()

    assert payload["taskId"] == "MILESTONE_22_TASK_5_INTEGRATION_REGRESSION_V1"
    assert payload["milestoneId"] == "MILESTONE_22"
    assert payload["nextStage"] == "MILESTONE_22_TASK_6_MILESTONE_CLOSURE_V1"
    assert payload["sourceValidationValid"] is True
    assert payload["sourceGuardValid"] is True
    assert payload["sourceGuardSnapshotCount"] == 2
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 5
    assert payload["remainingBudgetAfterCurrentTask"] == 3
    assert payload["recommendedClosureTaskNumber"] == 6
    assert payload["integrationCaseCount"] == 12
    assert payload["generatedArtifactCount"] == 4
    assert payload["validationCaseCount"] == 10
    assert payload["taskChainValidated"] is True
    assert payload["guardIntegrationValidated"] is True
    assert payload["artifactChainValidated"] is True
    assert payload["boundaryRegressionValidated"] is True
    assert payload["integrationRegressionReady"] is True
    assert payload["integrationRegressionExecuted"] is True
    assert payload["readyForMilestoneClosure"] is True
    assert payload["m21Task7Used"] is False
    assert payload["m21Task8Used"] is False
    assert payload["m20FinalTaskNumber"] == 7
    assert payload["m20Task7Used"] is True
    assert payload["m20Task8Used"] is False
    assert payload["requiredSnapshotFieldCount"] == 8
    assert payload["forbiddenRuntimeTraversalTokenCount"] == 5
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
    assert payload["integrationOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["integrationId"].startswith("MILESTONE-22-INTEGRATION-REGRESSION-")


def test_integration_cases_are_explicit() -> None:
    integration = build_milestone_22_integration_regression()

    assert "task_1_governed_opening_dependency_valid" in integration.integration_cases
    assert "task_2_scope_lock_dependency_valid" in integration.integration_cases
    assert "task_3_fast_snapshot_guard_dependency_valid" in integration.integration_cases
    assert "task_4_validation_artifacts_dependency_valid" in integration.integration_cases
    assert "m20_task7_snapshot_preserved" in integration.integration_cases
    assert "m20_task8_unused_preserved" in integration.integration_cases
    assert "runtime_boundaries_unchanged" in integration.integration_cases
    assert "ready_for_milestone_closure" in integration.integration_cases
