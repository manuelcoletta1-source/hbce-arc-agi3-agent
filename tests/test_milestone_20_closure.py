"""Tests for Milestone #20 closure."""

from __future__ import annotations

from hbce_arc_agi3.milestone_20_closure import (
    MILESTONE_20_CLOSED,
    MILESTONE_20_CLOSURE_READY,
    MILESTONE_20_FINAL_STATUS,
    REVISION,
    TASK_ID,
    build_milestone_20_closure,
    validate_milestone_20_closure,
)


def test_milestone_20_closure_contract() -> None:
    closure = build_milestone_20_closure(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_20_TASK_7_MILESTONE_CLOSURE_V1"
    assert REVISION == "MILESTONE_20_CLOSURE_v1"
    assert MILESTONE_20_CLOSURE_READY is True
    assert MILESTONE_20_CLOSED is True
    assert MILESTONE_20_FINAL_STATUS == "CLOSED_WITH_TASK_BUDGET_MAX_8"
    assert closure.task_budget_max == 8
    assert closure.final_task_number == 7
    assert closure.completed_task_count == 7
    assert closure.emergency_reserve_task_number == 8
    assert closure.closure_ok is True
    assert closure.valid is True
    assert validate_milestone_20_closure(closure) == ()


def test_milestone_20_closure_public_payload() -> None:
    payload = build_milestone_20_closure().to_public_dict()

    assert payload["taskId"] == "MILESTONE_20_TASK_7_MILESTONE_CLOSURE_V1"
    assert payload["milestoneId"] == "MILESTONE_20"
    assert payload["taskBudgetMax"] == 8
    assert payload["finalTaskNumber"] == 7
    assert payload["completedTaskCount"] == 7
    assert payload["emergencyReserveTaskNumber"] == 8
    assert payload["task8Used"] is False
    assert payload["emergencyReserveUnused"] is True
    assert payload["noRecursiveMetaLayer"] is True
    assert payload["maxReviewDepth"] == 1
    assert payload["maxAuthorizationDepth"] == 1
    assert payload["maxFinalizationDepth"] == 1
    assert payload["reopenMilestone19Required"] is False
    assert payload["rewriteMilestone19Required"] is False
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
    assert payload["closureId"].startswith("MILESTONE-20-CLOSURE-")


def test_milestone_20_completed_task_labels_stop_at_7() -> None:
    closure = build_milestone_20_closure()

    assert closure.completed_task_labels[0] == "MILESTONE_20_TASK_1_OPERATOR_DECISION_GATE"
    assert closure.completed_task_labels[-1] == "MILESTONE_20_TASK_7_MILESTONE_CLOSURE"
    assert closure.emergency_only_task_label == "MILESTONE_20_TASK_8_EMERGENCY_RESERVE_ONLY_UNUSED"
    assert len(closure.completed_task_labels) == 7
