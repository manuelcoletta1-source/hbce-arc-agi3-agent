"""Milestone #20 closure.

This closes Milestone 20 under the task-budget governance introduced after
Milestone 19. No Task 8 is used. No recursive meta-layer is allowed. No runtime,
solver, Kaggle, raw payload, secret, or legal-certification claim is introduced.

A milestone ending at Task 7: civilization has briefly remembered how counting works.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_20_governed_execution import (
    build_milestone_20_governed_execution,
    validate_milestone_20_governed_execution,
)
from hbce_arc_agi3.milestone_20_validation_integration import (
    build_milestone_20_validation_integration,
    validate_milestone_20_validation_integration,
)
from hbce_arc_agi3.milestone_task_budget_governance import (
    build_milestone_19_final_closure,
    validate_milestone_19_final_closure,
)


TASK_ID = "MILESTONE_20_TASK_7_MILESTONE_CLOSURE_V1"
REVISION = "MILESTONE_20_CLOSURE_v1"
MILESTONE_ID = "MILESTONE_20"

TASK_BUDGET_MAX = 8
FINAL_TASK_NUMBER = 7
EMERGENCY_RESERVE_TASK_NUMBER = 8

MILESTONE_20_CLOSURE_READY = True
MILESTONE_20_CLOSED = True
MILESTONE_20_TECHNICAL_STATUS = "PASS"
MILESTONE_20_PROCESS_STATUS = "GOVERNED_WITHIN_TASK_BUDGET"
MILESTONE_20_FINAL_STATUS = "CLOSED_WITH_TASK_BUDGET_MAX_8"
MILESTONE_20_TASK_8_USED = False
MILESTONE_20_EMERGENCY_RESERVE_UNUSED = True
MILESTONE_20_NO_RECURSIVE_META_LAYER = True
MILESTONE_20_REOPEN_MILESTONE_19_REQUIRED = False
MILESTONE_20_REWRITE_MILESTONE_19_REQUIRED = False

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
class Milestone20Closure:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    task_budget_max: int = TASK_BUDGET_MAX
    final_task_number: int = FINAL_TASK_NUMBER
    emergency_reserve_task_number: int = EMERGENCY_RESERVE_TASK_NUMBER
    completed_task_labels: tuple[str, ...] = (
        "MILESTONE_20_TASK_1_OPERATOR_DECISION_GATE",
        "MILESTONE_20_TASK_2_OPERATOR_DECISION_RECORD",
        "MILESTONE_20_TASK_3_OPERATOR_DECISION_RECORD_REVIEW",
        "MILESTONE_20_TASK_4_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE",
        "MILESTONE_20_TASK_5_GOVERNED_EXECUTION_BUDGET_ALIGNMENT",
        "MILESTONE_20_TASK_6_VALIDATION_AND_INTEGRATION",
        "MILESTONE_20_TASK_7_MILESTONE_CLOSURE",
    )
    emergency_only_task_label: str = "MILESTONE_20_TASK_8_EMERGENCY_RESERVE_ONLY_UNUSED"
    closure_summary: str = "Milestone 20 closed within task budget after governed execution validation."
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def closure_id(self) -> str:
        return f"MILESTONE-20-CLOSURE-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def completed_task_count(self) -> int:
        return len(self.completed_task_labels)

    @property
    def closure_ok(self) -> bool:
        milestone_19 = build_milestone_19_final_closure()
        milestone_20_governance = build_milestone_20_governed_execution()
        milestone_20_validation = build_milestone_20_validation_integration()

        return (
            MILESTONE_20_CLOSURE_READY is True
            and MILESTONE_20_CLOSED is True
            and MILESTONE_20_TECHNICAL_STATUS == "PASS"
            and MILESTONE_20_PROCESS_STATUS == "GOVERNED_WITHIN_TASK_BUDGET"
            and MILESTONE_20_FINAL_STATUS == "CLOSED_WITH_TASK_BUDGET_MAX_8"
            and self.task_budget_max == 8
            and self.final_task_number == 7
            and self.completed_task_count == 7
            and self.emergency_reserve_task_number == 8
            and MILESTONE_20_TASK_8_USED is False
            and MILESTONE_20_EMERGENCY_RESERVE_UNUSED is True
            and MILESTONE_20_NO_RECURSIVE_META_LAYER is True
            and MAX_REVIEW_DEPTH == 1
            and MAX_AUTHORIZATION_DEPTH == 1
            and MAX_FINALIZATION_DEPTH == 1
            and milestone_19.closure_ok is True
            and validate_milestone_19_final_closure(milestone_19) == ()
            and milestone_20_governance.valid is True
            and validate_milestone_20_governed_execution(milestone_20_governance) == ()
            and milestone_20_validation.valid is True
            and validate_milestone_20_validation_integration(milestone_20_validation) == ()
            and MILESTONE_20_REOPEN_MILESTONE_19_REQUIRED is False
            and MILESTONE_20_REWRITE_MILESTONE_19_REQUIRED is False
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
        milestone_20_governance = build_milestone_20_governed_execution()
        milestone_20_validation = build_milestone_20_validation_integration()

        if not milestone_19.closure_ok:
            issues.append("MILESTONE_19_NOT_CLOSED")
        issues.extend(f"MILESTONE_19_{issue}" for issue in validate_milestone_19_final_closure(milestone_19))

        if not milestone_20_governance.valid:
            issues.append("MILESTONE_20_GOVERNANCE_INVALID")
        issues.extend(f"MILESTONE_20_GOVERNANCE_{issue}" for issue in validate_milestone_20_governed_execution(milestone_20_governance))

        if not milestone_20_validation.valid:
            issues.append("MILESTONE_20_VALIDATION_INVALID")
        issues.extend(f"MILESTONE_20_VALIDATION_{issue}" for issue in validate_milestone_20_validation_integration(milestone_20_validation))

        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.final_task_number != 7:
            issues.append("FINAL_TASK_NUMBER_NOT_7")
        if self.completed_task_count != 7:
            issues.append("COMPLETED_TASK_COUNT_NOT_7")
        if self.emergency_reserve_task_number != 8:
            issues.append("EMERGENCY_RESERVE_TASK_NUMBER_NOT_8")
        if MILESTONE_20_TASK_8_USED:
            issues.append("TASK_8_USED_UNEXPECTEDLY")
        if not MILESTONE_20_EMERGENCY_RESERVE_UNUSED:
            issues.append("EMERGENCY_RESERVE_USED")
        if not MILESTONE_20_NO_RECURSIVE_META_LAYER:
            issues.append("RECURSIVE_META_LAYER_ALLOWED")
        if MAX_REVIEW_DEPTH != 1:
            issues.append("MAX_REVIEW_DEPTH_NOT_1")
        if MAX_AUTHORIZATION_DEPTH != 1:
            issues.append("MAX_AUTHORIZATION_DEPTH_NOT_1")
        if MAX_FINALIZATION_DEPTH != 1:
            issues.append("MAX_FINALIZATION_DEPTH_NOT_1")
        if MILESTONE_20_REOPEN_MILESTONE_19_REQUIRED:
            issues.append("MILESTONE_19_REOPEN_REQUIRED")
        if MILESTONE_20_REWRITE_MILESTONE_19_REQUIRED:
            issues.append("MILESTONE_19_REWRITE_REQUIRED")
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
        return self.closure_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "taskBudgetMax": self.task_budget_max,
            "finalTaskNumber": self.final_task_number,
            "completedTaskLabels": list(self.completed_task_labels),
            "completedTaskCount": self.completed_task_count,
            "emergencyReserveTaskNumber": self.emergency_reserve_task_number,
            "emergencyOnlyTaskLabel": self.emergency_only_task_label,
            "closureSummary": self.closure_summary,
            "milestone20ClosureReady": MILESTONE_20_CLOSURE_READY,
            "milestone20Closed": MILESTONE_20_CLOSED,
            "technicalStatus": MILESTONE_20_TECHNICAL_STATUS,
            "processStatus": MILESTONE_20_PROCESS_STATUS,
            "finalStatus": MILESTONE_20_FINAL_STATUS,
            "task8Used": MILESTONE_20_TASK_8_USED,
            "emergencyReserveUnused": MILESTONE_20_EMERGENCY_RESERVE_UNUSED,
            "noRecursiveMetaLayer": MILESTONE_20_NO_RECURSIVE_META_LAYER,
            "maxReviewDepth": MAX_REVIEW_DEPTH,
            "maxAuthorizationDepth": MAX_AUTHORIZATION_DEPTH,
            "maxFinalizationDepth": MAX_FINALIZATION_DEPTH,
            "reopenMilestone19Required": MILESTONE_20_REOPEN_MILESTONE_19_REQUIRED,
            "rewriteMilestone19Required": MILESTONE_20_REWRITE_MILESTONE_19_REQUIRED,
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
            "rawRequestBodyPersisted": RAW_REQUEST_BODY_PERSISTED,
            "secretPersisted": SECRET_PERSISTED,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
            "closureOk": self.closure_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["closureId"] = self.closure_id
        return payload


def build_milestone_20_closure(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone20Closure:
    return Milestone20Closure(metadata={} if metadata is None else metadata)


def validate_milestone_20_closure(closure: Milestone20Closure) -> tuple[str, ...]:
    return closure.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "MILESTONE_20_CLOSURE_READY",
    "MILESTONE_20_CLOSED",
    "MILESTONE_20_FINAL_STATUS",
    "Milestone20Closure",
    "build_milestone_20_closure",
    "validate_milestone_20_closure",
]
