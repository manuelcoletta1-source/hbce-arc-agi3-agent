"""SRSC controlled smoke-run result archive closure.

Milestone #19 Task 117 - local diagnostic-only archive closure implementation.

This module creates public-safe local closure records for reviewed smoke-run
result archives. It does not modify the archive module, smoke-run module,
usage runner, artifact emitter, activation layers, adapter, solver runtime,
candidate generator, ranker, verifier, benchmark layer, Kaggle behavior,
private core behavior, raw payload behavior, secret handling or legal
certification behavior.
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
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive import (
    FAIL_CLOSED_ACTIVE,
    LEGAL_CERTIFICATION,
    PRIVATE_CORE_EXPOSURE,
    RAW_REQUEST_BODY_PERSISTED,
    SECRET_PERSISTED,
    CREDENTIAL_PERSISTED,
    API_KEY_PERSISTED,
    INTERNET_DURING_EVAL,
    EXTERNAL_API_DEPENDENCY,
    KAGGLE_AUTHENTICATION_PERFORMED,
    KAGGLE_SUBMISSION_BINDING,
    REAL_EVALUATION_PERFORMED,
    REAL_SUBMISSION_AUTHORIZED,
    BENCHMARK_BINDING,
    CANDIDATE_GENERATOR_BINDING,
    CANDIDATE_GENERATOR_MODIFIED,
    RANKER_BINDING,
    RANKER_MODIFIED,
    VERIFIER_BINDING,
    VERIFIER_MODIFIED,
    RESULT_ARCHIVE_REVISION,
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTED,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_ONLY,
    SMOKE_RUN_MODULE_MODIFIED,
    USAGE_RUNNER_MODIFIED,
    ARTIFACT_EMITTER_MODIFIED,
    USAGE_LAYER_MODIFIED,
    ACTIVATION_WRAPPER_MODIFIED,
    ADAPTER_MODIFIED,
    RUNTIME_SOLVER_MODIFIED_IN_ARCHIVE,
    RUNTIME_WIRING_ALLOWED_IN_ARCHIVE,
    SOLVER_RUNTIME_BINDING_IN_ARCHIVE,
    BENCHMARK_SCORE_CLAIMED,
    KAGGLE_SUBMISSION_SENT,
    DiagnosticArtifactEmissionUsageSmokeRunResultArchive,
)


TASK_ID = "MILESTONE_19_TASK_117_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_LOCAL_IMPLEMENTATION_V1"
AUTHORIZATION_TASK_ID = "MILESTONE_19_TASK_116_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_AUTHORIZATION_REVIEW_V1"
SOURCE_ARCHIVE_TASK_ID = "MILESTONE_19_TASK_113_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_IMPLEMENTATION_V1"
SOURCE_ARCHIVE_REVIEW_TASK_ID = "MILESTONE_19_TASK_114_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTATION_REVIEW_V1"
CLOSURE_REVISION = "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_LOCAL_V1"

CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTED = True
DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_ONLY = True

RESULT_ARCHIVE_MODIFIED = False
RESULT_ARCHIVE_MODULE_MODIFIED = False
SMOKE_RUN_MODULE_MODIFIED_IN_CLOSURE = False
USAGE_RUNNER_MODIFIED_IN_CLOSURE = False
ARTIFACT_EMITTER_MODIFIED_IN_CLOSURE = False
USAGE_LAYER_MODIFIED_IN_CLOSURE = False
ACTIVATION_WRAPPER_MODIFIED_IN_CLOSURE = False
ADAPTER_MODIFIED_IN_CLOSURE = False

RUNTIME_ACTIVATION_AUTHORIZED = False
RUNTIME_SOLVER_MODIFIED_IN_CLOSURE = False
RUNTIME_WIRING_ALLOWED_IN_CLOSURE = False
SOLVER_RUNTIME_BINDING_IN_CLOSURE = False

CANDIDATE_GENERATOR_MODIFIED_IN_CLOSURE = False
CANDIDATE_GENERATOR_BINDING_IN_CLOSURE = False
RANKER_MODIFIED_IN_CLOSURE = False
RANKER_BINDING_IN_CLOSURE = False
VERIFIER_MODIFIED_IN_CLOSURE = False
VERIFIER_BINDING_IN_CLOSURE = False

BENCHMARK_SCORE_CLAIMED_IN_CLOSURE = False
BENCHMARK_BINDING_IN_CLOSURE = False
REAL_EVALUATION_PERFORMED_IN_CLOSURE = False
REAL_SUBMISSION_AUTHORIZED_IN_CLOSURE = False

KAGGLE_AUTHENTICATION_PERFORMED_IN_CLOSURE = False
KAGGLE_SUBMISSION_SENT_IN_CLOSURE = False
KAGGLE_SUBMISSION_BINDING_IN_CLOSURE = False

INTERNET_DURING_EVAL_IN_CLOSURE = False
EXTERNAL_API_DEPENDENCY_IN_CLOSURE = False
PRIVATE_CORE_EXPOSURE_IN_CLOSURE = False

RAW_REQUEST_BODY_PERSISTED_IN_CLOSURE = False
SECRET_PERSISTED_IN_CLOSURE = False
CREDENTIAL_PERSISTED_IN_CLOSURE = False
API_KEY_PERSISTED_IN_CLOSURE = False

LEGAL_CERTIFICATION_IN_CLOSURE = False
FAIL_CLOSED_ACTIVE_IN_CLOSURE = True


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
class DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosurePlan:
    """Plan for closing a reviewed local diagnostic smoke-run archive."""

    closure_scope: str = "local diagnostic smoke-run result archive closure"
    source_archive_task_id: str = SOURCE_ARCHIVE_TASK_ID
    source_archive_review_task_id: str = SOURCE_ARCHIVE_REVIEW_TASK_ID
    authorization_task_id: str = AUTHORIZATION_TASK_ID
    closure_purpose: str = "close reviewed local diagnostic smoke-run archive chain"
    poc_v0_9_source_document: str = POC_V0_9_SOURCE_DOCUMENT
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "closure_scope", _clean_text(self.closure_scope, field_name="closure_scope"))
        object.__setattr__(self, "source_archive_task_id", _clean_text(self.source_archive_task_id, field_name="source_archive_task_id"))
        object.__setattr__(self, "source_archive_review_task_id", _clean_text(self.source_archive_review_task_id, field_name="source_archive_review_task_id"))
        object.__setattr__(self, "authorization_task_id", _clean_text(self.authorization_task_id, field_name="authorization_task_id"))
        object.__setattr__(self, "closure_purpose", _clean_text(self.closure_purpose, field_name="closure_purpose"))
        object.__setattr__(self, "poc_v0_9_source_document", _clean_text(self.poc_v0_9_source_document, field_name="poc_v0_9_source_document"))
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def closure_plan_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-SMOKE-RUN-ARCHIVE-CLOSURE-PLAN", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-PLAN-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "closureScope": self.closure_scope,
            "sourceArchiveTaskId": self.source_archive_task_id,
            "sourceArchiveReviewTaskId": self.source_archive_review_task_id,
            "authorizationTaskId": self.authorization_task_id,
            "closurePurpose": self.closure_purpose,
            "pocV09SourceDocument": self.poc_v0_9_source_document,
            "pocV09Status": POC_V0_9_STATUS,
            "pocV09Maturity": POC_V0_9_MATURITY,
            "pocV09RuntimeImplemented": POC_V0_9_RUNTIME_IMPLEMENTED,
            "pocV09Benchmarked": POC_V0_9_BENCHMARKED,
            "pocV09FaultInjectionPerformed": POC_V0_9_FAULT_INJECTION_PERFORMED,
            "pocV09ProductionReady": POC_V0_9_PRODUCTION_READY,
            "metadata": dict(self.metadata),
            "closureRevision": CLOSURE_REVISION,
            "resultArchiveRevision": RESULT_ARCHIVE_REVISION,
            "technicalContinuityEvidenceOnly": True,
            "noScoreClaimMarker": True,
            "noSubmissionMarker": True,
            "legalCertification": LEGAL_CERTIFICATION_IN_CLOSURE,
            "failClosedActive": FAIL_CLOSED_ACTIVE_IN_CLOSURE,
        }
        if include_id:
            payload["closurePlanId"] = self.closure_plan_id
        return payload


@dataclass(frozen=True)
class DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosure:
    """Public-safe local closure record for one reviewed archive."""

    plan: DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosurePlan
    source_archive_id: str
    source_suite_result_id: str
    source_archive_ok: bool
    source_validation_issues: tuple[str, ...]
    reviewed_artifact_paths: tuple[str, ...]
    reviewed_module_path: str
    reviewed_test_paths: tuple[str, ...]
    source_archived_case_count: int
    source_archived_passed_count: int
    source_archived_failed_count: int
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_archive_id", _clean_text(self.source_archive_id, field_name="source_archive_id"))
        object.__setattr__(self, "source_suite_result_id", _clean_text(self.source_suite_result_id, field_name="source_suite_result_id"))
        object.__setattr__(self, "source_validation_issues", tuple(str(issue) for issue in self.source_validation_issues))
        object.__setattr__(self, "reviewed_artifact_paths", _clean_tuple(self.reviewed_artifact_paths, field_name="reviewed_artifact_paths"))
        object.__setattr__(self, "reviewed_module_path", _clean_text(self.reviewed_module_path, field_name="reviewed_module_path"))
        object.__setattr__(self, "reviewed_test_paths", _clean_tuple(self.reviewed_test_paths, field_name="reviewed_test_paths"))
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def closure_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-SMOKE-RUN-ARCHIVE-CLOSURE", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-{digest[:16].upper()}"

    @property
    def closure_ok(self) -> bool:
        return (
            CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTED is True
            and DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_ONLY is True
            and self.source_archive_ok is True
            and len(self.source_validation_issues) == 0
            and self.source_archived_case_count == self.source_archived_passed_count
            and self.source_archived_failed_count == 0
            and CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTED is True
            and DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_ONLY is True
            and RESULT_ARCHIVE_MODIFIED is False
            and RESULT_ARCHIVE_MODULE_MODIFIED is False
            and SMOKE_RUN_MODULE_MODIFIED is False
            and SMOKE_RUN_MODULE_MODIFIED_IN_CLOSURE is False
            and USAGE_RUNNER_MODIFIED is False
            and USAGE_RUNNER_MODIFIED_IN_CLOSURE is False
            and ARTIFACT_EMITTER_MODIFIED is False
            and ARTIFACT_EMITTER_MODIFIED_IN_CLOSURE is False
            and RUNTIME_SOLVER_MODIFIED_IN_ARCHIVE is False
            and RUNTIME_SOLVER_MODIFIED_IN_CLOSURE is False
            and RUNTIME_WIRING_ALLOWED_IN_ARCHIVE is False
            and RUNTIME_WIRING_ALLOWED_IN_CLOSURE is False
            and SOLVER_RUNTIME_BINDING_IN_ARCHIVE is False
            and SOLVER_RUNTIME_BINDING_IN_CLOSURE is False
            and BENCHMARK_SCORE_CLAIMED is False
            and BENCHMARK_SCORE_CLAIMED_IN_CLOSURE is False
            and KAGGLE_SUBMISSION_SENT is False
            and KAGGLE_SUBMISSION_SENT_IN_CLOSURE is False
            and PRIVATE_CORE_EXPOSURE is False
            and PRIVATE_CORE_EXPOSURE_IN_CLOSURE is False
            and RAW_REQUEST_BODY_PERSISTED is False
            and RAW_REQUEST_BODY_PERSISTED_IN_CLOSURE is False
            and SECRET_PERSISTED is False
            and SECRET_PERSISTED_IN_CLOSURE is False
            and CREDENTIAL_PERSISTED is False
            and CREDENTIAL_PERSISTED_IN_CLOSURE is False
            and API_KEY_PERSISTED is False
            and API_KEY_PERSISTED_IN_CLOSURE is False
            and LEGAL_CERTIFICATION is False
            and LEGAL_CERTIFICATION_IN_CLOSURE is False
            and FAIL_CLOSED_ACTIVE is True
            and FAIL_CLOSED_ACTIVE_IN_CLOSURE is True
            and POC_V0_9_RUNTIME_IMPLEMENTED is False
            and POC_V0_9_BENCHMARKED is False
            and POC_V0_9_FAULT_INJECTION_PERFORMED is False
            and POC_V0_9_PRODUCTION_READY is False
        )

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "taskId": TASK_ID,
            "closureRevision": CLOSURE_REVISION,
            "plan": self.plan.to_public_dict(),
            "sourceArchiveId": self.source_archive_id,
            "sourceSuiteResultId": self.source_suite_result_id,
            "sourceArchiveOk": self.source_archive_ok,
            "sourceValidationIssues": list(self.source_validation_issues),
            "reviewedArtifactPaths": list(self.reviewed_artifact_paths),
            "reviewedModulePath": self.reviewed_module_path,
            "reviewedTestPaths": list(self.reviewed_test_paths),
            "sourceArchivedCaseCount": self.source_archived_case_count,
            "sourceArchivedPassedCount": self.source_archived_passed_count,
            "sourceArchivedFailedCount": self.source_archived_failed_count,
            "closureOk": self.closure_ok,
            "metadata": dict(self.metadata),
            "controlledSmokeRunResultArchiveClosureImplemented": CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTED,
            "diagnosticSmokeRunResultArchiveClosureOnly": DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_ONLY,
            "resultArchiveModified": RESULT_ARCHIVE_MODIFIED,
            "resultArchiveModuleModified": RESULT_ARCHIVE_MODULE_MODIFIED,
            "smokeRunModuleModified": SMOKE_RUN_MODULE_MODIFIED or SMOKE_RUN_MODULE_MODIFIED_IN_CLOSURE,
            "usageRunnerModified": USAGE_RUNNER_MODIFIED or USAGE_RUNNER_MODIFIED_IN_CLOSURE,
            "artifactEmitterModified": ARTIFACT_EMITTER_MODIFIED or ARTIFACT_EMITTER_MODIFIED_IN_CLOSURE,
            "usageLayerModified": USAGE_LAYER_MODIFIED or USAGE_LAYER_MODIFIED_IN_CLOSURE,
            "activationWrapperModified": ACTIVATION_WRAPPER_MODIFIED or ACTIVATION_WRAPPER_MODIFIED_IN_CLOSURE,
            "adapterModified": ADAPTER_MODIFIED or ADAPTER_MODIFIED_IN_CLOSURE,
            "runtimeActivationAuthorized": RUNTIME_ACTIVATION_AUTHORIZED,
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED_IN_ARCHIVE or RUNTIME_SOLVER_MODIFIED_IN_CLOSURE,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED_IN_ARCHIVE or RUNTIME_WIRING_ALLOWED_IN_CLOSURE,
            "solverRuntimeBinding": SOLVER_RUNTIME_BINDING_IN_ARCHIVE or SOLVER_RUNTIME_BINDING_IN_CLOSURE,
            "candidateGeneratorModified": CANDIDATE_GENERATOR_MODIFIED or CANDIDATE_GENERATOR_MODIFIED_IN_CLOSURE,
            "candidateGeneratorBinding": CANDIDATE_GENERATOR_BINDING or CANDIDATE_GENERATOR_BINDING_IN_CLOSURE,
            "rankerModified": RANKER_MODIFIED or RANKER_MODIFIED_IN_CLOSURE,
            "rankerBinding": RANKER_BINDING or RANKER_BINDING_IN_CLOSURE,
            "verifierModified": VERIFIER_MODIFIED or VERIFIER_MODIFIED_IN_CLOSURE,
            "verifierBinding": VERIFIER_BINDING or VERIFIER_BINDING_IN_CLOSURE,
            "benchmarkScoreClaimed": BENCHMARK_SCORE_CLAIMED or BENCHMARK_SCORE_CLAIMED_IN_CLOSURE,
            "benchmarkBinding": BENCHMARK_BINDING or BENCHMARK_BINDING_IN_CLOSURE,
            "realEvaluationPerformed": REAL_EVALUATION_PERFORMED or REAL_EVALUATION_PERFORMED_IN_CLOSURE,
            "realSubmissionAuthorized": REAL_SUBMISSION_AUTHORIZED or REAL_SUBMISSION_AUTHORIZED_IN_CLOSURE,
            "kaggleAuthenticationPerformed": KAGGLE_AUTHENTICATION_PERFORMED or KAGGLE_AUTHENTICATION_PERFORMED_IN_CLOSURE,
            "kaggleSubmissionSent": KAGGLE_SUBMISSION_SENT or KAGGLE_SUBMISSION_SENT_IN_CLOSURE,
            "kaggleSubmissionBinding": KAGGLE_SUBMISSION_BINDING or KAGGLE_SUBMISSION_BINDING_IN_CLOSURE,
            "internetDuringEval": INTERNET_DURING_EVAL or INTERNET_DURING_EVAL_IN_CLOSURE,
            "externalApiDependency": EXTERNAL_API_DEPENDENCY or EXTERNAL_API_DEPENDENCY_IN_CLOSURE,
            "privateCoreExposure": PRIVATE_CORE_EXPOSURE or PRIVATE_CORE_EXPOSURE_IN_CLOSURE,
            "rawRequestBodyPersisted": RAW_REQUEST_BODY_PERSISTED or RAW_REQUEST_BODY_PERSISTED_IN_CLOSURE,
            "secretPersisted": SECRET_PERSISTED or SECRET_PERSISTED_IN_CLOSURE,
            "credentialPersisted": CREDENTIAL_PERSISTED or CREDENTIAL_PERSISTED_IN_CLOSURE,
            "apiKeyPersisted": API_KEY_PERSISTED or API_KEY_PERSISTED_IN_CLOSURE,
            "legalCertification": LEGAL_CERTIFICATION or LEGAL_CERTIFICATION_IN_CLOSURE,
            "failClosedActive": FAIL_CLOSED_ACTIVE and FAIL_CLOSED_ACTIVE_IN_CLOSURE,
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
            payload["closureId"] = self.closure_id
        return payload


def build_controlled_smoke_run_result_archive_closure_plan(
    *,
    closure_scope: str = "local diagnostic smoke-run result archive closure",
    source_archive_task_id: str = SOURCE_ARCHIVE_TASK_ID,
    source_archive_review_task_id: str = SOURCE_ARCHIVE_REVIEW_TASK_ID,
    authorization_task_id: str = AUTHORIZATION_TASK_ID,
    closure_purpose: str = "close reviewed local diagnostic smoke-run archive chain",
    poc_v0_9_source_document: str = POC_V0_9_SOURCE_DOCUMENT,
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosurePlan:
    return DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosurePlan(
        closure_scope=closure_scope,
        source_archive_task_id=source_archive_task_id,
        source_archive_review_task_id=source_archive_review_task_id,
        authorization_task_id=authorization_task_id,
        closure_purpose=closure_purpose,
        poc_v0_9_source_document=poc_v0_9_source_document,
        metadata={} if metadata is None else metadata,
    )


def close_controlled_smoke_run_result_archive(
    archive: DiagnosticArtifactEmissionUsageSmokeRunResultArchive,
    *,
    plan: DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosurePlan | None = None,
    reviewed_artifact_paths: Sequence[str] = (
        "examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-local-implementation-v1/task-113-smoke-run-result-archive.json",
        "examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-local-implementation-v1/task-113-smoke-run-result-archive.md",
    ),
    reviewed_module_path: str = "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive.py",
    reviewed_test_paths: Sequence[str] = (
        "tests/test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive.py",
        "tests/test_milestone_19_task_113_srsc_diagnostic_adapter_controlled_activation_usage_artifact_emission_usage_smoke_run_result_archive_local_implementation.py",
    ),
    source_validation_issues: Sequence[str] = (),
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosure:
    active_plan = plan or build_controlled_smoke_run_result_archive_closure_plan()
    return DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosure(
        plan=active_plan,
        source_archive_id=archive.archive_id,
        source_suite_result_id=archive.source_suite_result_id,
        source_archive_ok=archive.archive_ok,
        source_validation_issues=tuple(source_validation_issues),
        reviewed_artifact_paths=tuple(reviewed_artifact_paths),
        reviewed_module_path=reviewed_module_path,
        reviewed_test_paths=tuple(reviewed_test_paths),
        source_archived_case_count=archive.archived_case_count,
        source_archived_passed_count=archive.archived_passed_count,
        source_archived_failed_count=archive.archived_failed_count,
        metadata={} if metadata is None else metadata,
    )


def validate_controlled_smoke_run_result_archive_closure(
    closure: DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosure,
) -> tuple[str, ...]:
    issues: list[str] = []

    if not closure.closure_ok:
        issues.append("CLOSURE_NOT_OK")
    if not closure.source_archive_ok:
        issues.append("SOURCE_ARCHIVE_NOT_OK")
    if closure.source_validation_issues:
        issues.append("SOURCE_VALIDATION_ISSUES_PRESENT")
    if closure.source_archived_case_count != closure.source_archived_passed_count:
        issues.append("SOURCE_ARCHIVED_CASE_COUNT_NOT_FULL_PASS")
    if closure.source_archived_failed_count != 0:
        issues.append("SOURCE_ARCHIVED_FAILED_COUNT_NONZERO")
    if RESULT_ARCHIVE_MODIFIED or RESULT_ARCHIVE_MODULE_MODIFIED:
        issues.append("RESULT_ARCHIVE_MODIFIED")
    if SMOKE_RUN_MODULE_MODIFIED or SMOKE_RUN_MODULE_MODIFIED_IN_CLOSURE:
        issues.append("SMOKE_RUN_MODULE_MODIFIED")
    if USAGE_RUNNER_MODIFIED or USAGE_RUNNER_MODIFIED_IN_CLOSURE:
        issues.append("USAGE_RUNNER_MODIFIED")
    if ARTIFACT_EMITTER_MODIFIED or ARTIFACT_EMITTER_MODIFIED_IN_CLOSURE:
        issues.append("ARTIFACT_EMITTER_MODIFIED")
    if RUNTIME_SOLVER_MODIFIED_IN_ARCHIVE or RUNTIME_SOLVER_MODIFIED_IN_CLOSURE:
        issues.append("RUNTIME_SOLVER_MODIFIED")
    if RUNTIME_WIRING_ALLOWED_IN_ARCHIVE or RUNTIME_WIRING_ALLOWED_IN_CLOSURE:
        issues.append("RUNTIME_WIRING_ALLOWED")
    if SOLVER_RUNTIME_BINDING_IN_ARCHIVE or SOLVER_RUNTIME_BINDING_IN_CLOSURE:
        issues.append("SOLVER_RUNTIME_BINDING")
    if BENCHMARK_SCORE_CLAIMED or BENCHMARK_SCORE_CLAIMED_IN_CLOSURE:
        issues.append("BENCHMARK_SCORE_CLAIMED")
    if KAGGLE_SUBMISSION_SENT or KAGGLE_SUBMISSION_SENT_IN_CLOSURE:
        issues.append("KAGGLE_SUBMISSION_SENT")
    if PRIVATE_CORE_EXPOSURE or PRIVATE_CORE_EXPOSURE_IN_CLOSURE:
        issues.append("PRIVATE_CORE_EXPOSURE")
    if RAW_REQUEST_BODY_PERSISTED or RAW_REQUEST_BODY_PERSISTED_IN_CLOSURE:
        issues.append("RAW_REQUEST_BODY_PERSISTED")
    if SECRET_PERSISTED or SECRET_PERSISTED_IN_CLOSURE:
        issues.append("SECRET_PERSISTED")
    if CREDENTIAL_PERSISTED or CREDENTIAL_PERSISTED_IN_CLOSURE:
        issues.append("CREDENTIAL_PERSISTED")
    if API_KEY_PERSISTED or API_KEY_PERSISTED_IN_CLOSURE:
        issues.append("API_KEY_PERSISTED")
    if LEGAL_CERTIFICATION or LEGAL_CERTIFICATION_IN_CLOSURE:
        issues.append("LEGAL_CERTIFICATION")
    if not (FAIL_CLOSED_ACTIVE and FAIL_CLOSED_ACTIVE_IN_CLOSURE):
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
    "AUTHORIZATION_TASK_ID",
    "CLOSURE_REVISION",
    "CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTED",
    "DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_ONLY",
    "TASK_ID",
    "DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosure",
    "DiagnosticArtifactEmissionUsageSmokeRunResultArchiveClosurePlan",
    "build_controlled_smoke_run_result_archive_closure_plan",
    "close_controlled_smoke_run_result_archive",
    "validate_controlled_smoke_run_result_archive_closure",
]
