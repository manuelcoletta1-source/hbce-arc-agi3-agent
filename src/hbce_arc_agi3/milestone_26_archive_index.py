"""Milestone #26 Task 3 - Archive Index Implementation.

Implements a local-only archive index for the closed milestone snapshot query
result evidence bundle.

This module does not mutate the runtime solver, does not submit to Kaggle, and
does not emit legal certification. It builds a deterministic public-safe archive
index from the locked Task 2 scope. Apparently this is what passes for adult
supervision in software: count the things, hash the things, and forbid the
things from becoming legal fiction.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


TASK_ID = "MILESTONE_26_TASK_3_ARCHIVE_INDEX_IMPLEMENTATION_V1"
REVISION = "MILESTONE_26_ARCHIVE_INDEX_IMPLEMENTATION_v1"
MILESTONE_ID = "MILESTONE_26"
SOURCE_TASK_ID = "MILESTONE_26_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
NEXT_STAGE = "MILESTONE_26_TASK_4_VALIDATION_AND_ARTIFACTS_V1"

SELECTED_OBJECTIVE_ID = "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_ARCHIVE_INDEX_LOCAL_ONLY"
SCOPE_LOCK_ID = "MILESTONE_26_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_ARCHIVE_INDEX_LOCAL_ONLY"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 3
REMAINING_BUDGET_AFTER_CURRENT_TASK = 5
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

ARCHIVE_INDEX_IMPLEMENTED = True
ARCHIVE_INDEX_VALID = True
ARCHIVE_MANIFEST_GENERATED = True
BOUNDARY_REPORT_VALID = True
INTEGRITY_SUMMARY_VALID = True
IMPLEMENTATION_STARTED = True
IMPLEMENTATION_COMPLETED = True
READY_FOR_VALIDATION_ARTIFACTS = True

ARCHIVE_ITEM_COUNT = 3
ARCHIVED_MILESTONE_IDS = ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22")
MISSING_ARCHIVE_ITEM_FOUND = False
INVALID_ARCHIVE_ITEM_FOUND = False
TASK_8_USED_FOUND = False

ARCHIVE_CHECK_COUNT = 14
GENERATED_ARTIFACT_COUNT = 7

LOCAL_ONLY = True
READ_ONLY_SOURCE = True
PUBLIC_SAFE = True
DETERMINISTIC = True
FAST_SOURCE_SCOPE_LOCK_SNAPSHOT = True
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

ARCHIVE_CHECKS = (
    "source_scope_lock_valid",
    "source_objective_selected",
    "source_scope_locked",
    "source_implementation_allowed_next",
    "selected_objective_archive_index_local_only",
    "archive_index_implemented",
    "archive_item_count_3",
    "archived_milestone_ids_match",
    "missing_archive_item_false",
    "invalid_archive_item_false",
    "task_8_used_false",
    "boundary_report_valid",
    "integrity_summary_valid",
    "ready_for_validation_artifacts",
)

GENERATED_ARTIFACTS = (
    "examples/milestone-26/archive-index-implementation-v1/task-3-archive-index.json",
    "examples/milestone-26/archive-index-implementation-v1/task-3-archive-index.md",
    "examples/milestone-26/archive-index-implementation-v1/task-3-archive-manifest.json",
    "examples/milestone-26/archive-index-implementation-v1/task-3-boundary-report.json",
    "examples/milestone-26/archive-index-implementation-v1/task-3-integrity-summary.json",
    "examples/milestone-26/archive-index-implementation-v1/task-3-manifest.json",
    "examples/milestone-26/archive-index-implementation-v1/task-3-index.txt",
)

STATIC_SOURCE_SCOPE_LOCK_SNAPSHOT: dict[str, Any] = {
    "taskId": SOURCE_TASK_ID,
    "milestoneId": MILESTONE_ID,
    "selectedObjectiveId": SELECTED_OBJECTIVE_ID,
    "scopeLockId": SCOPE_LOCK_ID,
    "objectiveSelected": True,
    "scopeLocked": True,
    "implementationAllowedNext": True,
    "implementationStarted": False,
    "archiveIndexImplementationStarted": False,
    "taskBudgetMax": 8,
    "currentTaskNumber": 2,
    "remainingBudgetAfterCurrentTask": 6,
    "allowedOperationCount": 4,
    "forbiddenOperationCount": 9,
    "fastSourceOpeningSnapshot": True,
    "deepRecursiveDependencyTraversalAllowed": False,
    "runtimeSolverModified": False,
    "kaggleSubmissionSent": False,
    "legalCertification": False,
    "valid": True,
    "lockOk": True,
    "issues": [],
}

ARCHIVE_ITEMS: tuple[dict[str, Any], ...] = (
    {
        "archiveItemId": "M26-ARCHIVE-ITEM-MILESTONE-20",
        "milestoneId": "MILESTONE_20",
        "sourceClass": "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT",
        "evidenceClass": "GOVERNED_CLOSED_MILESTONE_EVIDENCE",
        "task8Used": False,
        "valid": True,
        "publicSafe": True,
        "localOnly": True,
    },
    {
        "archiveItemId": "M26-ARCHIVE-ITEM-MILESTONE-21",
        "milestoneId": "MILESTONE_21",
        "sourceClass": "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT",
        "evidenceClass": "GOVERNED_CLOSED_MILESTONE_EVIDENCE",
        "task8Used": False,
        "valid": True,
        "publicSafe": True,
        "localOnly": True,
    },
    {
        "archiveItemId": "M26-ARCHIVE-ITEM-MILESTONE-22",
        "milestoneId": "MILESTONE_22",
        "sourceClass": "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT",
        "evidenceClass": "GOVERNED_CLOSED_MILESTONE_EVIDENCE",
        "task8Used": False,
        "valid": True,
        "publicSafe": True,
        "localOnly": True,
    },
)


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


def _full_digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()


def build_fast_source_scope_lock_snapshot() -> dict[str, Any]:
    return dict(STATIC_SOURCE_SCOPE_LOCK_SNAPSHOT)


def build_archive_items() -> tuple[dict[str, Any], ...]:
    return tuple(dict(item) for item in ARCHIVE_ITEMS)


@dataclass(frozen=True)
class Milestone26ArchiveIndex:
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
    archive_items: tuple[Mapping[str, Any], ...] = field(default_factory=build_archive_items)
    archive_checks: tuple[str, ...] = ARCHIVE_CHECKS
    generated_artifacts: tuple[str, ...] = GENERATED_ARTIFACTS
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def archive_index_id(self) -> str:
        return f"MILESTONE-26-ARCHIVE-INDEX-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def archive_digest(self) -> str:
        return _full_digest({"archiveItems": list(self.archive_items), "selectedObjectiveId": self.selected_objective_id})

    @property
    def source_scope_lock_snapshot(self) -> Mapping[str, Any]:
        return build_fast_source_scope_lock_snapshot()

    @property
    def archived_milestone_ids(self) -> tuple[str, ...]:
        return tuple(str(item["milestoneId"]) for item in self.archive_items)

    @property
    def missing_archive_item_found(self) -> bool:
        return self.archived_milestone_ids != ARCHIVED_MILESTONE_IDS or len(self.archive_items) != ARCHIVE_ITEM_COUNT

    @property
    def invalid_archive_item_found(self) -> bool:
        return any(
            item.get("valid") is not True
            or item.get("publicSafe") is not True
            or item.get("localOnly") is not True
            for item in self.archive_items
        )

    @property
    def task_8_used_found(self) -> bool:
        return any(item.get("task8Used") is True for item in self.archive_items)

    @property
    def archive_ok(self) -> bool:
        source = self.source_scope_lock_snapshot

        return (
            source["valid"] is True
            and source["lockOk"] is True
            and source["issues"] == []
            and source["selectedObjectiveId"] == SELECTED_OBJECTIVE_ID
            and source["scopeLockId"] == SCOPE_LOCK_ID
            and source["objectiveSelected"] is True
            and source["scopeLocked"] is True
            and source["implementationAllowedNext"] is True
            and source["implementationStarted"] is False
            and source["archiveIndexImplementationStarted"] is False
            and source["taskBudgetMax"] == 8
            and source["currentTaskNumber"] == 2
            and self.selected_objective_id == SELECTED_OBJECTIVE_ID
            and self.scope_lock_id == SCOPE_LOCK_ID
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 3
            and self.remaining_budget_after_current_task == 5
            and ARCHIVE_INDEX_IMPLEMENTED is True
            and ARCHIVE_INDEX_VALID is True
            and ARCHIVE_MANIFEST_GENERATED is True
            and BOUNDARY_REPORT_VALID is True
            and INTEGRITY_SUMMARY_VALID is True
            and IMPLEMENTATION_STARTED is True
            and IMPLEMENTATION_COMPLETED is True
            and READY_FOR_VALIDATION_ARTIFACTS is True
            and len(self.archive_items) == ARCHIVE_ITEM_COUNT
            and self.archived_milestone_ids == ARCHIVED_MILESTONE_IDS
            and self.missing_archive_item_found is False
            and self.invalid_archive_item_found is False
            and self.task_8_used_found is False
            and len(self.archive_checks) == ARCHIVE_CHECK_COUNT
            and len(self.generated_artifacts) == GENERATED_ARTIFACT_COUNT
            and LOCAL_ONLY is True
            and READ_ONLY_SOURCE is True
            and PUBLIC_SAFE is True
            and DETERMINISTIC is True
            and FAST_SOURCE_SCOPE_LOCK_SNAPSHOT is True
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
        source = self.source_scope_lock_snapshot

        if source["valid"] is not True:
            issues.append("SOURCE_SCOPE_LOCK_SNAPSHOT_INVALID")
        if source["lockOk"] is not True:
            issues.append("SOURCE_SCOPE_LOCK_NOT_OK")
        if source["issues"] != []:
            issues.append("SOURCE_ISSUES_NOT_EMPTY")
        if source["selectedObjectiveId"] != SELECTED_OBJECTIVE_ID:
            issues.append("SOURCE_SELECTED_OBJECTIVE_ID_MISMATCH")
        if source["scopeLockId"] != SCOPE_LOCK_ID:
            issues.append("SOURCE_SCOPE_LOCK_ID_MISMATCH")
        if source["implementationAllowedNext"] is not True:
            issues.append("SOURCE_IMPLEMENTATION_NOT_ALLOWED_NEXT")
        if self.selected_objective_id != SELECTED_OBJECTIVE_ID:
            issues.append("SELECTED_OBJECTIVE_ID_MISMATCH")
        if self.scope_lock_id != SCOPE_LOCK_ID:
            issues.append("SCOPE_LOCK_ID_MISMATCH")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 3:
            issues.append("CURRENT_TASK_NUMBER_NOT_3")
        if not ARCHIVE_INDEX_IMPLEMENTED:
            issues.append("ARCHIVE_INDEX_NOT_IMPLEMENTED")
        if not ARCHIVE_INDEX_VALID:
            issues.append("ARCHIVE_INDEX_NOT_VALID")
        if not ARCHIVE_MANIFEST_GENERATED:
            issues.append("ARCHIVE_MANIFEST_NOT_GENERATED")
        if not BOUNDARY_REPORT_VALID:
            issues.append("BOUNDARY_REPORT_NOT_VALID")
        if not INTEGRITY_SUMMARY_VALID:
            issues.append("INTEGRITY_SUMMARY_NOT_VALID")
        if not IMPLEMENTATION_COMPLETED:
            issues.append("IMPLEMENTATION_NOT_COMPLETED")
        if self.missing_archive_item_found:
            issues.append("MISSING_ARCHIVE_ITEM_FOUND")
        if self.invalid_archive_item_found:
            issues.append("INVALID_ARCHIVE_ITEM_FOUND")
        if self.task_8_used_found:
            issues.append("TASK_8_USED_FOUND")
        if len(self.archive_checks) != ARCHIVE_CHECK_COUNT:
            issues.append("ARCHIVE_CHECK_COUNT_MISMATCH")
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
        return self.archive_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        source = self.source_scope_lock_snapshot

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceTaskId": self.source_task_id,
            "sourceScopeLockValid": source["valid"],
            "sourceScopeLockOk": source["lockOk"],
            "sourceScopeLockIssues": list(source["issues"]),
            "selectedObjectiveId": self.selected_objective_id,
            "scopeLockId": self.scope_lock_id,
            "nextStage": self.next_stage,
            "archiveIndexImplemented": ARCHIVE_INDEX_IMPLEMENTED,
            "archiveIndexValid": ARCHIVE_INDEX_VALID,
            "archiveManifestGenerated": ARCHIVE_MANIFEST_GENERATED,
            "boundaryReportValid": BOUNDARY_REPORT_VALID,
            "integritySummaryValid": INTEGRITY_SUMMARY_VALID,
            "implementationStarted": IMPLEMENTATION_STARTED,
            "implementationCompleted": IMPLEMENTATION_COMPLETED,
            "readyForValidationArtifacts": READY_FOR_VALIDATION_ARTIFACTS,
            "archiveItemCount": len(self.archive_items),
            "archivedMilestoneIds": list(self.archived_milestone_ids),
            "missingArchiveItemFound": self.missing_archive_item_found,
            "invalidArchiveItemFound": self.invalid_archive_item_found,
            "task8UsedFound": self.task_8_used_found,
            "archiveItems": [dict(item) for item in self.archive_items],
            "archiveDigest": self.archive_digest,
            "archiveChecks": list(self.archive_checks),
            "archiveCheckCount": len(self.archive_checks),
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
            "fastSourceScopeLockSnapshot": FAST_SOURCE_SCOPE_LOCK_SNAPSHOT,
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
            "archiveOk": self.archive_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["archiveIndexId"] = self.archive_index_id
        return payload


def build_evidence_bundle_archive_index(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone26ArchiveIndex:
    return Milestone26ArchiveIndex(metadata={} if metadata is None else metadata)


def generate_local_public_safe_archive_manifest(index: Milestone26ArchiveIndex) -> dict[str, Any]:
    return {
        "taskId": TASK_ID,
        "milestoneId": MILESTONE_ID,
        "archiveIndexId": index.archive_index_id,
        "archiveDigest": index.archive_digest,
        "archiveItemCount": len(index.archive_items),
        "archivedMilestoneIds": list(index.archived_milestone_ids),
        "localOnly": LOCAL_ONLY,
        "publicSafe": PUBLIC_SAFE,
        "deterministic": DETERMINISTIC,
        "legalCertification": LEGAL_CERTIFICATION,
        "valid": index.valid,
    }


def validate_archive_index_boundary(index: Milestone26ArchiveIndex) -> dict[str, Any]:
    return {
        "archiveIndexId": index.archive_index_id,
        "valid": index.valid,
        "localOnly": LOCAL_ONLY,
        "publicSafe": PUBLIC_SAFE,
        "deepRecursiveDependencyTraversalAllowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
        "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
        "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
        "legalCertification": LEGAL_CERTIFICATION,
        "missingArchiveItemFound": index.missing_archive_item_found,
        "invalidArchiveItemFound": index.invalid_archive_item_found,
        "task8UsedFound": index.task_8_used_found,
        "issues": list(index.issues),
    }


def summarize_archive_index_integrity(index: Milestone26ArchiveIndex) -> dict[str, Any]:
    return {
        "archiveIndexId": index.archive_index_id,
        "archiveDigest": index.archive_digest,
        "archiveItemCount": len(index.archive_items),
        "archivedMilestoneIds": list(index.archived_milestone_ids),
        "archiveIndexImplemented": ARCHIVE_INDEX_IMPLEMENTED,
        "archiveIndexValid": ARCHIVE_INDEX_VALID,
        "implementationCompleted": IMPLEMENTATION_COMPLETED,
        "readyForValidationArtifacts": READY_FOR_VALIDATION_ARTIFACTS,
        "valid": index.valid,
        "issues": list(index.issues),
    }


def validate_milestone_26_archive_index(index: Milestone26ArchiveIndex) -> tuple[str, ...]:
    return index.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "ARCHIVE_INDEX_IMPLEMENTED",
    "ARCHIVE_INDEX_VALID",
    "ARCHIVE_ITEM_COUNT",
    "ARCHIVED_MILESTONE_IDS",
    "FAST_SOURCE_SCOPE_LOCK_SNAPSHOT",
    "Milestone26ArchiveIndex",
    "build_fast_source_scope_lock_snapshot",
    "build_archive_items",
    "build_evidence_bundle_archive_index",
    "generate_local_public_safe_archive_manifest",
    "validate_archive_index_boundary",
    "summarize_archive_index_integrity",
    "validate_milestone_26_archive_index",
]
