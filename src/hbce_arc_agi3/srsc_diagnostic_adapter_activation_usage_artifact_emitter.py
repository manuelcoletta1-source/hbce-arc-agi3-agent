"""SRSC Diagnostic Adapter Controlled Activation Usage Artifact Emitter.

Milestone #19 Task 101 - local diagnostic-only artifact emission implementation.

This module emits deterministic local diagnostic artifacts from
DiagnosticActivationUsageResult objects. It does not wire into solver runtime,
candidate generation, ranking, verification, benchmarks, Kaggle behavior,
network behavior, or private core behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.srsc_claim_ledger import stable_digest
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage import (
    USAGE_REVISION,
    DiagnosticActivationUsageResult,
)


TASK_ID = "MILESTONE_19_TASK_101_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_LOCAL_IMPLEMENTATION_V1"
ARTIFACT_EMITTER_REVISION = "SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_USAGE_ARTIFACT_EMITTER_LOCAL_STANDALONE_V1"

CONTROLLED_ARTIFACT_EMISSION_IMPLEMENTED = True
DIAGNOSTIC_ARTIFACT_EMISSION_ONLY = True

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


AUTHORIZED_ARTIFACT_FAMILIES: tuple[str, ...] = (
    "local diagnostic report JSON",
    "local diagnostic report Markdown",
    "local milestone evidence package JSON",
    "local public-safe audit summary JSON",
    "local blocked usage report JSON",
    "local cross-trace planner attachment JSON",
    "local manifest fragment JSON",
    "local deterministic index TXT",
)

FORBIDDEN_ARTIFACT_FAMILIES: tuple[str, ...] = (
    "solver performance proof",
    "benchmark proof",
    "Kaggle evidence",
    "production runtime evidence",
    "legal certification evidence",
    "submission package",
    "score report",
    "private core evidence",
)

_JSON_FAMILIES = {
    "local diagnostic report JSON",
    "local milestone evidence package JSON",
    "local public-safe audit summary JSON",
    "local blocked usage report JSON",
    "local cross-trace planner attachment JSON",
    "local manifest fragment JSON",
}
_MARKDOWN_FAMILIES = {"local diagnostic report Markdown"}
_TEXT_FAMILIES = {"local deterministic index TXT"}

_AUTHORIZED_NORMALIZED = {value.lower(): value for value in AUTHORIZED_ARTIFACT_FAMILIES}
_FORBIDDEN_NORMALIZED = {value.lower(): value for value in FORBIDDEN_ARTIFACT_FAMILIES}


def _clean_text(value: str, *, field_name: str) -> str:
    cleaned = " ".join(str(value).strip().split())
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned


def _clean_metadata(value: Mapping[str, Any] | None) -> dict[str, Any]:
    if value is None:
        return {}
    return {str(key): value[key] for key in sorted(value)}


def _normalize_family(value: str) -> str:
    return _clean_text(value, field_name="artifact_family").lower()


def _content_type_for_family(family: str) -> str:
    if family in _JSON_FAMILIES:
        return "application/json"
    if family in _MARKDOWN_FAMILIES:
        return "text/markdown"
    if family in _TEXT_FAMILIES:
        return "text/plain"
    return "application/octet-stream"


def _extension_for_family(family: str) -> str:
    if family in _JSON_FAMILIES:
        return "json"
    if family in _MARKDOWN_FAMILIES:
        return "md"
    if family in _TEXT_FAMILIES:
        return "txt"
    return "bin"


def _slug(value: str) -> str:
    cleaned = "".join(char.lower() if char.isalnum() else "-" for char in value)
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or "artifact"


@dataclass(frozen=True)
class DiagnosticUsageArtifactEmissionRequest:
    """Explicit local diagnostic artifact emission request."""

    artifact_family: str
    usage_result: DiagnosticActivationUsageResult
    output_name: str
    source_usage_context: str
    emission_purpose: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "artifact_family",
            _clean_text(self.artifact_family, field_name="artifact_family"),
        )
        object.__setattr__(self, "output_name", _clean_text(self.output_name, field_name="output_name"))
        object.__setattr__(
            self,
            "source_usage_context",
            _clean_text(self.source_usage_context, field_name="source_usage_context"),
        )
        object.__setattr__(
            self,
            "emission_purpose",
            _clean_text(self.emission_purpose, field_name="emission_purpose"),
        )
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def normalized_artifact_family(self) -> str:
        return _normalize_family(self.artifact_family)

    @property
    def is_authorized_artifact_family(self) -> bool:
        return self.normalized_artifact_family in _AUTHORIZED_NORMALIZED

    @property
    def is_forbidden_artifact_family(self) -> bool:
        return self.normalized_artifact_family in _FORBIDDEN_NORMALIZED

    @property
    def canonical_artifact_family(self) -> str:
        if self.is_authorized_artifact_family:
            return _AUTHORIZED_NORMALIZED[self.normalized_artifact_family]
        if self.is_forbidden_artifact_family:
            return _FORBIDDEN_NORMALIZED[self.normalized_artifact_family]
        return self.artifact_family

    @property
    def request_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-USAGE-ARTIFACT-EMISSION-REQUEST", self.to_public_dict())
        return f"SRSC-DIAG-USAGE-ARTIFACT-EMIT-REQ-{digest[:16].upper()}"

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "artifactFamily": self.artifact_family,
            "canonicalArtifactFamily": self.canonical_artifact_family,
            "normalizedArtifactFamily": self.normalized_artifact_family,
            "outputName": self.output_name,
            "sourceUsageContext": self.source_usage_context,
            "emissionPurpose": self.emission_purpose,
            "sourceUsageResultId": self.usage_result.result_id,
            "sourceUsageRevision": USAGE_REVISION,
            "isAuthorizedArtifactFamily": self.is_authorized_artifact_family,
            "isForbiddenArtifactFamily": self.is_forbidden_artifact_family,
            "metadata": dict(self.metadata),
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
            "publicSafeOnly": True,
            "legalCertification": LEGAL_CERTIFICATION,
        }


@dataclass(frozen=True)
class DiagnosticUsageArtifactEmissionBlockedRequest:
    """Fail-closed blocked artifact emission request."""

    request_id: str
    artifact_family: str
    output_name: str
    reason: str
    source_usage_context: str
    emission_purpose: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "request_id", _clean_text(self.request_id, field_name="request_id"))
        object.__setattr__(
            self,
            "artifact_family",
            _clean_text(self.artifact_family, field_name="artifact_family"),
        )
        object.__setattr__(self, "output_name", _clean_text(self.output_name, field_name="output_name"))
        object.__setattr__(self, "reason", _clean_text(self.reason, field_name="reason"))
        object.__setattr__(
            self,
            "source_usage_context",
            _clean_text(self.source_usage_context, field_name="source_usage_context"),
        )
        object.__setattr__(
            self,
            "emission_purpose",
            _clean_text(self.emission_purpose, field_name="emission_purpose"),
        )

    @property
    def blocked_request_id(self) -> str:
        digest = stable_digest(
            "SRSC-DIAGNOSTIC-USAGE-ARTIFACT-EMISSION-BLOCKED",
            self.to_public_dict(include_id=False),
        )
        return f"SRSC-DIAG-USAGE-ARTIFACT-BLOCKED-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "requestId": self.request_id,
            "artifactFamily": self.artifact_family,
            "outputName": self.output_name,
            "reason": self.reason,
            "sourceUsageContext": self.source_usage_context,
            "emissionPurpose": self.emission_purpose,
            "controlledArtifactEmissionImplemented": CONTROLLED_ARTIFACT_EMISSION_IMPLEMENTED,
            "diagnosticArtifactEmissionOnly": DIAGNOSTIC_ARTIFACT_EMISSION_ONLY,
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
class DiagnosticUsageArtifact:
    """Deterministic public-safe diagnostic artifact."""

    artifact_family: str
    output_name: str
    content_type: str
    content: str
    payload: Mapping[str, Any]
    source_usage_result_id: str
    source_usage_context: str
    emission_purpose: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "artifact_family",
            _clean_text(self.artifact_family, field_name="artifact_family"),
        )
        object.__setattr__(self, "output_name", _clean_text(self.output_name, field_name="output_name"))
        object.__setattr__(self, "content_type", _clean_text(self.content_type, field_name="content_type"))
        object.__setattr__(self, "content", str(self.content))
        object.__setattr__(self, "payload", _clean_metadata(self.payload))
        object.__setattr__(
            self,
            "source_usage_result_id",
            _clean_text(self.source_usage_result_id, field_name="source_usage_result_id"),
        )
        object.__setattr__(
            self,
            "source_usage_context",
            _clean_text(self.source_usage_context, field_name="source_usage_context"),
        )
        object.__setattr__(
            self,
            "emission_purpose",
            _clean_text(self.emission_purpose, field_name="emission_purpose"),
        )

    @property
    def artifact_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-USAGE-ARTIFACT", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-USAGE-ARTIFACT-{digest[:16].upper()}"

    @property
    def filename(self) -> str:
        return f"{_slug(self.output_name)}.{_extension_for_family(self.artifact_family)}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "artifactFamily": self.artifact_family,
            "outputName": self.output_name,
            "filename": self.filename,
            "contentType": self.content_type,
            "content": self.content,
            "payload": dict(self.payload),
            "sourceUsageResultId": self.source_usage_result_id,
            "sourceUsageContext": self.source_usage_context,
            "sourceUsageRevision": USAGE_REVISION,
            "emissionPurpose": self.emission_purpose,
            "artifactEmitterRevision": ARTIFACT_EMITTER_REVISION,
            "controlledArtifactEmissionImplemented": CONTROLLED_ARTIFACT_EMISSION_IMPLEMENTED,
            "diagnosticArtifactEmissionOnly": DIAGNOSTIC_ARTIFACT_EMISSION_ONLY,
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
            "publicSafeOnly": True,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
        }
        if include_id:
            payload["artifactId"] = self.artifact_id
        return payload


@dataclass(frozen=True)
class DiagnosticUsageArtifactEmissionResult:
    """Result of local controlled diagnostic artifact emission."""

    artifacts: tuple[DiagnosticUsageArtifact, ...] = ()
    blocked_requests: tuple[DiagnosticUsageArtifactEmissionBlockedRequest, ...] = ()

    @property
    def result_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-USAGE-ARTIFACT-EMISSION-RESULT", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-USAGE-ARTIFACT-EMISSION-RESULT-{digest[:16].upper()}"

    @property
    def emitted_count(self) -> int:
        return len(self.artifacts)

    @property
    def blocked_count(self) -> int:
        return len(self.blocked_requests)

    @property
    def emission_ok(self) -> bool:
        return (
            CONTROLLED_ARTIFACT_EMISSION_IMPLEMENTED is True
            and DIAGNOSTIC_ARTIFACT_EMISSION_ONLY is True
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
            "artifactEmitterRevision": ARTIFACT_EMITTER_REVISION,
            "sourceUsageRevision": USAGE_REVISION,
            "emittedCount": self.emitted_count,
            "blockedCount": self.blocked_count,
            "emissionOk": self.emission_ok,
            "artifacts": [artifact.to_public_dict() for artifact in self.artifacts],
            "blockedRequests": [blocked.to_public_dict() for blocked in self.blocked_requests],
            "authorizedArtifactFamilies": list(AUTHORIZED_ARTIFACT_FAMILIES),
            "forbiddenArtifactFamilies": list(FORBIDDEN_ARTIFACT_FAMILIES),
            "controlledArtifactEmissionImplemented": CONTROLLED_ARTIFACT_EMISSION_IMPLEMENTED,
            "diagnosticArtifactEmissionOnly": DIAGNOSTIC_ARTIFACT_EMISSION_ONLY,
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
            "publicSafeOnly": True,
        }
        if include_id:
            payload["resultId"] = self.result_id
        return payload

    def to_json(self) -> str:
        return json.dumps(self.to_public_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _artifact_payload(request: DiagnosticUsageArtifactEmissionRequest) -> dict[str, Any]:
    usage_payload = request.usage_result.to_public_dict()
    return {
        "artifactFamily": request.canonical_artifact_family,
        "createdByTaskId": TASK_ID,
        "sourceUsageResultId": request.usage_result.result_id,
        "sourceUsageRevision": USAGE_REVISION,
        "sourceUsageContext": request.source_usage_context,
        "sourceCallSite": request.metadata.get("sourceCallSite", "local diagnostic artifact emission"),
        "emissionPurpose": request.emission_purpose,
        "acceptedCount": request.usage_result.accepted_count,
        "blockedReferenceCount": request.usage_result.blocked_reference_count,
        "blockedCallCount": request.usage_result.blocked_call_count,
        "blockedUsageRequestCount": request.usage_result.blocked_usage_request_count,
        "usageOk": request.usage_result.usage_ok,
        "diagnosticUsageOnly": True,
        "diagnosticArtifactEmissionOnly": True,
        "publicSafeOnly": True,
        "noScoreClaimMarker": True,
        "noSubmissionMarker": True,
        "technicalContinuityEvidenceOnly": True,
        "legalCertification": LEGAL_CERTIFICATION,
        "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
        "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED,
        "solverRuntimeBinding": SOLVER_RUNTIME_BINDING,
        "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
        "failClosedActive": FAIL_CLOSED_ACTIVE,
        "usageResult": usage_payload,
        "metadata": dict(request.metadata),
    }


def _json_content(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2)


def _markdown_content(payload: Mapping[str, Any]) -> str:
    lines = [
        "# SRSC Diagnostic Usage Artifact",
        "",
        f"- Artifact family: {payload['artifactFamily']}",
        f"- Source usage result: {payload['sourceUsageResultId']}",
        f"- Source usage context: {payload['sourceUsageContext']}",
        f"- Accepted count: {payload['acceptedCount']}",
        f"- Blocked reference count: {payload['blockedReferenceCount']}",
        f"- Blocked call count: {payload['blockedCallCount']}",
        f"- Blocked usage request count: {payload['blockedUsageRequestCount']}",
        f"- Diagnostic artifact emission only: {payload['diagnosticArtifactEmissionOnly']}",
        f"- No score claim marker: {payload['noScoreClaimMarker']}",
        f"- No submission marker: {payload['noSubmissionMarker']}",
        f"- Legal certification: {payload['legalCertification']}",
        f"- Fail closed active: {payload['failClosedActive']}",
        "",
        "Boundary: technical continuity evidence only.",
        "",
    ]
    return "\n".join(lines)


def _text_content(payload: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "SRSC DIAGNOSTIC USAGE ARTIFACT INDEX",
            f"artifactFamily={payload['artifactFamily']}",
            f"sourceUsageResultId={payload['sourceUsageResultId']}",
            f"sourceUsageContext={payload['sourceUsageContext']}",
            f"acceptedCount={payload['acceptedCount']}",
            f"blockedReferenceCount={payload['blockedReferenceCount']}",
            f"blockedCallCount={payload['blockedCallCount']}",
            f"blockedUsageRequestCount={payload['blockedUsageRequestCount']}",
            "technicalContinuityEvidenceOnly=true",
            f"legalCertification={str(payload['legalCertification']).lower()}",
            f"failClosedActive={str(payload['failClosedActive']).lower()}",
            "",
        ]
    )


def _content_for_family(family: str, payload: Mapping[str, Any]) -> str:
    if family in _JSON_FAMILIES:
        return _json_content(payload)
    if family in _MARKDOWN_FAMILIES:
        return _markdown_content(payload)
    if family in _TEXT_FAMILIES:
        return _text_content(payload)
    return ""


def _blocked_result(
    *,
    request: DiagnosticUsageArtifactEmissionRequest,
    reason: str,
) -> DiagnosticUsageArtifactEmissionResult:
    return DiagnosticUsageArtifactEmissionResult(
        artifacts=(),
        blocked_requests=(
            DiagnosticUsageArtifactEmissionBlockedRequest(
                request_id=request.request_id,
                artifact_family=request.artifact_family,
                output_name=request.output_name,
                reason=reason,
                source_usage_context=request.source_usage_context,
                emission_purpose=request.emission_purpose,
            ),
        ),
    )


def emit_controlled_usage_artifact(
    usage_result: DiagnosticActivationUsageResult,
    *,
    artifact_family: str,
    output_name: str,
    source_usage_context: str,
    emission_purpose: str,
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticUsageArtifactEmissionResult:
    """Emit one local deterministic diagnostic artifact."""

    request = DiagnosticUsageArtifactEmissionRequest(
        artifact_family=artifact_family,
        usage_result=usage_result,
        output_name=output_name,
        source_usage_context=source_usage_context,
        emission_purpose=emission_purpose,
        metadata={} if metadata is None else metadata,
    )

    if request.is_forbidden_artifact_family:
        return _blocked_result(request=request, reason="FORBIDDEN_ARTIFACT_FAMILY")

    if not request.is_authorized_artifact_family:
        return _blocked_result(request=request, reason="UNKNOWN_ARTIFACT_FAMILY")

    payload = _artifact_payload(request)
    family = request.canonical_artifact_family
    artifact = DiagnosticUsageArtifact(
        artifact_family=family,
        output_name=request.output_name,
        content_type=_content_type_for_family(family),
        content=_content_for_family(family, payload),
        payload=payload,
        source_usage_result_id=request.usage_result.result_id,
        source_usage_context=request.source_usage_context,
        emission_purpose=request.emission_purpose,
    )
    return DiagnosticUsageArtifactEmissionResult(artifacts=(artifact,), blocked_requests=())


def emit_controlled_usage_artifact_batch(
    usage_result: DiagnosticActivationUsageResult,
    *,
    artifact_families: Sequence[str],
    output_name_prefix: str,
    source_usage_context: str,
    emission_purpose: str,
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticUsageArtifactEmissionResult:
    """Emit a batch of local deterministic diagnostic artifacts."""

    artifacts: list[DiagnosticUsageArtifact] = []
    blocked: list[DiagnosticUsageArtifactEmissionBlockedRequest] = []

    for index, family in enumerate(artifact_families, start=1):
        result = emit_controlled_usage_artifact(
            usage_result,
            artifact_family=family,
            output_name=f"{output_name_prefix}-{index:02d}",
            source_usage_context=source_usage_context,
            emission_purpose=emission_purpose,
            metadata={} if metadata is None else metadata,
        )
        artifacts.extend(result.artifacts)
        blocked.extend(result.blocked_requests)

    return DiagnosticUsageArtifactEmissionResult(
        artifacts=tuple(artifacts),
        blocked_requests=tuple(blocked),
    )


__all__ = [
    "ACTIVATION_WRAPPER_MODIFIED",
    "ADAPTER_MODIFIED",
    "ARTIFACT_EMITTER_REVISION",
    "AUTHORIZED_ARTIFACT_FAMILIES",
    "BENCHMARK_BINDING",
    "BENCHMARK_SCORE_CLAIMED",
    "CANDIDATE_GENERATOR_BINDING",
    "CANDIDATE_GENERATOR_MODIFIED",
    "CONTROLLED_ARTIFACT_EMISSION_IMPLEMENTED",
    "DIAGNOSTIC_ARTIFACT_EMISSION_ONLY",
    "EXTERNAL_API_DEPENDENCY",
    "FAIL_CLOSED_ACTIVE",
    "FORBIDDEN_ARTIFACT_FAMILIES",
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
    "USAGE_LAYER_MODIFIED",
    "VERIFIER_BINDING",
    "VERIFIER_MODIFIED",
    "DiagnosticUsageArtifact",
    "DiagnosticUsageArtifactEmissionBlockedRequest",
    "DiagnosticUsageArtifactEmissionRequest",
    "DiagnosticUsageArtifactEmissionResult",
    "emit_controlled_usage_artifact",
    "emit_controlled_usage_artifact_batch",
]
