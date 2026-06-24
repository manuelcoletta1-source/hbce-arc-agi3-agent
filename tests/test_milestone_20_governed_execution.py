"""Tests for Milestone #20 governed execution."""

from __future__ import annotations

from hbce_arc_agi3.milestone_20_governed_execution import (
    MILESTONE_20_GOVERNED_EXECUTION_READY,
    MILESTONE_20_TASK_BUDGET_MAX,
    REVISION,
    TASK_ID,
    build_milestone_20_governed_execution,
    validate_milestone_20_governed_execution,
)


def test_milestone_20_governed_execution_contract() -> None:
    execution = build_milestone_20_governed_execution(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_20_TASK_5_GOVERNED_EXECUTION_BUDGET_ALIGNMENT_V1"
    assert REVISION == "MILESTONE_20_GOVERNED_EXECUTION_WITH_TASK_BUDGET_MAX_8_v1"
    assert MILESTONE_20_GOVERNED_EXECUTION_READY is True
    assert MILESTONE_20_TASK_BUDGET_MAX == 8
    assert execution.task_budget_max == 8
    assert execution.completed_task_count_at_alignment == 4
    assert execution.current_task_number == 5
    assert execution.recommended_closure_task_number == 7
    assert execution.emergency_reserve_task_count == 1
    assert execution.remaining_budget_after_current_task == 3
    assert execution.governed_execution_ok is True
    assert execution.valid is True
    assert validate_milestone_20_governed_execution(execution) == ()


def test_milestone_20_public_payload() -> None:
    payload = build_milestone_20_governed_execution().to_public_dict()

    assert payload["taskId"] == "MILESTONE_20_TASK_5_GOVERNED_EXECUTION_BUDGET_ALIGNMENT_V1"
    assert payload["milestoneId"] == "MILESTONE_20"
    assert payload["taskBudgetMax"] == 8
    assert payload["completedTaskCountAtAlignment"] == 4
    assert payload["currentTaskNumber"] == 5
    assert payload["recommendedClosureTaskNumber"] == 7
    assert payload["emergencyReserveTaskCount"] == 1
    assert payload["governedExecutionReady"] is True
    assert payload["governedExecutionOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["noRecursiveMetaLayer"] is True
    assert payload["maxReviewDepth"] == 1
    assert payload["maxAuthorizationDepth"] == 1
    assert payload["maxFinalizationDepth"] == 1
    assert payload["closureRequired"] is True
    assert payload["rewriteMilestone19Required"] is False
    assert payload["reopenMilestone19Required"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["rawRequestBodyPersisted"] is False
    assert payload["secretPersisted"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True
    assert payload["executionId"].startswith("MILESTONE-20-GOVERNED-EXECUTION-")


def test_milestone_20_task_labels_are_bounded() -> None:
    execution = build_milestone_20_governed_execution()

    assert len(execution.completed_task_labels) == 4
    assert len(execution.planned_remaining_task_labels) == 3
    assert execution.emergency_only_task_label == "MILESTONE_20_TASK_8_EMERGENCY_RESERVE_ONLY"
    assert len(execution.completed_task_labels) + len(execution.planned_remaining_task_labels) + execution.emergency_reserve_task_count == 8
