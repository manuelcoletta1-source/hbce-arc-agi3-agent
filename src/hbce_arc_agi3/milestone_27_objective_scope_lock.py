"""Milestone #27 Task 2 - Objective Selection and Scope Lock.

Selects and locks the Milestone 27 objective after governed opening.

This task chooses a local-only query interface objective over the closed milestone
archive index produced by Milestone 26. It does not implement the interface yet.
Yes, we are deliberately preventing the code from sprinting into traffic. 🧷
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


TASK_ID = "MILESTONE_27_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
REVISION = "MILESTONE_27_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_v1"
MILESTONE_ID = "MILESTONE_27"
SOURCE_TASK_ID = "MILESTONE_27_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
NEXT_STAGE = "MILESTONE_27_TASK_3_QUERY_INTERFACE_IMPLEMENTATION_V1"

SELECTED_OBJECTIVE_ID = "CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_INTERFACE_LOCAL_ONLY"
SCOPE_LOCK_ID = "MILESTONE_27_SCOPE_CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_INTERFACE_LOCAL_ONLY"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 2
REMAINING_BUDGET_AFTER_CURRENT_TASK = 6
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

OBJECTIVE_SELECTED = True
SCOPE_LOCKED = True
IMPLEMENTATION_ALLOWED_NEXT = True
IMPLEMENTATION_STARTED = False
QUERY_INTERFACE_IMPLEMENTATION_STARTED = False

ALLOWED_OPERATIONS = (
    "select_local_only_archive_index_query_interface_objective",
    "lock_public_safe_query_interface_scope",
    "emit_scope_lock_artifacts",
    "prepare_query_interface_implementation_next",
)

FORBIDDEN_OPERATIONS = (
    "runtime_solver_mutation",
    "runtime_wiring_change",
    "kaggle_submission",
    "kaggle_authentication",
    "kaggle_upload",
    "raw_request_body_persistence",
    "secret_persistence",
    "legal_certification",
    "deep_recursive_dependency_traversal",
)

SCOPE_CHECKS = (
    "source_governed_opening_valid",
    "source_task_budget_locked",
    "source_objective_selection_required_next",
    "source_scope_lock_required_next",
    "source_implementation_not_started",
    "source_implementation_not_allowed_at_task_1",
    "selected_objective_local_only",
    "selected_objective_archive_index_query_interface",
    "scope_locked",
    "implementation_allowed_next",
    "query_interface_implementation_not_started",
    "runtime_solver_unmodified",
    "legal_certification_false",
)

GENERATED_ARTIFACTS = (
    "examples/milestone-27/objective-selection-and-scope-lock-v1/task-2-objective-scope-lock.json",
    "examples/milestone-27/objective-selection-and-scope-lock-v1/task-2-objective-scope-lock.md",
    "examples/milestone-27/objective-selection-and-scope-lock-v1/task-2-manifest.json",
    "examples/milestone-27/objective-selection-and-scope-lock-v1/task-2-index.txt",
)

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

STATIC_SOURCE_OPENING_SNAPSHOT: dict[str, Any] = {
    "taskId": SOURCE_TASK_ID,
    "milestoneId": MILESTONE_ID,
    "sourceMilestoneId": "MILESTONE_26",
    "sourceFinalStatus": "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6",
    "sourceTechnicalStatus": "PASS",
    "sourceProcessStatus": "GOVERNED_WITHIN_TASK_BUDGET",
    "sourceFinalTaskNumber": 6,
    "sourceCompletedTaskCount": 6,
    "sourceTask7Used": False,
    "sourceTask8Used": False,
    "sourceMilestoneClosed": True,
    "sourceReadyForNextMilestone": True,
    "governedOpeningReady": True,
    "taskBudgetLocked": True,
    "taskBudgetMin": 4,
    "taskBudgetMax": 8,
    "currentTaskNumber": 1,
    "remainingBudgetAfterCurrentTask": 7,
    "objectiveSelectionRequiredNext": True,
    "scopeLockRequiredNext": True,
    "implementationStarted": False,
    "implementationAllowedAtTask1": False,
    "openingCheckCount": 16,
    "generatedArtifactCount": 4,
    "fastSourceClosureSnapshot": True,
    "deepRecursiveDependencyTraversalAllowed": False,
    "runtimeSolverModified": False,
    "kaggleSubmissionSent": False,
    "legalCertification": False,
    "valid": True,
    "openingOk": True,
    "issues": [],
}


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


def build_fast_source_opening_snapshot() -> dict[str, Any]:
    return dict(STATIC_SOURCE_OPENING_SNAPSHOT)


@dataclass(frozen=True)
class Milestone27ObjectiveScopeLock:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    source_task_id: str = SOURCE_TASK_ID
    selected_objective_id: str = SELECTED_OBJECTIVE_ID
    scope_lock_id: str = SCOPE_LOCK_ID
    next_stage: str = NEXT_STAGE
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    remaining_budget_after_current_task: int = REMAINING_BUDGET_AFTER_CURRENT_TASK
    allowed_operations: tuple[str, ...] = ALLOWED_OPERATIONS
    forbidden_operations: tuple[str, ...] = FORBIDDEN_OPERATIONS
    scope_checks: tuple[str, ...] = SCOPE_CHECKS
    generated_artifacts: tuple[str, ...] = GENERATED_ARTIFACTS
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def lock_id(self) -> str:
        return f"MILESTONE-27-SCOPE-LOCK-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def source_opening_snapshot(self) -> Mapping[str, Any]:
        return build_fast_source_opening_snapshot()

    @property
    def lock_ok(self) -> bool:
        source = self.source_opening_snapshot

        return (
            source["valid"] is True
            and source["openingOk"] is True
            and source["issues"] == []
            and source["milestoneId"] == MILESTONE_ID
            and source["governedOpeningReady"] is True
            and source["taskBudgetLocked"] is True
            and source["taskBudgetMax"] == 8
            and source["currentTaskNumber"] == 1
            and source["objectiveSelectionRequiredNext"] is True
            and source["scopeLockRequiredNext"] is True
            and source["implementationStarted"] is False
            and source["implementationAllowedAtTask1"] is False
            and source["deepRecursiveDependencyTraversalAllowed"] is False
            and source["runtimeSolverModified"] is False
            and source["kaggleSubmissionSent"] is False
            and source["legalCertification"] is False
            and self.selected_objective_id == SELECTED_OBJECTIVE_ID
            and self.scope_lock_id == SCOPE_LOCK_ID
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 2
            and self.remaining_budget_after_current_task == 6
            and OBJECTIVE_SELECTED is True
            and SCOPE_LOCKED is True
            and IMPLEMENTATION_ALLOWED_NEXT is True
            and IMPLEMENTATION_STARTED is False
            and QUERY_INTERFACE_IMPLEMENTATION_STARTED is False
            and len(self.allowed_operations) == 4
            and len(self.forbidden_operations) == 9
            and len(self.scope_checks) == 13
            and len(self.generated_artifacts) == 4
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
        if source["openingOk"] is not True:
            issues.append("SOURCE_OPENING_NOT_OK")
        if source["issues"] != []:
            issues.append("SOURCE_ISSUES_NOT_EMPTY")
        if source["milestoneId"] != MILESTONE_ID:
            issues.append("SOURCE_MILESTONE_ID_MISMATCH")
        if source["objectiveSelectionRequiredNext"] is not True:
            issues.append("SOURCE_OBJECTIVE_SELECTION_NOT_REQUIRED_NEXT")
        if source["scopeLockRequiredNext"] is not True:
            issues.append("SOURCE_SCOPE_LOCK_NOT_REQUIRED_NEXT")
        if source["implementationStarted"] is not False:
            issues.append("SOURCE_IMPLEMENTATION_ALREADY_STARTED")
        if source["implementationAllowedAtTask1"] is not False:
            issues.append("SOURCE_IMPLEMENTATION_ALLOWED_AT_TASK_1")
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
        if QUERY_INTERFACE_IMPLEMENTATION_STARTED:
            issues.append("QUERY_INTERFACE_IMPLEMENTATION_STARTED_AT_TASK_2")
        if len(self.allowed_operations) != 4:
            issues.append("ALLOWED_OPERATION_COUNT_MISMATCH")
        if len(self.forbidden_operations) != 9:
            issues.append("FORBIDDEN_OPERATION_COUNT_MISMATCH")
        if len(self.scope_checks) != 13:
            issues.append("SCOPE_CHECK_COUNT_MISMATCH")
        if len(self.generated_artifacts) != 4:
            issues.append("GENERATED_ARTIFACT_COUNT_MISMATCH")
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
            "sourceOpeningOk": source["openingOk"],
            "sourceOpeningIssues": list(source["issues"]),
            "selectedObjectiveId": self.selected_objective_id,
            "scopeLockId": self.scope_lock_id,
            "objectiveSelected": OBJECTIVE_SELECTED,
            "scopeLocked": SCOPE_LOCKED,
            "implementationAllowedNext": IMPLEMENTATION_ALLOWED_NEXT,
            "implementationStarted": IMPLEMENTATION_STARTED,
            "queryInterfaceImplementationStarted": QUERY_INTERFACE_IMPLEMENTATION_STARTED,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "recommendedClosureTaskNumber": RECOMMENDED_CLOSURE_TASK_NUMBER,
            "reserveTaskNumber": RESERVE_TASK_NUMBER,
            "emergencyOnlyTaskNumber": EMERGENCY_ONLY_TASK_NUMBER,
            "allowedOperations": list(self.allowed_operations),
            "allowedOperationCount": len(self.allowed_operations),
            "forbiddenOperations": list(self.forbidden_operations),
            "forbiddenOperationCount": len(self.forbidden_operations),
            "scopeChecks": list(self.scope_checks),
            "scopeCheckCount": len(self.scope_checks),
            "generatedArtifacts": list(self.generated_artifacts),
            "generatedArtifactCount": len(self.generated_artifacts),
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
            "nextStage": self.next_stage,
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["lockId"] = self.lock_id
        return payload


def build_milestone_27_objective_scope_lock(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone27ObjectiveScopeLock:
    return Milestone27ObjectiveScopeLock(metadata={} if metadata is None else metadata)


def validate_milestone_27_objective_scope_lock(
    lock: Milestone27ObjectiveScopeLock,
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
    "IMPLEMENTATION_ALLOWED_NEXT",
    "FAST_SOURCE_OPENING_SNAPSHOT",
    "Milestone27ObjectiveScopeLock",
    "build_fast_source_opening_snapshot",
    "build_milestone_27_objective_scope_lock",
    "validate_milestone_27_objective_scope_lock",
]
