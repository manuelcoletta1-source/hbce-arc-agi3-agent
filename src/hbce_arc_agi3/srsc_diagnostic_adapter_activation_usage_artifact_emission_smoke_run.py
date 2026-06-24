"""SRSC controlled artifact emission usage smoke-run.

Milestone #19 Task 109 - local diagnostic-only smoke-run implementation.

This module exercises the controlled artifact emission usage runner locally.
It also records the updated PoC v0.9 acceptance specification as a boundary
source. It does not implement PoC v0.9 runtime acceptance, benchmark validation,
fault injection, production readiness, solver runtime wiring, Kaggle submission,
or legal certification.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.srsc_claim_ledger import stable_digest
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage import (
    DiagnosticActivationUsageResult,
    run_controlled_activation_usage,
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_usage import (
    ARTIFACT_EMISSION_USAGE_REVISION,
    DEFAULT_DIAGNOSTIC_ARTIFACT_FAMILIES,
    DiagnosticArtifactEmissionUsageResult,
    run_controlled_artifact_emission_usage,
    run_controlled_artifact_emission_usage_batch,
)


TASK_ID = "MILESTONE_19_TASK_109_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_IMPLEMENTATION_V1"
SMOKE_RUN_REVISION = "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_STANDALONE_V1"

POC_V0_9_SOURCE_DOCUMENT = "docs/srsc-ai-poc-v0-9-bootstrap-reserved-ingress-backoff-governor-reserved-cpu-c1-cancellable-eviction-acceptance-specification.md"
POC_V0_9_STATUS = "POC_V0_9_SPECIFICATION_READY / IMPLEMENTATION_NOT_STARTED"
POC_V0_9_MATURITY = "DESIGNED / NOT_IMPLEMENTED / NOT_TESTED"
POC_V0_9_RUNTIME_IMPLEMENTED = False
POC_V0_9_BENCHMARKED = False
POC_V0_9_FAULT_INJECTION_PERFORMED = False
POC_V0_9_PRODUCTION_READY = False

CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED = True
DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_ONLY = True

USAGE_RUNNER_MODIFIED = False
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


AUTHORIZED_SMOKE_RUN_CASES: tuple[str, ...] = (
    "happy-path diagnostic report smoke-run",
    "custom artifact bundle smoke-run",
    "deterministic index smoke-run",
    "public-safe audit summary smoke-run",
    "forbidden usage context smoke-run",
    "unknown usage context smoke-run",
    "forbidden artifact family smoke-run",
    "mixed allowed and blocked artifact family smoke-run",
    "batch usage smoke-run",
    "deterministic identity smoke-run",
    "boundary marker smoke-run",
    "no-score and no-submission marker smoke-run",
)

FORBIDDEN_SMOKE_RUN_CASES: tuple[str, ...] = (
    "solver runtime smoke-run",
    "candidate generator smoke-run",
    "ranker score smoke-run",
    "verifier score smoke-run",
    "benchmark smoke-run",
    "Kaggle submission smoke-run",
    "public score smoke-run",
    "private score smoke-run",
    "production runtime smoke-run",
    "network/API smoke-run",
    "private core smoke-run",
    "legal certification smoke-run",
)

_AUTHORIZED_CASES = {value.lower(): value for value in AUTHORIZED_SMOKE_RUN_CASES}
_FORBIDDEN_CASES = {value.lower(): value for value in FORBIDDEN_SMOKE_RUN_CASES}


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


@dataclass(frozen=True)
class DiagnosticArtifactEmissionUsageSmokeRunPlan:
    smoke_run_scope: str = "local diagnostic artifact usage smoke-run"
    source_task_id: str = TASK_ID
    milestone_id: str = "MILESTONE_19"
    poc_v0_9_source_document: str = POC_V0_9_SOURCE_DOCUMENT
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "smoke_run_scope", _clean_text(self.smoke_run_scope, field_name="smoke_run_scope"))
        object.__setattr__(self, "source_task_id", _clean_text(self.source_task_id, field_name="source_task_id"))
        object.__setattr__(self, "milestone_id", _clean_text(self.milestone_id, field_name="milestone_id"))
        object.__setattr__(self, "poc_v0_9_source_document", _clean_text(self.poc_v0_9_source_document, field_name="poc_v0_9_source_document"))
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def plan_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-ARTIFACT-EMISSION-SMOKE-RUN-PLAN", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-ARTIFACT-SMOKE-RUN-PLAN-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "smokeRunScope": self.smoke_run_scope,
            "sourceTaskId": self.source_task_id,
            "milestoneId": self.milestone_id,
            "pocV09SourceDocument": self.poc_v0_9_source_document,
            "pocV09Status": POC_V0_9_STATUS,
            "pocV09Maturity": POC_V0_9_MATURITY,
            "pocV09RuntimeImplemented": POC_V0_9_RUNTIME_IMPLEMENTED,
            "pocV09Benchmarked": POC_V0_9_BENCHMARKED,
            "pocV09FaultInjectionPerformed": POC_V0_9_FAULT_INJECTION_PERFORMED,
            "pocV09ProductionReady": POC_V0_9_PRODUCTION_READY,
            "metadata": dict(self.metadata),
            "smokeRunRevision": SMOKE_RUN_REVISION,
            "artifactEmissionUsageRevision": ARTIFACT_EMISSION_USAGE_REVISION,
            "diagnosticArtifactEmissionUsageSmokeRunOnly": DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_ONLY,
            "technicalContinuityEvidenceOnly": True,
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
        }
        if include_id:
            payload["planId"] = self.plan_id
        return payload


@dataclass(frozen=True)
class DiagnosticArtifactEmissionUsageSmokeRunCase:
    case_id: str
    case_name: str
    usage_context: str
    artifact_families: tuple[str, ...] = DEFAULT_DIAGNOSTIC_ARTIFACT_FAMILIES
    output_name_prefix: str = "srsc-smoke-run"
    emission_purpose: str = "controlled artifact emission usage smoke-run"
    expected_emitted_count: int | None = None
    expected_blocked_artifact_count: int | None = None
    expected_blocked_usage_request_count: int | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "case_id", _clean_text(self.case_id, field_name="case_id"))
        object.__setattr__(self, "case_name", _clean_text(self.case_name, field_name="case_name"))
        object.__setattr__(self, "usage_context", _clean_text(self.usage_context, field_name="usage_context"))
        object.__setattr__(self, "artifact_families", _clean_tuple(self.artifact_families, field_name="artifact_families"))
        object.__setattr__(self, "output_name_prefix", _clean_text(self.output_name_prefix, field_name="output_name_prefix"))
        object.__setattr__(self, "emission_purpose", _clean_text(self.emission_purpose, field_name="emission_purpose"))
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def normalized_case_name(self) -> str:
        return self.case_name.lower()

    @property
    def is_authorized_case(self) -> bool:
        return self.normalized_case_name in _AUTHORIZED_CASES

    @property
    def is_forbidden_case(self) -> bool:
        return self.normalized_case_name in _FORBIDDEN_CASES

    @property
    def smoke_run_case_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-ARTIFACT-EMISSION-SMOKE-RUN-CASE", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-ARTIFACT-SMOKE-CASE-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "caseId": self.case_id,
            "caseName": self.case_name,
            "usageContext": self.usage_context,
            "artifactFamilies": list(self.artifact_families),
            "outputNamePrefix": self.output_name_prefix,
            "emissionPurpose": self.emission_purpose,
            "expectedEmittedCount": self.expected_emitted_count,
            "expectedBlockedArtifactCount": self.expected_blocked_artifact_count,
            "expectedBlockedUsageRequestCount": self.expected_blocked_usage_request_count,
            "metadata": dict(self.metadata),
            "isAuthorizedCase": self.is_authorized_case,
            "isForbiddenCase": self.is_forbidden_case,
        }
        if include_id:
            payload["smokeRunCaseId"] = self.smoke_run_case_id
        return payload


@dataclass(frozen=True)
class DiagnosticArtifactEmissionUsageSmokeRunResult:
    plan: DiagnosticArtifactEmissionUsageSmokeRunPlan
    smoke_run_case: DiagnosticArtifactEmissionUsageSmokeRunCase
    activation_usage_result: DiagnosticActivationUsageResult
    artifact_emission_usage_result: DiagnosticArtifactEmissionUsageResult | None
    blocked_reason: str | None = None

    @property
    def smoke_run_result_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-ARTIFACT-EMISSION-SMOKE-RUN-RESULT", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-ARTIFACT-SMOKE-RESULT-{digest[:16].upper()}"

    @property
    def emitted_artifact_count(self) -> int:
        return 0 if self.artifact_emission_usage_result is None else self.artifact_emission_usage_result.emitted_artifact_count

    @property
    def blocked_artifact_count(self) -> int:
        return 0 if self.artifact_emission_usage_result is None else self.artifact_emission_usage_result.blocked_artifact_count

    @property
    def blocked_usage_request_count(self) -> int:
        return 1 if self.artifact_emission_usage_result is None else self.artifact_emission_usage_result.blocked_usage_request_count

    @property
    def expectation_ok(self) -> bool:
        checks: list[bool] = []
        if self.smoke_run_case.expected_emitted_count is not None:
            checks.append(self.emitted_artifact_count == self.smoke_run_case.expected_emitted_count)
        if self.smoke_run_case.expected_blocked_artifact_count is not None:
            checks.append(self.blocked_artifact_count == self.smoke_run_case.expected_blocked_artifact_count)
        if self.smoke_run_case.expected_blocked_usage_request_count is not None:
            checks.append(self.blocked_usage_request_count == self.smoke_run_case.expected_blocked_usage_request_count)
        return all(checks) if checks else True

    @property
    def smoke_run_ok(self) -> bool:
        return (
            self.blocked_reason is None
            and self.expectation_ok
            and CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED is True
            and DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_ONLY is True
            and USAGE_RUNNER_MODIFIED is False
            and ARTIFACT_EMITTER_MODIFIED is False
            and RUNTIME_SOLVER_MODIFIED is False
            and RUNTIME_WIRING_ALLOWED is False
            and SOLVER_RUNTIME_BINDING is False
            and BENCHMARK_SCORE_CLAIMED is False
            and KAGGLE_SUBMISSION_SENT is False
            and LEGAL_CERTIFICATION is False
            and FAIL_CLOSED_ACTIVE is True
        )

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "taskId": TASK_ID,
            "smokeRunRevision": SMOKE_RUN_REVISION,
            "plan": self.plan.to_public_dict(),
            "case": self.smoke_run_case.to_public_dict(),
            "activationUsageResultId": self.activation_usage_result.result_id,
            "artifactEmissionUsageResult": None if self.artifact_emission_usage_result is None else self.artifact_emission_usage_result.to_public_dict(),
            "blockedReason": self.blocked_reason,
            "emittedArtifactCount": self.emitted_artifact_count,
            "blockedArtifactCount": self.blocked_artifact_count,
            "blockedUsageRequestCount": self.blocked_usage_request_count,
            "expectationOk": self.expectation_ok,
            "smokeRunOk": self.smoke_run_ok,
            "pocV09Status": POC_V0_9_STATUS,
            "pocV09Maturity": POC_V0_9_MATURITY,
            "pocV09RuntimeImplemented": POC_V0_9_RUNTIME_IMPLEMENTED,
            "pocV09Benchmarked": POC_V0_9_BENCHMARKED,
            "pocV09FaultInjectionPerformed": POC_V0_9_FAULT_INJECTION_PERFORMED,
            "pocV09ProductionReady": POC_V0_9_PRODUCTION_READY,
            "controlledArtifactEmissionUsageSmokeRunImplemented": CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED,
            "diagnosticArtifactEmissionUsageSmokeRunOnly": DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_ONLY,
            "usageRunnerModified": USAGE_RUNNER_MODIFIED,
            "artifactEmitterModified": ARTIFACT_EMITTER_MODIFIED,
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED,
            "solverRuntimeBinding": SOLVER_RUNTIME_BINDING,
            "benchmarkScoreClaimed": BENCHMARK_SCORE_CLAIMED,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
            "privateCoreExposure": PRIVATE_CORE_EXPOSURE,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
            "technicalContinuityEvidenceOnly": True,
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
        }
        if include_id:
            payload["smokeRunResultId"] = self.smoke_run_result_id
        return payload


@dataclass(frozen=True)
class DiagnosticArtifactEmissionUsageSmokeRunSuiteResult:
    plan: DiagnosticArtifactEmissionUsageSmokeRunPlan
    results: tuple[DiagnosticArtifactEmissionUsageSmokeRunResult, ...]

    @property
    def suite_result_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-ARTIFACT-EMISSION-SMOKE-RUN-SUITE", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-ARTIFACT-SMOKE-SUITE-{digest[:16].upper()}"

    @property
    def case_count(self) -> int:
        return len(self.results)

    @property
    def passed_count(self) -> int:
        return sum(1 for result in self.results if result.smoke_run_ok)

    @property
    def failed_count(self) -> int:
        return self.case_count - self.passed_count

    @property
    def suite_ok(self) -> bool:
        return self.case_count > 0 and self.failed_count == 0

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "taskId": TASK_ID,
            "smokeRunRevision": SMOKE_RUN_REVISION,
            "plan": self.plan.to_public_dict(),
            "results": [result.to_public_dict() for result in self.results],
            "caseCount": self.case_count,
            "passedCount": self.passed_count,
            "failedCount": self.failed_count,
            "suiteOk": self.suite_ok,
            "pocV09SourceDocument": self.plan.poc_v0_9_source_document,
            "pocV09Status": POC_V0_9_STATUS,
            "pocV09Maturity": POC_V0_9_MATURITY,
            "pocV09RuntimeImplemented": POC_V0_9_RUNTIME_IMPLEMENTED,
            "pocV09Benchmarked": POC_V0_9_BENCHMARKED,
            "pocV09FaultInjectionPerformed": POC_V0_9_FAULT_INJECTION_PERFORMED,
            "pocV09ProductionReady": POC_V0_9_PRODUCTION_READY,
            "controlledArtifactEmissionUsageSmokeRunImplemented": CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED,
            "diagnosticArtifactEmissionUsageSmokeRunOnly": DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_ONLY,
            "usageRunnerModified": USAGE_RUNNER_MODIFIED,
            "artifactEmitterModified": ARTIFACT_EMITTER_MODIFIED,
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED,
            "solverRuntimeBinding": SOLVER_RUNTIME_BINDING,
            "benchmarkScoreClaimed": BENCHMARK_SCORE_CLAIMED,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
            "privateCoreExposure": PRIVATE_CORE_EXPOSURE,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
            "technicalContinuityEvidenceOnly": True,
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
        }
        if include_id:
            payload["suiteResultId"] = self.suite_result_id
        return payload


def build_controlled_artifact_emission_usage_smoke_run_plan(
    *,
    smoke_run_scope: str = "local diagnostic artifact usage smoke-run",
    source_task_id: str = TASK_ID,
    milestone_id: str = "MILESTONE_19",
    poc_v0_9_source_document: str = POC_V0_9_SOURCE_DOCUMENT,
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticArtifactEmissionUsageSmokeRunPlan:
    return DiagnosticArtifactEmissionUsageSmokeRunPlan(
        smoke_run_scope=smoke_run_scope,
        source_task_id=source_task_id,
        milestone_id=milestone_id,
        poc_v0_9_source_document=poc_v0_9_source_document,
        metadata={} if metadata is None else metadata,
    )


def build_smoke_run_activation_usage_result(
    smoke_run_case: DiagnosticArtifactEmissionUsageSmokeRunCase,
    *,
    plan: DiagnosticArtifactEmissionUsageSmokeRunPlan,
) -> DiagnosticActivationUsageResult:
    payload = {
        "source_type": "CROSS_TRACE_DIAGNOSTIC_PLANNER_RECORD",
        "source_path": plan.poc_v0_9_source_document,
        "diagnostic_scope": smoke_run_case.case_name,
        "srsc_claim_id": "SRSC-CLAIM-12619C6F83128C07",
        "srsc_gate_decision_id": "SRSC-GATE-447AC5ED3C956D7E",
        "claim_state": "VERIFIED",
        "evidence_state": "PRESENT",
        "evidence_refs": (
            "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py",
            plan.poc_v0_9_source_document,
        ),
        "approved_for_record": True,
        "approved_as_verified": True,
        "metadata": {
            "smokeRunCaseId": smoke_run_case.case_id,
            "smokeRunCaseName": smoke_run_case.case_name,
            "pocV09Status": POC_V0_9_STATUS,
            "pocV09Maturity": POC_V0_9_MATURITY,
            "pocV09RuntimeImplemented": POC_V0_9_RUNTIME_IMPLEMENTED,
            "pocV09Benchmarked": POC_V0_9_BENCHMARKED,
            "pocV09FaultInjectionPerformed": POC_V0_9_FAULT_INJECTION_PERFORMED,
            "pocV09ProductionReady": POC_V0_9_PRODUCTION_READY,
            **dict(smoke_run_case.metadata),
        },
    }

    return run_controlled_activation_usage(
        payload,
        usage_context="local SRSC diagnostic report generation",
        call_site="controlled artifact emission usage smoke-run",
        source_artifact_path=plan.poc_v0_9_source_document,
        diagnostic_purpose=smoke_run_case.emission_purpose,
    )


def run_controlled_artifact_emission_usage_smoke_run(
    smoke_run_case: DiagnosticArtifactEmissionUsageSmokeRunCase,
    *,
    plan: DiagnosticArtifactEmissionUsageSmokeRunPlan | None = None,
) -> DiagnosticArtifactEmissionUsageSmokeRunResult:
    active_plan = plan or build_controlled_artifact_emission_usage_smoke_run_plan()
    activation_result = build_smoke_run_activation_usage_result(smoke_run_case, plan=active_plan)

    if smoke_run_case.is_forbidden_case:
        return DiagnosticArtifactEmissionUsageSmokeRunResult(
            plan=active_plan,
            smoke_run_case=smoke_run_case,
            activation_usage_result=activation_result,
            artifact_emission_usage_result=None,
            blocked_reason="FORBIDDEN_SMOKE_RUN_CASE",
        )

    if not smoke_run_case.is_authorized_case:
        return DiagnosticArtifactEmissionUsageSmokeRunResult(
            plan=active_plan,
            smoke_run_case=smoke_run_case,
            activation_usage_result=activation_result,
            artifact_emission_usage_result=None,
            blocked_reason="UNKNOWN_SMOKE_RUN_CASE",
        )

    artifact_result = run_controlled_artifact_emission_usage(
        activation_result,
        usage_context=smoke_run_case.usage_context,
        artifact_families=smoke_run_case.artifact_families,
        output_name_prefix=smoke_run_case.output_name_prefix,
        emission_purpose=smoke_run_case.emission_purpose,
        milestone_id=active_plan.milestone_id,
        source_task_id=active_plan.source_task_id,
        metadata={
            "smokeRunPlanId": active_plan.plan_id,
            "smokeRunCaseId": smoke_run_case.smoke_run_case_id,
            "smokeRunRevision": SMOKE_RUN_REVISION,
            "pocV09SourceDocument": active_plan.poc_v0_9_source_document,
            "pocV09Status": POC_V0_9_STATUS,
            "pocV09Maturity": POC_V0_9_MATURITY,
            **dict(smoke_run_case.metadata),
        },
        request_label=f"controlled artifact emission smoke-run request: {smoke_run_case.case_name}",
    )

    return DiagnosticArtifactEmissionUsageSmokeRunResult(
        plan=active_plan,
        smoke_run_case=smoke_run_case,
        activation_usage_result=activation_result,
        artifact_emission_usage_result=artifact_result,
        blocked_reason=None,
    )


def default_smoke_run_cases() -> tuple[DiagnosticArtifactEmissionUsageSmokeRunCase, ...]:
    return (
        DiagnosticArtifactEmissionUsageSmokeRunCase(
            case_id="SMOKE-001",
            case_name="happy-path diagnostic report smoke-run",
            usage_context="local diagnostic artifact usage",
            artifact_families=("local diagnostic report JSON",),
            output_name_prefix="task-109-happy-path",
            emission_purpose="Task 109 happy-path diagnostic report smoke-run",
            expected_emitted_count=1,
            expected_blocked_artifact_count=0,
            expected_blocked_usage_request_count=0,
        ),
        DiagnosticArtifactEmissionUsageSmokeRunCase(
            case_id="SMOKE-002",
            case_name="custom artifact bundle smoke-run",
            usage_context="local milestone artifact bundle usage",
            artifact_families=("local diagnostic report JSON", "local diagnostic report Markdown", "local deterministic index TXT"),
            output_name_prefix="task-109-bundle",
            emission_purpose="Task 109 custom artifact bundle smoke-run",
            expected_emitted_count=3,
            expected_blocked_artifact_count=0,
            expected_blocked_usage_request_count=0,
        ),
        DiagnosticArtifactEmissionUsageSmokeRunCase(
            case_id="SMOKE-003",
            case_name="deterministic index smoke-run",
            usage_context="local deterministic index artifact usage",
            artifact_families=("local deterministic index TXT",),
            output_name_prefix="task-109-index",
            emission_purpose="Task 109 deterministic index smoke-run",
            expected_emitted_count=1,
            expected_blocked_artifact_count=0,
            expected_blocked_usage_request_count=0,
        ),
        DiagnosticArtifactEmissionUsageSmokeRunCase(
            case_id="SMOKE-004",
            case_name="forbidden usage context smoke-run",
            usage_context="benchmark artifact usage",
            artifact_families=("local diagnostic report JSON",),
            output_name_prefix="task-109-forbidden-context",
            emission_purpose="Task 109 forbidden usage context smoke-run",
            expected_emitted_count=0,
            expected_blocked_artifact_count=0,
            expected_blocked_usage_request_count=1,
        ),
        DiagnosticArtifactEmissionUsageSmokeRunCase(
            case_id="SMOKE-005",
            case_name="forbidden artifact family smoke-run",
            usage_context="local diagnostic artifact usage",
            artifact_families=("score report",),
            output_name_prefix="task-109-forbidden-family",
            emission_purpose="Task 109 forbidden artifact family smoke-run",
            expected_emitted_count=0,
            expected_blocked_artifact_count=1,
            expected_blocked_usage_request_count=0,
        ),
        DiagnosticArtifactEmissionUsageSmokeRunCase(
            case_id="SMOKE-006",
            case_name="mixed allowed and blocked artifact family smoke-run",
            usage_context="local diagnostic artifact usage",
            artifact_families=("local diagnostic report JSON", "score report", "local deterministic index TXT"),
            output_name_prefix="task-109-mixed-family",
            emission_purpose="Task 109 mixed allowed and blocked artifact family smoke-run",
            expected_emitted_count=2,
            expected_blocked_artifact_count=1,
            expected_blocked_usage_request_count=0,
        ),
        DiagnosticArtifactEmissionUsageSmokeRunCase(
            case_id="SMOKE-007",
            case_name="boundary marker smoke-run",
            usage_context="local public-safe audit artifact usage",
            artifact_families=("local public-safe audit summary JSON",),
            output_name_prefix="task-109-boundary",
            emission_purpose="Task 109 boundary marker smoke-run",
            expected_emitted_count=1,
            expected_blocked_artifact_count=0,
            expected_blocked_usage_request_count=0,
        ),
        DiagnosticArtifactEmissionUsageSmokeRunCase(
            case_id="SMOKE-008",
            case_name="no-score and no-submission marker smoke-run",
            usage_context="local evidence package artifact usage",
            artifact_families=("local diagnostic report JSON",),
            output_name_prefix="task-109-no-score-no-submission",
            emission_purpose="Task 109 no-score and no-submission marker smoke-run",
            expected_emitted_count=1,
            expected_blocked_artifact_count=0,
            expected_blocked_usage_request_count=0,
        ),
    )


def run_controlled_artifact_emission_usage_smoke_run_suite(
    smoke_run_cases: Sequence[DiagnosticArtifactEmissionUsageSmokeRunCase] | None = None,
    *,
    plan: DiagnosticArtifactEmissionUsageSmokeRunPlan | None = None,
) -> DiagnosticArtifactEmissionUsageSmokeRunSuiteResult:
    active_plan = plan or build_controlled_artifact_emission_usage_smoke_run_plan()
    cases = tuple(smoke_run_cases) if smoke_run_cases is not None else default_smoke_run_cases()
    results = tuple(run_controlled_artifact_emission_usage_smoke_run(case, plan=active_plan) for case in cases)
    return DiagnosticArtifactEmissionUsageSmokeRunSuiteResult(plan=active_plan, results=results)


def run_default_batch_usage_smoke_run(
    *,
    plan: DiagnosticArtifactEmissionUsageSmokeRunPlan | None = None,
) -> tuple[DiagnosticArtifactEmissionUsageResult, ...]:
    active_plan = plan or build_controlled_artifact_emission_usage_smoke_run_plan()

    cases = (
        DiagnosticArtifactEmissionUsageSmokeRunCase(
            case_id="BATCH-001",
            case_name="batch usage smoke-run",
            usage_context="local deterministic index artifact usage",
            artifact_families=("local deterministic index TXT",),
            output_name_prefix="task-109-batch-a",
            emission_purpose="Task 109 batch usage smoke-run A",
        ),
        DiagnosticArtifactEmissionUsageSmokeRunCase(
            case_id="BATCH-002",
            case_name="batch usage smoke-run",
            usage_context="local deterministic index artifact usage",
            artifact_families=("local deterministic index TXT",),
            output_name_prefix="task-109-batch-b",
            emission_purpose="Task 109 batch usage smoke-run B",
        ),
    )

    usage_results = tuple(build_smoke_run_activation_usage_result(case, plan=active_plan) for case in cases)

    return run_controlled_artifact_emission_usage_batch(
        usage_results,
        usage_context="local deterministic index artifact usage",
        artifact_families=("local deterministic index TXT",),
        output_name_prefix="task-109-batch",
        emission_purpose="Task 109 batch usage smoke-run",
        milestone_id=active_plan.milestone_id,
        source_task_id=active_plan.source_task_id,
        metadata={
            "smokeRunPlanId": active_plan.plan_id,
            "smokeRunRevision": SMOKE_RUN_REVISION,
            "pocV09SourceDocument": active_plan.poc_v0_9_source_document,
            "pocV09Status": POC_V0_9_STATUS,
            "pocV09Maturity": POC_V0_9_MATURITY,
        },
    )
