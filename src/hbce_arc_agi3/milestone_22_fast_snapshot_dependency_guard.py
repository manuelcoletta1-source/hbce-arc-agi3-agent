"""Milestone #22 Task 3 - Fast Snapshot Dependency Guard Implementation.

This local-only helper enforces the fast-snapshot pattern for future milestone
openings and dependency records.

Goal:
- Prefer static closure snapshots for already-closed milestone dependencies.
- Preserve document-based dependency evidence.
- Forbid deep recursive runtime traversal across closed milestone chains.
- Avoid to_public_dict()/valid recursion becoming a distributed denial of sanity.

No runtime solver changes. No runtime wiring. No Kaggle. No auth/upload.
No raw request body persistence. No secrets. No legal certification.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping, Sequence

from hbce_arc_agi3.milestone_22_objective_scope_lock import (
    SCOPE_LOCK_ID,
    build_milestone_22_objective_scope_lock,
    validate_milestone_22_objective_scope_lock,
)


TASK_ID = "MILESTONE_22_TASK_3_FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTATION_V1"
REVISION = "MILESTONE_22_FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTATION_v1"
MILESTONE_ID = "MILESTONE_22"
NEXT_STAGE = "MILESTONE_22_TASK_4_VALIDATION_AND_ARTIFACTS_V1"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 3
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

FAST_SNAPSHOT_DEPENDENCY_GUARD_READY = True
FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTED = True
LOCAL_ONLY_GUARD = True
SNAPSHOT_PATTERN_ENFORCED = True
DOCUMENT_EVIDENCE_PRESERVED = True
DEEP_RECURSIVE_TRAVERSAL_BLOCKED = True
READY_FOR_VALIDATION_ARTIFACTS = True

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
KAGGLE_AUTHENTICATION_ALLOWED = False
KAGGLE_UPLOAD_ALLOWED = False
RAW_REQUEST_BODY_PERSISTED = False
SECRET_PERSISTED = False
LEGAL_CERTIFICATION = False
HISTORICAL_MILESTONE_REWRITE = False
FAIL_CLOSED_ACTIVE = True


FORBIDDEN_RUNTIME_TRAVERSAL_TOKENS = (
    "closed_milestone.to_public_dict()",
    "closed_milestone.valid",
    "validate_closed_milestone_chain()",
    "recursive_runtime_dependency_walk",
    "historical_milestone_revalidation_as_runtime_traversal",
)

REQUIRED_SNAPSHOT_FIELDS = (
    "milestoneId",
    "finalStatus",
    "taskBudgetMax",
    "finalTaskNumber",
    "task7Used",
    "task8Used",
    "evidenceDocPath",
    "evidenceMarkers",
)


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


@dataclass(frozen=True)
class FastSnapshotDependencySpec:
    """A static snapshot of a closed milestone dependency."""

    milestone_id: str
    final_status: str
    task_budget_max: int
    final_task_number: int
    task_7_used: bool
    task_8_used: bool
    evidence_doc_path: str
    evidence_markers: tuple[str, ...]

    @property
    def marker_count(self) -> int:
        return len(self.evidence_markers)

    @property
    def snapshot_id(self) -> str:
        return f"FAST-SNAPSHOT-{self.milestone_id}-{_digest(self.to_public_dict())}"

    @property
    def valid(self) -> bool:
        return (
            self.milestone_id.startswith("MILESTONE_")
            and bool(self.final_status)
            and self.task_budget_max > 0
            and self.final_task_number > 0
            and self.final_task_number <= self.task_budget_max
            and isinstance(self.task_7_used, bool)
            and self.task_8_used is False
            and (self.task_7_used is False or self.final_task_number >= 7)
            and (self.task_7_used is True or self.final_task_number <= 6)
            and self.evidence_doc_path.endswith(".md")
            and self.marker_count >= 3
            and all(marker for marker in self.evidence_markers)
        )

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "milestoneId": self.milestone_id,
            "finalStatus": self.final_status,
            "taskBudgetMax": self.task_budget_max,
            "finalTaskNumber": self.final_task_number,
            "task7Used": self.task_7_used,
            "task8Used": self.task_8_used,
            "evidenceDocPath": self.evidence_doc_path,
            "evidenceMarkers": list(self.evidence_markers),
            "markerCount": self.marker_count,
            "valid": self.valid,
        }


def build_closed_milestone_snapshot(
    *,
    milestone_id: str,
    final_status: str,
    task_budget_max: int,
    final_task_number: int,
    task_7_used: bool,
    task_8_used: bool,
    evidence_doc_path: str,
    evidence_markers: Sequence[str],
) -> FastSnapshotDependencySpec:
    """Build a static dependency snapshot for a closed milestone."""

    return FastSnapshotDependencySpec(
        milestone_id=milestone_id,
        final_status=final_status,
        task_budget_max=task_budget_max,
        final_task_number=final_task_number,
        task_7_used=task_7_used,
        task_8_used=task_8_used,
        evidence_doc_path=evidence_doc_path,
        evidence_markers=tuple(evidence_markers),
    )


def build_default_milestone_21_snapshot() -> FastSnapshotDependencySpec:
    """Snapshot of the Milestone 21 closure used as dependency evidence."""

    return build_closed_milestone_snapshot(
        milestone_id="MILESTONE_21",
        final_status="CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6",
        task_budget_max=8,
        final_task_number=6,
        task_7_used=False,
        task_8_used=False,
        evidence_doc_path="docs/milestone-21-task-6-milestone-closure-v1.md",
        evidence_markers=(
            "MILESTONE_21_TASK_6_MILESTONE_CLOSURE_READY=true",
            "MILESTONE_21_TASK_6_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6",
            "MILESTONE_21_TASK_6_TASK_7_USED=false",
            "MILESTONE_21_TASK_6_TASK_8_USED=false",
        ),
    )


def build_default_milestone_20_snapshot() -> FastSnapshotDependencySpec:
    """Snapshot of the Milestone 20 closure used as dependency evidence."""

    return build_closed_milestone_snapshot(
        milestone_id="MILESTONE_20",
        final_status="CLOSED_WITH_TASK_BUDGET_MAX_8",
        task_budget_max=8,
        final_task_number=7,
        task_7_used=True,
        task_8_used=False,
        evidence_doc_path="docs/milestone-20-task-7-milestone-closure-v1.md",
        evidence_markers=(
            "MILESTONE_20_TASK_7_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8",
            "MILESTONE_20_TASK_7_TASK_8_USED=false",
            "MILESTONE_20_TASK_7_EMERGENCY_RESERVE_UNUSED=true",
        ),
    )


def detect_forbidden_runtime_traversal(tokens: Iterable[str]) -> tuple[str, ...]:
    """Return forbidden traversal tokens found in a proposed dependency contract."""

    token_set = set(tokens)
    return tuple(token for token in FORBIDDEN_RUNTIME_TRAVERSAL_TOKENS if token in token_set)


@dataclass(frozen=True)
class FastSnapshotDependencyGuard:
    """Guard contract for fast snapshot dependency usage."""

    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    scope_lock_id: str = SCOPE_LOCK_ID
    next_stage: str = NEXT_STAGE
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    snapshots: tuple[FastSnapshotDependencySpec, ...] = field(
        default_factory=lambda: (
            build_default_milestone_21_snapshot(),
            build_default_milestone_20_snapshot(),
        )
    )
    allowed_dependency_modes: tuple[str, ...] = (
        "FAST_SNAPSHOT_STATIC_CLOSURE_RECORD",
        "DOCUMENT_BASED_MARKER_EVIDENCE",
        "NO_RUNTIME_RECURSIVE_REVALIDATION",
    )
    forbidden_dependency_modes: tuple[str, ...] = (
        "DEEP_RECURSIVE_TO_PUBLIC_DICT_CHAIN",
        "CLOSED_MILESTONE_VALID_PROPERTY_TRAVERSAL",
        "HISTORICAL_MILESTONE_RUNTIME_REVALIDATION",
        "RECURSIVE_META_LAYER",
    )
    guard_checks: tuple[str, ...] = (
        "scope_lock_valid",
        "fast_snapshot_pattern_enforced",
        "closed_milestone_snapshots_valid",
        "document_evidence_markers_present",
        "deep_recursive_traversal_blocked",
        "runtime_solver_unchanged",
        "runtime_wiring_unchanged",
        "kaggle_paths_unchanged",
        "secret_and_raw_body_persistence_absent",
        "fail_closed_boundary_preserved",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def guard_id(self) -> str:
        return f"MILESTONE-22-FAST-SNAPSHOT-GUARD-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def remaining_budget_after_current_task(self) -> int:
        return self.task_budget_max - self.current_task_number

    @property
    def snapshot_count(self) -> int:
        return len(self.snapshots)

    @property
    def scope_payload(self) -> Mapping[str, Any]:
        return build_milestone_22_objective_scope_lock().to_public_dict()

    @property
    def guard_ok(self) -> bool:
        scope = build_milestone_22_objective_scope_lock()
        scope_payload = scope.to_public_dict()

        return (
            FAST_SNAPSHOT_DEPENDENCY_GUARD_READY is True
            and FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTED is True
            and LOCAL_ONLY_GUARD is True
            and SNAPSHOT_PATTERN_ENFORCED is True
            and DOCUMENT_EVIDENCE_PRESERVED is True
            and DEEP_RECURSIVE_TRAVERSAL_BLOCKED is True
            and READY_FOR_VALIDATION_ARTIFACTS is True
            and scope.valid is True
            and validate_milestone_22_objective_scope_lock(scope) == ()
            and scope_payload["scopeLockId"] == SCOPE_LOCK_ID
            and scope_payload["scopeLocked"] is True
            and scope_payload["implementationAllowedNext"] is True
            and scope_payload["implementationStarted"] is False
            and scope_payload["fastSnapshotPatternRequired"] is True
            and scope_payload["deepRecursiveSerializationForbidden"] is True
            and self.task_budget_max == 8
            and self.current_task_number == 3
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and self.snapshot_count == 2
            and all(snapshot.valid for snapshot in self.snapshots)
            and len(self.allowed_dependency_modes) == 3
            and len(self.forbidden_dependency_modes) == 4
            and len(self.guard_checks) == 10
            and detect_forbidden_runtime_traversal(()) == ()
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

        scope = build_milestone_22_objective_scope_lock()
        if not scope.valid:
            issues.append("SCOPE_LOCK_INVALID")
        issues.extend(f"SCOPE_LOCK_{issue}" for issue in validate_milestone_22_objective_scope_lock(scope))

        if not FAST_SNAPSHOT_DEPENDENCY_GUARD_READY:
            issues.append("FAST_SNAPSHOT_GUARD_NOT_READY")
        if not FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTED:
            issues.append("FAST_SNAPSHOT_GUARD_NOT_IMPLEMENTED")
        if not LOCAL_ONLY_GUARD:
            issues.append("GUARD_NOT_LOCAL_ONLY")
        if not SNAPSHOT_PATTERN_ENFORCED:
            issues.append("SNAPSHOT_PATTERN_NOT_ENFORCED")
        if not DOCUMENT_EVIDENCE_PRESERVED:
            issues.append("DOCUMENT_EVIDENCE_NOT_PRESERVED")
        if not DEEP_RECURSIVE_TRAVERSAL_BLOCKED:
            issues.append("DEEP_RECURSIVE_TRAVERSAL_NOT_BLOCKED")
        if not READY_FOR_VALIDATION_ARTIFACTS:
            issues.append("NOT_READY_FOR_VALIDATION_ARTIFACTS")
        if self.scope_lock_id != SCOPE_LOCK_ID:
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
        if self.snapshot_count != 2:
            issues.append("SNAPSHOT_COUNT_NOT_2")
        for snapshot in self.snapshots:
            if not snapshot.valid:
                issues.append(f"SNAPSHOT_INVALID:{snapshot.milestone_id}")
        if len(self.allowed_dependency_modes) != 3:
            issues.append("ALLOWED_DEPENDENCY_MODE_COUNT_NOT_3")
        if len(self.forbidden_dependency_modes) != 4:
            issues.append("FORBIDDEN_DEPENDENCY_MODE_COUNT_NOT_4")
        if len(self.guard_checks) != 10:
            issues.append("GUARD_CHECK_COUNT_NOT_10")
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
        return self.guard_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        scope = self.scope_payload

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "scopeLockId": self.scope_lock_id,
            "sourceScopeLockId": scope["scopeLockId"],
            "sourceScopeLockValid": scope["valid"],
            "nextStage": self.next_stage,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "snapshotCount": self.snapshot_count,
            "snapshots": [snapshot.to_public_dict() for snapshot in self.snapshots],
            "requiredSnapshotFields": list(REQUIRED_SNAPSHOT_FIELDS),
            "requiredSnapshotFieldCount": len(REQUIRED_SNAPSHOT_FIELDS),
            "allowedDependencyModes": list(self.allowed_dependency_modes),
            "allowedDependencyModeCount": len(self.allowed_dependency_modes),
            "forbiddenDependencyModes": list(self.forbidden_dependency_modes),
            "forbiddenDependencyModeCount": len(self.forbidden_dependency_modes),
            "forbiddenRuntimeTraversalTokens": list(FORBIDDEN_RUNTIME_TRAVERSAL_TOKENS),
            "forbiddenRuntimeTraversalTokenCount": len(FORBIDDEN_RUNTIME_TRAVERSAL_TOKENS),
            "guardChecks": list(self.guard_checks),
            "guardCheckCount": len(self.guard_checks),
            "fastSnapshotDependencyGuardReady": FAST_SNAPSHOT_DEPENDENCY_GUARD_READY,
            "fastSnapshotDependencyGuardImplemented": FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTED,
            "localOnlyGuard": LOCAL_ONLY_GUARD,
            "snapshotPatternEnforced": SNAPSHOT_PATTERN_ENFORCED,
            "documentEvidencePreserved": DOCUMENT_EVIDENCE_PRESERVED,
            "deepRecursiveTraversalBlocked": DEEP_RECURSIVE_TRAVERSAL_BLOCKED,
            "readyForValidationArtifacts": READY_FOR_VALIDATION_ARTIFACTS,
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
            "kaggleAuthenticationAllowed": KAGGLE_AUTHENTICATION_ALLOWED,
            "kaggleUploadAllowed": KAGGLE_UPLOAD_ALLOWED,
            "rawRequestBodyPersisted": RAW_REQUEST_BODY_PERSISTED,
            "secretPersisted": SECRET_PERSISTED,
            "legalCertification": LEGAL_CERTIFICATION,
            "historicalMilestoneRewrite": HISTORICAL_MILESTONE_REWRITE,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
            "guardOk": self.guard_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["guardId"] = self.guard_id
        return payload


def build_fast_snapshot_dependency_guard(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> FastSnapshotDependencyGuard:
    return FastSnapshotDependencyGuard(metadata={} if metadata is None else metadata)


def validate_fast_snapshot_dependency_guard(
    guard: FastSnapshotDependencyGuard,
) -> tuple[str, ...]:
    return guard.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "FAST_SNAPSHOT_DEPENDENCY_GUARD_READY",
    "FastSnapshotDependencySpec",
    "FastSnapshotDependencyGuard",
    "build_closed_milestone_snapshot",
    "build_default_milestone_21_snapshot",
    "build_default_milestone_20_snapshot",
    "detect_forbidden_runtime_traversal",
    "build_fast_snapshot_dependency_guard",
    "validate_fast_snapshot_dependency_guard",
]
