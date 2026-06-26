"""Tests for Milestone #25 integration regression."""

from __future__ import annotations

from hbce_arc_agi3.milestone_25_integration_regression import (
    FAST_SOURCE_VALIDATION_SNAPSHOT,
    INTEGRATION_REGRESSION_EXECUTED,
    NEXT_STAGE,
    READY_FOR_MILESTONE_CLOSURE,
    TASK_ID,
    build_fast_source_validation_snapshot,
    build_milestone_25_integration_regression,
    validate_milestone_25_integration_regression,
)


def test_fast_source_validation_snapshot_contract() -> None:
    source = build_fast_source_validation_snapshot()

    assert source["taskId"] == "MILESTONE_25_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert source["milestoneId"] == "MILESTONE_25"
    assert source["validationArtifactsCreated"] is True
    assert source["evidenceBundleValidated"] is True
    assert source["evidenceManifestValidated"] is True
    assert source["boundaryReportValidated"] is True
    assert source["integritySummaryValidated"] is True
    assert source["readyForIntegrationRegression"] is True
    assert source["queryResultItemCount"] == 3
    assert source["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert source["valid"] is True
    assert source["validationOk"] is True
    assert source["issues"] == []


def test_integration_regression_contract() -> None:
    regression = build_milestone_25_integration_regression()

    assert TASK_ID == "MILESTONE_25_TASK_5_INTEGRATION_REGRESSION_V1"
    assert NEXT_STAGE == "MILESTONE_25_TASK_6_MILESTONE_CLOSURE_V1"
    assert INTEGRATION_REGRESSION_EXECUTED is True
    assert READY_FOR_MILESTONE_CLOSURE is True
    assert FAST_SOURCE_VALIDATION_SNAPSHOT is True
    assert regression.task_budget_max == 8
    assert regression.current_task_number == 5
    assert regression.remaining_budget_after_current_task == 3
    assert len(regression.regression_checks) == 14
    assert len(regression.generated_artifacts) == 5
    assert regression.regression_ok is True
    assert regression.valid is True
    assert validate_milestone_25_integration_regression(regression) == ()


def test_integration_regression_public_payload() -> None:
    payload = build_milestone_25_integration_regression().to_public_dict()

    assert payload["taskId"] == "MILESTONE_25_TASK_5_INTEGRATION_REGRESSION_V1"
    assert payload["milestoneId"] == "MILESTONE_25"
    assert payload["sourceTaskId"] == "MILESTONE_25_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert payload["nextStage"] == "MILESTONE_25_TASK_6_MILESTONE_CLOSURE_V1"
    assert payload["sourceValidationValid"] is True
    assert payload["sourceValidationOk"] is True
    assert payload["sourceValidationIssues"] == []
    assert payload["integrationRegressionExecuted"] is True
    assert payload["taskChainValidated"] is True
    assert payload["sourceArtifactsValidated"] is True
    assert payload["evidenceBundleRegressionValidated"] is True
    assert payload["boundaryRegressionValidated"] is True
    assert payload["integrityRegressionValidated"] is True
    assert payload["noMutationRegressionValidated"] is True
    assert payload["readyForMilestoneClosure"] is True
    assert payload["task1Valid"] is True
    assert payload["task2Valid"] is True
    assert payload["task3Valid"] is True
    assert payload["task4Valid"] is True
    assert payload["queryResultItemCount"] == 3
    assert payload["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert payload["regressionCheckCount"] == 14
    assert payload["generatedArtifactCount"] == 5
    assert payload["currentTaskNumber"] == 5
    assert payload["fastSourceValidationSnapshot"] is True
    assert payload["deepRecursiveDependencyTraversalAllowed"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["regressionOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["regressionId"].startswith("MILESTONE-25-INTEGRATION-REGRESSION-")
