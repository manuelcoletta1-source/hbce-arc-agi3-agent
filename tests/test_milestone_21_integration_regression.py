"""Tests for Milestone #21 integration regression."""

from __future__ import annotations

from hbce_arc_agi3.milestone_21_integration_regression import (
    INTEGRATION_REGRESSION_READY,
    NEXT_STAGE,
    REVISION,
    TASK_ID,
    build_milestone_21_integration_regression,
    validate_milestone_21_integration_regression,
)


def test_integration_regression_contract() -> None:
    regression = build_milestone_21_integration_regression(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_21_TASK_5_INTEGRATION_REGRESSION_V1"
    assert REVISION == "MILESTONE_21_INTEGRATION_REGRESSION_v1"
    assert NEXT_STAGE == "MILESTONE_21_TASK_6_MILESTONE_CLOSURE_V1"
    assert INTEGRATION_REGRESSION_READY is True
    assert regression.task_budget_max == 8
    assert regression.current_task_number == 5
    assert regression.recommended_closure_task_number == 6
    assert regression.reserve_task_number == 7
    assert regression.emergency_only_task_number == 8
    assert len(regression.integrated_task_labels) == 5
    assert len(regression.regression_checks) == 9
    assert len(regression.regression_artifacts) == 4
    assert regression.integration_ok is True
    assert regression.valid is True
    assert validate_milestone_21_integration_regression(regression) == ()


def test_integration_regression_public_payload() -> None:
    payload = build_milestone_21_integration_regression().to_public_dict()

    assert payload["taskId"] == "MILESTONE_21_TASK_5_INTEGRATION_REGRESSION_V1"
    assert payload["milestoneId"] == "MILESTONE_21"
    assert payload["nextStage"] == "MILESTONE_21_TASK_6_MILESTONE_CLOSURE_V1"
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 5
    assert payload["remainingBudgetAfterCurrentTask"] == 3
    assert payload["recommendedClosureTaskNumber"] == 6
    assert payload["milestone20FinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8"
    assert payload["milestone20Task8Used"] is False
    assert payload["milestone20EmergencyReserveUnused"] is True
    assert payload["task1TaskBudgetMax"] == 8
    assert payload["task2ScopeLocked"] is True
    assert payload["task3HandoffPackageCreated"] is True
    assert payload["task4ArtifactsReadyForIntegrationRegression"] is True
    assert payload["integratedTaskCount"] == 5
    assert payload["regressionCheckCount"] == 9
    assert payload["regressionArtifactCount"] == 4
    assert payload["integrationRegressionReady"] is True
    assert payload["taskChainIntegrated"] is True
    assert payload["regressionChecksCreated"] is True
    assert payload["regressionChecksPassed"] is True
    assert payload["readyForMilestoneClosure"] is True
    assert payload["noRecursiveMetaLayer"] is True
    assert payload["closureRequired"] is True
    assert payload["milestone20Task8Required"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["rawRequestBodyPersisted"] is False
    assert payload["secretPersisted"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True
    assert payload["integrationOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["integrationRegressionId"].startswith("MILESTONE-21-INTEGRATION-REGRESSION-")


def test_integration_regression_checks_are_explicit() -> None:
    regression = build_milestone_21_integration_regression()

    assert "milestone_20_closed_task_8_unused" in regression.regression_checks
    assert "task_1_governed_opening_valid" in regression.regression_checks
    assert "task_2_scope_lock_valid" in regression.regression_checks
    assert "task_3_handoff_package_valid" in regression.regression_checks
    assert "task_4_validation_artifacts_valid" in regression.regression_checks
    assert "forbidden_actions_absent" in regression.regression_checks
    assert "fail_closed_boundary_preserved" in regression.regression_checks
