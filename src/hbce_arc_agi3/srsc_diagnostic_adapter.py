"""SRSC Diagnostic Adapter.

Milestone #19 Task 89 - local standalone adapter implementation.

This module adapts explicit local diagnostic payloads into SRSC diagnostic
reference records. It does not wire into solver runtime, candidate generation,
ranking, verification, benchmark execution, or Kaggle submission behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, Iterable, Mapping, Sequence

from hbce_arc_agi3.srsc_claim_ledger import ClaimState, EvidenceState, stable_digest
from hbce_arc_agi3.srsc_diagnostic_reference import (
    BENCHMARK_SCORE_CLAIMED,
    CANDIDATE_GENERATOR_MODIFIED,
    DiagnosticReferenceBoundary,
    DiagnosticReferenceSourceType,
    EXTERNAL_API_DEPENDENCY,
    INTERNET_DURING_EVAL,
    KAGGLE_AUTHENTICATION_PERFORMED,
    RANKER_MODIFIED,
    REAL_EVALUATION_PERFORMED,
    REAL_SUBMISSION_AUTHORIZED,
    RUNTIME_ACTIVATION_AUTHORIZED,
    SCHEMA_REVISION,
    SrscDiagnosticReferenceRecord,
    VERIFIER_MODIFIED,
    create_diagnostic_reference_record,
)


TASK_ID = "MILESTONE_19_TASK_89_SRSC_DIAGNOSTIC_ADAPTER_LOCAL_IMPLEMENTATION_V1"
ADAPTER_REVISION = "SRSC_DIAGNOSTIC_ADAPTER_LOCAL_STANDALONE_V1"

ADAPTER_IMPLEMENTED = True
ADAPTER_ACTIVATED = False
DIAGNOSTIC_ADAPTER_LOCAL_ONLY = True

RUNTIME_SOLVER_MODIFIED = False
RUNTIME_WIRING_ALLOWED = False
KAGGLE_SUBMISSION_SENT = False
PRIVATE_CORE_EXPOSURE = False
LEGAL_CERTIFICATION = False
FAIL_CLOSED_ACTIVE = True


def _clean_text(value: str, *, field_name: str) -> str:
    cleaned = " ".join(str(value).strip().split())
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned


def _clean_refs(values: Iterable[str]) -> tuple[str, ...]:
    refs = tuple(_clean_text(value, field_name="evidence_ref") for value in values if str(value).strip())
    return tuple(dict.fromkeys(refs))


def _clean_metadata(value: Mapping[str, Any] | None) -> dict[str, Any]:
    if value is None:
        return {}
    return {str(key): value[key] for key in sorted(value)}


@dataclass(frozen=True)
class DiagnosticAdapterInput:
    """Explicit local diagnostic source payload."""

    source_type: DiagnosticReferenceSourceType | str
    source_path: str
    diagnostic_scope: str
    srsc_claim_id: str
    srsc_gate_decision_id: str
    claim_state: ClaimState | str
    evidence_state: EvidenceState | str
    evidence_refs: tuple[str, ...]
    boundary_state: DiagnosticReferenceBoundary | str = DiagnosticReferenceBoundary.PUBLIC_SAFE
    approved_for_record: bool = False
    approved_as_verified: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_type", DiagnosticReferenceSourceType(self.source_type))
        object.__setattr__(self, "source_path", _clean_text(self.source_path, field_name="source_path"))
        object.__setattr__(self, "diagnostic_scope", _clean_text(self.diagnostic_scope, field_name="diagnostic_scope"))
        object.__setattr__(self, "srsc_claim_id", _clean_text(self.srsc_claim_id, field_name="srsc_claim_id"))
        object.__setattr__(
            self,
            "srsc_gate_decision_id",
            _clean_text(self.srsc_gate_decision_id, field_name="srsc_gate_decision_id"),
        )
        object.__setattr__(self, "claim_state", ClaimState(self.claim_state))
        object.__setattr__(self, "evidence_state", EvidenceState(self.evidence_state))
        object.__setattr__(self, "evidence_refs", _clean_refs(self.evidence_refs))
        object.__setattr__(self, "boundary_state", DiagnosticReferenceBoundary(self.boundary_state))
        object.__setattr__(self, "approved_for_record", bool(self.approved_for_record))
        object.__setattr__(self, "approved_as_verified", bool(self.approved_as_verified))
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def input_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-ADAPTER-INPUT", self.to_public_dict())
        return f"SRSC-DIAG-ADAPTER-IN-{digest[:16].upper()}"

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "sourceType": self.source_type.value,
            "sourcePath": self.source_path,
            "diagnosticScope": self.diagnostic_scope,
            "srscClaimId": self.srsc_claim_id,
            "srscGateDecisionId": self.srsc_gate_decision_id,
            "claimState": self.claim_state.value,
            "evidenceState": self.evidence_state.value,
            "evidenceRefs": list(self.evidence_refs),
            "boundaryState": self.boundary_state.value,
            "approvedForRecord": self.approved_for_record,
            "approvedAsVerified": self.approved_as_verified,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class DiagnosticAdapterBlockedReference:
    """Fail-closed blocked adapter record."""

    input_id: str
    reason: str
    source_path: str = "UNKNOWN_SOURCE_PATH"
    diagnostic_scope: str = "UNKNOWN_DIAGNOSTIC_SCOPE"

    def __post_init__(self) -> None:
        object.__setattr__(self, "input_id", _clean_text(self.input_id, field_name="input_id"))
        object.__setattr__(self, "reason", _clean_text(self.reason, field_name="reason"))
        object.__setattr__(self, "source_path", _clean_text(self.source_path, field_name="source_path"))
        object.__setattr__(
            self,
            "diagnostic_scope",
            _clean_text(self.diagnostic_scope, field_name="diagnostic_scope"),
        )

    @property
    def blocked_reference_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-ADAPTER-BLOCKED", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-ADAPTER-BLOCKED-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "inputId": self.input_id,
            "reason": self.reason,
            "sourcePath": self.source_path,
            "diagnosticScope": self.diagnostic_scope,
            "adapterImplemented": ADAPTER_IMPLEMENTED,
            "adapterActivated": ADAPTER_ACTIVATED,
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
            "privateCoreExposure": PRIVATE_CORE_EXPOSURE,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
        }
        if include_id:
            payload["blockedReferenceId"] = self.blocked_reference_id
        return payload


@dataclass(frozen=True)
class DiagnosticAdapterResult:
    """Result of local diagnostic adapter execution."""

    accepted_references: tuple[SrscDiagnosticReferenceRecord, ...] = ()
    blocked_references: tuple[DiagnosticAdapterBlockedReference, ...] = ()

    @property
    def result_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-ADAPTER-RESULT", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-ADAPTER-RESULT-{digest[:16].upper()}"

    @property
    def accepted_count(self) -> int:
        return len(self.accepted_references)

    @property
    def blocked_count(self) -> int:
        return len(self.blocked_references)

    @property
    def all_references_valid(self) -> bool:
        return all(reference.is_valid_reference for reference in self.accepted_references)

    @property
    def fail_closed_ok(self) -> bool:
        return (
            ADAPTER_IMPLEMENTED is True
            and ADAPTER_ACTIVATED is False
            and RUNTIME_ACTIVATION_AUTHORIZED is False
            and RUNTIME_SOLVER_MODIFIED is False
            and RUNTIME_WIRING_ALLOWED is False
            and CANDIDATE_GENERATOR_MODIFIED is False
            and RANKER_MODIFIED is False
            and VERIFIER_MODIFIED is False
            and BENCHMARK_SCORE_CLAIMED is False
            and REAL_EVALUATION_PERFORMED is False
            and REAL_SUBMISSION_AUTHORIZED is False
            and KAGGLE_AUTHENTICATION_PERFORMED is False
            and KAGGLE_SUBMISSION_SENT is False
            and INTERNET_DURING_EVAL is False
            and EXTERNAL_API_DEPENDENCY is False
            and PRIVATE_CORE_EXPOSURE is False
            and LEGAL_CERTIFICATION is False
            and FAIL_CLOSED_ACTIVE is True
        )

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "taskId": TASK_ID,
            "adapterRevision": ADAPTER_REVISION,
            "schemaRevision": SCHEMA_REVISION,
            "acceptedCount": self.accepted_count,
            "blockedCount": self.blocked_count,
            "allReferencesValid": self.all_references_valid,
            "failClosedOk": self.fail_closed_ok,
            "acceptedReferences": [reference.to_public_dict() for reference in self.accepted_references],
            "blockedReferences": [blocked.to_public_dict() for blocked in self.blocked_references],
            "adapterImplemented": ADAPTER_IMPLEMENTED,
            "adapterActivated": ADAPTER_ACTIVATED,
            "diagnosticAdapterLocalOnly": DIAGNOSTIC_ADAPTER_LOCAL_ONLY,
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
        }
        if include_id:
            payload["resultId"] = self.result_id
        return payload

    def to_json(self) -> str:
        return json.dumps(self.to_public_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def adapt_diagnostic_input_to_reference(payload: DiagnosticAdapterInput | Mapping[str, Any]) -> DiagnosticAdapterResult:
    """Adapt one explicit local diagnostic payload into a diagnostic reference result."""

    try:
        adapter_input = payload if isinstance(payload, DiagnosticAdapterInput) else DiagnosticAdapterInput(**dict(payload))
        reference = create_diagnostic_reference_record(
            source_type=adapter_input.source_type,
            source_path=adapter_input.source_path,
            srsc_claim_id=adapter_input.srsc_claim_id,
            srsc_gate_decision_id=adapter_input.srsc_gate_decision_id,
            claim_state=adapter_input.claim_state,
            evidence_state=adapter_input.evidence_state,
            evidence_refs=adapter_input.evidence_refs,
            diagnostic_scope=adapter_input.diagnostic_scope,
            boundary_state=adapter_input.boundary_state,
            approved_for_record=adapter_input.approved_for_record,
            approved_as_verified=adapter_input.approved_as_verified,
            source_task=TASK_ID,
            metadata=adapter_input.metadata,
        )
        if reference.is_valid_reference:
            return DiagnosticAdapterResult(accepted_references=(reference,), blocked_references=())

        return DiagnosticAdapterResult(
            accepted_references=(),
            blocked_references=(
                DiagnosticAdapterBlockedReference(
                    input_id=adapter_input.input_id,
                    reason="REFERENCE_VALIDATION_FAILED",
                    source_path=adapter_input.source_path,
                    diagnostic_scope=adapter_input.diagnostic_scope,
                ),
            ),
        )
    except Exception as exc:
        return DiagnosticAdapterResult(
            accepted_references=(),
            blocked_references=(
                DiagnosticAdapterBlockedReference(
                    input_id="SRSC-DIAG-ADAPTER-IN-BLOCKED",
                    reason=f"INPUT_REJECTED:{type(exc).__name__}",
                ),
            ),
        )


def adapt_diagnostic_inputs_to_references(
    payloads: Sequence[DiagnosticAdapterInput | Mapping[str, Any]],
) -> DiagnosticAdapterResult:
    """Adapt multiple local diagnostic payloads into deterministic reference results."""

    accepted: list[SrscDiagnosticReferenceRecord] = []
    blocked: list[DiagnosticAdapterBlockedReference] = []

    for payload in payloads:
        result = adapt_diagnostic_input_to_reference(payload)
        accepted.extend(result.accepted_references)
        blocked.extend(result.blocked_references)

    return DiagnosticAdapterResult(
        accepted_references=tuple(accepted),
        blocked_references=tuple(blocked),
    )


__all__ = [
    "ADAPTER_ACTIVATED",
    "ADAPTER_IMPLEMENTED",
    "ADAPTER_REVISION",
    "DIAGNOSTIC_ADAPTER_LOCAL_ONLY",
    "FAIL_CLOSED_ACTIVE",
    "KAGGLE_SUBMISSION_SENT",
    "LEGAL_CERTIFICATION",
    "PRIVATE_CORE_EXPOSURE",
    "RUNTIME_SOLVER_MODIFIED",
    "RUNTIME_WIRING_ALLOWED",
    "TASK_ID",
    "DiagnosticAdapterBlockedReference",
    "DiagnosticAdapterInput",
    "DiagnosticAdapterResult",
    "adapt_diagnostic_input_to_reference",
    "adapt_diagnostic_inputs_to_references",
]
