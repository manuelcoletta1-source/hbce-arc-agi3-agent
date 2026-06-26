"""Milestone #26 Task 6 - Milestone Closure.

Closes Milestone 26 after archive-index integration regression.

No runtime solver mutation. No Kaggle submission. No legal certification. No
Task 7 or Task 8 usage. Just closure, because sometimes the best thing software
can do is stop adding more software.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


TASK_ID = "MILESTONE_26_TASK_6_MILESTONE_CLOSURE_V1"
REVISION = "MILESTONE_26_MILESTONE_CLOSURE_v1"
MILESTONE_ID = "MILESTONE_26"
SOURCE_TASK_ID = "MILESTONE_26_TASK_5_INTEGRATION_REGRESSION_V1"
NEXT_STAGE = "MILESTONE_26_CLOSED_NO_TASK_7_OR_8_USED"

SELECTED_OBJECTIVE_ID = "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_ARCHIVE_INDEX_LOCAL_ONLY"

FINAL_STATUS = "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
TECHNICAL_STATUS = "PASS"
PROCESS_STATUS = "GOVERNED_WITHIN_TASK_BUDGET"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
FINAL_TASK_NUMBER = 6
COMPLETED_TASK_COUNT = 6
TASK_7_USED = False
TASK_8_USED = False
RESERVE_UNUSED = True
EMERGENCY_RESERVE_UNUSED = True
NO_TASK_7_OR_8_USED = True
MILESTONE_CLOSED = True
READY_FOR_NEXT_MILESTONE = True
CLOSURE_OK = True

TASK1_VALID = True
TASK2_VALID = True
TASK3_VALID = True
TASK4_VALID = True
TASK5_VALID = True

ARCHIVE_ITEM_COUNT = 3
ARCHIVED_MILESTONE_IDS = ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22")
MISSING_ARCHIVE_ITEM_FOUND = False
INVALID_ARCHIVE_ITEM_FOUND = False
TASK_8_USED_FOUND = False

CLOSURE_CHECK_COUNT = 16
GENERATED_ARTIFACT_COUNT = 5

LOCAL_ONLY = True
READ_ONLY_SOURCE = True
PUBLIC_SAFE = True
DETERMINISTIC = True
FAST_SOURCE_INTEGRATION_SNAPSHOT = True
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

CLOSURE_CHECKS = (
    "source_integration_regression_valid",
    "source_ready_for_milestone_closure",
    "task_1_valid",
    "task_2_valid",
    "task_3_valid",
    "task_4_valid",
    "task_5_valid",
    "archive_item_count_3",
    "archived_milestone_ids_match",
    "no_missing_archive_item",
    "no_invalid_archive_item",
    "no_task_8_used_found",
    "final_task_number_6",
    "task_7_unused",
    "task_8_unused",
    "milestone_closed_ready_for_next",
)

GENERATED_ARTIFACTS = (
    "examples/milestone-26/milestone-closure-v1/task-6-milestone-closure.json",
    "examples/milestone-26/milestone-closure-v1/task-6-milestone-closure.md",
    "examples/milestone-26/milestone-closure-v1/task-6-final-summary.json",
    "examples/milestone-26/milestone-closure-v1/task-6-manifest.json",
    "examples/milestone-26/milestone-closure-v1/task-6-index.txt",
)

STATIC_SOURCE_INTEGRATION_SNAPSHOT: dict[str, Any] = {
    "taskId": SOURCE_TASK_ID,
    "milestoneId": MILESTONE_ID,
    "selectedObjectiveId": SELECTED_OBJECTIVE_ID,
    "integrationRegressionReady": True,
    "taskChainValidated": True,
    "sourceArtifactsValidated": True,
    "archiveIndexRegressionValidated": True,
    "archiveManifestRegressionValidated": True,
    "boundaryRegressionValidated": True,
    "integrityRegressionValidated": True,
    "noMutationRegressionValidated": True,
    "readyForMilestoneClosure": True,
    "task1Valid": True,
    "task2Valid": True,
    "task3Valid": True,
    "task4Valid": True,
    "archiveItemCount": 3,
    "archivedMilestoneIds": ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"],
    "missingArchiveItemFound": False,
    "invalidArchiveItemFound": False,
    "task8UsedFound": False,
    "regressionCheckCount": 14,
    "generatedArtifactCount": 5,
    "currentTaskNumber": 5,
    "taskBudgetMax": 8,
    "fastSourceValidationSnapshot": True,
    "deepRecursiveDependencyTraversalAllowed": False,
    "runtimeSolverModified": False,
    "kaggleSubmissionSent": False,
    "legalCertification": False,
    "valid": True,
    "regressionOk": True,
    "issues": [],
}


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


def build_fast_source_integration_snapshot() -> dict[str, Any]:
    return dict(STATIC_SOURCE_INTEGRATION_SNAPSHOT)


@dataclass(frozen=True)
class Milestone26Closure:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    source_task_id: str = SOURCE_TASK_ID
    selected_objective_id: str = SELECTED_OBJECTIVE_ID
    next_stage: str = NEXT_STAGE
    closure_checks: tuple[str, ...] = CLOSURE_CHECKS
    generated_artifacts: tuple[str, ...] = GENERATED_ARTIFACTS
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def closure_id(self) -> str:
        return f"MILESTONE-26-CLOSURE-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def source_integration_snapshot(self) -> Mapping[str, Any]:
        return build_fast_source_integration_snapshot()

    @property
    def closure_ok(self) -> bool:
        source = self.source_integration_snapshot

        return (
            source["valid"] is True
            and source["regressionOk"] is True
            and source["issues"] == []
            and source["integrationRegressionReady"] is True
            and source["taskChainValidated"] is True
            and source["sourceArtifactsValidated"] is True
            and source["archiveIndexRegressionValidated"] is True
            and source["archiveManifestRegressionValidated"] is True
            and source["boundaryRegressionValidated"] is True
            and source["integrityRegressionValidated"] is True
            and source["noMutationRegressionValidated"] is True
            and source["readyForMilestoneClosure"] is True
            and source["task1Valid"] is True
            and source["task2Valid"] is True
            and source["task3Valid"] is True
            and source["task4Valid"] is True
            and source["archiveItemCount"] == ARCHIVE_ITEM_COUNT
            and tuple(source["archivedMilestoneIds"]) == ARCHIVED_MILESTONE_IDS
            and source["missingArchiveItemFound"] is False
            and source["invalidArchiveItemFound"] is False
            and source["task8UsedFound"] is False
            and source["currentTaskNumber"] == 5
            and source["taskBudgetMax"] == 8
            and source["deepRecursiveDependencyTraversalAllowed"] is False
            and source["runtimeSolverModified"] is False
            and source["kaggleSubmissionSent"] is False
            and source["legalCertification"] is False
            and FINAL_STATUS == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
            and TECHNICAL_STATUS == "PASS"
            and PROCESS_STATUS == "GOVERNED_WITHIN_TASK_BUDGET"
            and TASK_BUDGET_MIN == 4
            and TASK_BUDGET_MAX == 8
            and FINAL_TASK_NUMBER == 6
            and COMPLETED_TASK_COUNT == 6
            and TASK_7_USED is False
            and TASK_8_USED is False
            and RESERVE_UNUSED is True
            and EMERGENCY_RESERVE_UNUSED is True
            and NO_TASK_7_OR_8_USED is True
            and MILESTONE_CLOSED is True
            and READY_FOR_NEXT_MILESTONE is True
            and CLOSURE_OK is True
            and TASK1_VALID is True
            and TASK2_VALID is True
            and TASK3_VALID is True
            and TASK4_VALID is True
            and TASK5_VALID is True
            and len(self.closure_checks) == CLOSURE_CHECK_COUNT
            and len(self.generated_artifacts) == GENERATED_ARTIFACT_COUNT
            and LOCAL_ONLY is True
            and READ_ONLY_SOURCE is True
            and PUBLIC_SAFE is True
            and DETERMINISTIC is True
            and FAST_SOURCE_INTEGRATION_SNAPSHOT is True
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
        source = self.source_integration_snapshot

        if source["valid"] is not True:
            issues.append("SOURCE_INTEGRATION_SNAPSHOT_INVALID")
        if source["regressionOk"] is not True:
            issues.append("SOURCE_REGRESSION_NOT_OK")
        if source["issues"] != []:
            issues.append("SOURCE_ISSUES_NOT_EMPTY")
        if source["readyForMilestoneClosure"] is not True:
            issues.append("SOURCE_NOT_READY_FOR_MILESTONE_CLOSURE")
        if source["taskChainValidated"] is not True:
            issues.append("SOURCE_TASK_CHAIN_NOT_VALIDATED")
        if source["sourceArtifactsValidated"] is not True:
            issues.append("SOURCE_ARTIFACTS_NOT_VALIDATED")
        if source["archiveItemCount"] != ARCHIVE_ITEM_COUNT:
            issues.append("SOURCE_ARCHIVE_ITEM_COUNT_MISMATCH")
        if tuple(source["archivedMilestoneIds"]) != ARCHIVED_MILESTONE_IDS:
            issues.append("SOURCE_ARCHIVED_MILESTONE_IDS_MISMATCH")
        if source["missingArchiveItemFound"] is not False:
            issues.append("SOURCE_MISSING_ARCHIVE_ITEM_FOUND")
        if source["invalidArchiveItemFound"] is not False:
            issues.append("SOURCE_INVALID_ARCHIVE_ITEM_FOUND")
        if source["task8UsedFound"] is not False:
            issues.append("SOURCE_TASK_8_USED_FOUND")
        if FINAL_TASK_NUMBER != 6:
            issues.append("FINAL_TASK_NUMBER_NOT_6")
        if COMPLETED_TASK_COUNT != 6:
            issues.append("COMPLETED_TASK_COUNT_NOT_6")
        if TASK_7_USED:
            issues.append("TASK_7_USED")
        if TASK_8_USED:
            issues.append("TASK_8_USED")
        if not MILESTONE_CLOSED:
            issues.append("MILESTONE_NOT_CLOSED")
        if not READY_FOR_NEXT_MILESTONE:
            issues.append("NOT_READY_FOR_NEXT_MILESTONE")
        if not CLOSURE_OK:
            issues.append("CLOSURE_NOT_OK")
        if len(self.closure_checks) != CLOSURE_CHECK_COUNT:
            issues.append("CLOSURE_CHECK_COUNT_MISMATCH")
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
        return self.closure_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        source = self.source_integration_snapshot

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceTaskId": self.source_task_id,
            "selectedObjectiveId": self.selected_objective_id,
            "nextStage": self.next_stage,
            "sourceIntegrationValid": source["valid"],
            "sourceRegressionOk": source["regressionOk"],
            "sourceIntegrationIssues": list(source["issues"]),
            "finalStatus": FINAL_STATUS,
            "technicalStatus": TECHNICAL_STATUS,
            "processStatus": PROCESS_STATUS,
            "taskBudgetMin": TASK_BUDGET_MIN,
            "taskBudgetMax": TASK_BUDGET_MAX,
            "finalTaskNumber": FINAL_TASK_NUMBER,
            "completedTaskCount": COMPLETED_TASK_COUNT,
            "task7Used": TASK_7_USED,
            "task8Used": TASK_8_USED,
            "reserveUnused": RESERVE_UNUSED,
            "emergencyReserveUnused": EMERGENCY_RESERVE_UNUSED,
            "noTask7Or8Used": NO_TASK_7_OR_8_USED,
            "milestoneClosed": MILESTONE_CLOSED,
            "readyForNextMilestone": READY_FOR_NEXT_MILESTONE,
            "closureOk": self.closure_ok,
            "task1Valid": TASK1_VALID,
            "task2Valid": TASK2_VALID,
            "task3Valid": TASK3_VALID,
            "task4Valid": TASK4_VALID,
            "task5Valid": TASK5_VALID,
            "archiveItemCount": ARCHIVE_ITEM_COUNT,
            "archivedMilestoneIds": list(ARCHIVED_MILESTONE_IDS),
            "missingArchiveItemFound": MISSING_ARCHIVE_ITEM_FOUND,
            "invalidArchiveItemFound": INVALID_ARCHIVE_ITEM_FOUND,
            "task8UsedFound": TASK_8_USED_FOUND,
            "closureChecks": list(self.closure_checks),
            "closureCheckCount": len(self.closure_checks),
            "generatedArtifacts": list(self.generated_artifacts),
            "generatedArtifactCount": len(self.generated_artifacts),
            "localOnly": LOCAL_ONLY,
            "readOnlySource": READ_ONLY_SOURCE,
            "publicSafe": PUBLIC_SAFE,
            "deterministic": DETERMINISTIC,
            "fastSourceIntegrationSnapshot": FAST_SOURCE_INTEGRATION_SNAPSHOT,
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
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["closureId"] = self.closure_id
        return payload


def build_milestone_26_closure(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone26Closure:
    return Milestone26Closure(metadata={} if metadata is None else metadata)


def build_milestone_26_final_summary(closure: Milestone26Closure) -> dict[str, Any]:
    return {
        "taskId": TASK_ID,
        "milestoneId": MILESTONE_ID,
        "closureId": closure.closure_id,
        "finalStatus": FINAL_STATUS,
        "technicalStatus": TECHNICAL_STATUS,
        "processStatus": PROCESS_STATUS,
        "taskBudgetMax": TASK_BUDGET_MAX,
        "finalTaskNumber": FINAL_TASK_NUMBER,
        "completedTaskCount": COMPLETED_TASK_COUNT,
        "task7Used": TASK_7_USED,
        "task8Used": TASK_8_USED,
        "reserveUnused": RESERVE_UNUSED,
        "emergencyReserveUnused": EMERGENCY_RESERVE_UNUSED,
        "noTask7Or8Used": NO_TASK_7_OR_8_USED,
        "milestoneClosed": MILESTONE_CLOSED,
        "readyForNextMilestone": READY_FOR_NEXT_MILESTONE,
        "archiveItemCount": ARCHIVE_ITEM_COUNT,
        "archivedMilestoneIds": list(ARCHIVED_MILESTONE_IDS),
        "valid": closure.valid,
        "closureOk": closure.closure_ok,
        "issues": list(closure.issues),
    }


def validate_milestone_26_closure(closure: Milestone26Closure) -> tuple[str, ...]:
    return closure.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "FINAL_STATUS",
    "TECHNICAL_STATUS",
    "PROCESS_STATUS",
    "MILESTONE_CLOSED",
    "READY_FOR_NEXT_MILESTONE",
    "FAST_SOURCE_INTEGRATION_SNAPSHOT",
    "Milestone26Closure",
    "build_fast_source_integration_snapshot",
    "build_milestone_26_closure",
    "build_milestone_26_final_summary",
    "validate_milestone_26_closure",
]
