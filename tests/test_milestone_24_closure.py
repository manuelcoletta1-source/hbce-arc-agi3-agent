"""Tests for Milestone #24 closure."""

from __future__ import annotations

from hbce_arc_agi3.milestone_24_closure import (
    FAST_SOURCE_INTEGRATION_SNAPSHOT,
    FINAL_STATUS,
    MILESTONE_CLOSED,
    NEXT_STAGE,
    TASK_7_USED,
    TASK_8_USED,
    TASK_ID,
    build_fast_source_integration_snapshot,
    build_milestone_24_closure,
    validate_milestone_24_closure,
)


def test_fast_source_integration_snapshot() -> None:
    source = build_fast_source_integration_snapshot()

    assert source["taskId"] == "MILESTONE_24_TASK_5_INTEGRATION_REGRESSION_V1"
    assert source["valid"] is True
    assert source["integrationOk"] is True
    assert source["readyForMilestoneClosure"] is True
    assert source["task1Valid"] is True
    assert source["task2Valid"] is True
    assert source["task3Valid"] is True
    assert source["task4Valid"] is True
    assert source["snapshotCount"] == 3
    assert source["fastSourceValidationSnapshot"] is True


def test_milestone_24_closure_contract() -> None:
    closure = build_milestone_24_closure()

    assert TASK_ID == "MILESTONE_24_TASK_6_MILESTONE_CLOSURE_V1"
    assert NEXT_STAGE == "MILESTONE_24_CLOSED_NO_TASK_7_OR_8_USED"
    assert FINAL_STATUS == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert MILESTONE_CLOSED is True
    assert TASK_7_USED is False
    assert TASK_8_USED is False
    assert FAST_SOURCE_INTEGRATION_SNAPSHOT is True
    assert closure.final_task_number == 6
    assert closure.completed_task_count == 6
    assert closure.task_budget_max == 8
    assert closure.closure_ok is True
    assert closure.valid is True
    assert validate_milestone_24_closure(closure) == ()


def test_milestone_24_closure_public_payload() -> None:
    payload = build_milestone_24_closure().to_public_dict()

    assert payload["taskId"] == "MILESTONE_24_TASK_6_MILESTONE_CLOSURE_V1"
    assert payload["milestoneId"] == "MILESTONE_24"
    assert payload["nextStage"] == "MILESTONE_24_CLOSED_NO_TASK_7_OR_8_USED"
    assert payload["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert payload["technicalStatus"] == "PASS"
    assert payload["processStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
    assert payload["finalTaskNumber"] == 6
    assert payload["completedTaskCount"] == 6
    assert payload["task7Used"] is False
    assert payload["task8Used"] is False
    assert payload["noTask7Or8Used"] is True
    assert payload["milestoneClosed"] is True
    assert payload["readyForNextMilestone"] is True
    assert payload["sourceIntegrationValid"] is True
    assert payload["sourceReadyForMilestoneClosure"] is True
    assert payload["sourceFastValidationSnapshot"] is True
    assert payload["sourceSnapshotCount"] == 3
    assert payload["fastSourceIntegrationSnapshot"] is True
    assert payload["deepRecursiveDependencyTraversalAllowed"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["closureOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["closureId"].startswith("MILESTONE-24-CLOSURE-")
