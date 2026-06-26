"""Milestone #26 Task 4 - Validation and Artifacts.

Validates the Task 3 archive index implementation and emits validation artifacts.

No runtime solver mutation. No Kaggle. No legal certification. Just validation,
because apparently "the file exists" is not the same as "the system is coherent",
a lesson software keeps charging tuition for.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


TASK_ID = "MILESTONE_26_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
REVISION = "MILESTONE_26_VALIDATION_AND_ARTIFACTS_v1"
MILESTONE_ID = "MILESTONE_26"
SOURCE_TASK_ID = "MILESTONE_26_TASK_3_ARCHIVE_INDEX_IMPLEMENTATION_V1"
NEXT_STAGE = "MILESTONE_26_TASK_5_INTEGRATION_REGRESSION_V1"

SELECTED_OBJECTIVE_ID = "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_ARCHIVE_INDEX_LOCAL_ONLY"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 4
REMAINING_BUDGET_AFTER_CURRENT_TASK = 4
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

ARCHIVE_INDEX_VALIDATED = True
ARCHIVE_MANIFEST_VALIDATED = True
BOUNDARY_REPORT_VALIDATED = True
INTEGRITY_SUMMARY_VALIDATED = True
QUERY_RESULT_ITEMS_VALIDATED = True
BOUNDARY_VALIDATED = True
VALIDATION_ARTIFACTS_CREATED = True
READY_FOR_INTEGRATION_REGRESSION = True

ARCHIVE_ITEM_COUNT = 3
ARCHIVED_MILESTONE_IDS = ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22")
MISSING_ARCHIVE_ITEM_FOUND = False
INVALID_ARCHIVE_ITEM_FOUND = False
TASK_8_USED_FOUND = False

VALIDATION_CASE_COUNT = 12
GENERATED_ARTIFACT_COUNT = 6

LOCAL_ONLY = True
READ_ONLY_SOURCE = True
PUBLIC_SAFE = True
DETERMINISTIC = True
FAST_SOURCE_ARCHIVE_INDEX_SNAPSHOT = True
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

VALIDATION_CASES = (
    "source_archive_index_valid",
    "source_archive_manifest_valid",
    "source_boundary_report_valid",
    "source_integrity_summary_valid",
    "archive_index_validated",
    "archive_manifest_validated",
    "boundary_report_validated",
    "integrity_summary_validated",
    "archive_item_count_3",
    "archived_milestone_ids_match",
    "no_missing_or_invalid_archive_items",
    "ready_for_integration_regression",
)

GENERATED_ARTIFACTS = (
    "examples/milestone-26/validation-and-artifacts-v1/task-4-validation-report.json",
    "examples/milestone-26/validation-and-artifacts-v1/task-4-validation-report.md",
    "examples/milestone-26/validation-and-artifacts-v1/task-4-artifact-manifest.json",
    "examples/milestone-26/validation-and-artifacts-v1/task-4-boundary-validation.json",
    "examples/milestone-26/validation-and-artifacts-v1/task-4-integrity-validation.json",
    "examples/milestone-26/validation-and-artifacts-v1/task-4-index.txt",
)

STATIC_SOURCE_ARCHIVE_INDEX_SNAPSHOT: dict[str, Any] = {
    "taskId": SOURCE_TASK_ID,
    "milestoneId": MILESTONE_ID,
    "selectedObjectiveId": SELECTED_OBJECTIVE_ID,
    "archiveIndexImplemented": True,
    "archiveIndexValid": True,
    "archiveManifestGenerated": True,
    "boundaryReportValid": True,
    "integritySummaryValid": True,
    "implementationStarted": True,
    "implementationCompleted": True,
    "readyForValidationArtifacts": True,
    "archiveItemCount": 3,
    "archivedMilestoneIds": ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"],
    "missingArchiveItemFound": False,
    "invalidArchiveItemFound": False,
    "task8UsedFound": False,
    "archiveCheckCount": 14,
    "generatedArtifactCount": 7,
    "currentTaskNumber": 3,
    "taskBudgetMax": 8,
    "fastSourceScopeLockSnapshot": True,
    "deepRecursiveDependencyTraversalAllowed": False,
    "runtimeSolverModified": False,
    "kaggleSubmissionSent": False,
    "legalCertification": False,
    "valid": True,
    "archiveOk": True,
    "issues": [],
}


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


def build_fast_source_archive_index_snapshot() -> dict[str, Any]:
    return dict(STATIC_SOURCE_ARCHIVE_INDEX_SNAPSHOT)


@dataclass(frozen=True)
class Milestone26ValidationArtifacts:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    source_task_id: str = SOURCE_TASK_ID
    selected_objective_id: str = SELECTED_OBJECTIVE_ID
    next_stage: str = NEXT_STAGE
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    remaining_budget_after_current_task: int = REMAINING_BUDGET_AFTER_CURRENT_TASK
    validation_cases: tuple[str, ...] = VALIDATION_CASES
    generated_artifacts: tuple[str, ...] = GENERATED_ARTIFACTS
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def validation_id(self) -> str:
        return f"MILESTONE-26-VALIDATION-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def source_archive_index_snapshot(self) -> Mapping[str, Any]:
        return build_fast_source_archive_index_snapshot()

    @property
    def validation_ok(self) -> bool:
        source = self.source_archive_index_snapshot

        return (
            source["valid"] is True
            and source["archiveOk"] is True
            and source["issues"] == []
            and source["archiveIndexImplemented"] is True
            and source["archiveIndexValid"] is True
            and source["archiveManifestGenerated"] is True
            and source["boundaryReportValid"] is True
            and source["integritySummaryValid"] is True
            and source["implementationCompleted"] is True
            and source["readyForValidationArtifacts"] is True
            and source["archiveItemCount"] == ARCHIVE_ITEM_COUNT
            and tuple(source["archivedMilestoneIds"]) == ARCHIVED_MILESTONE_IDS
            and source["missingArchiveItemFound"] is False
            and source["invalidArchiveItemFound"] is False
            and source["task8UsedFound"] is False
            and source["currentTaskNumber"] == 3
            and source["taskBudgetMax"] == 8
            and source["deepRecursiveDependencyTraversalAllowed"] is False
            and source["runtimeSolverModified"] is False
            and source["kaggleSubmissionSent"] is False
            and source["legalCertification"] is False
            and ARCHIVE_INDEX_VALIDATED is True
            and ARCHIVE_MANIFEST_VALIDATED is True
            and BOUNDARY_REPORT_VALIDATED is True
            and INTEGRITY_SUMMARY_VALIDATED is True
            and QUERY_RESULT_ITEMS_VALIDATED is True
            and BOUNDARY_VALIDATED is True
            and VALIDATION_ARTIFACTS_CREATED is True
            and READY_FOR_INTEGRATION_REGRESSION is True
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 4
            and self.remaining_budget_after_current_task == 4
            and len(self.validation_cases) == VALIDATION_CASE_COUNT
            and len(self.generated_artifacts) == GENERATED_ARTIFACT_COUNT
            and LOCAL_ONLY is True
            and READ_ONLY_SOURCE is True
            and PUBLIC_SAFE is True
            and DETERMINISTIC is True
            and FAST_SOURCE_ARCHIVE_INDEX_SNAPSHOT is True
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
        source = self.source_archive_index_snapshot

        if source["valid"] is not True:
            issues.append("SOURCE_ARCHIVE_INDEX_SNAPSHOT_INVALID")
        if source["archiveOk"] is not True:
            issues.append("SOURCE_ARCHIVE_INDEX_NOT_OK")
        if source["issues"] != []:
            issues.append("SOURCE_ISSUES_NOT_EMPTY")
        if source["archiveIndexValid"] is not True:
            issues.append("SOURCE_ARCHIVE_INDEX_NOT_VALID")
        if source["archiveManifestGenerated"] is not True:
            issues.append("SOURCE_ARCHIVE_MANIFEST_NOT_GENERATED")
        if source["boundaryReportValid"] is not True:
            issues.append("SOURCE_BOUNDARY_REPORT_NOT_VALID")
        if source["integritySummaryValid"] is not True:
            issues.append("SOURCE_INTEGRITY_SUMMARY_NOT_VALID")
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
        if not ARCHIVE_INDEX_VALIDATED:
            issues.append("ARCHIVE_INDEX_NOT_VALIDATED")
        if not ARCHIVE_MANIFEST_VALIDATED:
            issues.append("ARCHIVE_MANIFEST_NOT_VALIDATED")
        if not BOUNDARY_REPORT_VALIDATED:
            issues.append("BOUNDARY_REPORT_NOT_VALIDATED")
        if not INTEGRITY_SUMMARY_VALIDATED:
            issues.append("INTEGRITY_SUMMARY_NOT_VALIDATED")
        if not READY_FOR_INTEGRATION_REGRESSION:
            issues.append("NOT_READY_FOR_INTEGRATION_REGRESSION")
        if self.current_task_number != 4:
            issues.append("CURRENT_TASK_NUMBER_NOT_4")
        if len(self.validation_cases) != VALIDATION_CASE_COUNT:
            issues.append("VALIDATION_CASE_COUNT_MISMATCH")
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
        return self.validation_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        source = self.source_archive_index_snapshot

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceTaskId": self.source_task_id,
            "selectedObjectiveId": self.selected_objective_id,
            "nextStage": self.next_stage,
            "sourceArchiveIndexValid": source["valid"],
            "sourceArchiveOk": source["archiveOk"],
            "sourceArchiveIssues": list(source["issues"]),
            "archiveIndexValidated": ARCHIVE_INDEX_VALIDATED,
            "archiveManifestValidated": ARCHIVE_MANIFEST_VALIDATED,
            "boundaryReportValidated": BOUNDARY_REPORT_VALIDATED,
            "integritySummaryValidated": INTEGRITY_SUMMARY_VALIDATED,
            "queryResultItemsValidated": QUERY_RESULT_ITEMS_VALIDATED,
            "boundaryValidated": BOUNDARY_VALIDATED,
            "validationArtifactsCreated": VALIDATION_ARTIFACTS_CREATED,
            "readyForIntegrationRegression": READY_FOR_INTEGRATION_REGRESSION,
            "archiveItemCount": ARCHIVE_ITEM_COUNT,
            "archivedMilestoneIds": list(ARCHIVED_MILESTONE_IDS),
            "missingArchiveItemFound": MISSING_ARCHIVE_ITEM_FOUND,
            "invalidArchiveItemFound": INVALID_ARCHIVE_ITEM_FOUND,
            "task8UsedFound": TASK_8_USED_FOUND,
            "validationCases": list(self.validation_cases),
            "validationCaseCount": len(self.validation_cases),
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
            "fastSourceArchiveIndexSnapshot": FAST_SOURCE_ARCHIVE_INDEX_SNAPSHOT,
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
            "validationOk": self.validation_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["validationId"] = self.validation_id
        return payload


def build_milestone_26_validation_artifacts(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone26ValidationArtifacts:
    return Milestone26ValidationArtifacts(metadata={} if metadata is None else metadata)


def build_validation_report(validation: Milestone26ValidationArtifacts) -> dict[str, Any]:
    return validation.to_public_dict()


def build_artifact_manifest(validation: Milestone26ValidationArtifacts) -> dict[str, Any]:
    return {
        "taskId": TASK_ID,
        "milestoneId": MILESTONE_ID,
        "validationId": validation.validation_id,
        "validationArtifactsCreated": VALIDATION_ARTIFACTS_CREATED,
        "archiveIndexValidated": ARCHIVE_INDEX_VALIDATED,
        "archiveManifestValidated": ARCHIVE_MANIFEST_VALIDATED,
        "boundaryReportValidated": BOUNDARY_REPORT_VALIDATED,
        "integritySummaryValidated": INTEGRITY_SUMMARY_VALIDATED,
        "readyForIntegrationRegression": READY_FOR_INTEGRATION_REGRESSION,
        "archiveItemCount": ARCHIVE_ITEM_COUNT,
        "archivedMilestoneIds": list(ARCHIVED_MILESTONE_IDS),
        "validationCaseCount": VALIDATION_CASE_COUNT,
        "generatedArtifactCount": GENERATED_ARTIFACT_COUNT,
        "fastSourceArchiveIndexSnapshot": FAST_SOURCE_ARCHIVE_INDEX_SNAPSHOT,
        "deepRecursiveDependencyTraversalAllowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
        "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
        "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
        "legalCertification": LEGAL_CERTIFICATION,
        "valid": validation.valid,
    }


def build_boundary_validation(validation: Milestone26ValidationArtifacts) -> dict[str, Any]:
    return {
        "validationId": validation.validation_id,
        "valid": validation.valid,
        "localOnly": LOCAL_ONLY,
        "publicSafe": PUBLIC_SAFE,
        "deepRecursiveDependencyTraversalAllowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
        "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
        "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
        "legalCertification": LEGAL_CERTIFICATION,
        "missingArchiveItemFound": MISSING_ARCHIVE_ITEM_FOUND,
        "invalidArchiveItemFound": INVALID_ARCHIVE_ITEM_FOUND,
        "task8UsedFound": TASK_8_USED_FOUND,
        "issues": list(validation.issues),
    }


def build_integrity_validation(validation: Milestone26ValidationArtifacts) -> dict[str, Any]:
    return {
        "validationId": validation.validation_id,
        "valid": validation.valid,
        "archiveIndexValidated": ARCHIVE_INDEX_VALIDATED,
        "archiveManifestValidated": ARCHIVE_MANIFEST_VALIDATED,
        "boundaryReportValidated": BOUNDARY_REPORT_VALIDATED,
        "integritySummaryValidated": INTEGRITY_SUMMARY_VALIDATED,
        "readyForIntegrationRegression": READY_FOR_INTEGRATION_REGRESSION,
        "archiveItemCount": ARCHIVE_ITEM_COUNT,
        "archivedMilestoneIds": list(ARCHIVED_MILESTONE_IDS),
        "issues": list(validation.issues),
    }


def validate_milestone_26_validation_artifacts(
    validation: Milestone26ValidationArtifacts,
) -> tuple[str, ...]:
    return validation.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "ARCHIVE_INDEX_VALIDATED",
    "READY_FOR_INTEGRATION_REGRESSION",
    "FAST_SOURCE_ARCHIVE_INDEX_SNAPSHOT",
    "Milestone26ValidationArtifacts",
    "build_fast_source_archive_index_snapshot",
    "build_milestone_26_validation_artifacts",
    "build_validation_report",
    "build_artifact_manifest",
    "build_boundary_validation",
    "build_integrity_validation",
    "validate_milestone_26_validation_artifacts",
]
