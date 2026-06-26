"""Tests for Milestone #26 integration regression."""

from __future__ import annotations

from hbce_arc_agi3.milestone_26_integration_regression import (
    FAST_SOURCE_VALIDATION_SNAPSHOT,
    INTEGRATION_REGRESSION_READY,
    NEXT_STAGE,
    READY_FOR_MILESTONE_CLOSURE,
    TASK_CHAIN_VALIDATED,
    TASK_ID,
    build_fast_source_validation_snapshot,
    build_integration_regression_report,
    build_milestone_26_integration_regression,
    build_regression_boundary,
    validate_milestone_26_integration_regression,
)


def test_fast_source_validation_snapshot_contract() -> None:
    source = build_fast_source_validation_snapshot()

    assert source["taskId"] == "MILESTONE_26_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert source["milestoneId"] == "MILESTONE_26"
    assert source["archiveIndexValidated"] is True
    assert source["archiveManifestValidated"] is True
    assert source["boundaryReportValidated"] is True
    assert source["integritySummaryValidated"] is True
    assert source["readyForIntegrationRegression"] is True
    assert source["archiveItemCount"] == 3
    assert source["archivedMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert source["valid"] is True
    assert source["validationOk"] is True
    assert source["issues"] == []


def test_integration_regression_contract() -> None:
    regression = build_milestone_26_integration_regression()

    assert TASK_ID == "MILESTONE_26_TASK_5_INTEGRATION_REGRESSION_V1"
    assert NEXT_STAGE == "MILESTONE_26_TASK_6_MILESTONE_CLOSURE_V1"
    assert INTEGRATION_REGRESSION_READY is True
    assert TASK_CHAIN_VALIDATED is True
    assert READY_FOR_MILESTONE_CLOSURE is True
    assert FAST_SOURCE_VALIDATION_SNAPSHOT is True
    assert regression.current_task_number == 5
    assert regression.task_budget_max == 8
    assert regression.remaining_budget_after_current_task == 3
    assert len(regression.regression_checks) == 14
    assert len(regression.generated_artifacts) == 5
    assert regression.regression_ok is True
    assert regression.valid is True
    assert validate_milestone_26_integration_regression(regression) == ()


def test_integration_regression_reports() -> None:
    regression = build_milestone_26_integration_regression()
    report = build_integration_regression_report(regression)
    boundary = build_regression_boundary(regression)

    assert report["valid"] is True
    assert report["regressionOk"] is True
    assert report["issues"] == []
    assert report["taskChainValidated"] is True
    assert report["sourceArtifactsValidated"] is True
    assert report["archiveIndexRegressionValidated"] is True
    assert report["archiveManifestRegressionValidated"] is True
    assert report["boundaryRegressionValidated"] is True
    assert report["integrityRegressionValidated"] is True
    assert report["noMutationRegressionValidated"] is True
    assert report["readyForMilestoneClosure"] is True
    assert report["task1Valid"] is True
    assert report["task2Valid"] is True
    assert report["task3Valid"] is True
    assert report["task4Valid"] is True

    assert boundary["valid"] is True
    assert boundary["issues"] == []
    assert boundary["deepRecursiveDependencyTraversalAllowed"] is False
    assert boundary["runtimeSolverModified"] is False
    assert boundary["kaggleSubmissionSent"] is False
    assert boundary["legalCertification"] is False
    assert boundary["noMutationRegressionValidated"] is True
