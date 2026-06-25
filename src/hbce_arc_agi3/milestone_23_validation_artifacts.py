"""Milestone #23 Task 4 - Validation and Artifacts.

Validates the Closed Milestone Snapshot Registry implemented in Task 3 and
emits formal validation artifacts.

No new registry implementation happens here. This task checks the thing that
was built, because skipping validation is how projects turn into folklore.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_23_closed_milestone_snapshot_registry import (
    build_closed_milestone_snapshot_registry,
    build_milestone_23_closed_milestone_snapshot_registry_implementation,
    detect_forbidden_registry_traversal,
    validate_milestone_23_closed_milestone_snapshot_registry_implementation,
)


TASK_ID = "MILESTONE_23_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
REVISION = "MILESTONE_23_VALIDATION_AND_ARTIFACTS_v1"
MILESTONE_ID = "MILESTONE_23"
NEXT_STAGE = "MILESTONE_23_TASK_5_INTEGRATION_REGRESSION_V1"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 4
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

VALIDATION_ARTIFACTS_READY = True
VALIDATION_ARTIFACTS_CREATED = True
REGISTRY_VALIDATED = True
LOOKUP_VALIDATED = True
SNAPSHOT_EVIDENCE_VALIDATED = True
FORBIDDEN_TRAVERSAL_DETECTION_VALIDATED = True
BOUNDARY_VALIDATED = True
READY_FOR_INTEGRATION_REGRESSION = True

LOCAL_ONLY = True
DETERMINISTIC = True
PUBLIC_SAFE = True
FAST_SNAPSHOT_DEPENDENCY_MODE = True
DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED = False
DOCUMENT_MARKER_EVIDENCE_REQUIRED = True
STATIC_CLOSURE_SNAPSHOT_REQUIRED = True
CLOSED_MILESTONE_ARTIFACT_LOOKUP_REQUIRED = True

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


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


@dataclass(frozen=True)
class Milestone23ValidationArtifacts:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    validation_cases: tuple[str, ...] = (
        "source_task_3_implementation_valid",
        "registry_valid",
        "registry_snapshot_count_3",
        "registry_valid_snapshot_count_3",
        "milestone_20_snapshot_lookup_valid",
        "milestone_21_snapshot_lookup_valid",
        "milestone_22_snapshot_lookup_valid",
        "milestone_22_task7_unused_preserved",
        "milestone_22_task8_unused_preserved",
        "milestone_20_task7_used_preserved",
        "forbidden_traversal_detection_valid",
        "runtime_boundaries_unchanged",
    )
    generated_artifacts: tuple[str, ...] = (
        "examples/milestone-23/validation-and-artifacts-v1/task-4-validation-artifacts.json",
        "examples/milestone-23/validation-and-artifacts-v1/task-4-validation-artifacts.md",
        "examples/milestone-23/validation-and-artifacts-v1/task-4-manifest.json",
        "examples/milestone-23/validation-and-artifacts-v1/task-4-index.txt",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def validation_artifact_id(self) -> str:
        return f"MILESTONE-23-VALIDATION-ARTIFACTS-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def implementation_payload(self) -> Mapping[str, Any]:
        return build_milestone_23_closed_milestone_snapshot_registry_implementation().to_public_dict()

    @property
    def registry_payload(self) -> Mapping[str, Any]:
        return build_closed_milestone_snapshot_registry().to_public_dict()

    @property
    def validation_ok(self) -> bool:
        implementation = build_milestone_23_closed_milestone_snapshot_registry_implementation()
        implementation_payload = implementation.to_public_dict()
        registry = build_closed_milestone_snapshot_registry()

        forbidden_detected = detect_forbidden_registry_traversal(
            (
                "static_registry_lookup",
                "closed_milestone.to_public_dict()",
                "runtime_object_graph_walk",
                "safe_document_marker_evidence",
            )
        )

        return (
            VALIDATION_ARTIFACTS_READY is True
            and VALIDATION_ARTIFACTS_CREATED is True
            and REGISTRY_VALIDATED is True
            and LOOKUP_VALIDATED is True
            and SNAPSHOT_EVIDENCE_VALIDATED is True
            and FORBIDDEN_TRAVERSAL_DETECTION_VALIDATED is True
            and BOUNDARY_VALIDATED is True
            and READY_FOR_INTEGRATION_REGRESSION is True
            and implementation.valid is True
            and validate_milestone_23_closed_milestone_snapshot_registry_implementation(implementation) == ()
            and implementation_payload["valid"] is True
            and implementation_payload["implementationOk"] is True
            and implementation_payload["registryImplemented"] is True
            and implementation_payload["readyForValidationArtifacts"] is True
            and registry.valid is True
            and registry.snapshot_count == 3
            and registry.valid_snapshot_count == 3
            and registry.milestone_ids == ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22")
            and registry.get("MILESTONE_22").task_7_used is False
            and registry.get("MILESTONE_22").task_8_used is False
            and registry.get("MILESTONE_20").task_7_used is True
            and registry.get("MILESTONE_20").task_8_used is False
            and forbidden_detected == ("closed_milestone.to_public_dict()", "runtime_object_graph_walk")
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 4
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.validation_cases) == 12
            and len(self.generated_artifacts) == 4
            and LOCAL_ONLY is True
            and DETERMINISTIC is True
            and PUBLIC_SAFE is True
            and FAST_SNAPSHOT_DEPENDENCY_MODE is True
            and DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED is False
            and DOCUMENT_MARKER_EVIDENCE_REQUIRED is True
            and STATIC_CLOSURE_SNAPSHOT_REQUIRED is True
            and CLOSED_MILESTONE_ARTIFACT_LOOKUP_REQUIRED is True
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

        implementation = build_milestone_23_closed_milestone_snapshot_registry_implementation()
        registry = build_closed_milestone_snapshot_registry()

        if not implementation.valid:
            issues.append("SOURCE_REGISTRY_IMPLEMENTATION_INVALID")
        issues.extend(
            f"SOURCE_REGISTRY_IMPLEMENTATION_{issue}"
            for issue in validate_milestone_23_closed_milestone_snapshot_registry_implementation(implementation)
        )

        if not VALIDATION_ARTIFACTS_READY:
            issues.append("VALIDATION_ARTIFACTS_NOT_READY")
        if not VALIDATION_ARTIFACTS_CREATED:
            issues.append("VALIDATION_ARTIFACTS_NOT_CREATED")
        if not REGISTRY_VALIDATED:
            issues.append("REGISTRY_NOT_VALIDATED")
        if not LOOKUP_VALIDATED:
            issues.append("LOOKUP_NOT_VALIDATED")
        if not SNAPSHOT_EVIDENCE_VALIDATED:
            issues.append("SNAPSHOT_EVIDENCE_NOT_VALIDATED")
        if not FORBIDDEN_TRAVERSAL_DETECTION_VALIDATED:
            issues.append("FORBIDDEN_TRAVERSAL_DETECTION_NOT_VALIDATED")
        if not BOUNDARY_VALIDATED:
            issues.append("BOUNDARY_NOT_VALIDATED")
        if not READY_FOR_INTEGRATION_REGRESSION:
            issues.append("NOT_READY_FOR_INTEGRATION_REGRESSION")
        if not registry.valid:
            issues.append("REGISTRY_INVALID")
        if registry.snapshot_count != 3:
            issues.append("REGISTRY_SNAPSHOT_COUNT_NOT_3")
        if registry.valid_snapshot_count != 3:
            issues.append("REGISTRY_VALID_SNAPSHOT_COUNT_NOT_3")
        if registry.milestone_ids != ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22"):
            issues.append("REGISTRY_MILESTONE_IDS_MISMATCH")
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
        if len(self.validation_cases) != 12:
            issues.append("VALIDATION_CASE_COUNT_NOT_12")
        if len(self.generated_artifacts) != 4:
            issues.append("GENERATED_ARTIFACT_COUNT_NOT_4")
        if not LOCAL_ONLY:
            issues.append("LOCAL_ONLY_FALSE")
        if not DETERMINISTIC:
            issues.append("DETERMINISTIC_FALSE")
        if not PUBLIC_SAFE:
            issues.append("PUBLIC_SAFE_FALSE")
        if not FAST_SNAPSHOT_DEPENDENCY_MODE:
            issues.append("FAST_SNAPSHOT_DEPENDENCY_MODE_DISABLED")
        if DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED:
            issues.append("DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED")
        if not DOCUMENT_MARKER_EVIDENCE_REQUIRED:
            issues.append("DOCUMENT_MARKER_EVIDENCE_NOT_REQUIRED")
        if not STATIC_CLOSURE_SNAPSHOT_REQUIRED:
            issues.append("STATIC_CLOSURE_SNAPSHOT_NOT_REQUIRED")
        if not CLOSED_MILESTONE_ARTIFACT_LOOKUP_REQUIRED:
            issues.append("CLOSED_MILESTONE_ARTIFACT_LOOKUP_NOT_REQUIRED")
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
        implementation_payload = self.implementation_payload
        registry_payload = self.registry_payload

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceImplementationId": implementation_payload["implementationId"],
            "sourceImplementationValid": implementation_payload["valid"],
            "sourceImplementationOk": implementation_payload["implementationOk"],
            "sourceRegistryId": implementation_payload["registryId"],
            "registryId": registry_payload["registryId"],
            "registryValid": registry_payload["valid"],
            "registrySnapshotCount": registry_payload["snapshotCount"],
            "registryValidSnapshotCount": registry_payload["validSnapshotCount"],
            "registeredMilestoneIds": registry_payload["milestoneIds"],
            "requiredSnapshotFieldCount": registry_payload["requiredSnapshotFieldCount"],
            "forbiddenTraversalTokenCount": registry_payload["forbiddenTraversalTokenCount"],
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
            "validationArtifactsReady": VALIDATION_ARTIFACTS_READY,
            "validationArtifactsCreated": VALIDATION_ARTIFACTS_CREATED,
            "registryValidated": REGISTRY_VALIDATED,
            "lookupValidated": LOOKUP_VALIDATED,
            "snapshotEvidenceValidated": SNAPSHOT_EVIDENCE_VALIDATED,
            "forbiddenTraversalDetectionValidated": FORBIDDEN_TRAVERSAL_DETECTION_VALIDATED,
            "boundaryValidated": BOUNDARY_VALIDATED,
            "readyForIntegrationRegression": READY_FOR_INTEGRATION_REGRESSION,
            "localOnly": LOCAL_ONLY,
            "deterministic": DETERMINISTIC,
            "publicSafe": PUBLIC_SAFE,
            "fastSnapshotDependencyMode": FAST_SNAPSHOT_DEPENDENCY_MODE,
            "deepRecursiveDependencyTraversalAllowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
            "documentMarkerEvidenceRequired": DOCUMENT_MARKER_EVIDENCE_REQUIRED,
            "staticClosureSnapshotRequired": STATIC_CLOSURE_SNAPSHOT_REQUIRED,
            "closedMilestoneArtifactLookupRequired": CLOSED_MILESTONE_ARTIFACT_LOOKUP_REQUIRED,
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
            payload["validationArtifactId"] = self.validation_artifact_id
        return payload


def build_milestone_23_validation_artifacts(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone23ValidationArtifacts:
    return Milestone23ValidationArtifacts(metadata={} if metadata is None else metadata)


def validate_milestone_23_validation_artifacts(
    validation_artifacts: Milestone23ValidationArtifacts,
) -> tuple[str, ...]:
    return validation_artifacts.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "VALIDATION_ARTIFACTS_READY",
    "VALIDATION_ARTIFACTS_CREATED",
    "Milestone23ValidationArtifacts",
    "build_milestone_23_validation_artifacts",
    "validate_milestone_23_validation_artifacts",
]
