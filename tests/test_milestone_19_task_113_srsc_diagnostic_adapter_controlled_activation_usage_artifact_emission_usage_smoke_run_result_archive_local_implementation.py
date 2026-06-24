"""Milestone #19 Task 113 - SRSC smoke-run result archive local implementation validation."""

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
    TASK_ID,
    USAGE_RUNNER_MODIFIED,
    archive_controlled_smoke_run_suite_result,
    validate_controlled_smoke_run_result_archive,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_112 = ROOT / "docs" / "milestone-19-task-112-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-implementation-authorization-review-v1.md"
DOC_TASK_113 = ROOT / "docs" / "milestone-19-task-113-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-local-implementation-v1.md"
ARCHIVE_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive.py"
ARCHIVE_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-local-implementation-v1" / "task-113-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-local-implementation-v1" / "task-113-index.txt"
ARCHIVE_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-local-implementation-v1" / "task-113-smoke-run-result-archive.json"
ARCHIVE_MD = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-local-implementation-v1" / "task-113-smoke-run-result-archive.md"


def test_task_113_required_files_exist() -> None:
    assert DOC_TASK_112.exists()
    assert DOC_TASK_113.exists()
    assert ARCHIVE_MODULE.exists()
    assert ARCHIVE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert ARCHIVE_JSON.exists()
    assert ARCHIVE_MD.exists()


def test_task_113_dependency_markers() -> None:
    text = DOC_TASK_112.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_112_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_112_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_112_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_112_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_112_RESULT_ARCHIVE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_112_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_112_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_112_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_112_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_112_LEGAL_CERTIFICATION=false" in text


def test_task_113_archive_module_contract() -> None:
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)

    assert TASK_ID == "MILESTONE_19_TASK_113_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_IMPLEMENTATION_V1"
    assert RESULT_ARCHIVE_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_V1"
    assert archive.archive_ok is True
    assert validate_controlled_smoke_run_result_archive(archive) == ()
    assert archive.archived_case_count == 8
    assert archive.archived_passed_count == 8
    assert archive.archived_failed_count == 0


def test_task_113_canonical_markers() -> None:
    text = DOC_TASK_113.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_113_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_113_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_IMPLEMENTATION_READY" in text
    assert "MILESTONE_19_TASK_113_MODE=LOCAL_DIAGNOSTIC_ONLY_RESULT_ARCHIVE_NO_RUNTIME_WIRING" in text
    assert "MILESTONE_19_TASK_113_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_113_DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_ONLY=true" in text
    assert "MILESTONE_19_TASK_113_SMOKE_RUN_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_113_USAGE_RUNNER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_113_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_113_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_113_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_113_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_113_BENCHMARK_SCORE_CLAIMED=false" in text
    assert "MILESTONE_19_TASK_113_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_113_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_113_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_113_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_113_FAIL_CLOSED_ACTIVE=true" in text


def test_task_113_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_113_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_IMPLEMENTATION_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_IMPLEMENTATION_READY"
    assert manifest["mode"] == "LOCAL_DIAGNOSTIC_ONLY_RESULT_ARCHIVE_NO_RUNTIME_WIRING"
    assert manifest["controlledSmokeRunResultArchiveImplemented"] is True
    assert manifest["diagnosticSmokeRunResultArchiveOnly"] is True
    assert manifest["smokeRunModuleModified"] is False
    assert manifest["usageRunnerModified"] is False
    assert manifest["artifactEmitterModified"] is False
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


def test_task_113_static_archive_artifact() -> None:
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


def test_task_113_boundary_constants() -> None:
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
