"""Milestone #21 Task 2 - Objective Selection and Scope Lock.

This locks the objective before implementation. Humanity has tried the other
way around. It produced meetings, budget overruns, and software archaeology.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_21_governed_opening import (
    build_milestone_21_governed_opening,
    validate_milestone_21_governed_opening,
)
from hbce_arc_agi3.milestone_20_closure import (
    build_milestone_20_closure,
    validate_milestone_20_closure,
)


TASK_ID = "MILESTONE_21_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
REVISION = "MILESTONE_21_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_v1"
MILESTONE_ID = "MILESTONE_21"

SELECTED_OBJECTIVE = (
    "Build a governed local-only operator decision handoff package that carries the "
    "Milestone 20 operator-decision closure state into a bounded diagnostic implementation path."
)

SCOPE_LOCK_ID = "MILESTONE_21_SCOPE_OPERATOR_DECISION_HANDOFF_LOCAL_ONLY"
NEXT_STAGE = "MILESTONE_21_TASK_3_SCOPED_OPERATOR_DECISION_HANDOFF_IMPLEMENTATION_V1"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 2
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

OBJECTIVE_SELECTED = True
SCOPE_LOCK_READY = True
SCOPE_LOCKED = True
IMPLEMENTATION_ALLOWED_NEXT = True
IMPLEMENTATION_STARTED = False
CLOSURE_REQUIRED = True
NO_RECURSIVE_META_LAYER = True

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
class Milestone21ObjectiveScopeLock:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    selected_objective: str = SELECTED_OBJECTIVE
    scope_lock_id: str = SCOPE_LOCK_ID
    next_stage: str = NEXT_STAGE
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    in_scope_items: tuple[str, ...] = (
        "local_operator_decision_handoff_package",
        "milestone_20_closure_state_reference",
        "governed_budget_trace",
        "fail_closed_boundary_markers",
        "next_task_implementation_contract",
    )
    out_of_scope_items: tuple[str, ...] = (
        "runtime_solver_modification",
        "runtime_wiring_activation",
        "kaggle_submission",
        "raw_request_body_persistence",
        "secret_persistence",
        "legal_certification_claim",
        "milestone_20_reopen",
        "milestone_20_task_8_use",
        "milestone_19_reopen",
        "recursive_meta_layer",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def lock_record_id(self) -> str:
        return f"MILESTONE-21-SCOPE-LOCK-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def remaining_budget_after_current_task(self) -> int:
        return self.task_budget_max - self.current_task_number

    @property
    def scope_lock_ok(self) -> bool:
        opening = build_milestone_21_governed_opening()
        milestone_20 = build_milestone_20_closure()

        return (
            OBJECTIVE_SELECTED is True
            and SCOPE_LOCK_READY is True
            and SCOPE_LOCKED is True
            and IMPLEMENTATION_ALLOWED_NEXT is True
            and IMPLEMENTATION_STARTED is False
            and CLOSURE_REQUIRED is True
            and NO_RECURSIVE_META_LAYER is True
            and opening.valid is True
            and validate_milestone_21_governed_opening(opening) == ()
            and milestone_20.valid is True
            and validate_milestone_20_closure(milestone_20) == ()
            and self.task_budget_max == 8
            and self.current_task_number == 2
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.in_scope_items) == 5
            and len(self.out_of_scope_items) == 10
            and MAX_REVIEW_DEPTH == 1
            and MAX_AUTHORIZATION_DEPTH == 1
            and MAX_FINALIZATION_DEPTH == 1
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

        opening = build_milestone_21_governed_opening()
        milestone_20 = build_milestone_20_closure()

        if not opening.valid:
            issues.append("MILESTONE_21_OPENING_INVALID")
        issues.extend(f"MILESTONE_21_OPENING_{issue}" for issue in validate_milestone_21_governed_opening(opening))

        if not milestone_20.valid:
            issues.append("MILESTONE_20_NOT_CLOSED")
        issues.extend(f"MILESTONE_20_{issue}" for issue in validate_milestone_20_closure(milestone_20))

        if not OBJECTIVE_SELECTED:
            issues.append("OBJECTIVE_NOT_SELECTED")
        if not SCOPE_LOCK_READY:
            issues.append("SCOPE_LOCK_NOT_READY")
        if not SCOPE_LOCKED:
            issues.append("SCOPE_NOT_LOCKED")
        if not IMPLEMENTATION_ALLOWED_NEXT:
            issues.append("IMPLEMENTATION_NOT_ALLOWED_NEXT")
        if IMPLEMENTATION_STARTED:
            issues.append("IMPLEMENTATION_STARTED_TOO_EARLY")
        if not CLOSURE_REQUIRED:
            issues.append("CLOSURE_NOT_REQUIRED")
        if not NO_RECURSIVE_META_LAYER:
            issues.append("RECURSIVE_META_LAYER_ALLOWED")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 2:
            issues.append("CURRENT_TASK_NUMBER_NOT_2")
        if self.recommended_closure_task_number != 6:
            issues.append("RECOMMENDED_CLOSURE_TASK_NOT_6")
        if self.reserve_task_number != 7:
            issues.append("RESERVE_TASK_NUMBER_NOT_7")
        if self.emergency_only_task_number != 8:
            issues.append("EMERGENCY_TASK_NUMBER_NOT_8")
        if len(self.in_scope_items) != 5:
            issues.append("IN_SCOPE_ITEM_COUNT_NOT_5")
        if len(self.out_of_scope_items) != 10:
            issues.append("OUT_OF_SCOPE_ITEM_COUNT_NOT_10")
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
        return self.scope_lock_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "selectedObjective": self.selected_objective,
            "scopeLockId": self.scope_lock_id,
            "nextStage": self.next_stage,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "inScopeItems": list(self.in_scope_items),
            "inScopeItemCount": len(self.in_scope_items),
            "outOfScopeItems": list(self.out_of_scope_items),
            "outOfScopeItemCount": len(self.out_of_scope_items),
            "objectiveSelected": OBJECTIVE_SELECTED,
            "scopeLockReady": SCOPE_LOCK_READY,
            "scopeLocked": SCOPE_LOCKED,
            "implementationAllowedNext": IMPLEMENTATION_ALLOWED_NEXT,
            "implementationStarted": IMPLEMENTATION_STARTED,
            "closureRequired": CLOSURE_REQUIRED,
            "noRecursiveMetaLayer": NO_RECURSIVE_META_LAYER,
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
            "scopeLockOk": self.scope_lock_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["lockRecordId"] = self.lock_record_id
        return payload


def build_milestone_21_objective_scope_lock(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone21ObjectiveScopeLock:
    return Milestone21ObjectiveScopeLock(metadata={} if metadata is None else metadata)


def validate_milestone_21_objective_scope_lock(lock: Milestone21ObjectiveScopeLock) -> tuple[str, ...]:
    return lock.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "SELECTED_OBJECTIVE",
    "SCOPE_LOCK_ID",
    "NEXT_STAGE",
    "Milestone21ObjectiveScopeLock",
    "build_milestone_21_objective_scope_lock",
    "validate_milestone_21_objective_scope_lock",
]
