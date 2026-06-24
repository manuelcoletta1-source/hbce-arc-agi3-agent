"""Milestone #19 Task 122 - SRSC smoke-run result archive closure finalization implementation review validation."""

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
    TASK_ID as TASK_121_ID,
    finalize_controlled_smoke_run_result_archive_closure,
    validate_controlled_smoke_run_result_archive_closure_finalization,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_121 = ROOT / "docs" / "milestone-19-task-121-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-local-implementation-v1.md"
DOC_TASK_122 = ROOT / "docs" / "milestone-19-task-122-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-implementation-review-v1.md"
FINALIZATION_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_finalization.py"
FINALIZATION_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_finalization.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-implementation-review-v1" / "task-122-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-implementation-review-v1" / "task-122-index.txt"
FINALIZATION_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-local-implementation-v1" / "task-121-smoke-run-result-archive-closure-finalization.json"
FINALIZATION_MD = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-local-implementation-v1" / "task-121-smoke-run-result-archive-closure-finalization.md"


def _build_finalization():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    return finalize_controlled_smoke_run_result_archive_closure(closure)


def test_task_122_required_files_exist() -> None:
    assert DOC_TASK_121.exists()
    assert DOC_TASK_122.exists()
    assert FINALIZATION_MODULE.exists()
    assert FINALIZATION_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert FINALIZATION_JSON.exists()
    assert FINALIZATION_MD.exists()


def test_task_122_dependency_markers() -> None:
    text = DOC_TASK_121.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_121_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_READY=true" in text
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
    assert "MILESTONE_19_TASK_121_NEXT_STAGE=MILESTONE_19_TASK_122_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTATION_REVIEW_V1" in text


def test_task_122_finalization_contract_review() -> None:
    finalization = _build_finalization()
    assert TASK_121_ID == "MILESTONE_19_TASK_121_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_V1"
    assert FINALIZATION_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_V1"
    assert finalization.finalization_ok is True
    assert finalization.source_archived_case_count == 8
    assert finalization.source_archived_passed_count == 8
    assert finalization.source_archived_failed_count == 0
    assert validate_controlled_smoke_run_result_archive_closure_finalization(finalization) == ()
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_ONLY is True


def test_task_122_static_finalization_artifact_review() -> None:
    payload = json.loads(FINALIZATION_JSON.read_text(encoding="utf-8"))
    assert payload["finalizationId"].startswith("SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-FINALIZATION-")
    assert payload["finalizationOk"] is True
    assert payload["sourceArchivedCaseCount"] == 8
    assert payload["sourceArchivedPassedCount"] == 8
    assert payload["sourceArchivedFailedCount"] == 0
    assert payload["validationIssues"] == []
    assert payload["closureModified"] is False
    assert payload["closureModuleModified"] is False
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


def test_task_122_canonical_markers() -> None:
    text = DOC_TASK_122.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_122_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_122_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_122_MODE=REVIEW_ONLY_NO_CLOSURE_FINALIZATION_MODIFICATION" in text
    assert "MILESTONE_19_TASK_122_DECISION=ACCEPT_TASK_121_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_122_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_122_CLOSURE_FINALIZATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_122_CLOSURE_FINALIZATION_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_122_CLOSURE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_122_CLOSURE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_122_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_122_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_122_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_122_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_122_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_122_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_122_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_122_NEXT_STAGE=MILESTONE_19_TASK_123_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_PLANNING_V1" in text


def test_task_122_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_122_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_CLOSURE_FINALIZATION_MODIFICATION"
    assert manifest["decision"] == "ACCEPT_TASK_121_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION"
    assert manifest["controlledSmokeRunResultArchiveClosureFinalizationImplementationReviewPerformed"] is True
    assert manifest["task121SmokeRunResultArchiveClosureFinalizationImplementationAccepted"] is True
    assert manifest["implementationPerformedInTask122"] is False
    assert manifest["closureFinalizationModified"] is False
    assert manifest["closureFinalizationModuleModified"] is False
    assert manifest["closureModified"] is False
    assert manifest["closureModuleModified"] is False
    assert manifest["runtimeSolverModified"] is False
    assert manifest["runtimeWiringAllowed"] is False
    assert manifest["kaggleSubmissionSent"] is False
    assert manifest["privateCoreExposure"] is False
    assert manifest["rawRequestBodyPersisted"] is False
    assert manifest["secretPersisted"] is False
    assert manifest["legalCertification"] is False
    assert manifest["failClosedActive"] is True
    assert manifest["pocV09RuntimeImplemented"] is False
    assert manifest["pocV09Benchmarked"] is False
    assert manifest["pocV09FaultInjectionPerformed"] is False
    assert manifest["pocV09ProductionReady"] is False
