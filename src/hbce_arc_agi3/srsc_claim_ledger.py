"""SRSC Claim Ledger.

Milestone #19 Task 81 - local standalone implementation.

This module records SRSC claim metadata in a deterministic, public-safe and
fail-closed form. It does not modify solver runtime, candidate generation,
ranking, verification, benchmark execution, or Kaggle submission behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from typing import Any, Iterable, Mapping


TASK_ID = "MILESTONE_19_TASK_81_SRSC_CLAIM_LEDGER_EVIDENCE_GATE_LOCAL_IMPLEMENTATION_V1"
MODULE_REVISION = "SRSC_CLAIM_LEDGER_LOCAL_STANDALONE_V1"

RUNTIME_SOLVER_MODIFIED = False
RUNTIME_WIRING_ALLOWED = False
KAGGLE_SUBMISSION_SENT = False
PRIVATE_CORE_EXPOSURE = False
LEGAL_CERTIFICATION = False
FAIL_CLOSED_ACTIVE = True


class ClaimState(str, Enum):
    """Allowed SRSC epistemic claim states."""

    VERIFIED = "VERIFIED"
    REPORTED = "REPORTED"
    INFERRED = "INFERRED"
    HYPOTHESIS = "HYPOTHESIS"
    UNKNOWN = "UNKNOWN"
    CONFLICTING = "CONFLICTING"
    BLOCKED = "BLOCKED"


class EvidenceState(str, Enum):
    """Evidence availability state."""

    PRESENT = "PRESENT"
    MISSING = "MISSING"
    CONFLICTING = "CONFLICTING"
    UNSUPPORTED = "UNSUPPORTED"


class BoundaryState(str, Enum):
    """Boundary state for public-safe local records."""

    PUBLIC_SAFE = "PUBLIC_SAFE"
    BLOCKED_PRIVATE = "BLOCKED_PRIVATE"
    BLOCKED_RUNTIME = "BLOCKED_RUNTIME"
    BLOCKED_SUBMISSION = "BLOCKED_SUBMISSION"
    BLOCKED_UNKNOWN = "BLOCKED_UNKNOWN"


BLOCKED_CLAIM_STATES = {
    ClaimState.UNKNOWN,
    ClaimState.CONFLICTING,
    ClaimState.BLOCKED,
}

OPEN_CLAIM_STATES = {
    ClaimState.VERIFIED,
    ClaimState.REPORTED,
    ClaimState.INFERRED,
    ClaimState.HYPOTHESIS,
}


def _clean_text(value: str) -> str:
    cleaned = " ".join(str(value).strip().split())
    if not cleaned:
        raise ValueError("SRSC text field cannot be empty")
    return cleaned


def _clean_optional_mapping(value: Mapping[str, Any] | None) -> dict[str, Any]:
    if value is None:
        return {}
    return {str(key): value[key] for key in sorted(value)}


def _clean_refs(values: Iterable[str]) -> tuple[str, ...]:
    refs = tuple(_clean_text(value) for value in values if str(value).strip())
    return tuple(dict.fromkeys(refs))


def stable_json(payload: Mapping[str, Any]) -> str:
    """Return deterministic JSON for hashing and audit records."""

    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def stable_digest(prefix: str, payload: Mapping[str, Any]) -> str:
    """Return deterministic SHA-256 digest for a payload."""

    raw = f"{prefix}:{stable_json(payload)}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True)
class ClaimRecord:
    """Deterministic SRSC claim record.

    The record can be stored in a local ledger only when evidence, scope,
    claim state and boundary are explicit. Claims with missing evidence or
    blocked boundaries remain fail-closed.
    """

    claim_text: str
    claim_state: ClaimState
    evidence_state: EvidenceState
    evidence_refs: tuple[str, ...]
    scope: str
    boundary_state: BoundaryState = BoundaryState.PUBLIC_SAFE
    source_task: str = TASK_ID
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "claim_text", _clean_text(self.claim_text))
        object.__setattr__(self, "claim_state", ClaimState(self.claim_state))
        object.__setattr__(self, "evidence_state", EvidenceState(self.evidence_state))
        object.__setattr__(self, "evidence_refs", _clean_refs(self.evidence_refs))
        object.__setattr__(self, "scope", _clean_text(self.scope))
        object.__setattr__(self, "boundary_state", BoundaryState(self.boundary_state))
        object.__setattr__(self, "source_task", _clean_text(self.source_task))
        object.__setattr__(self, "metadata", _clean_optional_mapping(self.metadata))

    @property
    def claim_id(self) -> str:
        digest = stable_digest("SRSC-CLAIM", self.to_public_dict(include_id=False))
        return f"SRSC-CLAIM-{digest[:16].upper()}"

    @property
    def has_required_fields(self) -> bool:
        return bool(self.claim_text and self.scope and self.claim_state and self.boundary_state)

    @property
    def has_evidence(self) -> bool:
        return self.evidence_state == EvidenceState.PRESENT and bool(self.evidence_refs)

    @property
    def is_public_safe(self) -> bool:
        return self.boundary_state == BoundaryState.PUBLIC_SAFE

    @property
    def is_blocked_by_state(self) -> bool:
        return self.claim_state in BLOCKED_CLAIM_STATES

    @property
    def is_recordable(self) -> bool:
        return (
            self.has_required_fields
            and self.has_evidence
            and self.is_public_safe
            and not self.is_blocked_by_state
        )

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "claimText": self.claim_text,
            "claimState": self.claim_state.value,
            "evidenceState": self.evidence_state.value,
            "evidenceRefs": list(self.evidence_refs),
            "scope": self.scope,
            "boundaryState": self.boundary_state.value,
            "sourceTask": self.source_task,
            "metadata": dict(self.metadata),
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
            "privateCoreExposure": PRIVATE_CORE_EXPOSURE,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
        }
        if include_id:
            payload["claimId"] = self.claim_id
        return payload


@dataclass(frozen=True)
class ClaimLedger:
    """Immutable local SRSC ledger."""

    records: tuple[ClaimRecord, ...] = ()

    def add(self, record: ClaimRecord) -> "ClaimLedger":
        if not record.is_recordable:
            raise ValueError("SRSC claim is not recordable under fail-closed policy")
        if self.get(record.claim_id) is not None:
            return self
        return ClaimLedger(records=self.records + (record,))

    def get(self, claim_id: str) -> ClaimRecord | None:
        for record in self.records:
            if record.claim_id == claim_id:
                return record
        return None

    @property
    def record_count(self) -> int:
        return len(self.records)

    @property
    def ledger_id(self) -> str:
        digest = stable_digest("SRSC-LEDGER", self.to_public_dict(include_id=False))
        return f"SRSC-LEDGER-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "taskId": TASK_ID,
            "moduleRevision": MODULE_REVISION,
            "recordCount": self.record_count,
            "records": [record.to_public_dict() for record in self.records],
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
            "privateCoreExposure": PRIVATE_CORE_EXPOSURE,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
        }
        if include_id:
            payload["ledgerId"] = self.ledger_id
        return payload


def create_claim_record(
    *,
    claim_text: str,
    claim_state: ClaimState | str,
    evidence_state: EvidenceState | str,
    evidence_refs: Iterable[str],
    scope: str,
    boundary_state: BoundaryState | str = BoundaryState.PUBLIC_SAFE,
    source_task: str = TASK_ID,
    metadata: Mapping[str, Any] | None = None,
) -> ClaimRecord:
    """Create a deterministic SRSC claim record."""

    return ClaimRecord(
        claim_text=claim_text,
        claim_state=ClaimState(claim_state),
        evidence_state=EvidenceState(evidence_state),
        evidence_refs=tuple(evidence_refs),
        scope=scope,
        boundary_state=BoundaryState(boundary_state),
        source_task=source_task,
        metadata=metadata or {},
    )


__all__ = [
    "BLOCKED_CLAIM_STATES",
    "FAIL_CLOSED_ACTIVE",
    "KAGGLE_SUBMISSION_SENT",
    "LEGAL_CERTIFICATION",
    "MODULE_REVISION",
    "PRIVATE_CORE_EXPOSURE",
    "RUNTIME_SOLVER_MODIFIED",
    "RUNTIME_WIRING_ALLOWED",
    "TASK_ID",
    "BoundaryState",
    "ClaimLedger",
    "ClaimRecord",
    "ClaimState",
    "EvidenceState",
    "create_claim_record",
    "stable_digest",
    "stable_json",
]
