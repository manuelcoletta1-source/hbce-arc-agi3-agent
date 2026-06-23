"""SRSC Diagnostic Adapter Controlled Activation Usage Layer.

Milestone #19 Task 97 - local diagnostic-only usage implementation.

This module coordinates controlled diagnostic activation calls for local
public-safe evidence and audit flows. It does not wire into solver runtime,
candidate generation, ranking, verification, benchmarks, Kaggle behavior,
network behavior, or private core behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.srsc_claim_ledger import stable_digest
from hbce_arc_agi3.srsc_diagnostic_adapter import DiagnosticAdapterInput
from hbce_arc_agi3.srsc_diagnostic_adapter_activation import (
    ACTIVATION_REVISION,
    DiagnosticAdapterActivationResult,
    activate_diagnostic_adapter_batch_for_diagnostic_path,
    activate_diagnostic_adapter_for_diagnostic_path,
)


TASK_ID = "MILESTONE_19_TASK_97_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_LOCAL_IMPLEMENTATION_V1"
USAGE_REVISION = "SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_LOCAL_STANDALONE_V1"

CONTROLLED_USAGE_IMPLEMENTED = True
DIAGNOSTIC_USAGE_ONLY = True
ACTIVATION_WRAPPER_MODIFIED = False
ADAPTER_MODIFIED = False

RUNTIME_ACTIVATION_AUTHORIZED = False
RUNTIME_SOLVER_MODIFIED = False
RUNTIME_WIRING_ALLOWED = False
SOLVER_RUNTIME_BINDING = False

CANDIDATE_GENERATOR_MODIFIED = False
CANDIDATE_GENERATOR_BINDING = False
RANKER_MODIFIED = False
RANKER_BINDING = False
VERIFIER_MODIFIED = False
VERIFIER_BINDING = False
BENCHMARK_SCORE_CLAIMED = False
BENCHMARK_BINDING = False

REAL_EVALUATION_PERFORMED = False
REAL_SUBMISSION_AUTHORIZED = False
KAGGLE_AUTHENTICATION_PERFORMED = False
KAGGLE_SUBMISSION_SENT = False
KAGGLE_SUBMISSION_BINDING = False

INTERNET_DURING_EVAL = False
EXTERNAL_API_DEPENDENCY = False
PRIVATE_CORE_EXPOSURE = False
LEGAL_CERTIFICATION = False
FAIL_CLOSED_ACTIVE = True


ALLOWED_USAGE_CONTEXTS: tuple[str, ...] = (
    "local SRSC diagnostic report generation",
    "local milestone evidence packaging",
    "local public-safe audit summary creation",
    "local cross-trace planner evidence attachment",
    "local blocked-call report generation",
)

FORBIDDEN_USAGE_CONTEXTS: tuple[str, ...] = (
    "solver runtime execution",
    "runtime planner execution",
    "agent loop execution",
    "candidate generation",
    "candidate ranking",
    "verifier execution",
    "benchmark execution",
    "real evaluation execution",
    "Kaggle submission packaging",
    "score reporting",
    "private core execution",
    "network/API execution",
    "legal certification workflows",
)

_ALLOWED_USAGE_NORMALIZED = {value.lower(): value for value in ALLOWED_USAGE_CONTEXTS}
_FORBIDDEN_USAGE_NORMALIZED = {value.lower(): value for value in FORBIDDEN_USAGE_CONTEXTS}


def _clean_text(value: str, *, field_name: str) -> str:
    cleaned = " ".join(str(value).strip().split())
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned


def _normalize_usage_context(value: str) -> str:
    return _clean_text(value, field_name="usage_context").lower()


def _clean_metadata(value: Mapping[str, Any] | None) -> dict[str, Any]:
    if value is None:
        return {}
    return {str(key): value[key] for key in sorted(value)}


@dataclass(frozen=True)
class DiagnosticActivationUsageRequest:
    """Explicit local diagnostic-only usage request."""

    usage_context: str
    call_site: str
    diagnostic_payload: DiagnosticAdapterInput | Mapping[str, Any]
    source_artifact_path: str
    diagnostic_purpose: str
    expected_public_safe_output_type: str = "local deterministic JSON"
    retention_class: str = "local technical evidence"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "usage_context", _clean_text(self.usage_context, field_name="usage_context"))
        object.__setattr__(self, "call_site", _clean_text(self.call_site, field_name="call_site"))
        object.__setattr__(
            self,
            "source_artifact_path",
            _clean_text(self.source_artifact_path, field_name="source_artifact_path"),
        )
        object.__setattr__(
            self,
            "diagnostic_purpose",
            _clean_text(self.diagnostic_purpose, field_name="diagnostic_purpose"),
        )
        object.__setattr__(
            self,
            "expected_public_safe_output_type",
            _clean_text(
                self.expected_public_safe_output_type,
                field_name="expected_public_safe_output_type",
            ),
        )
        object.__setattr__(
            self,
            "retention_class",
            _clean_text(self.retention_class, field_name="retention_class"),
        )
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def normalized_usage_context(self) -> str:
        return _normalize_usage_context(self.usage_context)

    @property
    def is_allowed_usage_context(self) -> bool:
        return self.normalized_usage_context in _ALLOWED_USAGE_NORMALIZED

    @property
    def is_forbidden_usage_context(self) -> bool:
        return self.normalized_usage_context in _FORBIDDEN_USAGE_NORMALIZED

    @property
    def request_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-ACTIVATION-USAGE-REQUEST", self.to_public_dict())
        return f"SRSC-DIAG-ACT-USAGE-REQ-{digest[:16].upper()}"

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "usageContext": self.usage_context,
            "normalizedUsageContext": self.normalized_usage_context,
            "callSite": self.call_site,
            "sourceArtifactPath": self.source_artifact_path,
            "diagnosticPurpose": self.diagnostic_purpose,
            "expectedPublicSafeOutputType": self.expected_public_safe_output_type,
            "retentionClass": self.retention_class,
            "isAllowedUsageContext": self.is_allowed_usage_context,
            "isForbiddenUsageContext": self.is_forbidden_usage_context,
            "metadata": dict(self.metadata),
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
            "publicSafeOnly": True,
            "legalCertification": LEGAL_CERTIFICATION,
        }


@dataclass(frozen=True)
class DiagnosticActivationUsageBlockedRequest:
    """Fail-closed blocked diagnostic usage request."""

    request_id: str
    usage_context: str
    call_site: str
    reason: str
    source_artifact_path: str
    diagnostic_purpose: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _clean_text(self.request_id, field_name="request_id"))
        object.__setattr__(self, "usage_context", _clean_text(self.usage_context, field_name="usage_context"))
        object.__setattr__(self, "call_site", _clean_text(self.call_site, field_name="call_site"))
        object.__setattr__(self, "reason", _clean_text(self.reason, field_name="reason"))
        object.__setattr__(
            self,
            "source_artifact_path",
            _clean_text(self.source_artifact_path, field_name="source_artifact_path"),
        )
        object.__setattr__(
            self,
            "diagnostic_purpose",
            _clean_text(self.diagnostic_purpose, field_name="diagnostic_purpose"),
        )

    @property
    def blocked_request_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-ACTIVATION-USAGE-BLOCKED", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-ACT-USAGE-BLOCKED-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "requestId": self.request_id,
            "usageContext": self.usage_context,
            "callSite": self.call_site,
            "reason": self.reason,
            "sourceArtifactPath": self.source_artifact_path,
            "diagnosticPurpose": self.diagnostic_purpose,
            "controlledUsageImplemented": CONTROLLED_USAGE_IMPLEMENTED,
            "diagnosticUsageOnly": DIAGNOSTIC_USAGE_ONLY,
            "activationWrapperModified": ACTIVATION_WRAPPER_MODIFIED,
            "adapterModified": ADAPTER_MODIFIED,
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED,
            "solverRuntimeBinding": SOLVER_RUNTIME_BINDING,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
            "privateCoreExposure": PRIVATE_CORE_EXPOSURE,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
        }
        if include_id:
            payload["blockedRequestId"] = self.blocked_request_id
        return payload


@dataclass(frozen=True)
class DiagnosticActivationUsageResult:
    """Result of local controlled diagnostic activation usage."""

    activation_result: DiagnosticAdapterActivationResult = field(default_factory=DiagnosticAdapterActivationResult)
    blocked_requests: tuple[DiagnosticActivationUsageBlockedRequest, ...] = ()

    @property
    def result_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-ACTIVATION-USAGE-RESULT", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-ACT-USAGE-RESULT-{digest[:16].upper()}"

    @property
    def accepted_count(self) -> int:
        return self.activation_result.accepted_count

    @property
    def blocked_reference_count(self) -> int:
        return self.activation_result.blocked_reference_count

    @property
    def blocked_call_count(self) -> int:
        return self.activation_result.blocked_call_count

    @property
    def blocked_usage_request_count(self) -> int:
        return len(self.blocked_requests)

    @property
    def usage_ok(self) -> bool:
        return (
            CONTROLLED_USAGE_IMPLEMENTED is True
            and DIAGNOSTIC_USAGE_ONLY is True
            and ACTIVATION_WRAPPER_MODIFIED is False
            and ADAPTER_MODIFIED is False
            and RUNTIME_ACTIVATION_AUTHORIZED is False
            and RUNTIME_SOLVER_MODIFIED is False
            and RUNTIME_WIRING_ALLOWED is False
            and SOLVER_RUNTIME_BINDING is False
            and CANDIDATE_GENERATOR_MODIFIED is False
            and CANDIDATE_GENERATOR_BINDING is False
            and RANKER_MODIFIED is False
            and RANKER_BINDING is False
            and VERIFIER_MODIFIED is False
            and VERIFIER_BINDING is False
            and BENCHMARK_SCORE_CLAIMED is False
            and BENCHMARK_BINDING is False
            and REAL_EVALUATION_PERFORMED is False
            and REAL_SUBMISSION_AUTHORIZED is False
            and KAGGLE_AUTHENTICATION_PERFORMED is False
            and KAGGLE_SUBMISSION_SENT is False
            and KAGGLE_SUBMISSION_BINDING is False
            and INTERNET_DURING_EVAL is False
            and EXTERNAL_API_DEPENDENCY is False
            and PRIVATE_CORE_EXPOSURE is False
            and LEGAL_CERTIFICATION is False
            and FAIL_CLOSED_ACTIVE is True
            and self.activation_result.diagnostic_activation_ok is True
        )

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "taskId": TASK_ID,
            "usageRevision": USAGE_REVISION,
            "activationRevision": ACTIVATION_REVISION,
            "acceptedCount": self.accepted_count,
            "blockedReferenceCount": self.blocked_reference_count,
            "blockedCallCount": self.blocked_call_count,
            "blockedUsageRequestCount": self.blocked_usage_request_count,
            "usageOk": self.usage_ok,
            "activationResult": self.activation_result.to_public_dict(),
            "blockedRequests": [blocked.to_public_dict() for blocked in self.blocked_requests],
            "allowedUsageContexts": list(ALLOWED_USAGE_CONTEXTS),
            "forbiddenUsageContexts": list(FORBIDDEN_USAGE_CONTEXTS),
            "controlledUsageImplemented": CONTROLLED_USAGE_IMPLEMENTED,
            "diagnosticUsageOnly": DIAGNOSTIC_USAGE_ONLY,
            "activationWrapperModified": ACTIVATION_WRAPPER_MODIFIED,
            "adapterModified": ADAPTER_MODIFIED,
            "runtimeActivationAuthorized": RUNTIME_ACTIVATION_AUTHORIZED,
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED,
            "solverRuntimeBinding": SOLVER_RUNTIME_BINDING,
            "candidateGeneratorModified": CANDIDATE_GENERATOR_MODIFIED,
            "candidateGeneratorBinding": CANDIDATE_GENERATOR_BINDING,
            "rankerModified": RANKER_MODIFIED,
            "rankerBinding": RANKER_BINDING,
            "verifierModified": VERIFIER_MODIFIED,
            "verifierBinding": VERIFIER_BINDING,
            "benchmarkScoreClaimed": BENCHMARK_SCORE_CLAIMED,
            "benchmarkBinding": BENCHMARK_BINDING,
            "realEvaluationPerformed": REAL_EVALUATION_PERFORMED,
            "realSubmissionAuthorized": REAL_SUBMISSION_AUTHORIZED,
            "kaggleAuthenticationPerformed": KAGGLE_AUTHENTICATION_PERFORMED,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
            "kaggleSubmissionBinding": KAGGLE_SUBMISSION_BINDING,
            "internetDuringEval": INTERNET_DURING_EVAL,
            "externalApiDependency": EXTERNAL_API_DEPENDENCY,
            "privateCoreExposure": PRIVATE_CORE_EXPOSURE,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
            "publicSafeOnly": True,
        }
        if include_id:
            payload["resultId"] = self.result_id
        return payload

    def to_json(self) -> str:
        return json.dumps(self.to_public_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _blocked_usage_result(
    *,
    request: DiagnosticActivationUsageRequest,
    reason: str,
) -> DiagnosticActivationUsageResult:
    return DiagnosticActivationUsageResult(
        activation_result=DiagnosticAdapterActivationResult(),
        blocked_requests=(
            DiagnosticActivationUsageBlockedRequest(
                request_id=request.request_id,
                usage_context=request.usage_context,
                call_site=request.call_site,
                reason=reason,
                source_artifact_path=request.source_artifact_path,
                diagnostic_purpose=request.diagnostic_purpose,
            ),
        ),
    )


def run_controlled_activation_usage(
    payload: DiagnosticAdapterInput | Mapping[str, Any],
    *,
    usage_context: str,
    call_site: str,
    source_artifact_path: str,
    diagnostic_purpose: str,
    expected_public_safe_output_type: str = "local deterministic JSON",
    retention_class: str = "local technical evidence",
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticActivationUsageResult:
    """Run local diagnostic-only usage through the activation wrapper."""

    request = DiagnosticActivationUsageRequest(
        usage_context=usage_context,
        call_site=call_site,
        diagnostic_payload=payload,
        source_artifact_path=source_artifact_path,
        diagnostic_purpose=diagnostic_purpose,
        expected_public_safe_output_type=expected_public_safe_output_type,
        retention_class=retention_class,
        metadata={} if metadata is None else metadata,
    )

    if request.is_forbidden_usage_context:
        return _blocked_usage_result(request=request, reason="FORBIDDEN_USAGE_CONTEXT")

    if not request.is_allowed_usage_context:
        return _blocked_usage_result(request=request, reason="UNKNOWN_USAGE_CONTEXT")

    activation_metadata = dict(request.metadata)
    activation_metadata.update(
        {
            "usageRequestId": request.request_id,
            "usageContext": request.usage_context,
            "sourceArtifactPath": request.source_artifact_path,
            "diagnosticPurpose": request.diagnostic_purpose,
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
        }
    )

    activation_result = activate_diagnostic_adapter_for_diagnostic_path(
        payload,
        call_site=request.call_site,
        activation_scope="controlled diagnostic activation usage",
        metadata=activation_metadata,
    )
    return DiagnosticActivationUsageResult(activation_result=activation_result, blocked_requests=())


def run_controlled_activation_usage_batch(
    payloads: Sequence[DiagnosticAdapterInput | Mapping[str, Any]],
    *,
    usage_context: str,
    call_site: str,
    source_artifact_path: str,
    diagnostic_purpose: str,
    expected_public_safe_output_type: str = "local deterministic JSON batch",
    retention_class: str = "local technical evidence",
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticActivationUsageResult:
    """Run local diagnostic-only batch usage through the activation wrapper."""

    request = DiagnosticActivationUsageRequest(
        usage_context=usage_context,
        call_site=call_site,
        diagnostic_payload={},
        source_artifact_path=source_artifact_path,
        diagnostic_purpose=diagnostic_purpose,
        expected_public_safe_output_type=expected_public_safe_output_type,
        retention_class=retention_class,
        metadata={} if metadata is None else metadata,
    )

    if request.is_forbidden_usage_context:
        return _blocked_usage_result(request=request, reason="FORBIDDEN_USAGE_CONTEXT")

    if not request.is_allowed_usage_context:
        return _blocked_usage_result(request=request, reason="UNKNOWN_USAGE_CONTEXT")

    activation_metadata = dict(request.metadata)
    activation_metadata.update(
        {
            "usageRequestId": request.request_id,
            "usageContext": request.usage_context,
            "sourceArtifactPath": request.source_artifact_path,
            "diagnosticPurpose": request.diagnostic_purpose,
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
        }
    )

    activation_result = activate_diagnostic_adapter_batch_for_diagnostic_path(
        payloads,
        call_site=request.call_site,
        activation_scope="controlled diagnostic activation usage batch",
        metadata=activation_metadata,
    )
    return DiagnosticActivationUsageResult(activation_result=activation_result, blocked_requests=())


__all__ = [
    "ACTIVATION_WRAPPER_MODIFIED",
    "ADAPTER_MODIFIED",
    "ALLOWED_USAGE_CONTEXTS",
    "BENCHMARK_BINDING",
    "BENCHMARK_SCORE_CLAIMED",
    "CANDIDATE_GENERATOR_BINDING",
    "CANDIDATE_GENERATOR_MODIFIED",
    "CONTROLLED_USAGE_IMPLEMENTED",
    "DIAGNOSTIC_USAGE_ONLY",
    "EXTERNAL_API_DEPENDENCY",
    "FAIL_CLOSED_ACTIVE",
    "FORBIDDEN_USAGE_CONTEXTS",
    "INTERNET_DURING_EVAL",
    "KAGGLE_SUBMISSION_BINDING",
    "KAGGLE_SUBMISSION_SENT",
    "LEGAL_CERTIFICATION",
    "PRIVATE_CORE_EXPOSURE",
    "RANKER_BINDING",
    "RANKER_MODIFIED",
    "RUNTIME_SOLVER_MODIFIED",
    "RUNTIME_WIRING_ALLOWED",
    "SOLVER_RUNTIME_BINDING",
    "TASK_ID",
    "USAGE_REVISION",
    "VERIFIER_BINDING",
    "VERIFIER_MODIFIED",
    "DiagnosticActivationUsageBlockedRequest",
    "DiagnosticActivationUsageRequest",
    "DiagnosticActivationUsageResult",
    "run_controlled_activation_usage",
    "run_controlled_activation_usage_batch",
]
