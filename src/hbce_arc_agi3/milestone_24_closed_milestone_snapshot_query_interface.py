"""Milestone #24 Task 3 - Closed Milestone Snapshot Query Interface.

Implements a deterministic local-only read/query layer over the closed milestone
snapshot registry facts produced by Milestone 23.

Supported operations:
- list_closed_milestone_snapshots
- get_closed_milestone_snapshot
- summarize_closed_milestone_snapshot
- validate_query_result_boundary

No mutation. No historical rewrite. No runtime solver. No Kaggle upload. No deep
recursive traversal. In other words, the code is allowed to read the ledger, not
start a small constitutional crisis in Python.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Iterable, Mapping

from hbce_arc_agi3.milestone_24_objective_scope_lock import (
    build_fast_source_opening_snapshot,
    build_milestone_24_objective_scope_lock,
    validate_milestone_24_objective_scope_lock,
)


TASK_ID = "MILESTONE_24_TASK_3_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_IMPLEMENTATION_V1"
REVISION = "MILESTONE_24_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_IMPLEMENTATION_v1"
MILESTONE_ID = "MILESTONE_24"
NEXT_STAGE = "MILESTONE_24_TASK_4_VALIDATION_AND_ARTIFACTS_V1"

SOURCE_SCOPE_LOCK_ID = "MILESTONE_24_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY"
SELECTED_OBJECTIVE_ID = "CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY"

QUERY_INTERFACE_READY = True
QUERY_INTERFACE_IMPLEMENTED = True
QUERY_INTERFACE_LOCAL_ONLY = True
QUERY_INTERFACE_READ_ONLY = True
QUERY_INTERFACE_DETERMINISTIC = True
QUERY_INTERFACE_BOUNDARY_VALIDATED = True

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 3
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

FAST_SOURCE_SCOPE_LOCK_SNAPSHOT = True
FAST_SNAPSHOT_DEPENDENCY_MODE = True
DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED = False
DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_FORBIDDEN = True

NO_RECURSIVE_META_LAYER = True
CLOSURE_REQUIRED = True

MAX_REVIEW_DEPTH = 1
MAX_AUTHORIZATION_DEPTH = 1
MAX_FINALIZATION_DEPTH = 1

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

ALLOWED_QUERY_OPERATIONS = (
    "list_closed_milestone_snapshots",
    "get_closed_milestone_snapshot",
    "summarize_closed_milestone_snapshot",
    "validate_query_result_boundary",
)

FORBIDDEN_OPERATIONS = (
    "mutate_closed_milestone_snapshot",
    "rewrite_historical_milestone",
    "deep_recursive_dependency_traversal",
    "runtime_solver_execution",
    "kaggle_submission",
)

REQUIRED_SNAPSHOT_FIELDS = (
    "milestoneId",
    "finalStatus",
    "technicalStatus",
    "processStatus",
    "taskBudgetMax",
    "finalTaskNumber",
    "task7Used",
    "task8Used",
    "milestoneClosed",
    "legalCertification",
)

STATIC_CLOSED_MILESTONE_SNAPSHOTS: tuple[dict[str, Any], ...] = (
    {
        "milestoneId": "MILESTONE_20",
        "finalStatus": "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_7",
        "technicalStatus": "PASS",
        "processStatus": "GOVERNED_WITHIN_TASK_BUDGET",
        "taskBudgetMax": 8,
        "finalTaskNumber": 7,
        "completedTaskCount": 7,
        "task7Used": True,
        "task8Used": False,
        "reserveUnused": False,
        "emergencyReserveUnused": True,
        "milestoneClosed": True,
        "scope": "governed_execution",
        "sourceMode": "STATIC_CLOSED_MILESTONE_SNAPSHOT",
        "legalCertification": False,
    },
    {
        "milestoneId": "MILESTONE_21",
        "finalStatus": "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6",
        "technicalStatus": "PASS",
        "processStatus": "GOVERNED_WITHIN_TASK_BUDGET",
        "taskBudgetMax": 8,
        "finalTaskNumber": 6,
        "completedTaskCount": 6,
        "task7Used": False,
        "task8Used": False,
        "reserveUnused": True,
        "emergencyReserveUnused": True,
        "milestoneClosed": True,
        "scope": "governed_handoff",
        "sourceMode": "STATIC_CLOSED_MILESTONE_SNAPSHOT",
        "legalCertification": False,
    },
    {
        "milestoneId": "MILESTONE_22",
        "finalStatus": "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6",
        "technicalStatus": "PASS",
        "processStatus": "GOVERNED_WITHIN_TASK_BUDGET",
        "taskBudgetMax": 8,
        "finalTaskNumber": 6,
        "completedTaskCount": 6,
        "task7Used": False,
        "task8Used": False,
        "reserveUnused": True,
        "emergencyReserveUnused": True,
        "milestoneClosed": True,
        "scope": "fast_snapshot_guard",
        "sourceMode": "STATIC_CLOSED_MILESTONE_SNAPSHOT",
        "legalCertification": False,
    },
)


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


def _snapshot_id(snapshot: Mapping[str, Any]) -> str:
    payload = {key: snapshot[key] for key in REQUIRED_SNAPSHOT_FIELDS}
    return f"{snapshot['milestoneId']}-QUERY-SNAPSHOT-{_digest(payload)}"


def _copy_snapshot(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    copied = dict(snapshot)
    copied["snapshotId"] = _snapshot_id(snapshot)
    copied["valid"] = validate_query_result_boundary(copied)["valid"]
    return copied


def _normalized_milestone_id(milestone_id: str) -> str:
    return milestone_id.strip().upper().replace("-", "_")


def validate_query_result_boundary(result: Mapping[str, Any]) -> dict[str, Any]:
    issues: list[str] = []

    for field_name in REQUIRED_SNAPSHOT_FIELDS:
        if field_name not in result:
            issues.append(f"MISSING_REQUIRED_FIELD:{field_name}")

    if result.get("milestoneClosed") is not True:
        issues.append("MILESTONE_NOT_CLOSED")
    if result.get("taskBudgetMax") != 8:
        issues.append("TASK_BUDGET_MAX_NOT_8")
    if result.get("task8Used") is not False:
        issues.append("TASK_8_USED")
    if result.get("legalCertification") is not False:
        issues.append("LEGAL_CERTIFICATION_NOT_FALSE")
    if result.get("sourceMode") not in (None, "STATIC_CLOSED_MILESTONE_SNAPSHOT"):
        issues.append("SOURCE_MODE_NOT_STATIC")
    if HISTORICAL_MILESTONE_REWRITE:
        issues.append("HISTORICAL_MILESTONE_REWRITE_ENABLED")
    if RUNTIME_SOLVER_MODIFIED:
        issues.append("RUNTIME_SOLVER_MODIFIED")
    if RUNTIME_WIRING_ALLOWED:
        issues.append("RUNTIME_WIRING_ALLOWED")
    if KAGGLE_SUBMISSION_SENT:
        issues.append("KAGGLE_SUBMISSION_SENT")
    if DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED:
        issues.append("DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED")

    return {
        "operation": "validate_query_result_boundary",
        "valid": issues == [],
        "issues": issues,
        "requiredFieldCount": len(REQUIRED_SNAPSHOT_FIELDS),
        "readOnly": QUERY_INTERFACE_READ_ONLY,
        "localOnly": QUERY_INTERFACE_LOCAL_ONLY,
        "legalCertification": LEGAL_CERTIFICATION,
    }


def list_closed_milestone_snapshots() -> tuple[dict[str, Any], ...]:
    return tuple(_copy_snapshot(snapshot) for snapshot in STATIC_CLOSED_MILESTONE_SNAPSHOTS)


def get_closed_milestone_snapshot(milestone_id: str) -> dict[str, Any]:
    normalized = _normalized_milestone_id(milestone_id)

    for snapshot in STATIC_CLOSED_MILESTONE_SNAPSHOTS:
        if snapshot["milestoneId"] == normalized:
            return {
                "operation": "get_closed_milestone_snapshot",
                "found": True,
                "milestoneId": normalized,
                "snapshot": _copy_snapshot(snapshot),
                "valid": True,
                "issues": [],
                "localOnly": QUERY_INTERFACE_LOCAL_ONLY,
                "readOnly": QUERY_INTERFACE_READ_ONLY,
                "legalCertification": LEGAL_CERTIFICATION,
            }

    return {
        "operation": "get_closed_milestone_snapshot",
        "found": False,
        "milestoneId": normalized,
        "snapshot": None,
        "valid": False,
        "issues": ["MILESTONE_SNAPSHOT_NOT_FOUND"],
        "localOnly": QUERY_INTERFACE_LOCAL_ONLY,
        "readOnly": QUERY_INTERFACE_READ_ONLY,
        "legalCertification": LEGAL_CERTIFICATION,
    }


def summarize_closed_milestone_snapshot(milestone_id: str) -> dict[str, Any]:
    query = get_closed_milestone_snapshot(milestone_id)
    if not query["found"]:
        return {
            "operation": "summarize_closed_milestone_snapshot",
            "found": False,
            "milestoneId": query["milestoneId"],
            "summary": "",
            "valid": False,
            "issues": list(query["issues"]),
            "localOnly": QUERY_INTERFACE_LOCAL_ONLY,
            "readOnly": QUERY_INTERFACE_READ_ONLY,
            "legalCertification": LEGAL_CERTIFICATION,
        }

    snapshot = query["snapshot"]
    summary = (
        f"{snapshot['milestoneId']} closed with {snapshot['finalStatus']}; "
        f"finalTaskNumber={snapshot['finalTaskNumber']}; "
        f"task7Used={str(snapshot['task7Used']).lower()}; "
        f"task8Used={str(snapshot['task8Used']).lower()}; "
        f"scope={snapshot['scope']}."
    )

    return {
        "operation": "summarize_closed_milestone_snapshot",
        "found": True,
        "milestoneId": snapshot["milestoneId"],
        "summary": summary,
        "valid": True,
        "issues": [],
        "localOnly": QUERY_INTERFACE_LOCAL_ONLY,
        "readOnly": QUERY_INTERFACE_READ_ONLY,
        "legalCertification": LEGAL_CERTIFICATION,
    }


@dataclass(frozen=True)
class Milestone24QueryInterfaceImplementation:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    allowed_query_operations: tuple[str, ...] = ALLOWED_QUERY_OPERATIONS
    forbidden_operations: tuple[str, ...] = FORBIDDEN_OPERATIONS
    required_snapshot_fields: tuple[str, ...] = REQUIRED_SNAPSHOT_FIELDS
    implementation_checks: tuple[str, ...] = (
        "source_scope_lock_valid",
        "selected_objective_matched",
        "list_operation_ready",
        "get_operation_ready",
        "summary_operation_ready",
        "boundary_validation_ready",
        "snapshot_count_3",
        "read_only_boundary_preserved",
        "local_only_boundary_preserved",
        "task_budget_max_8",
        "deep_recursive_traversal_forbidden",
        "ready_for_validation_artifacts",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def implementation_id(self) -> str:
        return f"MILESTONE-24-QUERY-INTERFACE-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def source_scope_lock_payload(self) -> Mapping[str, Any]:
        scope_lock = build_milestone_24_objective_scope_lock()
        return scope_lock.to_public_dict()

    @property
    def source_opening_snapshot(self) -> Mapping[str, Any]:
        return build_fast_source_opening_snapshot()

    @property
    def snapshots(self) -> tuple[dict[str, Any], ...]:
        return list_closed_milestone_snapshots()

    @property
    def implementation_ok(self) -> bool:
        scope_lock = build_milestone_24_objective_scope_lock()
        scope_payload = scope_lock.to_public_dict()
        snapshots = self.snapshots
        m20 = get_closed_milestone_snapshot("MILESTONE_20")
        m21 = get_closed_milestone_snapshot("MILESTONE_21")
        m22 = get_closed_milestone_snapshot("MILESTONE_22")
        missing = get_closed_milestone_snapshot("MILESTONE_999")
        summary = summarize_closed_milestone_snapshot("MILESTONE_22")

        return (
            QUERY_INTERFACE_READY is True
            and QUERY_INTERFACE_IMPLEMENTED is True
            and QUERY_INTERFACE_LOCAL_ONLY is True
            and QUERY_INTERFACE_READ_ONLY is True
            and QUERY_INTERFACE_DETERMINISTIC is True
            and QUERY_INTERFACE_BOUNDARY_VALIDATED is True
            and scope_lock.valid is True
            and validate_milestone_24_objective_scope_lock(scope_lock) == ()
            and scope_payload["valid"] is True
            and scope_payload["lockOk"] is True
            and scope_payload["scopeLockId"] == SOURCE_SCOPE_LOCK_ID
            and scope_payload["selectedObjectiveId"] == SELECTED_OBJECTIVE_ID
            and scope_payload["implementationAllowedNext"] is True
            and scope_payload["implementationStarted"] is False
            and scope_payload["queryInterfaceImplementationStarted"] is False
            and scope_payload["fastSourceOpeningSnapshot"] is True
            and len(snapshots) == 3
            and all(snapshot["valid"] is True for snapshot in snapshots)
            and m20["found"] is True
            and m20["snapshot"]["task7Used"] is True
            and m20["snapshot"]["task8Used"] is False
            and m21["found"] is True
            and m21["snapshot"]["task7Used"] is False
            and m22["found"] is True
            and m22["snapshot"]["task7Used"] is False
            and m22["snapshot"]["task8Used"] is False
            and missing["found"] is False
            and missing["valid"] is False
            and summary["found"] is True
            and "MILESTONE_22 closed" in summary["summary"]
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 3
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.allowed_query_operations) == 4
            and len(self.forbidden_operations) == 5
            and len(self.required_snapshot_fields) == 10
            and len(self.implementation_checks) == 12
            and FAST_SOURCE_SCOPE_LOCK_SNAPSHOT is True
            and FAST_SNAPSHOT_DEPENDENCY_MODE is True
            and DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED is False
            and DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_FORBIDDEN is True
            and NO_RECURSIVE_META_LAYER is True
            and CLOSURE_REQUIRED is True
            and MAX_REVIEW_DEPTH == 1
            and MAX_AUTHORIZATION_DEPTH == 1
            and MAX_FINALIZATION_DEPTH == 1
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
        scope_lock = build_milestone_24_objective_scope_lock()
        scope_payload = scope_lock.to_public_dict()
        snapshots = self.snapshots

        if not scope_lock.valid:
            issues.append("SOURCE_SCOPE_LOCK_INVALID")
        issues.extend(f"SOURCE_SCOPE_LOCK_{issue}" for issue in validate_milestone_24_objective_scope_lock(scope_lock))
        if scope_payload["scopeLockId"] != SOURCE_SCOPE_LOCK_ID:
            issues.append("SOURCE_SCOPE_LOCK_ID_MISMATCH")
        if scope_payload["selectedObjectiveId"] != SELECTED_OBJECTIVE_ID:
            issues.append("SOURCE_OBJECTIVE_ID_MISMATCH")
        if scope_payload["implementationAllowedNext"] is not True:
            issues.append("SOURCE_IMPLEMENTATION_NOT_ALLOWED_NEXT")
        if not QUERY_INTERFACE_READY:
            issues.append("QUERY_INTERFACE_NOT_READY")
        if not QUERY_INTERFACE_IMPLEMENTED:
            issues.append("QUERY_INTERFACE_NOT_IMPLEMENTED")
        if not QUERY_INTERFACE_LOCAL_ONLY:
            issues.append("QUERY_INTERFACE_NOT_LOCAL_ONLY")
        if not QUERY_INTERFACE_READ_ONLY:
            issues.append("QUERY_INTERFACE_NOT_READ_ONLY")
        if not QUERY_INTERFACE_DETERMINISTIC:
            issues.append("QUERY_INTERFACE_NOT_DETERMINISTIC")
        if len(snapshots) != 3:
            issues.append("SNAPSHOT_COUNT_NOT_3")
        for snapshot in snapshots:
            boundary = validate_query_result_boundary(snapshot)
            if not boundary["valid"]:
                issues.extend(f"{snapshot.get('milestoneId', 'UNKNOWN')}:{issue}" for issue in boundary["issues"])
        if self.task_budget_min != 4:
            issues.append("TASK_BUDGET_MIN_NOT_4")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 3:
            issues.append("CURRENT_TASK_NUMBER_NOT_3")
        if self.recommended_closure_task_number != 6:
            issues.append("RECOMMENDED_CLOSURE_TASK_NOT_6")
        if self.reserve_task_number != 7:
            issues.append("RESERVE_TASK_NUMBER_NOT_7")
        if self.emergency_only_task_number != 8:
            issues.append("EMERGENCY_TASK_NUMBER_NOT_8")
        if len(self.allowed_query_operations) != 4:
            issues.append("ALLOWED_QUERY_OPERATION_COUNT_NOT_4")
        if len(self.forbidden_operations) != 5:
            issues.append("FORBIDDEN_OPERATION_COUNT_NOT_5")
        if len(self.required_snapshot_fields) != 10:
            issues.append("REQUIRED_SNAPSHOT_FIELD_COUNT_NOT_10")
        if len(self.implementation_checks) != 12:
            issues.append("IMPLEMENTATION_CHECK_COUNT_NOT_12")
        if not FAST_SOURCE_SCOPE_LOCK_SNAPSHOT:
            issues.append("FAST_SOURCE_SCOPE_LOCK_SNAPSHOT_DISABLED")
        if not FAST_SNAPSHOT_DEPENDENCY_MODE:
            issues.append("FAST_SNAPSHOT_DEPENDENCY_MODE_DISABLED")
        if DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED:
            issues.append("DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED")
        if not DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_FORBIDDEN:
            issues.append("DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_NOT_FORBIDDEN")
        if not NO_RECURSIVE_META_LAYER:
            issues.append("RECURSIVE_META_LAYER_ALLOWED")
        if not CLOSURE_REQUIRED:
            issues.append("CLOSURE_NOT_REQUIRED")
        if MAX_REVIEW_DEPTH != 1:
            issues.append("MAX_REVIEW_DEPTH_NOT_1")
        if MAX_AUTHORIZATION_DEPTH != 1:
            issues.append("MAX_AUTHORIZATION_DEPTH_NOT_1")
        if MAX_FINALIZATION_DEPTH != 1:
            issues.append("MAX_FINALIZATION_DEPTH_NOT_1")
        if RUNTIME_SOLVER_MODIFIED:
            issues.append("RUNTIME_SOLVER_MODIFIED")
        if RUNTIME_WIRING_ALLOWED:
            issues.append("RUNTIME_WIRING_ALLOWED")
        if KAGGLE_SUBMISSION_SENT:
            issues.append("KAGGLE_SUBMISSION_SENT")
        if KAGGLE_AUTHENTICATION_ALLOWED:
            issues.append("KAGGLE_AUTHENTICATION_ALLOWED")
        if KAGGLE_UPLOAD_ALLOWED:
            issues.append("KAGGLE_UPLOAD_ALLOWED")
        if RAW_REQUEST_BODY_PERSISTED:
            issues.append("RAW_REQUEST_BODY_PERSISTED")
        if SECRET_PERSISTED:
            issues.append("SECRET_PERSISTED")
        if LEGAL_CERTIFICATION:
            issues.append("LEGAL_CERTIFICATION")
        if HISTORICAL_MILESTONE_REWRITE:
            issues.append("HISTORICAL_MILESTONE_REWRITE")
        if not FAIL_CLOSED_ACTIVE:
            issues.append("FAIL_CLOSED_INACTIVE")

        return tuple(issues)

    @property
    def valid(self) -> bool:
        return self.implementation_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        scope_payload = self.source_scope_lock_payload
        snapshots = list(self.snapshots)

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceScopeLockId": scope_payload["scopeLockId"],
            "sourceLockValid": scope_payload["valid"],
            "sourceLockOk": scope_payload["lockOk"],
            "sourceSelectedObjectiveId": scope_payload["selectedObjectiveId"],
            "sourceImplementationAllowedNext": scope_payload["implementationAllowedNext"],
            "sourceFastOpeningSnapshot": scope_payload["fastSourceOpeningSnapshot"],
            "nextStage": self.next_stage,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.task_budget_max - self.current_task_number,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "allowedQueryOperations": list(self.allowed_query_operations),
            "allowedQueryOperationCount": len(self.allowed_query_operations),
            "forbiddenOperations": list(self.forbidden_operations),
            "forbiddenOperationCount": len(self.forbidden_operations),
            "requiredSnapshotFields": list(self.required_snapshot_fields),
            "requiredSnapshotFieldCount": len(self.required_snapshot_fields),
            "implementationChecks": list(self.implementation_checks),
            "implementationCheckCount": len(self.implementation_checks),
            "queryInterfaceReady": QUERY_INTERFACE_READY,
            "queryInterfaceImplemented": QUERY_INTERFACE_IMPLEMENTED,
            "queryInterfaceLocalOnly": QUERY_INTERFACE_LOCAL_ONLY,
            "queryInterfaceReadOnly": QUERY_INTERFACE_READ_ONLY,
            "queryInterfaceDeterministic": QUERY_INTERFACE_DETERMINISTIC,
            "queryInterfaceBoundaryValidated": QUERY_INTERFACE_BOUNDARY_VALIDATED,
            "snapshotCount": len(snapshots),
            "registeredMilestoneIds": [snapshot["milestoneId"] for snapshot in snapshots],
            "snapshots": snapshots,
            "m20Task7Used": get_closed_milestone_snapshot("MILESTONE_20")["snapshot"]["task7Used"],
            "m20Task8Used": get_closed_milestone_snapshot("MILESTONE_20")["snapshot"]["task8Used"],
            "m21Task7Used": get_closed_milestone_snapshot("MILESTONE_21")["snapshot"]["task7Used"],
            "m21Task8Used": get_closed_milestone_snapshot("MILESTONE_21")["snapshot"]["task8Used"],
            "m22Task7Used": get_closed_milestone_snapshot("MILESTONE_22")["snapshot"]["task7Used"],
            "m22Task8Used": get_closed_milestone_snapshot("MILESTONE_22")["snapshot"]["task8Used"],
            "missingSnapshotFound": get_closed_milestone_snapshot("MILESTONE_999")["found"],
            "summaryExample": summarize_closed_milestone_snapshot("MILESTONE_22")["summary"],
            "fastSourceScopeLockSnapshot": FAST_SOURCE_SCOPE_LOCK_SNAPSHOT,
            "fastSnapshotDependencyMode": FAST_SNAPSHOT_DEPENDENCY_MODE,
            "deepRecursiveDependencyTraversalAllowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
            "deepRecursiveDependencyTraversalForbidden": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_FORBIDDEN,
            "noRecursiveMetaLayer": NO_RECURSIVE_META_LAYER,
            "closureRequired": CLOSURE_REQUIRED,
            "maxReviewDepth": MAX_REVIEW_DEPTH,
            "maxAuthorizationDepth": MAX_AUTHORIZATION_DEPTH,
            "maxFinalizationDepth": MAX_FINALIZATION_DEPTH,
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
            "implementationOk": self.implementation_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["implementationId"] = self.implementation_id
        return payload


def build_milestone_24_query_interface_implementation(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone24QueryInterfaceImplementation:
    return Milestone24QueryInterfaceImplementation(metadata={} if metadata is None else metadata)


def validate_milestone_24_query_interface_implementation(
    implementation: Milestone24QueryInterfaceImplementation,
) -> tuple[str, ...]:
    return implementation.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "QUERY_INTERFACE_READY",
    "QUERY_INTERFACE_IMPLEMENTED",
    "list_closed_milestone_snapshots",
    "get_closed_milestone_snapshot",
    "summarize_closed_milestone_snapshot",
    "validate_query_result_boundary",
    "Milestone24QueryInterfaceImplementation",
    "build_milestone_24_query_interface_implementation",
    "validate_milestone_24_query_interface_implementation",
]
