"""Milestone #24 Task 1 - Governed Opening With Task Budget.

Opens Milestone 24 from the closed Milestone 23 snapshot registry closure.

Task 1 only opens the milestone, imports the previous closure as a source
snapshot, and fixes the task budget. No implementation begins here. Shocking,
yes: a beginning that behaves like a beginning instead of pretending to be the
entire project in a fake moustache.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping

from hbce_arc_agi3.milestone_23_closure import (
    build_milestone_23_closure,
    validate_milestone_23_closure,
)


TASK_ID = "MILESTONE_24_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
REVISION = "MILESTONE_24_GOVERNED_OPENING_WITH_TASK_BUDGET_v1"
MILESTONE_ID = "MILESTONE_24"
NEXT_STAGE = "MILESTONE_24_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"

SOURCE_MILESTONE_ID = "MILESTONE_23"
SOURCE_FINAL_STATUS = "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
SOURCE_TECHNICAL_STATUS = "PASS"
SOURCE_PROCESS_STATUS = "GOVERNED_WITHIN_TASK_BUDGET"
SOURCE_FINAL_TASK_NUMBER = 6
SOURCE_TASK_BUDGET_MAX = 8
SOURCE_TASK_7_USED = False
SOURCE_TASK_8_USED = False
SOURCE_RESERVE_UNUSED = True
SOURCE_EMERGENCY_RESERVE_UNUSED = True
SOURCE_MILESTONE_CLOSED = True

TASK_BUDGET_MIN = 4
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 1
RECOMMENDED_CLOSURE_TASK_NUMBER = 6
RESERVE_TASK_NUMBER = 7
EMERGENCY_ONLY_TASK_NUMBER = 8

GOVERNED_OPENING_READY = True
TASK_BUDGET_LOCKED = True
OBJECTIVE_SELECTION_REQUIRED_NEXT = True
SCOPE_LOCK_REQUIRED_NEXT = True
IMPLEMENTATION_STARTED = False
IMPLEMENTATION_ALLOWED_AT_TASK_1 = False

FAST_SNAPSHOT_DEPENDENCY_MODE = True
DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED = False
SOURCE_CLOSURE_SNAPSHOT_REQUIRED = True
DOCUMENT_MARKER_EVIDENCE_REQUIRED = True

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
class Milestone24GovernedOpening:
    milestone_id: str = MILESTONE_ID
    task_id: str = TASK_ID
    next_stage: str = NEXT_STAGE
    task_budget_min: int = TASK_BUDGET_MIN
    task_budget_max: int = TASK_BUDGET_MAX
    current_task_number: int = CURRENT_TASK_NUMBER
    recommended_closure_task_number: int = RECOMMENDED_CLOSURE_TASK_NUMBER
    reserve_task_number: int = RESERVE_TASK_NUMBER
    emergency_only_task_number: int = EMERGENCY_ONLY_TASK_NUMBER
    opening_checks: tuple[str, ...] = (
        "source_milestone_23_closure_valid",
        "source_final_status_preserved",
        "source_technical_status_pass",
        "source_process_status_governed",
        "source_final_task_number_6",
        "source_task_budget_max_8",
        "source_task_7_unused",
        "source_task_8_unused",
        "task_budget_min_4",
        "task_budget_max_8",
        "implementation_not_started",
        "objective_scope_lock_required_next",
    )
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def opening_id(self) -> str:
        return f"MILESTONE-24-GOVERNED-OPENING-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def source_closure_payload(self) -> Mapping[str, Any]:
        return build_milestone_23_closure().to_public_dict()

    @property
    def opening_ok(self) -> bool:
        source = build_milestone_23_closure()
        source_payload = source.to_public_dict()

        return (
            GOVERNED_OPENING_READY is True
            and TASK_BUDGET_LOCKED is True
            and OBJECTIVE_SELECTION_REQUIRED_NEXT is True
            and SCOPE_LOCK_REQUIRED_NEXT is True
            and IMPLEMENTATION_STARTED is False
            and IMPLEMENTATION_ALLOWED_AT_TASK_1 is False
            and source.valid is True
            and validate_milestone_23_closure(source) == ()
            and source_payload["valid"] is True
            and source_payload["closureOk"] is True
            and source_payload["milestoneClosed"] is True
            and source_payload["finalStatus"] == SOURCE_FINAL_STATUS
            and source_payload["technicalStatus"] == SOURCE_TECHNICAL_STATUS
            and source_payload["processStatus"] == SOURCE_PROCESS_STATUS
            and source_payload["finalTaskNumber"] == SOURCE_FINAL_TASK_NUMBER
            and source_payload["taskBudgetMax"] == SOURCE_TASK_BUDGET_MAX
            and source_payload["task7Used"] is SOURCE_TASK_7_USED
            and source_payload["task8Used"] is SOURCE_TASK_8_USED
            and source_payload["reserveUnused"] is SOURCE_RESERVE_UNUSED
            and source_payload["emergencyReserveUnused"] is SOURCE_EMERGENCY_RESERVE_UNUSED
            and source_payload["noTask7Or8Used"] is True
            and self.task_budget_min == 4
            and self.task_budget_max == 8
            and self.current_task_number == 1
            and self.recommended_closure_task_number == 6
            and self.reserve_task_number == 7
            and self.emergency_only_task_number == 8
            and len(self.opening_checks) == 12
            and FAST_SNAPSHOT_DEPENDENCY_MODE is True
            and DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED is False
            and SOURCE_CLOSURE_SNAPSHOT_REQUIRED is True
            and DOCUMENT_MARKER_EVIDENCE_REQUIRED is True
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
        source = build_milestone_23_closure()
        source_payload = source.to_public_dict()

        if not source.valid:
            issues.append("SOURCE_MILESTONE_23_CLOSURE_INVALID")
        issues.extend(f"SOURCE_MILESTONE_23_CLOSURE_{issue}" for issue in validate_milestone_23_closure(source))
        if source_payload["finalStatus"] != SOURCE_FINAL_STATUS:
            issues.append("SOURCE_FINAL_STATUS_MISMATCH")
        if source_payload["technicalStatus"] != SOURCE_TECHNICAL_STATUS:
            issues.append("SOURCE_TECHNICAL_STATUS_NOT_PASS")
        if source_payload["processStatus"] != SOURCE_PROCESS_STATUS:
            issues.append("SOURCE_PROCESS_STATUS_MISMATCH")
        if source_payload["finalTaskNumber"] != SOURCE_FINAL_TASK_NUMBER:
            issues.append("SOURCE_FINAL_TASK_NUMBER_NOT_6")
        if source_payload["taskBudgetMax"] != SOURCE_TASK_BUDGET_MAX:
            issues.append("SOURCE_TASK_BUDGET_MAX_NOT_8")
        if source_payload["task7Used"] is not False:
            issues.append("SOURCE_TASK_7_USED")
        if source_payload["task8Used"] is not False:
            issues.append("SOURCE_TASK_8_USED")
        if not GOVERNED_OPENING_READY:
            issues.append("GOVERNED_OPENING_NOT_READY")
        if not TASK_BUDGET_LOCKED:
            issues.append("TASK_BUDGET_NOT_LOCKED")
        if not OBJECTIVE_SELECTION_REQUIRED_NEXT:
            issues.append("OBJECTIVE_SELECTION_NOT_REQUIRED_NEXT")
        if not SCOPE_LOCK_REQUIRED_NEXT:
            issues.append("SCOPE_LOCK_NOT_REQUIRED_NEXT")
        if IMPLEMENTATION_STARTED:
            issues.append("IMPLEMENTATION_STARTED_AT_TASK_1")
        if IMPLEMENTATION_ALLOWED_AT_TASK_1:
            issues.append("IMPLEMENTATION_ALLOWED_AT_TASK_1")
        if self.task_budget_min != 4:
            issues.append("TASK_BUDGET_MIN_NOT_4")
        if self.task_budget_max != 8:
            issues.append("TASK_BUDGET_MAX_NOT_8")
        if self.current_task_number != 1:
            issues.append("CURRENT_TASK_NUMBER_NOT_1")
        if self.recommended_closure_task_number != 6:
            issues.append("RECOMMENDED_CLOSURE_TASK_NOT_6")
        if self.reserve_task_number != 7:
            issues.append("RESERVE_TASK_NUMBER_NOT_7")
        if self.emergency_only_task_number != 8:
            issues.append("EMERGENCY_TASK_NUMBER_NOT_8")
        if len(self.opening_checks) != 12:
            issues.append("OPENING_CHECK_COUNT_NOT_12")
        if not FAST_SNAPSHOT_DEPENDENCY_MODE:
            issues.append("FAST_SNAPSHOT_DEPENDENCY_MODE_DISABLED")
        if DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED:
            issues.append("DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED")
        if not SOURCE_CLOSURE_SNAPSHOT_REQUIRED:
            issues.append("SOURCE_CLOSURE_SNAPSHOT_NOT_REQUIRED")
        if not DOCUMENT_MARKER_EVIDENCE_REQUIRED:
            issues.append("DOCUMENT_MARKER_EVIDENCE_NOT_REQUIRED")
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
        return self.opening_ok and self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        source_payload = self.source_closure_payload

        payload = {
            "taskId": self.task_id,
            "milestoneId": self.milestone_id,
            "revision": REVISION,
            "sourceMilestoneId": SOURCE_MILESTONE_ID,
            "sourceClosureId": source_payload["closureId"],
            "sourceClosureValid": source_payload["valid"],
            "sourceClosureOk": source_payload["closureOk"],
            "sourceMilestoneClosed": source_payload["milestoneClosed"],
            "sourceFinalStatus": source_payload["finalStatus"],
            "sourceTechnicalStatus": source_payload["technicalStatus"],
            "sourceProcessStatus": source_payload["processStatus"],
            "sourceFinalTaskNumber": source_payload["finalTaskNumber"],
            "sourceTaskBudgetMax": source_payload["taskBudgetMax"],
            "sourceTask7Used": source_payload["task7Used"],
            "sourceTask8Used": source_payload["task8Used"],
            "sourceReserveUnused": source_payload["reserveUnused"],
            "sourceEmergencyReserveUnused": source_payload["emergencyReserveUnused"],
            "nextStage": self.next_stage,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "currentTaskNumber": self.current_task_number,
            "remainingBudgetAfterCurrentTask": self.task_budget_max - self.current_task_number,
            "recommendedClosureTaskNumber": self.recommended_closure_task_number,
            "reserveTaskNumber": self.reserve_task_number,
            "emergencyOnlyTaskNumber": self.emergency_only_task_number,
            "openingChecks": list(self.opening_checks),
            "openingCheckCount": len(self.opening_checks),
            "governedOpeningReady": GOVERNED_OPENING_READY,
            "taskBudgetLocked": TASK_BUDGET_LOCKED,
            "objectiveSelectionRequiredNext": OBJECTIVE_SELECTION_REQUIRED_NEXT,
            "scopeLockRequiredNext": SCOPE_LOCK_REQUIRED_NEXT,
            "implementationStarted": IMPLEMENTATION_STARTED,
            "implementationAllowedAtTask1": IMPLEMENTATION_ALLOWED_AT_TASK_1,
            "fastSnapshotDependencyMode": FAST_SNAPSHOT_DEPENDENCY_MODE,
            "deepRecursiveDependencyTraversalAllowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
            "sourceClosureSnapshotRequired": SOURCE_CLOSURE_SNAPSHOT_REQUIRED,
            "documentMarkerEvidenceRequired": DOCUMENT_MARKER_EVIDENCE_REQUIRED,
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
            "openingOk": self.opening_ok,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
        }
        if include_id:
            payload["openingId"] = self.opening_id
        return payload


def build_milestone_24_governed_opening(
    *,
    metadata: Mapping[str, Any] | None = None,
) -> Milestone24GovernedOpening:
    return Milestone24GovernedOpening(metadata={} if metadata is None else metadata)


def validate_milestone_24_governed_opening(
    opening: Milestone24GovernedOpening,
) -> tuple[str, ...]:
    return opening.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "NEXT_STAGE",
    "GOVERNED_OPENING_READY",
    "TASK_BUDGET_LOCKED",
    "Milestone24GovernedOpening",
    "build_milestone_24_governed_opening",
    "validate_milestone_24_governed_opening",
]
