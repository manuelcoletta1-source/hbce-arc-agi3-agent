"""SRSC Diagnostic Reference Record schema.

Milestone #19 Task 85 - local standalone schema implementation.

This module defines deterministic local records that allow diagnostic artifacts
to reference SRSC Claim Ledger and SRSC Evidence Gate identifiers without
creating solver runtime wiring, benchmark claims, or Kaggle submission behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import json
from typing import Any, Iterable, Mapping

from hbce_arc_agi3.srsc_claim_ledger import (
    ClaimState,
    EvidenceState,
    FAIL_CLOSED_ACTIVE,
    KAGGLE_SUBMISSION_SENT,
    LEGAL_CERTIFICATION,
    PRIVATE_CORE_EXPOSURE,
    RUNTIME_SOLVER_MODIFIED,
    RUNTIME_WIRING_ALLOWED,
    stable_digest,
)


TASK_ID = "MILESTONE_19_TASK_85_SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_LOCAL_IMPLEMENTATION_V1"
SCHEMA_REVISION = "SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_LOCAL_STANDALONE_V1"

RUNTIME_ACTIVATION_AUTHORIZED = False
CANDIDATE_GENERATOR_MODIFIED = False
RANKER_MODIFIED = False
VERIFIER_MODIFIED = False
BENCHMARK_SCORE_CLAIMED = False
REAL_EVALUATION_PERFORMED = False
REAL_SUBMISSION_AUTHORIZED = False
KAGGLE_AUTHENTICATION_PERFORMED = False
INTERNET_DURING_EVAL = False
EXTERNAL_API_DEPENDENCY = False


class DiagnosticReferenceSourceType(str, Enum):
    """Allowed public-safe diagnostic source types."""

    CROSS_TRACE_DIAGNOSTIC_PLANNER_RECORD = "CROSS_TRACE_DIAGNOSTIC_PLANNER_RECORD"
    PUBLIC_SAFE_AUDIT_SUMMARY = "PUBLIC_SAFE_AUDIT_SUMMARY"
    LOCAL_CLAIM_REVIEW_REPORT = "LOCAL_CLAIM_REVIEW_REPORT"
    EVIDENCE_BOUND_DIAGNOSTIC_NOTE = "EVIDENCE_BOUND_DIAGNOSTIC_NOTE"
    MILESTONE_CLOSURE_RECORD = "MILESTONE_CLOSURE_RECORD"
    SOURCE_FILE_EVIDENCE_NOTE = "SOURCE_FILE_EVIDENCE_NOTE"


class DiagnosticReferenceBoundary(str, Enum):
    """Boundary state for local diagnostic reference records."""

    PUBLIC_SAFE = "PUBLIC_SAFE"
    BLOCKED_MISSING_SCOPE = "BLOCKED_MISSING_SCOPE"
    BLOCKED_MISSING_EVIDENCE = "BLOCKED_MISSING_EVIDENCE"
    BLOCKED_RUNTIME_WIRING = "BLOCKED_RUNTIME_WIRING"
    BLOCKED_SUBMISSION = "BLOCKED_SUBMISSION"
    BLOCKED_PRIVATE_CORE = "BLOCKED_PRIVATE_CORE"
    BLOCKED_LEGAL_CERTIFICATION = "BLOCKED_LEGAL_CERTIFICATION"
    BLOCKED_UNKNOWN = "BLOCKED_UNKNOWN"


def _clean_text(value: str) -> str:
    cleaned = " ".join(str(value).strip().split())
    if not cleaned:
        raise ValueError("SRSC diagnostic reference text field cannot be empty")
    return cleaned


def _clean_refs(values: Iterable[str]) -> tuple[str, ...]:
    refs = tuple(_clean_text(value) for value in values if str(value).strip())
    return tuple(dict.fromkeys(refs))


def _clean_optional_mapping(value: Mapping[str, Any] | None) -> dict[str, Any]:
    if value is None:
        return {}
    return {str(key): value[key] for key in sorted(value)}


@dataclass(frozen=True)
class SrscDiagnosticReferenceRecord:
    """Deterministic local SRSC diagnostic reference record.

    The record links a diagnostic artifact to SRSC claim and gate identifiers.
    It is not an adapter. It does not alter solver runtime behavior.
    """

    source_type: DiagnosticReferenceSourceType
    source_path: str
    srsc_claim_id: str
    srsc_gate_decision_id: str
    claim_state: ClaimState
    evidence_state: EvidenceState
    evidence_refs: tuple[str, ...]
    diagnostic_scope: str
    boundary_state: DiagnosticReferenceBoundary = DiagnosticReferenceBoundary.PUBLIC_SAFE
    approved_for_record: bool = False
    approved_as_verified: bool = False
    source_task: str = TASK_ID
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_type", DiagnosticReferenceSourceType(self.source_type))
        object.__setattr__(self, "source_path", _clean_text(self.source_path))
        object.__setattr__(self, "srsc_claim_id", _clean_text(self.srsc_claim_id))
        object.__setattr__(self, "srsc_gate_decision_id", _clean_text(self.srsc_gate_decision_id))
        object.__setattr__(self, "claim_state", ClaimState(self.claim_state))
        object.__setattr__(self, "evidence_state", EvidenceState(self.evidence_state))
        object.__setattr__(self, "evidence_refs", _clean_refs(self.evidence_refs))
        object.__setattr__(self, "diagnostic_scope", _clean_text(self.diagnostic_scope))
        object.__setattr__(self, "boundary_state", DiagnosticReferenceBoundary(self.boundary_state))
        object.__setattr__(self, "approved_for_record", bool(self.approved_for_record))
        object.__setattr__(self, "approved_as_verified", bool(self.approved_as_verified))
        object.__setattr__(self, "source_task", _clean_text(self.source_task))
        object.__setattr__(self, "metadata", _clean_optional_mapping(self.metadata))

    @property
    def diagnostic_reference_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-REFERENCE", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-REF-{digest[:16].upper()}"

    @property
    def has_srsc_identifiers(self) -> bool:
        return self.srsc_claim_id.startswith("SRSC-CLAIM-") and self.srsc_gate_decision_id.startswith("SRSC-GATE-")

    @property
    def has_required_scope(self) -> bool:
        return bool(self.source_path and self.diagnostic_scope and self.source_type)

    @property
    def has_evidence(self) -> bool:
        return self.evidence_state == EvidenceState.PRESENT and bool(self.evidence_refs)

    @property
    def is_public_safe(self) -> bool:
        return self.boundary_state == DiagnosticReferenceBoundary.PUBLIC_SAFE

    @property
    def is_runtime_isolated(self) -> bool:
        return (
            RUNTIME_ACTIVATION_AUTHORIZED is False
            and RUNTIME_SOLVER_MODIFIED is False
            and RUNTIME_WIRING_ALLOWED is False
            and CANDIDATE_GENERATOR_MODIFIED is False
            and RANKER_MODIFIED is False
            and VERIFIER_MODIFIED is False
            and KAGGLE_SUBMISSION_SENT is False
        )

    @property
    def is_valid_reference(self) -> bool:
        if not self.has_required_scope:
            return False
        if not self.has_srsc_identifiers:
            return False
        if not self.has_evidence:
            return False
        if not self.is_public_safe:
            return False
        if not self.is_runtime_isolated:
            return False
        if self.approved_as_verified and not self.approved_for_record:
            return False
        if self.approved_as_verified and self.claim_state != ClaimState.VERIFIED:
            return False
        if self.claim_state in {ClaimState.UNKNOWN, ClaimState.CONFLICTING, ClaimState.BLOCKED}:
            return False
        return True

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "taskId": TASK_ID,
            "schemaRevision": SCHEMA_REVISION,
            "sourceType": self.source_type.value,
            "sourcePath": self.source_path,
            "srscClaimId": self.srsc_claim_id,
            "srscGateDecisionId": self.srsc_gate_decision_id,
            "claimState": self.claim_state.value,
            "evidenceState": self.evidence_state.value,
            "evidenceRefs": list(self.evidence_refs),
            "diagnosticScope": self.diagnostic_scope,
            "boundaryState": self.boundary_state.value,
            "approvedForRecord": self.approved_for_record,
            "approvedAsVerified": self.approved_as_verified,
            "sourceTask": self.source_task,
            "metadata": dict(self.metadata),
            "runtimeActivationAuthorized": RUNTIME_ACTIVATION_AUTHORIZED,
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED,
            "candidateGeneratorModified": CANDIDATE_GENERATOR_MODIFIED,
            "rankerModified": RANKER_MODIFIED,
            "verifierModified": VERIFIER_MODIFIED,
            "benchmarkScoreClaimed": BENCHMARK_SCORE_CLAIMED,
            "realEvaluationPerformed": REAL_EVALUATION_PERFORMED,
            "realSubmissionAuthorized": REAL_SUBMISSION_AUTHORIZED,
            "kaggleAuthenticationPerformed": KAGGLE_AUTHENTICATION_PERFORMED,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
            "internetDuringEval": INTERNET_DURING_EVAL,
            "externalApiDependency": EXTERNAL_API_DEPENDENCY,
            "privateCoreExposure": PRIVATE_CORE_EXPOSURE,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
            "validReference": self.is_valid_reference,
        }
        if include_id:
            payload["diagnosticReferenceId"] = self.diagnostic_reference_id
        return payload

    def to_json(self) -> str:
        """Return deterministic public JSON."""

        return json.dumps(self.to_public_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def create_diagnostic_reference_record(
    *,
    source_type: DiagnosticReferenceSourceType | str,
    source_path: str,
    srsc_claim_id: str,
    srsc_gate_decision_id: str,
    claim_state: ClaimState | str,
    evidence_state: EvidenceState | str,
    evidence_refs: Iterable[str],
    diagnostic_scope: str,
    boundary_state: DiagnosticReferenceBoundary | str = DiagnosticReferenceBoundary.PUBLIC_SAFE,
    approved_for_record: bool = False,
    approved_as_verified: bool = False,
    source_task: str = TASK_ID,
    metadata: Mapping[str, Any] | None = None,
) -> SrscDiagnosticReferenceRecord:
    """Create a deterministic local SRSC diagnostic reference record."""

    return SrscDiagnosticReferenceRecord(
        source_type=DiagnosticReferenceSourceType(source_type),
        source_path=source_path,
        srsc_claim_id=srsc_claim_id,
        srsc_gate_decision_id=srsc_gate_decision_id,
        claim_state=ClaimState(claim_state),
        evidence_state=EvidenceState(evidence_state),
        evidence_refs=tuple(evidence_refs),
        diagnostic_scope=diagnostic_scope,
        boundary_state=DiagnosticReferenceBoundary(boundary_state),
        approved_for_record=approved_for_record,
        approved_as_verified=approved_as_verified,
        source_task=source_task,
        metadata=metadata or {},
    )


__all__ = [
    "BENCHMARK_SCORE_CLAIMED",
    "CANDIDATE_GENERATOR_MODIFIED",
    "EXTERNAL_API_DEPENDENCY",
    "INTERNET_DURING_EVAL",
    "KAGGLE_AUTHENTICATION_PERFORMED",
    "RANKER_MODIFIED",
    "REAL_EVALUATION_PERFORMED",
    "REAL_SUBMISSION_AUTHORIZED",
    "RUNTIME_ACTIVATION_AUTHORIZED",
    "SCHEMA_REVISION",
    "TASK_ID",
    "VERIFIER_MODIFIED",
    "DiagnosticReferenceBoundary",
    "DiagnosticReferenceSourceType",
    "SrscDiagnosticReferenceRecord",
    "create_diagnostic_reference_record",
]
