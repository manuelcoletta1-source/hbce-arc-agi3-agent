"""Tests for Milestone #25 objective selection and scope lock."""

from __future__ import annotations

from hbce_arc_agi3.milestone_25_objective_scope_lock import (
    FAST_SOURCE_OPENING_SNAPSHOT,
    NEXT_STAGE,
    OBJECTIVE_SELECTED,
    SCOPE_LOCKED,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    TASK_ID,
    build_fast_source_opening_snapshot,
    build_milestone_25_objective_scope_lock,
    validate_milestone_25_objective_scope_lock,
)


def test_fast_source_opening_snapshot_contract() -> None:
    source = build_fast_source_opening_snapshot()

    assert source["taskId"] == "MILESTONE_25_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
    assert source["milestoneId"] == "MILESTONE_25"
    assert source["sourceMilestoneId"] == "MILESTONE_24"
    assert source["sourceFinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert source["sourceTask7Used"] is False
    assert source["sourceTask8Used"] is False
    assert source["sourceMilestoneClosed"] is True
    assert source["objectiveSelectionRequiredNext"] is True
    assert source["scopeLockRequiredNext"] is True
    assert source["implementationStarted"] is False
    assert source["fastSourceClosureSnapshot"] is True
    assert source["valid"] is True


def test_objective_scope_lock_contract() -> None:
    lock = build_milestone_25_objective_scope_lock()

    assert TASK_ID == "MILESTONE_25_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert SELECTED_OBJECTIVE_ID == "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"
    assert SCOPE_LOCK_ID == "MILESTONE_25_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"
    assert NEXT_STAGE == "MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_IMPLEMENTATION_V1"
    assert OBJECTIVE_SELECTED is True
    assert SCOPE_LOCKED is True
    assert FAST_SOURCE_OPENING_SNAPSHOT is True
    assert lock.task_budget_max == 8
    assert lock.current_task_number == 2
    assert lock.remaining_budget_after_current_task == 6
    assert len(lock.allowed_operations) == 4
    assert len(lock.forbidden_operations) == 9
    assert lock.lock_ok is True
    assert lock.valid is True
    assert validate_milestone_25_objective_scope_lock(lock) == ()


def test_objective_scope_lock_public_payload() -> None:
    payload = build_milestone_25_objective_scope_lock().to_public_dict()

    assert payload["taskId"] == "MILESTONE_25_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert payload["milestoneId"] == "MILESTONE_25"
    assert payload["sourceTaskId"] == "MILESTONE_25_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
    assert payload["sourceOpeningValid"] is True
    assert payload["selectedObjectiveId"] == "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"
    assert payload["scopeLockId"] == "MILESTONE_25_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"
    assert payload["nextStage"] == "MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_IMPLEMENTATION_V1"
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 2
    assert payload["objectiveSelected"] is True
    assert payload["scopeLocked"] is True
    assert payload["implementationAllowedNext"] is True
    assert payload["implementationStarted"] is False
    assert payload["evidenceBundleImplementationStarted"] is False
    assert payload["allowedOperationCount"] == 4
    assert payload["forbiddenOperationCount"] == 9
    assert payload["fastSourceOpeningSnapshot"] is True
    assert payload["deepRecursiveDependencyTraversalAllowed"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["lockOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["lockArtifactId"].startswith("MILESTONE-25-SCOPE-LOCK-")
