"""Milestone #22 Task 1 - Governed Opening With Task Budget.

Fast snapshot implementation.

Milestone 22 opens only after Milestone 21 has closed cleanly at Task 6.
This module declares budget, stop condition, reserve limits and anti-recursive
governance before implementation begins.

Important: it intentionally uses closure snapshots instead of recursively
serializing the full Milestone 19 -> 20 -> 21 chain inside to_public_dict().
That old pattern worked until it became a Python family reunion with no exit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


TASK_ID = "MILESTONE_22_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
REVISION = "MILESTONE_22_GOVERNED_OPENING_WITH_TASK_BUDGET_FAST_SNAPSHOT_v1"
MILESTONE_ID = "MILESTONE_22"
NEXT_STAGE = "MILESTONE_22_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"

OBJECTIVE = (
    "Open Milestone 22 under governed task-budget execution after Milestone 21 closure, "
    "requiring objective selection and scope lock before implementation."
)

STOP_CONDITION = (
    "Milestone 22 closes when the selected scoped objective is implemented, validated, "
    "integration-regression-tested, documented, committed and pushed within task budget."
)

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 1
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

MILESTONE_22_GOVERNED_OPENING_READY = True
MILESTONE_22_IMPLEMENTATION_STARTED = False
MILESTONE_22_OBJECTIVE_SELECTION_REQUIRED_NEXT = True
MILESTONE_22_SCOPE_LOCK_REQUIRED_NEXT = True
MILESTONE_22_CLOSURE_REQUIRED = True
MILESTONE_22_NO_RECURSIVE_META_LAYER = True

MILESTONE_21_FINAL_STATUS_SNAPSHOT = "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
MILESTONE_21_TECHNICAL_STATUS_SNAPSHOT = "PASS"
MILESTONE_21_PROCESS_STATUS_SNAPSHOT = "GOVERNED_WITHIN_TASK_BUDGET"
MILESTONE_21_TASK_7_USED_SNAPSHOT = False
MILESTONE_21_TASK_8_USED_SNAPSHOT = False
MILESTONE_21_RESERVE_UNUSED_SNAPSHOT = True
MILESTONE_21_EMERGENCY_RESERVE_UNUSED_SNAPSHOT = True

MILESTONE_20_FINAL_STATUS_SNAPSHOT = "CLOSED_WITH_TASK_BUDGET_MAX_8"
MILESTONE_20_TASK_8_USED_SNAPSHOT = False
MILESTONE_20_EMERGENCY_RESERVE_UNUSED_SNAPSHOT = True

MILESTONE_19_BUDGET_GUARD_ACTIVE_SNAPSHOT = True
STANDARD_MILESTONE_TASK_MAX_SNAPSHOT = 8

MILESTONE_21_REOPEN_REQUIRED = False
MILESTONE_21_TASK_7_REQUIRED = False
MILESTONE_21_TASK_8_REQUIRED = False
MILESTONE_20_REOPEN_REQUIRED = False
MILESTONE_20_TASK_8_REQUIRED = False
MILESTONE_19_REOPEN_REQUIRED = False

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
class Milestone22GovernedOpening:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    objective: str = OBJECTIVE
    stop_condition: str = STOP_CONDITION
    next_stage: str = NEXT_STAGE
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    planned_task_labels: tuple[str, ...] = (
        "MILESTONE_22_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET",
        "MILESTONE_22_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK",
        "MILESTONE_22_TASK_3_SCOPED_IMPLEMENTATION",
        "MILESTONE_22_TASK_4_VALIDATION_AND_ARTIFACTS",
        "MILESTONE_22_TASK_5_INTEGRATION_REGRESSION",
        "MILESTONE_22_TASK_6_MILESTONE_CLOSURE",
    )
    reserve_task_label: str = "MILESTONE_22_TASK_7_RESERVE_ONLY"
    emergency_task_label: str = "MILESTONE_22_TASK_8_EMERGENCY_ONLY"
    opening_checks: tuple[str, ...] = (
        "milestone_21_closed",
        "milestone_21_task_7_unused",
        "milestone_21_task_8_unused",
        "milestone_20_remains_closed",
        "milestone_19_budget_guard_active",
        "task_budget_declared",
        "stop_condition_declared",
        "scope_lock_required_next",
        "forbidden_actions_absent",
        "fail_closed_boundary_preserved",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def opening_id(self) -> str:
        return f"MILESTONE-22-GOVERNED-OPENING-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def remaining_budget_after_current_task(self) -> int:
        return self.task_budget_max - self.current_task_number

    @property
    def opening_ok(self) -> bool:
        return (
            MILESTONE_22_GOVERNED_OPENING_READY is True
            and MILESTONE_22_IMPLEMENTATION_STARTED is False
            and MILESTONE_22_OBJECTIVE_SELECTION_REQUIRED_NEXT is True
            and MILESTONE_22_SCOPE_LOCK_REQUIRED_NEXT is True
            and MILESTONE_22_CLOSURE_REQUIRED is True
            and MILESTONE_22_NO_RECURSIVE_META_LAYER is True
            and self.task_budget_min == 4
            and self.task_budget_max == STANDARD_MILESTONE_TASK_MAX_SNAPSHOT == 8
            and self.current_task_number == 1
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.planned_task_labels) == 6
            and len(self.opening_checks) == 10
            and MILESTONE_21_FINAL_STATUS_SNAPSHOT == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
            and MILESTONE_21_TECHNICAL_STATUS_SNAPSHOT == "PASS"
            and MILESTONE_21_PROCESS_STATUS_SNAPSHOT == "GOVERNED_WITHIN_TASK_BUDGET"
            and MILESTONE_21_TASK_7_USED_SNAPSHOT is False
            and MILESTONE_21_TASK_8_USED_SNAPSHOT is False
            and MILESTONE_21_RESERVE_UNUSED_SNAPSHOT is True
            and MILESTONE_21_EMERGENCY_RESERVE_UNUSED_SNAPSHOT is True
            and MILESTONE_20_FINAL_STATUS_SNAPSHOT == "CLOSED_WITH_TASK_BUDGET_MAX_8"
            and MILESTONE_20_TASK_8_USED_SNAPSHOT is False
            and MILESTONE_20_EMERGENCY_RESERVE_UNUSED_SNAPSHOT is True
            and MILESTONE_19_BUDGET_GUARD_ACTIVE_SNAPSHOT is True
            and MILESTONE_21_REOPEN_REQUIRED is False
            and MILESTONE_21_TASK_7_REQUIRED is False
            and MILESTONE_21_TASK_8_REQUIRED is False
            and MILESTONE_20_REOPEN_REQUIRED is False
            and MILESTONE_20_TASK_8_REQUIRED is False
            and MILESTONE_19_REOPEN_REQUIRED is False
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

        if not MILESTONE_22_GOVERNED_OPENING_READY:
            issues.append("GOVERNED_OPENING_NOT_READY")
        if MILESTONE_22_IMPLEMENTATION_STARTED:
            issues.append("IMPLEMENTATION_STARTED_TOO_EARLY")
        if not MILESTONE_22_OBJECTIVE_SELECTION_REQUIRED_NEXT:
            issues.append("OBJECTIVE_SELECTION_NOT_REQUIRED_NEXT")
        if not MILESTONE_22_SCOPE_LOCK_REQUIRED_NEXT:
            issues.append("SCOPE_LOCK_NOT_REQUIRED_NEXT")
        if not MILESTONE_22_CLOSURE_REQUIRED:
            issues.append("CLOSURE_NOT_REQUIRED")
        if not MILESTONE_22_NO_RECURSIVE_META_LAYER:
            issues.append("RECURSIVE_META_LAYER_ALLOWED")
        if self.task_budget_min != 4:
            issues.append("TASK_BUDGET_MIN_NOT_4")
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
        if len(self.opening_checks) != 10:
            issues.append("OPENING_CHECK_COUNT_NOT_10")
        if MILESTONE_21_FINAL_STATUS_SNAPSHOT != "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6":
            issues.append("MILESTONE_21_NOT_CLOSED")
        if MILESTONE_21_TASK_7_USED_SNAPSHOT:
            issues.append("MILESTONE_21_TASK_7_USED")
        if MILESTONE_21_TASK_8_USED_SNAPSHOT:
            issues.append("MILESTONE_21_TASK_8_USED")
        if MILESTONE_20_TASK_8_USED_SNAPSHOT:
            issues.append("MILESTONE_20_TASK_8_USED")
        if not MILESTONE_19_BUDGET_GUARD_ACTIVE_SNAPSHOT:
            issues.append("MILESTONE_19_BUDGET_GUARD_INACTIVE")
        if MILESTONE_21_REOPEN_REQUIRED:
            issues.append("MILESTONE_21_REOPEN_REQUIRED")
        if MILESTONE_21_TASK_7_REQUIRED:
            issues.append("MILESTONE_21_TASK_7_REQUIRED")
        if MILESTONE_21_TASK_8_REQUIRED:
            issues.append("MILESTONE_21_TASK_8_REQUIRED")
        if MILESTONE_20_REOPEN_REQUIRED:
            issues.append("MILESTONE_20_REOPEN_REQUIRED")
        if MILESTONE_20_TASK_8_REQUIRED:
            issues.append("MILESTONE_20_TASK_8_REQUIRED")
        if MILESTONE_19_REOPEN_REQUIRED:
            issues.append("MILESTONE_19_REOPEN_REQUIRED")
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
        return self.opening_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "objective": self.objective,
            "stopCondition": self.stop_condition,
            "nextStage": self.next_stage,
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
            "openingChecks": list(self.opening_checks),
            "openingCheckCount": len(self.opening_checks),
            "milestone21FinalStatus": MILESTONE_21_FINAL_STATUS_SNAPSHOT,
            "milestone21TechnicalStatus": MILESTONE_21_TECHNICAL_STATUS_SNAPSHOT,
            "milestone21ProcessStatus": MILESTONE_21_PROCESS_STATUS_SNAPSHOT,
            "milestone21Task7Used": MILESTONE_21_TASK_7_USED_SNAPSHOT,
            "milestone21Task8Used": MILESTONE_21_TASK_8_USED_SNAPSHOT,
            "milestone21ReserveUnused": MILESTONE_21_RESERVE_UNUSED_SNAPSHOT,
            "milestone21EmergencyReserveUnused": MILESTONE_21_EMERGENCY_RESERVE_UNUSED_SNAPSHOT,
            "milestone20FinalStatus": MILESTONE_20_FINAL_STATUS_SNAPSHOT,
            "milestone20Task8Used": MILESTONE_20_TASK_8_USED_SNAPSHOT,
            "milestone20EmergencyReserveUnused": MILESTONE_20_EMERGENCY_RESERVE_UNUSED_SNAPSHOT,
            "milestone19BudgetGuardActive": MILESTONE_19_BUDGET_GUARD_ACTIVE_SNAPSHOT,
            "governedOpeningReady": MILESTONE_22_GOVERNED_OPENING_READY,
            "implementationStarted": MILESTONE_22_IMPLEMENTATION_STARTED,
            "objectiveSelectionRequiredNext": MILESTONE_22_OBJECTIVE_SELECTION_REQUIRED_NEXT,
            "scopeLockRequiredNext": MILESTONE_22_SCOPE_LOCK_REQUIRED_NEXT,
            "closureRequired": MILESTONE_22_CLOSURE_REQUIRED,
            "noRecursiveMetaLayer": MILESTONE_22_NO_RECURSIVE_META_LAYER,
            "milestone21ReopenRequired": MILESTONE_21_REOPEN_REQUIRED,
            "milestone21Task7Required": MILESTONE_21_TASK_7_REQUIRED,
            "milestone21Task8Required": MILESTONE_21_TASK_8_REQUIRED,
            "milestone20ReopenRequired": MILESTONE_20_REOPEN_REQUIRED,
            "milestone20Task8Required": MILESTONE_20_TASK_8_REQUIRED,
            "milestone19ReopenRequired": MILESTONE_19_REOPEN_REQUIRED,
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
            "openingOk": self.opening_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["openingId"] = self.opening_id
        return payload


def build_milestone_22_governed_opening(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone22GovernedOpening:
    return Milestone22GovernedOpening(metadata={} if metadata is None else metadata)


def validate_milestone_22_governed_opening(opening: Milestone22GovernedOpening) -> tuple[str, ...]:
    return opening.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "MILESTONE_22_GOVERNED_OPENING_READY",
    "Milestone22GovernedOpening",
    "build_milestone_22_governed_opening",
    "validate_milestone_22_governed_opening",
]
