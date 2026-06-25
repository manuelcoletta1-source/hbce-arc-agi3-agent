"""Tests for Milestone #24 integration regression."""

from __future__ import annotations

from hbce_arc_agi3.milestone_24_integration_regression import (
    FAST_SOURCE_VALIDATION_SNAPSHOT,
    INTEGRATION_REGRESSION_EXECUTED,
    INTEGRATION_REGRESSION_READY,
    NEXT_STAGE,
    REVISION,
    TASK_ID,
    build_boundary_regression,
    build_milestone_24_integration_regression,
    build_regression_evidence,
    build_task_chain_snapshot,
    validate_milestone_24_integration_regression,
)


def test_integration_regression_contract() -> None:
    regression = build_milestone_24_integration_regression(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_24_TASK_5_INTEGRATION_REGRESSION_V1"
    assert REVISION == "MILESTONE_24_INTEGRATION_REGRESSION_FAST_SOURCE_VALIDATION_SNAPSHOT_v1"
    assert NEXT_STAGE == "MILESTONE_24_TASK_6_MILESTONE_CLOSURE_V1"
    assert INTEGRATION_REGRESSION_READY is True
    assert INTEGRATION_REGRESSION_EXECUTED is True
    assert FAST_SOURCE_VALIDATION_SNAPSHOT is True
    assert regression.task_budget_min == 4
    assert regression.task_budget_max == 8
    assert regression.current_task_number == 5
    assert regression.recommended_closure_task_number == 6
    assert len(regression.regression_cases) == 12
    assert len(regression.generated_artifacts) == 6
    assert regression.integration_ok is True
    assert regression.valid is True
    assert validate_milestone_24_integration_regression(regression) == ()


def test_task_chain_snapshot_contract() -> None:
    chain = build_task_chain_snapshot()

    assert chain["task1Valid"] is True
    assert chain["task1NextStage"] == "MILESTONE_24_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert chain["task2Valid"] is True
    assert chain["task2NextStage"] == "MILESTONE_24_TASK_3_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_IMPLEMENTATION_V1"
    assert chain["task2ImplementationAllowedNext"] is True
    assert chain["task3Valid"] is True
    assert chain["task3NextStage"] == "MILESTONE_24_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert chain["task3QueryInterfaceImplemented"] is True
    assert chain["task3SnapshotCount"] == 3
    assert chain["task4Valid"] is True
    assert chain["task4NextStage"] == "MILESTONE_24_TASK_5_INTEGRATION_REGRESSION_V1"
    assert chain["task4ReadyForIntegrationRegression"] is True


def test_regression_evidence_contract() -> None:
    evidence = build_regression_evidence()

    assert evidence["valid"] is True
    assert evidence["snapshotCount"] == 3
    assert evidence["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert evidence["queryEvidenceValid"] is True
    assert evidence["m20Task7Used"] is True
    assert evidence["m20Task8Used"] is False
    assert evidence["m21Task7Used"] is False
    assert evidence["m21Task8Used"] is False
    assert evidence["m22Task7Used"] is False
    assert evidence["m22Task8Used"] is False
    assert evidence["missingSnapshotFound"] is False
    assert evidence["missingSnapshotValid"] is False
    assert evidence["summaryM22Valid"] is True
    assert "MILESTONE_22 closed" in evidence["summaryM22Text"]
    assert evidence["localOnly"] is True
    assert evidence["readOnly"] is True
    assert evidence["legalCertification"] is False


def test_boundary_regression_contract() -> None:
    boundary = build_boundary_regression()

    assert boundary["valid"] is True
    assert boundary["sourceBoundaryReportValid"] is True
    assert boundary["validBoundaryCount"] == 3
    assert boundary["validBoundaryPassCount"] == 3
    assert boundary["brokenBoundaryValid"] is False
    assert "TASK_8_USED" in boundary["brokenBoundaryIssues"]
    assert boundary["localOnly"] is True
    assert boundary["readOnly"] is True
    assert boundary["legalCertification"] is False


def test_integration_regression_public_payload() -> None:
    payload = build_milestone_24_integration_regression().to_public_dict()

    assert payload["taskId"] == "MILESTONE_24_TASK_5_INTEGRATION_REGRESSION_V1"
    assert payload["milestoneId"] == "MILESTONE_24"
    assert payload["nextStage"] == "MILESTONE_24_TASK_6_MILESTONE_CLOSURE_V1"
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 5
    assert payload["task1Valid"] is True
    assert payload["task2Valid"] is True
    assert payload["task3Valid"] is True
    assert payload["task4Valid"] is True
    assert payload["task2ImplementationAllowedNext"] is True
    assert payload["task3QueryInterfaceImplemented"] is True
    assert payload["task3SnapshotCount"] == 3
    assert payload["task4ReadyForIntegrationRegression"] is True
    assert payload["integrationRegressionReady"] is True
    assert payload["integrationRegressionExecuted"] is True
    assert payload["taskChainValidated"] is True
    assert payload["sourceArtifactsValidated"] is True
    assert payload["queryInterfaceRegressionValidated"] is True
    assert payload["boundaryRegressionValidated"] is True
    assert payload["noMutationRegressionValidated"] is True
    assert payload["readyForMilestoneClosure"] is True
    assert payload["regressionCaseCount"] == 12
    assert payload["generatedArtifactCount"] == 6
    assert payload["snapshotCount"] == 3
    assert payload["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert payload["m20Task7Used"] is True
    assert payload["m20Task8Used"] is False
    assert payload["m21Task7Used"] is False
    assert payload["m21Task8Used"] is False
    assert payload["m22Task7Used"] is False
    assert payload["m22Task8Used"] is False
    assert payload["missingSnapshotFound"] is False
    assert payload["localOnly"] is True
    assert payload["readOnly"] is True
    assert payload["fastSourceValidationSnapshot"] is True
    assert payload["deepRecursiveDependencyTraversalAllowed"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["integrationOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["integrationId"].startswith("MILESTONE-24-INTEGRATION-REGRESSION-")
