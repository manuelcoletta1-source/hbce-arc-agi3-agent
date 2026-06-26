"""Milestone #26 Task 1 - Governed Opening With Task Budget.

Opens Milestone 26 from the closed Milestone 25 snapshot.

This task only opens the milestone and locks the task budget. It does not select
the objective and does not start implementation. Humanity keeps wanting to skip
this step, and then acts surprised when software turns into soup.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


TASK_ID = "MILESTONE_26_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
REVISION = "MILESTONE_26_GOVERNED_OPENING_WITH_TASK_BUDGET_v1"
MILESTONE_ID = "MILESTONE_26"
SOURCE_MILESTONE_ID = "MILESTONE_25"
SOURCE_TASK_ID = "MILESTONE_25_TASK_6_MILESTONE_CLOSURE_V1"
NEXT_STAGE = "MILESTONE_26_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"

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

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 1
REMAINING_BUDGET_AFTER_CURRENT_TASK = 7
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

GOVERNED_OPENING_READY = True
TASK_BUDGET_LOCKED = True
OBJECTIVE_SELECTION_REQUIRED_NEXT = True
SCOPE_LOCK_REQUIRED_NEXT = True
IMPLEMENTATION_STARTED = False
IMPLEMENTATION_ALLOWED_AT_TASK_1 = False

OPENING_CHECK_COUNT = 13
GENERATED_ARTIFACT_COUNT = 4

LOCAL_ONLY = True
READ_ONLY_SOURCE = True
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
    "source_milestone_25_closed",
    "source_final_status_closed_at_task_6",
    "source_technical_status_pass",
    "source_process_status_governed",
    "source_task_7_unused",
    "source_task_8_unused",
    "source_ready_for_next_milestone",
    "task_budget_min_4",
    "task_budget_max_8",
    "current_task_number_1",
    "objective_selection_required_next",
    "implementation_not_started",
    "local_only_public_safe_no_kaggle_no_legal_certification",
)

GENERATED_ARTIFACTS = (
    "examples/milestone-26/governed-opening-with-task-budget-v1/task-1-governed-opening.json",
    "examples/milestone-26/governed-opening-with-task-budget-v1/task-1-governed-opening.md",
    "examples/milestone-26/governed-opening-with-task-budget-v1/task-1-manifest.json",
    "examples/milestone-26/governed-opening-with-task-budget-v1/task-1-index.txt",
)

STATIC_SOURCE_CLOSURE_SNAPSHOT: dict[str, Any] = {
    "taskId": SOURCE_TASK_ID,
    "milestoneId": SOURCE_MILESTONE_ID,
    "finalStatus": SOURCE_FINAL_STATUS,
    "technicalStatus": SOURCE_TECHNICAL_STATUS,
    "processStatus": SOURCE_PROCESS_STATUS,
    "taskBudgetMax": 8,
    "finalTaskNumber": 6,
    "completedTaskCount": 6,
    "task7Used": False,
    "task8Used": False,
    "reserveUnused": True,
    "emergencyReserveUnused": True,
    "noTask7Or8Used": True,
    "milestoneClosed": True,
    "readyForNextMilestone": True,
    "fastSourceIntegrationSnapshot": True,
    "deepRecursiveDependencyTraversalAllowed": False,
    "runtimeSolverModified": False,
    "kaggleSubmissionSent": False,
    "legalCertification": False,
    "valid": True,
    "closureOk": True,
    "issues": [],
}


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


def build_fast_source_closure_snapshot() -> dict[str, Any]:
    return dict(STATIC_SOURCE_CLOSURE_SNAPSHOT)


@dataclass(frozen=True)
class Milestone26GovernedOpening:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    source_milestone_id: str = SOURCE_MILESTONE_ID
    source_task_id: str = SOURCE_TASK_ID
    next_stage: str = NEXT_STAGE
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    remaining_budget_after_current_task: int = REMAINING_BUDGET_AFTER_CURRENT_TASK
    opening_checks: tuple[str, ...] = OPENING_CHECKS
    generated_artifacts: tuple[str, ...] = GENERATED_ARTIFACTS
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def opening_id(self) -> str:
        return f"MILESTONE-26-GOVERNED-OPENING-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def source_closure_snapshot(self) -> Mapping[str, Any]:
        return build_fast_source_closure_snapshot()

    @property
    def opening_ok(self) -> bool:
        source = self.source_closure_snapshot

        return (
            source["valid"] is True
            and source["closureOk"] is True
            and source["issues"] == []
            and source["milestoneId"] == SOURCE_MILESTONE_ID
            and source["finalStatus"] == SOURCE_FINAL_STATUS
            and source["technicalStatus"] == "PASS"
            and source["processStatus"] == SOURCE_PROCESS_STATUS
            and source["finalTaskNumber"] == 6
            and source["completedTaskCount"] == 6
            and source["task7Used"] is False
            and source["task8Used"] is False
            and source["noTask7Or8Used"] is True
            and source["milestoneClosed"] is True
            and source["readyForNextMilestone"] is True
            and source["deepRecursiveDependencyTraversalAllowed"] is False
            and source["runtimeSolverModified"] is False
            and source["kaggleSubmissionSent"] is False
            and source["legalCertification"] is False
            and self.milestone_id == "MILESTONE_26"
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 1
            and self.remaining_budget_after_current_task == 7
            and GOVERNED_OPENING_READY is True
            and TASK_BUDGET_LOCKED is True
            and OBJECTIVE_SELECTION_REQUIRED_NEXT is True
            and SCOPE_LOCK_REQUIRED_NEXT is True
            and IMPLEMENTATION_STARTED is False
            and IMPLEMENTATION_ALLOWED_AT_TASK_1 is False
            and len(self.opening_checks) == OPENING_CHECK_COUNT
            and len(self.generated_artifacts) == GENERATED_ARTIFACT_COUNT
            and LOCAL_ONLY is True
            and READ_ONLY_SOURCE is True
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
        if source["closureOk"] is not True:
            issues.append("SOURCE_CLOSURE_NOT_OK")
        if source["issues"] != []:
            issues.append("SOURCE_ISSUES_NOT_EMPTY")
        if source["milestoneId"] != SOURCE_MILESTONE_ID:
            issues.append("SOURCE_MILESTONE_ID_MISMATCH")
        if source["finalStatus"] != SOURCE_FINAL_STATUS:
            issues.append("SOURCE_FINAL_STATUS_MISMATCH")
        if source["technicalStatus"] != "PASS":
            issues.append("SOURCE_TECHNICAL_STATUS_NOT_PASS")
        if source["processStatus"] != SOURCE_PROCESS_STATUS:
            issues.append("SOURCE_PROCESS_STATUS_MISMATCH")
        if source["finalTaskNumber"] != 6:
            issues.append("SOURCE_FINAL_TASK_NUMBER_NOT_6")
        if source["completedTaskCount"] != 6:
            issues.append("SOURCE_COMPLETED_TASK_COUNT_NOT_6")
        if source["task7Used"] is not False:
            issues.append("SOURCE_TASK_7_USED")
        if source["task8Used"] is not False:
            issues.append("SOURCE_TASK_8_USED")
        if source["milestoneClosed"] is not True:
            issues.append("SOURCE_MILESTONE_NOT_CLOSED")
        if source["readyForNextMilestone"] is not True:
            issues.append("SOURCE_NOT_READY_FOR_NEXT_MILESTONE")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 1:
            issues.append("CURRENT_TASK_NUMBER_NOT_1")
        if not OBJECTIVE_SELECTION_REQUIRED_NEXT:
            issues.append("OBJECTIVE_SELECTION_NOT_REQUIRED_NEXT")
        if not SCOPE_LOCK_REQUIRED_NEXT:
            issues.append("SCOPE_LOCK_NOT_REQUIRED_NEXT")
        if IMPLEMENTATION_STARTED:
            issues.append("IMPLEMENTATION_STARTED_AT_TASK_1")
        if IMPLEMENTATION_ALLOWED_AT_TASK_1:
            issues.append("IMPLEMENTATION_ALLOWED_AT_TASK_1")
        if len(self.opening_checks) != OPENING_CHECK_COUNT:
            issues.append("OPENING_CHECK_COUNT_MISMATCH")
        if len(self.generated_artifacts) != GENERATED_ARTIFACT_COUNT:
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
        return self.opening_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        source = self.source_closure_snapshot

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceTaskId": self.source_task_id,
            "sourceMilestoneId": self.source_milestone_id,
            "sourceClosureValid": source["valid"],
            "sourceClosureOk": source["closureOk"],
            "sourceClosureIssues": list(source["issues"]),
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
            "nextStage": self.next_stage,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "recommendedClosureTaskNumber": RECOMMENDED_CLOSURE_TASK_NUMBER,
            "reserveTaskNumber": RESERVE_TASK_NUMBER,
            "emergencyOnlyTaskNumber": EMERGENCY_ONLY_TASK_NUMBER,
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
            "readOnlySource": READ_ONLY_SOURCE,
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


def build_milestone_26_governed_opening(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone26GovernedOpening:
    return Milestone26GovernedOpening(metadata={} if metadata is None else metadata)


def validate_milestone_26_governed_opening(
    opening: Milestone26GovernedOpening,
) -> tuple[str, ...]:
    return opening.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "GOVERNED_OPENING_READY",
    "TASK_BUDGET_LOCKED",
    "OBJECTIVE_SELECTION_REQUIRED_NEXT",
    "FAST_SOURCE_CLOSURE_SNAPSHOT",
    "Milestone26GovernedOpening",
    "build_fast_source_closure_snapshot",
    "build_milestone_26_governed_opening",
    "validate_milestone_26_governed_opening",
]
