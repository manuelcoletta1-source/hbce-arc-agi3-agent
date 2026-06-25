"""Tests for Milestone #21 closure."""

from __future__ import annotations

from hbce_arc_agi3.milestone_21_closure import (
    MILESTONE_21_CLOSED,
    MILESTONE_21_CLOSURE_READY,
    MILESTONE_21_FINAL_STATUS,
    NEXT_STAGE,
    REVISION,
    TASK_ID,
    build_milestone_21_closure,
    validate_milestone_21_closure,
)


def test_milestone_21_closure_contract() -> None:
    closure = build_milestone_21_closure(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_21_TASK_6_MILESTONE_CLOSURE_V1"
    assert REVISION == "MILESTONE_21_MILESTONE_CLOSURE_v1"
    assert NEXT_STAGE == "MILESTONE_21_CLOSED_NO_TASK_7_OR_8_USED"
    assert MILESTONE_21_CLOSURE_READY is True
    assert MILESTONE_21_CLOSED is True
    assert MILESTONE_21_FINAL_STATUS == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert closure.task_budget_max == 8
    assert closure.final_task_number == 6
    assert closure.completed_task_count == 6
    assert closure.remaining_budget_after_closure == 2
    assert closure.reserve_task_number == 7
    assert closure.emergency_only_task_number == 8
    assert len(closure.closure_checks) == 10
    assert closure.closure_ok is True
    assert closure.valid is True
    assert validate_milestone_21_closure(closure) == ()


def test_milestone_21_closure_public_payload() -> None:
    payload = build_milestone_21_closure().to_public_dict()

    assert payload["taskId"] == "MILESTONE_21_TASK_6_MILESTONE_CLOSURE_V1"
    assert payload["milestoneId"] == "MILESTONE_21"
    assert payload["nextStage"] == "MILESTONE_21_CLOSED_NO_TASK_7_OR_8_USED"
    assert payload["taskBudgetMax"] == 8
    assert payload["finalTaskNumber"] == 6
    assert payload["completedTaskCount"] == 6
    assert payload["remainingBudgetAfterClosure"] == 2
    assert payload["reserveTaskNumber"] == 7
    assert payload["emergencyOnlyTaskNumber"] == 8
    assert payload["milestone20FinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8"
    assert payload["milestone20Task8Used"] is False
    assert payload["task5ReadyForMilestoneClosure"] is True
    assert payload["closureCheckCount"] == 10
    assert payload["closureReady"] is True
    assert payload["milestone21Closed"] is True
    assert payload["technicalStatus"] == "PASS"
    assert payload["processStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
    assert payload["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert payload["task7Used"] is False
    assert payload["task8Used"] is False
    assert payload["reserveUnused"] is True
    assert payload["emergencyReserveUnused"] is True
    assert payload["noRecursiveMetaLayer"] is True
    assert payload["closureCompleted"] is True
    assert payload["milestone20Task8Required"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["rawRequestBodyPersisted"] is False
    assert payload["secretPersisted"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True
    assert payload["closureOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["closureId"].startswith("MILESTONE-21-CLOSURE-")


def test_milestone_21_closure_stops_before_reserve_tasks() -> None:
    closure = build_milestone_21_closure()

    assert closure.completed_task_labels[-1] == "MILESTONE_21_TASK_6_MILESTONE_CLOSURE"
    assert closure.reserve_task_label == "MILESTONE_21_TASK_7_RESERVE_ONLY_UNUSED"
    assert closure.emergency_task_label == "MILESTONE_21_TASK_8_EMERGENCY_ONLY_UNUSED"
    assert len(closure.completed_task_labels) == 6
