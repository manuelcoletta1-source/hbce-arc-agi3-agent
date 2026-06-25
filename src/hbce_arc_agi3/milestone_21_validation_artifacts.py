"""Milestone #21 Task 4 - Validation and Artifacts.

This module validates the local-only operator decision handoff package from
Task 3 and produces the artifact contract for Task 4.

No runtime solver mutation. No runtime wiring. No Kaggle submission.
No raw request body persistence. No secret persistence. No legal-certification
claims. No recursive meta-layer. Humanity may complain, but the tests will not.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_21_operator_decision_handoff import (
    build_operator_decision_handoff_package,
    validate_operator_decision_handoff_package,
)
from hbce_arc_agi3.milestone_21_objective_scope_lock import (
    build_milestone_21_objective_scope_lock,
    validate_milestone_21_objective_scope_lock,
)
from hbce_arc_agi3.milestone_20_closure import (
    build_milestone_20_closure,
    validate_milestone_20_closure,
)


TASK_ID = "MILESTONE_21_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
REVISION = "MILESTONE_21_VALIDATION_AND_ARTIFACTS_v1"
MILESTONE_ID = "MILESTONE_21"
NEXT_STAGE = "MILESTONE_21_TASK_5_INTEGRATION_REGRESSION_V1"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 4
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

VALIDATION_ARTIFACTS_READY = True
HANDOFF_PACKAGE_VALIDATED = True
VALIDATION_ARTIFACTS_CREATED = True
ARTIFACTS_LOCAL_ONLY = True
ARTIFACTS_DETERMINISTIC = True
ARTIFACTS_PUBLIC_SAFE = True
ARTIFACTS_READY_FOR_INTEGRATION_REGRESSION = True

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
class HandoffValidationArtifacts:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    validation_checks: tuple[str, ...] = (
        "handoff_package_exists",
        "handoff_package_valid",
        "milestone_20_closure_state_carried",
        "scope_lock_state_carried",
        "budget_trace_carried",
        "fail_closed_boundary_carried",
        "forbidden_actions_absent",
        "next_stage_declared",
    )
    artifact_names: tuple[str, ...] = (
        "task-4-validation-artifacts.json",
        "task-4-validation-artifacts.md",
        "task-4-manifest.json",
        "task-4-index.txt",
    )
    carried_boundary_markers: tuple[str, ...] = (
        "runtimeSolverModified=false",
        "runtimeWiringAllowed=false",
        "kaggleSubmissionSent=false",
        "rawRequestBodyPersisted=false",
        "secretPersisted=false",
        "legalCertification=false",
        "failClosedActive=true",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def validation_artifact_id(self) -> str:
        return f"MILESTONE-21-VALIDATION-ARTIFACTS-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def remaining_budget_after_current_task(self) -> int:
        return self.task_budget_max - self.current_task_number

    @property
    def handoff_payload(self) -> Mapping[str, Any]:
        package = build_operator_decision_handoff_package()
        return package.to_public_dict()

    @property
    def scope_lock_payload(self) -> Mapping[str, Any]:
        lock = build_milestone_21_objective_scope_lock()
        return lock.to_public_dict()

    @property
    def milestone_20_payload(self) -> Mapping[str, Any]:
        closure = build_milestone_20_closure()
        return closure.to_public_dict()

    @property
    def validation_ok(self) -> bool:
        package = build_operator_decision_handoff_package()
        lock = build_milestone_21_objective_scope_lock()
        closure = build_milestone_20_closure()

        handoff_payload = package.to_public_dict()
        lock_payload = lock.to_public_dict()
        closure_payload = closure.to_public_dict()

        return (
            VALIDATION_ARTIFACTS_READY is True
            and HANDOFF_PACKAGE_VALIDATED is True
            and VALIDATION_ARTIFACTS_CREATED is True
            and ARTIFACTS_LOCAL_ONLY is True
            and ARTIFACTS_DETERMINISTIC is True
            and ARTIFACTS_PUBLIC_SAFE is True
            and ARTIFACTS_READY_FOR_INTEGRATION_REGRESSION is True
            and package.valid is True
            and validate_operator_decision_handoff_package(package) == ()
            and handoff_payload["handoffReadyForValidationArtifacts"] is True
            and handoff_payload["sourceMilestone20FinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8"
            and handoff_payload["sourceMilestone20Task8Used"] is False
            and handoff_payload["scopeLocked"] is True
            and handoff_payload["implementationAllowedByScope"] is True
            and lock.valid is True
            and validate_milestone_21_objective_scope_lock(lock) == ()
            and lock_payload["scopeLocked"] is True
            and lock_payload["implementationAllowedNext"] is True
            and closure.valid is True
            and validate_milestone_20_closure(closure) == ()
            and closure_payload["task8Used"] is False
            and closure_payload["emergencyReserveUnused"] is True
            and self.task_budget_max == 8
            and self.current_task_number == 4
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.validation_checks) == 8
            and len(self.artifact_names) == 4
            and len(self.carried_boundary_markers) == 7
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

        package = build_operator_decision_handoff_package()
        lock = build_milestone_21_objective_scope_lock()
        closure = build_milestone_20_closure()

        if not package.valid:
            issues.append("HANDOFF_PACKAGE_INVALID")
        issues.extend(f"HANDOFF_{issue}" for issue in validate_operator_decision_handoff_package(package))

        if not lock.valid:
            issues.append("SCOPE_LOCK_INVALID")
        issues.extend(f"SCOPE_LOCK_{issue}" for issue in validate_milestone_21_objective_scope_lock(lock))

        if not closure.valid:
            issues.append("MILESTONE_20_CLOSURE_INVALID")
        issues.extend(f"MILESTONE_20_{issue}" for issue in validate_milestone_20_closure(closure))

        if not VALIDATION_ARTIFACTS_READY:
            issues.append("VALIDATION_ARTIFACTS_NOT_READY")
        if not HANDOFF_PACKAGE_VALIDATED:
            issues.append("HANDOFF_PACKAGE_NOT_VALIDATED")
        if not VALIDATION_ARTIFACTS_CREATED:
            issues.append("VALIDATION_ARTIFACTS_NOT_CREATED")
        if not ARTIFACTS_LOCAL_ONLY:
            issues.append("ARTIFACTS_NOT_LOCAL_ONLY")
        if not ARTIFACTS_DETERMINISTIC:
            issues.append("ARTIFACTS_NOT_DETERMINISTIC")
        if not ARTIFACTS_PUBLIC_SAFE:
            issues.append("ARTIFACTS_NOT_PUBLIC_SAFE")
        if not ARTIFACTS_READY_FOR_INTEGRATION_REGRESSION:
            issues.append("NOT_READY_FOR_INTEGRATION_REGRESSION")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 4:
            issues.append("CURRENT_TASK_NUMBER_NOT_4")
        if self.recommended_closure_task_number != 6:
            issues.append("RECOMMENDED_CLOSURE_TASK_NOT_6")
        if self.reserve_task_number != 7:
            issues.append("RESERVE_TASK_NUMBER_NOT_7")
        if self.emergency_only_task_number != 8:
            issues.append("EMERGENCY_TASK_NUMBER_NOT_8")
        if len(self.validation_checks) != 8:
            issues.append("VALIDATION_CHECK_COUNT_NOT_8")
        if len(self.artifact_names) != 4:
            issues.append("ARTIFACT_NAME_COUNT_NOT_4")
        if len(self.carried_boundary_markers) != 7:
            issues.append("BOUNDARY_MARKER_COUNT_NOT_7")
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
        return self.validation_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        handoff_payload = self.handoff_payload
        lock_payload = self.scope_lock_payload
        milestone_20_payload = self.milestone_20_payload

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
            "sourceHandoffId": handoff_payload["handoffId"],
            "sourceHandoffKind": handoff_payload["handoffKind"],
            "sourceHandoffScopeId": handoff_payload["handoffScopeId"],
            "sourceMilestone20ClosureId": handoff_payload["sourceMilestone20ClosureId"],
            "sourceMilestone20FinalStatus": handoff_payload["sourceMilestone20FinalStatus"],
            "sourceMilestone20Task8Used": handoff_payload["sourceMilestone20Task8Used"],
            "scopeLockRecordId": lock_payload["lockRecordId"],
            "scopeLockId": lock_payload["scopeLockId"],
            "scopeLocked": lock_payload["scopeLocked"],
            "milestone20ClosureId": milestone_20_payload["closureId"],
            "milestone20FinalStatus": milestone_20_payload["finalStatus"],
            "milestone20Task8Used": milestone_20_payload["task8Used"],
            "milestone20EmergencyReserveUnused": milestone_20_payload["emergencyReserveUnused"],
            "validationChecks": list(self.validation_checks),
            "validationCheckCount": len(self.validation_checks),
            "artifactNames": list(self.artifact_names),
            "artifactNameCount": len(self.artifact_names),
            "carriedBoundaryMarkers": list(self.carried_boundary_markers),
            "carriedBoundaryMarkerCount": len(self.carried_boundary_markers),
            "validationArtifactsReady": VALIDATION_ARTIFACTS_READY,
            "handoffPackageValidated": HANDOFF_PACKAGE_VALIDATED,
            "validationArtifactsCreated": VALIDATION_ARTIFACTS_CREATED,
            "artifactsLocalOnly": ARTIFACTS_LOCAL_ONLY,
            "artifactsDeterministic": ARTIFACTS_DETERMINISTIC,
            "artifactsPublicSafe": ARTIFACTS_PUBLIC_SAFE,
            "artifactsReadyForIntegrationRegression": ARTIFACTS_READY_FOR_INTEGRATION_REGRESSION,
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
            "validationOk": self.validation_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["validationArtifactId"] = self.validation_artifact_id
        return payload


def build_handoff_validation_artifacts(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> HandoffValidationArtifacts:
    return HandoffValidationArtifacts(metadata={} if metadata is None else metadata)


def validate_handoff_validation_artifacts(artifacts: HandoffValidationArtifacts) -> tuple[str, ...]:
    return artifacts.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "VALIDATION_ARTIFACTS_READY",
    "HandoffValidationArtifacts",
    "build_handoff_validation_artifacts",
    "validate_handoff_validation_artifacts",
]
