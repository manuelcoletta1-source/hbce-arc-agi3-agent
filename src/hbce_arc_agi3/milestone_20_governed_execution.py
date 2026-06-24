"""Milestone #20 governed execution.

Milestone 20 must run under the task-budget governance installed after
Milestone 19. Translation for the exhausted carbon-based operator: no more
infinite meta-task noodle soup.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_task_budget_governance import (
    STANDARD_MILESTONE_TASK_MAX,
    build_standard_milestone_policy,
)


TASK_ID = "MILESTONE_20_TASK_5_GOVERNED_EXECUTION_BUDGET_ALIGNMENT_V1"
MILESTONE_ID = "MILESTONE_20"
REVISION = "MILESTONE_20_GOVERNED_EXECUTION_WITH_TASK_BUDGET_MAX_8_v1"

MILESTONE_20_TASK_BUDGET_MAX = 8
MILESTONE_20_TASK_BUDGET_MIN = 5
MILESTONE_20_COMPLETED_TASK_COUNT_AT_ALIGNMENT = 4
MILESTONE_20_REMAINING_TASK_BUDGET_AFTER_ALIGNMENT = 3
MILESTONE_20_EMERGENCY_RESERVE_TASK_COUNT = 1

MILESTONE_20_GOVERNED_EXECUTION_READY = True
MILESTONE_20_NO_RECURSIVE_META_LAYER = True
MILESTONE_20_MAX_REVIEW_DEPTH = 1
MILESTONE_20_MAX_AUTHORIZATION_DEPTH = 1
MILESTONE_20_MAX_FINALIZATION_DEPTH = 1
MILESTONE_20_CLOSURE_REQUIRED = True
MILESTONE_20_REWRITE_MILESTONE_19_REQUIRED = False
MILESTONE_20_REOPEN_MILESTONE_19_REQUIRED = False

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
class Milestone20GovernedExecution:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    task_budget_min: int = MILESTONE_20_TASK_BUDGET_MIN
    task_budget_max: int = MILESTONE_20_TASK_BUDGET_MAX
    completed_task_count_at_alignment: int = MILESTONE_20_COMPLETED_TASK_COUNT_AT_ALIGNMENT
    current_task_number: int = 5
    recommended_closure_task_number: int = 7
    emergency_reserve_task_count: int = MILESTONE_20_EMERGENCY_RESERVE_TASK_COUNT
    stop_condition: str = "operator decision value selection gate validated, regression tested, full suite passed, milestone closure committed and pushed"
    completed_task_labels: tuple[str, ...] = (
        "MILESTONE_20_TASK_1_OPERATOR_DECISION_GATE",
        "MILESTONE_20_TASK_2_OPERATOR_DECISION_RECORD",
        "MILESTONE_20_TASK_3_OPERATOR_DECISION_RECORD_REVIEW",
        "MILESTONE_20_TASK_4_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE",
    )
    planned_remaining_task_labels: tuple[str, ...] = (
        "MILESTONE_20_TASK_5_GOVERNED_EXECUTION_BUDGET_ALIGNMENT",
        "MILESTONE_20_TASK_6_VALIDATION_AND_INTEGRATION",
        "MILESTONE_20_TASK_7_MILESTONE_CLOSURE",
    )
    emergency_only_task_label: str = "MILESTONE_20_TASK_8_EMERGENCY_RESERVE_ONLY"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def execution_id(self) -> str:
        return f"MILESTONE-20-GOVERNED-EXECUTION-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def remaining_budget_after_current_task(self) -> int:
        return self.task_budget_max - self.current_task_number

    @property
    def governed_execution_ok(self) -> bool:
        return (
            MILESTONE_20_GOVERNED_EXECUTION_READY is True
            and self.task_budget_max == STANDARD_MILESTONE_TASK_MAX
            and self.task_budget_max == 8
            and self.completed_task_count_at_alignment == 4
            and self.current_task_number == 5
            and self.recommended_closure_task_number <= 7
            and self.emergency_reserve_task_count == 1
            and MILESTONE_20_NO_RECURSIVE_META_LAYER is True
            and MILESTONE_20_MAX_REVIEW_DEPTH == 1
            and MILESTONE_20_MAX_AUTHORIZATION_DEPTH == 1
            and MILESTONE_20_MAX_FINALIZATION_DEPTH == 1
            and MILESTONE_20_CLOSURE_REQUIRED is True
            and MILESTONE_20_REWRITE_MILESTONE_19_REQUIRED is False
            and MILESTONE_20_REOPEN_MILESTONE_19_REQUIRED is False
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

        policy = build_standard_milestone_policy(
            milestone_id=self.milestone_id,
            objective="Explicit operator decision value selection gate governed execution",
            stop_condition=self.stop_condition,
            task_budget_min=self.task_budget_min,
            task_budget_max=self.task_budget_max,
            metadata={"source": REVISION},
        )

        if not policy.valid:
            issues.extend(f"POLICY_{issue}" for issue in policy.issues)
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number > self.task_budget_max:
            issues.append("CURRENT_TASK_EXCEEDS_BUDGET")
        if self.recommended_closure_task_number > self.task_budget_max:
            issues.append("RECOMMENDED_CLOSURE_EXCEEDS_BUDGET")
        if self.emergency_reserve_task_count != 1:
            issues.append("EMERGENCY_RESERVE_COUNT_MISMATCH")
        if not MILESTONE_20_NO_RECURSIVE_META_LAYER:
            issues.append("RECURSIVE_META_LAYER_ALLOWED")
        if MILESTONE_20_MAX_REVIEW_DEPTH != 1:
            issues.append("MAX_REVIEW_DEPTH_NOT_1")
        if MILESTONE_20_MAX_AUTHORIZATION_DEPTH != 1:
            issues.append("MAX_AUTHORIZATION_DEPTH_NOT_1")
        if MILESTONE_20_MAX_FINALIZATION_DEPTH != 1:
            issues.append("MAX_FINALIZATION_DEPTH_NOT_1")
        if not MILESTONE_20_CLOSURE_REQUIRED:
            issues.append("CLOSURE_NOT_REQUIRED")
        if MILESTONE_20_REWRITE_MILESTONE_19_REQUIRED:
            issues.append("MILESTONE_19_REWRITE_REQUIRED")
        if MILESTONE_20_REOPEN_MILESTONE_19_REQUIRED:
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
        return self.governed_execution_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "completedTaskCountAtAlignment": self.completed_task_count_at_alignment,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "emergencyReserveTaskCount": self.emergency_reserve_task_count,
            "stopCondition": self.stop_condition,
            "completedTaskLabels": list(self.completed_task_labels),
            "plannedRemainingTaskLabels": list(self.planned_remaining_task_labels),
            "emergencyOnlyTaskLabel": self.emergency_only_task_label,
            "governedExecutionReady": MILESTONE_20_GOVERNED_EXECUTION_READY,
            "governedExecutionOk": self.governed_execution_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "noRecursiveMetaLayer": MILESTONE_20_NO_RECURSIVE_META_LAYER,
            "maxReviewDepth": MILESTONE_20_MAX_REVIEW_DEPTH,
            "maxAuthorizationDepth": MILESTONE_20_MAX_AUTHORIZATION_DEPTH,
            "maxFinalizationDepth": MILESTONE_20_MAX_FINALIZATION_DEPTH,
            "closureRequired": MILESTONE_20_CLOSURE_REQUIRED,
            "rewriteMilestone19Required": MILESTONE_20_REWRITE_MILESTONE_19_REQUIRED,
            "reopenMilestone19Required": MILESTONE_20_REOPEN_MILESTONE_19_REQUIRED,
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
            "rawRequestBodyPersisted": RAW_REQUEST_BODY_PERSISTED,
            "secretPersisted": SECRET_PERSISTED,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["executionId"] = self.execution_id
        return payload


def build_milestone_20_governed_execution(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone20GovernedExecution:
    return Milestone20GovernedExecution(metadata={} if metadata is None else metadata)


def validate_milestone_20_governed_execution(execution: Milestone20GovernedExecution) -> tuple[str, ...]:
    return execution.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "MILESTONE_20_TASK_BUDGET_MAX",
    "MILESTONE_20_GOVERNED_EXECUTION_READY",
    "Milestone20GovernedExecution",
    "build_milestone_20_governed_execution",
    "validate_milestone_20_governed_execution",
]
