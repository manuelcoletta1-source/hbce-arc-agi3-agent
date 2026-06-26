"""Tests for Milestone #26 closure."""

from __future__ import annotations

from hbce_arc_agi3.milestone_26_closure import (
    FAST_SOURCE_INTEGRATION_SNAPSHOT,
    FINAL_STATUS,
    MILESTONE_CLOSED,
    NEXT_STAGE,
    PROCESS_STATUS,
    READY_FOR_NEXT_MILESTONE,
    TASK_ID,
    TECHNICAL_STATUS,
    build_fast_source_integration_snapshot,
    build_milestone_26_closure,
    build_milestone_26_final_summary,
    validate_milestone_26_closure,
)


def test_fast_source_integration_snapshot_contract() -> None:
    source = build_fast_source_integration_snapshot()

    assert source["taskId"] == "MILESTONE_26_TASK_5_INTEGRATION_REGRESSION_V1"
    assert source["milestoneId"] == "MILESTONE_26"
    assert source["integrationRegressionReady"] is True
    assert source["taskChainValidated"] is True
    assert source["sourceArtifactsValidated"] is True
    assert source["readyForMilestoneClosure"] is True
    assert source["task1Valid"] is True
    assert source["task2Valid"] is True
    assert source["task3Valid"] is True
    assert source["task4Valid"] is True
    assert source["archiveItemCount"] == 3
    assert source["archivedMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert source["valid"] is True
    assert source["regressionOk"] is True
    assert source["issues"] == []


def test_milestone_26_closure_contract() -> None:
    closure = build_milestone_26_closure()

    assert TASK_ID == "MILESTONE_26_TASK_6_MILESTONE_CLOSURE_V1"
    assert NEXT_STAGE == "MILESTONE_26_CLOSED_NO_TASK_7_OR_8_USED"
    assert FINAL_STATUS == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert TECHNICAL_STATUS == "PASS"
    assert PROCESS_STATUS == "GOVERNED_WITHIN_TASK_BUDGET"
    assert MILESTONE_CLOSED is True
    assert READY_FOR_NEXT_MILESTONE is True
    assert FAST_SOURCE_INTEGRATION_SNAPSHOT is True
    assert closure.closure_ok is True
    assert closure.valid is True
    assert len(closure.closure_checks) == 16
    assert len(closure.generated_artifacts) == 5
    assert validate_milestone_26_closure(closure) == ()


def test_milestone_26_final_summary() -> None:
    closure = build_milestone_26_closure()
    summary = build_milestone_26_final_summary(closure)

    assert summary["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert summary["technicalStatus"] == "PASS"
    assert summary["processStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
    assert summary["finalTaskNumber"] == 6
    assert summary["completedTaskCount"] == 6
    assert summary["task7Used"] is False
    assert summary["task8Used"] is False
    assert summary["reserveUnused"] is True
    assert summary["emergencyReserveUnused"] is True
    assert summary["noTask7Or8Used"] is True
    assert summary["milestoneClosed"] is True
    assert summary["readyForNextMilestone"] is True
    assert summary["archiveItemCount"] == 3
    assert summary["archivedMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert summary["valid"] is True
    assert summary["closureOk"] is True
    assert summary["issues"] == []
