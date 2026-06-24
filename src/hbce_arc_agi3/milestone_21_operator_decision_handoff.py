"""Milestone #21 Task 3 - Scoped Operator Decision Handoff Implementation.

This module implements a local-only handoff package carrying the Milestone 20
operator-decision closure state into the bounded Milestone 21 diagnostic path.

It does not modify the runtime solver. It does not activate runtime wiring.
It does not submit to Kaggle. It does not persist raw request bodies or secrets.
It does not make legal-certification claims.

A handoff, not a séance. Important distinction, apparently.
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
from hbce_arc_agi3.milestone_21_objective_scope_lock import (
    SCOPE_LOCK_ID,
    build_milestone_21_objective_scope_lock,
    validate_milestone_21_objective_scope_lock,
)


TASK_ID = "MILESTONE_21_TASK_3_SCOPED_OPERATOR_DECISION_HANDOFF_IMPLEMENTATION_V1"
REVISION = "MILESTONE_21_SCOPED_OPERATOR_DECISION_HANDOFF_IMPLEMENTATION_v1"
MILESTONE_ID = "MILESTONE_21"
NEXT_STAGE = "MILESTONE_21_TASK_4_VALIDATION_AND_ARTIFACTS_V1"

HANDOFF_KIND = "LOCAL_ONLY_OPERATOR_DECISION_HANDOFF_PACKAGE"
HANDOFF_SCOPE_ID = SCOPE_LOCK_ID
SOURCE_MILESTONE_ID = "MILESTONE_20"
SOURCE_TASK_ID = "MILESTONE_20_TASK_7_MILESTONE_CLOSURE_V1"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 3
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

HANDOFF_IMPLEMENTATION_READY = True
HANDOFF_PACKAGE_CREATED = True
HANDOFF_LOCAL_ONLY = True
HANDOFF_BOUNDED_DIAGNOSTIC_ONLY = True
HANDOFF_CARRIES_MILESTONE_20_CLOSURE_STATE = True
HANDOFF_CARRIES_SCOPE_LOCK = True
HANDOFF_CARRIES_BUDGET_TRACE = True
HANDOFF_CARRIES_FAIL_CLOSED_BOUNDARY = True
HANDOFF_READY_FOR_VALIDATION_ARTIFACTS = True

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
class OperatorDecisionHandoffPackage:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    handoff_kind: str = HANDOFF_KIND
    handoff_scope_id: str = HANDOFF_SCOPE_ID
    source_milestone_id: str = SOURCE_MILESTONE_ID
    source_task_id: str = SOURCE_TASK_ID
    next_stage: str = NEXT_STAGE
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    carried_state_keys: tuple[str, ...] = (
        "milestone20ClosureId",
        "milestone20FinalStatus",
        "milestone20Task8Used",
        "milestone20EmergencyReserveUnused",
        "milestone21ScopeLockId",
        "milestone21TaskBudgetMax",
        "milestone21CurrentTaskNumber",
        "failClosedBoundary",
        "nextStage",
    )
    implementation_contract_items: tuple[str, ...] = (
        "build_local_only_handoff_payload",
        "reference_milestone_20_closure_state",
        "include_scope_lock_trace",
        "include_budget_trace",
        "include_fail_closed_boundary_markers",
        "prepare_validation_artifact_handoff",
    )
    forbidden_actions: tuple[str, ...] = (
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
    def handoff_id(self) -> str:
        return f"MILESTONE-21-OPERATOR-DECISION-HANDOFF-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def remaining_budget_after_current_task(self) -> int:
        return self.task_budget_max - self.current_task_number

    @property
    def milestone_20_closure_payload(self) -> Mapping[str, Any]:
        closure = build_milestone_20_closure()
        return closure.to_public_dict()

    @property
    def scope_lock_payload(self) -> Mapping[str, Any]:
        lock = build_milestone_21_objective_scope_lock()
        return lock.to_public_dict()

    @property
    def handoff_ok(self) -> bool:
        closure = build_milestone_20_closure()
        lock = build_milestone_21_objective_scope_lock()

        closure_payload = closure.to_public_dict()
        lock_payload = lock.to_public_dict()

        return (
            HANDOFF_IMPLEMENTATION_READY is True
            and HANDOFF_PACKAGE_CREATED is True
            and HANDOFF_LOCAL_ONLY is True
            and HANDOFF_BOUNDED_DIAGNOSTIC_ONLY is True
            and HANDOFF_CARRIES_MILESTONE_20_CLOSURE_STATE is True
            and HANDOFF_CARRIES_SCOPE_LOCK is True
            and HANDOFF_CARRIES_BUDGET_TRACE is True
            and HANDOFF_CARRIES_FAIL_CLOSED_BOUNDARY is True
            and HANDOFF_READY_FOR_VALIDATION_ARTIFACTS is True
            and closure.valid is True
            and validate_milestone_20_closure(closure) == ()
            and closure_payload["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8"
            and closure_payload["task8Used"] is False
            and closure_payload["emergencyReserveUnused"] is True
            and lock.valid is True
            and validate_milestone_21_objective_scope_lock(lock) == ()
            and lock_payload["scopeLockId"] == SCOPE_LOCK_ID
            and lock_payload["scopeLocked"] is True
            and lock_payload["implementationAllowedNext"] is True
            and lock_payload["implementationStarted"] is False
            and self.handoff_scope_id == SCOPE_LOCK_ID
            and self.task_budget_max == 8
            and self.current_task_number == 3
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.carried_state_keys) == 9
            and len(self.implementation_contract_items) == 6
            and len(self.forbidden_actions) == 10
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

        closure = build_milestone_20_closure()
        lock = build_milestone_21_objective_scope_lock()

        if not closure.valid:
            issues.append("MILESTONE_20_CLOSURE_INVALID")
        issues.extend(f"MILESTONE_20_{issue}" for issue in validate_milestone_20_closure(closure))

        if not lock.valid:
            issues.append("MILESTONE_21_SCOPE_LOCK_INVALID")
        issues.extend(f"MILESTONE_21_SCOPE_LOCK_{issue}" for issue in validate_milestone_21_objective_scope_lock(lock))

        if not HANDOFF_IMPLEMENTATION_READY:
            issues.append("HANDOFF_IMPLEMENTATION_NOT_READY")
        if not HANDOFF_PACKAGE_CREATED:
            issues.append("HANDOFF_PACKAGE_NOT_CREATED")
        if not HANDOFF_LOCAL_ONLY:
            issues.append("HANDOFF_NOT_LOCAL_ONLY")
        if not HANDOFF_BOUNDED_DIAGNOSTIC_ONLY:
            issues.append("HANDOFF_NOT_BOUNDED_DIAGNOSTIC_ONLY")
        if not HANDOFF_CARRIES_MILESTONE_20_CLOSURE_STATE:
            issues.append("MILESTONE_20_CLOSURE_STATE_NOT_CARRIED")
        if not HANDOFF_CARRIES_SCOPE_LOCK:
            issues.append("SCOPE_LOCK_NOT_CARRIED")
        if not HANDOFF_CARRIES_BUDGET_TRACE:
            issues.append("BUDGET_TRACE_NOT_CARRIED")
        if not HANDOFF_CARRIES_FAIL_CLOSED_BOUNDARY:
            issues.append("FAIL_CLOSED_BOUNDARY_NOT_CARRIED")
        if not HANDOFF_READY_FOR_VALIDATION_ARTIFACTS:
            issues.append("NOT_READY_FOR_VALIDATION_ARTIFACTS")
        if self.handoff_scope_id != SCOPE_LOCK_ID:
            issues.append("SCOPE_LOCK_ID_MISMATCH")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 3:
            issues.append("CURRENT_TASK_NUMBER_NOT_3")
        if self.recommended_closure_task_number != 6:
            issues.append("RECOMMENDED_CLOSURE_TASK_NOT_6")
        if self.reserve_task_number != 7:
            issues.append("RESERVE_TASK_NUMBER_NOT_7")
        if self.emergency_only_task_number != 8:
            issues.append("EMERGENCY_TASK_NUMBER_NOT_8")
        if len(self.carried_state_keys) != 9:
            issues.append("CARRIED_STATE_KEY_COUNT_NOT_9")
        if len(self.implementation_contract_items) != 6:
            issues.append("IMPLEMENTATION_CONTRACT_ITEM_COUNT_NOT_6")
        if len(self.forbidden_actions) != 10:
            issues.append("FORBIDDEN_ACTION_COUNT_NOT_10")
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
        return self.handoff_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        closure_payload = self.milestone_20_closure_payload
        scope_payload = self.scope_lock_payload

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "handoffKind": self.handoff_kind,
            "handoffScopeId": self.handoff_scope_id,
            "sourceMilestoneId": self.source_milestone_id,
            "sourceTaskId": self.source_task_id,
            "sourceMilestone20ClosureId": closure_payload["closureId"],
            "sourceMilestone20FinalStatus": closure_payload["finalStatus"],
            "sourceMilestone20Task8Used": closure_payload["task8Used"],
            "sourceMilestone20EmergencyReserveUnused": closure_payload["emergencyReserveUnused"],
            "scopeLockRecordId": scope_payload["lockRecordId"],
            "scopeLockId": scope_payload["scopeLockId"],
            "scopeLocked": scope_payload["scopeLocked"],
            "implementationAllowedByScope": scope_payload["implementationAllowedNext"],
            "implementationStartedBeforeTask3": scope_payload["implementationStarted"],
            "nextStage": self.next_stage,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "carriedStateKeys": list(self.carried_state_keys),
            "carriedStateKeyCount": len(self.carried_state_keys),
            "implementationContractItems": list(self.implementation_contract_items),
            "implementationContractItemCount": len(self.implementation_contract_items),
            "forbiddenActions": list(self.forbidden_actions),
            "forbiddenActionCount": len(self.forbidden_actions),
            "handoffImplementationReady": HANDOFF_IMPLEMENTATION_READY,
            "handoffPackageCreated": HANDOFF_PACKAGE_CREATED,
            "handoffLocalOnly": HANDOFF_LOCAL_ONLY,
            "handoffBoundedDiagnosticOnly": HANDOFF_BOUNDED_DIAGNOSTIC_ONLY,
            "handoffCarriesMilestone20ClosureState": HANDOFF_CARRIES_MILESTONE_20_CLOSURE_STATE,
            "handoffCarriesScopeLock": HANDOFF_CARRIES_SCOPE_LOCK,
            "handoffCarriesBudgetTrace": HANDOFF_CARRIES_BUDGET_TRACE,
            "handoffCarriesFailClosedBoundary": HANDOFF_CARRIES_FAIL_CLOSED_BOUNDARY,
            "handoffReadyForValidationArtifacts": HANDOFF_READY_FOR_VALIDATION_ARTIFACTS,
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
            "handoffOk": self.handoff_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["handoffId"] = self.handoff_id
        return payload


def build_operator_decision_handoff_package(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> OperatorDecisionHandoffPackage:
    return OperatorDecisionHandoffPackage(metadata={} if metadata is None else metadata)


def validate_operator_decision_handoff_package(package: OperatorDecisionHandoffPackage) -> tuple[str, ...]:
    return package.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "HANDOFF_KIND",
    "HANDOFF_SCOPE_ID",
    "NEXT_STAGE",
    "OperatorDecisionHandoffPackage",
    "build_operator_decision_handoff_package",
    "validate_operator_decision_handoff_package",
]
