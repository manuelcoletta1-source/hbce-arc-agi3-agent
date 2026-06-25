"""Milestone #23 Task 1 - Governed Opening With Task Budget.

Milestone 23 opens from the closed Milestone 22 Fast Snapshot Dependency Guard
chain.

This opening uses a static closure snapshot instead of recursively walking the
previous milestone runtime object graph. Because apparently we need to write
software that prevents software from staring too long into its own family tree.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


TASK_ID = "MILESTONE_23_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
REVISION = "MILESTONE_23_GOVERNED_OPENING_WITH_TASK_BUDGET_v1"
MILESTONE_ID = "MILESTONE_23"
NEXT_STAGE = "MILESTONE_23_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 1
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

OPENING_READY = True
GOVERNED_TASK_BUDGET_READY = True
OBJECTIVE_SELECTION_REQUIRED_NEXT = True
SCOPE_LOCK_REQUIRED_NEXT = True
IMPLEMENTATION_STARTED = False
IMPLEMENTATION_ALLOWED_AT_TASK_1 = False

SOURCE_MILESTONE_ID = "MILESTONE_22"
SOURCE_FINAL_STATUS = "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
SOURCE_FINAL_TASK_NUMBER = 6
SOURCE_TASK_BUDGET_MAX = 8
SOURCE_TASK_7_USED = False
SOURCE_TASK_8_USED = False
SOURCE_RESERVE_UNUSED = True
SOURCE_EMERGENCY_RESERVE_UNUSED = True
SOURCE_EVIDENCE_DOC_PATH = "docs/milestone-22-task-6-milestone-closure-v1.md"
SOURCE_EVIDENCE_ARTIFACT_PATH = "examples/milestone-22/milestone-closure-v1/task-6-milestone-closure.json"

FAST_SNAPSHOT_DEPENDENCY_MODE = True
DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED = False
DOCUMENT_MARKER_EVIDENCE_REQUIRED = True

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
class Milestone22ClosureSnapshot:
    milestone_id: str = SOURCE_MILESTONE_ID
    final_status: str = SOURCE_FINAL_STATUS
    final_task_number: int = SOURCE_FINAL_TASK_NUMBER
    task_budget_max: int = SOURCE_TASK_BUDGET_MAX
    task_7_used: bool = SOURCE_TASK_7_USED
    task_8_used: bool = SOURCE_TASK_8_USED
    reserve_unused: bool = SOURCE_RESERVE_UNUSED
    emergency_reserve_unused: bool = SOURCE_EMERGENCY_RESERVE_UNUSED
    evidence_doc_path: str = SOURCE_EVIDENCE_DOC_PATH
    evidence_artifact_path: str = SOURCE_EVIDENCE_ARTIFACT_PATH
    evidence_markers: tuple[str, ...] = (
        "MILESTONE_22_TASK_6_MILESTONE_CLOSURE_READY=true",
        "MILESTONE_22_TASK_6_FINAL_STATUS=CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6",
        "MILESTONE_22_TASK_6_TASK_7_USED=false",
        "MILESTONE_22_TASK_6_TASK_8_USED=false",
        "MILESTONE_22_TASK_6_MILESTONE_CLOSED=true",
    )

    @property
    def snapshot_id(self) -> str:
        return f"MILESTONE-22-CLOSURE-SNAPSHOT-{_digest(self.to_public_dict())}"

    @property
    def marker_count(self) -> int:
        return len(self.evidence_markers)

    @property
    def valid(self) -> bool:
        return (
            self.milestone_id == "MILESTONE_22"
            and self.final_status == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
            and self.final_task_number == 6
            and self.task_budget_max == 8
            and self.task_7_used is False
            and self.task_8_used is False
            and self.reserve_unused is True
            and self.emergency_reserve_unused is True
            and self.evidence_doc_path.endswith(".md")
            and self.evidence_artifact_path.endswith(".json")
            and self.marker_count == 5
        )

    def to_public_dict(self) -> dict[str, Any]:
        return {
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
            "markerCount": self.marker_count,
            "valid": self.valid,
        }


@dataclass(frozen=True)
class Milestone23GovernedOpening:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    source_snapshot: Milestone22ClosureSnapshot = field(default_factory=Milestone22ClosureSnapshot)
    opening_checks: tuple[str, ...] = (
        "source_milestone_22_closed",
        "source_task_7_unused",
        "source_task_8_unused",
        "source_closure_artifact_valid",
        "task_budget_min_4",
        "task_budget_max_8",
        "current_task_1",
        "objective_selection_required_next",
        "scope_lock_required_next",
        "implementation_not_started",
        "runtime_boundaries_unchanged",
        "ready_for_task_2_scope_lock",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def opening_id(self) -> str:
        return f"MILESTONE-23-GOVERNED-OPENING-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def remaining_budget_after_current_task(self) -> int:
        return self.task_budget_max - self.current_task_number

    @property
    def opening_ok(self) -> bool:
        return (
            OPENING_READY is True
            and GOVERNED_TASK_BUDGET_READY is True
            and OBJECTIVE_SELECTION_REQUIRED_NEXT is True
            and SCOPE_LOCK_REQUIRED_NEXT is True
            and IMPLEMENTATION_STARTED is False
            and IMPLEMENTATION_ALLOWED_AT_TASK_1 is False
            and self.source_snapshot.valid is True
            and FAST_SNAPSHOT_DEPENDENCY_MODE is True
            and DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED is False
            and DOCUMENT_MARKER_EVIDENCE_REQUIRED is True
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 1
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.opening_checks) == 12
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

        if not OPENING_READY:
            issues.append("OPENING_NOT_READY")
        if not GOVERNED_TASK_BUDGET_READY:
            issues.append("GOVERNED_TASK_BUDGET_NOT_READY")
        if not OBJECTIVE_SELECTION_REQUIRED_NEXT:
            issues.append("OBJECTIVE_SELECTION_NOT_REQUIRED_NEXT")
        if not SCOPE_LOCK_REQUIRED_NEXT:
            issues.append("SCOPE_LOCK_NOT_REQUIRED_NEXT")
        if IMPLEMENTATION_STARTED:
            issues.append("IMPLEMENTATION_STARTED_AT_TASK_1")
        if IMPLEMENTATION_ALLOWED_AT_TASK_1:
            issues.append("IMPLEMENTATION_ALLOWED_AT_TASK_1")
        if not self.source_snapshot.valid:
            issues.append("SOURCE_MILESTONE_22_CLOSURE_SNAPSHOT_INVALID")
        if not FAST_SNAPSHOT_DEPENDENCY_MODE:
            issues.append("FAST_SNAPSHOT_DEPENDENCY_MODE_DISABLED")
        if DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED:
            issues.append("DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED")
        if not DOCUMENT_MARKER_EVIDENCE_REQUIRED:
            issues.append("DOCUMENT_MARKER_EVIDENCE_NOT_REQUIRED")
        if self.task_budget_min != 4:
            issues.append("TASK_BUDGET_MIN_NOT_4")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 1:
            issues.append("CURRENT_TASK_NUMBER_NOT_1")
        if self.recommended_closure_task_number != 6:
            issues.append("RECOMMENDED_CLOSURE_TASK_NOT_6")
        if self.reserve_task_number != 7:
            issues.append("RESERVE_TASK_NUMBER_NOT_7")
        if self.emergency_only_task_number != 8:
            issues.append("EMERGENCY_TASK_NUMBER_NOT_8")
        if len(self.opening_checks) != 12:
            issues.append("OPENING_CHECK_COUNT_NOT_12")
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
        return self.opening_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceMilestoneId": self.source_snapshot.milestone_id,
            "sourceClosureSnapshotId": self.source_snapshot.snapshot_id,
            "sourceClosureSnapshotValid": self.source_snapshot.valid,
            "sourceFinalStatus": self.source_snapshot.final_status,
            "sourceFinalTaskNumber": self.source_snapshot.final_task_number,
            "sourceTaskBudgetMax": self.source_snapshot.task_budget_max,
            "sourceTask7Used": self.source_snapshot.task_7_used,
            "sourceTask8Used": self.source_snapshot.task_8_used,
            "sourceReserveUnused": self.source_snapshot.reserve_unused,
            "sourceEmergencyReserveUnused": self.source_snapshot.emergency_reserve_unused,
            "sourceEvidenceDocPath": self.source_snapshot.evidence_doc_path,
            "sourceEvidenceArtifactPath": self.source_snapshot.evidence_artifact_path,
            "sourceEvidenceMarkerCount": self.source_snapshot.marker_count,
            "nextStage": self.next_stage,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "openingChecks": list(self.opening_checks),
            "openingCheckCount": len(self.opening_checks),
            "openingReady": OPENING_READY,
            "governedTaskBudgetReady": GOVERNED_TASK_BUDGET_READY,
            "objectiveSelectionRequiredNext": OBJECTIVE_SELECTION_REQUIRED_NEXT,
            "scopeLockRequiredNext": SCOPE_LOCK_REQUIRED_NEXT,
            "implementationStarted": IMPLEMENTATION_STARTED,
            "implementationAllowedAtTask1": IMPLEMENTATION_ALLOWED_AT_TASK_1,
            "fastSnapshotDependencyMode": FAST_SNAPSHOT_DEPENDENCY_MODE,
            "deepRecursiveDependencyTraversalAllowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
            "documentMarkerEvidenceRequired": DOCUMENT_MARKER_EVIDENCE_REQUIRED,
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
            "openingOk": self.opening_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["openingId"] = self.opening_id
        return payload


def build_milestone_23_governed_opening(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone23GovernedOpening:
    return Milestone23GovernedOpening(metadata={} if metadata is None else metadata)


def validate_milestone_23_governed_opening(
    opening: Milestone23GovernedOpening,
) -> tuple[str, ...]:
    return opening.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "OPENING_READY",
    "GOVERNED_TASK_BUDGET_READY",
    "Milestone22ClosureSnapshot",
    "Milestone23GovernedOpening",
    "build_milestone_23_governed_opening",
    "validate_milestone_23_governed_opening",
]
