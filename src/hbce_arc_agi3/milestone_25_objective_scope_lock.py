"""Milestone #25 Task 2 - Objective Selection and Scope Lock.

Selects and locks the Milestone 25 objective.

No implementation starts in Task 2. This task only selects the objective,
defines allowed and forbidden operations, and locks the local-only boundary.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


TASK_ID = "MILESTONE_25_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
REVISION = "MILESTONE_25_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_v1"
MILESTONE_ID = "MILESTONE_25"
SOURCE_TASK_ID = "MILESTONE_25_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
NEXT_STAGE = "MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_IMPLEMENTATION_V1"

SELECTED_OBJECTIVE_ID = "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"
SCOPE_LOCK_ID = "MILESTONE_25_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 2
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

OBJECTIVE_SELECTED = True
SCOPE_LOCKED = True
IMPLEMENTATION_ALLOWED_NEXT = True
IMPLEMENTATION_STARTED = False
EVIDENCE_BUNDLE_IMPLEMENTATION_STARTED = False

LOCAL_ONLY = True
READ_ONLY_SOURCE = True
PUBLIC_SAFE = True
DETERMINISTIC = True
FAST_SOURCE_OPENING_SNAPSHOT = True
FAST_SNAPSHOT_DEPENDENCY_MODE = True
DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED = False
DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_FORBIDDEN = True
NO_RECURSIVE_META_LAYER = True

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

ALLOWED_OPERATIONS = (
    "build_closed_milestone_snapshot_query_result_evidence_bundle",
    "generate_local_public_safe_evidence_manifest",
    "validate_evidence_bundle_boundary",
    "summarize_evidence_bundle_integrity",
)

FORBIDDEN_OPERATIONS = (
    "modify_runtime_solver",
    "send_kaggle_submission",
    "authenticate_to_kaggle",
    "upload_to_kaggle",
    "persist_raw_request_body",
    "persist_secret",
    "rewrite_historical_milestone",
    "perform_deep_recursive_dependency_traversal",
    "emit_legal_certification",
)

STATIC_SOURCE_OPENING_SNAPSHOT: dict[str, Any] = {
    "taskId": SOURCE_TASK_ID,
    "milestoneId": "MILESTONE_25",
    "sourceMilestoneId": "MILESTONE_24",
    "sourceFinalStatus": "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6",
    "sourceTask7Used": False,
    "sourceTask8Used": False,
    "sourceMilestoneClosed": True,
    "taskBudgetMin": 4,
    "taskBudgetMax": 8,
    "currentTaskNumber": 1,
    "remainingBudgetAfterCurrentTask": 7,
    "objectiveSelectionRequiredNext": True,
    "scopeLockRequiredNext": True,
    "implementationStarted": False,
    "implementationAllowedAtTask1": False,
    "fastSourceClosureSnapshot": True,
    "deepRecursiveDependencyTraversalAllowed": False,
    "valid": True,
}


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


def build_fast_source_opening_snapshot() -> dict[str, Any]:
    return dict(STATIC_SOURCE_OPENING_SNAPSHOT)


@dataclass(frozen=True)
class Milestone25ObjectiveScopeLock:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    source_task_id: str = SOURCE_TASK_ID
    next_stage: str = NEXT_STAGE
    selected_objective_id: str = SELECTED_OBJECTIVE_ID
    scope_lock_id: str = SCOPE_LOCK_ID
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    allowed_operations: tuple[str, ...] = ALLOWED_OPERATIONS
    forbidden_operations: tuple[str, ...] = FORBIDDEN_OPERATIONS
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def lock_id(self) -> str:
        return f"MILESTONE-25-SCOPE-LOCK-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def source_opening_snapshot(self) -> Mapping[str, Any]:
        return build_fast_source_opening_snapshot()

    @property
    def remaining_budget_after_current_task(self) -> int:
        return self.task_budget_max - self.current_task_number

    @property
    def lock_ok(self) -> bool:
        source = self.source_opening_snapshot

        return (
            source["valid"] is True
            and source["milestoneId"] == "MILESTONE_25"
            and source["sourceMilestoneId"] == "MILESTONE_24"
            and source["sourceFinalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
            and source["sourceTask7Used"] is False
            and source["sourceTask8Used"] is False
            and source["sourceMilestoneClosed"] is True
            and source["taskBudgetMax"] == 8
            and source["currentTaskNumber"] == 1
            and source["objectiveSelectionRequiredNext"] is True
            and source["scopeLockRequiredNext"] is True
            and source["implementationStarted"] is False
            and source["implementationAllowedAtTask1"] is False
            and source["fastSourceClosureSnapshot"] is True
            and self.selected_objective_id == SELECTED_OBJECTIVE_ID
            and self.scope_lock_id == SCOPE_LOCK_ID
            and OBJECTIVE_SELECTED is True
            and SCOPE_LOCKED is True
            and IMPLEMENTATION_ALLOWED_NEXT is True
            and IMPLEMENTATION_STARTED is False
            and EVIDENCE_BUNDLE_IMPLEMENTATION_STARTED is False
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 2
            and self.remaining_budget_after_current_task == 6
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.allowed_operations) == 4
            and len(self.forbidden_operations) == 9
            and LOCAL_ONLY is True
            and READ_ONLY_SOURCE is True
            and PUBLIC_SAFE is True
            and DETERMINISTIC is True
            and FAST_SOURCE_OPENING_SNAPSHOT is True
            and FAST_SNAPSHOT_DEPENDENCY_MODE is True
            and DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED is False
            and DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_FORBIDDEN is True
            and NO_RECURSIVE_META_LAYER is True
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
        source = self.source_opening_snapshot

        if source["valid"] is not True:
            issues.append("SOURCE_OPENING_SNAPSHOT_INVALID")
        if source["milestoneId"] != "MILESTONE_25":
            issues.append("SOURCE_MILESTONE_ID_MISMATCH")
        if source["objectiveSelectionRequiredNext"] is not True:
            issues.append("SOURCE_OBJECTIVE_SELECTION_NOT_REQUIRED")
        if source["scopeLockRequiredNext"] is not True:
            issues.append("SOURCE_SCOPE_LOCK_NOT_REQUIRED")
        if source["implementationStarted"] is not False:
            issues.append("SOURCE_IMPLEMENTATION_ALREADY_STARTED")
        if self.selected_objective_id != SELECTED_OBJECTIVE_ID:
            issues.append("SELECTED_OBJECTIVE_ID_MISMATCH")
        if self.scope_lock_id != SCOPE_LOCK_ID:
            issues.append("SCOPE_LOCK_ID_MISMATCH")
        if not OBJECTIVE_SELECTED:
            issues.append("OBJECTIVE_NOT_SELECTED")
        if not SCOPE_LOCKED:
            issues.append("SCOPE_NOT_LOCKED")
        if not IMPLEMENTATION_ALLOWED_NEXT:
            issues.append("IMPLEMENTATION_NOT_ALLOWED_NEXT")
        if IMPLEMENTATION_STARTED:
            issues.append("IMPLEMENTATION_STARTED_AT_TASK_2")
        if EVIDENCE_BUNDLE_IMPLEMENTATION_STARTED:
            issues.append("EVIDENCE_BUNDLE_IMPLEMENTATION_STARTED_AT_TASK_2")
        if self.task_budget_min != 4:
            issues.append("TASK_BUDGET_MIN_NOT_4")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 2:
            issues.append("CURRENT_TASK_NUMBER_NOT_2")
        if self.remaining_budget_after_current_task != 6:
            issues.append("REMAINING_BUDGET_NOT_6")
        if len(self.allowed_operations) != 4:
            issues.append("ALLOWED_OPERATION_COUNT_NOT_4")
        if len(self.forbidden_operations) != 9:
            issues.append("FORBIDDEN_OPERATION_COUNT_NOT_9")
        if DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED:
            issues.append("DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED")
        if RUNTIME_SOLVER_MODIFIED:
            issues.append("RUNTIME_SOLVER_MODIFIED")
        if KAGGLE_SUBMISSION_SENT:
            issues.append("KAGGLE_SUBMISSION_SENT")
        if LEGAL_CERTIFICATION:
            issues.append("LEGAL_CERTIFICATION")

        return tuple(issues)

    @property
    def valid(self) -> bool:
        return self.lock_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        source = self.source_opening_snapshot

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceTaskId": self.source_task_id,
            "sourceOpeningValid": source["valid"],
            "sourceMilestoneId": source["milestoneId"],
            "sourceFinalStatus": source["sourceFinalStatus"],
            "sourceTask7Used": source["sourceTask7Used"],
            "sourceTask8Used": source["sourceTask8Used"],
            "sourceMilestoneClosed": source["sourceMilestoneClosed"],
            "sourceObjectiveSelectionRequiredNext": source["objectiveSelectionRequiredNext"],
            "sourceScopeLockRequiredNext": source["scopeLockRequiredNext"],
            "sourceImplementationStarted": source["implementationStarted"],
            "sourceFastClosureSnapshot": source["fastSourceClosureSnapshot"],
            "selectedObjectiveId": self.selected_objective_id,
            "scopeLockId": self.scope_lock_id,
            "nextStage": self.next_stage,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "objectiveSelected": OBJECTIVE_SELECTED,
            "scopeLocked": SCOPE_LOCKED,
            "implementationAllowedNext": IMPLEMENTATION_ALLOWED_NEXT,
            "implementationStarted": IMPLEMENTATION_STARTED,
            "evidenceBundleImplementationStarted": EVIDENCE_BUNDLE_IMPLEMENTATION_STARTED,
            "allowedOperations": list(self.allowed_operations),
            "allowedOperationCount": len(self.allowed_operations),
            "forbiddenOperations": list(self.forbidden_operations),
            "forbiddenOperationCount": len(self.forbidden_operations),
            "localOnly": LOCAL_ONLY,
            "readOnlySource": READ_ONLY_SOURCE,
            "publicSafe": PUBLIC_SAFE,
            "deterministic": DETERMINISTIC,
            "fastSourceOpeningSnapshot": FAST_SOURCE_OPENING_SNAPSHOT,
            "fastSnapshotDependencyMode": FAST_SNAPSHOT_DEPENDENCY_MODE,
            "deepRecursiveDependencyTraversalAllowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
            "deepRecursiveDependencyTraversalForbidden": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_FORBIDDEN,
            "noRecursiveMetaLayer": NO_RECURSIVE_META_LAYER,
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
            payload["lockArtifactId"] = self.lock_id
        return payload


def build_milestone_25_objective_scope_lock(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone25ObjectiveScopeLock:
    return Milestone25ObjectiveScopeLock(metadata={} if metadata is None else metadata)


def validate_milestone_25_objective_scope_lock(
    lock: Milestone25ObjectiveScopeLock,
) -> tuple[str, ...]:
    return lock.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "SELECTED_OBJECTIVE_ID",
    "SCOPE_LOCK_ID",
    "OBJECTIVE_SELECTED",
    "SCOPE_LOCKED",
    "FAST_SOURCE_OPENING_SNAPSHOT",
    "build_fast_source_opening_snapshot",
    "Milestone25ObjectiveScopeLock",
    "build_milestone_25_objective_scope_lock",
    "validate_milestone_25_objective_scope_lock",
]
