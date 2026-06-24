"""Milestone #19 Task 120 - SRSC smoke-run result archive closure finalization authorization review validation."""

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
    validate_controlled_smoke_run_result_archive_closure,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_119 = ROOT / "docs" / "milestone-19-task-119-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-planning-v1.md"
DOC_TASK_120 = ROOT / "docs" / "milestone-19-task-120-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-authorization-review-v1.md"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-authorization-review-v1" / "task-120-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-authorization-review-v1" / "task-120-index.txt"
CLOSURE_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-local-implementation-v1" / "task-117-smoke-run-result-archive-closure.json"


def test_task_120_required_files_exist() -> None:
    assert DOC_TASK_119.exists()
    assert DOC_TASK_120.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert CLOSURE_JSON.exists()


def test_task_120_dependency_markers() -> None:
    text = DOC_TASK_119.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_119_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_119_DECISION=PLAN_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_ONLY" in text
    assert "MILESTONE_19_TASK_119_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_AUTHORIZATION_REVIEW_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_119_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_119_CLOSURE_FINALIZATION_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_119_ARCHIVE_CLOSURE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_119_ARCHIVE_CLOSURE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_119_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_119_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_119_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_119_LEGAL_CERTIFICATION=false" in text


def test_task_120_closure_still_valid_for_authorization_review() -> None:
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    assert closure.closure_ok is True
    assert closure.source_archived_case_count == 8
    assert closure.source_archived_passed_count == 8
    assert closure.source_archived_failed_count == 0
    assert validate_controlled_smoke_run_result_archive_closure(closure) == ()


def test_task_120_static_closure_artifact_is_public_safe() -> None:
    payload = json.loads(CLOSURE_JSON.read_text(encoding="utf-8"))
    assert payload["closureOk"] is True
    assert payload["validationIssues"] == []
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


def test_task_120_canonical_markers() -> None:
    text = DOC_TASK_120.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_120_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_120_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_AUTHORIZATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_120_MODE=REVIEW_ONLY_NO_CLOSURE_FINALIZATION_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_120_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_120_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_120_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_120_CLOSURE_FINALIZATION_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_120_ARCHIVE_CLOSURE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_120_ARCHIVE_CLOSURE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_120_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_120_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_120_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_120_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_120_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_120_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_120_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_120_NEXT_STAGE=MILESTONE_19_TASK_121_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_V1" in text


def test_task_120_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_120_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_AUTHORIZATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_AUTHORIZATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_CLOSURE_FINALIZATION_IMPLEMENTATION"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_ONLY"
    assert manifest["controlledSmokeRunResultArchiveClosureFinalizationAuthorizationReviewPerformed"] is True
    assert manifest["controlledSmokeRunResultArchiveClosureFinalizationLocalImplementationAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask120"] is False
    assert manifest["closureFinalizationImplemented"] is False
    assert manifest["archiveClosureModified"] is False
    assert manifest["archiveClosureModuleModified"] is False
    assert manifest["resultArchiveModified"] is False
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
    assert "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_finalization.py" in manifest["authorizedFutureModules"]
