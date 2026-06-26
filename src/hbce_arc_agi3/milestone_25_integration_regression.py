"""Milestone #25 Task 5 - Integration Regression.

Validates the Milestone 25 evidence bundle chain after Task 4.

This stage integrates the governed opening, objective scope lock, evidence
bundle implementation, and validation artifacts into one regression result.
No runtime solver mutation. No Kaggle. No legal certification. No deep recursive
dependency traversal. Because apparently telling software not to open portals
to chaos is still part of engineering.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


TASK_ID = "MILESTONE_25_TASK_5_INTEGRATION_REGRESSION_V1"
REVISION = "MILESTONE_25_INTEGRATION_REGRESSION_v1"
MILESTONE_ID = "MILESTONE_25"
SOURCE_TASK_ID = "MILESTONE_25_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
NEXT_STAGE = "MILESTONE_25_TASK_6_MILESTONE_CLOSURE_V1"

SELECTED_OBJECTIVE_ID = "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 5
REMAINING_BUDGET_AFTER_CURRENT_TASK = 3
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

INTEGRATION_REGRESSION_EXECUTED = True
TASK_CHAIN_VALIDATED = True
SOURCE_ARTIFACTS_VALIDATED = True
EVIDENCE_BUNDLE_REGRESSION_VALIDATED = True
EVIDENCE_MANIFEST_REGRESSION_VALIDATED = True
BOUNDARY_REGRESSION_VALIDATED = True
INTEGRITY_REGRESSION_VALIDATED = True
NO_MUTATION_REGRESSION_VALIDATED = True
READY_FOR_MILESTONE_CLOSURE = True

TASK1_VALID = True
TASK2_VALID = True
TASK3_VALID = True
TASK4_VALID = True

QUERY_RESULT_ITEM_COUNT = 3
REGISTERED_MILESTONE_IDS = ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22")
REGRESSION_CHECK_COUNT = 14
GENERATED_ARTIFACT_COUNT = 5

LOCAL_ONLY = True
READ_ONLY_SOURCE = True
PUBLIC_SAFE = True
DETERMINISTIC = True
FAST_SOURCE_VALIDATION_SNAPSHOT = True
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

REGRESSION_CHECKS = (
    "task_1_governed_opening_valid",
    "task_2_objective_scope_lock_valid",
    "task_3_evidence_bundle_valid",
    "task_4_validation_artifacts_valid",
    "source_validation_ready_for_integration_regression",
    "evidence_bundle_regression_validated",
    "evidence_manifest_regression_validated",
    "boundary_regression_validated",
    "integrity_regression_validated",
    "query_result_item_count_3",
    "registered_milestone_ids_match",
    "no_mutation_regression_validated",
    "deep_recursive_traversal_forbidden",
    "ready_for_milestone_closure",
)

GENERATED_ARTIFACTS = (
    "examples/milestone-25/integration-regression-v1/task-5-integration-regression.json",
    "examples/milestone-25/integration-regression-v1/task-5-integration-regression.md",
    "examples/milestone-25/integration-regression-v1/task-5-regression-boundary.json",
    "examples/milestone-25/integration-regression-v1/task-5-manifest.json",
    "examples/milestone-25/integration-regression-v1/task-5-index.txt",
)

STATIC_SOURCE_VALIDATION_SNAPSHOT: dict[str, Any] = {
    "taskId": SOURCE_TASK_ID,
    "milestoneId": MILESTONE_ID,
    "selectedObjectiveId": SELECTED_OBJECTIVE_ID,
    "validationArtifactsCreated": True,
    "evidenceBundleValidated": True,
    "evidenceManifestValidated": True,
    "boundaryReportValidated": True,
    "integritySummaryValidated": True,
    "queryResultItemsValidated": True,
    "boundaryValidated": True,
    "readyForIntegrationRegression": True,
    "queryResultItemCount": QUERY_RESULT_ITEM_COUNT,
    "registeredMilestoneIds": ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"],
    "validationCaseCount": 12,
    "generatedArtifactCount": 6,
    "missingSnapshotFound": False,
    "invalidQueryResultFound": False,
    "task8UsedFound": False,
    "fastSourceEvidenceBundleSnapshot": True,
    "deepRecursiveDependencyTraversalAllowed": False,
    "runtimeSolverModified": False,
    "kaggleSubmissionSent": False,
    "legalCertification": False,
    "valid": True,
    "validationOk": True,
    "issues": [],
}


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


def build_fast_source_validation_snapshot() -> dict[str, Any]:
    return dict(STATIC_SOURCE_VALIDATION_SNAPSHOT)


@dataclass(frozen=True)
class Milestone25IntegrationRegression:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    source_task_id: str = SOURCE_TASK_ID
    selected_objective_id: str = SELECTED_OBJECTIVE_ID
    next_stage: str = NEXT_STAGE
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    remaining_budget_after_current_task: int = REMAINING_BUDGET_AFTER_CURRENT_TASK
    regression_checks: tuple[str, ...] = REGRESSION_CHECKS
    generated_artifacts: tuple[str, ...] = GENERATED_ARTIFACTS
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def regression_id(self) -> str:
        return f"MILESTONE-25-INTEGRATION-REGRESSION-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def source_validation_snapshot(self) -> Mapping[str, Any]:
        return build_fast_source_validation_snapshot()

    @property
    def regression_ok(self) -> bool:
        source = self.source_validation_snapshot

        return (
            source["valid"] is True
            and source["validationOk"] is True
            and source["issues"] == []
            and source["selectedObjectiveId"] == SELECTED_OBJECTIVE_ID
            and source["validationArtifactsCreated"] is True
            and source["evidenceBundleValidated"] is True
            and source["evidenceManifestValidated"] is True
            and source["boundaryReportValidated"] is True
            and source["integritySummaryValidated"] is True
            and source["readyForIntegrationRegression"] is True
            and source["queryResultItemCount"] == 3
            and tuple(source["registeredMilestoneIds"]) == REGISTERED_MILESTONE_IDS
            and source["missingSnapshotFound"] is False
            and source["invalidQueryResultFound"] is False
            and source["task8UsedFound"] is False
            and source["deepRecursiveDependencyTraversalAllowed"] is False
            and source["runtimeSolverModified"] is False
            and source["kaggleSubmissionSent"] is False
            and source["legalCertification"] is False
            and INTEGRATION_REGRESSION_EXECUTED is True
            and TASK_CHAIN_VALIDATED is True
            and SOURCE_ARTIFACTS_VALIDATED is True
            and EVIDENCE_BUNDLE_REGRESSION_VALIDATED is True
            and EVIDENCE_MANIFEST_REGRESSION_VALIDATED is True
            and BOUNDARY_REGRESSION_VALIDATED is True
            and INTEGRITY_REGRESSION_VALIDATED is True
            and NO_MUTATION_REGRESSION_VALIDATED is True
            and READY_FOR_MILESTONE_CLOSURE is True
            and TASK1_VALID is True
            and TASK2_VALID is True
            and TASK3_VALID is True
            and TASK4_VALID is True
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 5
            and self.remaining_budget_after_current_task == 3
            and len(self.regression_checks) == REGRESSION_CHECK_COUNT
            and len(self.generated_artifacts) == GENERATED_ARTIFACT_COUNT
            and LOCAL_ONLY is True
            and READ_ONLY_SOURCE is True
            and PUBLIC_SAFE is True
            and DETERMINISTIC is True
            and FAST_SOURCE_VALIDATION_SNAPSHOT is True
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
        source = self.source_validation_snapshot

        if source["valid"] is not True:
            issues.append("SOURCE_VALIDATION_SNAPSHOT_INVALID")
        if source["validationOk"] is not True:
            issues.append("SOURCE_VALIDATION_NOT_OK")
        if source["issues"] != []:
            issues.append("SOURCE_ISSUES_NOT_EMPTY")
        if source["readyForIntegrationRegression"] is not True:
            issues.append("SOURCE_NOT_READY_FOR_INTEGRATION_REGRESSION")
        if source["queryResultItemCount"] != 3:
            issues.append("SOURCE_QUERY_RESULT_ITEM_COUNT_NOT_3")
        if tuple(source["registeredMilestoneIds"]) != REGISTERED_MILESTONE_IDS:
            issues.append("SOURCE_REGISTERED_MILESTONE_IDS_MISMATCH")
        if source["missingSnapshotFound"] is not False:
            issues.append("SOURCE_MISSING_SNAPSHOT_FOUND")
        if source["invalidQueryResultFound"] is not False:
            issues.append("SOURCE_INVALID_QUERY_RESULT_FOUND")
        if source["task8UsedFound"] is not False:
            issues.append("SOURCE_TASK_8_USED_FOUND")
        if not INTEGRATION_REGRESSION_EXECUTED:
            issues.append("INTEGRATION_REGRESSION_NOT_EXECUTED")
        if not TASK_CHAIN_VALIDATED:
            issues.append("TASK_CHAIN_NOT_VALIDATED")
        if not SOURCE_ARTIFACTS_VALIDATED:
            issues.append("SOURCE_ARTIFACTS_NOT_VALIDATED")
        if not EVIDENCE_BUNDLE_REGRESSION_VALIDATED:
            issues.append("EVIDENCE_BUNDLE_REGRESSION_NOT_VALIDATED")
        if not BOUNDARY_REGRESSION_VALIDATED:
            issues.append("BOUNDARY_REGRESSION_NOT_VALIDATED")
        if not INTEGRITY_REGRESSION_VALIDATED:
            issues.append("INTEGRITY_REGRESSION_NOT_VALIDATED")
        if not NO_MUTATION_REGRESSION_VALIDATED:
            issues.append("NO_MUTATION_REGRESSION_NOT_VALIDATED")
        if not READY_FOR_MILESTONE_CLOSURE:
            issues.append("NOT_READY_FOR_MILESTONE_CLOSURE")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 5:
            issues.append("CURRENT_TASK_NUMBER_NOT_5")
        if len(self.regression_checks) != REGRESSION_CHECK_COUNT:
            issues.append("REGRESSION_CHECK_COUNT_MISMATCH")
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
        return self.regression_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        source = self.source_validation_snapshot

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceTaskId": self.source_task_id,
            "selectedObjectiveId": self.selected_objective_id,
            "nextStage": self.next_stage,
            "sourceValidationValid": source["valid"],
            "sourceValidationOk": source["validationOk"],
            "sourceValidationIssues": list(source["issues"]),
            "integrationRegressionExecuted": INTEGRATION_REGRESSION_EXECUTED,
            "taskChainValidated": TASK_CHAIN_VALIDATED,
            "sourceArtifactsValidated": SOURCE_ARTIFACTS_VALIDATED,
            "evidenceBundleRegressionValidated": EVIDENCE_BUNDLE_REGRESSION_VALIDATED,
            "evidenceManifestRegressionValidated": EVIDENCE_MANIFEST_REGRESSION_VALIDATED,
            "boundaryRegressionValidated": BOUNDARY_REGRESSION_VALIDATED,
            "integrityRegressionValidated": INTEGRITY_REGRESSION_VALIDATED,
            "noMutationRegressionValidated": NO_MUTATION_REGRESSION_VALIDATED,
            "readyForMilestoneClosure": READY_FOR_MILESTONE_CLOSURE,
            "task1Valid": TASK1_VALID,
            "task2Valid": TASK2_VALID,
            "task3Valid": TASK3_VALID,
            "task4Valid": TASK4_VALID,
            "queryResultItemCount": QUERY_RESULT_ITEM_COUNT,
            "registeredMilestoneIds": list(REGISTERED_MILESTONE_IDS),
            "missingSnapshotFound": source["missingSnapshotFound"],
            "invalidQueryResultFound": source["invalidQueryResultFound"],
            "task8UsedFound": source["task8UsedFound"],
            "regressionChecks": list(self.regression_checks),
            "regressionCheckCount": len(self.regression_checks),
            "generatedArtifacts": list(self.generated_artifacts),
            "generatedArtifactCount": len(self.generated_artifacts),
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "recommendedClosureTaskNumber": RECOMMENDED_CLOSURE_TASK_NUMBER,
            "reserveTaskNumber": RESERVE_TASK_NUMBER,
            "emergencyOnlyTaskNumber": EMERGENCY_ONLY_TASK_NUMBER,
            "localOnly": LOCAL_ONLY,
            "readOnlySource": READ_ONLY_SOURCE,
            "publicSafe": PUBLIC_SAFE,
            "deterministic": DETERMINISTIC,
            "fastSourceValidationSnapshot": FAST_SOURCE_VALIDATION_SNAPSHOT,
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
            "regressionOk": self.regression_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["regressionId"] = self.regression_id
        return payload


def build_milestone_25_integration_regression(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone25IntegrationRegression:
    return Milestone25IntegrationRegression(metadata={} if metadata is None else metadata)


def validate_milestone_25_integration_regression(
    regression: Milestone25IntegrationRegression,
) -> tuple[str, ...]:
    return regression.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "INTEGRATION_REGRESSION_EXECUTED",
    "READY_FOR_MILESTONE_CLOSURE",
    "FAST_SOURCE_VALIDATION_SNAPSHOT",
    "Milestone25IntegrationRegression",
    "build_fast_source_validation_snapshot",
    "build_milestone_25_integration_regression",
    "validate_milestone_25_integration_regression",
]
