"""Tests for Milestone #22 objective selection and scope lock."""

from __future__ import annotations

from hbce_arc_agi3.milestone_22_objective_scope_lock import (
    NEXT_STAGE,
    OBJECTIVE_SELECTION_READY,
    REVISION,
    SCOPE_LOCKED,
    SCOPE_LOCK_ID,
    SCOPE_LOCK_READY,
    TASK_ID,
    build_milestone_22_objective_scope_lock,
    validate_milestone_22_objective_scope_lock,
)


def test_scope_lock_contract() -> None:
    scope = build_milestone_22_objective_scope_lock(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_22_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert REVISION == "MILESTONE_22_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_v1"
    assert NEXT_STAGE == "MILESTONE_22_TASK_3_FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTATION_V1"
    assert SCOPE_LOCK_ID == "MILESTONE_22_SCOPE_FAST_SNAPSHOT_DEPENDENCY_GUARD_LOCAL_ONLY"
    assert OBJECTIVE_SELECTION_READY is True
    assert SCOPE_LOCK_READY is True
    assert SCOPE_LOCKED is True
    assert scope.task_budget_max == 8
    assert scope.current_task_number == 2
    assert scope.recommended_closure_task_number == 6
    assert scope.reserve_task_number == 7
    assert scope.emergency_only_task_number == 8
    assert len(scope.allowed_implementation_targets) == 4
    assert len(scope.forbidden_targets) == 10
    assert len(scope.scope_checks) == 10
    assert scope.scope_lock_ok is True
    assert scope.valid is True
    assert validate_milestone_22_objective_scope_lock(scope) == ()


def test_scope_lock_public_payload() -> None:
    payload = build_milestone_22_objective_scope_lock().to_public_dict()

    assert payload["taskId"] == "MILESTONE_22_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert payload["milestoneId"] == "MILESTONE_22"
    assert payload["nextStage"] == "MILESTONE_22_TASK_3_FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTATION_V1"
    assert payload["scopeLockId"] == "MILESTONE_22_SCOPE_FAST_SNAPSHOT_DEPENDENCY_GUARD_LOCAL_ONLY"
    assert "fast snapshot dependency guard" in payload["selectedObjective"]
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 2
    assert payload["remainingBudgetAfterCurrentTask"] == 6
    assert payload["recommendedClosureTaskNumber"] == 6
    assert payload["sourceOpeningValid"] is True
    assert payload["sourceOpeningTaskBudgetMax"] == 8
    assert payload["allowedImplementationTargetCount"] == 4
    assert payload["forbiddenTargetCount"] == 10
    assert payload["scopeCheckCount"] == 10
    assert payload["objectiveSelectionReady"] is True
    assert payload["scopeLockReady"] is True
    assert payload["scopeLocked"] is True
    assert payload["implementationAllowedNext"] is True
    assert payload["implementationStarted"] is False
    assert payload["fastSnapshotPatternRequired"] is True
    assert payload["deepRecursiveSerializationForbidden"] is True
    assert payload["documentBasedDependencyEvidenceRequired"] is True
    assert payload["closedMilestoneRevalidationAsRuntimeTraversalForbidden"] is True
    assert payload["milestone21Task7Required"] is False
    assert payload["milestone21Task8Required"] is False
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
    assert payload["lockRecordId"].startswith("MILESTONE-22-SCOPE-LOCK-")


def test_scope_lock_forbidden_targets_are_explicit() -> None:
    scope = build_milestone_22_objective_scope_lock()

    assert "runtime_solver_patch" in scope.forbidden_targets
    assert "runtime_wiring_activation" in scope.forbidden_targets
    assert "kaggle_submission" in scope.forbidden_targets
    assert "raw_request_body_persistence" in scope.forbidden_targets
    assert "secret_persistence" in scope.forbidden_targets
    assert "historical_milestone_rewrite" in scope.forbidden_targets
    assert "recursive_meta_layer" in scope.forbidden_targets
