"""Tests for Milestone #24 objective selection and scope lock."""

from __future__ import annotations

from hbce_arc_agi3.milestone_24_objective_scope_lock import (
    FAST_SOURCE_OPENING_SNAPSHOT,
    NEXT_STAGE,
    OBJECTIVE_SELECTION_READY,
    REVISION,
    SCOPE_LOCK_ID,
    SCOPE_LOCK_READY,
    SELECTED_OBJECTIVE_ID,
    TASK_ID,
    build_fast_source_opening_snapshot,
    build_milestone_24_objective_scope_lock,
    validate_milestone_24_objective_scope_lock,
)


def test_milestone_24_objective_scope_lock_contract() -> None:
    scope_lock = build_milestone_24_objective_scope_lock(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_24_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert REVISION == "MILESTONE_24_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_FAST_SOURCE_OPENING_SNAPSHOT_v1"
    assert NEXT_STAGE == "MILESTONE_24_TASK_3_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_IMPLEMENTATION_V1"
    assert SCOPE_LOCK_ID == "MILESTONE_24_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY"
    assert SELECTED_OBJECTIVE_ID == "CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY"
    assert OBJECTIVE_SELECTION_READY is True
    assert SCOPE_LOCK_READY is True
    assert FAST_SOURCE_OPENING_SNAPSHOT is True
    assert scope_lock.task_budget_min == 4
    assert scope_lock.task_budget_max == 8
    assert scope_lock.current_task_number == 2
    assert scope_lock.recommended_closure_task_number == 6
    assert len(scope_lock.allowed_query_operations) == 4
    assert len(scope_lock.forbidden_operations) == 5
    assert len(scope_lock.scope_checks) == 12
    assert scope_lock.lock_ok is True
    assert scope_lock.valid is True
    assert validate_milestone_24_objective_scope_lock(scope_lock) == ()


def test_fast_source_snapshot_contract() -> None:
    source = build_fast_source_opening_snapshot()

    assert source["valid"] is True
    assert source["openingOk"] is True
    assert source["sourceMilestoneId"] == "MILESTONE_23"
    assert source["sourceFinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert source["sourceTask7Used"] is False
    assert source["sourceTask8Used"] is False
    assert source["objectiveSelectionRequiredNext"] is True
    assert source["scopeLockRequiredNext"] is True
    assert source["implementationStarted"] is False
    assert source["implementationAllowedAtTask1"] is False


def test_milestone_24_objective_scope_lock_public_payload() -> None:
    payload = build_milestone_24_objective_scope_lock().to_public_dict()

    assert payload["taskId"] == "MILESTONE_24_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert payload["milestoneId"] == "MILESTONE_24"
    assert payload["sourceOpeningValid"] is True
    assert payload["sourceOpeningOk"] is True
    assert payload["sourceMilestoneId"] == "MILESTONE_23"
    assert payload["sourceFinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert payload["sourceTask7Used"] is False
    assert payload["sourceTask8Used"] is False
    assert payload["sourceObjectiveSelectionRequiredNext"] is True
    assert payload["sourceScopeLockRequiredNext"] is True
    assert payload["sourceImplementationStarted"] is False
    assert payload["sourceImplementationAllowedAtTask1"] is False
    assert payload["scopeLockId"] == "MILESTONE_24_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY"
    assert payload["selectedObjectiveId"] == "CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY"
    assert payload["selectedObjectiveTitle"] == "Closed Milestone Snapshot Query Interface Local Only"
    assert payload["allowedQueryOperationCount"] == 4
    assert payload["forbiddenOperationCount"] == 5
    assert payload["nextStage"] == "MILESTONE_24_TASK_3_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_IMPLEMENTATION_V1"
    assert payload["taskBudgetMin"] == 4
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 2
    assert payload["remainingBudgetAfterCurrentTask"] == 6
    assert payload["scopeCheckCount"] == 12
    assert payload["objectiveSelectionReady"] is True
    assert payload["scopeLockReady"] is True
    assert payload["objectiveSelected"] is True
    assert payload["scopeLocked"] is True
    assert payload["implementationAllowedNext"] is True
    assert payload["implementationStarted"] is False
    assert payload["queryInterfaceImplementationStarted"] is False
    assert payload["fastSourceOpeningSnapshot"] is True
    assert payload["deepRecursiveDependencyTraversalForbidden"] is True
    assert payload["runtimeSolverModified"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["lockOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["lockId"].startswith("MILESTONE-24-SCOPE-LOCK-")


def test_scope_operations_are_explicit() -> None:
    scope_lock = build_milestone_24_objective_scope_lock()

    assert "list_closed_milestone_snapshots" in scope_lock.allowed_query_operations
    assert "get_closed_milestone_snapshot" in scope_lock.allowed_query_operations
    assert "summarize_closed_milestone_snapshot" in scope_lock.allowed_query_operations
    assert "validate_query_result_boundary" in scope_lock.allowed_query_operations
    assert "mutate_closed_milestone_snapshot" in scope_lock.forbidden_operations
    assert "rewrite_historical_milestone" in scope_lock.forbidden_operations
    assert "deep_recursive_dependency_traversal" in scope_lock.forbidden_operations
    assert "runtime_solver_execution" in scope_lock.forbidden_operations
    assert "kaggle_submission" in scope_lock.forbidden_operations
