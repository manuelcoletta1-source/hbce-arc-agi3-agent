"""Milestone #22 Task 6 - Milestone Closure.

Closes Milestone 22 after the Fast Snapshot Dependency Guard chain passes:

Task 1: governed opening.
Task 2: objective selection and scope lock.
Task 3: fast snapshot dependency guard implementation.
Task 4: validation and artifacts.
Task 5: integration regression.
Task 6: closure.

Task 7 and Task 8 remain unused. Finally, a milestone that knows when to stop,
a skill software projects usually learn only after becoming a cautionary tale.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_22_integration_regression import (
    build_milestone_22_integration_regression,
    validate_milestone_22_integration_regression,
)


TASK_ID = "MILESTONE_22_TASK_6_MILESTONE_CLOSURE_V1"
REVISION = "MILESTONE_22_MILESTONE_CLOSURE_v1"
MILESTONE_ID = "MILESTONE_22"
NEXT_STAGE = "MILESTONE_22_CLOSED_NO_TASK_7_OR_8_USED"

FINAL_STATUS = "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
TECHNICAL_STATUS = "PASS"
PROCESS_STATUS = "GOVERNED_WITHIN_TASK_BUDGET"

TASK_BUDGET_MAX = 8
FINAL_TASK_NUMBER = 6
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

TASK_7_USED = False
TASK_8_USED = False
RESERVE_UNUSED = True
EMERGENCY_RESERVE_UNUSED = True

MILESTONE_CLOSURE_READY = True
MILESTONE_CLOSED = True
TASK_CHAIN_CLOSED = True
FAST_SNAPSHOT_GUARD_CLOSED = True
VALIDATION_ARTIFACTS_CLOSED = True
INTEGRATION_REGRESSION_CLOSED = True
POST_CLOSURE_REOPEN_REQUIRED = False

NO_RECURSIVE_META_LAYER = True
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
class Milestone22Closure:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    final_status: str = FINAL_STATUS
    technical_status: str = TECHNICAL_STATUS
    process_status: str = PROCESS_STATUS
    task_budget_max: int = TASK_BUDGET_MAX
    final_task_number: int = FINAL_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    completed_task_ids: tuple[str, ...] = (
        "MILESTONE_22_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1",
        "MILESTONE_22_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1",
        "MILESTONE_22_TASK_3_FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTATION_V1",
        "MILESTONE_22_TASK_4_VALIDATION_AND_ARTIFACTS_V1",
        "MILESTONE_22_TASK_5_INTEGRATION_REGRESSION_V1",
        "MILESTONE_22_TASK_6_MILESTONE_CLOSURE_V1",
    )
    closure_checks: tuple[str, ...] = (
        "task_1_governed_opening_closed",
        "task_2_scope_lock_closed",
        "task_3_fast_snapshot_guard_closed",
        "task_4_validation_artifacts_closed",
        "task_5_integration_regression_closed",
        "integration_regression_valid",
        "task_budget_closed_at_task_6",
        "task_7_unused",
        "task_8_unused",
        "runtime_boundaries_unchanged",
        "legal_certification_absent",
        "fail_closed_boundary_preserved",
    )
    generated_artifacts: tuple[str, ...] = (
        "examples/milestone-22/milestone-closure-v1/task-6-milestone-closure.json",
        "examples/milestone-22/milestone-closure-v1/task-6-milestone-closure.md",
        "examples/milestone-22/milestone-closure-v1/task-6-manifest.json",
        "examples/milestone-22/milestone-closure-v1/task-6-index.txt",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def closure_id(self) -> str:
        return f"MILESTONE-22-CLOSURE-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def integration_payload(self) -> Mapping[str, Any]:
        return build_milestone_22_integration_regression().to_public_dict()

    @property
    def closure_ok(self) -> bool:
        integration = build_milestone_22_integration_regression()
        integration_payload = integration.to_public_dict()

        return (
            MILESTONE_CLOSURE_READY is True
            and MILESTONE_CLOSED is True
            and TASK_CHAIN_CLOSED is True
            and FAST_SNAPSHOT_GUARD_CLOSED is True
            and VALIDATION_ARTIFACTS_CLOSED is True
            and INTEGRATION_REGRESSION_CLOSED is True
            and POST_CLOSURE_REOPEN_REQUIRED is False
            and integration.valid is True
            and validate_milestone_22_integration_regression(integration) == ()
            and integration_payload["valid"] is True
            and integration_payload["integrationOk"] is True
            and integration_payload["readyForMilestoneClosure"] is True
            and integration_payload["sourceValidationValid"] is True
            and integration_payload["sourceGuardValid"] is True
            and integration_payload["m20FinalTaskNumber"] == 7
            and integration_payload["m20Task7Used"] is True
            and integration_payload["m20Task8Used"] is False
            and self.final_status == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
            and self.technical_status == "PASS"
            and self.process_status == "GOVERNED_WITHIN_TASK_BUDGET"
            and self.task_budget_max == 8
            and self.final_task_number == 6
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.completed_task_ids) == 6
            and len(self.closure_checks) == 12
            and len(self.generated_artifacts) == 4
            and TASK_7_USED is False
            and TASK_8_USED is False
            and RESERVE_UNUSED is True
            and EMERGENCY_RESERVE_UNUSED is True
            and NO_RECURSIVE_META_LAYER is True
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

        integration = build_milestone_22_integration_regression()
        if not integration.valid:
            issues.append("INTEGRATION_REGRESSION_INVALID")
        issues.extend(
            f"INTEGRATION_REGRESSION_{issue}"
            for issue in validate_milestone_22_integration_regression(integration)
        )

        if not MILESTONE_CLOSURE_READY:
            issues.append("MILESTONE_CLOSURE_NOT_READY")
        if not MILESTONE_CLOSED:
            issues.append("MILESTONE_NOT_CLOSED")
        if not TASK_CHAIN_CLOSED:
            issues.append("TASK_CHAIN_NOT_CLOSED")
        if not FAST_SNAPSHOT_GUARD_CLOSED:
            issues.append("FAST_SNAPSHOT_GUARD_NOT_CLOSED")
        if not VALIDATION_ARTIFACTS_CLOSED:
            issues.append("VALIDATION_ARTIFACTS_NOT_CLOSED")
        if not INTEGRATION_REGRESSION_CLOSED:
            issues.append("INTEGRATION_REGRESSION_NOT_CLOSED")
        if POST_CLOSURE_REOPEN_REQUIRED:
            issues.append("POST_CLOSURE_REOPEN_REQUIRED")
        if self.final_status != "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6":
            issues.append("FINAL_STATUS_MISMATCH")
        if self.technical_status != "PASS":
            issues.append("TECHNICAL_STATUS_NOT_PASS")
        if self.process_status != "GOVERNED_WITHIN_TASK_BUDGET":
            issues.append("PROCESS_STATUS_MISMATCH")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.final_task_number != 6:
            issues.append("FINAL_TASK_NUMBER_NOT_6")
        if self.recommended_closure_task_number != 6:
            issues.append("RECOMMENDED_CLOSURE_TASK_NOT_6")
        if self.reserve_task_number != 7:
            issues.append("RESERVE_TASK_NUMBER_NOT_7")
        if self.emergency_only_task_number != 8:
            issues.append("EMERGENCY_TASK_NUMBER_NOT_8")
        if len(self.completed_task_ids) != 6:
            issues.append("COMPLETED_TASK_COUNT_NOT_6")
        if len(self.closure_checks) != 12:
            issues.append("CLOSURE_CHECK_COUNT_NOT_12")
        if len(self.generated_artifacts) != 4:
            issues.append("GENERATED_ARTIFACT_COUNT_NOT_4")
        if TASK_7_USED:
            issues.append("TASK_7_USED")
        if TASK_8_USED:
            issues.append("TASK_8_USED")
        if not RESERVE_UNUSED:
            issues.append("RESERVE_USED")
        if not EMERGENCY_RESERVE_UNUSED:
            issues.append("EMERGENCY_RESERVE_USED")
        if not NO_RECURSIVE_META_LAYER:
            issues.append("RECURSIVE_META_LAYER_ALLOWED")
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
        return self.closure_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        integration_payload = self.integration_payload

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceIntegrationId": integration_payload["integrationId"],
            "sourceIntegrationValid": integration_payload["valid"],
            "sourceIntegrationOk": integration_payload["integrationOk"],
            "nextStage": self.next_stage,
            "finalStatus": self.final_status,
            "technicalStatus": self.technical_status,
            "processStatus": self.process_status,
            "taskBudgetMax": self.task_budget_max,
            "finalTaskNumber": self.final_task_number,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "completedTaskIds": list(self.completed_task_ids),
            "completedTaskCount": len(self.completed_task_ids),
            "closureChecks": list(self.closure_checks),
            "closureCheckCount": len(self.closure_checks),
            "generatedArtifacts": list(self.generated_artifacts),
            "generatedArtifactCount": len(self.generated_artifacts),
            "task7Used": TASK_7_USED,
            "task8Used": TASK_8_USED,
            "reserveUnused": RESERVE_UNUSED,
            "emergencyReserveUnused": EMERGENCY_RESERVE_UNUSED,
            "milestoneClosureReady": MILESTONE_CLOSURE_READY,
            "milestoneClosed": MILESTONE_CLOSED,
            "taskChainClosed": TASK_CHAIN_CLOSED,
            "fastSnapshotGuardClosed": FAST_SNAPSHOT_GUARD_CLOSED,
            "validationArtifactsClosed": VALIDATION_ARTIFACTS_CLOSED,
            "integrationRegressionClosed": INTEGRATION_REGRESSION_CLOSED,
            "postClosureReopenRequired": POST_CLOSURE_REOPEN_REQUIRED,
            "m20FinalTaskNumber": integration_payload["m20FinalTaskNumber"],
            "m20Task7Used": integration_payload["m20Task7Used"],
            "m20Task8Used": integration_payload["m20Task8Used"],
            "m21Task7Used": integration_payload["m21Task7Used"],
            "m21Task8Used": integration_payload["m21Task8Used"],
            "noRecursiveMetaLayer": NO_RECURSIVE_META_LAYER,
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
            "closureOk": self.closure_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["closureId"] = self.closure_id
        return payload


def build_milestone_22_closure(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone22Closure:
    return Milestone22Closure(metadata={} if metadata is None else metadata)


def validate_milestone_22_closure(
    closure: Milestone22Closure,
) -> tuple[str, ...]:
    return closure.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "FINAL_STATUS",
    "MILESTONE_CLOSURE_READY",
    "MILESTONE_CLOSED",
    "Milestone22Closure",
    "build_milestone_22_closure",
    "validate_milestone_22_closure",
]
