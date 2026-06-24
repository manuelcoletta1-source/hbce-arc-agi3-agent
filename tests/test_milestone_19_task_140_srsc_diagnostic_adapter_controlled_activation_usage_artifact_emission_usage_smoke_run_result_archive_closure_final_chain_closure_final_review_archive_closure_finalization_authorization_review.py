"""Milestone #19 Task 140 - SRSC final review archive closure finalization authorization validation."""

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
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure import (
    close_controlled_smoke_run_result_archive_closure_final_chain,
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review import (
    review_controlled_smoke_run_result_archive_closure_final_chain_closure,
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive import (
    archive_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review,
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure import (
    close_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive,
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_139 = ROOT / "docs" / "milestone-19-task-139-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-finalization-planning-v1.md"
DOC_TASK_140 = ROOT / "docs" / "milestone-19-task-140-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-finalization-authorization-review-v1.md"
CLOSURE_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure.py"
CLOSURE_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-finalization-authorization-review-v1" / "task-140-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-finalization-authorization-review-v1" / "task-140-index.txt"
CLOSURE_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-local-implementation-v1" / "task-137-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure.json"


def _build_closure():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    finalization = finalize_controlled_smoke_run_result_archive_closure(closure)
    final_chain = close_controlled_smoke_run_result_archive_closure_final_chain(finalization)
    final_review = review_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain)
    final_review_archive = archive_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review(final_review)
    return close_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive(final_review_archive)


def test_task_140_required_files_exist() -> None:
    assert DOC_TASK_139.exists()
    assert DOC_TASK_140.exists()
    assert CLOSURE_MODULE.exists()
    assert CLOSURE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert CLOSURE_JSON.exists()


def test_task_140_dependency_markers() -> None:
    text = DOC_TASK_139.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_139_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_139_DECISION=PLAN_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_ONLY" in text
    assert "MILESTONE_19_TASK_139_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_AUTHORIZATION_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_139_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_139_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_139_FINAL_REVIEW_ARCHIVE_CLOSURE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_139_FINAL_REVIEW_ARCHIVE_CLOSURE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_139_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_139_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_139_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_139_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_139_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_139_LEGAL_CERTIFICATION=false" in text


def test_task_140_closure_still_valid_for_finalization_authorization() -> None:
    closure = _build_closure()
    assert closure.final_review_archive_closure_ok is True
    assert closure.source_final_review_archive_ok is True
    assert closure.source_final_review_ok is True
    assert closure.source_archived_case_count == 8
    assert closure.source_archived_passed_count == 8
    assert closure.source_archived_failed_count == 0
    assert len(closure.chain_coverage_tasks) == 16
    assert closure.chain_coverage_tasks[0] == "MILESTONE_19_TASK_107"
    assert closure.chain_coverage_tasks[-1] == "MILESTONE_19_TASK_122"
    assert validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure(closure) == ()


def test_task_140_static_closure_artifact_is_public_safe() -> None:
    payload = json.loads(CLOSURE_JSON.read_text(encoding="utf-8"))
    assert payload["finalReviewArchiveClosureOk"] is True
    assert payload["sourceFinalReviewArchiveOk"] is True
    assert payload["sourceFinalReviewOk"] is True
    assert payload["sourceArchivedCaseCount"] == 8
    assert payload["sourceArchivedPassedCount"] == 8
    assert payload["sourceArchivedFailedCount"] == 0
    assert payload["validationIssues"] == []
    assert payload["coveredTaskRange"] == "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"
    assert payload["chainCoverageTaskCount"] == 16
    assert payload["finalReviewArchiveClosureLocalOnly"] is True
    assert payload["finalReviewArchiveClosureTechnicalContinuityEvidenceOnly"] is True
    assert payload["finalReviewArchiveClosureModifiesSourceArchive"] is False
    assert payload["finalReviewArchiveClosureModifiesSourceFinalReview"] is False
    assert payload["finalReviewArchiveClosureModifiesSourceFinalChainClosure"] is False
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


def test_task_140_canonical_markers() -> None:
    text = DOC_TASK_140.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_140_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_140_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_AUTHORIZATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_140_MODE=AUTHORIZATION_REVIEW_ONLY_NO_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_140_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_140_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_AUTHORIZATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_140_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_140_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_140_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_140_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_140_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_140_FINAL_REVIEW_ARCHIVE_CLOSURE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_140_FINAL_REVIEW_ARCHIVE_CLOSURE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_140_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_140_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_140_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_140_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_140_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_140_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_140_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_140_NEXT_STAGE=MILESTONE_19_TASK_141_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_V1" in text


def test_task_140_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_140_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_AUTHORIZATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_AUTHORIZATION_REVIEW_READY"
    assert manifest["mode"] == "AUTHORIZATION_REVIEW_ONLY_NO_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTATION"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_ONLY"
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveClosureFinalizationAuthorizationReviewPerformed"] is True
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveClosureFinalizationLocalImplementationAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask140"] is False
    assert manifest["finalReviewArchiveClosureFinalizationImplemented"] is False
    assert manifest["finalReviewArchiveClosureFinalizationModified"] is False
    assert manifest["finalReviewArchiveClosureFinalizationModuleModified"] is False
    assert manifest["finalReviewArchiveClosureModified"] is False
    assert manifest["finalReviewArchiveClosureModuleModified"] is False
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
    assert manifest["coveredTaskRange"] == "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"
    assert "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure_finalization.py" in manifest["authorizedFutureModules"]
