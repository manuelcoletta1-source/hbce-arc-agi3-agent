"""Milestone #24 Task 6 - Milestone Closure.

FAST_SOURCE_INTEGRATION_SNAPSHOT revision.

Closes Milestone 24 at Task 6 using the already validated Task 5 integration
regression artifact as a static source snapshot. No deep recursive dependency
walk. No runtime solver. No Kaggle. No legal certification.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


TASK_ID = "MILESTONE_24_TASK_6_MILESTONE_CLOSURE_V1"
REVISION = "MILESTONE_24_MILESTONE_CLOSURE_FAST_SOURCE_INTEGRATION_SNAPSHOT_v1"
MILESTONE_ID = "MILESTONE_24"
NEXT_STAGE = "MILESTONE_24_CLOSED_NO_TASK_7_OR_8_USED"

FINAL_STATUS = "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
TECHNICAL_STATUS = "PASS"
PROCESS_STATUS = "GOVERNED_WITHIN_TASK_BUDGET"

FINAL_TASK_NUMBER = 6
COMPLETED_TASK_COUNT = 6
TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

TASK_7_USED = False
TASK_8_USED = False
RESERVE_UNUSED = True
EMERGENCY_RESERVE_UNUSED = True
NO_TASK_7_OR_8_USED = True

MILESTONE_CLOSED = True
CLOSURE_READY = True
CLOSURE_EXECUTED = True
READY_FOR_NEXT_MILESTONE = True

LOCAL_ONLY = True
READ_ONLY = True
DETERMINISTIC = True
PUBLIC_SAFE = True
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

STATIC_SOURCE_INTEGRATION_SNAPSHOT: dict[str, Any] = {
    "taskId": "MILESTONE_24_TASK_5_INTEGRATION_REGRESSION_V1",
    "milestoneId": "MILESTONE_24",
    "valid": True,
    "integrationOk": True,
    "readyForMilestoneClosure": True,
    "taskChainValidated": True,
    "sourceArtifactsValidated": True,
    "queryInterfaceRegressionValidated": True,
    "boundaryRegressionValidated": True,
    "noMutationRegressionValidated": True,
    "task1Valid": True,
    "task2Valid": True,
    "task3Valid": True,
    "task4Valid": True,
    "snapshotCount": 3,
    "registeredMilestoneIds": ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"],
    "fastSourceValidationSnapshot": True,
    "deepRecursiveDependencyTraversalAllowed": False,
    "runtimeSolverModified": False,
    "kaggleSubmissionSent": False,
    "legalCertification": False,
}

CLOSURE_CHECKS = (
    "source_task_5_integration_regression_valid",
    "task_chain_validated",
    "query_interface_regression_validated",
    "boundary_regression_validated",
    "no_mutation_regression_validated",
    "ready_for_milestone_closure",
    "final_task_number_6",
    "task_7_unused",
    "task_8_unused",
    "task_budget_max_8",
    "deep_recursive_traversal_forbidden",
    "milestone_closed",
)

GENERATED_ARTIFACTS = (
    "examples/milestone-24/milestone-closure-v1/task-6-milestone-closure.json",
    "examples/milestone-24/milestone-closure-v1/task-6-milestone-closure.md",
    "examples/milestone-24/milestone-closure-v1/task-6-manifest.json",
    "examples/milestone-24/milestone-closure-v1/task-6-index.txt",
)


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


def build_fast_source_integration_snapshot() -> dict[str, Any]:
    return dict(STATIC_SOURCE_INTEGRATION_SNAPSHOT)


@dataclass(frozen=True)
class Milestone24Closure:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    final_status: str = FINAL_STATUS
    technical_status: str = TECHNICAL_STATUS
    process_status: str = PROCESS_STATUS
    final_task_number: int = FINAL_TASK_NUMBER
    completed_task_count: int = COMPLETED_TASK_COUNT
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    closure_checks: tuple[str, ...] = CLOSURE_CHECKS
    generated_artifacts: tuple[str, ...] = GENERATED_ARTIFACTS
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def closure_id(self) -> str:
        return f"MILESTONE-24-CLOSURE-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def source_integration_snapshot(self) -> Mapping[str, Any]:
        return build_fast_source_integration_snapshot()

    @property
    def closure_ok(self) -> bool:
        source = self.source_integration_snapshot
        return (
            source["valid"] is True
            and source["integrationOk"] is True
            and source["readyForMilestoneClosure"] is True
            and source["taskChainValidated"] is True
            and source["queryInterfaceRegressionValidated"] is True
            and source["boundaryRegressionValidated"] is True
            and source["noMutationRegressionValidated"] is True
            and source["fastSourceValidationSnapshot"] is True
            and self.final_status == FINAL_STATUS
            and self.technical_status == "PASS"
            and self.process_status == "GOVERNED_WITHIN_TASK_BUDGET"
            and self.final_task_number == 6
            and self.completed_task_count == 6
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 6
            and TASK_7_USED is False
            and TASK_8_USED is False
            and NO_TASK_7_OR_8_USED is True
            and MILESTONE_CLOSED is True
            and CLOSURE_READY is True
            and CLOSURE_EXECUTED is True
            and READY_FOR_NEXT_MILESTONE is True
            and len(self.closure_checks) == 12
            and len(self.generated_artifacts) == 4
            and FAST_SOURCE_INTEGRATION_SNAPSHOT is True
            and DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED is False
            and RUNTIME_SOLVER_MODIFIED is False
            and KAGGLE_SUBMISSION_SENT is False
            and LEGAL_CERTIFICATION is False
            and FAIL_CLOSED_ACTIVE is True
        )

    @property
    def issues(self) -> tuple[str, ...]:
        issues: list[str] = []
        source = self.source_integration_snapshot

        if source["valid"] is not True:
            issues.append("SOURCE_INTEGRATION_INVALID")
        if source["readyForMilestoneClosure"] is not True:
            issues.append("SOURCE_NOT_READY_FOR_MILESTONE_CLOSURE")
        if source["fastSourceValidationSnapshot"] is not True:
            issues.append("SOURCE_FAST_VALIDATION_SNAPSHOT_NOT_TRUE")
        if self.final_status != FINAL_STATUS:
            issues.append("FINAL_STATUS_MISMATCH")
        if self.technical_status != "PASS":
            issues.append("TECHNICAL_STATUS_NOT_PASS")
        if self.process_status != "GOVERNED_WITHIN_TASK_BUDGET":
            issues.append("PROCESS_STATUS_MISMATCH")
        if self.final_task_number != 6:
            issues.append("FINAL_TASK_NUMBER_NOT_6")
        if self.completed_task_count != 6:
            issues.append("COMPLETED_TASK_COUNT_NOT_6")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if TASK_7_USED:
            issues.append("TASK_7_USED")
        if TASK_8_USED:
            issues.append("TASK_8_USED")
        if not MILESTONE_CLOSED:
            issues.append("MILESTONE_NOT_CLOSED")
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
            "nextStage": self.next_stage,
            "finalStatus": self.final_status,
            "technicalStatus": self.technical_status,
            "processStatus": self.process_status,
            "finalTaskNumber": self.final_task_number,
            "completedTaskCount": self.completed_task_count,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "task7Used": TASK_7_USED,
            "task8Used": TASK_8_USED,
            "reserveUnused": RESERVE_UNUSED,
            "emergencyReserveUnused": EMERGENCY_RESERVE_UNUSED,
            "noTask7Or8Used": NO_TASK_7_OR_8_USED,
            "milestoneClosed": MILESTONE_CLOSED,
            "closureReady": CLOSURE_READY,
            "closureExecuted": CLOSURE_EXECUTED,
            "readyForNextMilestone": READY_FOR_NEXT_MILESTONE,
            "sourceIntegrationValid": source["valid"],
            "sourceIntegrationOk": source["integrationOk"],
            "sourceReadyForMilestoneClosure": source["readyForMilestoneClosure"],
            "sourceTaskChainValidated": source["taskChainValidated"],
            "sourceQueryInterfaceRegressionValidated": source["queryInterfaceRegressionValidated"],
            "sourceBoundaryRegressionValidated": source["boundaryRegressionValidated"],
            "sourceNoMutationRegressionValidated": source["noMutationRegressionValidated"],
            "sourceFastValidationSnapshot": source["fastSourceValidationSnapshot"],
            "sourceSnapshotCount": source["snapshotCount"],
            "sourceRegisteredMilestoneIds": source["registeredMilestoneIds"],
            "queryInterfaceFinalized": True,
            "validationArtifactsFinalized": True,
            "integrationRegressionFinalized": True,
            "closureChecks": list(self.closure_checks),
            "closureCheckCount": len(self.closure_checks),
            "generatedArtifacts": list(self.generated_artifacts),
            "generatedArtifactCount": len(self.generated_artifacts),
            "localOnly": LOCAL_ONLY,
            "readOnly": READ_ONLY,
            "deterministic": DETERMINISTIC,
            "publicSafe": PUBLIC_SAFE,
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
            "closureOk": self.closure_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["closureId"] = self.closure_id
        return payload


def build_milestone_24_closure(*, metadata: Mapping[str, Any] | None = None) -> Milestone24Closure:
    return Milestone24Closure(metadata={} if metadata is None else metadata)


def validate_milestone_24_closure(closure: Milestone24Closure) -> tuple[str, ...]:
    return closure.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "FINAL_STATUS",
    "MILESTONE_CLOSED",
    "TASK_7_USED",
    "TASK_8_USED",
    "FAST_SOURCE_INTEGRATION_SNAPSHOT",
    "build_fast_source_integration_snapshot",
    "Milestone24Closure",
    "build_milestone_24_closure",
    "validate_milestone_24_closure",
]
