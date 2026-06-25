"""Tests for Milestone #23 objective scope lock."""

from __future__ import annotations

from hbce_arc_agi3.milestone_23_objective_scope_lock import (
    NEXT_STAGE,
    OBJECTIVE_SELECTION_READY,
    SCOPE_LOCKED,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    REVISION,
    TASK_ID,
    build_milestone_23_objective_scope_lock,
    validate_milestone_23_objective_scope_lock,
)


def test_objective_scope_lock_contract() -> None:
    lock = build_milestone_23_objective_scope_lock(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_23_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert REVISION == "MILESTONE_23_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_v1"
    assert NEXT_STAGE == "MILESTONE_23_TASK_3_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_IMPLEMENTATION_V1"
    assert SCOPE_LOCK_ID == "MILESTONE_23_SCOPE_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY"
    assert SELECTED_OBJECTIVE_ID == "CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY"
    assert OBJECTIVE_SELECTION_READY is True
    assert SCOPE_LOCKED is True
    assert lock.task_budget_min == 4
    assert lock.task_budget_max == 8
    assert lock.current_task_number == 2
    assert lock.recommended_closure_task_number == 6
    assert lock.reserve_task_number == 7
    assert lock.emergency_only_task_number == 8
    assert len(lock.objective_candidates) == 3
    assert lock.rejected_objective_count == 2
    assert len(lock.scope_constraints) == 12
    assert lock.lock_ok is True
    assert lock.valid is True
    assert validate_milestone_23_objective_scope_lock(lock) == ()


def test_scope_lock_public_payload() -> None:
    payload = build_milestone_23_objective_scope_lock().to_public_dict()

    assert payload["taskId"] == "MILESTONE_23_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert payload["milestoneId"] == "MILESTONE_23"
    assert payload["nextStage"] == "MILESTONE_23_TASK_3_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_IMPLEMENTATION_V1"
    assert payload["sourceOpeningValid"] is True
    assert payload["sourceMilestoneId"] == "MILESTONE_22"
    assert payload["sourceFinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert payload["sourceFinalTaskNumber"] == 6
    assert payload["sourceTask7Used"] is False
    assert payload["sourceTask8Used"] is False
    assert payload["scopeLockId"] == "MILESTONE_23_SCOPE_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY"
    assert payload["selectedObjectiveId"] == "CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY"
    assert payload["selectedObjective"]["selected"] is True
    assert payload["selectedObjective"]["localOnly"] is True
    assert payload["objectiveCandidateCount"] == 3
    assert payload["rejectedObjectiveCount"] == 2
    assert payload["scopeConstraintCount"] == 12
    assert payload["taskBudgetMin"] == 4
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 2
    assert payload["remainingBudgetAfterCurrentTask"] == 6
    assert payload["objectiveSelectionReady"] is True
    assert payload["objectiveSelected"] is True
    assert payload["scopeLocked"] is True
    assert payload["implementationAllowedNext"] is True
    assert payload["implementationStarted"] is False
    assert payload["registryImplementationStarted"] is False
    assert payload["fastSnapshotDependencyModeRequired"] is True
    assert payload["deepRecursiveDependencyTraversalForbidden"] is True
    assert payload["documentMarkerEvidenceRequired"] is True
    assert payload["staticClosureSnapshotRequired"] is True
    assert payload["closedMilestoneArtifactLookupRequired"] is True
    assert payload["sourceMilestone22ClosureRequired"] is True
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["kaggleAuthenticationAllowed"] is False
    assert payload["kaggleUploadAllowed"] is False
    assert payload["rawRequestBodyPersisted"] is False
    assert payload["secretPersisted"] is False
    assert payload["legalCertification"] is False
    assert payload["historicalMilestoneRewrite"] is False
    assert payload["failClosedActive"] is True
    assert payload["lockOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["lockId"].startswith("MILESTONE-23-SCOPE-LOCK-")


def test_rejected_objectives_are_out_of_scope() -> None:
    payload = build_milestone_23_objective_scope_lock().to_public_dict()
    rejected = [candidate for candidate in payload["objectiveCandidates"] if not candidate["selected"]]

    assert len(rejected) == 2
    assert rejected[0]["objectiveId"] == "RUNTIME_SOLVER_PATCH"
    assert rejected[0]["runtimeSolverModified"] is True
    assert rejected[1]["objectiveId"] == "KAGGLE_SUBMISSION_PREPARATION"
    assert rejected[1]["kaggleSubmissionAllowed"] is True
