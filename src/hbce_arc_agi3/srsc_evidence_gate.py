"""SRSC Evidence Gate.

Milestone #19 Task 81 - local standalone implementation.

The gate evaluates SRSC claim records under deterministic fail-closed rules.
It does not wire into solver runtime, ranking, verification, benchmark
execution, or Kaggle submission behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from hbce_arc_agi3.srsc_claim_ledger import (
    BoundaryState,
    ClaimRecord,
    ClaimState,
    EvidenceState,
    FAIL_CLOSED_ACTIVE,
    KAGGLE_SUBMISSION_SENT,
    LEGAL_CERTIFICATION,
    PRIVATE_CORE_EXPOSURE,
    RUNTIME_SOLVER_MODIFIED,
    RUNTIME_WIRING_ALLOWED,
    TASK_ID,
    stable_digest,
)


GATE_REVISION = "SRSC_EVIDENCE_GATE_LOCAL_STANDALONE_V1"


@dataclass(frozen=True)
class EvidenceGateDecision:
    """Decision emitted by the SRSC Evidence Gate."""

    claim_id: str
    gate_status: str
    approved_for_record: bool
    approved_as_verified: bool
    reasons: tuple[str, ...]
    task_id: str = TASK_ID
    gate_revision: str = GATE_REVISION
    runtime_solver_modified: bool = RUNTIME_SOLVER_MODIFIED
    runtime_wiring_allowed: bool = RUNTIME_WIRING_ALLOWED
    kaggle_submission_sent: bool = KAGGLE_SUBMISSION_SENT
    private_core_exposure: bool = PRIVATE_CORE_EXPOSURE
    legal_certification: bool = LEGAL_CERTIFICATION
    fail_closed_active: bool = FAIL_CLOSED_ACTIVE

    @property
    def decision_id(self) -> str:
        digest = stable_digest("SRSC-GATE", self.to_public_dict(include_id=False))
        return f"SRSC-GATE-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "claimId": self.claim_id,
            "gateStatus": self.gate_status,
            "approvedForRecord": self.approved_for_record,
            "approvedAsVerified": self.approved_as_verified,
            "reasons": list(self.reasons),
            "taskId": self.task_id,
            "gateRevision": self.gate_revision,
            "runtimeSolverModified": self.runtime_solver_modified,
            "runtimeWiringAllowed": self.runtime_wiring_allowed,
            "kaggleSubmissionSent": self.kaggle_submission_sent,
            "privateCoreExposure": self.private_core_exposure,
            "legalCertification": self.legal_certification,
            "failClosedActive": self.fail_closed_active,
        }
        if include_id:
            payload["decisionId"] = self.decision_id
        return payload


def evaluate_claim_record(record: ClaimRecord) -> EvidenceGateDecision:
    """Evaluate a claim record under fail-closed SRSC rules."""

    reasons: list[str] = []

    if not record.has_required_fields:
        reasons.append("REQUIRED_FIELDS_MISSING")

    if record.evidence_state != EvidenceState.PRESENT:
        reasons.append(f"EVIDENCE_STATE_{record.evidence_state.value}")

    if not record.evidence_refs:
        reasons.append("EVIDENCE_REFS_MISSING")

    if record.boundary_state != BoundaryState.PUBLIC_SAFE:
        reasons.append(f"BOUNDARY_{record.boundary_state.value}")

    if record.claim_state in {ClaimState.UNKNOWN, ClaimState.CONFLICTING, ClaimState.BLOCKED}:
        reasons.append(f"CLAIM_STATE_{record.claim_state.value}")

    approved_for_record = not reasons
    approved_as_verified = approved_for_record and record.claim_state == ClaimState.VERIFIED

    if approved_as_verified:
        gate_status = "APPROVED_VERIFIED_CLAIM"
        reasons.append("VERIFIED_WITH_PRESENT_EVIDENCE_PUBLIC_SAFE")
    elif approved_for_record:
        gate_status = "APPROVED_NON_VERIFIED_RECORD"
        reasons.append(f"RECORDABLE_{record.claim_state.value}")
    else:
        gate_status = "BLOCKED_FAIL_CLOSED"

    return EvidenceGateDecision(
        claim_id=record.claim_id,
        gate_status=gate_status,
        approved_for_record=approved_for_record,
        approved_as_verified=approved_as_verified,
        reasons=tuple(reasons),
    )


def evaluate_claim_records(records: Iterable[ClaimRecord]) -> tuple[EvidenceGateDecision, ...]:
    """Evaluate multiple claim records."""

    return tuple(evaluate_claim_record(record) for record in records)


__all__ = [
    "GATE_REVISION",
    "EvidenceGateDecision",
    "evaluate_claim_record",
    "evaluate_claim_records",
]
