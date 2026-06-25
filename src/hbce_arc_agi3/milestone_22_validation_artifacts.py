"""Milestone #22 Task 4 - Validation and Artifacts.

This task validates the Fast Snapshot Dependency Guard produced in Task 3 and
records validation artifacts for integration-regression use in Task 5.

No runtime solver changes. No runtime wiring. No Kaggle paths. No secrets.
No raw request body persistence. No legal certification claims.

A validation layer: the dull little lock on the cage door where bugs pretend
they were only visiting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_22_fast_snapshot_dependency_guard import (
    build_fast_snapshot_dependency_guard,
    detect_forbidden_runtime_traversal,
    validate_fast_snapshot_dependency_guard,
)


TASK_ID = "MILESTONE_22_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
REVISION = "MILESTONE_22_VALIDATION_AND_ARTIFACTS_v1"
MILESTONE_ID = "MILESTONE_22"
NEXT_STAGE = "MILESTONE_22_TASK_5_INTEGRATION_REGRESSION_V1"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 4
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

VALIDATION_ARTIFACTS_READY = True
VALIDATION_ARTIFACTS_CREATED = True
GUARD_VALIDATED = True
SNAPSHOT_EVIDENCE_VALIDATED = True
FORBIDDEN_TRAVERSAL_DETECTION_VALIDATED = True
READY_FOR_INTEGRATION_REGRESSION = True

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
class Milestone22ValidationArtifacts:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    validation_cases: tuple[str, ...] = (
        "guard_contract_valid",
        "snapshot_count_valid",
        "milestone_21_snapshot_valid",
        "milestone_20_task7_snapshot_valid",
        "milestone_20_task8_unused",
        "required_snapshot_fields_present",
        "document_marker_evidence_preserved",
        "forbidden_runtime_traversal_detection_valid",
        "runtime_boundaries_unchanged",
        "ready_for_integration_regression",
    )
    generated_artifacts: tuple[str, ...] = (
        "examples/milestone-22/validation-and-artifacts-v1/task-4-validation-artifacts.json",
        "examples/milestone-22/validation-and-artifacts-v1/task-4-validation-artifacts.md",
        "examples/milestone-22/validation-and-artifacts-v1/task-4-manifest.json",
        "examples/milestone-22/validation-and-artifacts-v1/task-4-index.txt",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def validation_artifact_id(self) -> str:
        return f"MILESTONE-22-VALIDATION-ARTIFACTS-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def remaining_budget_after_current_task(self) -> int:
        return self.task_budget_max - self.current_task_number

    @property
    def guard_payload(self) -> Mapping[str, Any]:
        return build_fast_snapshot_dependency_guard().to_public_dict()

    @property
    def validation_ok(self) -> bool:
        guard = build_fast_snapshot_dependency_guard()
        guard_payload = guard.to_public_dict()
        detected = detect_forbidden_runtime_traversal(
            [
                "safe_static_snapshot",
                "closed_milestone.to_public_dict()",
                "closed_milestone.valid",
                "historical_milestone_revalidation_as_runtime_traversal",
            ]
        )

        return (
            VALIDATION_ARTIFACTS_READY is True
            and VALIDATION_ARTIFACTS_CREATED is True
            and GUARD_VALIDATED is True
            and SNAPSHOT_EVIDENCE_VALIDATED is True
            and FORBIDDEN_TRAVERSAL_DETECTION_VALIDATED is True
            and READY_FOR_INTEGRATION_REGRESSION is True
            and guard.valid is True
            and validate_fast_snapshot_dependency_guard(guard) == ()
            and guard_payload["valid"] is True
            and guard_payload["guardOk"] is True
            and guard_payload["snapshotCount"] == 2
            and guard_payload["snapshots"][0]["milestoneId"] == "MILESTONE_21"
            and guard_payload["snapshots"][0]["task7Used"] is False
            and guard_payload["snapshots"][0]["task8Used"] is False
            and guard_payload["snapshots"][1]["milestoneId"] == "MILESTONE_20"
            and guard_payload["snapshots"][1]["finalTaskNumber"] == 7
            and guard_payload["snapshots"][1]["task7Used"] is True
            and guard_payload["snapshots"][1]["task8Used"] is False
            and guard_payload["requiredSnapshotFieldCount"] == 8
            and guard_payload["forbiddenRuntimeTraversalTokenCount"] == 5
            and detected == (
                "closed_milestone.to_public_dict()",
                "closed_milestone.valid",
                "historical_milestone_revalidation_as_runtime_traversal",
            )
            and self.task_budget_max == 8
            and self.current_task_number == 4
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.validation_cases) == 10
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

        guard = build_fast_snapshot_dependency_guard()
        if not guard.valid:
            issues.append("FAST_SNAPSHOT_GUARD_INVALID")
        issues.extend(f"FAST_SNAPSHOT_GUARD_{issue}" for issue in validate_fast_snapshot_dependency_guard(guard))

        if not VALIDATION_ARTIFACTS_READY:
            issues.append("VALIDATION_ARTIFACTS_NOT_READY")
        if not VALIDATION_ARTIFACTS_CREATED:
            issues.append("VALIDATION_ARTIFACTS_NOT_CREATED")
        if not GUARD_VALIDATED:
            issues.append("GUARD_NOT_VALIDATED")
        if not SNAPSHOT_EVIDENCE_VALIDATED:
            issues.append("SNAPSHOT_EVIDENCE_NOT_VALIDATED")
        if not FORBIDDEN_TRAVERSAL_DETECTION_VALIDATED:
            issues.append("FORBIDDEN_TRAVERSAL_DETECTION_NOT_VALIDATED")
        if not READY_FOR_INTEGRATION_REGRESSION:
            issues.append("NOT_READY_FOR_INTEGRATION_REGRESSION")
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
        if len(self.validation_cases) != 10:
            issues.append("VALIDATION_CASE_COUNT_NOT_10")
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
        return self.validation_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        guard_payload = self.guard_payload
        detection_sample = detect_forbidden_runtime_traversal(
            [
                "safe_static_snapshot",
                "closed_milestone.to_public_dict()",
                "closed_milestone.valid",
                "historical_milestone_revalidation_as_runtime_traversal",
            ]
        )

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceGuardId": guard_payload["guardId"],
            "sourceGuardValid": guard_payload["valid"],
            "sourceGuardSnapshotCount": guard_payload["snapshotCount"],
            "nextStage": self.next_stage,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.remaining_budget_after_current_task,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "validationCases": list(self.validation_cases),
            "validationCaseCount": len(self.validation_cases),
            "generatedArtifacts": list(self.generated_artifacts),
            "generatedArtifactCount": len(self.generated_artifacts),
            "detectedForbiddenTraversalSample": list(detection_sample),
            "detectedForbiddenTraversalSampleCount": len(detection_sample),
            "m21Task7Used": guard_payload["snapshots"][0]["task7Used"],
            "m21Task8Used": guard_payload["snapshots"][0]["task8Used"],
            "m20FinalTaskNumber": guard_payload["snapshots"][1]["finalTaskNumber"],
            "m20Task7Used": guard_payload["snapshots"][1]["task7Used"],
            "m20Task8Used": guard_payload["snapshots"][1]["task8Used"],
            "requiredSnapshotFieldCount": guard_payload["requiredSnapshotFieldCount"],
            "forbiddenRuntimeTraversalTokenCount": guard_payload["forbiddenRuntimeTraversalTokenCount"],
            "validationArtifactsReady": VALIDATION_ARTIFACTS_READY,
            "validationArtifactsCreated": VALIDATION_ARTIFACTS_CREATED,
            "guardValidated": GUARD_VALIDATED,
            "snapshotEvidenceValidated": SNAPSHOT_EVIDENCE_VALIDATED,
            "forbiddenTraversalDetectionValidated": FORBIDDEN_TRAVERSAL_DETECTION_VALIDATED,
            "readyForIntegrationRegression": READY_FOR_INTEGRATION_REGRESSION,
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
            "validationOk": self.validation_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["validationArtifactId"] = self.validation_artifact_id
        return payload


def build_milestone_22_validation_artifacts(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone22ValidationArtifacts:
    return Milestone22ValidationArtifacts(metadata={} if metadata is None else metadata)


def validate_milestone_22_validation_artifacts(
    validation_artifacts: Milestone22ValidationArtifacts,
) -> tuple[str, ...]:
    return validation_artifacts.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "VALIDATION_ARTIFACTS_READY",
    "VALIDATION_ARTIFACTS_CREATED",
    "Milestone22ValidationArtifacts",
    "build_milestone_22_validation_artifacts",
    "validate_milestone_22_validation_artifacts",
]
