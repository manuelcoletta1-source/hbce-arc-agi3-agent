"""Tests for Milestone #23 integration regression."""

from __future__ import annotations

from hbce_arc_agi3.milestone_23_integration_regression import (
    INTEGRATION_REGRESSION_EXECUTED,
    INTEGRATION_REGRESSION_READY,
    NEXT_STAGE,
    READY_FOR_MILESTONE_CLOSURE,
    REVISION,
    TASK_ID,
    build_milestone_23_integration_regression,
    validate_milestone_23_integration_regression,
)


def test_integration_regression_contract() -> None:
    integration = build_milestone_23_integration_regression(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_23_TASK_5_INTEGRATION_REGRESSION_V1"
    assert REVISION == "MILESTONE_23_INTEGRATION_REGRESSION_v1"
    assert NEXT_STAGE == "MILESTONE_23_TASK_6_MILESTONE_CLOSURE_V1"
    assert INTEGRATION_REGRESSION_READY is True
    assert INTEGRATION_REGRESSION_EXECUTED is True
    assert READY_FOR_MILESTONE_CLOSURE is True
    assert integration.task_budget_min == 4
    assert integration.task_budget_max == 8
    assert integration.current_task_number == 5
    assert integration.recommended_closure_task_number == 6
    assert integration.reserve_task_number == 7
    assert integration.emergency_only_task_number == 8
    assert len(integration.integration_cases) == 16
    assert len(integration.generated_artifacts) == 4
    assert integration.integration_ok is True
    assert integration.valid is True
    assert validate_milestone_23_integration_regression(integration) == ()


def test_integration_regression_public_payload() -> None:
    payload = build_milestone_23_integration_regression().to_public_dict()

    assert payload["taskId"] == "MILESTONE_23_TASK_5_INTEGRATION_REGRESSION_V1"
    assert payload["milestoneId"] == "MILESTONE_23"
    assert payload["nextStage"] == "MILESTONE_23_TASK_6_MILESTONE_CLOSURE_V1"
    assert payload["sourceTask1Valid"] is True
    assert payload["sourceTask2Valid"] is True
    assert payload["sourceTask3Valid"] is True
    assert payload["sourceTask4Valid"] is True
    assert payload["registryValid"] is True
    assert payload["registrySnapshotCount"] == 3
    assert payload["registryValidSnapshotCount"] == 3
    assert payload["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert payload["taskBudgetMin"] == 4
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 5
    assert payload["remainingBudgetAfterCurrentTask"] == 3
    assert payload["integrationCaseCount"] == 16
    assert payload["generatedArtifactCount"] == 4
    assert payload["integrationRegressionReady"] is True
    assert payload["integrationRegressionExecuted"] is True
    assert payload["taskChainValidated"] is True
    assert payload["registryIntegrationValidated"] is True
    assert payload["artifactChainValidated"] is True
    assert payload["boundaryRegressionValidated"] is True
    assert payload["forbiddenTraversalRegressionValidated"] is True
    assert payload["staticLookupRegressionValidated"] is True
    assert payload["readyForMilestoneClosure"] is True
    assert payload["m20Task7Used"] is True
    assert payload["m20Task8Used"] is False
    assert payload["m21Task7Used"] is False
    assert payload["m21Task8Used"] is False
    assert payload["m22Task7Used"] is False
    assert payload["m22Task8Used"] is False
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
    assert payload["integrationOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["integrationId"].startswith("MILESTONE-23-INTEGRATION-REGRESSION-")


def test_integration_cases_are_explicit() -> None:
    integration = build_milestone_23_integration_regression()

    assert "task_1_governed_opening_valid" in integration.integration_cases
    assert "task_2_objective_scope_lock_valid" in integration.integration_cases
    assert "task_3_snapshot_registry_implementation_valid" in integration.integration_cases
    assert "task_4_validation_artifacts_valid" in integration.integration_cases
    assert "registry_lookup_m22_valid" in integration.integration_cases
    assert "m22_task7_unused_preserved" in integration.integration_cases
    assert "m22_task8_unused_preserved" in integration.integration_cases
    assert "forbidden_traversal_detection_regression_valid" in integration.integration_cases
    assert "runtime_boundary_regression_valid" in integration.integration_cases
