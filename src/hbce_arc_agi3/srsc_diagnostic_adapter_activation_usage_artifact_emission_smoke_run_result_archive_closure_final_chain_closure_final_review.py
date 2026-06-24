"""SRSC controlled smoke-run result archive closure final-chain closure final review.

Milestone #19 Task 129 - local diagnostic-only final review implementation.

This module reviews the already-closed final-chain closure from Task 125,
accepted by Task 126 and authorized by Task 128. It does not modify solver
runtime, benchmark behavior, Kaggle behavior, private-core exposure, raw payload
handling, secrets, credentials or legal certification. Humanity survives another
audit because the flags remain false.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.srsc_claim_ledger import stable_digest
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run import (
    POC_V0_9_BENCHMARKED,
    POC_V0_9_FAULT_INJECTION_PERFORMED,
    POC_V0_9_MATURITY,
    POC_V0_9_PRODUCTION_READY,
    POC_V0_9_RUNTIME_IMPLEMENTED,
    POC_V0_9_SOURCE_DOCUMENT,
    POC_V0_9_STATUS,
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure import (
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTED,
    COVERED_TASK_RANGE,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_ONLY,
    FINAL_CHAIN_CLOSURE_REVISION,
    TASK_ID as FINAL_CHAIN_CLOSURE_TASK_ID,
    DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosure,
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure,
)


TASK_ID = "MILESTONE_19_TASK_129_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_LOCAL_IMPLEMENTATION_V1"
AUTHORIZATION_TASK_ID = "MILESTONE_19_TASK_128_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_AUTHORIZATION_REVIEW_V1"
PLANNING_TASK_ID = "MILESTONE_19_TASK_127_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_PLANNING_V1"
IMPLEMENTATION_REVIEW_TASK_ID = "MILESTONE_19_TASK_126_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTATION_REVIEW_V1"

FINAL_REVIEW_REVISION = "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_LOCAL_V1"

CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_IMPLEMENTED = True
DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ONLY = True

FINAL_CHAIN_CLOSURE_MODIFIED = False
FINAL_CHAIN_CLOSURE_MODULE_MODIFIED = False
CLOSURE_FINALIZATION_MODIFIED = False
CLOSURE_FINALIZATION_MODULE_MODIFIED = False
CLOSURE_MODIFIED = False
CLOSURE_MODULE_MODIFIED = False
RESULT_ARCHIVE_MODIFIED = False
RESULT_ARCHIVE_MODULE_MODIFIED = False
SMOKE_RUN_MODULE_MODIFIED = False
USAGE_RUNNER_MODIFIED = False
ARTIFACT_EMITTER_MODIFIED = False

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

KAGGLE_AUTHENTICATION_PERFORMED = False
KAGGLE_SUBMISSION_SENT = False
KAGGLE_SUBMISSION_BINDING = False

INTERNET_DURING_EVAL = False
EXTERNAL_API_DEPENDENCY = False
PRIVATE_CORE_EXPOSURE = False

RAW_REQUEST_BODY_PERSISTED = False
SECRET_PERSISTED = False
CREDENTIAL_PERSISTED = False
API_KEY_PERSISTED = False

LEGAL_CERTIFICATION = False
FAIL_CLOSED_ACTIVE = True


def _clean_text(value: str, *, field_name: str) -> str:
    cleaned = " ".join(str(value).strip().split())
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned


def _clean_metadata(value: Mapping[str, Any] | None) -> dict[str, Any]:
    if value is None:
        return {}
    return {str(key): value[key] for key in sorted(value)}


def _clean_tuple(values: Sequence[str], *, field_name: str) -> tuple[str, ...]:
    cleaned = tuple(_clean_text(value, field_name=field_name) for value in values)
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned


@dataclass(frozen=True)
class DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosureFinalReviewPlan:
    """Plan for local deterministic final review of the final-chain closure."""

    final_review_scope: str = "local diagnostic final-chain closure final review"
    covered_task_range: str = COVERED_TASK_RANGE
    source_final_chain_closure_task_id: str = FINAL_CHAIN_CLOSURE_TASK_ID
    implementation_review_task_id: str = IMPLEMENTATION_REVIEW_TASK_ID
    planning_task_id: str = PLANNING_TASK_ID
    authorization_task_id: str = AUTHORIZATION_TASK_ID
    final_review_purpose: str = "review final-chain closure technical continuity and public-safe boundary"
    poc_v0_9_source_document: str = POC_V0_9_SOURCE_DOCUMENT
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "final_review_scope", _clean_text(self.final_review_scope, field_name="final_review_scope"))
        object.__setattr__(self, "covered_task_range", _clean_text(self.covered_task_range, field_name="covered_task_range"))
        object.__setattr__(self, "source_final_chain_closure_task_id", _clean_text(self.source_final_chain_closure_task_id, field_name="source_final_chain_closure_task_id"))
        object.__setattr__(self, "implementation_review_task_id", _clean_text(self.implementation_review_task_id, field_name="implementation_review_task_id"))
        object.__setattr__(self, "planning_task_id", _clean_text(self.planning_task_id, field_name="planning_task_id"))
        object.__setattr__(self, "authorization_task_id", _clean_text(self.authorization_task_id, field_name="authorization_task_id"))
        object.__setattr__(self, "final_review_purpose", _clean_text(self.final_review_purpose, field_name="final_review_purpose"))
        object.__setattr__(self, "poc_v0_9_source_document", _clean_text(self.poc_v0_9_source_document, field_name="poc_v0_9_source_document"))
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def final_review_plan_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-SMOKE-RUN-ARCHIVE-CLOSURE-FINAL-CHAIN-CLOSURE-FINAL-REVIEW-PLAN", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-FINAL-CHAIN-FINAL-REVIEW-PLAN-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "finalReviewScope": self.final_review_scope,
            "coveredTaskRange": self.covered_task_range,
            "sourceFinalChainClosureTaskId": self.source_final_chain_closure_task_id,
            "implementationReviewTaskId": self.implementation_review_task_id,
            "planningTaskId": self.planning_task_id,
            "authorizationTaskId": self.authorization_task_id,
            "finalReviewPurpose": self.final_review_purpose,
            "pocV09SourceDocument": self.poc_v0_9_source_document,
            "pocV09Status": POC_V0_9_STATUS,
            "pocV09Maturity": POC_V0_9_MATURITY,
            "pocV09RuntimeImplemented": POC_V0_9_RUNTIME_IMPLEMENTED,
            "pocV09Benchmarked": POC_V0_9_BENCHMARKED,
            "pocV09FaultInjectionPerformed": POC_V0_9_FAULT_INJECTION_PERFORMED,
            "pocV09ProductionReady": POC_V0_9_PRODUCTION_READY,
            "metadata": dict(self.metadata),
            "finalReviewRevision": FINAL_REVIEW_REVISION,
            "technicalContinuityEvidenceOnly": True,
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
        }
        if include_id:
            payload["finalReviewPlanId"] = self.final_review_plan_id
        return payload


@dataclass(frozen=True)
class DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosureFinalReview:
    """Public-safe final review record for the final-chain closure."""

    plan: DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosureFinalReviewPlan
    source_final_chain_closure_id: str
    source_final_chain_closure_ok: bool
    source_final_chain_closure_validation_issues: tuple[str, ...]
    source_finalization_id: str
    source_closure_id: str
    source_archive_id: str
    source_suite_result_id: str
    source_archived_case_count: int
    source_archived_passed_count: int
    source_archived_failed_count: int
    chain_coverage_tasks: tuple[str, ...]
    reviewed_final_chain_closure_artifact_paths: tuple[str, ...]
    reviewed_final_chain_closure_module_path: str
    reviewed_final_chain_closure_test_paths: tuple[str, ...]
    accepted_implementation_review_task_id: str = IMPLEMENTATION_REVIEW_TASK_ID
    authorization_task_id: str = AUTHORIZATION_TASK_ID
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_final_chain_closure_id", _clean_text(self.source_final_chain_closure_id, field_name="source_final_chain_closure_id"))
        object.__setattr__(self, "source_final_chain_closure_validation_issues", tuple(str(issue) for issue in self.source_final_chain_closure_validation_issues))
        object.__setattr__(self, "source_finalization_id", _clean_text(self.source_finalization_id, field_name="source_finalization_id"))
        object.__setattr__(self, "source_closure_id", _clean_text(self.source_closure_id, field_name="source_closure_id"))
        object.__setattr__(self, "source_archive_id", _clean_text(self.source_archive_id, field_name="source_archive_id"))
        object.__setattr__(self, "source_suite_result_id", _clean_text(self.source_suite_result_id, field_name="source_suite_result_id"))
        object.__setattr__(self, "chain_coverage_tasks", _clean_tuple(self.chain_coverage_tasks, field_name="chain_coverage_tasks"))
        object.__setattr__(self, "reviewed_final_chain_closure_artifact_paths", _clean_tuple(self.reviewed_final_chain_closure_artifact_paths, field_name="reviewed_final_chain_closure_artifact_paths"))
        object.__setattr__(self, "reviewed_final_chain_closure_module_path", _clean_text(self.reviewed_final_chain_closure_module_path, field_name="reviewed_final_chain_closure_module_path"))
        object.__setattr__(self, "reviewed_final_chain_closure_test_paths", _clean_tuple(self.reviewed_final_chain_closure_test_paths, field_name="reviewed_final_chain_closure_test_paths"))
        object.__setattr__(self, "accepted_implementation_review_task_id", _clean_text(self.accepted_implementation_review_task_id, field_name="accepted_implementation_review_task_id"))
        object.__setattr__(self, "authorization_task_id", _clean_text(self.authorization_task_id, field_name="authorization_task_id"))
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def final_review_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-SMOKE-RUN-ARCHIVE-CLOSURE-FINAL-CHAIN-CLOSURE-FINAL-REVIEW", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-FINAL-CHAIN-FINAL-REVIEW-{digest[:16].upper()}"

    @property
    def final_review_ok(self) -> bool:
        return (
            CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_IMPLEMENTED is True
            and DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ONLY is True
            and CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTED is True
            and DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_ONLY is True
            and self.source_final_chain_closure_ok is True
            and len(self.source_final_chain_closure_validation_issues) == 0
            and self.source_archived_case_count == 8
            and self.source_archived_passed_count == 8
            and self.source_archived_failed_count == 0
            and self.plan.covered_task_range == COVERED_TASK_RANGE
            and len(self.chain_coverage_tasks) == 16
            and self.chain_coverage_tasks[0] == "MILESTONE_19_TASK_107"
            and self.chain_coverage_tasks[-1] == "MILESTONE_19_TASK_122"
            and FINAL_CHAIN_CLOSURE_MODIFIED is False
            and FINAL_CHAIN_CLOSURE_MODULE_MODIFIED is False
            and CLOSURE_FINALIZATION_MODIFIED is False
            and CLOSURE_FINALIZATION_MODULE_MODIFIED is False
            and CLOSURE_MODIFIED is False
            and CLOSURE_MODULE_MODIFIED is False
            and RESULT_ARCHIVE_MODIFIED is False
            and RESULT_ARCHIVE_MODULE_MODIFIED is False
            and SMOKE_RUN_MODULE_MODIFIED is False
            and USAGE_RUNNER_MODIFIED is False
            and ARTIFACT_EMITTER_MODIFIED is False
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
            and KAGGLE_AUTHENTICATION_PERFORMED is False
            and KAGGLE_SUBMISSION_SENT is False
            and KAGGLE_SUBMISSION_BINDING is False
            and INTERNET_DURING_EVAL is False
            and EXTERNAL_API_DEPENDENCY is False
            and PRIVATE_CORE_EXPOSURE is False
            and RAW_REQUEST_BODY_PERSISTED is False
            and SECRET_PERSISTED is False
            and CREDENTIAL_PERSISTED is False
            and API_KEY_PERSISTED is False
            and LEGAL_CERTIFICATION is False
            and FAIL_CLOSED_ACTIVE is True
            and POC_V0_9_RUNTIME_IMPLEMENTED is False
            and POC_V0_9_BENCHMARKED is False
            and POC_V0_9_FAULT_INJECTION_PERFORMED is False
            and POC_V0_9_PRODUCTION_READY is False
        )

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "taskId": TASK_ID,
            "finalReviewRevision": FINAL_REVIEW_REVISION,
            "sourceFinalChainClosureRevision": FINAL_CHAIN_CLOSURE_REVISION,
            "plan": self.plan.to_public_dict(),
            "sourceFinalChainClosureId": self.source_final_chain_closure_id,
            "sourceFinalChainClosureOk": self.source_final_chain_closure_ok,
            "sourceFinalChainClosureValidationIssues": list(self.source_final_chain_closure_validation_issues),
            "sourceFinalizationId": self.source_finalization_id,
            "sourceClosureId": self.source_closure_id,
            "sourceArchiveId": self.source_archive_id,
            "sourceSuiteResultId": self.source_suite_result_id,
            "sourceArchivedCaseCount": self.source_archived_case_count,
            "sourceArchivedPassedCount": self.source_archived_passed_count,
            "sourceArchivedFailedCount": self.source_archived_failed_count,
            "coveredTaskRange": self.plan.covered_task_range,
            "chainCoverageTasks": list(self.chain_coverage_tasks),
            "chainCoverageTaskCount": len(self.chain_coverage_tasks),
            "reviewedFinalChainClosureArtifactPaths": list(self.reviewed_final_chain_closure_artifact_paths),
            "reviewedFinalChainClosureModulePath": self.reviewed_final_chain_closure_module_path,
            "reviewedFinalChainClosureTestPaths": list(self.reviewed_final_chain_closure_test_paths),
            "acceptedImplementationReviewTaskId": self.accepted_implementation_review_task_id,
            "authorizationTaskId": self.authorization_task_id,
            "finalReviewOk": self.final_review_ok,
            "metadata": dict(self.metadata),
            "controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewImplemented": CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_IMPLEMENTED,
            "diagnosticSmokeRunResultArchiveClosureFinalChainClosureFinalReviewOnly": DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ONLY,
            "controlledSmokeRunResultArchiveClosureFinalChainClosureImplemented": CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTED,
            "diagnosticSmokeRunResultArchiveClosureFinalChainClosureOnly": DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_ONLY,
            "finalChainClosureModified": FINAL_CHAIN_CLOSURE_MODIFIED,
            "finalChainClosureModuleModified": FINAL_CHAIN_CLOSURE_MODULE_MODIFIED,
            "closureFinalizationModified": CLOSURE_FINALIZATION_MODIFIED,
            "closureFinalizationModuleModified": CLOSURE_FINALIZATION_MODULE_MODIFIED,
            "closureModified": CLOSURE_MODIFIED,
            "closureModuleModified": CLOSURE_MODULE_MODIFIED,
            "resultArchiveModified": RESULT_ARCHIVE_MODIFIED,
            "resultArchiveModuleModified": RESULT_ARCHIVE_MODULE_MODIFIED,
            "smokeRunModuleModified": SMOKE_RUN_MODULE_MODIFIED,
            "usageRunnerModified": USAGE_RUNNER_MODIFIED,
            "artifactEmitterModified": ARTIFACT_EMITTER_MODIFIED,
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
            "kaggleAuthenticationPerformed": KAGGLE_AUTHENTICATION_PERFORMED,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT,
            "kaggleSubmissionBinding": KAGGLE_SUBMISSION_BINDING,
            "internetDuringEval": INTERNET_DURING_EVAL,
            "externalApiDependency": EXTERNAL_API_DEPENDENCY,
            "privateCoreExposure": PRIVATE_CORE_EXPOSURE,
            "rawRequestBodyPersisted": RAW_REQUEST_BODY_PERSISTED,
            "secretPersisted": SECRET_PERSISTED,
            "credentialPersisted": CREDENTIAL_PERSISTED,
            "apiKeyPersisted": API_KEY_PERSISTED,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
            "pocV09Status": POC_V0_9_STATUS,
            "pocV09Maturity": POC_V0_9_MATURITY,
            "pocV09RuntimeImplemented": POC_V0_9_RUNTIME_IMPLEMENTED,
            "pocV09Benchmarked": POC_V0_9_BENCHMARKED,
            "pocV09FaultInjectionPerformed": POC_V0_9_FAULT_INJECTION_PERFORMED,
            "pocV09ProductionReady": POC_V0_9_PRODUCTION_READY,
            "technicalContinuityEvidenceOnly": True,
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
        }
        if include_id:
            payload["finalReviewId"] = self.final_review_id
        return payload


def build_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_plan(
    *,
    final_review_scope: str = "local diagnostic final-chain closure final review",
    covered_task_range: str = COVERED_TASK_RANGE,
    source_final_chain_closure_task_id: str = FINAL_CHAIN_CLOSURE_TASK_ID,
    implementation_review_task_id: str = IMPLEMENTATION_REVIEW_TASK_ID,
    planning_task_id: str = PLANNING_TASK_ID,
    authorization_task_id: str = AUTHORIZATION_TASK_ID,
    final_review_purpose: str = "review final-chain closure technical continuity and public-safe boundary",
    poc_v0_9_source_document: str = POC_V0_9_SOURCE_DOCUMENT,
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosureFinalReviewPlan:
    return DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosureFinalReviewPlan(
        final_review_scope=final_review_scope,
        covered_task_range=covered_task_range,
        source_final_chain_closure_task_id=source_final_chain_closure_task_id,
        implementation_review_task_id=implementation_review_task_id,
        planning_task_id=planning_task_id,
        authorization_task_id=authorization_task_id,
        final_review_purpose=final_review_purpose,
        poc_v0_9_source_document=poc_v0_9_source_document,
        metadata={} if metadata is None else metadata,
    )


def review_controlled_smoke_run_result_archive_closure_final_chain_closure(
    final_chain_closure: DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosure,
    *,
    plan: DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosureFinalReviewPlan | None = None,
    reviewed_final_chain_closure_artifact_paths: Sequence[str] = (
        "examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-local-implementation-v1/task-125-smoke-run-result-archive-closure-final-chain-closure.json",
        "examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-local-implementation-v1/task-125-smoke-run-result-archive-closure-final-chain-closure.md",
    ),
    reviewed_final_chain_closure_module_path: str = "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure.py",
    reviewed_final_chain_closure_test_paths: Sequence[str] = (
        "tests/test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure.py",
        "tests/test_milestone_19_task_125_srsc_diagnostic_adapter_controlled_activation_usage_artifact_emission_usage_smoke_run_result_archive_closure_final_chain_closure_local_implementation.py",
        "tests/test_milestone_19_task_126_srsc_diagnostic_adapter_controlled_activation_usage_artifact_emission_usage_smoke_run_result_archive_closure_final_chain_closure_implementation_review.py",
        "tests/test_milestone_19_task_127_srsc_diagnostic_adapter_controlled_activation_usage_artifact_emission_usage_smoke_run_result_archive_closure_final_chain_closure_final_review_planning.py",
        "tests/test_milestone_19_task_128_srsc_diagnostic_adapter_controlled_activation_usage_artifact_emission_usage_smoke_run_result_archive_closure_final_chain_closure_final_review_authorization_review.py",
    ),
    source_final_chain_closure_validation_issues: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosureFinalReview:
    active_plan = plan or build_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_plan()
    issues = tuple(source_final_chain_closure_validation_issues) if source_final_chain_closure_validation_issues is not None else validate_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain_closure)

    return DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosureFinalReview(
        plan=active_plan,
        source_final_chain_closure_id=final_chain_closure.final_chain_closure_id,
        source_final_chain_closure_ok=final_chain_closure.final_chain_closure_ok,
        source_final_chain_closure_validation_issues=issues,
        source_finalization_id=final_chain_closure.source_finalization_id,
        source_closure_id=final_chain_closure.source_closure_id,
        source_archive_id=final_chain_closure.source_archive_id,
        source_suite_result_id=final_chain_closure.source_suite_result_id,
        source_archived_case_count=final_chain_closure.source_archived_case_count,
        source_archived_passed_count=final_chain_closure.source_archived_passed_count,
        source_archived_failed_count=final_chain_closure.source_archived_failed_count,
        chain_coverage_tasks=final_chain_closure.chain_coverage_tasks,
        reviewed_final_chain_closure_artifact_paths=tuple(reviewed_final_chain_closure_artifact_paths),
        reviewed_final_chain_closure_module_path=reviewed_final_chain_closure_module_path,
        reviewed_final_chain_closure_test_paths=tuple(reviewed_final_chain_closure_test_paths),
        metadata={} if metadata is None else metadata,
    )


def validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review(
    final_review: DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosureFinalReview,
) -> tuple[str, ...]:
    issues: list[str] = []

    if not final_review.final_review_ok:
        issues.append("FINAL_REVIEW_NOT_OK")
    if not final_review.source_final_chain_closure_ok:
        issues.append("SOURCE_FINAL_CHAIN_CLOSURE_NOT_OK")
    if final_review.source_final_chain_closure_validation_issues:
        issues.append("SOURCE_FINAL_CHAIN_CLOSURE_VALIDATION_ISSUES_PRESENT")
    if final_review.source_archived_case_count != 8:
        issues.append("SOURCE_ARCHIVED_CASE_COUNT_MISMATCH")
    if final_review.source_archived_passed_count != 8:
        issues.append("SOURCE_ARCHIVED_PASSED_COUNT_MISMATCH")
    if final_review.source_archived_failed_count != 0:
        issues.append("SOURCE_ARCHIVED_FAILED_COUNT_NONZERO")
    if final_review.plan.covered_task_range != COVERED_TASK_RANGE:
        issues.append("COVERED_TASK_RANGE_MISMATCH")
    if len(final_review.chain_coverage_tasks) != 16:
        issues.append("CHAIN_COVERAGE_TASK_COUNT_MISMATCH")
    if final_review.chain_coverage_tasks and final_review.chain_coverage_tasks[0] != "MILESTONE_19_TASK_107":
        issues.append("CHAIN_COVERAGE_START_MISMATCH")
    if final_review.chain_coverage_tasks and final_review.chain_coverage_tasks[-1] != "MILESTONE_19_TASK_122":
        issues.append("CHAIN_COVERAGE_END_MISMATCH")
    if FINAL_CHAIN_CLOSURE_MODIFIED or FINAL_CHAIN_CLOSURE_MODULE_MODIFIED:
        issues.append("FINAL_CHAIN_CLOSURE_MODIFIED")
    if CLOSURE_FINALIZATION_MODIFIED or CLOSURE_FINALIZATION_MODULE_MODIFIED:
        issues.append("CLOSURE_FINALIZATION_MODIFIED")
    if CLOSURE_MODIFIED or CLOSURE_MODULE_MODIFIED:
        issues.append("CLOSURE_MODIFIED")
    if RESULT_ARCHIVE_MODIFIED or RESULT_ARCHIVE_MODULE_MODIFIED:
        issues.append("RESULT_ARCHIVE_MODIFIED")
    if SMOKE_RUN_MODULE_MODIFIED:
        issues.append("SMOKE_RUN_MODULE_MODIFIED")
    if USAGE_RUNNER_MODIFIED:
        issues.append("USAGE_RUNNER_MODIFIED")
    if ARTIFACT_EMITTER_MODIFIED:
        issues.append("ARTIFACT_EMITTER_MODIFIED")
    if RUNTIME_SOLVER_MODIFIED:
        issues.append("RUNTIME_SOLVER_MODIFIED")
    if RUNTIME_WIRING_ALLOWED:
        issues.append("RUNTIME_WIRING_ALLOWED")
    if SOLVER_RUNTIME_BINDING:
        issues.append("SOLVER_RUNTIME_BINDING")
    if BENCHMARK_SCORE_CLAIMED:
        issues.append("BENCHMARK_SCORE_CLAIMED")
    if KAGGLE_SUBMISSION_SENT:
        issues.append("KAGGLE_SUBMISSION_SENT")
    if PRIVATE_CORE_EXPOSURE:
        issues.append("PRIVATE_CORE_EXPOSURE")
    if RAW_REQUEST_BODY_PERSISTED:
        issues.append("RAW_REQUEST_BODY_PERSISTED")
    if SECRET_PERSISTED:
        issues.append("SECRET_PERSISTED")
    if CREDENTIAL_PERSISTED:
        issues.append("CREDENTIAL_PERSISTED")
    if API_KEY_PERSISTED:
        issues.append("API_KEY_PERSISTED")
    if LEGAL_CERTIFICATION:
        issues.append("LEGAL_CERTIFICATION")
    if not FAIL_CLOSED_ACTIVE:
        issues.append("FAIL_CLOSED_INACTIVE")
    if POC_V0_9_RUNTIME_IMPLEMENTED:
        issues.append("POC_V0_9_RUNTIME_IMPLEMENTED")
    if POC_V0_9_BENCHMARKED:
        issues.append("POC_V0_9_BENCHMARKED")
    if POC_V0_9_FAULT_INJECTION_PERFORMED:
        issues.append("POC_V0_9_FAULT_INJECTION_PERFORMED")
    if POC_V0_9_PRODUCTION_READY:
        issues.append("POC_V0_9_PRODUCTION_READY")

    return tuple(issues)


__all__ = [
    "FINAL_REVIEW_REVISION",
    "TASK_ID",
    "CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_IMPLEMENTED",
    "DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ONLY",
    "DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosureFinalReview",
    "DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosureFinalReviewPlan",
    "build_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_plan",
    "review_controlled_smoke_run_result_archive_closure_final_chain_closure",
    "validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review",
]
