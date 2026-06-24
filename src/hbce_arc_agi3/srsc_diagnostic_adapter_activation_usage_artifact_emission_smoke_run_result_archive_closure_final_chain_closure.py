"""SRSC controlled smoke-run result archive closure final-chain closure.

Milestone #19 Task 125 - local diagnostic-only final chain closure implementation.

This module creates public-safe local final-chain closure records for the
reviewed SRSC diagnostic artifact emission usage smoke-run result archive
closure chain. It does not modify runtime wiring, solver behavior, benchmark
behavior, Kaggle behavior, private-core behavior, raw payload behavior, secret
handling or legal certification behavior. Astonishingly, software can avoid
inventing a leaderboard when politely told not to.
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
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_finalization import (
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_ONLY,
    FINALIZATION_REVISION,
    TASK_ID as SOURCE_FINALIZATION_TASK_ID,
    DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalization,
    validate_controlled_smoke_run_result_archive_closure_finalization,
)


TASK_ID = "MILESTONE_19_TASK_125_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_IMPLEMENTATION_V1"
AUTHORIZATION_TASK_ID = "MILESTONE_19_TASK_124_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_AUTHORIZATION_REVIEW_V1"
PLANNING_TASK_ID = "MILESTONE_19_TASK_123_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_PLANNING_V1"
FINALIZATION_REVIEW_TASK_ID = "MILESTONE_19_TASK_122_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTATION_REVIEW_V1"
COVERED_TASK_RANGE = "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"

FINAL_CHAIN_CLOSURE_REVISION = "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_V1"

CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTED = True
DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_ONLY = True

CLOSURE_FINALIZATION_MODIFIED = False
CLOSURE_FINALIZATION_MODULE_MODIFIED = False
CLOSURE_MODIFIED = False
CLOSURE_MODULE_MODIFIED = False
RESULT_ARCHIVE_MODIFIED = False
RESULT_ARCHIVE_MODULE_MODIFIED = False
SMOKE_RUN_MODULE_MODIFIED = False
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
class DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosurePlan:
    """Plan for locally closing the reviewed archive / closure / finalization chain."""

    final_chain_closure_scope: str = "local diagnostic smoke-run result archive closure final chain closure"
    covered_task_range: str = COVERED_TASK_RANGE
    source_finalization_task_id: str = SOURCE_FINALIZATION_TASK_ID
    finalization_review_task_id: str = FINALIZATION_REVIEW_TASK_ID
    planning_task_id: str = PLANNING_TASK_ID
    authorization_task_id: str = AUTHORIZATION_TASK_ID
    final_chain_closure_purpose: str = "close reviewed local diagnostic archive closure finalization chain"
    poc_v0_9_source_document: str = POC_V0_9_SOURCE_DOCUMENT
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "final_chain_closure_scope", _clean_text(self.final_chain_closure_scope, field_name="final_chain_closure_scope"))
        object.__setattr__(self, "covered_task_range", _clean_text(self.covered_task_range, field_name="covered_task_range"))
        object.__setattr__(self, "source_finalization_task_id", _clean_text(self.source_finalization_task_id, field_name="source_finalization_task_id"))
        object.__setattr__(self, "finalization_review_task_id", _clean_text(self.finalization_review_task_id, field_name="finalization_review_task_id"))
        object.__setattr__(self, "planning_task_id", _clean_text(self.planning_task_id, field_name="planning_task_id"))
        object.__setattr__(self, "authorization_task_id", _clean_text(self.authorization_task_id, field_name="authorization_task_id"))
        object.__setattr__(self, "final_chain_closure_purpose", _clean_text(self.final_chain_closure_purpose, field_name="final_chain_closure_purpose"))
        object.__setattr__(self, "poc_v0_9_source_document", _clean_text(self.poc_v0_9_source_document, field_name="poc_v0_9_source_document"))
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def final_chain_closure_plan_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-SMOKE-RUN-ARCHIVE-CLOSURE-FINAL-CHAIN-CLOSURE-PLAN", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-FINAL-CHAIN-CLOSURE-PLAN-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "finalChainClosureScope": self.final_chain_closure_scope,
            "coveredTaskRange": self.covered_task_range,
            "sourceFinalizationTaskId": self.source_finalization_task_id,
            "finalizationReviewTaskId": self.finalization_review_task_id,
            "planningTaskId": self.planning_task_id,
            "authorizationTaskId": self.authorization_task_id,
            "finalChainClosurePurpose": self.final_chain_closure_purpose,
            "pocV09SourceDocument": self.poc_v0_9_source_document,
            "pocV09Status": POC_V0_9_STATUS,
            "pocV09Maturity": POC_V0_9_MATURITY,
            "pocV09RuntimeImplemented": POC_V0_9_RUNTIME_IMPLEMENTED,
            "pocV09Benchmarked": POC_V0_9_BENCHMARKED,
            "pocV09FaultInjectionPerformed": POC_V0_9_FAULT_INJECTION_PERFORMED,
            "pocV09ProductionReady": POC_V0_9_PRODUCTION_READY,
            "metadata": dict(self.metadata),
            "finalChainClosureRevision": FINAL_CHAIN_CLOSURE_REVISION,
            "sourceFinalizationRevision": FINALIZATION_REVISION,
            "technicalContinuityEvidenceOnly": True,
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
        }
        if include_id:
            payload["finalChainClosurePlanId"] = self.final_chain_closure_plan_id
        return payload


@dataclass(frozen=True)
class DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosure:
    """Public-safe local final-chain closure record for the reviewed SRSC chain."""

    plan: DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosurePlan
    source_finalization_id: str
    source_closure_id: str
    source_archive_id: str
    source_suite_result_id: str
    source_finalization_ok: bool
    source_finalization_validation_issues: tuple[str, ...]
    reviewed_finalization_artifact_paths: tuple[str, ...]
    reviewed_finalization_module_path: str
    reviewed_finalization_test_paths: tuple[str, ...]
    source_archived_case_count: int
    source_archived_passed_count: int
    source_archived_failed_count: int
    chain_coverage_tasks: tuple[str, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_finalization_id", _clean_text(self.source_finalization_id, field_name="source_finalization_id"))
        object.__setattr__(self, "source_closure_id", _clean_text(self.source_closure_id, field_name="source_closure_id"))
        object.__setattr__(self, "source_archive_id", _clean_text(self.source_archive_id, field_name="source_archive_id"))
        object.__setattr__(self, "source_suite_result_id", _clean_text(self.source_suite_result_id, field_name="source_suite_result_id"))
        object.__setattr__(self, "source_finalization_validation_issues", tuple(str(issue) for issue in self.source_finalization_validation_issues))
        object.__setattr__(self, "reviewed_finalization_artifact_paths", _clean_tuple(self.reviewed_finalization_artifact_paths, field_name="reviewed_finalization_artifact_paths"))
        object.__setattr__(self, "reviewed_finalization_module_path", _clean_text(self.reviewed_finalization_module_path, field_name="reviewed_finalization_module_path"))
        object.__setattr__(self, "reviewed_finalization_test_paths", _clean_tuple(self.reviewed_finalization_test_paths, field_name="reviewed_finalization_test_paths"))
        object.__setattr__(self, "chain_coverage_tasks", _clean_tuple(self.chain_coverage_tasks, field_name="chain_coverage_tasks"))
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def final_chain_closure_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-SMOKE-RUN-ARCHIVE-CLOSURE-FINAL-CHAIN-CLOSURE", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-FINAL-CHAIN-CLOSURE-{digest[:16].upper()}"

    @property
    def final_chain_closure_ok(self) -> bool:
        return (
            CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTED is True
            and DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_ONLY is True
            and CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED is True
            and DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_ONLY is True
            and self.source_finalization_ok is True
            and len(self.source_finalization_validation_issues) == 0
            and self.source_archived_case_count == self.source_archived_passed_count
            and self.source_archived_failed_count == 0
            and self.plan.covered_task_range == COVERED_TASK_RANGE
            and len(self.chain_coverage_tasks) == 16
            and self.chain_coverage_tasks[0] == "MILESTONE_19_TASK_107"
            and self.chain_coverage_tasks[-1] == "MILESTONE_19_TASK_122"
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
            and REAL_SUBMISSION_AUTHORIZED is False
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
            "finalChainClosureRevision": FINAL_CHAIN_CLOSURE_REVISION,
            "sourceFinalizationRevision": FINALIZATION_REVISION,
            "plan": self.plan.to_public_dict(),
            "sourceFinalizationId": self.source_finalization_id,
            "sourceClosureId": self.source_closure_id,
            "sourceArchiveId": self.source_archive_id,
            "sourceSuiteResultId": self.source_suite_result_id,
            "sourceFinalizationOk": self.source_finalization_ok,
            "sourceFinalizationValidationIssues": list(self.source_finalization_validation_issues),
            "reviewedFinalizationArtifactPaths": list(self.reviewed_finalization_artifact_paths),
            "reviewedFinalizationModulePath": self.reviewed_finalization_module_path,
            "reviewedFinalizationTestPaths": list(self.reviewed_finalization_test_paths),
            "sourceArchivedCaseCount": self.source_archived_case_count,
            "sourceArchivedPassedCount": self.source_archived_passed_count,
            "sourceArchivedFailedCount": self.source_archived_failed_count,
            "coveredTaskRange": self.plan.covered_task_range,
            "chainCoverageTasks": list(self.chain_coverage_tasks),
            "chainCoverageTaskCount": len(self.chain_coverage_tasks),
            "finalChainClosureOk": self.final_chain_closure_ok,
            "metadata": dict(self.metadata),
            "controlledSmokeRunResultArchiveClosureFinalChainClosureImplemented": CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTED,
            "diagnosticSmokeRunResultArchiveClosureFinalChainClosureOnly": DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_ONLY,
            "controlledSmokeRunResultArchiveClosureFinalizationImplemented": CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED,
            "diagnosticSmokeRunResultArchiveClosureFinalizationOnly": DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_ONLY,
            "closureFinalizationModified": CLOSURE_FINALIZATION_MODIFIED,
            "closureFinalizationModuleModified": CLOSURE_FINALIZATION_MODULE_MODIFIED,
            "closureModified": CLOSURE_MODIFIED,
            "closureModuleModified": CLOSURE_MODULE_MODIFIED,
            "resultArchiveModified": RESULT_ARCHIVE_MODIFIED,
            "resultArchiveModuleModified": RESULT_ARCHIVE_MODULE_MODIFIED,
            "smokeRunModuleModified": SMOKE_RUN_MODULE_MODIFIED,
            "usageRunnerModified": USAGE_RUNNER_MODIFIED,
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
            payload["finalChainClosureId"] = self.final_chain_closure_id
        return payload


def build_controlled_smoke_run_result_archive_closure_final_chain_closure_plan(
    *,
    final_chain_closure_scope: str = "local diagnostic smoke-run result archive closure final chain closure",
    covered_task_range: str = COVERED_TASK_RANGE,
    source_finalization_task_id: str = SOURCE_FINALIZATION_TASK_ID,
    finalization_review_task_id: str = FINALIZATION_REVIEW_TASK_ID,
    planning_task_id: str = PLANNING_TASK_ID,
    authorization_task_id: str = AUTHORIZATION_TASK_ID,
    final_chain_closure_purpose: str = "close reviewed local diagnostic archive closure finalization chain",
    poc_v0_9_source_document: str = POC_V0_9_SOURCE_DOCUMENT,
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosurePlan:
    return DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosurePlan(
        final_chain_closure_scope=final_chain_closure_scope,
        covered_task_range=covered_task_range,
        source_finalization_task_id=source_finalization_task_id,
        finalization_review_task_id=finalization_review_task_id,
        planning_task_id=planning_task_id,
        authorization_task_id=authorization_task_id,
        final_chain_closure_purpose=final_chain_closure_purpose,
        poc_v0_9_source_document=poc_v0_9_source_document,
        metadata={} if metadata is None else metadata,
    )


def default_chain_coverage_tasks() -> tuple[str, ...]:
    return tuple(f"MILESTONE_19_TASK_{number}" for number in range(107, 123))


def close_controlled_smoke_run_result_archive_closure_final_chain(
    finalization: DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalization,
    *,
    plan: DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosurePlan | None = None,
    reviewed_finalization_artifact_paths: Sequence[str] = (
        "examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-local-implementation-v1/task-121-smoke-run-result-archive-closure-finalization.json",
        "examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-local-implementation-v1/task-121-smoke-run-result-archive-closure-finalization.md",
    ),
    reviewed_finalization_module_path: str = "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_finalization.py",
    reviewed_finalization_test_paths: Sequence[str] = (
        "tests/test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_finalization.py",
        "tests/test_milestone_19_task_121_srsc_diagnostic_adapter_controlled_activation_usage_artifact_emission_usage_smoke_run_result_archive_closure_finalization_local_implementation.py",
        "tests/test_milestone_19_task_122_srsc_diagnostic_adapter_controlled_activation_usage_artifact_emission_usage_smoke_run_result_archive_closure_finalization_implementation_review.py",
        "tests/test_milestone_19_task_123_srsc_diagnostic_adapter_controlled_activation_usage_artifact_emission_usage_smoke_run_result_archive_closure_final_chain_closure_planning.py",
        "tests/test_milestone_19_task_124_srsc_diagnostic_adapter_controlled_activation_usage_artifact_emission_usage_smoke_run_result_archive_closure_final_chain_closure_authorization_review.py",
    ),
    source_finalization_validation_issues: Sequence[str] | None = None,
    chain_coverage_tasks: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosure:
    active_plan = plan or build_controlled_smoke_run_result_archive_closure_final_chain_closure_plan()
    issues = tuple(source_finalization_validation_issues) if source_finalization_validation_issues is not None else validate_controlled_smoke_run_result_archive_closure_finalization(finalization)
    active_chain_coverage_tasks = tuple(chain_coverage_tasks) if chain_coverage_tasks is not None else default_chain_coverage_tasks()

    return DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosure(
        plan=active_plan,
        source_finalization_id=finalization.finalization_id,
        source_closure_id=finalization.source_closure_id,
        source_archive_id=finalization.source_archive_id,
        source_suite_result_id=finalization.source_suite_result_id,
        source_finalization_ok=finalization.finalization_ok,
        source_finalization_validation_issues=issues,
        reviewed_finalization_artifact_paths=tuple(reviewed_finalization_artifact_paths),
        reviewed_finalization_module_path=reviewed_finalization_module_path,
        reviewed_finalization_test_paths=tuple(reviewed_finalization_test_paths),
        source_archived_case_count=finalization.source_archived_case_count,
        source_archived_passed_count=finalization.source_archived_passed_count,
        source_archived_failed_count=finalization.source_archived_failed_count,
        chain_coverage_tasks=active_chain_coverage_tasks,
        metadata={} if metadata is None else metadata,
    )


def validate_controlled_smoke_run_result_archive_closure_final_chain_closure(
    final_chain_closure: DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosure,
) -> tuple[str, ...]:
    issues: list[str] = []

    if not final_chain_closure.final_chain_closure_ok:
        issues.append("FINAL_CHAIN_CLOSURE_NOT_OK")
    if not final_chain_closure.source_finalization_ok:
        issues.append("SOURCE_FINALIZATION_NOT_OK")
    if final_chain_closure.source_finalization_validation_issues:
        issues.append("SOURCE_FINALIZATION_VALIDATION_ISSUES_PRESENT")
    if final_chain_closure.source_archived_case_count != final_chain_closure.source_archived_passed_count:
        issues.append("SOURCE_ARCHIVED_CASE_COUNT_NOT_FULL_PASS")
    if final_chain_closure.source_archived_failed_count != 0:
        issues.append("SOURCE_ARCHIVED_FAILED_COUNT_NONZERO")
    if final_chain_closure.plan.covered_task_range != COVERED_TASK_RANGE:
        issues.append("COVERED_TASK_RANGE_MISMATCH")
    if len(final_chain_closure.chain_coverage_tasks) != 16:
        issues.append("CHAIN_COVERAGE_TASK_COUNT_MISMATCH")
    if final_chain_closure.chain_coverage_tasks and final_chain_closure.chain_coverage_tasks[0] != "MILESTONE_19_TASK_107":
        issues.append("CHAIN_COVERAGE_START_MISMATCH")
    if final_chain_closure.chain_coverage_tasks and final_chain_closure.chain_coverage_tasks[-1] != "MILESTONE_19_TASK_122":
        issues.append("CHAIN_COVERAGE_END_MISMATCH")
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
    "COVERED_TASK_RANGE",
    "FINAL_CHAIN_CLOSURE_REVISION",
    "TASK_ID",
    "CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTED",
    "DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_ONLY",
    "DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosure",
    "DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalChainClosurePlan",
    "build_controlled_smoke_run_result_archive_closure_final_chain_closure_plan",
    "close_controlled_smoke_run_result_archive_closure_final_chain",
    "default_chain_coverage_tasks",
    "validate_controlled_smoke_run_result_archive_closure_final_chain_closure",
]
