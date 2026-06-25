"""Tests for Milestone #24 governed opening."""

from __future__ import annotations

from hbce_arc_agi3.milestone_24_governed_opening import (
    GOVERNED_OPENING_READY,
    NEXT_STAGE,
    REVISION,
    TASK_BUDGET_LOCKED,
    TASK_ID,
    build_milestone_24_governed_opening,
    validate_milestone_24_governed_opening,
)


def test_milestone_24_governed_opening_contract() -> None:
    opening = build_milestone_24_governed_opening(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_24_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
    assert REVISION == "MILESTONE_24_GOVERNED_OPENING_WITH_TASK_BUDGET_v1"
    assert NEXT_STAGE == "MILESTONE_24_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert GOVERNED_OPENING_READY is True
    assert TASK_BUDGET_LOCKED is True
    assert opening.task_budget_min == 4
    assert opening.task_budget_max == 8
    assert opening.current_task_number == 1
    assert opening.recommended_closure_task_number == 6
    assert opening.reserve_task_number == 7
    assert opening.emergency_only_task_number == 8
    assert len(opening.opening_checks) == 12
    assert opening.opening_ok is True
    assert opening.valid is True
    assert validate_milestone_24_governed_opening(opening) == ()


def test_milestone_24_governed_opening_public_payload() -> None:
    payload = build_milestone_24_governed_opening().to_public_dict()

    assert payload["taskId"] == "MILESTONE_24_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
    assert payload["milestoneId"] == "MILESTONE_24"
    assert payload["sourceMilestoneId"] == "MILESTONE_23"
    assert payload["sourceClosureValid"] is True
    assert payload["sourceClosureOk"] is True
    assert payload["sourceMilestoneClosed"] is True
    assert payload["sourceFinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert payload["sourceTechnicalStatus"] == "PASS"
    assert payload["sourceProcessStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
    assert payload["sourceFinalTaskNumber"] == 6
    assert payload["sourceTaskBudgetMax"] == 8
    assert payload["sourceTask7Used"] is False
    assert payload["sourceTask8Used"] is False
    assert payload["sourceReserveUnused"] is True
    assert payload["sourceEmergencyReserveUnused"] is True
    assert payload["nextStage"] == "MILESTONE_24_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
    assert payload["taskBudgetMin"] == 4
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 1
    assert payload["remainingBudgetAfterCurrentTask"] == 7
    assert payload["openingCheckCount"] == 12
    assert payload["governedOpeningReady"] is True
    assert payload["taskBudgetLocked"] is True
    assert payload["objectiveSelectionRequiredNext"] is True
    assert payload["scopeLockRequiredNext"] is True
    assert payload["implementationStarted"] is False
    assert payload["implementationAllowedAtTask1"] is False
    assert payload["fastSnapshotDependencyMode"] is True
    assert payload["deepRecursiveDependencyTraversalAllowed"] is False
    assert payload["sourceClosureSnapshotRequired"] is True
    assert payload["documentMarkerEvidenceRequired"] is True
    assert payload["noRecursiveMetaLayer"] is True
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
    assert payload["openingId"].startswith("MILESTONE-24-GOVERNED-OPENING-")


def test_opening_checks_are_explicit() -> None:
    opening = build_milestone_24_governed_opening()

    assert "source_milestone_23_closure_valid" in opening.opening_checks
    assert "source_final_status_preserved" in opening.opening_checks
    assert "source_final_task_number_6" in opening.opening_checks
    assert "source_task_7_unused" in opening.opening_checks
    assert "source_task_8_unused" in opening.opening_checks
    assert "task_budget_max_8" in opening.opening_checks
    assert "implementation_not_started" in opening.opening_checks
    assert "objective_scope_lock_required_next" in opening.opening_checks
