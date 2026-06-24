"""SRSC controlled smoke-run result archive.

Milestone #19 Task 113 - local diagnostic-only result archive implementation.

This module archives public-safe summaries of reviewed smoke-run suite results.
It does not modify the smoke-run module, usage runner, artifact emitter,
activation usage layer, activation wrapper, adapter, solver runtime, candidate
generator, ranker, verifier, benchmark layer, Kaggle behavior, private core
behavior, or legal certification behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.srsc_claim_ledger import stable_digest
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run import (
    BENCHMARK_SCORE_CLAIMED,
    CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED,
    DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_ONLY,
    FAIL_CLOSED_ACTIVE,
    KAGGLE_SUBMISSION_SENT,
    LEGAL_CERTIFICATION,
    POC_V0_9_BENCHMARKED,
    POC_V0_9_FAULT_INJECTION_PERFORMED,
    POC_V0_9_MATURITY,
    POC_V0_9_PRODUCTION_READY,
    POC_V0_9_RUNTIME_IMPLEMENTED,
    POC_V0_9_SOURCE_DOCUMENT,
    POC_V0_9_STATUS,
    PRIVATE_CORE_EXPOSURE,
    RUNTIME_SOLVER_MODIFIED,
    RUNTIME_WIRING_ALLOWED,
    SMOKE_RUN_REVISION,
    SOLVER_RUNTIME_BINDING,
    TASK_ID as SOURCE_SMOKE_RUN_TASK_ID,
    DiagnosticArtifactEmissionUsageSmokeRunResult,
    DiagnosticArtifactEmissionUsageSmokeRunSuiteResult,
)


TASK_ID = "MILESTONE_19_TASK_113_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_IMPLEMENTATION_V1"
AUTHORIZATION_TASK_ID = "MILESTONE_19_TASK_112_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"
RESULT_ARCHIVE_REVISION = "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_V1"

CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTED = True
DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_ONLY = True

SMOKE_RUN_MODULE_MODIFIED = False
USAGE_RUNNER_MODIFIED = False
ARTIFACT_EMITTER_MODIFIED = False
USAGE_LAYER_MODIFIED = False
ACTIVATION_WRAPPER_MODIFIED = False
ADAPTER_MODIFIED = False

RUNTIME_ACTIVATION_AUTHORIZED = False
RUNTIME_SOLVER_MODIFIED_IN_ARCHIVE = False
RUNTIME_WIRING_ALLOWED_IN_ARCHIVE = False
SOLVER_RUNTIME_BINDING_IN_ARCHIVE = False

CANDIDATE_GENERATOR_MODIFIED = False
CANDIDATE_GENERATOR_BINDING = False
RANKER_MODIFIED = False
RANKER_BINDING = False
VERIFIER_MODIFIED = False
VERIFIER_BINDING = False

BENCHMARK_BINDING = False
REAL_EVALUATION_PERFORMED = False
REAL_SUBMISSION_AUTHORIZED = False

KAGGLE_AUTHENTICATION_PERFORMED = False
KAGGLE_SUBMISSION_BINDING = False

INTERNET_DURING_EVAL = False
EXTERNAL_API_DEPENDENCY = False
RAW_REQUEST_BODY_PERSISTED = False
SECRET_PERSISTED = False
CREDENTIAL_PERSISTED = False
API_KEY_PERSISTED = False


def _clean_text(value: str, *, field_name: str) -> str:
    cleaned = " ".join(str(value).strip().split())
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned


def _clean_metadata(value: Mapping[str, Any] | None) -> dict[str, Any]:
    if value is None:
        return {}
    return {str(key): value[key] for key in sorted(value)}


@dataclass(frozen=True)
class DiagnosticArtifactEmissionUsageSmokeRunResultArchivePlan:
    """Plan for creating a deterministic local smoke-run result archive."""

    archive_scope: str = "local diagnostic smoke-run result archive"
    source_task_id: str = SOURCE_SMOKE_RUN_TASK_ID
    authorization_task_id: str = AUTHORIZATION_TASK_ID
    milestone_id: str = "MILESTONE_19"
    archive_purpose: str = "archive reviewed local diagnostic smoke-run results"
    poc_v0_9_source_document: str = POC_V0_9_SOURCE_DOCUMENT
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "archive_scope", _clean_text(self.archive_scope, field_name="archive_scope"))
        object.__setattr__(self, "source_task_id", _clean_text(self.source_task_id, field_name="source_task_id"))
        object.__setattr__(self, "authorization_task_id", _clean_text(self.authorization_task_id, field_name="authorization_task_id"))
        object.__setattr__(self, "milestone_id", _clean_text(self.milestone_id, field_name="milestone_id"))
        object.__setattr__(self, "archive_purpose", _clean_text(self.archive_purpose, field_name="archive_purpose"))
        object.__setattr__(self, "poc_v0_9_source_document", _clean_text(self.poc_v0_9_source_document, field_name="poc_v0_9_source_document"))
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def plan_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-SMOKE-RUN-RESULT-ARCHIVE-PLAN", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-SMOKE-ARCHIVE-PLAN-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "archiveScope": self.archive_scope,
            "sourceTaskId": self.source_task_id,
            "authorizationTaskId": self.authorization_task_id,
            "milestoneId": self.milestone_id,
            "archivePurpose": self.archive_purpose,
            "pocV09SourceDocument": self.poc_v0_9_source_document,
            "pocV09Status": POC_V0_9_STATUS,
            "pocV09Maturity": POC_V0_9_MATURITY,
            "pocV09RuntimeImplemented": POC_V0_9_RUNTIME_IMPLEMENTED,
            "pocV09Benchmarked": POC_V0_9_BENCHMARKED,
            "pocV09FaultInjectionPerformed": POC_V0_9_FAULT_INJECTION_PERFORMED,
            "pocV09ProductionReady": POC_V0_9_PRODUCTION_READY,
            "metadata": dict(self.metadata),
            "resultArchiveRevision": RESULT_ARCHIVE_REVISION,
            "smokeRunRevision": SMOKE_RUN_REVISION,
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
class DiagnosticArtifactEmissionUsageSmokeRunResultArchiveEntry:
    """Public-safe archive entry for one smoke-run result."""

    case_id: str
    case_name: str
    smoke_run_result_id: str
    emitted_artifact_count: int
    blocked_artifact_count: int
    blocked_usage_request_count: int
    blocked_reason: str | None
    expectation_ok: bool
    smoke_run_ok: bool
    no_score_claim_marker: bool = True
    no_submission_marker: bool = True
    legal_certification: bool = False
    fail_closed_active: bool = True
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "case_id", _clean_text(self.case_id, field_name="case_id"))
        object.__setattr__(self, "case_name", _clean_text(self.case_name, field_name="case_name"))
        object.__setattr__(self, "smoke_run_result_id", _clean_text(self.smoke_run_result_id, field_name="smoke_run_result_id"))
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @classmethod
    def from_smoke_run_result(
        cls,
        result: DiagnosticArtifactEmissionUsageSmokeRunResult,
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> "DiagnosticArtifactEmissionUsageSmokeRunResultArchiveEntry":
        public = result.to_public_dict()
        return cls(
            case_id=result.smoke_run_case.case_id,
            case_name=result.smoke_run_case.case_name,
            smoke_run_result_id=result.smoke_run_result_id,
            emitted_artifact_count=result.emitted_artifact_count,
            blocked_artifact_count=result.blocked_artifact_count,
            blocked_usage_request_count=result.blocked_usage_request_count,
            blocked_reason=result.blocked_reason,
            expectation_ok=result.expectation_ok,
            smoke_run_ok=result.smoke_run_ok,
            no_score_claim_marker=bool(public.get("noScoreClaimMarker", True)),
            no_submission_marker=bool(public.get("noSubmissionMarker", True)),
            legal_certification=bool(public.get("legalCertification", False)),
            fail_closed_active=bool(public.get("failClosedActive", True)),
            metadata={} if metadata is None else metadata,
        )

    @property
    def entry_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-SMOKE-RUN-RESULT-ARCHIVE-ENTRY", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-SMOKE-ARCHIVE-ENTRY-{digest[:16].upper()}"

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "caseId": self.case_id,
            "caseName": self.case_name,
            "smokeRunResultId": self.smoke_run_result_id,
            "emittedArtifactCount": self.emitted_artifact_count,
            "blockedArtifactCount": self.blocked_artifact_count,
            "blockedUsageRequestCount": self.blocked_usage_request_count,
            "blockedReason": self.blocked_reason,
            "expectationOk": self.expectation_ok,
            "smokeRunOk": self.smoke_run_ok,
            "noScoreClaimMarker": self.no_score_claim_marker,
            "noSubmissionMarker": self.no_submission_marker,
            "legalCertification": self.legal_certification,
            "failClosedActive": self.fail_closed_active,
            "metadata": dict(self.metadata),
        }
        if include_id:
            payload["entryId"] = self.entry_id
        return payload


@dataclass(frozen=True)
class DiagnosticArtifactEmissionUsageSmokeRunResultArchive:
    """Deterministic local archive for one smoke-run suite result."""

    plan: DiagnosticArtifactEmissionUsageSmokeRunResultArchivePlan
    source_suite_result_id: str
    source_suite_ok: bool
    source_case_count: int
    source_passed_count: int
    source_failed_count: int
    entries: tuple[DiagnosticArtifactEmissionUsageSmokeRunResultArchiveEntry, ...]
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "source_suite_result_id", _clean_text(self.source_suite_result_id, field_name="source_suite_result_id"))
        object.__setattr__(self, "metadata", _clean_metadata(self.metadata))

    @property
    def archive_id(self) -> str:
        digest = stable_digest("SRSC-DIAGNOSTIC-SMOKE-RUN-RESULT-ARCHIVE", self.to_public_dict(include_id=False))
        return f"SRSC-DIAG-SMOKE-ARCHIVE-{digest[:16].upper()}"

    @property
    def archived_case_count(self) -> int:
        return len(self.entries)

    @property
    def archived_passed_count(self) -> int:
        return sum(1 for entry in self.entries if entry.smoke_run_ok)

    @property
    def archived_failed_count(self) -> int:
        return self.archived_case_count - self.archived_passed_count

    @property
    def emitted_artifact_count(self) -> int:
        return sum(entry.emitted_artifact_count for entry in self.entries)

    @property
    def blocked_artifact_count(self) -> int:
        return sum(entry.blocked_artifact_count for entry in self.entries)

    @property
    def blocked_usage_request_count(self) -> int:
        return sum(entry.blocked_usage_request_count for entry in self.entries)

    @property
    def archive_ok(self) -> bool:
        return (
            CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTED is True
            and DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_ONLY is True
            and self.source_suite_ok is True
            and self.archived_case_count == self.source_case_count
            and self.archived_passed_count == self.source_passed_count
            and self.archived_failed_count == self.source_failed_count
            and all(entry.no_score_claim_marker for entry in self.entries)
            and all(entry.no_submission_marker for entry in self.entries)
            and all(entry.legal_certification is False for entry in self.entries)
            and all(entry.fail_closed_active is True for entry in self.entries)
            and SMOKE_RUN_MODULE_MODIFIED is False
            and USAGE_RUNNER_MODIFIED is False
            and ARTIFACT_EMITTER_MODIFIED is False
            and RUNTIME_SOLVER_MODIFIED is False
            and RUNTIME_WIRING_ALLOWED is False
            and SOLVER_RUNTIME_BINDING is False
            and BENCHMARK_SCORE_CLAIMED is False
            and KAGGLE_SUBMISSION_SENT is False
            and PRIVATE_CORE_EXPOSURE is False
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
            "resultArchiveRevision": RESULT_ARCHIVE_REVISION,
            "plan": self.plan.to_public_dict(),
            "sourceSuiteResultId": self.source_suite_result_id,
            "sourceSuiteOk": self.source_suite_ok,
            "sourceCaseCount": self.source_case_count,
            "sourcePassedCount": self.source_passed_count,
            "sourceFailedCount": self.source_failed_count,
            "entries": [entry.to_public_dict() for entry in self.entries],
            "archivedCaseCount": self.archived_case_count,
            "archivedPassedCount": self.archived_passed_count,
            "archivedFailedCount": self.archived_failed_count,
            "emittedArtifactCount": self.emitted_artifact_count,
            "blockedArtifactCount": self.blocked_artifact_count,
            "blockedUsageRequestCount": self.blocked_usage_request_count,
            "archiveOk": self.archive_ok,
            "metadata": dict(self.metadata),
            "controlledSmokeRunResultArchiveImplemented": CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTED,
            "diagnosticSmokeRunResultArchiveOnly": DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_ONLY,
            "smokeRunModuleModified": SMOKE_RUN_MODULE_MODIFIED,
            "usageRunnerModified": USAGE_RUNNER_MODIFIED,
            "artifactEmitterModified": ARTIFACT_EMITTER_MODIFIED,
            "usageLayerModified": USAGE_LAYER_MODIFIED,
            "activationWrapperModified": ACTIVATION_WRAPPER_MODIFIED,
            "adapterModified": ADAPTER_MODIFIED,
            "runtimeActivationAuthorized": RUNTIME_ACTIVATION_AUTHORIZED,
            "runtimeSolverModified": RUNTIME_SOLVER_MODIFIED_IN_ARCHIVE or RUNTIME_SOLVER_MODIFIED,
            "runtimeWiringAllowed": RUNTIME_WIRING_ALLOWED_IN_ARCHIVE or RUNTIME_WIRING_ALLOWED,
            "solverRuntimeBinding": SOLVER_RUNTIME_BINDING_IN_ARCHIVE or SOLVER_RUNTIME_BINDING,
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
            payload["archiveId"] = self.archive_id
        return payload


def build_controlled_smoke_run_result_archive_plan(
    *,
    archive_scope: str = "local diagnostic smoke-run result archive",
    source_task_id: str = SOURCE_SMOKE_RUN_TASK_ID,
    authorization_task_id: str = AUTHORIZATION_TASK_ID,
    milestone_id: str = "MILESTONE_19",
    archive_purpose: str = "archive reviewed local diagnostic smoke-run results",
    poc_v0_9_source_document: str = POC_V0_9_SOURCE_DOCUMENT,
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticArtifactEmissionUsageSmokeRunResultArchivePlan:
    return DiagnosticArtifactEmissionUsageSmokeRunResultArchivePlan(
        archive_scope=archive_scope,
        source_task_id=source_task_id,
        authorization_task_id=authorization_task_id,
        milestone_id=milestone_id,
        archive_purpose=archive_purpose,
        poc_v0_9_source_document=poc_v0_9_source_document,
        metadata={} if metadata is None else metadata,
    )


def archive_controlled_smoke_run_suite_result(
    suite_result: DiagnosticArtifactEmissionUsageSmokeRunSuiteResult,
    *,
    plan: DiagnosticArtifactEmissionUsageSmokeRunResultArchivePlan | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> DiagnosticArtifactEmissionUsageSmokeRunResultArchive:
    active_plan = plan or build_controlled_smoke_run_result_archive_plan()
    entries = tuple(
        DiagnosticArtifactEmissionUsageSmokeRunResultArchiveEntry.from_smoke_run_result(
            result,
            metadata={
                "sourceSuiteResultId": suite_result.suite_result_id,
                "sourceTaskId": active_plan.source_task_id,
                "authorizationTaskId": active_plan.authorization_task_id,
            },
        )
        for result in suite_result.results
    )
    return DiagnosticArtifactEmissionUsageSmokeRunResultArchive(
        plan=active_plan,
        source_suite_result_id=suite_result.suite_result_id,
        source_suite_ok=suite_result.suite_ok,
        source_case_count=suite_result.case_count,
        source_passed_count=suite_result.passed_count,
        source_failed_count=suite_result.failed_count,
        entries=entries,
        metadata={} if metadata is None else metadata,
    )


def validate_controlled_smoke_run_result_archive(
    archive: DiagnosticArtifactEmissionUsageSmokeRunResultArchive,
) -> tuple[str, ...]:
    issues: list[str] = []

    if not archive.archive_ok:
        issues.append("ARCHIVE_NOT_OK")
    if archive.archived_case_count != archive.source_case_count:
        issues.append("ARCHIVED_CASE_COUNT_MISMATCH")
    if archive.archived_passed_count != archive.source_passed_count:
        issues.append("ARCHIVED_PASSED_COUNT_MISMATCH")
    if archive.archived_failed_count != archive.source_failed_count:
        issues.append("ARCHIVED_FAILED_COUNT_MISMATCH")
    if any(not entry.no_score_claim_marker for entry in archive.entries):
        issues.append("NO_SCORE_MARKER_MISSING")
    if any(not entry.no_submission_marker for entry in archive.entries):
        issues.append("NO_SUBMISSION_MARKER_MISSING")
    if any(entry.legal_certification is not False for entry in archive.entries):
        issues.append("LEGAL_CERTIFICATION_ENTRY_VIOLATION")
    if any(entry.fail_closed_active is not True for entry in archive.entries):
        issues.append("FAIL_CLOSED_ENTRY_VIOLATION")
    if RUNTIME_SOLVER_MODIFIED or RUNTIME_SOLVER_MODIFIED_IN_ARCHIVE:
        issues.append("RUNTIME_SOLVER_MODIFIED")
    if RUNTIME_WIRING_ALLOWED or RUNTIME_WIRING_ALLOWED_IN_ARCHIVE:
        issues.append("RUNTIME_WIRING_ALLOWED")
    if SOLVER_RUNTIME_BINDING or SOLVER_RUNTIME_BINDING_IN_ARCHIVE:
        issues.append("SOLVER_RUNTIME_BINDING")
    if BENCHMARK_SCORE_CLAIMED:
        issues.append("BENCHMARK_SCORE_CLAIMED")
    if KAGGLE_SUBMISSION_SENT:
        issues.append("KAGGLE_SUBMISSION_SENT")
    if PRIVATE_CORE_EXPOSURE:
        issues.append("PRIVATE_CORE_EXPOSURE")
    if LEGAL_CERTIFICATION:
        issues.append("LEGAL_CERTIFICATION")
    if POC_V0_9_RUNTIME_IMPLEMENTED:
        issues.append("POC_V0_9_RUNTIME_IMPLEMENTED")
    if POC_V0_9_BENCHMARKED:
        issues.append("POC_V0_9_BENCHMARKED")
    if POC_V0_9_FAULT_INJECTION_PERFORMED:
        issues.append("POC_V0_9_FAULT_INJECTION_PERFORMED")
    if POC_V0_9_PRODUCTION_READY:
        issues.append("POC_V0_9_PRODUCTION_READY")
    if RAW_REQUEST_BODY_PERSISTED:
        issues.append("RAW_REQUEST_BODY_PERSISTED")
    if SECRET_PERSISTED or CREDENTIAL_PERSISTED or API_KEY_PERSISTED:
        issues.append("SECRET_OR_CREDENTIAL_PERSISTED")

    return tuple(issues)


__all__ = [
    "ADAPTER_MODIFIED",
    "API_KEY_PERSISTED",
        "ARTIFACT_EMITTER_MODIFIED",
    "AUTHORIZATION_TASK_ID",
    "BENCHMARK_BINDING",
    "CANDIDATE_GENERATOR_BINDING",
    "CANDIDATE_GENERATOR_MODIFIED",
    "CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTED",
    "CREDENTIAL_PERSISTED",
    "DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_ONLY",
    "EXTERNAL_API_DEPENDENCY",
    "FAIL_CLOSED_ACTIVE",
    "INTERNET_DURING_EVAL",
    "KAGGLE_AUTHENTICATION_PERFORMED",
    "KAGGLE_SUBMISSION_BINDING",
    "LEGAL_CERTIFICATION",
    "PRIVATE_CORE_EXPOSURE",
    "RAW_REQUEST_BODY_PERSISTED",
    "RANKER_BINDING",
    "RANKER_MODIFIED",
    "REAL_EVALUATION_PERFORMED",
    "REAL_SUBMISSION_AUTHORIZED",
    "RESULT_ARCHIVE_REVISION",
    "RUNTIME_ACTIVATION_AUTHORIZED",
    "RUNTIME_SOLVER_MODIFIED_IN_ARCHIVE",
    "RUNTIME_WIRING_ALLOWED_IN_ARCHIVE",
    "SECRET_PERSISTED",
    "SMOKE_RUN_MODULE_MODIFIED",
    "SOLVER_RUNTIME_BINDING_IN_ARCHIVE",
    "TASK_ID",
    "USAGE_LAYER_MODIFIED",
    "USAGE_RUNNER_MODIFIED",
    "VERIFIER_BINDING",
    "VERIFIER_MODIFIED",
    "DiagnosticArtifactEmissionUsageSmokeRunResultArchive",
    "DiagnosticArtifactEmissionUsageSmokeRunResultArchiveEntry",
    "DiagnosticArtifactEmissionUsageSmokeRunResultArchivePlan",
    "archive_controlled_smoke_run_suite_result",
    "build_controlled_smoke_run_result_archive_plan",
    "validate_controlled_smoke_run_result_archive",
]
