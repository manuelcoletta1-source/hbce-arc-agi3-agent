"""Tests for Milestone #27 governed opening."""

from __future__ import annotations

from hbce_arc_agi3.milestone_27_governed_opening import (
    FAST_SOURCE_CLOSURE_SNAPSHOT,
    GOVERNED_OPENING_READY,
    NEXT_STAGE,
    SOURCE_FINAL_STATUS,
    SOURCE_MILESTONE_ID,
    TASK_BUDGET_LOCKED,
    TASK_ID,
    build_fast_source_closure_snapshot,
    build_milestone_27_governed_opening,
    validate_milestone_27_governed_opening,
)


def test_fast_source_closure_snapshot_contract() -> None:
    source = build_fast_source_closure_snapshot()

    assert source["taskId"] == "MILESTONE_26_TASK_6_MILESTONE_CLOSURE_V1"
    assert source["milestoneId"] == "MILESTONE_26"
    assert source["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert source["technicalStatus"] == "PASS"
    assert source["processStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
    assert source["finalTaskNumber"] == 6
    assert source["completedTaskCount"] == 6
    assert source["task7Used"] is False
    assert source["task8Used"] is False
    assert source["milestoneClosed"] is True
    assert source["readyForNextMilestone"] is True
    assert source["closureOk"] is True
    assert source["valid"] is True
    assert source["issues"] == []


def test_governed_opening_contract() -> None:
    opening = build_milestone_27_governed_opening()

    assert TASK_ID == "MILESTONE_27_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
    assert SOURCE_MILESTONE_ID == "MILESTONE_26"
    assert SOURCE_FINAL_STATUS == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert NEXT_STAGE == "MILESTONE_27_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert GOVERNED_OPENING_READY is True
    assert TASK_BUDGET_LOCKED is True
    assert FAST_SOURCE_CLOSURE_SNAPSHOT is True
    assert opening.milestone_id == "MILESTONE_27"
    assert opening.task_budget_min == 4
    assert opening.task_budget_max == 8
    assert opening.current_task_number == 1
    assert opening.remaining_budget_after_current_task == 7
    assert len(opening.opening_checks) == 16
    assert len(opening.generated_artifacts) == 4
    assert opening.opening_ok is True
    assert opening.valid is True
    assert validate_milestone_27_governed_opening(opening) == ()


def test_governed_opening_public_payload() -> None:
    payload = build_milestone_27_governed_opening().to_public_dict()

    assert payload["taskId"] == "MILESTONE_27_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
    assert payload["milestoneId"] == "MILESTONE_27"
    assert payload["sourceMilestoneId"] == "MILESTONE_26"
    assert payload["sourceFinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert payload["sourceTechnicalStatus"] == "PASS"
    assert payload["sourceProcessStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
    assert payload["sourceFinalTaskNumber"] == 6
    assert payload["sourceCompletedTaskCount"] == 6
    assert payload["sourceTask7Used"] is False
    assert payload["sourceTask8Used"] is False
    assert payload["sourceMilestoneClosed"] is True
    assert payload["sourceReadyForNextMilestone"] is True
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 1
    assert payload["objectiveSelectionRequiredNext"] is True
    assert payload["scopeLockRequiredNext"] is True
    assert payload["implementationStarted"] is False
    assert payload["implementationAllowedAtTask1"] is False
    assert payload["fastSourceClosureSnapshot"] is True
    assert payload["deepRecursiveDependencyTraversalAllowed"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["openingOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["nextStage"] == "MILESTONE_27_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert payload["openingId"].startswith("MILESTONE-27-GOVERNED-OPENING-")
