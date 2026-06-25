"""Tests for Milestone #22 governed opening."""

from __future__ import annotations

from hbce_arc_agi3.milestone_22_governed_opening import (
    MILESTONE_22_GOVERNED_OPENING_READY,
    NEXT_STAGE,
    REVISION,
    TASK_ID,
    build_milestone_22_governed_opening,
    validate_milestone_22_governed_opening,
)


def test_milestone_22_opening_contract() -> None:
    opening = build_milestone_22_governed_opening(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_22_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
    assert REVISION == "MILESTONE_22_GOVERNED_OPENING_WITH_TASK_BUDGET_FAST_SNAPSHOT_v1"
    assert NEXT_STAGE == "MILESTONE_22_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert MILESTONE_22_GOVERNED_OPENING_READY is True
    assert opening.task_budget_min == 4
    assert opening.task_budget_max == 8
    assert opening.current_task_number == 1
    assert opening.recommended_closure_task_number == 6
    assert opening.reserve_task_number == 7
    assert opening.emergency_only_task_number == 8
    assert len(opening.planned_task_labels) == 6
    assert len(opening.opening_checks) == 10
    assert opening.opening_ok is True
    assert opening.valid is True
    assert validate_milestone_22_governed_opening(opening) == ()


def test_milestone_22_public_payload() -> None:
    payload = build_milestone_22_governed_opening().to_public_dict()

    assert payload["taskId"] == "MILESTONE_22_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
    assert payload["milestoneId"] == "MILESTONE_22"
    assert payload["nextStage"] == "MILESTONE_22_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert payload["taskBudgetMin"] == 4
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 1
    assert payload["remainingBudgetAfterCurrentTask"] == 7
    assert payload["recommendedClosureTaskNumber"] == 6
    assert payload["reserveTaskNumber"] == 7
    assert payload["emergencyOnlyTaskNumber"] == 8
    assert payload["plannedTaskCount"] == 6
    assert payload["openingCheckCount"] == 10
    assert payload["milestone21FinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert payload["milestone21Task7Used"] is False
    assert payload["milestone21Task8Used"] is False
    assert payload["milestone21ReserveUnused"] is True
    assert payload["milestone21EmergencyReserveUnused"] is True
    assert payload["milestone20FinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8"
    assert payload["milestone20Task8Used"] is False
    assert payload["milestone19BudgetGuardActive"] is True
    assert payload["governedOpeningReady"] is True
    assert payload["implementationStarted"] is False
    assert payload["objectiveSelectionRequiredNext"] is True
    assert payload["scopeLockRequiredNext"] is True
    assert payload["closureRequired"] is True
    assert payload["noRecursiveMetaLayer"] is True
    assert payload["milestone21ReopenRequired"] is False
    assert payload["milestone21Task7Required"] is False
    assert payload["milestone21Task8Required"] is False
    assert payload["milestone20Task8Required"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["rawRequestBodyPersisted"] is False
    assert payload["secretPersisted"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True
    assert payload["openingOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["openingId"].startswith("MILESTONE-22-GOVERNED-OPENING-")


def test_milestone_22_task_plan_is_bounded() -> None:
    opening = build_milestone_22_governed_opening()

    assert opening.planned_task_labels[0] == "MILESTONE_22_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET"
    assert opening.planned_task_labels[-1] == "MILESTONE_22_TASK_6_MILESTONE_CLOSURE"
    assert opening.reserve_task_label == "MILESTONE_22_TASK_7_RESERVE_ONLY"
    assert opening.emergency_task_label == "MILESTONE_22_TASK_8_EMERGENCY_ONLY"
    assert len(opening.planned_task_labels) + 1 + 1 == 8
