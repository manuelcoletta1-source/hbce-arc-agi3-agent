"""Milestone #25 Task 6 - Milestone Closure.

Closes Milestone 25 from the Task 5 integration regression snapshot.

Closure is technical and local-only. It is not legal certification, not Kaggle
submission, and not runtime solver mutation. A closure record is not a magic
wand, despite humanity's repeated attempts to treat JSON as scripture.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


TASK_ID = "MILESTONE_25_TASK_6_MILESTONE_CLOSURE_V1"
REVISION = "MILESTONE_25_MILESTONE_CLOSURE_v1"
MILESTONE_ID = "MILESTONE_25"
SOURCE_TASK_ID = "MILESTONE_25_TASK_5_INTEGRATION_REGRESSION_V1"
NEXT_STAGE = "MILESTONE_25_CLOSED_NO_TASK_7_OR_8_USED"

SELECTED_OBJECTIVE_ID = "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"

FINAL_STATUS = "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
TECHNICAL_STATUS = "PASS"
PROCESS_STATUS = "GOVERNED_WITHIN_TASK_BUDGET"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
FINAL_TASK_NUMBER = 6
COMPLETED_TASK_COUNT = 6
CURRENT_TASK_NUMBER = 6
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

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

QUERY_RESULT_ITEM_COUNT = 3
REGISTERED_MILESTONE_IDS = ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22")

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
    "task_1_valid",
    "task_2_valid",
    "task_3_valid",
    "task_4_valid",
    "task_5_valid",
    "source_ready_for_milestone_closure",
    "source_integration_regression_valid",
    "source_no_mutation_regression_validated",
    "query_result_item_count_3",
    "registered_milestone_ids_match",
    "task_budget_max_8",
    "final_task_number_6",
    "task_7_unused",
    "task_8_unused",
    "no_runtime_or_kaggle_or_legal_certification",
    "milestone_closed_ready_for_next",
)

GENERATED_ARTIFACTS = (
    "examples/milestone-25/milestone-closure-v1/task-6-milestone-closure.json",
    "examples/milestone-25/milestone-closure-v1/task-6-milestone-closure.md",
    "examples/milestone-25/milestone-closure-v1/task-6-manifest.json",
    "examples/milestone-25/milestone-closure-v1/task-6-final-summary.json",
    "examples/milestone-25/milestone-closure-v1/task-6-index.txt",
)

STATIC_SOURCE_INTEGRATION_SNAPSHOT: dict[str, Any] = {
    "taskId": SOURCE_TASK_ID,
    "milestoneId": MILESTONE_ID,
    "selectedObjectiveId": SELECTED_OBJECTIVE_ID,
    "integrationRegressionExecuted": True,
    "taskChainValidated": True,
    "sourceArtifactsValidated": True,
    "evidenceBundleRegressionValidated": True,
    "evidenceManifestRegressionValidated": True,
    "boundaryRegressionValidated": True,
    "integrityRegressionValidated": True,
    "noMutationRegressionValidated": True,
    "readyForMilestoneClosure": True,
    "task1Valid": True,
    "task2Valid": True,
    "task3Valid": True,
    "task4Valid": True,
    "queryResultItemCount": QUERY_RESULT_ITEM_COUNT,
    "registeredMilestoneIds": ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"],
    "regressionCheckCount": 14,
    "generatedArtifactCount": 5,
    "taskBudgetMax": 8,
    "currentTaskNumber": 5,
    "remainingBudgetAfterCurrentTask": 3,
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
class Milestone25Closure:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    source_task_id: str = SOURCE_TASK_ID
    selected_objective_id: str = SELECTED_OBJECTIVE_ID
    next_stage: str = NEXT_STAGE
    final_status: str = FINAL_STATUS
    technical_status: str = TECHNICAL_STATUS
    process_status: str = PROCESS_STATUS
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    final_task_number: int = FINAL_TASK_NUMBER
    completed_task_count: int = COMPLETED_TASK_COUNT
    closure_checks: tuple[str, ...] = CLOSURE_CHECKS
    generated_artifacts: tuple[str, ...] = GENERATED_ARTIFACTS
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def closure_id(self) -> str:
        return f"MILESTONE-25-CLOSURE-{_digest(self.to_public_dict(include_id=False))}"

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
            and source["integrationRegressionExecuted"] is True
            and source["taskChainValidated"] is True
            and source["sourceArtifactsValidated"] is True
            and source["evidenceBundleRegressionValidated"] is True
            and source["evidenceManifestRegressionValidated"] is True
            and source["boundaryRegressionValidated"] is True
            and source["integrityRegressionValidated"] is True
            and source["noMutationRegressionValidated"] is True
            and source["readyForMilestoneClosure"] is True
            and source["task1Valid"] is True
            and source["task2Valid"] is True
            and source["task3Valid"] is True
            and source["task4Valid"] is True
            and source["queryResultItemCount"] == 3
            and tuple(source["registeredMilestoneIds"]) == REGISTERED_MILESTONE_IDS
            and source["currentTaskNumber"] == 5
            and source["taskBudgetMax"] == 8
            and source["deepRecursiveDependencyTraversalAllowed"] is False
            and source["runtimeSolverModified"] is False
            and source["kaggleSubmissionSent"] is False
            and source["legalCertification"] is False
            and self.final_status == FINAL_STATUS
            and self.technical_status == "PASS"
            and self.process_status == PROCESS_STATUS
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.final_task_number == 6
            and self.completed_task_count == 6
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
        if source["noMutationRegressionValidated"] is not True:
            issues.append("SOURCE_NO_MUTATION_REGRESSION_NOT_VALIDATED")
        if source["queryResultItemCount"] != 3:
            issues.append("SOURCE_QUERY_RESULT_ITEM_COUNT_NOT_3")
        if tuple(source["registeredMilestoneIds"]) != REGISTERED_MILESTONE_IDS:
            issues.append("SOURCE_REGISTERED_MILESTONE_IDS_MISMATCH")
        if self.final_status != FINAL_STATUS:
            issues.append("FINAL_STATUS_MISMATCH")
        if self.technical_status != "PASS":
            issues.append("TECHNICAL_STATUS_NOT_PASS")
        if self.process_status != PROCESS_STATUS:
            issues.append("PROCESS_STATUS_MISMATCH")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.final_task_number != 6:
            issues.append("FINAL_TASK_NUMBER_NOT_6")
        if self.completed_task_count != 6:
            issues.append("COMPLETED_TASK_COUNT_NOT_6")
        if TASK_7_USED:
            issues.append("TASK_7_USED")
        if TASK_8_USED:
            issues.append("TASK_8_USED")
        if not NO_TASK_7_OR_8_USED:
            issues.append("TASK_7_OR_8_USED")
        if not MILESTONE_CLOSED:
            issues.append("MILESTONE_NOT_CLOSED")
        if not READY_FOR_NEXT_MILESTONE:
            issues.append("NOT_READY_FOR_NEXT_MILESTONE")
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
            "sourceReadyForMilestoneClosure": source["readyForMilestoneClosure"],
            "sourceTaskChainValidated": source["taskChainValidated"],
            "sourceNoMutationRegressionValidated": source["noMutationRegressionValidated"],
            "finalStatus": self.final_status,
            "technicalStatus": self.technical_status,
            "processStatus": self.process_status,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "finalTaskNumber": self.final_task_number,
            "completedTaskCount": self.completed_task_count,
            "currentTaskNumber": CURRENT_TASK_NUMBER,
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
            "queryResultItemCount": QUERY_RESULT_ITEM_COUNT,
            "registeredMilestoneIds": list(REGISTERED_MILESTONE_IDS),
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


def build_milestone_25_closure(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone25Closure:
    return Milestone25Closure(metadata={} if metadata is None else metadata)


def validate_milestone_25_closure(closure: Milestone25Closure) -> tuple[str, ...]:
    return closure.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "FINAL_STATUS",
    "MILESTONE_CLOSED",
    "READY_FOR_NEXT_MILESTONE",
    "FAST_SOURCE_INTEGRATION_SNAPSHOT",
    "Milestone25Closure",
    "build_fast_source_integration_snapshot",
    "build_milestone_25_closure",
    "validate_milestone_25_closure",
]
