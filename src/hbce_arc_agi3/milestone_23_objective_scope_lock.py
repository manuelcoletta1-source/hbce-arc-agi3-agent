"""Milestone #23 Task 2 - Objective Selection and Scope Lock.

Milestone 23 objective:
    Closed Milestone Snapshot Registry local-only.

Purpose:
    Turn the Fast Snapshot Dependency Guard from Milestone 22 into a reusable
    local-only registry pattern for closed milestone snapshots.

This task only selects and locks scope. It does not implement the registry yet.
Implementation begins in Task 3. Because apparently humans need a written
barrier between "choose the target" and "start drilling into the wall."
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_23_governed_opening import (
    build_milestone_23_governed_opening,
    validate_milestone_23_governed_opening,
)


TASK_ID = "MILESTONE_23_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
REVISION = "MILESTONE_23_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_v1"
MILESTONE_ID = "MILESTONE_23"
NEXT_STAGE = "MILESTONE_23_TASK_3_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_IMPLEMENTATION_V1"

SCOPE_LOCK_ID = "MILESTONE_23_SCOPE_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY"
SELECTED_OBJECTIVE_ID = "CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 2
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

OBJECTIVE_SELECTION_READY = True
OBJECTIVE_SELECTED = True
SCOPE_LOCKED = True
IMPLEMENTATION_ALLOWED_NEXT = True
IMPLEMENTATION_STARTED = False
REGISTRY_IMPLEMENTATION_STARTED = False

FAST_SNAPSHOT_DEPENDENCY_MODE_REQUIRED = True
DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_FORBIDDEN = True
DOCUMENT_MARKER_EVIDENCE_REQUIRED = True
STATIC_CLOSURE_SNAPSHOT_REQUIRED = True
CLOSED_MILESTONE_ARTIFACT_LOOKUP_REQUIRED = True
SOURCE_MILESTONE_22_CLOSURE_REQUIRED = True

NO_RECURSIVE_META_LAYER = True
CLOSURE_REQUIRED = True

MAX_REVIEW_DEPTH = 1
MAX_AUTHORIZATION_DEPTH = 1
MAX_FINALIZATION_DEPTH = 1

RUNTIME_SOLVER_MODIFIED = False
RUNTIME_WIRING_ALLOWED = False
KAGGLE_SUBMISSION_SENT = False
KAGGLE_AUTHENTICATION_ALLOWED = False
KAGGLE_UPLOAD_ALLOWED = False
RAW_REQUEST_BODY_PERSISTED = False
SECRET_PERSISTED = False
LEGAL_CERTIFICATION = False
HISTORICAL_MILESTONE_REWRITE = False
FAIL_CLOSED_ACTIVE = True


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


@dataclass(frozen=True)
class Milestone23ObjectiveCandidate:
    objective_id: str
    selected: bool
    rationale: str
    implementation_starts_at_task: int
    local_only: bool = True
    public_safe: bool = True
    deterministic: bool = True
    runtime_solver_modified: bool = False
    runtime_wiring_allowed: bool = False
    kaggle_submission_allowed: bool = False

    @property
    def valid(self) -> bool:
        return (
            bool(self.objective_id)
            and bool(self.rationale)
            and self.implementation_starts_at_task == 3
            and self.local_only is True
            and self.public_safe is True
            and self.deterministic is True
            and self.runtime_solver_modified is False
            and self.runtime_wiring_allowed is False
            and self.kaggle_submission_allowed is False
        )

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "objectiveId": self.objective_id,
            "selected": self.selected,
            "rationale": self.rationale,
            "implementationStartsAtTask": self.implementation_starts_at_task,
            "localOnly": self.local_only,
            "publicSafe": self.public_safe,
            "deterministic": self.deterministic,
            "runtimeSolverModified": self.runtime_solver_modified,
            "runtimeWiringAllowed": self.runtime_wiring_allowed,
            "kaggleSubmissionAllowed": self.kaggle_submission_allowed,
            "valid": self.valid,
        }


@dataclass(frozen=True)
class Milestone23ObjectiveScopeLock:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    scope_lock_id: str = SCOPE_LOCK_ID
    selected_objective_id: str = SELECTED_OBJECTIVE_ID
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    objective_candidates: tuple[Milestone23ObjectiveCandidate, ...] = (
        Milestone23ObjectiveCandidate(
            objective_id="CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY",
            selected=True,
            rationale=(
                "Implement a local-only registry of closed milestone snapshots so future "
                "milestones can resolve closure evidence without deep recursive traversal."
            ),
            implementation_starts_at_task=3,
        ),
        Milestone23ObjectiveCandidate(
            objective_id="RUNTIME_SOLVER_PATCH",
            selected=False,
            rationale="Rejected for this milestone because runtime solver modification is out of scope.",
            implementation_starts_at_task=3,
            runtime_solver_modified=True,
        ),
        Milestone23ObjectiveCandidate(
            objective_id="KAGGLE_SUBMISSION_PREPARATION",
            selected=False,
            rationale="Rejected because real submission and Kaggle paths remain blocked.",
            implementation_starts_at_task=3,
            kaggle_submission_allowed=True,
        ),
    )
    scope_constraints: tuple[str, ...] = (
        "local_only",
        "deterministic",
        "public_safe",
        "closed_milestone_snapshot_registry_only",
        "document_marker_evidence_required",
        "static_closure_snapshot_required",
        "fast_snapshot_dependency_mode_required",
        "deep_recursive_dependency_traversal_forbidden",
        "no_runtime_solver_modification",
        "no_runtime_wiring",
        "no_kaggle_submission",
        "ready_for_task_3_registry_implementation",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def lock_id(self) -> str:
        return f"MILESTONE-23-SCOPE-LOCK-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def selected_objective(self) -> Milestone23ObjectiveCandidate:
        selected = [candidate for candidate in self.objective_candidates if candidate.selected]
        if len(selected) != 1:
            raise ValueError("Expected exactly one selected objective candidate")
        return selected[0]

    @property
    def rejected_objective_count(self) -> int:
        return len([candidate for candidate in self.objective_candidates if not candidate.selected])

    @property
    def opening_payload(self) -> Mapping[str, Any]:
        return build_milestone_23_governed_opening().to_public_dict()

    @property
    def lock_ok(self) -> bool:
        opening = build_milestone_23_governed_opening()
        opening_payload = opening.to_public_dict()

        return (
            OBJECTIVE_SELECTION_READY is True
            and OBJECTIVE_SELECTED is True
            and SCOPE_LOCKED is True
            and IMPLEMENTATION_ALLOWED_NEXT is True
            and IMPLEMENTATION_STARTED is False
            and REGISTRY_IMPLEMENTATION_STARTED is False
            and opening.valid is True
            and validate_milestone_23_governed_opening(opening) == ()
            and opening_payload["valid"] is True
            and opening_payload["objectiveSelectionRequiredNext"] is True
            and opening_payload["scopeLockRequiredNext"] is True
            and opening_payload["implementationStarted"] is False
            and opening_payload["sourceMilestoneId"] == "MILESTONE_22"
            and opening_payload["sourceTask7Used"] is False
            and opening_payload["sourceTask8Used"] is False
            and self.scope_lock_id == SCOPE_LOCK_ID
            and self.selected_objective_id == SELECTED_OBJECTIVE_ID
            and self.selected_objective.objective_id == SELECTED_OBJECTIVE_ID
            and self.selected_objective.selected is True
            and self.selected_objective.valid is True
            and self.rejected_objective_count == 2
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 2
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.objective_candidates) == 3
            and len(self.scope_constraints) == 12
            and FAST_SNAPSHOT_DEPENDENCY_MODE_REQUIRED is True
            and DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_FORBIDDEN is True
            and DOCUMENT_MARKER_EVIDENCE_REQUIRED is True
            and STATIC_CLOSURE_SNAPSHOT_REQUIRED is True
            and CLOSED_MILESTONE_ARTIFACT_LOOKUP_REQUIRED is True
            and SOURCE_MILESTONE_22_CLOSURE_REQUIRED is True
            and NO_RECURSIVE_META_LAYER is True
            and CLOSURE_REQUIRED is True
            and MAX_REVIEW_DEPTH == 1
            and MAX_AUTHORIZATION_DEPTH == 1
            and MAX_FINALIZATION_DEPTH == 1
            and RUNTIME_SOLVER_MODIFIED is False
            and RUNTIME_WIRING_ALLOWED is False
            and KAGGLE_SUBMISSION_SENT is False
            and KAGGLE_AUTHENTICATION_ALLOWED is False
            and KAGGLE_UPLOAD_ALLOWED is False
            and RAW_REQUEST_BODY_PERSISTED is False
            and SECRET_PERSISTED is False
            and LEGAL_CERTIFICATION is False
            and HISTORICAL_MILESTONE_REWRITE is False
            and FAIL_CLOSED_ACTIVE is True
        )

    @property
    def issues(self) -> tuple[str, ...]:
        issues: list[str] = []

        opening = build_milestone_23_governed_opening()
        if not opening.valid:
            issues.append("MILESTONE_23_GOVERNED_OPENING_INVALID")
        issues.extend(f"MILESTONE_23_GOVERNED_OPENING_{issue}" for issue in validate_milestone_23_governed_opening(opening))

        if not OBJECTIVE_SELECTION_READY:
            issues.append("OBJECTIVE_SELECTION_NOT_READY")
        if not OBJECTIVE_SELECTED:
            issues.append("OBJECTIVE_NOT_SELECTED")
        if not SCOPE_LOCKED:
            issues.append("SCOPE_NOT_LOCKED")
        if not IMPLEMENTATION_ALLOWED_NEXT:
            issues.append("IMPLEMENTATION_NOT_ALLOWED_NEXT")
        if IMPLEMENTATION_STARTED:
            issues.append("IMPLEMENTATION_STARTED_AT_TASK_2")
        if REGISTRY_IMPLEMENTATION_STARTED:
            issues.append("REGISTRY_IMPLEMENTATION_STARTED_AT_TASK_2")
        if self.scope_lock_id != SCOPE_LOCK_ID:
            issues.append("SCOPE_LOCK_ID_MISMATCH")
        if self.selected_objective_id != SELECTED_OBJECTIVE_ID:
            issues.append("SELECTED_OBJECTIVE_ID_MISMATCH")
        if self.selected_objective.objective_id != SELECTED_OBJECTIVE_ID:
            issues.append("SELECTED_OBJECTIVE_MISMATCH")
        if self.rejected_objective_count != 2:
            issues.append("REJECTED_OBJECTIVE_COUNT_NOT_2")
        if self.task_budget_min != 4:
            issues.append("TASK_BUDGET_MIN_NOT_4")
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
        if len(self.objective_candidates) != 3:
            issues.append("OBJECTIVE_CANDIDATE_COUNT_NOT_3")
        if len(self.scope_constraints) != 12:
            issues.append("SCOPE_CONSTRAINT_COUNT_NOT_12")
        if not FAST_SNAPSHOT_DEPENDENCY_MODE_REQUIRED:
            issues.append("FAST_SNAPSHOT_DEPENDENCY_MODE_NOT_REQUIRED")
        if not DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_FORBIDDEN:
            issues.append("DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_NOT_FORBIDDEN")
        if not DOCUMENT_MARKER_EVIDENCE_REQUIRED:
            issues.append("DOCUMENT_MARKER_EVIDENCE_NOT_REQUIRED")
        if not STATIC_CLOSURE_SNAPSHOT_REQUIRED:
            issues.append("STATIC_CLOSURE_SNAPSHOT_NOT_REQUIRED")
        if not CLOSED_MILESTONE_ARTIFACT_LOOKUP_REQUIRED:
            issues.append("CLOSED_MILESTONE_ARTIFACT_LOOKUP_NOT_REQUIRED")
        if not SOURCE_MILESTONE_22_CLOSURE_REQUIRED:
            issues.append("SOURCE_MILESTONE_22_CLOSURE_NOT_REQUIRED")
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
        if RUNTIME_SOLVER_MODIFIED:
            issues.append("RUNTIME_SOLVER_MODIFIED")
        if RUNTIME_WIRING_ALLOWED:
            issues.append("RUNTIME_WIRING_ALLOWED")
        if KAGGLE_SUBMISSION_SENT:
            issues.append("KAGGLE_SUBMISSION_SENT")
        if KAGGLE_AUTHENTICATION_ALLOWED:
            issues.append("KAGGLE_AUTHENTICATION_ALLOWED")
        if KAGGLE_UPLOAD_ALLOWED:
            issues.append("KAGGLE_UPLOAD_ALLOWED")
        if RAW_REQUEST_BODY_PERSISTED:
            issues.append("RAW_REQUEST_BODY_PERSISTED")
        if SECRET_PERSISTED:
            issues.append("SECRET_PERSISTED")
        if LEGAL_CERTIFICATION:
            issues.append("LEGAL_CERTIFICATION")
        if HISTORICAL_MILESTONE_REWRITE:
            issues.append("HISTORICAL_MILESTONE_REWRITE")
        if not FAIL_CLOSED_ACTIVE:
            issues.append("FAIL_CLOSED_INACTIVE")

        return tuple(issues)

    @property
    def valid(self) -> bool:
        return self.lock_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        opening_payload = self.opening_payload

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceOpeningId": opening_payload["openingId"],
            "sourceOpeningValid": opening_payload["valid"],
            "sourceMilestoneId": opening_payload["sourceMilestoneId"],
            "sourceFinalStatus": opening_payload["sourceFinalStatus"],
            "sourceFinalTaskNumber": opening_payload["sourceFinalTaskNumber"],
            "sourceTask7Used": opening_payload["sourceTask7Used"],
            "sourceTask8Used": opening_payload["sourceTask8Used"],
            "nextStage": self.next_stage,
            "scopeLockId": self.scope_lock_id,
            "selectedObjectiveId": self.selected_objective_id,
            "selectedObjective": self.selected_objective.to_public_dict(),
            "objectiveCandidates": [candidate.to_public_dict() for candidate in self.objective_candidates],
            "objectiveCandidateCount": len(self.objective_candidates),
            "rejectedObjectiveCount": self.rejected_objective_count,
            "scopeConstraints": list(self.scope_constraints),
            "scopeConstraintCount": len(self.scope_constraints),
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.task_budget_max - self.current_task_number,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "objectiveSelectionReady": OBJECTIVE_SELECTION_READY,
            "objectiveSelected": OBJECTIVE_SELECTED,
            "scopeLocked": SCOPE_LOCKED,
            "implementationAllowedNext": IMPLEMENTATION_ALLOWED_NEXT,
            "implementationStarted": IMPLEMENTATION_STARTED,
            "registryImplementationStarted": REGISTRY_IMPLEMENTATION_STARTED,
            "fastSnapshotDependencyModeRequired": FAST_SNAPSHOT_DEPENDENCY_MODE_REQUIRED,
            "deepRecursiveDependencyTraversalForbidden": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_FORBIDDEN,
            "documentMarkerEvidenceRequired": DOCUMENT_MARKER_EVIDENCE_REQUIRED,
            "staticClosureSnapshotRequired": STATIC_CLOSURE_SNAPSHOT_REQUIRED,
            "closedMilestoneArtifactLookupRequired": CLOSED_MILESTONE_ARTIFACT_LOOKUP_REQUIRED,
            "sourceMilestone22ClosureRequired": SOURCE_MILESTONE_22_CLOSURE_REQUIRED,
            "noRecursiveMetaLayer": NO_RECURSIVE_META_LAYER,
            "closureRequired": CLOSURE_REQUIRED,
            "maxReviewDepth": MAX_REVIEW_DEPTH,
            "maxAuthorizationDepth": MAX_AUTHORIZATION_DEPTH,
            "maxFinalizationDepth": MAX_FINALIZATION_DEPTH,
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
            "kaggleAuthenticationAllowed": KAGGLE_AUTHENTICATION_ALLOWED,
            "kaggleUploadAllowed": KAGGLE_UPLOAD_ALLOWED,
            "rawRequestBodyPersisted": RAW_REQUEST_BODY_PERSISTED,
            "secretPersisted": SECRET_PERSISTED,
            "legalCertification": LEGAL_CERTIFICATION,
            "historicalMilestoneRewrite": HISTORICAL_MILESTONE_REWRITE,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
            "lockOk": self.lock_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["lockId"] = self.lock_id
        return payload


def build_milestone_23_objective_scope_lock(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone23ObjectiveScopeLock:
    return Milestone23ObjectiveScopeLock(metadata={} if metadata is None else metadata)


def validate_milestone_23_objective_scope_lock(
    scope_lock: Milestone23ObjectiveScopeLock,
) -> tuple[str, ...]:
    return scope_lock.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "SCOPE_LOCK_ID",
    "SELECTED_OBJECTIVE_ID",
    "OBJECTIVE_SELECTION_READY",
    "SCOPE_LOCKED",
    "Milestone23ObjectiveCandidate",
    "Milestone23ObjectiveScopeLock",
    "build_milestone_23_objective_scope_lock",
    "validate_milestone_23_objective_scope_lock",
]
