"""Milestone #19 Task 123 - SRSC smoke-run result archive closure final chain closure planning validation."""

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
    finalize_controlled_smoke_run_result_archive_closure,
    validate_controlled_smoke_run_result_archive_closure_finalization,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_122 = ROOT / "docs" / "milestone-19-task-122-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-implementation-review-v1.md"
DOC_TASK_123 = ROOT / "docs" / "milestone-19-task-123-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-planning-v1.md"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-planning-v1" / "task-123-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-planning-v1" / "task-123-index.txt"
FINALIZATION_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-finalization-local-implementation-v1" / "task-121-smoke-run-result-archive-closure-finalization.json"


def test_task_123_required_files_exist() -> None:
    assert DOC_TASK_122.exists()
    assert DOC_TASK_123.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert FINALIZATION_JSON.exists()


def test_task_123_dependency_markers() -> None:
    text = DOC_TASK_122.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_122_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_122_DECISION=ACCEPT_TASK_121_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_122_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_122_CLOSURE_FINALIZATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_122_CLOSURE_FINALIZATION_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_122_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_122_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_122_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_122_LEGAL_CERTIFICATION=false" in text


def test_task_123_finalization_still_valid_for_final_chain_planning() -> None:
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    finalization = finalize_controlled_smoke_run_result_archive_closure(closure)

    assert finalization.finalization_ok is True
    assert finalization.source_archived_case_count == 8
    assert finalization.source_archived_passed_count == 8
    assert finalization.source_archived_failed_count == 0
    assert validate_controlled_smoke_run_result_archive_closure_finalization(finalization) == ()


def test_task_123_static_finalization_artifact_is_public_safe() -> None:
    payload = json.loads(FINALIZATION_JSON.read_text(encoding="utf-8"))
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
    assert payload["failClosedActive"] is True


def test_task_123_canonical_markers() -> None:
    text = DOC_TASK_123.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_123_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_123_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_PLANNING_READY" in text
    assert "MILESTONE_19_TASK_123_MODE=PLANNING_ONLY_NO_FINAL_CHAIN_CLOSURE_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_123_DECISION=PLAN_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_ONLY" in text
    assert "MILESTONE_19_TASK_123_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_PLANNING_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_123_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_AUTHORIZATION_REVIEW_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_123_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_123_FINAL_CHAIN_CLOSURE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_123_CLOSURE_FINALIZATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_123_CLOSURE_FINALIZATION_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_123_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_123_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_123_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_123_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_123_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_123_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_123_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_123_NEXT_STAGE=MILESTONE_19_TASK_124_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_AUTHORIZATION_REVIEW_V1" in text


def test_task_123_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_123_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_PLANNING_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_PLANNING_READY"
    assert manifest["mode"] == "PLANNING_ONLY_NO_FINAL_CHAIN_CLOSURE_IMPLEMENTATION"
    assert manifest["decision"] == "PLAN_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_ONLY"
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosurePlanningPerformed"] is True
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosureAuthorizationReviewRequiredNext"] is True
    assert manifest["implementationPerformedInTask123"] is False
    assert manifest["finalChainClosureImplemented"] is False
    assert manifest["closureFinalizationModified"] is False
    assert manifest["closureFinalizationModuleModified"] is False
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
    assert manifest["coveredTaskRange"] == "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"
