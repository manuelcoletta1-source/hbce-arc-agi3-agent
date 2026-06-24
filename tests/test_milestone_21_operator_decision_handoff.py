"""Tests for Milestone #21 scoped operator decision handoff implementation."""

from __future__ import annotations

from hbce_arc_agi3.milestone_21_operator_decision_handoff import (
    HANDOFF_KIND,
    HANDOFF_SCOPE_ID,
    NEXT_STAGE,
    REVISION,
    TASK_ID,
    build_operator_decision_handoff_package,
    validate_operator_decision_handoff_package,
)


def test_operator_decision_handoff_contract() -> None:
    package = build_operator_decision_handoff_package(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_21_TASK_3_SCOPED_OPERATOR_DECISION_HANDOFF_IMPLEMENTATION_V1"
    assert REVISION == "MILESTONE_21_SCOPED_OPERATOR_DECISION_HANDOFF_IMPLEMENTATION_v1"
    assert HANDOFF_KIND == "LOCAL_ONLY_OPERATOR_DECISION_HANDOFF_PACKAGE"
    assert HANDOFF_SCOPE_ID == "MILESTONE_21_SCOPE_OPERATOR_DECISION_HANDOFF_LOCAL_ONLY"
    assert NEXT_STAGE == "MILESTONE_21_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert package.task_budget_max == 8
    assert package.current_task_number == 3
    assert package.recommended_closure_task_number == 6
    assert package.reserve_task_number == 7
    assert package.emergency_only_task_number == 8
    assert len(package.carried_state_keys) == 9
    assert len(package.implementation_contract_items) == 6
    assert len(package.forbidden_actions) == 10
    assert package.handoff_ok is True
    assert package.valid is True
    assert validate_operator_decision_handoff_package(package) == ()


def test_operator_decision_handoff_public_payload() -> None:
    payload = build_operator_decision_handoff_package().to_public_dict()

    assert payload["taskId"] == "MILESTONE_21_TASK_3_SCOPED_OPERATOR_DECISION_HANDOFF_IMPLEMENTATION_V1"
    assert payload["milestoneId"] == "MILESTONE_21"
    assert payload["handoffKind"] == "LOCAL_ONLY_OPERATOR_DECISION_HANDOFF_PACKAGE"
    assert payload["handoffScopeId"] == "MILESTONE_21_SCOPE_OPERATOR_DECISION_HANDOFF_LOCAL_ONLY"
    assert payload["sourceMilestoneId"] == "MILESTONE_20"
    assert payload["sourceTaskId"] == "MILESTONE_20_TASK_7_MILESTONE_CLOSURE_V1"
    assert payload["sourceMilestone20FinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8"
    assert payload["sourceMilestone20Task8Used"] is False
    assert payload["sourceMilestone20EmergencyReserveUnused"] is True
    assert payload["scopeLocked"] is True
    assert payload["implementationAllowedByScope"] is True
    assert payload["implementationStartedBeforeTask3"] is False
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 3
    assert payload["remainingBudgetAfterCurrentTask"] == 5
    assert payload["recommendedClosureTaskNumber"] == 6
    assert payload["carriedStateKeyCount"] == 9
    assert payload["implementationContractItemCount"] == 6
    assert payload["forbiddenActionCount"] == 10
    assert payload["handoffPackageCreated"] is True
    assert payload["handoffLocalOnly"] is True
    assert payload["handoffBoundedDiagnosticOnly"] is True
    assert payload["handoffReadyForValidationArtifacts"] is True
    assert payload["noRecursiveMetaLayer"] is True
    assert payload["milestone20Task8Required"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["rawRequestBodyPersisted"] is False
    assert payload["secretPersisted"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True
    assert payload["handoffOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["handoffId"].startswith("MILESTONE-21-OPERATOR-DECISION-HANDOFF-")


def test_operator_decision_handoff_forbidden_actions_are_explicit() -> None:
    package = build_operator_decision_handoff_package()

    assert "runtime_solver_modification" in package.forbidden_actions
    assert "runtime_wiring_activation" in package.forbidden_actions
    assert "kaggle_submission" in package.forbidden_actions
    assert "raw_request_body_persistence" in package.forbidden_actions
    assert "secret_persistence" in package.forbidden_actions
    assert "milestone_20_task_8_use" in package.forbidden_actions
    assert "recursive_meta_layer" in package.forbidden_actions
