"""Tests for Milestone #21 objective selection and scope lock."""

from __future__ import annotations

from hbce_arc_agi3.milestone_21_objective_scope_lock import (
    NEXT_STAGE,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE,
    REVISION,
    TASK_ID,
    build_milestone_21_objective_scope_lock,
    validate_milestone_21_objective_scope_lock,
)


def test_scope_lock_contract() -> None:
    lock = build_milestone_21_objective_scope_lock(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_21_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert REVISION == "MILESTONE_21_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_v1"
    assert SCOPE_LOCK_ID == "MILESTONE_21_SCOPE_OPERATOR_DECISION_HANDOFF_LOCAL_ONLY"
    assert NEXT_STAGE == "MILESTONE_21_TASK_3_SCOPED_OPERATOR_DECISION_HANDOFF_IMPLEMENTATION_V1"
    assert "operator decision handoff" in SELECTED_OBJECTIVE
    assert lock.task_budget_max == 8
    assert lock.current_task_number == 2
    assert lock.recommended_closure_task_number == 6
    assert lock.reserve_task_number == 7
    assert lock.emergency_only_task_number == 8
    assert len(lock.in_scope_items) == 5
    assert len(lock.out_of_scope_items) == 10
    assert lock.scope_lock_ok is True
    assert lock.valid is True
    assert validate_milestone_21_objective_scope_lock(lock) == ()


def test_scope_lock_public_payload() -> None:
    payload = build_milestone_21_objective_scope_lock().to_public_dict()

    assert payload["taskId"] == "MILESTONE_21_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert payload["milestoneId"] == "MILESTONE_21"
    assert payload["scopeLockId"] == "MILESTONE_21_SCOPE_OPERATOR_DECISION_HANDOFF_LOCAL_ONLY"
    assert payload["nextStage"] == "MILESTONE_21_TASK_3_SCOPED_OPERATOR_DECISION_HANDOFF_IMPLEMENTATION_V1"
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 2
    assert payload["remainingBudgetAfterCurrentTask"] == 6
    assert payload["recommendedClosureTaskNumber"] == 6
    assert payload["reserveTaskNumber"] == 7
    assert payload["emergencyOnlyTaskNumber"] == 8
    assert payload["inScopeItemCount"] == 5
    assert payload["outOfScopeItemCount"] == 10
    assert payload["objectiveSelected"] is True
    assert payload["scopeLockReady"] is True
    assert payload["scopeLocked"] is True
    assert payload["implementationAllowedNext"] is True
    assert payload["implementationStarted"] is False
    assert payload["closureRequired"] is True
    assert payload["noRecursiveMetaLayer"] is True
    assert payload["milestone20Task8Required"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["rawRequestBodyPersisted"] is False
    assert payload["secretPersisted"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True
    assert payload["scopeLockOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["lockRecordId"].startswith("MILESTONE-21-SCOPE-LOCK-")


def test_scope_items_are_explicit() -> None:
    lock = build_milestone_21_objective_scope_lock()

    assert "local_operator_decision_handoff_package" in lock.in_scope_items
    assert "next_task_implementation_contract" in lock.in_scope_items
    assert "runtime_solver_modification" in lock.out_of_scope_items
    assert "kaggle_submission" in lock.out_of_scope_items
    assert "milestone_20_task_8_use" in lock.out_of_scope_items
    assert "recursive_meta_layer" in lock.out_of_scope_items
