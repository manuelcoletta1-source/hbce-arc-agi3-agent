"""Milestone #19 Task 135 - SRSC final review archive closure planning validation."""

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
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_134 = ROOT / "docs" / "milestone-19-task-134-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-implementation-review-v1.md"
DOC_TASK_135 = ROOT / "docs" / "milestone-19-task-135-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-planning-v1.md"
ARCHIVE_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive.py"
ARCHIVE_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-planning-v1" / "task-135-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-planning-v1" / "task-135-index.txt"
ARCHIVE_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-local-implementation-v1" / "task-133-smoke-run-result-archive-closure-final-chain-closure-final-review-archive.json"


def _build_archive():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    finalization = finalize_controlled_smoke_run_result_archive_closure(closure)
    final_chain = close_controlled_smoke_run_result_archive_closure_final_chain(finalization)
    final_review = review_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain)
    return archive_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review(final_review)


def test_task_135_required_files_exist() -> None:
    assert DOC_TASK_134.exists()
    assert DOC_TASK_135.exists()
    assert ARCHIVE_MODULE.exists()
    assert ARCHIVE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert ARCHIVE_JSON.exists()


def test_task_135_dependency_markers() -> None:
    text = DOC_TASK_134.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_134_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_134_DECISION=ACCEPT_TASK_133_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_LOCAL_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_134_TASK_133_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_IMPLEMENTATION_ACCEPTED=true" in text
    assert "MILESTONE_19_TASK_134_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_134_FINAL_REVIEW_ARCHIVE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_134_FINAL_REVIEW_ARCHIVE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_134_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_134_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_134_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_134_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_134_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_134_LEGAL_CERTIFICATION=false" in text


def test_task_135_archive_still_valid_for_closure_planning() -> None:
    archive = _build_archive()
    assert archive.final_review_archive_ok is True
    assert archive.source_final_review_ok is True
    assert archive.source_archived_case_count == 8
    assert archive.source_archived_passed_count == 8
    assert archive.source_archived_failed_count == 0
    assert len(archive.chain_coverage_tasks) == 16
    assert archive.chain_coverage_tasks[0] == "MILESTONE_19_TASK_107"
    assert archive.chain_coverage_tasks[-1] == "MILESTONE_19_TASK_122"
    assert validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive(archive) == ()


def test_task_135_static_archive_artifact_is_public_safe() -> None:
    payload = json.loads(ARCHIVE_JSON.read_text(encoding="utf-8"))
    assert payload["finalReviewArchiveOk"] is True
    assert payload["sourceFinalReviewOk"] is True
    assert payload["sourceArchivedCaseCount"] == 8
    assert payload["sourceArchivedPassedCount"] == 8
    assert payload["sourceArchivedFailedCount"] == 0
    assert payload["validationIssues"] == []
    assert payload["coveredTaskRange"] == "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"
    assert payload["chainCoverageTaskCount"] == 16
    assert payload["finalReviewArchiveLocalOnly"] is True
    assert payload["finalReviewArchiveTechnicalContinuityEvidenceOnly"] is True
    assert payload["finalReviewArchiveModifiesSourceFinalReview"] is False
    assert payload["finalReviewArchiveModifiesSourceFinalChainClosure"] is False
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


def test_task_135_canonical_markers() -> None:
    text = DOC_TASK_135.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_135_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_135_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_PLANNING_READY" in text
    assert "MILESTONE_19_TASK_135_MODE=PLANNING_ONLY_NO_FINAL_REVIEW_ARCHIVE_CLOSURE_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_135_DECISION=PLAN_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_ONLY" in text
    assert "MILESTONE_19_TASK_135_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_PLANNING_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_135_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_AUTHORIZATION_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_135_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_135_FINAL_REVIEW_ARCHIVE_CLOSURE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_135_FINAL_REVIEW_ARCHIVE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_135_FINAL_REVIEW_ARCHIVE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_135_FINAL_REVIEW_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_135_FINAL_REVIEW_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_135_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_135_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_135_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_135_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_135_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_135_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_135_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_135_NEXT_STAGE=MILESTONE_19_TASK_136_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_AUTHORIZATION_REVIEW_V1" in text


def test_task_135_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_135_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_PLANNING_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_PLANNING_READY"
    assert manifest["mode"] == "PLANNING_ONLY_NO_FINAL_REVIEW_ARCHIVE_CLOSURE_IMPLEMENTATION"
    assert manifest["decision"] == "PLAN_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_ONLY"
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveClosurePlanningPerformed"] is True
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveClosureAuthorizationRequiredNext"] is True
    assert manifest["implementationPerformedInTask135"] is False
    assert manifest["finalReviewArchiveClosureImplemented"] is False
    assert manifest["finalReviewArchiveModified"] is False
    assert manifest["finalReviewArchiveModuleModified"] is False
    assert manifest["finalReviewModified"] is False
    assert manifest["finalReviewModuleModified"] is False
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
