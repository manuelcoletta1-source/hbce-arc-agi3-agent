"""SRSC Diagnostic Adapter Controlled Activation.

Milestone #19 Task 93 - controlled diagnostic-only activation implementation.

This module exposes a local diagnostic-only activation wrapper around the
SRSC Diagnostic Adapter. It does not wire into solver runtime, candidate
generation, ranking, verification, benchmark execution, network behavior,
or Kaggle submission behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.srsc_claim_ledger import stable_digest
from hbce_arc_agi3.srsc_diagnostic_adapter import (
    ADAPTER_REVISION,
    DiagnosticAdapterInput,
    DiagnosticAdapterResult,
    adapt_diagnostic_input_to_reference,
    adapt_diagnostic_inputs_to_references,
)


TASK_ID = "MILESTONE_19_TASK_93_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_LOCAL_IMPLEMENTATION_V1"
ACTIVATION_REVISION = "SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_LOCAL_STANDALONE_V1"

CONTROLLED_ACTIVATION_IMPLEMENTED = True
DIAGNOSTIC_ONLY_ACTIVATION = True
ADAPTER_ACTIVATED_FOR_DIAGNOSTIC_PATH_ONLY = True

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


ALLOWED_CALL_SITES: tuple[str, ...] = (
    "local diagnostic scripts",
    "public-safe audit artifact builders",
    "SRSC review artifact generators",
    "milestone closure evidence builders",
    "cross-trace diagnostic planners",
)

FORBIDDEN_CALL_SITES: tuple[str, ...] = (
    "solver runtime loop",
    "agent planner",
    "world model",
    "observer runtime path",
    "candidate generator",
    "candidate ranker",
    "verifier",
    "benchmark executor",
    "Kaggle submission package builder",
    "real evaluation runner",
    "private core modules",
    "network or API clients",
)

_ALLOWED_NORMALIZED = {value.lower(): value for value in ALLOWED_CALL_SITES}
_FORBIDDEN_NORMALIZED = {value.lower(): value for value in FORBIDDEN_CALL_SITES}


def _clean_text(value: str, *, field_name: str) -> str:
    cleaned = " ".join(str(value).strip().split())
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned


def _normalize_call_site(value: str) -> str:
    return _clean_text(value, field_name="call_site").lower()


def _clean_metadata(value: Mapping[str, Any] | None) -> dict[str, Any]:
    if value is None:
        return {}
    return {str(key): value[key] for key in sorted(value)}


@dataclass(frozen=True)
class DiagnosticAdapterActivationInput:
    """Explicit diagnostic-only activation request."""

    call_site: str
    diagnostic_payload: DiagnosticAdapterInput | Mapping[str, Any]
    activation_scope: str = "controlled diagnostic adapter activation"
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        call_site = _clean_text(self.call_site, field_name="call_site")
        activation_scope = _clean_text(self.activation_scope, field_name="activation_scope")
        object.__setattr__(self, "call_site", call_site)
        object.__setattr__(self, "activation_scope", activation_scope)
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def normalized_call_site(self) -> str:
        return _normalize_call_site(self.call_site)

    @property
    def is_allowed_call_site(self) -> bool:
        return self.normalized_call_site in _ALLOWED_NORMALIZED

    @property
    def is_forbidden_call_site(self) -> bool:
        return self.normalized_call_site in _FORBIDDEN_NORMALIZED

    @property
    def input_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-ADAPTER-ACTIVATION-INPUT", self.to_public_dict())
        return f"SRSC-DIAG-ACT-IN-{digest[:16].upper()}"

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "callSite": self.call_site,
            "normalizedCallSite": self.normalized_call_site,
            "activationScope": self.activation_scope,
            "isAllowedCallSite": self.is_allowed_call_site,
            "isForbiddenCallSite": self.is_forbidden_call_site,
            "metadata": dict(self.metadata),
        }


@dataclass(frozen=True)
class DiagnosticAdapterActivationBlockedCall:
    """Fail-closed blocked activation call."""

    input_id: str
    call_site: str
    reason: str
    activation_scope: str = "controlled diagnostic adapter activation"

    def __post_init__(self) -> None:
        object.__setattr__(self, "input_id", _clean_text(self.input_id, field_name="input_id"))
        object.__setattr__(self, "call_site", _clean_text(self.call_site, field_name="call_site"))
        object.__setattr__(self, "reason", _clean_text(self.reason, field_name="reason"))
        object.__setattr__(
            self,
            "activation_scope",
            _clean_text(self.activation_scope, field_name="activation_scope"),
        )

    @property
    def blocked_call_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-ADAPTER-ACTIVATION-BLOCKED", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-ACT-BLOCKED-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "inputId": self.input_id,
            "callSite": self.call_site,
            "activationScope": self.activation_scope,
            "reason": self.reason,
            "controlledActivationImplemented": CONTROLLED_ACTIVATION_IMPLEMENTED,
            "diagnosticOnlyActivation": DIAGNOSTIC_ONLY_ACTIVATION,
            "adapterActivatedForDiagnosticPathOnly": ADAPTER_ACTIVATED_FOR_DIAGNOSTIC_PATH_ONLY,
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED,
            "solverRuntimeBinding": SOLVER_RUNTIME_BINDING,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
            "privateCoreExposure": PRIVATE_CORE_EXPOSURE,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
        }
        if include_id:
            payload["blockedCallId"] = self.blocked_call_id
        return payload


@dataclass(frozen=True)
class DiagnosticAdapterActivationResult:
    """Result of controlled diagnostic-only activation."""

    adapter_result: DiagnosticAdapterResult = field(default_factory=DiagnosticAdapterResult)
    blocked_calls: tuple[DiagnosticAdapterActivationBlockedCall, ...] = ()

    @property
    def result_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-ADAPTER-ACTIVATION-RESULT", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-ACT-RESULT-{digest[:16].upper()}"

    @property
    def accepted_count(self) -> int:
        return self.adapter_result.accepted_count

    @property
    def blocked_reference_count(self) -> int:
        return self.adapter_result.blocked_count

    @property
    def blocked_call_count(self) -> int:
        return len(self.blocked_calls)

    @property
    def diagnostic_activation_ok(self) -> bool:
        return (
            CONTROLLED_ACTIVATION_IMPLEMENTED is True
            and DIAGNOSTIC_ONLY_ACTIVATION is True
            and ADAPTER_ACTIVATED_FOR_DIAGNOSTIC_PATH_ONLY is True
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
        )

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "taskId": TASK_ID,
            "activationRevision": ACTIVATION_REVISION,
            "adapterRevision": ADAPTER_REVISION,
            "acceptedCount": self.accepted_count,
            "blockedReferenceCount": self.blocked_reference_count,
            "blockedCallCount": self.blocked_call_count,
            "diagnosticActivationOk": self.diagnostic_activation_ok,
            "adapterResult": self.adapter_result.to_public_dict(),
            "blockedCalls": [blocked.to_public_dict() for blocked in self.blocked_calls],
            "allowedCallSites": list(ALLOWED_CALL_SITES),
            "forbiddenCallSites": list(FORBIDDEN_CALL_SITES),
            "controlledActivationImplemented": CONTROLLED_ACTIVATION_IMPLEMENTED,
            "diagnosticOnlyActivation": DIAGNOSTIC_ONLY_ACTIVATION,
            "adapterActivatedForDiagnosticPathOnly": ADAPTER_ACTIVATED_FOR_DIAGNOSTIC_PATH_ONLY,
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
        }
        if include_id:
            payload["resultId"] = self.result_id
        return payload

    def to_json(self) -> str:
        return json.dumps(self.to_public_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _blocked_activation_result(
    *,
    activation_input: DiagnosticAdapterActivationInput,
    reason: str,
) -> DiagnosticAdapterActivationResult:
    return DiagnosticAdapterActivationResult(
        adapter_result=DiagnosticAdapterResult(),
        blocked_calls=(
            DiagnosticAdapterActivationBlockedCall(
                input_id=activation_input.input_id,
                call_site=activation_input.call_site,
                reason=reason,
                activation_scope=activation_input.activation_scope,
            ),
        ),
    )


def activate_diagnostic_adapter_for_diagnostic_path(
    payload: DiagnosticAdapterInput | Mapping[str, Any],
    *,
    call_site: str,
    activation_scope: str = "controlled diagnostic adapter activation",
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticAdapterActivationResult:
    """Activate the SRSC adapter for a local diagnostic-only path."""

    activation_input = DiagnosticAdapterActivationInput(
        call_site=call_site,
        diagnostic_payload=payload,
        activation_scope=activation_scope,
        metadata={} if metadata is None else metadata,
    )

    if activation_input.is_forbidden_call_site:
        return _blocked_activation_result(
            activation_input=activation_input,
            reason="FORBIDDEN_CALL_SITE",
        )

    if not activation_input.is_allowed_call_site:
        return _blocked_activation_result(
            activation_input=activation_input,
            reason="UNKNOWN_CALL_SITE",
        )

    adapter_result = adapt_diagnostic_input_to_reference(payload)
    return DiagnosticAdapterActivationResult(adapter_result=adapter_result, blocked_calls=())


def activate_diagnostic_adapter_batch_for_diagnostic_path(
    payloads: Sequence[DiagnosticAdapterInput | Mapping[str, Any]],
    *,
    call_site: str,
    activation_scope: str = "controlled diagnostic adapter activation batch",
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticAdapterActivationResult:
    """Activate the SRSC adapter for multiple local diagnostic payloads."""

    activation_input = DiagnosticAdapterActivationInput(
        call_site=call_site,
        diagnostic_payload={},
        activation_scope=activation_scope,
        metadata={} if metadata is None else metadata,
    )

    if activation_input.is_forbidden_call_site:
        return _blocked_activation_result(
            activation_input=activation_input,
            reason="FORBIDDEN_CALL_SITE",
        )

    if not activation_input.is_allowed_call_site:
        return _blocked_activation_result(
            activation_input=activation_input,
            reason="UNKNOWN_CALL_SITE",
        )

    adapter_result = adapt_diagnostic_inputs_to_references(payloads)
    return DiagnosticAdapterActivationResult(adapter_result=adapter_result, blocked_calls=())


__all__ = [
    "ACTIVATION_REVISION",
    "ADAPTER_ACTIVATED_FOR_DIAGNOSTIC_PATH_ONLY",
    "ALLOWED_CALL_SITES",
    "BENCHMARK_BINDING",
    "BENCHMARK_SCORE_CLAIMED",
    "CANDIDATE_GENERATOR_BINDING",
    "CANDIDATE_GENERATOR_MODIFIED",
    "CONTROLLED_ACTIVATION_IMPLEMENTED",
    "DIAGNOSTIC_ONLY_ACTIVATION",
    "EXTERNAL_API_DEPENDENCY",
    "FAIL_CLOSED_ACTIVE",
    "FORBIDDEN_CALL_SITES",
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
    "VERIFIER_BINDING",
    "VERIFIER_MODIFIED",
    "DiagnosticAdapterActivationBlockedCall",
    "DiagnosticAdapterActivationInput",
    "DiagnosticAdapterActivationResult",
    "activate_diagnostic_adapter_batch_for_diagnostic_path",
    "activate_diagnostic_adapter_for_diagnostic_path",
]
