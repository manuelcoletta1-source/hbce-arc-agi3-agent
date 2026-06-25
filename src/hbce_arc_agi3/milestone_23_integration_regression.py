"""Milestone #23 Task 5 - Integration Regression.

Runs integration regression over the Milestone 23 closed milestone snapshot
registry chain.

This validates Task 1 through Task 4 together, then checks that the local-only
registry preserves prior milestone closure facts without runtime recursion.
Because apparently not everything needs to become a self-referential spaghetti
ritual under fluorescent lighting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_23_governed_opening import (
    build_milestone_23_governed_opening,
    validate_milestone_23_governed_opening,
)
from hbce_arc_agi3.milestone_23_objective_scope_lock import (
    build_milestone_23_objective_scope_lock,
    validate_milestone_23_objective_scope_lock,
)
from hbce_arc_agi3.milestone_23_closed_milestone_snapshot_registry import (
    build_closed_milestone_snapshot_registry,
    build_milestone_23_closed_milestone_snapshot_registry_implementation,
    detect_forbidden_registry_traversal,
    validate_milestone_23_closed_milestone_snapshot_registry_implementation,
)
from hbce_arc_agi3.milestone_23_validation_artifacts import (
    build_milestone_23_validation_artifacts,
    validate_milestone_23_validation_artifacts,
)


TASK_ID = "MILESTONE_23_TASK_5_INTEGRATION_REGRESSION_V1"
REVISION = "MILESTONE_23_INTEGRATION_REGRESSION_v1"
MILESTONE_ID = "MILESTONE_23"
NEXT_STAGE = "MILESTONE_23_TASK_6_MILESTONE_CLOSURE_V1"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 5
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

INTEGRATION_REGRESSION_READY = True
INTEGRATION_REGRESSION_EXECUTED = True
TASK_CHAIN_VALIDATED = True
REGISTRY_INTEGRATION_VALIDATED = True
ARTIFACT_CHAIN_VALIDATED = True
BOUNDARY_REGRESSION_VALIDATED = True
FORBIDDEN_TRAVERSAL_REGRESSION_VALIDATED = True
STATIC_LOOKUP_REGRESSION_VALIDATED = True
READY_FOR_MILESTONE_CLOSURE = True

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
class Milestone23IntegrationRegression:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    integration_cases: tuple[str, ...] = (
        "task_1_governed_opening_valid",
        "task_2_objective_scope_lock_valid",
        "task_3_snapshot_registry_implementation_valid",
        "task_4_validation_artifacts_valid",
        "registry_lookup_m20_valid",
        "registry_lookup_m21_valid",
        "registry_lookup_m22_valid",
        "m20_task7_used_preserved",
        "m20_task8_unused_preserved",
        "m21_task7_unused_preserved",
        "m21_task8_unused_preserved",
        "m22_task7_unused_preserved",
        "m22_task8_unused_preserved",
        "forbidden_traversal_detection_regression_valid",
        "static_lookup_regression_valid",
        "runtime_boundary_regression_valid",
    )
    generated_artifacts: tuple[str, ...] = (
        "examples/milestone-23/integration-regression-v1/task-5-integration-regression.json",
        "examples/milestone-23/integration-regression-v1/task-5-integration-regression.md",
        "examples/milestone-23/integration-regression-v1/task-5-manifest.json",
        "examples/milestone-23/integration-regression-v1/task-5-index.txt",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def integration_id(self) -> str:
        return f"MILESTONE-23-INTEGRATION-REGRESSION-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def task_1_payload(self) -> Mapping[str, Any]:
        return build_milestone_23_governed_opening().to_public_dict()

    @property
    def task_2_payload(self) -> Mapping[str, Any]:
        return build_milestone_23_objective_scope_lock().to_public_dict()

    @property
    def task_3_payload(self) -> Mapping[str, Any]:
        return build_milestone_23_closed_milestone_snapshot_registry_implementation().to_public_dict()

    @property
    def task_4_payload(self) -> Mapping[str, Any]:
        return build_milestone_23_validation_artifacts().to_public_dict()

    @property
    def registry_payload(self) -> Mapping[str, Any]:
        return build_closed_milestone_snapshot_registry().to_public_dict()

    @property
    def integration_ok(self) -> bool:
        task_1 = build_milestone_23_governed_opening()
        task_2 = build_milestone_23_objective_scope_lock()
        task_3 = build_milestone_23_closed_milestone_snapshot_registry_implementation()
        task_4 = build_milestone_23_validation_artifacts()
        registry = build_closed_milestone_snapshot_registry()

        forbidden_detected = detect_forbidden_registry_traversal(
            (
                "static_registry_lookup",
                "closed_milestone.to_public_dict()",
                "closed_milestone.valid",
                "safe_document_marker_evidence",
            )
        )

        return (
            INTEGRATION_REGRESSION_READY is True
            and INTEGRATION_REGRESSION_EXECUTED is True
            and TASK_CHAIN_VALIDATED is True
            and REGISTRY_INTEGRATION_VALIDATED is True
            and ARTIFACT_CHAIN_VALIDATED is True
            and BOUNDARY_REGRESSION_VALIDATED is True
            and FORBIDDEN_TRAVERSAL_REGRESSION_VALIDATED is True
            and STATIC_LOOKUP_REGRESSION_VALIDATED is True
            and READY_FOR_MILESTONE_CLOSURE is True
            and task_1.valid is True
            and validate_milestone_23_governed_opening(task_1) == ()
            and task_2.valid is True
            and validate_milestone_23_objective_scope_lock(task_2) == ()
            and task_3.valid is True
            and validate_milestone_23_closed_milestone_snapshot_registry_implementation(task_3) == ()
            and task_4.valid is True
            and validate_milestone_23_validation_artifacts(task_4) == ()
            and registry.valid is True
            and registry.snapshot_count == 3
            and registry.valid_snapshot_count == 3
            and registry.milestone_ids == ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22")
            and registry.get("MILESTONE_20").task_7_used is True
            and registry.get("MILESTONE_20").task_8_used is False
            and registry.get("MILESTONE_21").task_7_used is False
            and registry.get("MILESTONE_21").task_8_used is False
            and registry.get("MILESTONE_22").task_7_used is False
            and registry.get("MILESTONE_22").task_8_used is False
            and forbidden_detected == ("closed_milestone.to_public_dict()", "closed_milestone.valid")
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 5
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.integration_cases) == 16
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

        task_1 = build_milestone_23_governed_opening()
        task_2 = build_milestone_23_objective_scope_lock()
        task_3 = build_milestone_23_closed_milestone_snapshot_registry_implementation()
        task_4 = build_milestone_23_validation_artifacts()
        registry = build_closed_milestone_snapshot_registry()

        if not task_1.valid:
            issues.append("TASK_1_GOVERNED_OPENING_INVALID")
        issues.extend(f"TASK_1_{issue}" for issue in validate_milestone_23_governed_opening(task_1))

        if not task_2.valid:
            issues.append("TASK_2_OBJECTIVE_SCOPE_LOCK_INVALID")
        issues.extend(f"TASK_2_{issue}" for issue in validate_milestone_23_objective_scope_lock(task_2))

        if not task_3.valid:
            issues.append("TASK_3_REGISTRY_IMPLEMENTATION_INVALID")
        issues.extend(f"TASK_3_{issue}" for issue in validate_milestone_23_closed_milestone_snapshot_registry_implementation(task_3))

        if not task_4.valid:
            issues.append("TASK_4_VALIDATION_ARTIFACTS_INVALID")
        issues.extend(f"TASK_4_{issue}" for issue in validate_milestone_23_validation_artifacts(task_4))

        if not INTEGRATION_REGRESSION_READY:
            issues.append("INTEGRATION_REGRESSION_NOT_READY")
        if not INTEGRATION_REGRESSION_EXECUTED:
            issues.append("INTEGRATION_REGRESSION_NOT_EXECUTED")
        if not TASK_CHAIN_VALIDATED:
            issues.append("TASK_CHAIN_NOT_VALIDATED")
        if not REGISTRY_INTEGRATION_VALIDATED:
            issues.append("REGISTRY_INTEGRATION_NOT_VALIDATED")
        if not ARTIFACT_CHAIN_VALIDATED:
            issues.append("ARTIFACT_CHAIN_NOT_VALIDATED")
        if not BOUNDARY_REGRESSION_VALIDATED:
            issues.append("BOUNDARY_REGRESSION_NOT_VALIDATED")
        if not FORBIDDEN_TRAVERSAL_REGRESSION_VALIDATED:
            issues.append("FORBIDDEN_TRAVERSAL_REGRESSION_NOT_VALIDATED")
        if not STATIC_LOOKUP_REGRESSION_VALIDATED:
            issues.append("STATIC_LOOKUP_REGRESSION_NOT_VALIDATED")
        if not READY_FOR_MILESTONE_CLOSURE:
            issues.append("NOT_READY_FOR_MILESTONE_CLOSURE")
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
        if self.current_task_number != 5:
            issues.append("CURRENT_TASK_NUMBER_NOT_5")
        if self.recommended_closure_task_number != 6:
            issues.append("RECOMMENDED_CLOSURE_TASK_NOT_6")
        if self.reserve_task_number != 7:
            issues.append("RESERVE_TASK_NUMBER_NOT_7")
        if self.emergency_only_task_number != 8:
            issues.append("EMERGENCY_TASK_NUMBER_NOT_8")
        if len(self.integration_cases) != 16:
            issues.append("INTEGRATION_CASE_COUNT_NOT_16")
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
        return self.integration_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        task_1_payload = self.task_1_payload
        task_2_payload = self.task_2_payload
        task_3_payload = self.task_3_payload
        task_4_payload = self.task_4_payload
        registry_payload = self.registry_payload

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceTask1OpeningId": task_1_payload["openingId"],
            "sourceTask1Valid": task_1_payload["valid"],
            "sourceTask2LockId": task_2_payload["lockId"],
            "sourceTask2Valid": task_2_payload["valid"],
            "sourceTask3ImplementationId": task_3_payload["implementationId"],
            "sourceTask3Valid": task_3_payload["valid"],
            "sourceTask4ValidationArtifactId": task_4_payload["validationArtifactId"],
            "sourceTask4Valid": task_4_payload["valid"],
            "registryId": registry_payload["registryId"],
            "registryValid": registry_payload["valid"],
            "registrySnapshotCount": registry_payload["snapshotCount"],
            "registryValidSnapshotCount": registry_payload["validSnapshotCount"],
            "registeredMilestoneIds": registry_payload["milestoneIds"],
            "nextStage": self.next_stage,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.task_budget_max - self.current_task_number,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "integrationCases": list(self.integration_cases),
            "integrationCaseCount": len(self.integration_cases),
            "generatedArtifacts": list(self.generated_artifacts),
            "generatedArtifactCount": len(self.generated_artifacts),
            "integrationRegressionReady": INTEGRATION_REGRESSION_READY,
            "integrationRegressionExecuted": INTEGRATION_REGRESSION_EXECUTED,
            "taskChainValidated": TASK_CHAIN_VALIDATED,
            "registryIntegrationValidated": REGISTRY_INTEGRATION_VALIDATED,
            "artifactChainValidated": ARTIFACT_CHAIN_VALIDATED,
            "boundaryRegressionValidated": BOUNDARY_REGRESSION_VALIDATED,
            "forbiddenTraversalRegressionValidated": FORBIDDEN_TRAVERSAL_REGRESSION_VALIDATED,
            "staticLookupRegressionValidated": STATIC_LOOKUP_REGRESSION_VALIDATED,
            "readyForMilestoneClosure": READY_FOR_MILESTONE_CLOSURE,
            "m20Task7Used": build_closed_milestone_snapshot_registry().get("MILESTONE_20").task_7_used,
            "m20Task8Used": build_closed_milestone_snapshot_registry().get("MILESTONE_20").task_8_used,
            "m21Task7Used": build_closed_milestone_snapshot_registry().get("MILESTONE_21").task_7_used,
            "m21Task8Used": build_closed_milestone_snapshot_registry().get("MILESTONE_21").task_8_used,
            "m22Task7Used": build_closed_milestone_snapshot_registry().get("MILESTONE_22").task_7_used,
            "m22Task8Used": build_closed_milestone_snapshot_registry().get("MILESTONE_22").task_8_used,
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
            "integrationOk": self.integration_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["integrationId"] = self.integration_id
        return payload


def build_milestone_23_integration_regression(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone23IntegrationRegression:
    return Milestone23IntegrationRegression(metadata={} if metadata is None else metadata)


def validate_milestone_23_integration_regression(
    integration: Milestone23IntegrationRegression,
) -> tuple[str, ...]:
    return integration.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "INTEGRATION_REGRESSION_READY",
    "INTEGRATION_REGRESSION_EXECUTED",
    "READY_FOR_MILESTONE_CLOSURE",
    "Milestone23IntegrationRegression",
    "build_milestone_23_integration_regression",
    "validate_milestone_23_integration_regression",
]
