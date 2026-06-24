"""Milestone #21 governed opening.

Milestone 21 opens only after Milestone 20 was closed under budget.
This module declares the task budget before implementation work starts.

It exists because apparently software projects need a seatbelt, a speed limiter,
and a small courtroom just to avoid growing tentacles.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_20_closure import (
    build_milestone_20_closure,
    validate_milestone_20_closure,
)
from hbce_arc_agi3.milestone_task_budget_governance import (
    STANDARD_MILESTONE_TASK_MAX,
    build_standard_milestone_policy,
)


TASK_ID = "MILESTONE_21_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
REVISION = "MILESTONE_21_GOVERNED_OPENING_WITH_TASK_BUDGET_v1"
MILESTONE_ID = "MILESTONE_21"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 1
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

MILESTONE_21_GOVERNED_OPENING_READY = True
MILESTONE_21_IMPLEMENTATION_STARTED = False
MILESTONE_21_SCOPE_LOCK_REQUIRED_NEXT = True
MILESTONE_21_CLOSURE_REQUIRED = True
MILESTONE_21_NO_RECURSIVE_META_LAYER = True

MAX_REVIEW_DEPTH = 1
MAX_AUTHORIZATION_DEPTH = 1
MAX_FINALIZATION_DEPTH = 1

MILESTONE_20_REOPEN_REQUIRED = False
MILESTONE_20_TASK_8_REQUIRED = False
MILESTONE_19_REOPEN_REQUIRED = False

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
class Milestone21GovernedOpening:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    objective: str = (
        "Open Milestone 21 under governed task-budget execution before any implementation work starts."
    )
    stop_condition: str = (
        "Milestone 21 closes when scoped work is implemented, validated, regression-tested, "
        "documented, committed and pushed within task budget."
    )
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    planned_task_labels: tuple[str, ...] = (
        "MILESTONE_21_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET",
        "MILESTONE_21_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK",
        "MILESTONE_21_TASK_3_IMPLEMENTATION",
        "MILESTONE_21_TASK_4_VALIDATION_AND_ARTIFACTS",
        "MILESTONE_21_TASK_5_INTEGRATION_REGRESSION",
        "MILESTONE_21_TASK_6_MILESTONE_CLOSURE",
    )
    reserve_task_label: str = "MILESTONE_21_TASK_7_RESERVE_ONLY"
    emergency_task_label: str = "MILESTONE_21_TASK_8_EMERGENCY_ONLY"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def opening_id(self) -> str:
        return f"MILESTONE-21-GOVERNED-OPENING-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def remaining_budget_after_current_task(self) -> int:
        return self.task_budget_max - self.current_task_number

    @property
    def opening_ok(self) -> bool:
        milestone_20 = build_milestone_20_closure()
        policy = build_standard_milestone_policy(
            milestone_id=self.milestone_id,
            objective=self.objective,
            stop_condition=self.stop_condition,
            task_budget_min=self.task_budget_min,
            task_budget_max=self.task_budget_max,
            metadata={"source": REVISION},
        )

        return (
            MILESTONE_21_GOVERNED_OPENING_READY is True
            and MILESTONE_21_IMPLEMENTATION_STARTED is False
            and MILESTONE_21_SCOPE_LOCK_REQUIRED_NEXT is True
            and MILESTONE_21_CLOSURE_REQUIRED is True
            and MILESTONE_21_NO_RECURSIVE_META_LAYER is True
            and policy.valid is True
            and self.task_budget_max == STANDARD_MILESTONE_TASK_MAX == 8
            and self.current_task_number == 1
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.planned_task_labels) == 6
            and MAX_REVIEW_DEPTH == 1
            and MAX_AUTHORIZATION_DEPTH == 1
            and MAX_FINALIZATION_DEPTH == 1
            and milestone_20.valid is True
            and validate_milestone_20_closure(milestone_20) == ()
            and MILESTONE_20_REOPEN_REQUIRED is False
            and MILESTONE_20_TASK_8_REQUIRED is False
            and MILESTONE_19_REOPEN_REQUIRED is False
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

        milestone_20 = build_milestone_20_closure()
        milestone_20_issues = validate_milestone_20_closure(milestone_20)
        if not milestone_20.valid:
            issues.append("MILESTONE_20_NOT_CLOSED")
        issues.extend(f"MILESTONE_20_{issue}" for issue in milestone_20_issues)

        policy = build_standard_milestone_policy(
            milestone_id=self.milestone_id,
            objective=self.objective,
            stop_condition=self.stop_condition,
            task_budget_min=self.task_budget_min,
            task_budget_max=self.task_budget_max,
            metadata={"source": REVISION},
        )
        if not policy.valid:
            issues.extend(f"POLICY_{issue}" for issue in policy.issues)

        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 1:
            issues.append("CURRENT_TASK_NUMBER_NOT_1")
        if self.recommended_closure_task_number != 6:
            issues.append("RECOMMENDED_CLOSURE_TASK_NOT_6")
        if self.reserve_task_number != 7:
            issues.append("RESERVE_TASK_NUMBER_NOT_7")
        if self.emergency_only_task_number != 8:
            issues.append("EMERGENCY_TASK_NUMBER_NOT_8")
        if len(self.planned_task_labels) != 6:
            issues.append("PLANNED_TASK_COUNT_NOT_6")
        if MILESTONE_21_IMPLEMENTATION_STARTED:
            issues.append("IMPLEMENTATION_STARTED_TOO_EARLY")
        if not MILESTONE_21_SCOPE_LOCK_REQUIRED_NEXT:
            issues.append("SCOPE_LOCK_NOT_REQUIRED_NEXT")
        if not MILESTONE_21_CLOSURE_REQUIRED:
            issues.append("CLOSURE_NOT_REQUIRED")
        if not MILESTONE_21_NO_RECURSIVE_META_LAYER:
            issues.append("RECURSIVE_META_LAYER_ALLOWED")
        if MAX_REVIEW_DEPTH != 1:
            issues.append("MAX_REVIEW_DEPTH_NOT_1")
        if MAX_AUTHORIZATION_DEPTH != 1:
            issues.append("MAX_AUTHORIZATION_DEPTH_NOT_1")
        if MAX_FINALIZATION_DEPTH != 1:
            issues.append("MAX_FINALIZATION_DEPTH_NOT_1")
        if MILESTONE_20_REOPEN_REQUIRED:
            issues.append("MILESTONE_20_REOPEN_REQUIRED")
        if MILESTONE_20_TASK_8_REQUIRED:
            issues.append("MILESTONE_20_TASK_8_REQUIRED")
        if MILESTONE_19_REOPEN_REQUIRED:
            issues.append("MILESTONE_19_REOPEN_REQUIRED")
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
        return self.opening_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "objective": self.objective,
            "stopCondition": self.stop_condition,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "plannedTaskLabels": list(self.planned_task_labels),
            "plannedTaskCount": len(self.planned_task_labels),
            "reserveTaskLabel": self.reserve_task_label,
            "emergencyTaskLabel": self.emergency_task_label,
            "governedOpeningReady": MILESTONE_21_GOVERNED_OPENING_READY,
            "implementationStarted": MILESTONE_21_IMPLEMENTATION_STARTED,
            "scopeLockRequiredNext": MILESTONE_21_SCOPE_LOCK_REQUIRED_NEXT,
            "closureRequired": MILESTONE_21_CLOSURE_REQUIRED,
            "noRecursiveMetaLayer": MILESTONE_21_NO_RECURSIVE_META_LAYER,
            "maxReviewDepth": MAX_REVIEW_DEPTH,
            "maxAuthorizationDepth": MAX_AUTHORIZATION_DEPTH,
            "maxFinalizationDepth": MAX_FINALIZATION_DEPTH,
            "milestone20ReopenRequired": MILESTONE_20_REOPEN_REQUIRED,
            "milestone20Task8Required": MILESTONE_20_TASK_8_REQUIRED,
            "milestone19ReopenRequired": MILESTONE_19_REOPEN_REQUIRED,
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
            "rawRequestBodyPersisted": RAW_REQUEST_BODY_PERSISTED,
            "secretPersisted": SECRET_PERSISTED,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
            "openingOk": self.opening_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["openingId"] = self.opening_id
        return payload


def build_milestone_21_governed_opening(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone21GovernedOpening:
    return Milestone21GovernedOpening(metadata={} if metadata is None else metadata)


def validate_milestone_21_governed_opening(opening: Milestone21GovernedOpening) -> tuple[str, ...]:
    return opening.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "MILESTONE_21_GOVERNED_OPENING_READY",
    "Milestone21GovernedOpening",
    "build_milestone_21_governed_opening",
    "validate_milestone_21_governed_opening",
]
