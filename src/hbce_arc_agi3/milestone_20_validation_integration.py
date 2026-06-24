"""Milestone #20 validation and integration.

This module validates the governed Milestone 20 chain after the budget guard.
It does not implement new runtime behavior. It does not reopen Milestone 19.
It just checks that humans and scripts stop breeding tasks like wet gremlins.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_20_governed_execution import (
    MILESTONE_20_TASK_BUDGET_MAX,
    build_milestone_20_governed_execution,
    validate_milestone_20_governed_execution,
)
from hbce_arc_agi3.milestone_task_budget_governance import (
    build_milestone_19_final_closure,
    validate_milestone_19_final_closure,
)


TASK_ID = "MILESTONE_20_TASK_6_VALIDATION_AND_INTEGRATION_V1"
REVISION = "MILESTONE_20_VALIDATION_AND_INTEGRATION_v1"
MILESTONE_ID = "MILESTONE_20"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 6
NEXT_CLOSURE_TASK_NUMBER = 7
EMERGENCY_RESERVE_TASK_NUMBER = 8

VALIDATION_AND_INTEGRATION_READY = True
MILESTONE_19_REMAINS_CLOSED = True
MILESTONE_20_GOVERNANCE_VALIDATED = True
MILESTONE_20_READY_FOR_CLOSURE = True
NO_RECURSIVE_META_LAYER = True
CLOSURE_REQUIRED_NEXT = True

MAX_REVIEW_DEPTH = 1
MAX_AUTHORIZATION_DEPTH = 1
MAX_FINALIZATION_DEPTH = 1

RUNTIME_SOLVER_MODIFIED = False
RUNTIME_WIRING_ALLOWED = False
KAGGLE_SUBMISSION_SENT = False
RAW_REQUEST_BODY_PERSISTED = False
SECRET_PERSISTED = False
LEGAL_CERTIFICATION = False
FAIL_CLOSED_ACTIVE = True


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


@dataclass(frozen=True)
class Milestone20ValidationIntegration:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    current_task_number: int = CURRENT_TASK_NUMBER
    task_budget_max: int = TASK_BUDGET_MAX
    next_closure_task_number: int = NEXT_CLOSURE_TASK_NUMBER
    emergency_reserve_task_number: int = EMERGENCY_RESERVE_TASK_NUMBER
    integrated_task_labels: tuple[str, ...] = (
        "MILESTONE_20_TASK_1_OPERATOR_DECISION_GATE",
        "MILESTONE_20_TASK_2_OPERATOR_DECISION_RECORD",
        "MILESTONE_20_TASK_3_OPERATOR_DECISION_RECORD_REVIEW",
        "MILESTONE_20_TASK_4_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE",
        "MILESTONE_20_TASK_5_GOVERNED_EXECUTION_BUDGET_ALIGNMENT",
        "MILESTONE_20_TASK_6_VALIDATION_AND_INTEGRATION",
    )
    required_closure_task_label: str = "MILESTONE_20_TASK_7_MILESTONE_CLOSURE"
    emergency_only_task_label: str = "MILESTONE_20_TASK_8_EMERGENCY_RESERVE_ONLY"
    stop_condition: str = "Milestone 20 closure committed and pushed after validation and integration evidence passes full suite."
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def validation_id(self) -> str:
        return f"MILESTONE-20-VALIDATION-INTEGRATION-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def remaining_budget_after_current_task(self) -> int:
        return self.task_budget_max - self.current_task_number

    @property
    def validation_ok(self) -> bool:
        milestone_19 = build_milestone_19_final_closure()
        milestone_20 = build_milestone_20_governed_execution()

        return (
            VALIDATION_AND_INTEGRATION_READY is True
            and milestone_19.closure_ok is True
            and validate_milestone_19_final_closure(milestone_19) == ()
            and milestone_20.valid is True
            and validate_milestone_20_governed_execution(milestone_20) == ()
            and self.task_budget_max == MILESTONE_20_TASK_BUDGET_MAX == 8
            and self.current_task_number == 6
            and self.next_closure_task_number == 7
            and self.emergency_reserve_task_number == 8
            and len(self.integrated_task_labels) == 6
            and MILESTONE_19_REMAINS_CLOSED is True
            and MILESTONE_20_GOVERNANCE_VALIDATED is True
            and MILESTONE_20_READY_FOR_CLOSURE is True
            and NO_RECURSIVE_META_LAYER is True
            and CLOSURE_REQUIRED_NEXT is True
            and MAX_REVIEW_DEPTH == 1
            and MAX_AUTHORIZATION_DEPTH == 1
            and MAX_FINALIZATION_DEPTH == 1
            and RUNTIME_SOLVER_MODIFIED is False
            and RUNTIME_WIRING_ALLOWED is False
            and KAGGLE_SUBMISSION_SENT is False
            and RAW_REQUEST_BODY_PERSISTED is False
            and SECRET_PERSISTED is False
            and LEGAL_CERTIFICATION is False
            and FAIL_CLOSED_ACTIVE is True
        )

    @property
    def issues(self) -> tuple[str, ...]:
        issues: list[str] = []

        milestone_19 = build_milestone_19_final_closure()
        milestone_20 = build_milestone_20_governed_execution()

        if not milestone_19.closure_ok:
            issues.append("MILESTONE_19_NOT_CLOSED")
        issues.extend(f"MILESTONE_19_{issue}" for issue in validate_milestone_19_final_closure(milestone_19))

        if not milestone_20.valid:
            issues.append("MILESTONE_20_GOVERNED_EXECUTION_INVALID")
        issues.extend(f"MILESTONE_20_GOVERNANCE_{issue}" for issue in validate_milestone_20_governed_execution(milestone_20))

        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 6:
            issues.append("CURRENT_TASK_NUMBER_NOT_6")
        if self.next_closure_task_number != 7:
            issues.append("NEXT_CLOSURE_TASK_NUMBER_NOT_7")
        if self.emergency_reserve_task_number != 8:
            issues.append("EMERGENCY_RESERVE_TASK_NUMBER_NOT_8")
        if len(self.integrated_task_labels) != 6:
            issues.append("INTEGRATED_TASK_COUNT_NOT_6")
        if not MILESTONE_19_REMAINS_CLOSED:
            issues.append("MILESTONE_19_REOPENED")
        if not MILESTONE_20_READY_FOR_CLOSURE:
            issues.append("MILESTONE_20_NOT_READY_FOR_CLOSURE")
        if not NO_RECURSIVE_META_LAYER:
            issues.append("RECURSIVE_META_LAYER_ALLOWED")
        if not CLOSURE_REQUIRED_NEXT:
            issues.append("CLOSURE_NOT_REQUIRED_NEXT")
        if MAX_REVIEW_DEPTH != 1:
            issues.append("MAX_REVIEW_DEPTH_NOT_1")
        if MAX_AUTHORIZATION_DEPTH != 1:
            issues.append("MAX_AUTHORIZATION_DEPTH_NOT_1")
        if MAX_FINALIZATION_DEPTH != 1:
            issues.append("MAX_FINALIZATION_DEPTH_NOT_1")
        if RUNTIME_SOLVER_MODIFIED:
            issues.append("RUNTIME_SOLVER_MODIFIED")
        if RUNTIME_WIRING_ALLOWED:
            issues.append("RUNTIME_WIRING_ALLOWED")
        if KAGGLE_SUBMISSION_SENT:
            issues.append("KAGGLE_SUBMISSION_SENT")
        if RAW_REQUEST_BODY_PERSISTED:
            issues.append("RAW_REQUEST_BODY_PERSISTED")
        if SECRET_PERSISTED:
            issues.append("SECRET_PERSISTED")
        if LEGAL_CERTIFICATION:
            issues.append("LEGAL_CERTIFICATION")
        if not FAIL_CLOSED_ACTIVE:
            issues.append("FAIL_CLOSED_INACTIVE")

        return tuple(issues)

    @property
    def valid(self) -> bool:
        return self.validation_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "currentTaskNumber": self.current_task_number,
            "taskBudgetMax": self.task_budget_max,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "nextClosureTaskNumber": self.next_closure_task_number,
            "emergencyReserveTaskNumber": self.emergency_reserve_task_number,
            "integratedTaskLabels": list(self.integrated_task_labels),
            "integratedTaskCount": len(self.integrated_task_labels),
            "requiredClosureTaskLabel": self.required_closure_task_label,
            "emergencyOnlyTaskLabel": self.emergency_only_task_label,
            "stopCondition": self.stop_condition,
            "validationAndIntegrationReady": VALIDATION_AND_INTEGRATION_READY,
            "milestone19RemainsClosed": MILESTONE_19_REMAINS_CLOSED,
            "milestone20GovernanceValidated": MILESTONE_20_GOVERNANCE_VALIDATED,
            "milestone20ReadyForClosure": MILESTONE_20_READY_FOR_CLOSURE,
            "noRecursiveMetaLayer": NO_RECURSIVE_META_LAYER,
            "closureRequiredNext": CLOSURE_REQUIRED_NEXT,
            "maxReviewDepth": MAX_REVIEW_DEPTH,
            "maxAuthorizationDepth": MAX_AUTHORIZATION_DEPTH,
            "maxFinalizationDepth": MAX_FINALIZATION_DEPTH,
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
            "rawRequestBodyPersisted": RAW_REQUEST_BODY_PERSISTED,
            "secretPersisted": SECRET_PERSISTED,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
            "validationOk": self.validation_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["validationId"] = self.validation_id
        return payload


def build_milestone_20_validation_integration(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone20ValidationIntegration:
    return Milestone20ValidationIntegration(metadata={} if metadata is None else metadata)


def validate_milestone_20_validation_integration(validation: Milestone20ValidationIntegration) -> tuple[str, ...]:
    return validation.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "VALIDATION_AND_INTEGRATION_READY",
    "MILESTONE_20_READY_FOR_CLOSURE",
    "Milestone20ValidationIntegration",
    "build_milestone_20_validation_integration",
    "validate_milestone_20_validation_integration",
]
