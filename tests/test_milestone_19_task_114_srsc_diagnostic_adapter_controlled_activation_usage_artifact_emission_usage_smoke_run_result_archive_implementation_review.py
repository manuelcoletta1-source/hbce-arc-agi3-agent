"""Milestone #19 Task 114 - SRSC smoke-run result archive implementation review validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run import (
    run_controlled_artifact_emission_usage_smoke_run_suite,
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive import (
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTED,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_ONLY,
    FAIL_CLOSED_ACTIVE,
    LEGAL_CERTIFICATION,
    POC_V0_9_BENCHMARKED,
    POC_V0_9_FAULT_INJECTION_PERFORMED,
    POC_V0_9_PRODUCTION_READY,
    POC_V0_9_RUNTIME_IMPLEMENTED,
    PRIVATE_CORE_EXPOSURE,
    RAW_REQUEST_BODY_PERSISTED,
    RESULT_ARCHIVE_REVISION,
    RUNTIME_SOLVER_MODIFIED_IN_ARCHIVE,
    RUNTIME_WIRING_ALLOWED_IN_ARCHIVE,
    SECRET_PERSISTED,
    SMOKE_RUN_MODULE_MODIFIED,
    SOLVER_RUNTIME_BINDING_IN_ARCHIVE,
    TASK_ID as TASK_113_ID,
    USAGE_RUNNER_MODIFIED,
    archive_controlled_smoke_run_suite_result,
    validate_controlled_smoke_run_result_archive,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_113 = ROOT / "docs" / "milestone-19-task-113-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-local-implementation-v1.md"
DOC_TASK_114 = ROOT / "docs" / "milestone-19-task-114-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-implementation-review-v1.md"
ARCHIVE_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive.py"
ARCHIVE_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-implementation-review-v1" / "task-114-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-implementation-review-v1" / "task-114-index.txt"
ARCHIVE_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-local-implementation-v1" / "task-113-smoke-run-result-archive.json"
ARCHIVE_MD = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-local-implementation-v1" / "task-113-smoke-run-result-archive.md"


def test_task_114_required_files_exist() -> None:
    assert DOC_TASK_113.exists()
    assert DOC_TASK_114.exists()
    assert ARCHIVE_MODULE.exists()
    assert ARCHIVE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert ARCHIVE_JSON.exists()
    assert ARCHIVE_MD.exists()


def test_task_114_dependency_markers() -> None:
    text = DOC_TASK_113.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_113_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_113_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_113_DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_ONLY=true" in text
    assert "MILESTONE_19_TASK_113_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_113_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_113_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_113_LEGAL_CERTIFICATION=false" in text


def test_task_114_archive_module_review_contract() -> None:
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)

    assert TASK_113_ID == "MILESTONE_19_TASK_113_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_IMPLEMENTATION_V1"
    assert RESULT_ARCHIVE_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_V1"
    assert archive.archive_ok is True
    assert validate_controlled_smoke_run_result_archive(archive) == ()
    assert archive.archived_case_count == 8
    assert archive.archived_passed_count == 8
    assert archive.archived_failed_count == 0
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_ONLY is True
    assert SMOKE_RUN_MODULE_MODIFIED is False
    assert USAGE_RUNNER_MODIFIED is False
    assert RUNTIME_SOLVER_MODIFIED_IN_ARCHIVE is False
    assert RUNTIME_WIRING_ALLOWED_IN_ARCHIVE is False
    assert SOLVER_RUNTIME_BINDING_IN_ARCHIVE is False
    assert PRIVATE_CORE_EXPOSURE is False
    assert RAW_REQUEST_BODY_PERSISTED is False
    assert SECRET_PERSISTED is False
    assert LEGAL_CERTIFICATION is False
    assert FAIL_CLOSED_ACTIVE is True
    assert POC_V0_9_RUNTIME_IMPLEMENTED is False
    assert POC_V0_9_BENCHMARKED is False
    assert POC_V0_9_FAULT_INJECTION_PERFORMED is False
    assert POC_V0_9_PRODUCTION_READY is False


def test_task_114_static_archive_artifact_review() -> None:
    payload = json.loads(ARCHIVE_JSON.read_text(encoding="utf-8"))
    assert payload["archiveId"].startswith("SRSC-DIAG-SMOKE-ARCHIVE-")
    assert payload["archiveOk"] is True
    assert payload["archivedCaseCount"] == 8
    assert payload["archivedPassedCount"] == 8
    assert payload["archivedFailedCount"] == 0
    assert payload["validationIssues"] == []
    assert payload["controlledSmokeRunResultArchiveImplemented"] is True
    assert payload["diagnosticSmokeRunResultArchiveOnly"] is True
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["solverRuntimeBinding"] is False
    assert payload["benchmarkScoreClaimed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["rawRequestBodyPersisted"] is False
    assert payload["secretPersisted"] is False
    assert payload["credentialPersisted"] is False
    assert payload["apiKeyPersisted"] is False


def test_task_114_canonical_markers() -> None:
    text = DOC_TASK_114.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_114_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_114_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_114_MODE=REVIEW_ONLY_NO_RESULT_ARCHIVE_MODIFICATION" in text
    assert "MILESTONE_19_TASK_114_DECISION=ACCEPT_TASK_113_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_114_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_114_RESULT_ARCHIVE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_114_RESULT_ARCHIVE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_114_SMOKE_RUN_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_114_USAGE_RUNNER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_114_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_114_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_114_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_114_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_114_BENCHMARK_SCORE_CLAIMED=false" in text
    assert "MILESTONE_19_TASK_114_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_114_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_114_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_114_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_114_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_114_POC_V0_9_RUNTIME_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_114_POC_V0_9_BENCHMARKED=false" in text
    assert "MILESTONE_19_TASK_114_POC_V0_9_PRODUCTION_READY=false" in text


def test_task_114_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_114_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_RESULT_ARCHIVE_MODIFICATION"
    assert manifest["decision"] == "ACCEPT_TASK_113_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_IMPLEMENTATION"
    assert manifest["controlledSmokeRunResultArchiveImplementationReviewPerformed"] is True
    assert manifest["task113SmokeRunResultArchiveImplementationAccepted"] is True
    assert manifest["implementationPerformedInTask114"] is False
    assert manifest["resultArchiveModifiedInTask114"] is False
    assert manifest["resultArchiveModuleModifiedInTask114"] is False
    assert manifest["smokeRunModuleModifiedInTask114"] is False
    assert manifest["usageRunnerModifiedInTask114"] is False
    assert manifest["artifactEmitterModifiedInTask114"] is False
    assert manifest["runtimeSolverModified"] is False
    assert manifest["runtimeWiringAllowed"] is False
    assert manifest["solverRuntimeBinding"] is False
    assert manifest["benchmarkScoreClaimed"] is False
    assert manifest["kaggleSubmissionSent"] is False
    assert manifest["privateCoreExposure"] is False
    assert manifest["rawRequestBodyPersisted"] is False
    assert manifest["secretPersisted"] is False
    assert manifest["credentialPersisted"] is False
    assert manifest["apiKeyPersisted"] is False
    assert manifest["legalCertification"] is False
    assert manifest["failClosedActive"] is True
    assert manifest["pocV09RuntimeImplemented"] is False
    assert manifest["pocV09Benchmarked"] is False
    assert manifest["pocV09FaultInjectionPerformed"] is False
    assert manifest["pocV09ProductionReady"] is False
