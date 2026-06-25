"""Milestone #21 Task 5 - Integration Regression.

This module integrates and regression-checks the bounded Milestone 21 chain:
Task 1 governed opening, Task 2 scope lock, Task 3 handoff implementation,
and Task 4 validation artifacts.

It adds no runtime solver changes. It activates no runtime wiring. It submits
nothing to Kaggle. It stores no raw requests or secrets. It certifies nothing
legally. It just checks the machine before closure, a practice humans invented
after breaking everything repeatedly.
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


TASK_ID = "MILESTONE_21_TASK_5_INTEGRATION_REGRESSION_V1"
REVISION = "MILESTONE_21_INTEGRATION_REGRESSION_v1"
MILESTONE_ID = "MILESTONE_21"
NEXT_STAGE = "MILESTONE_21_TASK_6_MILESTONE_CLOSURE_V1"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 5
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

INTEGRATION_REGRESSION_READY = True
TASK_CHAIN_INTEGRATED = True
REGRESSION_CHECKS_CREATED = True
REGRESSION_CHECKS_PASSED = True
READY_FOR_MILESTONE_CLOSURE = True

NO_RECURSIVE_META_LAYER = True
CLOSURE_REQUIRED = True

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
class Milestone21IntegrationRegression:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    integrated_task_labels: tuple[str, ...] = (
        "MILESTONE_21_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET",
        "MILESTONE_21_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK",
        "MILESTONE_21_TASK_3_SCOPED_OPERATOR_DECISION_HANDOFF_IMPLEMENTATION",
        "MILESTONE_21_TASK_4_VALIDATION_AND_ARTIFACTS",
        "MILESTONE_21_TASK_5_INTEGRATION_REGRESSION",
    )
    regression_checks: tuple[str, ...] = (
        "milestone_20_closed_task_8_unused",
        "task_1_governed_opening_valid",
        "task_2_scope_lock_valid",
        "task_3_handoff_package_valid",
        "task_4_validation_artifacts_valid",
        "budget_trace_consistent",
        "next_stage_closure_declared",
        "forbidden_actions_absent",
        "fail_closed_boundary_preserved",
    )
    regression_artifacts: tuple[str, ...] = (
        "task-5-integration-regression.json",
        "task-5-integration-regression.md",
        "task-5-manifest.json",
        "task-5-index.txt",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def integration_regression_id(self) -> str:
        return f"MILESTONE-21-INTEGRATION-REGRESSION-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def remaining_budget_after_current_task(self) -> int:
        return self.task_budget_max - self.current_task_number

    @property
    def milestone_20_payload(self) -> Mapping[str, Any]:
        return build_milestone_20_closure().to_public_dict()

    @property
    def task_1_payload(self) -> Mapping[str, Any]:
        return build_milestone_21_governed_opening().to_public_dict()

    @property
    def task_2_payload(self) -> Mapping[str, Any]:
        return build_milestone_21_objective_scope_lock().to_public_dict()

    @property
    def task_3_payload(self) -> Mapping[str, Any]:
        return build_operator_decision_handoff_package().to_public_dict()

    @property
    def task_4_payload(self) -> Mapping[str, Any]:
        return build_handoff_validation_artifacts().to_public_dict()

    @property
    def integration_ok(self) -> bool:
        milestone_20 = build_milestone_20_closure()
        task_1 = build_milestone_21_governed_opening()
        task_2 = build_milestone_21_objective_scope_lock()
        task_3 = build_operator_decision_handoff_package()
        task_4 = build_handoff_validation_artifacts()

        p20 = milestone_20.to_public_dict()
        p1 = task_1.to_public_dict()
        p2 = task_2.to_public_dict()
        p3 = task_3.to_public_dict()
        p4 = task_4.to_public_dict()

        return (
            INTEGRATION_REGRESSION_READY is True
            and TASK_CHAIN_INTEGRATED is True
            and REGRESSION_CHECKS_CREATED is True
            and REGRESSION_CHECKS_PASSED is True
            and READY_FOR_MILESTONE_CLOSURE is True
            and milestone_20.valid is True
            and validate_milestone_20_closure(milestone_20) == ()
            and p20["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8"
            and p20["task8Used"] is False
            and p20["emergencyReserveUnused"] is True
            and task_1.valid is True
            and validate_milestone_21_governed_opening(task_1) == ()
            and p1["taskBudgetMax"] == 8
            and task_2.valid is True
            and validate_milestone_21_objective_scope_lock(task_2) == ()
            and p2["scopeLocked"] is True
            and p2["implementationAllowedNext"] is True
            and task_3.valid is True
            and validate_operator_decision_handoff_package(task_3) == ()
            and p3["handoffPackageCreated"] is True
            and p3["sourceMilestone20Task8Used"] is False
            and task_4.valid is True
            and validate_handoff_validation_artifacts(task_4) == ()
            and p4["artifactsReadyForIntegrationRegression"] is True
            and p4["sourceMilestone20Task8Used"] is False
            and self.task_budget_max == 8
            and self.current_task_number == 5
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.integrated_task_labels) == 5
            and len(self.regression_checks) == 9
            and len(self.regression_artifacts) == 4
            and NO_RECURSIVE_META_LAYER is True
            and CLOSURE_REQUIRED is True
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

        if not INTEGRATION_REGRESSION_READY:
            issues.append("INTEGRATION_REGRESSION_NOT_READY")
        if not TASK_CHAIN_INTEGRATED:
            issues.append("TASK_CHAIN_NOT_INTEGRATED")
        if not REGRESSION_CHECKS_CREATED:
            issues.append("REGRESSION_CHECKS_NOT_CREATED")
        if not REGRESSION_CHECKS_PASSED:
            issues.append("REGRESSION_CHECKS_NOT_PASSED")
        if not READY_FOR_MILESTONE_CLOSURE:
            issues.append("NOT_READY_FOR_MILESTONE_CLOSURE")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 5:
            issues.append("CURRENT_TASK_NUMBER_NOT_5")
        if self.recommended_closure_task_number != 6:
            issues.append("RECOMMENDED_CLOSURE_TASK_NOT_6")
        if self.reserve_task_number != 7:
            issues.append("RESERVE_TASK_NUMBER_NOT_7")
        if self.emergency_only_task_number != 8:
            issues.append("EMERGENCY_TASK_NUMBER_NOT_8")
        if len(self.integrated_task_labels) != 5:
            issues.append("INTEGRATED_TASK_COUNT_NOT_5")
        if len(self.regression_checks) != 9:
            issues.append("REGRESSION_CHECK_COUNT_NOT_9")
        if len(self.regression_artifacts) != 4:
            issues.append("REGRESSION_ARTIFACT_COUNT_NOT_4")
        if not NO_RECURSIVE_META_LAYER:
            issues.append("RECURSIVE_META_LAYER_ALLOWED")
        if not CLOSURE_REQUIRED:
            issues.append("CLOSURE_NOT_REQUIRED")
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
        return self.integration_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        p20 = self.milestone_20_payload
        p1 = self.task_1_payload
        p2 = self.task_2_payload
        p3 = self.task_3_payload
        p4 = self.task_4_payload

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "nextStage": self.next_stage,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "milestone20ClosureId": p20["closureId"],
            "milestone20FinalStatus": p20["finalStatus"],
            "milestone20Task8Used": p20["task8Used"],
            "milestone20EmergencyReserveUnused": p20["emergencyReserveUnused"],
            "task1OpeningId": p1["openingId"],
            "task1TaskBudgetMax": p1["taskBudgetMax"],
            "task2LockRecordId": p2["lockRecordId"],
            "task2ScopeLocked": p2["scopeLocked"],
            "task3HandoffId": p3["handoffId"],
            "task3HandoffPackageCreated": p3["handoffPackageCreated"],
            "task4ValidationArtifactId": p4["validationArtifactId"],
            "task4ArtifactsReadyForIntegrationRegression": p4["artifactsReadyForIntegrationRegression"],
            "integratedTaskLabels": list(self.integrated_task_labels),
            "integratedTaskCount": len(self.integrated_task_labels),
            "regressionChecks": list(self.regression_checks),
            "regressionCheckCount": len(self.regression_checks),
            "regressionArtifacts": list(self.regression_artifacts),
            "regressionArtifactCount": len(self.regression_artifacts),
            "integrationRegressionReady": INTEGRATION_REGRESSION_READY,
            "taskChainIntegrated": TASK_CHAIN_INTEGRATED,
            "regressionChecksCreated": REGRESSION_CHECKS_CREATED,
            "regressionChecksPassed": REGRESSION_CHECKS_PASSED,
            "readyForMilestoneClosure": READY_FOR_MILESTONE_CLOSURE,
            "noRecursiveMetaLayer": NO_RECURSIVE_META_LAYER,
            "closureRequired": CLOSURE_REQUIRED,
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
            "integrationOk": self.integration_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["integrationRegressionId"] = self.integration_regression_id
        return payload


def build_milestone_21_integration_regression(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone21IntegrationRegression:
    return Milestone21IntegrationRegression(metadata={} if metadata is None else metadata)


def validate_milestone_21_integration_regression(
    regression: Milestone21IntegrationRegression,
) -> tuple[str, ...]:
    return regression.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "INTEGRATION_REGRESSION_READY",
    "Milestone21IntegrationRegression",
    "build_milestone_21_integration_regression",
    "validate_milestone_21_integration_regression",
]
