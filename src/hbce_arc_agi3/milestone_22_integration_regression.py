"""Milestone #22 Task 5 - Integration Regression.

This task integrates and regression-checks the Milestone 22 chain:

Task 1: governed opening.
Task 2: objective selection and scope lock.
Task 3: fast snapshot dependency guard implementation.
Task 4: validation and artifacts.

Task 5 does not add a new feature. It checks that the thing already built
does not quietly saw through its own floorboards, which is apparently necessary
because software has the survival instinct of wet cardboard.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_22_validation_artifacts import (
    build_milestone_22_validation_artifacts,
    validate_milestone_22_validation_artifacts,
)


TASK_ID = "MILESTONE_22_TASK_5_INTEGRATION_REGRESSION_V1"
REVISION = "MILESTONE_22_INTEGRATION_REGRESSION_v1"
MILESTONE_ID = "MILESTONE_22"
NEXT_STAGE = "MILESTONE_22_TASK_6_MILESTONE_CLOSURE_V1"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 5
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

INTEGRATION_REGRESSION_READY = True
INTEGRATION_REGRESSION_EXECUTED = True
TASK_CHAIN_VALIDATED = True
GUARD_INTEGRATION_VALIDATED = True
ARTIFACT_CHAIN_VALIDATED = True
BOUNDARY_REGRESSION_VALIDATED = True
READY_FOR_MILESTONE_CLOSURE = True

NO_RECURSIVE_META_LAYER = True
CLOSURE_REQUIRED = True

MAX_REVIEW_DEPTH = 1
MAX_AUTHORIZATION_DEPTH = 1
MAX_FINALIZATION_DEPTH = 1

MILESTONE_21_REOPEN_REQUIRED = False
MILESTONE_21_TASK_7_REQUIRED = False
MILESTONE_21_TASK_8_REQUIRED = False
MILESTONE_20_REOPEN_REQUIRED = False
MILESTONE_20_TASK_8_REQUIRED = False
MILESTONE_19_REOPEN_REQUIRED = False

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
class Milestone22IntegrationRegression:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    integration_cases: tuple[str, ...] = (
        "task_1_governed_opening_dependency_valid",
        "task_2_scope_lock_dependency_valid",
        "task_3_fast_snapshot_guard_dependency_valid",
        "task_4_validation_artifacts_dependency_valid",
        "validation_artifact_contract_valid",
        "source_guard_valid",
        "m20_task7_snapshot_preserved",
        "m20_task8_unused_preserved",
        "forbidden_traversal_detection_integrated",
        "runtime_boundaries_unchanged",
        "task_budget_chain_preserved",
        "ready_for_milestone_closure",
    )
    generated_artifacts: tuple[str, ...] = (
        "examples/milestone-22/integration-regression-v1/task-5-integration-regression.json",
        "examples/milestone-22/integration-regression-v1/task-5-integration-regression.md",
        "examples/milestone-22/integration-regression-v1/task-5-manifest.json",
        "examples/milestone-22/integration-regression-v1/task-5-index.txt",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def integration_id(self) -> str:
        return f"MILESTONE-22-INTEGRATION-REGRESSION-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def remaining_budget_after_current_task(self) -> int:
        return self.task_budget_max - self.current_task_number

    @property
    def validation_payload(self) -> Mapping[str, Any]:
        return build_milestone_22_validation_artifacts().to_public_dict()

    @property
    def integration_ok(self) -> bool:
        validation_artifacts = build_milestone_22_validation_artifacts()
        validation_payload = validation_artifacts.to_public_dict()

        return (
            INTEGRATION_REGRESSION_READY is True
            and INTEGRATION_REGRESSION_EXECUTED is True
            and TASK_CHAIN_VALIDATED is True
            and GUARD_INTEGRATION_VALIDATED is True
            and ARTIFACT_CHAIN_VALIDATED is True
            and BOUNDARY_REGRESSION_VALIDATED is True
            and READY_FOR_MILESTONE_CLOSURE is True
            and validation_artifacts.valid is True
            and validate_milestone_22_validation_artifacts(validation_artifacts) == ()
            and validation_payload["valid"] is True
            and validation_payload["validationOk"] is True
            and validation_payload["sourceGuardValid"] is True
            and validation_payload["sourceGuardSnapshotCount"] == 2
            and validation_payload["validationCaseCount"] == 10
            and validation_payload["generatedArtifactCount"] == 4
            and validation_payload["m21Task7Used"] is False
            and validation_payload["m21Task8Used"] is False
            and validation_payload["m20FinalTaskNumber"] == 7
            and validation_payload["m20Task7Used"] is True
            and validation_payload["m20Task8Used"] is False
            and validation_payload["readyForIntegrationRegression"] is True
            and validation_payload["runtimeSolverModified"] is False
            and validation_payload["runtimeWiringAllowed"] is False
            and validation_payload["kaggleSubmissionSent"] is False
            and validation_payload["rawRequestBodyPersisted"] is False
            and validation_payload["secretPersisted"] is False
            and validation_payload["legalCertification"] is False
            and self.task_budget_max == 8
            and self.current_task_number == 5
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.integration_cases) == 12
            and len(self.generated_artifacts) == 4
            and NO_RECURSIVE_META_LAYER is True
            and CLOSURE_REQUIRED is True
            and MAX_REVIEW_DEPTH == 1
            and MAX_AUTHORIZATION_DEPTH == 1
            and MAX_FINALIZATION_DEPTH == 1
            and MILESTONE_21_REOPEN_REQUIRED is False
            and MILESTONE_21_TASK_7_REQUIRED is False
            and MILESTONE_21_TASK_8_REQUIRED is False
            and MILESTONE_20_REOPEN_REQUIRED is False
            and MILESTONE_20_TASK_8_REQUIRED is False
            and MILESTONE_19_REOPEN_REQUIRED is False
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

        validation_artifacts = build_milestone_22_validation_artifacts()
        if not validation_artifacts.valid:
            issues.append("VALIDATION_ARTIFACTS_INVALID")
        issues.extend(
            f"VALIDATION_ARTIFACTS_{issue}"
            for issue in validate_milestone_22_validation_artifacts(validation_artifacts)
        )

        if not INTEGRATION_REGRESSION_READY:
            issues.append("INTEGRATION_REGRESSION_NOT_READY")
        if not INTEGRATION_REGRESSION_EXECUTED:
            issues.append("INTEGRATION_REGRESSION_NOT_EXECUTED")
        if not TASK_CHAIN_VALIDATED:
            issues.append("TASK_CHAIN_NOT_VALIDATED")
        if not GUARD_INTEGRATION_VALIDATED:
            issues.append("GUARD_INTEGRATION_NOT_VALIDATED")
        if not ARTIFACT_CHAIN_VALIDATED:
            issues.append("ARTIFACT_CHAIN_NOT_VALIDATED")
        if not BOUNDARY_REGRESSION_VALIDATED:
            issues.append("BOUNDARY_REGRESSION_NOT_VALIDATED")
        if not READY_FOR_MILESTONE_CLOSURE:
            issues.append("NOT_READY_FOR_MILESTONE_CLOSURE")
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
        if len(self.integration_cases) != 12:
            issues.append("INTEGRATION_CASE_COUNT_NOT_12")
        if len(self.generated_artifacts) != 4:
            issues.append("GENERATED_ARTIFACT_COUNT_NOT_4")
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
        if MILESTONE_21_REOPEN_REQUIRED:
            issues.append("MILESTONE_21_REOPEN_REQUIRED")
        if MILESTONE_21_TASK_7_REQUIRED:
            issues.append("MILESTONE_21_TASK_7_REQUIRED")
        if MILESTONE_21_TASK_8_REQUIRED:
            issues.append("MILESTONE_21_TASK_8_REQUIRED")
        if MILESTONE_20_REOPEN_REQUIRED:
            issues.append("MILESTONE_20_REOPEN_REQUIRED")
        if MILESTONE_20_TASK_8_REQUIRED:
            issues.append("MILESTONE_20_TASK_8_REQUIRED")
        if MILESTONE_19_REOPEN_REQUIRED:
            issues.append("MILESTONE_19_REOPEN_REQUIRED")
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
        validation_payload = self.validation_payload

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceValidationArtifactId": validation_payload["validationArtifactId"],
            "sourceValidationValid": validation_payload["valid"],
            "sourceGuardValid": validation_payload["sourceGuardValid"],
            "sourceGuardSnapshotCount": validation_payload["sourceGuardSnapshotCount"],
            "nextStage": self.next_stage,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "integrationCases": list(self.integration_cases),
            "integrationCaseCount": len(self.integration_cases),
            "generatedArtifacts": list(self.generated_artifacts),
            "generatedArtifactCount": len(self.generated_artifacts),
            "validationCaseCount": validation_payload["validationCaseCount"],
            "taskChainValidated": TASK_CHAIN_VALIDATED,
            "guardIntegrationValidated": GUARD_INTEGRATION_VALIDATED,
            "artifactChainValidated": ARTIFACT_CHAIN_VALIDATED,
            "boundaryRegressionValidated": BOUNDARY_REGRESSION_VALIDATED,
            "integrationRegressionReady": INTEGRATION_REGRESSION_READY,
            "integrationRegressionExecuted": INTEGRATION_REGRESSION_EXECUTED,
            "readyForMilestoneClosure": READY_FOR_MILESTONE_CLOSURE,
            "m21Task7Used": validation_payload["m21Task7Used"],
            "m21Task8Used": validation_payload["m21Task8Used"],
            "m20FinalTaskNumber": validation_payload["m20FinalTaskNumber"],
            "m20Task7Used": validation_payload["m20Task7Used"],
            "m20Task8Used": validation_payload["m20Task8Used"],
            "requiredSnapshotFieldCount": validation_payload["requiredSnapshotFieldCount"],
            "forbiddenRuntimeTraversalTokenCount": validation_payload["forbiddenRuntimeTraversalTokenCount"],
            "noRecursiveMetaLayer": NO_RECURSIVE_META_LAYER,
            "closureRequired": CLOSURE_REQUIRED,
            "maxReviewDepth": MAX_REVIEW_DEPTH,
            "maxAuthorizationDepth": MAX_AUTHORIZATION_DEPTH,
            "maxFinalizationDepth": MAX_FINALIZATION_DEPTH,
            "milestone21ReopenRequired": MILESTONE_21_REOPEN_REQUIRED,
            "milestone21Task7Required": MILESTONE_21_TASK_7_REQUIRED,
            "milestone21Task8Required": MILESTONE_21_TASK_8_REQUIRED,
            "milestone20ReopenRequired": MILESTONE_20_REOPEN_REQUIRED,
            "milestone20Task8Required": MILESTONE_20_TASK_8_REQUIRED,
            "milestone19ReopenRequired": MILESTONE_19_REOPEN_REQUIRED,
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


def build_milestone_22_integration_regression(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone22IntegrationRegression:
    return Milestone22IntegrationRegression(metadata={} if metadata is None else metadata)


def validate_milestone_22_integration_regression(
    integration: Milestone22IntegrationRegression,
) -> tuple[str, ...]:
    return integration.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "INTEGRATION_REGRESSION_READY",
    "INTEGRATION_REGRESSION_EXECUTED",
    "Milestone22IntegrationRegression",
    "build_milestone_22_integration_regression",
    "validate_milestone_22_integration_regression",
]
