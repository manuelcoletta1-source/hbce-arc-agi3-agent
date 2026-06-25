"""Milestone #22 Task 2 - Objective Selection and Scope Lock.

This task selects and locks the Milestone 22 objective.

Selected scope: local-only fast snapshot dependency guard.
Purpose: prevent deep recursive to_public_dict()/validity traversal across
closed milestone chains while preserving document-based dependency evidence.

Translation for the tired mammal reading this: stop making every object call
every ancestor object until the repo starts reenacting genealogy as infrastructure.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_22_governed_opening import (
    build_milestone_22_governed_opening,
    validate_milestone_22_governed_opening,
)


TASK_ID = "MILESTONE_22_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
REVISION = "MILESTONE_22_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_v1"
MILESTONE_ID = "MILESTONE_22"
NEXT_STAGE = "MILESTONE_22_TASK_3_FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTATION_V1"

SCOPE_LOCK_ID = "MILESTONE_22_SCOPE_FAST_SNAPSHOT_DEPENDENCY_GUARD_LOCAL_ONLY"

SELECTED_OBJECTIVE = (
    "Create a local-only fast snapshot dependency guard for future milestone openings "
    "that prevents deep recursive to_public_dict()/validity traversal across closed "
    "milestone chains while preserving document-based dependency evidence."
)

SCOPE_BOUNDARY = (
    "Task 3 may implement a local-only helper/contract for fast snapshot dependency "
    "guarding. It must not modify runtime solver behavior, runtime wiring, Kaggle "
    "submission paths, authentication, upload logic, or historical milestone closure "
    "semantics."
)

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 2
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

OBJECTIVE_SELECTION_READY = True
SCOPE_LOCK_READY = True
SCOPE_LOCKED = True
IMPLEMENTATION_ALLOWED_NEXT = True
IMPLEMENTATION_STARTED = False

FAST_SNAPSHOT_PATTERN_REQUIRED = True
DEEP_RECURSIVE_SERIALIZATION_FORBIDDEN = True
DOCUMENT_BASED_DEPENDENCY_EVIDENCE_REQUIRED = True
CLOSED_MILESTONE_REVALIDATION_AS_RUNTIME_TRAVERSAL_FORBIDDEN = True

NO_RECURSIVE_META_LAYER = True
CLOSURE_REQUIRED = True

MAX_REVIEW_DEPTH = 1
MAX_AUTHORIZATION_DEPTH = 1
MAX_FINALIZATION_DEPTH = 1

MILESTONE_21_REOPEN_REQUIRED = False
MILESTONE_21_TASK_7_REQUIRED = False
MILESTONE_21_TASK_8_REQUIRED = False
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
class Milestone22ObjectiveScopeLock:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    scope_lock_id: str = SCOPE_LOCK_ID
    selected_objective: str = SELECTED_OBJECTIVE
    scope_boundary: str = SCOPE_BOUNDARY
    next_stage: str = NEXT_STAGE
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    allowed_implementation_targets: tuple[str, ...] = (
        "src/hbce_arc_agi3/milestone_22_fast_snapshot_dependency_guard.py",
        "tests/test_milestone_22_fast_snapshot_dependency_guard.py",
        "docs/milestone-22-task-3-fast-snapshot-dependency-guard-implementation-v1.md",
        "examples/milestone-22/fast-snapshot-dependency-guard-implementation-v1/",
    )
    forbidden_targets: tuple[str, ...] = (
        "runtime_solver_patch",
        "runtime_wiring_activation",
        "kaggle_authentication",
        "kaggle_upload",
        "kaggle_submission",
        "raw_request_body_persistence",
        "secret_persistence",
        "historical_milestone_rewrite",
        "legal_certification_claim",
        "recursive_meta_layer",
    )
    scope_checks: tuple[str, ...] = (
        "task_1_governed_opening_valid",
        "objective_selected",
        "scope_lock_declared",
        "task_budget_preserved",
        "fast_snapshot_required",
        "deep_recursive_serialization_forbidden",
        "document_dependency_evidence_required",
        "implementation_allowed_next",
        "forbidden_targets_absent",
        "fail_closed_boundary_preserved",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def lock_record_id(self) -> str:
        return f"MILESTONE-22-SCOPE-LOCK-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def remaining_budget_after_current_task(self) -> int:
        return self.task_budget_max - self.current_task_number

    @property
    def opening_payload(self) -> Mapping[str, Any]:
        return build_milestone_22_governed_opening().to_public_dict()

    @property
    def scope_lock_ok(self) -> bool:
        opening = build_milestone_22_governed_opening()
        opening_payload = opening.to_public_dict()

        return (
            OBJECTIVE_SELECTION_READY is True
            and SCOPE_LOCK_READY is True
            and SCOPE_LOCKED is True
            and IMPLEMENTATION_ALLOWED_NEXT is True
            and IMPLEMENTATION_STARTED is False
            and opening.valid is True
            and validate_milestone_22_governed_opening(opening) == ()
            and opening_payload["objectiveSelectionRequiredNext"] is True
            and opening_payload["scopeLockRequiredNext"] is True
            and opening_payload["implementationStarted"] is False
            and opening_payload["taskBudgetMax"] == 8
            and self.task_budget_max == 8
            and self.current_task_number == 2
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and self.scope_lock_id == SCOPE_LOCK_ID
            and len(self.allowed_implementation_targets) == 4
            and len(self.forbidden_targets) == 10
            and len(self.scope_checks) == 10
            and FAST_SNAPSHOT_PATTERN_REQUIRED is True
            and DEEP_RECURSIVE_SERIALIZATION_FORBIDDEN is True
            and DOCUMENT_BASED_DEPENDENCY_EVIDENCE_REQUIRED is True
            and CLOSED_MILESTONE_REVALIDATION_AS_RUNTIME_TRAVERSAL_FORBIDDEN is True
            and NO_RECURSIVE_META_LAYER is True
            and CLOSURE_REQUIRED is True
            and MAX_REVIEW_DEPTH == 1
            and MAX_AUTHORIZATION_DEPTH == 1
            and MAX_FINALIZATION_DEPTH == 1
            and MILESTONE_21_REOPEN_REQUIRED is False
            and MILESTONE_21_TASK_7_REQUIRED is False
            and MILESTONE_21_TASK_8_REQUIRED is False
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

        opening = build_milestone_22_governed_opening()
        if not opening.valid:
            issues.append("MILESTONE_22_OPENING_INVALID")
        issues.extend(f"MILESTONE_22_OPENING_{issue}" for issue in validate_milestone_22_governed_opening(opening))

        if not OBJECTIVE_SELECTION_READY:
            issues.append("OBJECTIVE_SELECTION_NOT_READY")
        if not SCOPE_LOCK_READY:
            issues.append("SCOPE_LOCK_NOT_READY")
        if not SCOPE_LOCKED:
            issues.append("SCOPE_NOT_LOCKED")
        if not IMPLEMENTATION_ALLOWED_NEXT:
            issues.append("IMPLEMENTATION_NOT_ALLOWED_NEXT")
        if IMPLEMENTATION_STARTED:
            issues.append("IMPLEMENTATION_STARTED_TOO_EARLY")
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
        if self.scope_lock_id != SCOPE_LOCK_ID:
            issues.append("SCOPE_LOCK_ID_MISMATCH")
        if len(self.allowed_implementation_targets) != 4:
            issues.append("ALLOWED_IMPLEMENTATION_TARGET_COUNT_NOT_4")
        if len(self.forbidden_targets) != 10:
            issues.append("FORBIDDEN_TARGET_COUNT_NOT_10")
        if len(self.scope_checks) != 10:
            issues.append("SCOPE_CHECK_COUNT_NOT_10")
        if not FAST_SNAPSHOT_PATTERN_REQUIRED:
            issues.append("FAST_SNAPSHOT_PATTERN_NOT_REQUIRED")
        if not DEEP_RECURSIVE_SERIALIZATION_FORBIDDEN:
            issues.append("DEEP_RECURSIVE_SERIALIZATION_NOT_FORBIDDEN")
        if not DOCUMENT_BASED_DEPENDENCY_EVIDENCE_REQUIRED:
            issues.append("DOCUMENT_DEPENDENCY_EVIDENCE_NOT_REQUIRED")
        if not CLOSED_MILESTONE_REVALIDATION_AS_RUNTIME_TRAVERSAL_FORBIDDEN:
            issues.append("CLOSED_MILESTONE_RUNTIME_TRAVERSAL_NOT_FORBIDDEN")
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
        opening = self.opening_payload

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "scopeLockId": self.scope_lock_id,
            "selectedObjective": self.selected_objective,
            "scopeBoundary": self.scope_boundary,
            "nextStage": self.next_stage,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "sourceOpeningId": opening["openingId"],
            "sourceOpeningRevision": opening["revision"],
            "sourceOpeningValid": opening["valid"],
            "sourceOpeningTaskBudgetMax": opening["taskBudgetMax"],
            "sourceOpeningCurrentTaskNumber": opening["currentTaskNumber"],
            "allowedImplementationTargets": list(self.allowed_implementation_targets),
            "allowedImplementationTargetCount": len(self.allowed_implementation_targets),
            "forbiddenTargets": list(self.forbidden_targets),
            "forbiddenTargetCount": len(self.forbidden_targets),
            "scopeChecks": list(self.scope_checks),
            "scopeCheckCount": len(self.scope_checks),
            "objectiveSelectionReady": OBJECTIVE_SELECTION_READY,
            "scopeLockReady": SCOPE_LOCK_READY,
            "scopeLocked": SCOPE_LOCKED,
            "implementationAllowedNext": IMPLEMENTATION_ALLOWED_NEXT,
            "implementationStarted": IMPLEMENTATION_STARTED,
            "fastSnapshotPatternRequired": FAST_SNAPSHOT_PATTERN_REQUIRED,
            "deepRecursiveSerializationForbidden": DEEP_RECURSIVE_SERIALIZATION_FORBIDDEN,
            "documentBasedDependencyEvidenceRequired": DOCUMENT_BASED_DEPENDENCY_EVIDENCE_REQUIRED,
            "closedMilestoneRevalidationAsRuntimeTraversalForbidden": CLOSED_MILESTONE_REVALIDATION_AS_RUNTIME_TRAVERSAL_FORBIDDEN,
            "noRecursiveMetaLayer": NO_RECURSIVE_META_LAYER,
            "closureRequired": CLOSURE_REQUIRED,
            "maxReviewDepth": MAX_REVIEW_DEPTH,
            "maxAuthorizationDepth": MAX_AUTHORIZATION_DEPTH,
            "maxFinalizationDepth": MAX_FINALIZATION_DEPTH,
            "milestone21ReopenRequired": MILESTONE_21_REOPEN_REQUIRED,
            "milestone21Task7Required": MILESTONE_21_TASK_7_REQUIRED,
            "milestone21Task8Required": MILESTONE_21_TASK_8_REQUIRED,
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


def build_milestone_22_objective_scope_lock(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone22ObjectiveScopeLock:
    return Milestone22ObjectiveScopeLock(metadata={} if metadata is None else metadata)


def validate_milestone_22_objective_scope_lock(
    scope_lock: Milestone22ObjectiveScopeLock,
) -> tuple[str, ...]:
    return scope_lock.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "SCOPE_LOCK_ID",
    "OBJECTIVE_SELECTION_READY",
    "SCOPE_LOCK_READY",
    "SCOPE_LOCKED",
    "Milestone22ObjectiveScopeLock",
    "build_milestone_22_objective_scope_lock",
    "validate_milestone_22_objective_scope_lock",
]
