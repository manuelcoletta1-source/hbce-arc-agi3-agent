"""Milestone #24 Task 4 - Validation and Artifacts.

Validates the local-only closed milestone snapshot query interface from Task 3
and produces deterministic validation evidence.

This task does not add query features. It validates what already exists. A rare
moment of restraint in software, usually seen only in museums.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_24_closed_milestone_snapshot_query_interface import (
    build_milestone_24_query_interface_implementation,
    get_closed_milestone_snapshot,
    list_closed_milestone_snapshots,
    summarize_closed_milestone_snapshot,
    validate_milestone_24_query_interface_implementation,
    validate_query_result_boundary,
)


TASK_ID = "MILESTONE_24_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
REVISION = "MILESTONE_24_VALIDATION_AND_ARTIFACTS_v1"
MILESTONE_ID = "MILESTONE_24"
NEXT_STAGE = "MILESTONE_24_TASK_5_INTEGRATION_REGRESSION_V1"

SOURCE_TASK_ID = "MILESTONE_24_TASK_3_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_IMPLEMENTATION_V1"
SOURCE_IMPLEMENTATION_READY = True
SOURCE_IMPLEMENTATION_VALID = True
SOURCE_QUERY_INTERFACE_IMPLEMENTED = True

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 4
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

VALIDATION_ARTIFACTS_READY = True
VALIDATION_ARTIFACTS_CREATED = True
QUERY_INTERFACE_VALIDATED = True
QUERY_OPERATIONS_VALIDATED = True
BOUNDARY_VALIDATED = True
QUERY_EXAMPLES_VALIDATED = True
READY_FOR_INTEGRATION_REGRESSION = True

LOCAL_ONLY = True
READ_ONLY = True
DETERMINISTIC = True
PUBLIC_SAFE = True
FAST_SOURCE_IMPLEMENTATION_SNAPSHOT = True
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

VALIDATION_CASES = (
    "source_implementation_valid",
    "list_operation_returns_three_snapshots",
    "get_operation_returns_m20",
    "get_operation_returns_m21",
    "get_operation_returns_m22",
    "get_missing_snapshot_fails_closed",
    "summary_operation_returns_m22_summary",
    "boundary_validation_accepts_valid_snapshot",
    "boundary_validation_rejects_task8_used",
    "query_interface_read_only",
    "query_interface_local_only",
    "deep_recursive_traversal_forbidden",
)

GENERATED_ARTIFACTS = (
    "examples/milestone-24/validation-and-artifacts-v1/task-4-validation-report.json",
    "examples/milestone-24/validation-and-artifacts-v1/task-4-boundary-report.json",
    "examples/milestone-24/validation-and-artifacts-v1/task-4-query-evidence.json",
    "examples/milestone-24/validation-and-artifacts-v1/task-4-validation-report.md",
    "examples/milestone-24/validation-and-artifacts-v1/task-4-manifest.json",
    "examples/milestone-24/validation-and-artifacts-v1/task-4-index.txt",
)


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


def build_query_evidence() -> dict[str, Any]:
    snapshots = list_closed_milestone_snapshots()
    m20 = get_closed_milestone_snapshot("MILESTONE_20")
    m21 = get_closed_milestone_snapshot("MILESTONE_21")
    m22 = get_closed_milestone_snapshot("MILESTONE_22")
    missing = get_closed_milestone_snapshot("MILESTONE_999")
    summary = summarize_closed_milestone_snapshot("MILESTONE_22")

    return {
        "operation": "build_query_evidence",
        "snapshotCount": len(snapshots),
        "registeredMilestoneIds": [snapshot["milestoneId"] for snapshot in snapshots],
        "m20Found": m20["found"],
        "m20Task7Used": m20["snapshot"]["task7Used"],
        "m20Task8Used": m20["snapshot"]["task8Used"],
        "m21Found": m21["found"],
        "m21Task7Used": m21["snapshot"]["task7Used"],
        "m21Task8Used": m21["snapshot"]["task8Used"],
        "m22Found": m22["found"],
        "m22Task7Used": m22["snapshot"]["task7Used"],
        "m22Task8Used": m22["snapshot"]["task8Used"],
        "missingSnapshotFound": missing["found"],
        "missingSnapshotValid": missing["valid"],
        "summaryM22Found": summary["found"],
        "summaryM22Valid": summary["valid"],
        "summaryM22Text": summary["summary"],
        "localOnly": LOCAL_ONLY,
        "readOnly": READ_ONLY,
        "legalCertification": LEGAL_CERTIFICATION,
        "valid": (
            len(snapshots) == 3
            and [snapshot["milestoneId"] for snapshot in snapshots] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
            and m20["found"] is True
            and m20["snapshot"]["task7Used"] is True
            and m20["snapshot"]["task8Used"] is False
            and m21["found"] is True
            and m21["snapshot"]["task7Used"] is False
            and m22["found"] is True
            and m22["snapshot"]["task8Used"] is False
            and missing["found"] is False
            and missing["valid"] is False
            and summary["found"] is True
            and "MILESTONE_22 closed" in summary["summary"]
        ),
        "issues": [],
    }


def build_boundary_report() -> dict[str, Any]:
    snapshots = list_closed_milestone_snapshots()
    valid_boundaries = [validate_query_result_boundary(snapshot) for snapshot in snapshots]

    broken_snapshot = dict(get_closed_milestone_snapshot("MILESTONE_21")["snapshot"])
    broken_snapshot["task8Used"] = True
    broken_boundary = validate_query_result_boundary(broken_snapshot)

    issues: list[str] = []
    if not all(boundary["valid"] for boundary in valid_boundaries):
        issues.append("VALID_SNAPSHOT_BOUNDARY_FAILED")
    if broken_boundary["valid"] is not False:
        issues.append("BROKEN_SNAPSHOT_BOUNDARY_NOT_REJECTED")
    if "TASK_8_USED" not in broken_boundary["issues"]:
        issues.append("BROKEN_SNAPSHOT_TASK8_ISSUE_NOT_DETECTED")

    return {
        "operation": "build_boundary_report",
        "validBoundaryCount": len(valid_boundaries),
        "validBoundaryPassCount": sum(1 for boundary in valid_boundaries if boundary["valid"]),
        "brokenBoundaryValid": broken_boundary["valid"],
        "brokenBoundaryIssues": broken_boundary["issues"],
        "requiredFieldCount": valid_boundaries[0]["requiredFieldCount"] if valid_boundaries else 0,
        "localOnly": LOCAL_ONLY,
        "readOnly": READ_ONLY,
        "legalCertification": LEGAL_CERTIFICATION,
        "valid": issues == [],
        "issues": issues,
    }


@dataclass(frozen=True)
class Milestone24ValidationArtifacts:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    validation_cases: tuple[str, ...] = VALIDATION_CASES
    generated_artifacts: tuple[str, ...] = GENERATED_ARTIFACTS
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def validation_id(self) -> str:
        return f"MILESTONE-24-VALIDATION-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def source_implementation_payload(self) -> Mapping[str, Any]:
        implementation = build_milestone_24_query_interface_implementation()
        return implementation.to_public_dict()

    @property
    def query_evidence(self) -> Mapping[str, Any]:
        return build_query_evidence()

    @property
    def boundary_report(self) -> Mapping[str, Any]:
        return build_boundary_report()

    @property
    def validation_ok(self) -> bool:
        implementation = build_milestone_24_query_interface_implementation()
        source_payload = implementation.to_public_dict()
        evidence = self.query_evidence
        boundary = self.boundary_report

        return (
            VALIDATION_ARTIFACTS_READY is True
            and VALIDATION_ARTIFACTS_CREATED is True
            and QUERY_INTERFACE_VALIDATED is True
            and QUERY_OPERATIONS_VALIDATED is True
            and BOUNDARY_VALIDATED is True
            and QUERY_EXAMPLES_VALIDATED is True
            and READY_FOR_INTEGRATION_REGRESSION is True
            and implementation.valid is True
            and validate_milestone_24_query_interface_implementation(implementation) == ()
            and source_payload["valid"] is True
            and source_payload["implementationOk"] is True
            and source_payload["queryInterfaceImplemented"] is True
            and source_payload["queryInterfaceReadOnly"] is True
            and source_payload["snapshotCount"] == 3
            and source_payload["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
            and evidence["valid"] is True
            and evidence["snapshotCount"] == 3
            and evidence["missingSnapshotFound"] is False
            and boundary["valid"] is True
            and boundary["validBoundaryPassCount"] == 3
            and boundary["brokenBoundaryValid"] is False
            and len(self.validation_cases) == 12
            and len(self.generated_artifacts) == 6
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 4
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and LOCAL_ONLY is True
            and READ_ONLY is True
            and DETERMINISTIC is True
            and PUBLIC_SAFE is True
            and FAST_SOURCE_IMPLEMENTATION_SNAPSHOT is True
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
        implementation = build_milestone_24_query_interface_implementation()
        source_payload = implementation.to_public_dict()
        evidence = self.query_evidence
        boundary = self.boundary_report

        if not implementation.valid:
            issues.append("SOURCE_QUERY_INTERFACE_IMPLEMENTATION_INVALID")
        issues.extend(f"SOURCE_QUERY_INTERFACE_{issue}" for issue in validate_milestone_24_query_interface_implementation(implementation))
        if source_payload["queryInterfaceImplemented"] is not True:
            issues.append("SOURCE_QUERY_INTERFACE_NOT_IMPLEMENTED")
        if source_payload["queryInterfaceReadOnly"] is not True:
            issues.append("SOURCE_QUERY_INTERFACE_NOT_READ_ONLY")
        if source_payload["snapshotCount"] != 3:
            issues.append("SOURCE_SNAPSHOT_COUNT_NOT_3")
        if evidence["valid"] is not True:
            issues.append("QUERY_EVIDENCE_INVALID")
            issues.extend(f"QUERY_EVIDENCE_{issue}" for issue in evidence["issues"])
        if boundary["valid"] is not True:
            issues.append("BOUNDARY_REPORT_INVALID")
            issues.extend(f"BOUNDARY_{issue}" for issue in boundary["issues"])
        if not VALIDATION_ARTIFACTS_READY:
            issues.append("VALIDATION_ARTIFACTS_NOT_READY")
        if not VALIDATION_ARTIFACTS_CREATED:
            issues.append("VALIDATION_ARTIFACTS_NOT_CREATED")
        if not QUERY_INTERFACE_VALIDATED:
            issues.append("QUERY_INTERFACE_NOT_VALIDATED")
        if not QUERY_OPERATIONS_VALIDATED:
            issues.append("QUERY_OPERATIONS_NOT_VALIDATED")
        if not BOUNDARY_VALIDATED:
            issues.append("BOUNDARY_NOT_VALIDATED")
        if not QUERY_EXAMPLES_VALIDATED:
            issues.append("QUERY_EXAMPLES_NOT_VALIDATED")
        if not READY_FOR_INTEGRATION_REGRESSION:
            issues.append("NOT_READY_FOR_INTEGRATION_REGRESSION")
        if len(self.validation_cases) != 12:
            issues.append("VALIDATION_CASE_COUNT_NOT_12")
        if len(self.generated_artifacts) != 6:
            issues.append("GENERATED_ARTIFACT_COUNT_NOT_6")
        if self.task_budget_min != 4:
            issues.append("TASK_BUDGET_MIN_NOT_4")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 4:
            issues.append("CURRENT_TASK_NUMBER_NOT_4")
        if self.recommended_closure_task_number != 6:
            issues.append("RECOMMENDED_CLOSURE_TASK_NOT_6")
        if self.reserve_task_number != 7:
            issues.append("RESERVE_TASK_NUMBER_NOT_7")
        if self.emergency_only_task_number != 8:
            issues.append("EMERGENCY_TASK_NUMBER_NOT_8")
        if not LOCAL_ONLY:
            issues.append("LOCAL_ONLY_FALSE")
        if not READ_ONLY:
            issues.append("READ_ONLY_FALSE")
        if not DETERMINISTIC:
            issues.append("DETERMINISTIC_FALSE")
        if not PUBLIC_SAFE:
            issues.append("PUBLIC_SAFE_FALSE")
        if not FAST_SOURCE_IMPLEMENTATION_SNAPSHOT:
            issues.append("FAST_SOURCE_IMPLEMENTATION_SNAPSHOT_DISABLED")
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
        return self.validation_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        source_payload = self.source_implementation_payload
        evidence = self.query_evidence
        boundary = self.boundary_report

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceTaskId": SOURCE_TASK_ID,
            "sourceImplementationReady": SOURCE_IMPLEMENTATION_READY,
            "sourceImplementationValid": source_payload["valid"],
            "sourceImplementationOk": source_payload["implementationOk"],
            "sourceQueryInterfaceImplemented": source_payload["queryInterfaceImplemented"],
            "sourceQueryInterfaceReadOnly": source_payload["queryInterfaceReadOnly"],
            "sourceSnapshotCount": source_payload["snapshotCount"],
            "sourceRegisteredMilestoneIds": source_payload["registeredMilestoneIds"],
            "sourceMissingSnapshotFound": source_payload["missingSnapshotFound"],
            "nextStage": self.next_stage,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.task_budget_max - self.current_task_number,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "validationCases": list(self.validation_cases),
            "validationCaseCount": len(self.validation_cases),
            "generatedArtifacts": list(self.generated_artifacts),
            "generatedArtifactCount": len(self.generated_artifacts),
            "queryEvidence": dict(evidence),
            "boundaryReport": dict(boundary),
            "validationArtifactsReady": VALIDATION_ARTIFACTS_READY,
            "validationArtifactsCreated": VALIDATION_ARTIFACTS_CREATED,
            "queryInterfaceValidated": QUERY_INTERFACE_VALIDATED,
            "queryOperationsValidated": QUERY_OPERATIONS_VALIDATED,
            "boundaryValidated": BOUNDARY_VALIDATED,
            "queryExamplesValidated": QUERY_EXAMPLES_VALIDATED,
            "readyForIntegrationRegression": READY_FOR_INTEGRATION_REGRESSION,
            "localOnly": LOCAL_ONLY,
            "readOnly": READ_ONLY,
            "deterministic": DETERMINISTIC,
            "publicSafe": PUBLIC_SAFE,
            "fastSourceImplementationSnapshot": FAST_SOURCE_IMPLEMENTATION_SNAPSHOT,
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
            "validationOk": self.validation_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["validationId"] = self.validation_id
        return payload


def build_milestone_24_validation_artifacts(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone24ValidationArtifacts:
    return Milestone24ValidationArtifacts(metadata={} if metadata is None else metadata)


def validate_milestone_24_validation_artifacts(
    validation: Milestone24ValidationArtifacts,
) -> tuple[str, ...]:
    return validation.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "VALIDATION_ARTIFACTS_READY",
    "VALIDATION_ARTIFACTS_CREATED",
    "build_query_evidence",
    "build_boundary_report",
    "Milestone24ValidationArtifacts",
    "build_milestone_24_validation_artifacts",
    "validate_milestone_24_validation_artifacts",
]
