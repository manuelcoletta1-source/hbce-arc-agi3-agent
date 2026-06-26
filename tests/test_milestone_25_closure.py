"""Tests for Milestone #25 closure."""

from __future__ import annotations

from hbce_arc_agi3.milestone_25_closure import (
    FAST_SOURCE_INTEGRATION_SNAPSHOT,
    FINAL_STATUS,
    MILESTONE_CLOSED,
    NEXT_STAGE,
    READY_FOR_NEXT_MILESTONE,
    TASK_ID,
    build_fast_source_integration_snapshot,
    build_milestone_25_closure,
    validate_milestone_25_closure,
)


def test_fast_source_integration_snapshot_contract() -> None:
    source = build_fast_source_integration_snapshot()

    assert source["taskId"] == "MILESTONE_25_TASK_5_INTEGRATION_REGRESSION_V1"
    assert source["milestoneId"] == "MILESTONE_25"
    assert source["integrationRegressionExecuted"] is True
    assert source["taskChainValidated"] is True
    assert source["readyForMilestoneClosure"] is True
    assert source["noMutationRegressionValidated"] is True
    assert source["queryResultItemCount"] == 3
    assert source["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert source["currentTaskNumber"] == 5
    assert source["valid"] is True
    assert source["regressionOk"] is True
    assert source["issues"] == []


def test_milestone_25_closure_contract() -> None:
    closure = build_milestone_25_closure()

    assert TASK_ID == "MILESTONE_25_TASK_6_MILESTONE_CLOSURE_V1"
    assert FINAL_STATUS == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert NEXT_STAGE == "MILESTONE_25_CLOSED_NO_TASK_7_OR_8_USED"
    assert MILESTONE_CLOSED is True
    assert READY_FOR_NEXT_MILESTONE is True
    assert FAST_SOURCE_INTEGRATION_SNAPSHOT is True
    assert closure.task_budget_max == 8
    assert closure.final_task_number == 6
    assert closure.completed_task_count == 6
    assert len(closure.closure_checks) == 16
    assert len(closure.generated_artifacts) == 5
    assert closure.closure_ok is True
    assert closure.valid is True
    assert validate_milestone_25_closure(closure) == ()


def test_milestone_25_closure_public_payload() -> None:
    payload = build_milestone_25_closure().to_public_dict()

    assert payload["taskId"] == "MILESTONE_25_TASK_6_MILESTONE_CLOSURE_V1"
    assert payload["milestoneId"] == "MILESTONE_25"
    assert payload["sourceTaskId"] == "MILESTONE_25_TASK_5_INTEGRATION_REGRESSION_V1"
    assert payload["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert payload["technicalStatus"] == "PASS"
    assert payload["processStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
    assert payload["finalTaskNumber"] == 6
    assert payload["completedTaskCount"] == 6
    assert payload["task7Used"] is False
    assert payload["task8Used"] is False
    assert payload["reserveUnused"] is True
    assert payload["emergencyReserveUnused"] is True
    assert payload["noTask7Or8Used"] is True
    assert payload["milestoneClosed"] is True
    assert payload["readyForNextMilestone"] is True
    assert payload["task1Valid"] is True
    assert payload["task2Valid"] is True
    assert payload["task3Valid"] is True
    assert payload["task4Valid"] is True
    assert payload["task5Valid"] is True
    assert payload["queryResultItemCount"] == 3
    assert payload["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert payload["fastSourceIntegrationSnapshot"] is True
    assert payload["deepRecursiveDependencyTraversalAllowed"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["closureOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["closureId"].startswith("MILESTONE-25-CLOSURE-")
