"""Milestone #23 Task 3 - Closed Milestone Snapshot Registry Implementation.

Implements a local-only registry for closed milestone snapshots.

The registry provides static lookup of closed milestone closure evidence without
deep recursive traversal into historical milestone runtime objects. A tiny
thing, yes. Also the difference between a controlled chain and software chewing
through its own ancestry like a deranged ouroboros.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

from hbce_arc_agi3.milestone_23_objective_scope_lock import (
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    build_milestone_23_objective_scope_lock,
    validate_milestone_23_objective_scope_lock,
)


TASK_ID = "MILESTONE_23_TASK_3_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_IMPLEMENTATION_V1"
REVISION = "MILESTONE_23_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_IMPLEMENTATION_v1"
MILESTONE_ID = "MILESTONE_23"
NEXT_STAGE = "MILESTONE_23_TASK_4_VALIDATION_AND_ARTIFACTS_V1"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 3
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

REGISTRY_IMPLEMENTATION_READY = True
REGISTRY_IMPLEMENTED = True
REGISTRY_LOOKUP_READY = True
REGISTRY_STATIC_SNAPSHOTS_READY = True
REGISTRY_VALIDATION_READY = True
READY_FOR_VALIDATION_ARTIFACTS = True

LOCAL_ONLY = True
DETERMINISTIC = True
PUBLIC_SAFE = True
FAST_SNAPSHOT_DEPENDENCY_MODE = True
DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED = False
DOCUMENT_MARKER_EVIDENCE_REQUIRED = True
STATIC_CLOSURE_SNAPSHOT_REQUIRED = True
CLOSED_MILESTONE_ARTIFACT_LOOKUP_REQUIRED = True

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

FORBIDDEN_TRAVERSAL_TOKENS = (
    "closed_milestone.to_public_dict()",
    "closed_milestone.valid",
    "historical_milestone_revalidation_as_runtime_traversal",
    "recursive_previous_milestone_lookup",
    "runtime_object_graph_walk",
)

REQUIRED_SNAPSHOT_FIELDS = (
    "milestoneId",
    "finalStatus",
    "finalTaskNumber",
    "taskBudgetMax",
    "task7Used",
    "task8Used",
    "evidenceDocPath",
    "evidenceArtifactPath",
    "evidenceMarkers",
    "valid",
)


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


def detect_forbidden_registry_traversal(tokens: Iterable[str]) -> tuple[str, ...]:
    token_set = tuple(tokens)
    return tuple(token for token in token_set if token in FORBIDDEN_TRAVERSAL_TOKENS)


@dataclass(frozen=True)
class ClosedMilestoneSnapshot:
    milestone_id: str
    final_status: str
    final_task_number: int
    task_budget_max: int
    task_7_used: bool
    task_8_used: bool
    reserve_unused: bool
    emergency_reserve_unused: bool
    evidence_doc_path: str
    evidence_artifact_path: str
    evidence_markers: tuple[str, ...]
    source_commit_hint: str = "STATIC_SNAPSHOT"

    @property
    def snapshot_id(self) -> str:
        return f"{self.milestone_id}-CLOSED-SNAPSHOT-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def marker_count(self) -> int:
        return len(self.evidence_markers)

    @property
    def valid(self) -> bool:
        return (
            self.milestone_id.startswith("MILESTONE_")
            and bool(self.final_status)
            and self.final_task_number >= 1
            and self.task_budget_max == 8
            and self.task_8_used is False
            and self.evidence_doc_path.endswith(".md")
            and self.evidence_artifact_path.endswith(".json")
            and self.marker_count >= 5
            and all(marker.startswith(self.milestone_id) for marker in self.evidence_markers)
        )

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "milestoneId": self.milestone_id,
            "finalStatus": self.final_status,
            "finalTaskNumber": self.final_task_number,
            "taskBudgetMax": self.task_budget_max,
            "task7Used": self.task_7_used,
            "task8Used": self.task_8_used,
            "reserveUnused": self.reserve_unused,
            "emergencyReserveUnused": self.emergency_reserve_unused,
            "evidenceDocPath": self.evidence_doc_path,
            "evidenceArtifactPath": self.evidence_artifact_path,
            "evidenceMarkers": list(self.evidence_markers),
            "evidenceMarkerCount": self.marker_count,
            "sourceCommitHint": self.source_commit_hint,
            "valid": self.valid,
        }
        if include_id:
            payload["snapshotId"] = self.snapshot_id
        return payload


MILESTONE_22_SNAPSHOT = ClosedMilestoneSnapshot(
    milestone_id="MILESTONE_22",
    final_status="CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6",
    final_task_number=6,
    task_budget_max=8,
    task_7_used=False,
    task_8_used=False,
    reserve_unused=True,
    emergency_reserve_unused=True,
    evidence_doc_path="docs/milestone-22-task-6-milestone-closure-v1.md",
    evidence_artifact_path="examples/milestone-22/milestone-closure-v1/task-6-milestone-closure.json",
    evidence_markers=(
        "MILESTONE_22_TASK_6_MILESTONE_CLOSURE_READY=true",
        "MILESTONE_22_TASK_6_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6",
        "MILESTONE_22_TASK_6_TASK_7_USED=false",
        "MILESTONE_22_TASK_6_TASK_8_USED=false",
        "MILESTONE_22_TASK_6_MILESTONE_CLOSED=true",
    ),
    source_commit_hint="fda1035",
)

MILESTONE_21_SNAPSHOT = ClosedMilestoneSnapshot(
    milestone_id="MILESTONE_21",
    final_status="CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6",
    final_task_number=6,
    task_budget_max=8,
    task_7_used=False,
    task_8_used=False,
    reserve_unused=True,
    emergency_reserve_unused=True,
    evidence_doc_path="docs/milestone-21-task-6-milestone-closure-v1.md",
    evidence_artifact_path="examples/milestone-21/milestone-closure-v1/task-6-milestone-closure.json",
    evidence_markers=(
        "MILESTONE_21_TASK_6_MILESTONE_CLOSURE_READY=true",
        "MILESTONE_21_TASK_6_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6",
        "MILESTONE_21_TASK_6_TASK_7_USED=false",
        "MILESTONE_21_TASK_6_TASK_8_USED=false",
        "MILESTONE_21_TASK_6_MILESTONE_CLOSED=true",
    ),
    source_commit_hint="612e6d0",
)

MILESTONE_20_SNAPSHOT = ClosedMilestoneSnapshot(
    milestone_id="MILESTONE_20",
    final_status="CLOSED_WITH_TASK_BUDGET_MAX_8",
    final_task_number=7,
    task_budget_max=8,
    task_7_used=True,
    task_8_used=False,
    reserve_unused=False,
    emergency_reserve_unused=True,
    evidence_doc_path="docs/milestone-20-governed-execution-closure-v1.md",
    evidence_artifact_path="examples/milestone-20/governed-execution-closure-v1/milestone-20-closure.json",
    evidence_markers=(
        "MILESTONE_20_CLOSED=true",
        "MILESTONE_20_FINAL_TASK_NUMBER=7",
        "MILESTONE_20_TASK_7_USED=true",
        "MILESTONE_20_TASK_8_USED=false",
        "MILESTONE_20_TASK_BUDGET_MAX=8",
    ),
    source_commit_hint="9968c32",
)


@dataclass(frozen=True)
class ClosedMilestoneSnapshotRegistry:
    snapshots: tuple[ClosedMilestoneSnapshot, ...] = (
        MILESTONE_20_SNAPSHOT,
        MILESTONE_21_SNAPSHOT,
        MILESTONE_22_SNAPSHOT,
    )

    @property
    def registry_id(self) -> str:
        return f"CLOSED-MILESTONE-SNAPSHOT-REGISTRY-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def milestone_ids(self) -> tuple[str, ...]:
        return tuple(snapshot.milestone_id for snapshot in self.snapshots)

    @property
    def snapshot_count(self) -> int:
        return len(self.snapshots)

    @property
    def valid_snapshot_count(self) -> int:
        return len([snapshot for snapshot in self.snapshots if snapshot.valid])

    @property
    def valid(self) -> bool:
        return (
            self.snapshot_count == 3
            and self.valid_snapshot_count == 3
            and self.milestone_ids == ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22")
            and len(set(self.milestone_ids)) == self.snapshot_count
            and MILESTONE_22_SNAPSHOT.task_7_used is False
            and MILESTONE_22_SNAPSHOT.task_8_used is False
            and MILESTONE_21_SNAPSHOT.task_7_used is False
            and MILESTONE_21_SNAPSHOT.task_8_used is False
            and MILESTONE_20_SNAPSHOT.task_7_used is True
            and MILESTONE_20_SNAPSHOT.task_8_used is False
        )

    def contains(self, milestone_id: str) -> bool:
        return milestone_id in self.milestone_ids

    def get(self, milestone_id: str) -> ClosedMilestoneSnapshot:
        for snapshot in self.snapshots:
            if snapshot.milestone_id == milestone_id:
                return snapshot
        raise KeyError(f"Closed milestone snapshot not registered: {milestone_id}")

    def try_get(self, milestone_id: str) -> ClosedMilestoneSnapshot | None:
        try:
            return self.get(milestone_id)
        except KeyError:
            return None

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "registryRevision": REVISION,
            "snapshotCount": self.snapshot_count,
            "validSnapshotCount": self.valid_snapshot_count,
            "milestoneIds": list(self.milestone_ids),
            "snapshots": [snapshot.to_public_dict() for snapshot in self.snapshots],
            "requiredSnapshotFields": list(REQUIRED_SNAPSHOT_FIELDS),
            "requiredSnapshotFieldCount": len(REQUIRED_SNAPSHOT_FIELDS),
            "forbiddenTraversalTokens": list(FORBIDDEN_TRAVERSAL_TOKENS),
            "forbiddenTraversalTokenCount": len(FORBIDDEN_TRAVERSAL_TOKENS),
            "localOnly": LOCAL_ONLY,
            "deterministic": DETERMINISTIC,
            "publicSafe": PUBLIC_SAFE,
            "fastSnapshotDependencyMode": FAST_SNAPSHOT_DEPENDENCY_MODE,
            "deepRecursiveDependencyTraversalAllowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
            "documentMarkerEvidenceRequired": DOCUMENT_MARKER_EVIDENCE_REQUIRED,
            "staticClosureSnapshotRequired": STATIC_CLOSURE_SNAPSHOT_REQUIRED,
            "closedMilestoneArtifactLookupRequired": CLOSED_MILESTONE_ARTIFACT_LOOKUP_REQUIRED,
            "valid": self.valid,
        }
        if include_id:
            payload["registryId"] = self.registry_id
        return payload


@dataclass(frozen=True)
class Milestone23ClosedMilestoneSnapshotRegistryImplementation:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    registry: ClosedMilestoneSnapshotRegistry = field(default_factory=ClosedMilestoneSnapshotRegistry)
    implementation_checks: tuple[str, ...] = (
        "scope_lock_valid",
        "selected_objective_matches_registry",
        "registry_implemented",
        "registry_lookup_ready",
        "three_static_snapshots_registered",
        "milestone_22_snapshot_registered",
        "milestone_22_task7_unused_preserved",
        "milestone_22_task8_unused_preserved",
        "milestone_20_task7_used_preserved",
        "deep_recursive_traversal_forbidden",
        "runtime_boundaries_unchanged",
        "ready_for_validation_artifacts",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def implementation_id(self) -> str:
        return f"MILESTONE-23-SNAPSHOT-REGISTRY-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def scope_lock_payload(self) -> Mapping[str, Any]:
        return build_milestone_23_objective_scope_lock().to_public_dict()

    @property
    def implementation_ok(self) -> bool:
        scope_lock = build_milestone_23_objective_scope_lock()
        scope_lock_payload = scope_lock.to_public_dict()
        forbidden_sample = detect_forbidden_registry_traversal(
            (
                "static_registry_lookup",
                "closed_milestone.to_public_dict()",
                "recursive_previous_milestone_lookup",
                "safe_document_marker_evidence",
            )
        )

        return (
            REGISTRY_IMPLEMENTATION_READY is True
            and REGISTRY_IMPLEMENTED is True
            and REGISTRY_LOOKUP_READY is True
            and REGISTRY_STATIC_SNAPSHOTS_READY is True
            and REGISTRY_VALIDATION_READY is True
            and READY_FOR_VALIDATION_ARTIFACTS is True
            and scope_lock.valid is True
            and validate_milestone_23_objective_scope_lock(scope_lock) == ()
            and scope_lock_payload["valid"] is True
            and scope_lock_payload["scopeLocked"] is True
            and scope_lock_payload["selectedObjectiveId"] == "CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY"
            and scope_lock_payload["implementationAllowedNext"] is True
            and scope_lock_payload["implementationStarted"] is False
            and self.registry.valid is True
            and self.registry.snapshot_count == 3
            and self.registry.valid_snapshot_count == 3
            and self.registry.contains("MILESTONE_22") is True
            and self.registry.get("MILESTONE_22").task_7_used is False
            and self.registry.get("MILESTONE_22").task_8_used is False
            and self.registry.get("MILESTONE_20").task_7_used is True
            and self.registry.get("MILESTONE_20").task_8_used is False
            and forbidden_sample == ("closed_milestone.to_public_dict()", "recursive_previous_milestone_lookup")
            and LOCAL_ONLY is True
            and DETERMINISTIC is True
            and PUBLIC_SAFE is True
            and FAST_SNAPSHOT_DEPENDENCY_MODE is True
            and DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED is False
            and DOCUMENT_MARKER_EVIDENCE_REQUIRED is True
            and STATIC_CLOSURE_SNAPSHOT_REQUIRED is True
            and CLOSED_MILESTONE_ARTIFACT_LOOKUP_REQUIRED is True
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 3
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.implementation_checks) == 12
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

        scope_lock = build_milestone_23_objective_scope_lock()
        if not scope_lock.valid:
            issues.append("OBJECTIVE_SCOPE_LOCK_INVALID")
        issues.extend(f"OBJECTIVE_SCOPE_LOCK_{issue}" for issue in validate_milestone_23_objective_scope_lock(scope_lock))

        if not REGISTRY_IMPLEMENTATION_READY:
            issues.append("REGISTRY_IMPLEMENTATION_NOT_READY")
        if not REGISTRY_IMPLEMENTED:
            issues.append("REGISTRY_NOT_IMPLEMENTED")
        if not REGISTRY_LOOKUP_READY:
            issues.append("REGISTRY_LOOKUP_NOT_READY")
        if not REGISTRY_STATIC_SNAPSHOTS_READY:
            issues.append("REGISTRY_STATIC_SNAPSHOTS_NOT_READY")
        if not REGISTRY_VALIDATION_READY:
            issues.append("REGISTRY_VALIDATION_NOT_READY")
        if not READY_FOR_VALIDATION_ARTIFACTS:
            issues.append("NOT_READY_FOR_VALIDATION_ARTIFACTS")
        if not self.registry.valid:
            issues.append("REGISTRY_INVALID")
        if self.registry.snapshot_count != 3:
            issues.append("REGISTRY_SNAPSHOT_COUNT_NOT_3")
        if not self.registry.contains("MILESTONE_22"):
            issues.append("MILESTONE_22_NOT_REGISTERED")
        if self.task_budget_min != 4:
            issues.append("TASK_BUDGET_MIN_NOT_4")
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
        if len(self.implementation_checks) != 12:
            issues.append("IMPLEMENTATION_CHECK_COUNT_NOT_12")
        if not LOCAL_ONLY:
            issues.append("LOCAL_ONLY_FALSE")
        if not DETERMINISTIC:
            issues.append("DETERMINISTIC_FALSE")
        if not PUBLIC_SAFE:
            issues.append("PUBLIC_SAFE_FALSE")
        if not FAST_SNAPSHOT_DEPENDENCY_MODE:
            issues.append("FAST_SNAPSHOT_DEPENDENCY_MODE_DISABLED")
        if DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED:
            issues.append("DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED")
        if not DOCUMENT_MARKER_EVIDENCE_REQUIRED:
            issues.append("DOCUMENT_MARKER_EVIDENCE_NOT_REQUIRED")
        if not STATIC_CLOSURE_SNAPSHOT_REQUIRED:
            issues.append("STATIC_CLOSURE_SNAPSHOT_NOT_REQUIRED")
        if not CLOSED_MILESTONE_ARTIFACT_LOOKUP_REQUIRED:
            issues.append("CLOSED_MILESTONE_ARTIFACT_LOOKUP_NOT_REQUIRED")
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
        return self.implementation_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        scope_lock_payload = self.scope_lock_payload
        registry_payload = self.registry.to_public_dict()

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceScopeLockId": scope_lock_payload["lockId"],
            "sourceScopeLockValid": scope_lock_payload["valid"],
            "scopeLockId": scope_lock_payload["scopeLockId"],
            "selectedObjectiveId": scope_lock_payload["selectedObjectiveId"],
            "nextStage": self.next_stage,
            "registryId": registry_payload["registryId"],
            "registryValid": registry_payload["valid"],
            "registrySnapshotCount": registry_payload["snapshotCount"],
            "registryValidSnapshotCount": registry_payload["validSnapshotCount"],
            "registeredMilestoneIds": registry_payload["milestoneIds"],
            "requiredSnapshotFieldCount": registry_payload["requiredSnapshotFieldCount"],
            "forbiddenTraversalTokenCount": registry_payload["forbiddenTraversalTokenCount"],
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.task_budget_max - self.current_task_number,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "implementationChecks": list(self.implementation_checks),
            "implementationCheckCount": len(self.implementation_checks),
            "registryImplementationReady": REGISTRY_IMPLEMENTATION_READY,
            "registryImplemented": REGISTRY_IMPLEMENTED,
            "registryLookupReady": REGISTRY_LOOKUP_READY,
            "registryStaticSnapshotsReady": REGISTRY_STATIC_SNAPSHOTS_READY,
            "registryValidationReady": REGISTRY_VALIDATION_READY,
            "readyForValidationArtifacts": READY_FOR_VALIDATION_ARTIFACTS,
            "localOnly": LOCAL_ONLY,
            "deterministic": DETERMINISTIC,
            "publicSafe": PUBLIC_SAFE,
            "fastSnapshotDependencyMode": FAST_SNAPSHOT_DEPENDENCY_MODE,
            "deepRecursiveDependencyTraversalAllowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
            "documentMarkerEvidenceRequired": DOCUMENT_MARKER_EVIDENCE_REQUIRED,
            "staticClosureSnapshotRequired": STATIC_CLOSURE_SNAPSHOT_REQUIRED,
            "closedMilestoneArtifactLookupRequired": CLOSED_MILESTONE_ARTIFACT_LOOKUP_REQUIRED,
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
            "implementationOk": self.implementation_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["implementationId"] = self.implementation_id
        return payload


def build_closed_milestone_snapshot_registry() -> ClosedMilestoneSnapshotRegistry:
    return ClosedMilestoneSnapshotRegistry()


def build_milestone_23_closed_milestone_snapshot_registry_implementation(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone23ClosedMilestoneSnapshotRegistryImplementation:
    return Milestone23ClosedMilestoneSnapshotRegistryImplementation(metadata={} if metadata is None else metadata)


def validate_milestone_23_closed_milestone_snapshot_registry_implementation(
    implementation: Milestone23ClosedMilestoneSnapshotRegistryImplementation,
) -> tuple[str, ...]:
    return implementation.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "REGISTRY_IMPLEMENTATION_READY",
    "REGISTRY_IMPLEMENTED",
    "ClosedMilestoneSnapshot",
    "ClosedMilestoneSnapshotRegistry",
    "Milestone23ClosedMilestoneSnapshotRegistryImplementation",
    "build_closed_milestone_snapshot_registry",
    "build_milestone_23_closed_milestone_snapshot_registry_implementation",
    "validate_milestone_23_closed_milestone_snapshot_registry_implementation",
    "detect_forbidden_registry_traversal",
]
