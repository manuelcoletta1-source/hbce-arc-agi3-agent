"""Tests for Milestone #20 validation and integration."""

from __future__ import annotations

from hbce_arc_agi3.milestone_20_validation_integration import (
    MILESTONE_20_READY_FOR_CLOSURE,
    REVISION,
    TASK_ID,
    VALIDATION_AND_INTEGRATION_READY,
    build_milestone_20_validation_integration,
    validate_milestone_20_validation_integration,
)


def test_validation_integration_contract() -> None:
    validation = build_milestone_20_validation_integration(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_20_TASK_6_VALIDATION_AND_INTEGRATION_V1"
    assert REVISION == "MILESTONE_20_VALIDATION_AND_INTEGRATION_v1"
    assert VALIDATION_AND_INTEGRATION_READY is True
    assert MILESTONE_20_READY_FOR_CLOSURE is True
    assert validation.task_budget_max == 8
    assert validation.current_task_number == 6
    assert validation.next_closure_task_number == 7
    assert validation.emergency_reserve_task_number == 8
    assert validation.remaining_budget_after_current_task == 2
    assert len(validation.integrated_task_labels) == 6
    assert validation.validation_ok is True
    assert validation.valid is True
    assert validate_milestone_20_validation_integration(validation) == ()


def test_validation_public_payload() -> None:
    payload = build_milestone_20_validation_integration().to_public_dict()

    assert payload["taskId"] == "MILESTONE_20_TASK_6_VALIDATION_AND_INTEGRATION_V1"
    assert payload["milestoneId"] == "MILESTONE_20"
    assert payload["currentTaskNumber"] == 6
    assert payload["taskBudgetMax"] == 8
    assert payload["remainingBudgetAfterCurrentTask"] == 2
    assert payload["nextClosureTaskNumber"] == 7
    assert payload["emergencyReserveTaskNumber"] == 8
    assert payload["integratedTaskCount"] == 6
    assert payload["milestone19RemainsClosed"] is True
    assert payload["milestone20GovernanceValidated"] is True
    assert payload["milestone20ReadyForClosure"] is True
    assert payload["noRecursiveMetaLayer"] is True
    assert payload["closureRequiredNext"] is True
    assert payload["maxReviewDepth"] == 1
    assert payload["maxAuthorizationDepth"] == 1
    assert payload["maxFinalizationDepth"] == 1
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["rawRequestBodyPersisted"] is False
    assert payload["secretPersisted"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True
    assert payload["validationOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["validationId"].startswith("MILESTONE-20-VALIDATION-INTEGRATION-")


def test_validation_integrated_labels_are_bounded() -> None:
    validation = build_milestone_20_validation_integration()

    assert validation.integrated_task_labels[0] == "MILESTONE_20_TASK_1_OPERATOR_DECISION_GATE"
    assert validation.integrated_task_labels[-1] == "MILESTONE_20_TASK_6_VALIDATION_AND_INTEGRATION"
    assert validation.required_closure_task_label == "MILESTONE_20_TASK_7_MILESTONE_CLOSURE"
    assert validation.emergency_only_task_label == "MILESTONE_20_TASK_8_EMERGENCY_RESERVE_ONLY"
    assert len(validation.integrated_task_labels) + 1 + 1 == 8
