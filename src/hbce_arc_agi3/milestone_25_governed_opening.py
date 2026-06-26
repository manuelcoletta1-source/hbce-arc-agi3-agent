"""Milestone #25 Task 1 - Governed Opening With Task Budget.

Opens Milestone 25 from the already closed Milestone 24 closure snapshot.

Task 1 only opens the milestone and establishes the governed task budget.
No implementation starts here. No runtime solver. No Kaggle. No legal
certification. No deep recursive ancestry walk.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


TASK_ID = "MILESTONE_25_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
REVISION = "MILESTONE_25_GOVERNED_OPENING_WITH_TASK_BUDGET_v1"
MILESTONE_ID = "MILESTONE_25"
SOURCE_MILESTONE_ID = "MILESTONE_24"
NEXT_STAGE = "MILESTONE_25_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 1
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

SOURCE_FINAL_STATUS = "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
SOURCE_TECHNICAL_STATUS = "PASS"
SOURCE_PROCESS_STATUS = "GOVERNED_WITHIN_TASK_BUDGET"
SOURCE_FINAL_TASK_NUMBER = 6
SOURCE_COMPLETED_TASK_COUNT = 6
SOURCE_TASK_7_USED = False
SOURCE_TASK_8_USED = False
SOURCE_NO_TASK_7_OR_8_USED = True
SOURCE_MILESTONE_CLOSED = True
SOURCE_READY_FOR_NEXT_MILESTONE = True
SOURCE_NEXT_STAGE = "MILESTONE_24_CLOSED_NO_TASK_7_OR_8_USED"

GOVERNED_OPENING_READY = True
TASK_BUDGET_LOCKED = True
OBJECTIVE_SELECTION_REQUIRED_NEXT = True
SCOPE_LOCK_REQUIRED_NEXT = True
IMPLEMENTATION_STARTED = False
IMPLEMENTATION_ALLOWED_AT_TASK_1 = False

LOCAL_ONLY = True
PUBLIC_SAFE = True
DETERMINISTIC = True
FAST_SOURCE_CLOSURE_SNAPSHOT = True
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

OPENING_CHECKS = (
    "source_milestone_24_closed",
    "source_final_status_closed_at_task_6",
    "source_task_7_unused",
    "source_task_8_unused",
    "task_budget_min_4",
    "task_budget_max_8",
    "current_task_number_1",
    "objective_selection_required_next",
    "scope_lock_required_next",
    "implementation_not_started",
    "deep_recursive_traversal_forbidden",
    "ready_for_task_2",
)

GENERATED_ARTIFACTS = (
    "examples/milestone-25/governed-opening-with-task-budget-v1/task-1-governed-opening.json",
    "examples/milestone-25/governed-opening-with-task-budget-v1/task-1-governed-opening.md",
    "examples/milestone-25/governed-opening-with-task-budget-v1/task-1-manifest.json",
    "examples/milestone-25/governed-opening-with-task-budget-v1/task-1-index.txt",
)

STATIC_SOURCE_CLOSURE_SNAPSHOT: dict[str, Any] = {
    "milestoneId": SOURCE_MILESTONE_ID,
    "finalStatus": SOURCE_FINAL_STATUS,
    "technicalStatus": SOURCE_TECHNICAL_STATUS,
    "processStatus": SOURCE_PROCESS_STATUS,
    "finalTaskNumber": SOURCE_FINAL_TASK_NUMBER,
    "completedTaskCount": SOURCE_COMPLETED_TASK_COUNT,
    "taskBudgetMax": 8,
    "task7Used": SOURCE_TASK_7_USED,
    "task8Used": SOURCE_TASK_8_USED,
    "noTask7Or8Used": SOURCE_NO_TASK_7_OR_8_USED,
    "milestoneClosed": SOURCE_MILESTONE_CLOSED,
    "readyForNextMilestone": SOURCE_READY_FOR_NEXT_MILESTONE,
    "nextStage": SOURCE_NEXT_STAGE,
    "sourceMode": "FAST_SOURCE_CLOSURE_SNAPSHOT",
    "legalCertification": False,
    "valid": True,
}


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


def build_fast_source_closure_snapshot() -> dict[str, Any]:
    return dict(STATIC_SOURCE_CLOSURE_SNAPSHOT)


@dataclass(frozen=True)
class Milestone25GovernedOpening:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    opening_checks: tuple[str, ...] = OPENING_CHECKS
    generated_artifacts: tuple[str, ...] = GENERATED_ARTIFACTS
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def opening_id(self) -> str:
        return f"MILESTONE-25-GOVERNED-OPENING-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def source_closure_snapshot(self) -> Mapping[str, Any]:
        return build_fast_source_closure_snapshot()

    @property
    def remaining_budget_after_current_task(self) -> int:
        return self.task_budget_max - self.current_task_number

    @property
    def opening_ok(self) -> bool:
        source = self.source_closure_snapshot
        return (
            source["valid"] is True
            and source["milestoneId"] == SOURCE_MILESTONE_ID
            and source["finalStatus"] == SOURCE_FINAL_STATUS
            and source["technicalStatus"] == "PASS"
            and source["processStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
            and source["finalTaskNumber"] == 6
            and source["task7Used"] is False
            and source["task8Used"] is False
            and source["noTask7Or8Used"] is True
            and source["milestoneClosed"] is True
            and source["readyForNextMilestone"] is True
            and GOVERNED_OPENING_READY is True
            and TASK_BUDGET_LOCKED is True
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 1
            and self.remaining_budget_after_current_task == 7
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and OBJECTIVE_SELECTION_REQUIRED_NEXT is True
            and SCOPE_LOCK_REQUIRED_NEXT is True
            and IMPLEMENTATION_STARTED is False
            and IMPLEMENTATION_ALLOWED_AT_TASK_1 is False
            and len(self.opening_checks) == 12
            and len(self.generated_artifacts) == 4
            and LOCAL_ONLY is True
            and PUBLIC_SAFE is True
            and DETERMINISTIC is True
            and FAST_SOURCE_CLOSURE_SNAPSHOT is True
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
        source = self.source_closure_snapshot

        if source["valid"] is not True:
            issues.append("SOURCE_CLOSURE_SNAPSHOT_INVALID")
        if source["milestoneId"] != SOURCE_MILESTONE_ID:
            issues.append("SOURCE_MILESTONE_ID_MISMATCH")
        if source["finalStatus"] != SOURCE_FINAL_STATUS:
            issues.append("SOURCE_FINAL_STATUS_MISMATCH")
        if source["task7Used"] is not False:
            issues.append("SOURCE_TASK_7_USED")
        if source["task8Used"] is not False:
            issues.append("SOURCE_TASK_8_USED")
        if source["milestoneClosed"] is not True:
            issues.append("SOURCE_MILESTONE_NOT_CLOSED")
        if self.task_budget_min != 4:
            issues.append("TASK_BUDGET_MIN_NOT_4")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 1:
            issues.append("CURRENT_TASK_NUMBER_NOT_1")
        if self.remaining_budget_after_current_task != 7:
            issues.append("REMAINING_BUDGET_NOT_7")
        if not OBJECTIVE_SELECTION_REQUIRED_NEXT:
            issues.append("OBJECTIVE_SELECTION_NOT_REQUIRED_NEXT")
        if not SCOPE_LOCK_REQUIRED_NEXT:
            issues.append("SCOPE_LOCK_NOT_REQUIRED_NEXT")
        if IMPLEMENTATION_STARTED:
            issues.append("IMPLEMENTATION_STARTED_AT_TASK_1")
        if IMPLEMENTATION_ALLOWED_AT_TASK_1:
            issues.append("IMPLEMENTATION_ALLOWED_AT_TASK_1")
        if len(self.opening_checks) != 12:
            issues.append("OPENING_CHECK_COUNT_NOT_12")
        if len(self.generated_artifacts) != 4:
            issues.append("GENERATED_ARTIFACT_COUNT_NOT_4")
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
        return self.opening_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        source = self.source_closure_snapshot
        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceMilestoneId": source["milestoneId"],
            "sourceFinalStatus": source["finalStatus"],
            "sourceTechnicalStatus": source["technicalStatus"],
            "sourceProcessStatus": source["processStatus"],
            "sourceFinalTaskNumber": source["finalTaskNumber"],
            "sourceCompletedTaskCount": source["completedTaskCount"],
            "sourceTask7Used": source["task7Used"],
            "sourceTask8Used": source["task8Used"],
            "sourceNoTask7Or8Used": source["noTask7Or8Used"],
            "sourceMilestoneClosed": source["milestoneClosed"],
            "sourceReadyForNextMilestone": source["readyForNextMilestone"],
            "sourceNextStage": source["nextStage"],
            "sourceMode": source["sourceMode"],
            "nextStage": self.next_stage,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "governedOpeningReady": GOVERNED_OPENING_READY,
            "taskBudgetLocked": TASK_BUDGET_LOCKED,
            "objectiveSelectionRequiredNext": OBJECTIVE_SELECTION_REQUIRED_NEXT,
            "scopeLockRequiredNext": SCOPE_LOCK_REQUIRED_NEXT,
            "implementationStarted": IMPLEMENTATION_STARTED,
            "implementationAllowedAtTask1": IMPLEMENTATION_ALLOWED_AT_TASK_1,
            "openingChecks": list(self.opening_checks),
            "openingCheckCount": len(self.opening_checks),
            "generatedArtifacts": list(self.generated_artifacts),
            "generatedArtifactCount": len(self.generated_artifacts),
            "localOnly": LOCAL_ONLY,
            "publicSafe": PUBLIC_SAFE,
            "deterministic": DETERMINISTIC,
            "fastSourceClosureSnapshot": FAST_SOURCE_CLOSURE_SNAPSHOT,
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
            "openingOk": self.opening_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["openingId"] = self.opening_id
        return payload


def build_milestone_25_governed_opening(*, metadata: Mapping[str, Any] | None = None) -> Milestone25GovernedOpening:
    return Milestone25GovernedOpening(metadata={} if metadata is None else metadata)


def validate_milestone_25_governed_opening(opening: Milestone25GovernedOpening) -> tuple[str, ...]:
    return opening.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "GOVERNED_OPENING_READY",
    "TASK_BUDGET_LOCKED",
    "FAST_SOURCE_CLOSURE_SNAPSHOT",
    "build_fast_source_closure_snapshot",
    "Milestone25GovernedOpening",
    "build_milestone_25_governed_opening",
    "validate_milestone_25_governed_opening",
]
