"""Milestone #19 Task 121 - SRSC smoke-run result archive closure finalization local implementation validation."""

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
    close_controlled_smoke_run_result_archive,
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_finalization import (
    FINALIZATION_REVISION,
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_ONLY,
    TASK_ID,
    finalize_controlled_smoke_run_result_archive_closure,
    validate_controlled_smoke_run_result_archive_closure_finalization,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_120 = ROOT / "docs" / "milestone-19-task-120-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-authorization-review-v1.md"
DOC_TASK_121 = ROOT / "docs" / "milestone-19-task-121-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-local-implementation-v1.md"
FINALIZATION_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_finalization.py"
FINALIZATION_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_finalization.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-local-implementation-v1" / "task-121-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-local-implementation-v1" / "task-121-index.txt"
FINALIZATION_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-local-implementation-v1" / "task-121-smoke-run-result-archive-closure-finalization.json"
FINALIZATION_MD = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-local-implementation-v1" / "task-121-smoke-run-result-archive-closure-finalization.md"


def _build_finalization():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    return finalize_controlled_smoke_run_result_archive_closure(closure)


def test_task_121_required_files_exist() -> None:
    assert DOC_TASK_120.exists()
    assert DOC_TASK_121.exists()
    assert FINALIZATION_MODULE.exists()
    assert FINALIZATION_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert FINALIZATION_JSON.exists()
    assert FINALIZATION_MD.exists()


def test_task_121_dependency_markers() -> None:
    text = DOC_TASK_120.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_120_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_120_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_120_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_120_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_120_CLOSURE_FINALIZATION_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_120_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_120_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_120_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_120_LEGAL_CERTIFICATION=false" in text


def test_task_121_finalization_contract() -> None:
    finalization = _build_finalization()
    assert TASK_ID == "MILESTONE_19_TASK_121_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_V1"
    assert FINALIZATION_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_V1"
    assert finalization.finalization_ok is True
    assert finalization.source_archived_case_count == 8
    assert finalization.source_archived_passed_count == 8
    assert finalization.source_archived_failed_count == 0
    assert validate_controlled_smoke_run_result_archive_closure_finalization(finalization) == ()
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_ONLY is True


def test_task_121_canonical_markers() -> None:
    text = DOC_TASK_121.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_121_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_121_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_READY" in text
    assert "MILESTONE_19_TASK_121_MODE=LOCAL_DIAGNOSTIC_ONLY_CLOSURE_FINALIZATION_NO_RUNTIME_WIRING" in text
    assert "MILESTONE_19_TASK_121_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_121_DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_ONLY=true" in text
    assert "MILESTONE_19_TASK_121_CLOSURE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_121_CLOSURE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_121_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_121_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_121_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_121_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_121_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_121_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_121_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_121_NEXT_STAGE=MILESTONE_19_TASK_122_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTATION_REVIEW_V1" in text


def test_task_121_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_121_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_READY"
    assert manifest["mode"] == "LOCAL_DIAGNOSTIC_ONLY_CLOSURE_FINALIZATION_NO_RUNTIME_WIRING"
    assert manifest["controlledSmokeRunResultArchiveClosureFinalizationImplemented"] is True
    assert manifest["diagnosticSmokeRunResultArchiveClosureFinalizationOnly"] is True
    assert manifest["closureModified"] is False
    assert manifest["closureModuleModified"] is False
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


def test_task_121_static_finalization_artifact() -> None:
    payload = json.loads(FINALIZATION_JSON.read_text(encoding="utf-8"))
    assert payload["finalizationId"].startswith("SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-FINALIZATION-")
    assert payload["finalizationOk"] is True
    assert payload["sourceArchivedCaseCount"] == 8
    assert payload["sourceArchivedPassedCount"] == 8
    assert payload["sourceArchivedFailedCount"] == 0
    assert payload["validationIssues"] == []
    assert payload["closureModified"] is False
    assert payload["closureModuleModified"] is False
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
