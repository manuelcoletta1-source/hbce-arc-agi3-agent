"""Tests for Milestone #23 governed opening."""

from __future__ import annotations

from hbce_arc_agi3.milestone_23_governed_opening import (
    GOVERNED_TASK_BUDGET_READY,
    NEXT_STAGE,
    OPENING_READY,
    REVISION,
    TASK_ID,
    Milestone22ClosureSnapshot,
    build_milestone_23_governed_opening,
    validate_milestone_23_governed_opening,
)


def test_milestone_22_static_closure_snapshot() -> None:
    snapshot = Milestone22ClosureSnapshot()

    assert snapshot.valid is True
    assert snapshot.milestone_id == "MILESTONE_22"
    assert snapshot.final_status == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert snapshot.final_task_number == 6
    assert snapshot.task_budget_max == 8
    assert snapshot.task_7_used is False
    assert snapshot.task_8_used is False
    assert snapshot.reserve_unused is True
    assert snapshot.emergency_reserve_unused is True
    assert snapshot.marker_count == 5
    assert snapshot.snapshot_id.startswith("MILESTONE-22-CLOSURE-SNAPSHOT-")


def test_governed_opening_contract() -> None:
    opening = build_milestone_23_governed_opening(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_23_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
    assert REVISION == "MILESTONE_23_GOVERNED_OPENING_WITH_TASK_BUDGET_v1"
    assert NEXT_STAGE == "MILESTONE_23_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert OPENING_READY is True
    assert GOVERNED_TASK_BUDGET_READY is True
    assert opening.task_budget_min == 4
    assert opening.task_budget_max == 8
    assert opening.current_task_number == 1
    assert opening.recommended_closure_task_number == 6
    assert opening.reserve_task_number == 7
    assert opening.emergency_only_task_number == 8
    assert len(opening.opening_checks) == 12
    assert opening.opening_ok is True
    assert opening.valid is True
    assert validate_milestone_23_governed_opening(opening) == ()


def test_governed_opening_public_payload() -> None:
    payload = build_milestone_23_governed_opening().to_public_dict()

    assert payload["taskId"] == "MILESTONE_23_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
    assert payload["milestoneId"] == "MILESTONE_23"
    assert payload["nextStage"] == "MILESTONE_23_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert payload["sourceMilestoneId"] == "MILESTONE_22"
    assert payload["sourceClosureSnapshotValid"] is True
    assert payload["sourceFinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert payload["sourceFinalTaskNumber"] == 6
    assert payload["sourceTaskBudgetMax"] == 8
    assert payload["sourceTask7Used"] is False
    assert payload["sourceTask8Used"] is False
    assert payload["sourceReserveUnused"] is True
    assert payload["sourceEmergencyReserveUnused"] is True
    assert payload["sourceEvidenceMarkerCount"] == 5
    assert payload["taskBudgetMin"] == 4
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 1
    assert payload["remainingBudgetAfterCurrentTask"] == 7
    assert payload["recommendedClosureTaskNumber"] == 6
    assert payload["openingCheckCount"] == 12
    assert payload["openingReady"] is True
    assert payload["governedTaskBudgetReady"] is True
    assert payload["objectiveSelectionRequiredNext"] is True
    assert payload["scopeLockRequiredNext"] is True
    assert payload["implementationStarted"] is False
    assert payload["implementationAllowedAtTask1"] is False
    assert payload["fastSnapshotDependencyMode"] is True
    assert payload["deepRecursiveDependencyTraversalAllowed"] is False
    assert payload["documentMarkerEvidenceRequired"] is True
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
    assert payload["openingOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["openingId"].startswith("MILESTONE-23-GOVERNED-OPENING-")
