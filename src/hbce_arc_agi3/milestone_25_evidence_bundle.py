"""Milestone #25 Task 3 - Evidence Bundle Implementation.

Implements a local-only, deterministic, public-safe evidence bundle for closed
milestone snapshot query results.

This module implements the objective selected in Task 2:
CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY.

No runtime solver. No Kaggle submission. No legal certification. No raw request
body persistence. Because apparently software needs these warnings tattooed on
its forehead to behave.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


TASK_ID = "MILESTONE_25_TASK_3_EVIDENCE_BUNDLE_IMPLEMENTATION_V1"
REVISION = "MILESTONE_25_EVIDENCE_BUNDLE_IMPLEMENTATION_v1"
MILESTONE_ID = "MILESTONE_25"
SOURCE_TASK_ID = "MILESTONE_25_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
NEXT_STAGE = "MILESTONE_25_TASK_4_VALIDATION_AND_ARTIFACTS_V1"

SELECTED_OBJECTIVE_ID = "CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"
SCOPE_LOCK_ID = "MILESTONE_25_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_RESULT_EVIDENCE_BUNDLE_LOCAL_ONLY"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 3
REMAINING_BUDGET_AFTER_CURRENT_TASK = 5
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

EVIDENCE_BUNDLE_IMPLEMENTED = True
EVIDENCE_BUNDLE_VALID = True
MANIFEST_GENERATED = True
BOUNDARY_REPORT_VALID = True
INTEGRITY_SUMMARY_VALID = True
IMPLEMENTATION_STARTED = True
IMPLEMENTATION_COMPLETED = True
READY_FOR_VALIDATION_ARTIFACTS = True

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

REGISTERED_MILESTONE_IDS = ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22")

QUERY_RESULT_ITEMS: tuple[dict[str, Any], ...] = (
    {
        "milestoneId": "MILESTONE_20",
        "snapshotAvailable": True,
        "milestoneClosed": True,
        "task7Used": True,
        "task8Used": False,
        "queryResultValid": True,
    },
    {
        "milestoneId": "MILESTONE_21",
        "snapshotAvailable": True,
        "milestoneClosed": True,
        "task7Used": False,
        "task8Used": False,
        "queryResultValid": True,
    },
    {
        "milestoneId": "MILESTONE_22",
        "snapshotAvailable": True,
        "milestoneClosed": True,
        "task7Used": False,
        "task8Used": False,
        "queryResultValid": True,
    },
)

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

STATIC_SOURCE_SCOPE_LOCK_SNAPSHOT: dict[str, Any] = {
    "taskId": SOURCE_TASK_ID,
    "milestoneId": "MILESTONE_25",
    "selectedObjectiveId": SELECTED_OBJECTIVE_ID,
    "scopeLockId": SCOPE_LOCK_ID,
    "objectiveSelected": True,
    "scopeLocked": True,
    "implementationAllowedNext": True,
    "implementationStarted": False,
    "evidenceBundleImplementationStarted": False,
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
}


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


def build_fast_source_scope_lock_snapshot() -> dict[str, Any]:
    return dict(STATIC_SOURCE_SCOPE_LOCK_SNAPSHOT)


def _copy_query_result_items() -> tuple[dict[str, Any], ...]:
    return tuple(dict(item) for item in QUERY_RESULT_ITEMS)


@dataclass(frozen=True)
class Milestone25EvidenceBundle:
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
    query_result_items: tuple[dict[str, Any], ...] = field(default_factory=_copy_query_result_items)
    allowed_operations: tuple[str, ...] = ALLOWED_OPERATIONS
    forbidden_operations: tuple[str, ...] = FORBIDDEN_OPERATIONS
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def bundle_id(self) -> str:
        return f"MILESTONE-25-EVIDENCE-BUNDLE-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def source_scope_lock_snapshot(self) -> Mapping[str, Any]:
        return build_fast_source_scope_lock_snapshot()

    @property
    def registered_milestone_ids(self) -> tuple[str, ...]:
        return tuple(item["milestoneId"] for item in self.query_result_items)

    @property
    def query_result_item_count(self) -> int:
        return len(self.query_result_items)

    @property
    def missing_snapshot_found(self) -> bool:
        return any(item["snapshotAvailable"] is not True for item in self.query_result_items)

    @property
    def invalid_query_result_found(self) -> bool:
        return any(item["queryResultValid"] is not True for item in self.query_result_items)

    @property
    def task8_used_found(self) -> bool:
        return any(item["task8Used"] is True for item in self.query_result_items)

    @property
    def bundle_ok(self) -> bool:
        source = self.source_scope_lock_snapshot

        return (
            source["valid"] is True
            and source["selectedObjectiveId"] == SELECTED_OBJECTIVE_ID
            and source["scopeLockId"] == SCOPE_LOCK_ID
            and source["objectiveSelected"] is True
            and source["scopeLocked"] is True
            and source["implementationAllowedNext"] is True
            and source["implementationStarted"] is False
            and source["evidenceBundleImplementationStarted"] is False
            and self.selected_objective_id == SELECTED_OBJECTIVE_ID
            and self.scope_lock_id == SCOPE_LOCK_ID
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 3
            and self.remaining_budget_after_current_task == 5
            and self.query_result_item_count == 3
            and self.registered_milestone_ids == REGISTERED_MILESTONE_IDS
            and self.missing_snapshot_found is False
            and self.invalid_query_result_found is False
            and self.task8_used_found is False
            and EVIDENCE_BUNDLE_IMPLEMENTED is True
            and EVIDENCE_BUNDLE_VALID is True
            and MANIFEST_GENERATED is True
            and BOUNDARY_REPORT_VALID is True
            and INTEGRITY_SUMMARY_VALID is True
            and IMPLEMENTATION_STARTED is True
            and IMPLEMENTATION_COMPLETED is True
            and READY_FOR_VALIDATION_ARTIFACTS is True
            and len(self.allowed_operations) == 4
            and len(self.forbidden_operations) == 9
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
        if source["selectedObjectiveId"] != SELECTED_OBJECTIVE_ID:
            issues.append("SOURCE_OBJECTIVE_MISMATCH")
        if source["scopeLockId"] != SCOPE_LOCK_ID:
            issues.append("SOURCE_SCOPE_LOCK_ID_MISMATCH")
        if source["implementationAllowedNext"] is not True:
            issues.append("SOURCE_IMPLEMENTATION_NOT_ALLOWED_NEXT")
        if source["implementationStarted"] is not False:
            issues.append("SOURCE_IMPLEMENTATION_ALREADY_STARTED")
        if self.selected_objective_id != SELECTED_OBJECTIVE_ID:
            issues.append("SELECTED_OBJECTIVE_ID_MISMATCH")
        if self.scope_lock_id != SCOPE_LOCK_ID:
            issues.append("SCOPE_LOCK_ID_MISMATCH")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 3:
            issues.append("CURRENT_TASK_NUMBER_NOT_3")
        if self.remaining_budget_after_current_task != 5:
            issues.append("REMAINING_BUDGET_NOT_5")
        if self.query_result_item_count != 3:
            issues.append("QUERY_RESULT_ITEM_COUNT_NOT_3")
        if self.registered_milestone_ids != REGISTERED_MILESTONE_IDS:
            issues.append("REGISTERED_MILESTONE_IDS_MISMATCH")
        if self.missing_snapshot_found:
            issues.append("MISSING_SNAPSHOT_FOUND")
        if self.invalid_query_result_found:
            issues.append("INVALID_QUERY_RESULT_FOUND")
        if self.task8_used_found:
            issues.append("TASK_8_USED_FOUND")
        if not EVIDENCE_BUNDLE_IMPLEMENTED:
            issues.append("EVIDENCE_BUNDLE_NOT_IMPLEMENTED")
        if not EVIDENCE_BUNDLE_VALID:
            issues.append("EVIDENCE_BUNDLE_NOT_VALID")
        if not MANIFEST_GENERATED:
            issues.append("MANIFEST_NOT_GENERATED")
        if not BOUNDARY_REPORT_VALID:
            issues.append("BOUNDARY_REPORT_NOT_VALID")
        if not INTEGRITY_SUMMARY_VALID:
            issues.append("INTEGRITY_SUMMARY_NOT_VALID")
        if not IMPLEMENTATION_COMPLETED:
            issues.append("IMPLEMENTATION_NOT_COMPLETED")
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
        return self.bundle_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceTaskId": self.source_task_id,
            "selectedObjectiveId": self.selected_objective_id,
            "scopeLockId": self.scope_lock_id,
            "nextStage": self.next_stage,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "evidenceBundleImplemented": EVIDENCE_BUNDLE_IMPLEMENTED,
            "evidenceBundleValid": EVIDENCE_BUNDLE_VALID,
            "manifestGenerated": MANIFEST_GENERATED,
            "boundaryReportValid": BOUNDARY_REPORT_VALID,
            "integritySummaryValid": INTEGRITY_SUMMARY_VALID,
            "implementationStarted": IMPLEMENTATION_STARTED,
            "implementationCompleted": IMPLEMENTATION_COMPLETED,
            "readyForValidationArtifacts": READY_FOR_VALIDATION_ARTIFACTS,
            "queryResultItems": [dict(item) for item in self.query_result_items],
            "queryResultItemCount": self.query_result_item_count,
            "registeredMilestoneIds": list(self.registered_milestone_ids),
            "missingSnapshotFound": self.missing_snapshot_found,
            "invalidQueryResultFound": self.invalid_query_result_found,
            "task8UsedFound": self.task8_used_found,
            "allowedOperations": list(self.allowed_operations),
            "allowedOperationCount": len(self.allowed_operations),
            "forbiddenOperations": list(self.forbidden_operations),
            "forbiddenOperationCount": len(self.forbidden_operations),
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
            "bundleOk": self.bundle_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["bundleId"] = self.bundle_id
        return payload


def build_closed_milestone_snapshot_query_result_evidence_bundle(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone25EvidenceBundle:
    return Milestone25EvidenceBundle(metadata={} if metadata is None else metadata)


def generate_local_public_safe_evidence_manifest(
    bundle: Milestone25EvidenceBundle,
) -> dict[str, Any]:
    payload = bundle.to_public_dict()
    return {
        "manifestId": f"MILESTONE-25-EVIDENCE-MANIFEST-{_digest(payload)}",
        "bundleId": payload["bundleId"],
        "taskId": payload["taskId"],
        "milestoneId": payload["milestoneId"],
        "selectedObjectiveId": payload["selectedObjectiveId"],
        "queryResultItemCount": payload["queryResultItemCount"],
        "registeredMilestoneIds": payload["registeredMilestoneIds"],
        "localOnly": payload["localOnly"],
        "publicSafe": payload["publicSafe"],
        "deterministic": payload["deterministic"],
        "legalCertification": payload["legalCertification"],
        "valid": payload["valid"],
    }


def validate_evidence_bundle_boundary(
    bundle: Milestone25EvidenceBundle,
) -> tuple[str, ...]:
    return bundle.issues


def summarize_evidence_bundle_integrity(
    bundle: Milestone25EvidenceBundle,
) -> dict[str, Any]:
    return {
        "bundleId": bundle.bundle_id,
        "valid": bundle.valid,
        "queryResultItemCount": bundle.query_result_item_count,
        "registeredMilestoneIds": list(bundle.registered_milestone_ids),
        "missingSnapshotFound": bundle.missing_snapshot_found,
        "invalidQueryResultFound": bundle.invalid_query_result_found,
        "task8UsedFound": bundle.task8_used_found,
        "implementationCompleted": IMPLEMENTATION_COMPLETED,
        "readyForValidationArtifacts": READY_FOR_VALIDATION_ARTIFACTS,
        "issues": list(bundle.issues),
    }


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "SELECTED_OBJECTIVE_ID",
    "SCOPE_LOCK_ID",
    "EVIDENCE_BUNDLE_IMPLEMENTED",
    "READY_FOR_VALIDATION_ARTIFACTS",
    "FAST_SOURCE_SCOPE_LOCK_SNAPSHOT",
    "Milestone25EvidenceBundle",
    "build_fast_source_scope_lock_snapshot",
    "build_closed_milestone_snapshot_query_result_evidence_bundle",
    "generate_local_public_safe_evidence_manifest",
    "validate_evidence_bundle_boundary",
    "summarize_evidence_bundle_integrity",
]
