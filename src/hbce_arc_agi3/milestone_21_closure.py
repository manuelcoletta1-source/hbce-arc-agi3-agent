"""Milestone #21 Task 6 - Milestone Closure.

This closes Milestone 21 at Task 6 after governed opening, scope lock,
scoped implementation, validation artifacts, and integration regression.

Task 7 remains reserve-only. Task 8 remains emergency-only.
Neither is used. A small miracle: the process stopped when it said it would.
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
from hbce_arc_agi3.milestone_21_governed_opening import (
    build_milestone_21_governed_opening,
    validate_milestone_21_governed_opening,
)
from hbce_arc_agi3.milestone_21_objective_scope_lock import (
    build_milestone_21_objective_scope_lock,
    validate_milestone_21_objective_scope_lock,
)
from hbce_arc_agi3.milestone_21_operator_decision_handoff import (
    build_operator_decision_handoff_package,
    validate_operator_decision_handoff_package,
)
from hbce_arc_agi3.milestone_21_validation_artifacts import (
    build_handoff_validation_artifacts,
    validate_handoff_validation_artifacts,
)
from hbce_arc_agi3.milestone_21_integration_regression import (
    build_milestone_21_integration_regression,
    validate_milestone_21_integration_regression,
)


TASK_ID = "MILESTONE_21_TASK_6_MILESTONE_CLOSURE_V1"
REVISION = "MILESTONE_21_MILESTONE_CLOSURE_v1"
MILESTONE_ID = "MILESTONE_21"
NEXT_STAGE = "MILESTONE_21_CLOSED_NO_TASK_7_OR_8_USED"

TASK_BUDGET_MAX = 8
FINAL_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

MILESTONE_21_CLOSURE_READY = True
MILESTONE_21_CLOSED = True
MILESTONE_21_TECHNICAL_STATUS = "PASS"
MILESTONE_21_PROCESS_STATUS = "GOVERNED_WITHIN_TASK_BUDGET"
MILESTONE_21_FINAL_STATUS = "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
MILESTONE_21_TASK_7_USED = False
MILESTONE_21_TASK_8_USED = False
MILESTONE_21_RESERVE_UNUSED = True
MILESTONE_21_EMERGENCY_RESERVE_UNUSED = True

NO_RECURSIVE_META_LAYER = True
CLOSURE_REQUIRED = True
CLOSURE_COMPLETED = True

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
class Milestone21Closure:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    task_budget_max: int = TASK_BUDGET_MAX
    final_task_number: int = FINAL_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    completed_task_labels: tuple[str, ...] = (
        "MILESTONE_21_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET",
        "MILESTONE_21_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK",
        "MILESTONE_21_TASK_3_SCOPED_OPERATOR_DECISION_HANDOFF_IMPLEMENTATION",
        "MILESTONE_21_TASK_4_VALIDATION_AND_ARTIFACTS",
        "MILESTONE_21_TASK_5_INTEGRATION_REGRESSION",
        "MILESTONE_21_TASK_6_MILESTONE_CLOSURE",
    )
    reserve_task_label: str = "MILESTONE_21_TASK_7_RESERVE_ONLY_UNUSED"
    emergency_task_label: str = "MILESTONE_21_TASK_8_EMERGENCY_ONLY_UNUSED"
    closure_checks: tuple[str, ...] = (
        "milestone_20_closed_task_8_unused",
        "milestone_21_task_1_valid",
        "milestone_21_task_2_valid",
        "milestone_21_task_3_valid",
        "milestone_21_task_4_valid",
        "milestone_21_task_5_valid",
        "task_budget_respected",
        "reserve_tasks_unused",
        "forbidden_actions_absent",
        "fail_closed_boundary_preserved",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def closure_id(self) -> str:
        return f"MILESTONE-21-CLOSURE-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def completed_task_count(self) -> int:
        return len(self.completed_task_labels)

    @property
    def remaining_budget_after_closure(self) -> int:
        return self.task_budget_max - self.final_task_number

    @property
    def closure_ok(self) -> bool:
        milestone_20 = build_milestone_20_closure()
        task_1 = build_milestone_21_governed_opening()
        task_2 = build_milestone_21_objective_scope_lock()
        task_3 = build_operator_decision_handoff_package()
        task_4 = build_handoff_validation_artifacts()
        task_5 = build_milestone_21_integration_regression()

        p20 = milestone_20.to_public_dict()
        p5 = task_5.to_public_dict()

        return (
            MILESTONE_21_CLOSURE_READY is True
            and MILESTONE_21_CLOSED is True
            and MILESTONE_21_TECHNICAL_STATUS == "PASS"
            and MILESTONE_21_PROCESS_STATUS == "GOVERNED_WITHIN_TASK_BUDGET"
            and MILESTONE_21_FINAL_STATUS == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
            and MILESTONE_21_TASK_7_USED is False
            and MILESTONE_21_TASK_8_USED is False
            and MILESTONE_21_RESERVE_UNUSED is True
            and MILESTONE_21_EMERGENCY_RESERVE_UNUSED is True
            and milestone_20.valid is True
            and validate_milestone_20_closure(milestone_20) == ()
            and p20["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8"
            and p20["task8Used"] is False
            and task_1.valid is True
            and validate_milestone_21_governed_opening(task_1) == ()
            and task_2.valid is True
            and validate_milestone_21_objective_scope_lock(task_2) == ()
            and task_3.valid is True
            and validate_operator_decision_handoff_package(task_3) == ()
            and task_4.valid is True
            and validate_handoff_validation_artifacts(task_4) == ()
            and task_5.valid is True
            and validate_milestone_21_integration_regression(task_5) == ()
            and p5["readyForMilestoneClosure"] is True
            and p5["regressionChecksPassed"] is True
            and self.task_budget_max == 8
            and self.final_task_number == 6
            and self.completed_task_count == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.closure_checks) == 10
            and NO_RECURSIVE_META_LAYER is True
            and CLOSURE_REQUIRED is True
            and CLOSURE_COMPLETED is True
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

        milestone_20 = build_milestone_20_closure()
        task_1 = build_milestone_21_governed_opening()
        task_2 = build_milestone_21_objective_scope_lock()
        task_3 = build_operator_decision_handoff_package()
        task_4 = build_handoff_validation_artifacts()
        task_5 = build_milestone_21_integration_regression()

        if not milestone_20.valid:
            issues.append("MILESTONE_20_CLOSURE_INVALID")
        issues.extend(f"MILESTONE_20_{issue}" for issue in validate_milestone_20_closure(milestone_20))

        if not task_1.valid:
            issues.append("TASK_1_OPENING_INVALID")
        issues.extend(f"TASK_1_{issue}" for issue in validate_milestone_21_governed_opening(task_1))

        if not task_2.valid:
            issues.append("TASK_2_SCOPE_LOCK_INVALID")
        issues.extend(f"TASK_2_{issue}" for issue in validate_milestone_21_objective_scope_lock(task_2))

        if not task_3.valid:
            issues.append("TASK_3_HANDOFF_INVALID")
        issues.extend(f"TASK_3_{issue}" for issue in validate_operator_decision_handoff_package(task_3))

        if not task_4.valid:
            issues.append("TASK_4_ARTIFACTS_INVALID")
        issues.extend(f"TASK_4_{issue}" for issue in validate_handoff_validation_artifacts(task_4))

        if not task_5.valid:
            issues.append("TASK_5_REGRESSION_INVALID")
        issues.extend(f"TASK_5_{issue}" for issue in validate_milestone_21_integration_regression(task_5))

        if not MILESTONE_21_CLOSURE_READY:
            issues.append("CLOSURE_NOT_READY")
        if not MILESTONE_21_CLOSED:
            issues.append("MILESTONE_21_NOT_CLOSED")
        if MILESTONE_21_TECHNICAL_STATUS != "PASS":
            issues.append("TECHNICAL_STATUS_NOT_PASS")
        if MILESTONE_21_PROCESS_STATUS != "GOVERNED_WITHIN_TASK_BUDGET":
            issues.append("PROCESS_STATUS_NOT_GOVERNED_WITHIN_TASK_BUDGET")
        if MILESTONE_21_FINAL_STATUS != "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6":
            issues.append("FINAL_STATUS_INVALID")
        if MILESTONE_21_TASK_7_USED:
            issues.append("TASK_7_USED")
        if MILESTONE_21_TASK_8_USED:
            issues.append("TASK_8_USED")
        if not MILESTONE_21_RESERVE_UNUSED:
            issues.append("RESERVE_USED")
        if not MILESTONE_21_EMERGENCY_RESERVE_UNUSED:
            issues.append("EMERGENCY_RESERVE_USED")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.final_task_number != 6:
            issues.append("FINAL_TASK_NUMBER_NOT_6")
        if self.completed_task_count != 6:
            issues.append("COMPLETED_TASK_COUNT_NOT_6")
        if self.reserve_task_number != 7:
            issues.append("RESERVE_TASK_NUMBER_NOT_7")
        if self.emergency_only_task_number != 8:
            issues.append("EMERGENCY_TASK_NUMBER_NOT_8")
        if len(self.closure_checks) != 10:
            issues.append("CLOSURE_CHECK_COUNT_NOT_10")
        if not NO_RECURSIVE_META_LAYER:
            issues.append("RECURSIVE_META_LAYER_ALLOWED")
        if not CLOSURE_REQUIRED:
            issues.append("CLOSURE_NOT_REQUIRED")
        if not CLOSURE_COMPLETED:
            issues.append("CLOSURE_NOT_COMPLETED")
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
        return self.closure_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        milestone_20 = build_milestone_20_closure().to_public_dict()
        task_1 = build_milestone_21_governed_opening().to_public_dict()
        task_2 = build_milestone_21_objective_scope_lock().to_public_dict()
        task_3 = build_operator_decision_handoff_package().to_public_dict()
        task_4 = build_handoff_validation_artifacts().to_public_dict()
        task_5 = build_milestone_21_integration_regression().to_public_dict()

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "nextStage": self.next_stage,
            "taskBudgetMax": self.task_budget_max,
            "finalTaskNumber": self.final_task_number,
            "completedTaskLabels": list(self.completed_task_labels),
            "completedTaskCount": self.completed_task_count,
            "remainingBudgetAfterClosure": self.remaining_budget_after_closure,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "reserveTaskLabel": self.reserve_task_label,
            "emergencyTaskLabel": self.emergency_task_label,
            "milestone20ClosureId": milestone_20["closureId"],
            "milestone20FinalStatus": milestone_20["finalStatus"],
            "milestone20Task8Used": milestone_20["task8Used"],
            "task1OpeningId": task_1["openingId"],
            "task2LockRecordId": task_2["lockRecordId"],
            "task3HandoffId": task_3["handoffId"],
            "task4ValidationArtifactId": task_4["validationArtifactId"],
            "task5IntegrationRegressionId": task_5["integrationRegressionId"],
            "task5ReadyForMilestoneClosure": task_5["readyForMilestoneClosure"],
            "closureChecks": list(self.closure_checks),
            "closureCheckCount": len(self.closure_checks),
            "closureReady": MILESTONE_21_CLOSURE_READY,
            "milestone21Closed": MILESTONE_21_CLOSED,
            "technicalStatus": MILESTONE_21_TECHNICAL_STATUS,
            "processStatus": MILESTONE_21_PROCESS_STATUS,
            "finalStatus": MILESTONE_21_FINAL_STATUS,
            "task7Used": MILESTONE_21_TASK_7_USED,
            "task8Used": MILESTONE_21_TASK_8_USED,
            "reserveUnused": MILESTONE_21_RESERVE_UNUSED,
            "emergencyReserveUnused": MILESTONE_21_EMERGENCY_RESERVE_UNUSED,
            "noRecursiveMetaLayer": NO_RECURSIVE_META_LAYER,
            "closureRequired": CLOSURE_REQUIRED,
            "closureCompleted": CLOSURE_COMPLETED,
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
            "closureOk": self.closure_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["closureId"] = self.closure_id
        return payload


def build_milestone_21_closure(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone21Closure:
    return Milestone21Closure(metadata={} if metadata is None else metadata)


def validate_milestone_21_closure(closure: Milestone21Closure) -> tuple[str, ...]:
    return closure.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "MILESTONE_21_CLOSURE_READY",
    "MILESTONE_21_CLOSED",
    "MILESTONE_21_FINAL_STATUS",
    "Milestone21Closure",
    "build_milestone_21_closure",
    "validate_milestone_21_closure",
]
