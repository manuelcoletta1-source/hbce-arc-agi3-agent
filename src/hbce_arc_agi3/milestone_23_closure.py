"""Milestone #23 Task 6 - Milestone Closure.

Closes Milestone 23 at Task 6.

Milestone 23 produced a local-only Closed Milestone Snapshot Registry and
validated it through integration regression. Task 6 seals the milestone so
Task 7 and Task 8 remain unused unless a real post-closure defect appears.
Because apparently software does better when someone occasionally says: stop.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_23_integration_regression import (
    build_milestone_23_integration_regression,
    validate_milestone_23_integration_regression,
)
from hbce_arc_agi3.milestone_23_closed_milestone_snapshot_registry import (
    build_closed_milestone_snapshot_registry,
)


TASK_ID = "MILESTONE_23_TASK_6_MILESTONE_CLOSURE_V1"
REVISION = "MILESTONE_23_MILESTONE_CLOSURE_v1"
MILESTONE_ID = "MILESTONE_23"
NEXT_STAGE = "MILESTONE_23_CLOSED_NO_TASK_7_OR_8_USED"

FINAL_STATUS = "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
TECHNICAL_STATUS = "PASS"
PROCESS_STATUS = "GOVERNED_WITHIN_TASK_BUDGET"

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
FINAL_TASK_NUMBER = 6
COMPLETED_TASK_COUNT = 6
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
TASK_7_USED = False
TASK_8_USED = False
RESERVE_UNUSED = True
EMERGENCY_RESERVE_UNUSED = True

MILESTONE_CLOSURE_READY = True
MILESTONE_CLOSED = True
TASK_CHAIN_CLOSED = True
REGISTRY_CHAIN_CLOSED = True
INTEGRATION_REGRESSION_CLOSED = True
CLOSURE_ARTIFACTS_CREATED = True
NO_TASK_7_OR_8_USED = True

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
class Milestone23Closure:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    final_status: str = FINAL_STATUS
    technical_status: str = TECHNICAL_STATUS
    process_status: str = PROCESS_STATUS
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    final_task_number: int = FINAL_TASK_NUMBER
    completed_task_count: int = COMPLETED_TASK_COUNT
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    task_7_used: bool = TASK_7_USED
    task_8_used: bool = TASK_8_USED
    reserve_unused: bool = RESERVE_UNUSED
    emergency_reserve_unused: bool = EMERGENCY_RESERVE_UNUSED
    closure_checks: tuple[str, ...] = (
        "task_1_governed_opening_closed",
        "task_2_objective_scope_lock_closed",
        "task_3_snapshot_registry_implementation_closed",
        "task_4_validation_artifacts_closed",
        "task_5_integration_regression_closed",
        "registry_snapshot_count_3_preserved",
        "registered_milestones_m20_m21_m22_preserved",
        "m20_task7_used_preserved",
        "m20_task8_unused_preserved",
        "m21_task7_unused_preserved",
        "m22_task7_unused_preserved",
        "m22_task8_unused_preserved",
        "deep_recursive_traversal_forbidden",
        "runtime_boundary_preserved",
        "task_7_unused",
        "task_8_unused",
    )
    generated_artifacts: tuple[str, ...] = (
        "examples/milestone-23/milestone-closure-v1/task-6-milestone-closure.json",
        "examples/milestone-23/milestone-closure-v1/task-6-milestone-closure.md",
        "examples/milestone-23/milestone-closure-v1/task-6-manifest.json",
        "examples/milestone-23/milestone-closure-v1/task-6-index.txt",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def closure_id(self) -> str:
        return f"MILESTONE-23-CLOSURE-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def integration_payload(self) -> Mapping[str, Any]:
        return build_milestone_23_integration_regression().to_public_dict()

    @property
    def registry_payload(self) -> Mapping[str, Any]:
        return build_closed_milestone_snapshot_registry().to_public_dict()

    @property
    def closure_ok(self) -> bool:
        integration = build_milestone_23_integration_regression()
        integration_payload = integration.to_public_dict()
        registry = build_closed_milestone_snapshot_registry()

        return (
            MILESTONE_CLOSURE_READY is True
            and MILESTONE_CLOSED is True
            and TASK_CHAIN_CLOSED is True
            and REGISTRY_CHAIN_CLOSED is True
            and INTEGRATION_REGRESSION_CLOSED is True
            and CLOSURE_ARTIFACTS_CREATED is True
            and NO_TASK_7_OR_8_USED is True
            and integration.valid is True
            and validate_milestone_23_integration_regression(integration) == ()
            and integration_payload["valid"] is True
            and integration_payload["integrationOk"] is True
            and integration_payload["readyForMilestoneClosure"] is True
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
            and self.final_status == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
            and self.technical_status == "PASS"
            and self.process_status == "GOVERNED_WITHIN_TASK_BUDGET"
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.final_task_number == 6
            and self.completed_task_count == 6
            and self.recommended_closure_task_number == 6
            and self.task_7_used is False
            and self.task_8_used is False
            and self.reserve_unused is True
            and self.emergency_reserve_unused is True
            and len(self.closure_checks) == 16
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

        integration = build_milestone_23_integration_regression()
        registry = build_closed_milestone_snapshot_registry()

        if not integration.valid:
            issues.append("SOURCE_INTEGRATION_REGRESSION_INVALID")
        issues.extend(f"SOURCE_INTEGRATION_{issue}" for issue in validate_milestone_23_integration_regression(integration))

        if not MILESTONE_CLOSURE_READY:
            issues.append("MILESTONE_CLOSURE_NOT_READY")
        if not MILESTONE_CLOSED:
            issues.append("MILESTONE_NOT_CLOSED")
        if not TASK_CHAIN_CLOSED:
            issues.append("TASK_CHAIN_NOT_CLOSED")
        if not REGISTRY_CHAIN_CLOSED:
            issues.append("REGISTRY_CHAIN_NOT_CLOSED")
        if not INTEGRATION_REGRESSION_CLOSED:
            issues.append("INTEGRATION_REGRESSION_NOT_CLOSED")
        if not CLOSURE_ARTIFACTS_CREATED:
            issues.append("CLOSURE_ARTIFACTS_NOT_CREATED")
        if not NO_TASK_7_OR_8_USED:
            issues.append("TASK_7_OR_8_USED")
        if not registry.valid:
            issues.append("REGISTRY_INVALID")
        if registry.snapshot_count != 3:
            issues.append("REGISTRY_SNAPSHOT_COUNT_NOT_3")
        if registry.valid_snapshot_count != 3:
            issues.append("REGISTRY_VALID_SNAPSHOT_COUNT_NOT_3")
        if registry.milestone_ids != ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22"):
            issues.append("REGISTRY_MILESTONE_IDS_MISMATCH")
        if self.final_status != "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6":
            issues.append("FINAL_STATUS_MISMATCH")
        if self.technical_status != "PASS":
            issues.append("TECHNICAL_STATUS_NOT_PASS")
        if self.process_status != "GOVERNED_WITHIN_TASK_BUDGET":
            issues.append("PROCESS_STATUS_MISMATCH")
        if self.task_budget_min != 4:
            issues.append("TASK_BUDGET_MIN_NOT_4")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.final_task_number != 6:
            issues.append("FINAL_TASK_NUMBER_NOT_6")
        if self.completed_task_count != 6:
            issues.append("COMPLETED_TASK_COUNT_NOT_6")
        if self.recommended_closure_task_number != 6:
            issues.append("RECOMMENDED_CLOSURE_TASK_NOT_6")
        if self.task_7_used:
            issues.append("TASK_7_USED")
        if self.task_8_used:
            issues.append("TASK_8_USED")
        if not self.reserve_unused:
            issues.append("RESERVE_NOT_UNUSED")
        if not self.emergency_reserve_unused:
            issues.append("EMERGENCY_RESERVE_NOT_UNUSED")
        if len(self.closure_checks) != 16:
            issues.append("CLOSURE_CHECK_COUNT_NOT_16")
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
        return self.closure_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        integration_payload = self.integration_payload
        registry_payload = self.registry_payload

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceIntegrationId": integration_payload["integrationId"],
            "sourceIntegrationValid": integration_payload["valid"],
            "sourceIntegrationOk": integration_payload["integrationOk"],
            "sourceReadyForMilestoneClosure": integration_payload["readyForMilestoneClosure"],
            "registryId": registry_payload["registryId"],
            "registryValid": registry_payload["valid"],
            "registrySnapshotCount": registry_payload["snapshotCount"],
            "registryValidSnapshotCount": registry_payload["validSnapshotCount"],
            "registeredMilestoneIds": registry_payload["milestoneIds"],
            "nextStage": self.next_stage,
            "finalStatus": self.final_status,
            "technicalStatus": self.technical_status,
            "processStatus": self.process_status,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "finalTaskNumber": self.final_task_number,
            "completedTaskCount": self.completed_task_count,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "task7Used": self.task_7_used,
            "task8Used": self.task_8_used,
            "reserveUnused": self.reserve_unused,
            "emergencyReserveUnused": self.emergency_reserve_unused,
            "closureChecks": list(self.closure_checks),
            "closureCheckCount": len(self.closure_checks),
            "generatedArtifacts": list(self.generated_artifacts),
            "generatedArtifactCount": len(self.generated_artifacts),
            "milestoneClosureReady": MILESTONE_CLOSURE_READY,
            "milestoneClosed": MILESTONE_CLOSED,
            "taskChainClosed": TASK_CHAIN_CLOSED,
            "registryChainClosed": REGISTRY_CHAIN_CLOSED,
            "integrationRegressionClosed": INTEGRATION_REGRESSION_CLOSED,
            "closureArtifactsCreated": CLOSURE_ARTIFACTS_CREATED,
            "noTask7Or8Used": NO_TASK_7_OR_8_USED,
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
            "closureOk": self.closure_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["closureId"] = self.closure_id
        return payload


def build_milestone_23_closure(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone23Closure:
    return Milestone23Closure(metadata={} if metadata is None else metadata)


def validate_milestone_23_closure(
    closure: Milestone23Closure,
) -> tuple[str, ...]:
    return closure.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "FINAL_STATUS",
    "MILESTONE_CLOSURE_READY",
    "MILESTONE_CLOSED",
    "Milestone23Closure",
    "build_milestone_23_closure",
    "validate_milestone_23_closure",
]
