"""SRSC controlled diagnostic artifact emission usage runner.

Milestone #19 Task 105 - local diagnostic-only artifact emission usage implementation.

This module uses the Task 101 artifact emitter in a controlled local usage layer.
It does not modify the emitter, the controlled activation usage layer, the
activation wrapper, the adapter, solver runtime, candidate generation, ranking,
verification, benchmarks, Kaggle behavior, network behavior, or private core
behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.srsc_claim_ledger import stable_digest
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage import (
    DiagnosticActivationUsageResult,
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emitter import (
    ARTIFACT_EMITTER_REVISION,
    AUTHORIZED_ARTIFACT_FAMILIES,
    FORBIDDEN_ARTIFACT_FAMILIES,
    DiagnosticUsageArtifactEmissionResult,
    emit_controlled_usage_artifact_batch,
)


TASK_ID = "MILESTONE_19_TASK_105_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_LOCAL_IMPLEMENTATION_V1"
ARTIFACT_EMISSION_USAGE_REVISION = "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_LOCAL_STANDALONE_V1"

CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTED = True
DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_ONLY = True

ARTIFACT_EMITTER_MODIFIED = False
USAGE_LAYER_MODIFIED = False
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


AUTHORIZED_USAGE_CONTEXTS: tuple[str, ...] = (
    "local diagnostic artifact usage",
    "local milestone artifact bundle usage",
    "local evidence package artifact usage",
    "local public-safe audit artifact usage",
    "local blocked request artifact usage",
    "local cross-trace attachment artifact usage",
    "local deterministic index artifact usage",
)

FORBIDDEN_USAGE_CONTEXTS: tuple[str, ...] = (
    "solver runtime artifact usage",
    "candidate generator artifact usage",
    "ranker score artifact usage",
    "verifier score artifact usage",
    "benchmark artifact usage",
    "Kaggle submission artifact usage",
    "public score artifact usage",
    "private score artifact usage",
    "production runtime artifact usage",
    "network/API artifact usage",
    "private core artifact usage",
    "legal certification artifact usage",
)

DEFAULT_DIAGNOSTIC_ARTIFACT_FAMILIES: tuple[str, ...] = (
    "local diagnostic report JSON",
    "local diagnostic report Markdown",
    "local public-safe audit summary JSON",
    "local deterministic index TXT",
)

_AUTHORIZED_CONTEXTS_NORMALIZED = {value.lower(): value for value in AUTHORIZED_USAGE_CONTEXTS}
_FORBIDDEN_CONTEXTS_NORMALIZED = {value.lower(): value for value in FORBIDDEN_USAGE_CONTEXTS}


def _clean_text(value: str, *, field_name: str) -> str:
    cleaned = " ".join(str(value).strip().split())
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned


def _clean_tuple(values: Sequence[str], *, field_name: str) -> tuple[str, ...]:
    cleaned = tuple(_clean_text(value, field_name=field_name) for value in values)
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned


def _clean_metadata(value: Mapping[str, Any] | None) -> dict[str, Any]:
    if value is None:
        return {}
    return {str(key): value[key] for key in sorted(value)}


def _normalize(value: str) -> str:
    return _clean_text(value, field_name="value").lower()


@dataclass(frozen=True)
class DiagnosticArtifactEmissionUsagePlan:
    """Deterministic local plan for diagnostic artifact emission usage."""

    usage_context: str
    artifact_families: tuple[str, ...]
    output_name_prefix: str
    emission_purpose: str
    milestone_id: str
    source_task_id: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "usage_context",
            _clean_text(self.usage_context, field_name="usage_context"),
        )
        object.__setattr__(
            self,
            "artifact_families",
            _clean_tuple(self.artifact_families, field_name="artifact_families"),
        )
        object.__setattr__(
            self,
            "output_name_prefix",
            _clean_text(self.output_name_prefix, field_name="output_name_prefix"),
        )
        object.__setattr__(
            self,
            "emission_purpose",
            _clean_text(self.emission_purpose, field_name="emission_purpose"),
        )
        object.__setattr__(
            self,
            "milestone_id",
            _clean_text(self.milestone_id, field_name="milestone_id"),
        )
        object.__setattr__(
            self,
            "source_task_id",
            _clean_text(self.source_task_id, field_name="source_task_id"),
        )
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def normalized_usage_context(self) -> str:
        return _normalize(self.usage_context)

    @property
    def is_authorized_usage_context(self) -> bool:
        return self.normalized_usage_context in _AUTHORIZED_CONTEXTS_NORMALIZED

    @property
    def is_forbidden_usage_context(self) -> bool:
        return self.normalized_usage_context in _FORBIDDEN_CONTEXTS_NORMALIZED

    @property
    def canonical_usage_context(self) -> str:
        if self.is_authorized_usage_context:
            return _AUTHORIZED_CONTEXTS_NORMALIZED[self.normalized_usage_context]
        if self.is_forbidden_usage_context:
            return _FORBIDDEN_CONTEXTS_NORMALIZED[self.normalized_usage_context]
        return self.usage_context

    @property
    def plan_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-ARTIFACT-EMISSION-USAGE-PLAN", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-ARTIFACT-USAGE-PLAN-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "usageContext": self.usage_context,
            "canonicalUsageContext": self.canonical_usage_context,
            "artifactFamilies": list(self.artifact_families),
            "outputNamePrefix": self.output_name_prefix,
            "emissionPurpose": self.emission_purpose,
            "milestoneId": self.milestone_id,
            "sourceTaskId": self.source_task_id,
            "metadata": dict(self.metadata),
            "isAuthorizedUsageContext": self.is_authorized_usage_context,
            "isForbiddenUsageContext": self.is_forbidden_usage_context,
            "artifactEmitterRevision": ARTIFACT_EMITTER_REVISION,
            "artifactEmissionUsageRevision": ARTIFACT_EMISSION_USAGE_REVISION,
            "diagnosticArtifactEmissionUsageOnly": DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_ONLY,
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
            "technicalContinuityEvidenceOnly": True,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
        }
        if include_id:
            payload["planId"] = self.plan_id
        return payload


@dataclass(frozen=True)
class DiagnosticArtifactEmissionUsageRequest:
    """Explicit local controlled artifact emission usage request."""

    usage_result: DiagnosticActivationUsageResult
    usage_plan: DiagnosticArtifactEmissionUsagePlan
    request_label: str = "controlled artifact emission usage request"

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "request_label",
            _clean_text(self.request_label, field_name="request_label"),
        )

    @property
    def request_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-ARTIFACT-EMISSION-USAGE-REQUEST", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-ARTIFACT-USAGE-REQ-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "requestLabel": self.request_label,
            "usagePlan": self.usage_plan.to_public_dict(),
            "sourceUsageResultId": self.usage_result.result_id,
            "sourceUsageOk": self.usage_result.usage_ok,
            "sourceUsageAcceptedCount": self.usage_result.accepted_count,
            "sourceUsageBlockedReferenceCount": self.usage_result.blocked_reference_count,
            "sourceUsageBlockedCallCount": self.usage_result.blocked_call_count,
            "sourceUsageBlockedUsageRequestCount": self.usage_result.blocked_usage_request_count,
            "diagnosticArtifactEmissionUsageOnly": DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_ONLY,
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
            "legalCertification": LEGAL_CERTIFICATION,
        }
        if include_id:
            payload["requestId"] = self.request_id
        return payload


@dataclass(frozen=True)
class DiagnosticArtifactEmissionUsageBlockedRequest:
    """Fail-closed blocked controlled artifact emission usage request."""

    request_id: str
    reason: str
    usage_context: str
    output_name_prefix: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _clean_text(self.request_id, field_name="request_id"))
        object.__setattr__(self, "reason", _clean_text(self.reason, field_name="reason"))
        object.__setattr__(
            self,
            "usage_context",
            _clean_text(self.usage_context, field_name="usage_context"),
        )
        object.__setattr__(
            self,
            "output_name_prefix",
            _clean_text(self.output_name_prefix, field_name="output_name_prefix"),
        )

    @property
    def blocked_request_id(self) -> str:
        digest = stable_digest(
            "SRSC-DIAGNOSTIC-ARTIFACT-EMISSION-USAGE-BLOCKED",
            self.to_public_dict(include_id=False),
        )
        return f"SRSC-DIAG-ARTIFACT-USAGE-BLOCKED-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "requestId": self.request_id,
            "reason": self.reason,
            "usageContext": self.usage_context,
            "outputNamePrefix": self.output_name_prefix,
            "controlledArtifactEmissionUsageImplemented": CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTED,
            "diagnosticArtifactEmissionUsageOnly": DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_ONLY,
            "artifactEmitterModified": ARTIFACT_EMITTER_MODIFIED,
            "usageLayerModified": USAGE_LAYER_MODIFIED,
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
class DiagnosticArtifactEmissionUsageResult:
    """Result for controlled local diagnostic artifact emission usage."""

    usage_request: DiagnosticArtifactEmissionUsageRequest
    artifact_emission_result: DiagnosticUsageArtifactEmissionResult | None = None
    blocked_requests: tuple[DiagnosticArtifactEmissionUsageBlockedRequest, ...] = ()

    @property
    def result_id(self) -> str:
        digest = stable_digest(
            "SRSC-DIAGNOSTIC-ARTIFACT-EMISSION-USAGE-RESULT",
            self.to_public_dict(include_id=False),
        )
        return f"SRSC-DIAG-ARTIFACT-USAGE-RESULT-{digest[:16].upper()}"

    @property
    def emitted_artifact_count(self) -> int:
        if self.artifact_emission_result is None:
            return 0
        return self.artifact_emission_result.emitted_count

    @property
    def blocked_artifact_count(self) -> int:
        if self.artifact_emission_result is None:
            return 0
        return self.artifact_emission_result.blocked_count

    @property
    def blocked_usage_request_count(self) -> int:
        return len(self.blocked_requests)

    @property
    def usage_ok(self) -> bool:
        return (
            CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTED is True
            and DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_ONLY is True
            and ARTIFACT_EMITTER_MODIFIED is False
            and USAGE_LAYER_MODIFIED is False
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
        )

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "taskId": TASK_ID,
            "artifactEmissionUsageRevision": ARTIFACT_EMISSION_USAGE_REVISION,
            "artifactEmitterRevision": ARTIFACT_EMITTER_REVISION,
            "usageRequest": self.usage_request.to_public_dict(),
            "artifactEmissionResult": (
                None
                if self.artifact_emission_result is None
                else self.artifact_emission_result.to_public_dict()
            ),
            "blockedUsageRequests": [
                blocked.to_public_dict() for blocked in self.blocked_requests
            ],
            "emittedArtifactCount": self.emitted_artifact_count,
            "blockedArtifactCount": self.blocked_artifact_count,
            "blockedUsageRequestCount": self.blocked_usage_request_count,
            "usageOk": self.usage_ok,
            "authorizedUsageContexts": list(AUTHORIZED_USAGE_CONTEXTS),
            "forbiddenUsageContexts": list(FORBIDDEN_USAGE_CONTEXTS),
            "authorizedArtifactFamilies": list(AUTHORIZED_ARTIFACT_FAMILIES),
            "forbiddenArtifactFamilies": list(FORBIDDEN_ARTIFACT_FAMILIES),
            "controlledArtifactEmissionUsageImplemented": CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTED,
            "diagnosticArtifactEmissionUsageOnly": DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_ONLY,
            "artifactEmitterModified": ARTIFACT_EMITTER_MODIFIED,
            "usageLayerModified": USAGE_LAYER_MODIFIED,
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
            "technicalContinuityEvidenceOnly": True,
        }
        if include_id:
            payload["resultId"] = self.result_id
        return payload


def build_controlled_artifact_emission_usage_plan(
    *,
    usage_context: str,
    artifact_families: Sequence[str] = DEFAULT_DIAGNOSTIC_ARTIFACT_FAMILIES,
    output_name_prefix: str,
    emission_purpose: str,
    milestone_id: str = "MILESTONE_19",
    source_task_id: str = TASK_ID,
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticArtifactEmissionUsagePlan:
    """Build a deterministic local diagnostic artifact emission usage plan."""

    return DiagnosticArtifactEmissionUsagePlan(
        usage_context=usage_context,
        artifact_families=tuple(artifact_families),
        output_name_prefix=output_name_prefix,
        emission_purpose=emission_purpose,
        milestone_id=milestone_id,
        source_task_id=source_task_id,
        metadata={} if metadata is None else metadata,
    )


def _blocked_result(
    usage_request: DiagnosticArtifactEmissionUsageRequest,
    *,
    reason: str,
) -> DiagnosticArtifactEmissionUsageResult:
    return DiagnosticArtifactEmissionUsageResult(
        usage_request=usage_request,
        artifact_emission_result=None,
        blocked_requests=(
            DiagnosticArtifactEmissionUsageBlockedRequest(
                request_id=usage_request.request_id,
                reason=reason,
                usage_context=usage_request.usage_plan.usage_context,
                output_name_prefix=usage_request.usage_plan.output_name_prefix,
            ),
        ),
    )


def run_controlled_artifact_emission_usage(
    usage_result: DiagnosticActivationUsageResult,
    *,
    usage_context: str,
    artifact_families: Sequence[str] = DEFAULT_DIAGNOSTIC_ARTIFACT_FAMILIES,
    output_name_prefix: str,
    emission_purpose: str,
    milestone_id: str = "MILESTONE_19",
    source_task_id: str = TASK_ID,
    metadata: Mapping[str, Any] | None = None,
    request_label: str = "controlled artifact emission usage request",
) -> DiagnosticArtifactEmissionUsageResult:
    """Run one controlled local diagnostic artifact emission usage request."""

    plan = build_controlled_artifact_emission_usage_plan(
        usage_context=usage_context,
        artifact_families=artifact_families,
        output_name_prefix=output_name_prefix,
        emission_purpose=emission_purpose,
        milestone_id=milestone_id,
        source_task_id=source_task_id,
        metadata={} if metadata is None else metadata,
    )
    request = DiagnosticArtifactEmissionUsageRequest(
        usage_result=usage_result,
        usage_plan=plan,
        request_label=request_label,
    )

    if plan.is_forbidden_usage_context:
        return _blocked_result(request, reason="FORBIDDEN_USAGE_CONTEXT")

    if not plan.is_authorized_usage_context:
        return _blocked_result(request, reason="UNKNOWN_USAGE_CONTEXT")

    emission_result = emit_controlled_usage_artifact_batch(
        usage_result,
        artifact_families=plan.artifact_families,
        output_name_prefix=plan.output_name_prefix,
        source_usage_context=plan.canonical_usage_context,
        emission_purpose=plan.emission_purpose,
        metadata={
            **dict(plan.metadata),
            "milestoneId": plan.milestone_id,
            "sourceTaskId": plan.source_task_id,
            "usagePlanId": plan.plan_id,
            "usageRequestId": request.request_id,
            "usageRunnerRevision": ARTIFACT_EMISSION_USAGE_REVISION,
            "sourceCallSite": "controlled artifact emission usage runner",
        },
    )

    return DiagnosticArtifactEmissionUsageResult(
        usage_request=request,
        artifact_emission_result=emission_result,
        blocked_requests=(),
    )


def run_controlled_artifact_emission_usage_batch(
    usage_results: Sequence[DiagnosticActivationUsageResult],
    *,
    usage_context: str,
    artifact_families: Sequence[str] = DEFAULT_DIAGNOSTIC_ARTIFACT_FAMILIES,
    output_name_prefix: str,
    emission_purpose: str,
    milestone_id: str = "MILESTONE_19",
    source_task_id: str = TASK_ID,
    metadata: Mapping[str, Any] | None = None,
) -> tuple[DiagnosticArtifactEmissionUsageResult, ...]:
    """Run multiple controlled local diagnostic artifact emission usage requests."""

    results: list[DiagnosticArtifactEmissionUsageResult] = []
    for index, usage_result in enumerate(usage_results, start=1):
        results.append(
            run_controlled_artifact_emission_usage(
                usage_result,
                usage_context=usage_context,
                artifact_families=artifact_families,
                output_name_prefix=f"{output_name_prefix}-{index:02d}",
                emission_purpose=emission_purpose,
                milestone_id=milestone_id,
                source_task_id=source_task_id,
                metadata={} if metadata is None else metadata,
                request_label=f"controlled artifact emission usage batch request {index}",
            )
        )
    return tuple(results)


__all__ = [
    "ACTIVATION_WRAPPER_MODIFIED",
    "ADAPTER_MODIFIED",
    "ARTIFACT_EMISSION_USAGE_REVISION",
    "ARTIFACT_EMITTER_MODIFIED",
    "AUTHORIZED_USAGE_CONTEXTS",
    "BENCHMARK_BINDING",
    "BENCHMARK_SCORE_CLAIMED",
    "CANDIDATE_GENERATOR_BINDING",
    "CANDIDATE_GENERATOR_MODIFIED",
    "CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTED",
    "DEFAULT_DIAGNOSTIC_ARTIFACT_FAMILIES",
    "DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_ONLY",
    "EXTERNAL_API_DEPENDENCY",
    "FAIL_CLOSED_ACTIVE",
    "FORBIDDEN_USAGE_CONTEXTS",
    "INTERNET_DURING_EVAL",
    "KAGGLE_AUTHENTICATION_PERFORMED",
    "KAGGLE_SUBMISSION_BINDING",
    "KAGGLE_SUBMISSION_SENT",
    "LEGAL_CERTIFICATION",
    "PRIVATE_CORE_EXPOSURE",
    "RANKER_BINDING",
    "RANKER_MODIFIED",
    "REAL_EVALUATION_PERFORMED",
    "REAL_SUBMISSION_AUTHORIZED",
    "RUNTIME_ACTIVATION_AUTHORIZED",
    "RUNTIME_SOLVER_MODIFIED",
    "RUNTIME_WIRING_ALLOWED",
    "SOLVER_RUNTIME_BINDING",
    "TASK_ID",
    "USAGE_LAYER_MODIFIED",
    "VERIFIER_BINDING",
    "VERIFIER_MODIFIED",
    "DiagnosticArtifactEmissionUsageBlockedRequest",
    "DiagnosticArtifactEmissionUsagePlan",
    "DiagnosticArtifactEmissionUsageRequest",
    "DiagnosticArtifactEmissionUsageResult",
    "build_controlled_artifact_emission_usage_plan",
    "run_controlled_artifact_emission_usage",
    "run_controlled_artifact_emission_usage_batch",
]
