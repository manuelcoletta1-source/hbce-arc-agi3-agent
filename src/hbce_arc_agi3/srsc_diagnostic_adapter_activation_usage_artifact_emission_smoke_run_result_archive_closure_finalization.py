"""SRSC controlled smoke-run result archive closure finalization.

Milestone #19 Task 121 - local diagnostic-only finalization implementation.

This module creates public-safe local finalization records for reviewed
smoke-run result archive closure records. It does not modify runtime wiring,
solver behavior, benchmark behavior, Kaggle behavior, private-core behavior,
raw payload behavior, secret handling or legal certification behavior.
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
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure import (
    CLOSURE_REVISION,
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTED,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_ONLY,
    TASK_ID as SOURCE_CLOSURE_TASK_ID,
    DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosure,
    validate_controlled_smoke_run_result_archive_closure,
)


TASK_ID = "MILESTONE_19_TASK_121_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_V1"
AUTHORIZATION_TASK_ID = "MILESTONE_19_TASK_120_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_AUTHORIZATION_REVIEW_V1"
SOURCE_CLOSURE_REVIEW_TASK_ID = "MILESTONE_19_TASK_118_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTATION_REVIEW_V1"
SOURCE_CLOSURE_IMPLEMENTATION_TASK_ID = "MILESTONE_19_TASK_117_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_LOCAL_IMPLEMENTATION_V1"

FINALIZATION_REVISION = "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_V1"

CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED = True
DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_ONLY = True

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
class DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalizationPlan:
    """Plan for finalizing a reviewed local diagnostic smoke-run archive closure."""

    finalization_scope: str = "local diagnostic smoke-run result archive closure finalization"
    source_closure_task_id: str = SOURCE_CLOSURE_TASK_ID
    source_closure_review_task_id: str = SOURCE_CLOSURE_REVIEW_TASK_ID
    source_closure_implementation_task_id: str = SOURCE_CLOSURE_IMPLEMENTATION_TASK_ID
    authorization_task_id: str = AUTHORIZATION_TASK_ID
    finalization_purpose: str = "finalize reviewed local diagnostic smoke-run archive closure chain"
    poc_v0_9_source_document: str = POC_V0_9_SOURCE_DOCUMENT
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "finalization_scope", _clean_text(self.finalization_scope, field_name="finalization_scope"))
        object.__setattr__(self, "source_closure_task_id", _clean_text(self.source_closure_task_id, field_name="source_closure_task_id"))
        object.__setattr__(self, "source_closure_review_task_id", _clean_text(self.source_closure_review_task_id, field_name="source_closure_review_task_id"))
        object.__setattr__(self, "source_closure_implementation_task_id", _clean_text(self.source_closure_implementation_task_id, field_name="source_closure_implementation_task_id"))
        object.__setattr__(self, "authorization_task_id", _clean_text(self.authorization_task_id, field_name="authorization_task_id"))
        object.__setattr__(self, "finalization_purpose", _clean_text(self.finalization_purpose, field_name="finalization_purpose"))
        object.__setattr__(self, "poc_v0_9_source_document", _clean_text(self.poc_v0_9_source_document, field_name="poc_v0_9_source_document"))
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def finalization_plan_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-SMOKE-RUN-ARCHIVE-CLOSURE-FINALIZATION-PLAN", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-FINALIZATION-PLAN-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "finalizationScope": self.finalization_scope,
            "sourceClosureTaskId": self.source_closure_task_id,
            "sourceClosureReviewTaskId": self.source_closure_review_task_id,
            "sourceClosureImplementationTaskId": self.source_closure_implementation_task_id,
            "authorizationTaskId": self.authorization_task_id,
            "finalizationPurpose": self.finalization_purpose,
            "pocV09SourceDocument": self.poc_v0_9_source_document,
            "pocV09Status": POC_V0_9_STATUS,
            "pocV09Maturity": POC_V0_9_MATURITY,
            "pocV09RuntimeImplemented": POC_V0_9_RUNTIME_IMPLEMENTED,
            "pocV09Benchmarked": POC_V0_9_BENCHMARKED,
            "pocV09FaultInjectionPerformed": POC_V0_9_FAULT_INJECTION_PERFORMED,
            "pocV09ProductionReady": POC_V0_9_PRODUCTION_READY,
            "metadata": dict(self.metadata),
            "finalizationRevision": FINALIZATION_REVISION,
            "sourceClosureRevision": CLOSURE_REVISION,
            "technicalContinuityEvidenceOnly": True,
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
            "legalCertification": LEGAL_CERTIFICATION,
            "failClosedActive": FAIL_CLOSED_ACTIVE,
        }
        if include_id:
            payload["finalizationPlanId"] = self.finalization_plan_id
        return payload


@dataclass(frozen=True)
class DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalization:
    """Public-safe local finalization record for one reviewed archive closure."""

    plan: DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalizationPlan
    source_closure_id: str
    source_archive_id: str
    source_suite_result_id: str
    source_closure_ok: bool
    source_closure_validation_issues: tuple[str, ...]
    reviewed_closure_artifact_paths: tuple[str, ...]
    reviewed_closure_module_path: str
    reviewed_closure_test_paths: tuple[str, ...]
    source_archived_case_count: int
    source_archived_passed_count: int
    source_archived_failed_count: int
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_closure_id", _clean_text(self.source_closure_id, field_name="source_closure_id"))
        object.__setattr__(self, "source_archive_id", _clean_text(self.source_archive_id, field_name="source_archive_id"))
        object.__setattr__(self, "source_suite_result_id", _clean_text(self.source_suite_result_id, field_name="source_suite_result_id"))
        object.__setattr__(self, "source_closure_validation_issues", tuple(str(issue) for issue in self.source_closure_validation_issues))
        object.__setattr__(self, "reviewed_closure_artifact_paths", _clean_tuple(self.reviewed_closure_artifact_paths, field_name="reviewed_closure_artifact_paths"))
        object.__setattr__(self, "reviewed_closure_module_path", _clean_text(self.reviewed_closure_module_path, field_name="reviewed_closure_module_path"))
        object.__setattr__(self, "reviewed_closure_test_paths", _clean_tuple(self.reviewed_closure_test_paths, field_name="reviewed_closure_test_paths"))
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def finalization_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-SMOKE-RUN-ARCHIVE-CLOSURE-FINALIZATION", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-FINALIZATION-{digest[:16].upper()}"

    @property
    def finalization_ok(self) -> bool:
        return (
            CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED is True
            and DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_ONLY is True
            and CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTED is True
            and DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_ONLY is True
            and self.source_closure_ok is True
            and len(self.source_closure_validation_issues) == 0
            and self.source_archived_case_count == self.source_archived_passed_count
            and self.source_archived_failed_count == 0
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
            "finalizationRevision": FINALIZATION_REVISION,
            "sourceClosureRevision": CLOSURE_REVISION,
            "plan": self.plan.to_public_dict(),
            "sourceClosureId": self.source_closure_id,
            "sourceArchiveId": self.source_archive_id,
            "sourceSuiteResultId": self.source_suite_result_id,
            "sourceClosureOk": self.source_closure_ok,
            "sourceClosureValidationIssues": list(self.source_closure_validation_issues),
            "reviewedClosureArtifactPaths": list(self.reviewed_closure_artifact_paths),
            "reviewedClosureModulePath": self.reviewed_closure_module_path,
            "reviewedClosureTestPaths": list(self.reviewed_closure_test_paths),
            "sourceArchivedCaseCount": self.source_archived_case_count,
            "sourceArchivedPassedCount": self.source_archived_passed_count,
            "sourceArchivedFailedCount": self.source_archived_failed_count,
            "finalizationOk": self.finalization_ok,
            "metadata": dict(self.metadata),
            "controlledSmokeRunResultArchiveClosureFinalizationImplemented": CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED,
            "diagnosticSmokeRunResultArchiveClosureFinalizationOnly": DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_ONLY,
            "controlledSmokeRunResultArchiveClosureImplemented": CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTED,
            "diagnosticSmokeRunResultArchiveClosureOnly": DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_ONLY,
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
            payload["finalizationId"] = self.finalization_id
        return payload


def build_controlled_smoke_run_result_archive_closure_finalization_plan(
    *,
    finalization_scope: str = "local diagnostic smoke-run result archive closure finalization",
    source_closure_task_id: str = SOURCE_CLOSURE_TASK_ID,
    source_closure_review_task_id: str = SOURCE_CLOSURE_REVIEW_TASK_ID,
    source_closure_implementation_task_id: str = SOURCE_CLOSURE_IMPLEMENTATION_TASK_ID,
    authorization_task_id: str = AUTHORIZATION_TASK_ID,
    finalization_purpose: str = "finalize reviewed local diagnostic smoke-run archive closure chain",
    poc_v0_9_source_document: str = POC_V0_9_SOURCE_DOCUMENT,
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalizationPlan:
    return DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalizationPlan(
        finalization_scope=finalization_scope,
        source_closure_task_id=source_closure_task_id,
        source_closure_review_task_id=source_closure_review_task_id,
        source_closure_implementation_task_id=source_closure_implementation_task_id,
        authorization_task_id=authorization_task_id,
        finalization_purpose=finalization_purpose,
        poc_v0_9_source_document=poc_v0_9_source_document,
        metadata={} if metadata is None else metadata,
    )


def finalize_controlled_smoke_run_result_archive_closure(
    closure: DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosure,
    *,
    plan: DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalizationPlan | None = None,
    reviewed_closure_artifact_paths: Sequence[str] = (
        "examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-local-implementation-v1/task-117-smoke-run-result-archive-closure.json",
        "examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-local-implementation-v1/task-117-smoke-run-result-archive-closure.md",
    ),
    reviewed_closure_module_path: str = "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure.py",
    reviewed_closure_test_paths: Sequence[str] = (
        "tests/test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure.py",
        "tests/test_milestone_19_task_117_srsc_diagnostic_adapter_controlled_activation_usage_artifact_emission_usage_smoke_run_result_archive_closure_local_implementation.py",
        "tests/test_milestone_19_task_118_srsc_diagnostic_adapter_controlled_activation_usage_artifact_emission_usage_smoke_run_result_archive_closure_implementation_review.py",
    ),
    source_closure_validation_issues: Sequence[str] | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalization:
    active_plan = plan or build_controlled_smoke_run_result_archive_closure_finalization_plan()
    issues = tuple(source_closure_validation_issues) if source_closure_validation_issues is not None else validate_controlled_smoke_run_result_archive_closure(closure)
    return DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalization(
        plan=active_plan,
        source_closure_id=closure.closure_id,
        source_archive_id=closure.source_archive_id,
        source_suite_result_id=closure.source_suite_result_id,
        source_closure_ok=closure.closure_ok,
        source_closure_validation_issues=issues,
        reviewed_closure_artifact_paths=tuple(reviewed_closure_artifact_paths),
        reviewed_closure_module_path=reviewed_closure_module_path,
        reviewed_closure_test_paths=tuple(reviewed_closure_test_paths),
        source_archived_case_count=closure.source_archived_case_count,
        source_archived_passed_count=closure.source_archived_passed_count,
        source_archived_failed_count=closure.source_archived_failed_count,
        metadata={} if metadata is None else metadata,
    )


def validate_controlled_smoke_run_result_archive_closure_finalization(
    finalization: DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalization,
) -> tuple[str, ...]:
    issues: list[str] = []

    if not finalization.finalization_ok:
        issues.append("FINALIZATION_NOT_OK")
    if not finalization.source_closure_ok:
        issues.append("SOURCE_CLOSURE_NOT_OK")
    if finalization.source_closure_validation_issues:
        issues.append("SOURCE_CLOSURE_VALIDATION_ISSUES_PRESENT")
    if finalization.source_archived_case_count != finalization.source_archived_passed_count:
        issues.append("SOURCE_ARCHIVED_CASE_COUNT_NOT_FULL_PASS")
    if finalization.source_archived_failed_count != 0:
        issues.append("SOURCE_ARCHIVED_FAILED_COUNT_NONZERO")
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
    "FINALIZATION_REVISION",
    "TASK_ID",
    "CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED",
    "DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_ONLY",
    "DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalization",
    "DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosureFinalizationPlan",
    "build_controlled_smoke_run_result_archive_closure_finalization_plan",
    "finalize_controlled_smoke_run_result_archive_closure",
    "validate_controlled_smoke_run_result_archive_closure_finalization",
]
