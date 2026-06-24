"""Milestone #19 Task 118 - SRSC smoke-run result archive closure implementation review validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run import (
    run_controlled_artifact_emission_usage_smoke_run_suite,
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive import (
    archive_controlled_smoke_run_suite_result,
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure import (
    CLOSURE_REVISION,
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTED,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_ONLY,
    TASK_ID as TASK_117_ID,
    close_controlled_smoke_run_result_archive,
    validate_controlled_smoke_run_result_archive_closure,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_117 = ROOT / "docs" / "milestone-19-task-117-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-local-implementation-v1.md"
DOC_TASK_118 = ROOT / "docs" / "milestone-19-task-118-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-implementation-review-v1.md"
CLOSURE_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure.py"
CLOSURE_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-implementation-review-v1" / "task-118-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-implementation-review-v1" / "task-118-index.txt"
CLOSURE_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-local-implementation-v1" / "task-117-smoke-run-result-archive-closure.json"
CLOSURE_MD = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-local-implementation-v1" / "task-117-smoke-run-result-archive-closure.md"


def _build_closure():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    return close_controlled_smoke_run_result_archive(archive)


def test_task_118_required_files_exist() -> None:
    assert DOC_TASK_117.exists()
    assert DOC_TASK_118.exists()
    assert CLOSURE_MODULE.exists()
    assert CLOSURE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert CLOSURE_JSON.exists()
    assert CLOSURE_MD.exists()


def test_task_118_dependency_markers() -> None:
    text = DOC_TASK_117.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_117_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_117_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_117_DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_ONLY=true" in text
    assert "MILESTONE_19_TASK_117_RESULT_ARCHIVE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_117_RESULT_ARCHIVE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_117_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_117_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_117_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_117_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_117_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_117_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_117_NEXT_STAGE=MILESTONE_19_TASK_118_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTATION_REVIEW_V1" in text


def test_task_118_closure_contract_review() -> None:
    closure = _build_closure()
    assert TASK_117_ID == "MILESTONE_19_TASK_117_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_LOCAL_IMPLEMENTATION_V1"
    assert CLOSURE_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_LOCAL_V1"
    assert closure.closure_ok is True
    assert closure.source_archived_case_count == 8
    assert closure.source_archived_passed_count == 8
    assert closure.source_archived_failed_count == 0
    assert validate_controlled_smoke_run_result_archive_closure(closure) == ()
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_ONLY is True


def test_task_118_static_closure_artifact_review() -> None:
    payload = json.loads(CLOSURE_JSON.read_text(encoding="utf-8"))
    assert payload["closureId"].startswith("SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-")
    assert payload["closureOk"] is True
    assert payload["sourceArchivedCaseCount"] == 8
    assert payload["sourceArchivedPassedCount"] == 8
    assert payload["sourceArchivedFailedCount"] == 0
    assert payload["validationIssues"] == []
    assert payload["resultArchiveModified"] is False
    assert payload["resultArchiveModuleModified"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["solverRuntimeBinding"] is False
    assert payload["benchmarkScoreClaimed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["privateCoreExposure"] is False
    assert payload["rawRequestBodyPersisted"] is False
    assert payload["secretPersisted"] is False
    assert payload["credentialPersisted"] is False
    assert payload["apiKeyPersisted"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True


def test_task_118_canonical_markers() -> None:
    text = DOC_TASK_118.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_118_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_118_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_118_MODE=REVIEW_ONLY_NO_ARCHIVE_CLOSURE_MODIFICATION" in text
    assert "MILESTONE_19_TASK_118_DECISION=ACCEPT_TASK_117_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_LOCAL_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_118_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_118_ARCHIVE_CLOSURE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_118_ARCHIVE_CLOSURE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_118_RESULT_ARCHIVE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_118_RESULT_ARCHIVE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_118_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_118_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_118_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_118_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_118_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_118_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_118_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_118_NEXT_STAGE=MILESTONE_19_TASK_119_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_PLANNING_V1" in text


def test_task_118_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_118_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_ARCHIVE_CLOSURE_MODIFICATION"
    assert manifest["decision"] == "ACCEPT_TASK_117_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_LOCAL_IMPLEMENTATION"
    assert manifest["controlledSmokeRunResultArchiveClosureImplementationReviewPerformed"] is True
    assert manifest["task117SmokeRunResultArchiveClosureImplementationAccepted"] is True
    assert manifest["implementationPerformedInTask118"] is False
    assert manifest["archiveClosureModified"] is False
    assert manifest["archiveClosureModuleModified"] is False
    assert manifest["resultArchiveModified"] is False
    assert manifest["resultArchiveModuleModified"] is False
    assert manifest["runtimeSolverModified"] is False
    assert manifest["runtimeWiringAllowed"] is False
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
