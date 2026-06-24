"""Milestone #19 Task 131 - SRSC final review archive planning validation."""

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
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_130 = ROOT / "docs" / "milestone-19-task-130-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-implementation-review-v1.md"
DOC_TASK_131 = ROOT / "docs" / "milestone-19-task-131-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-planning-v1.md"
FINAL_REVIEW_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review.py"
FINAL_REVIEW_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-planning-v1" / "task-131-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-planning-v1" / "task-131-index.txt"
FINAL_REVIEW_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-local-implementation-v1" / "task-129-smoke-run-result-archive-closure-final-chain-closure-final-review.json"


def _build_final_review():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    finalization = finalize_controlled_smoke_run_result_archive_closure(closure)
    final_chain = close_controlled_smoke_run_result_archive_closure_final_chain(finalization)
    return review_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain)


def test_task_131_required_files_exist() -> None:
    assert DOC_TASK_130.exists()
    assert DOC_TASK_131.exists()
    assert FINAL_REVIEW_MODULE.exists()
    assert FINAL_REVIEW_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert FINAL_REVIEW_JSON.exists()


def test_task_131_dependency_markers() -> None:
    text = DOC_TASK_130.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_130_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_130_DECISION=ACCEPT_TASK_129_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_LOCAL_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_130_TASK_129_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_IMPLEMENTATION_ACCEPTED=true" in text
    assert "MILESTONE_19_TASK_130_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_130_FINAL_REVIEW_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_130_FINAL_REVIEW_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_130_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_130_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_130_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_130_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_130_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_130_LEGAL_CERTIFICATION=false" in text


def test_task_131_final_review_still_valid_for_archive_planning() -> None:
    final_review = _build_final_review()
    assert final_review.final_review_ok is True
    assert final_review.source_final_chain_closure_ok is True
    assert final_review.source_archived_case_count == 8
    assert final_review.source_archived_passed_count == 8
    assert final_review.source_archived_failed_count == 0
    assert len(final_review.chain_coverage_tasks) == 16
    assert final_review.chain_coverage_tasks[0] == "MILESTONE_19_TASK_107"
    assert final_review.chain_coverage_tasks[-1] == "MILESTONE_19_TASK_122"
    assert validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review(final_review) == ()


def test_task_131_static_final_review_artifact_is_public_safe() -> None:
    payload = json.loads(FINAL_REVIEW_JSON.read_text(encoding="utf-8"))
    assert payload["finalReviewOk"] is True
    assert payload["sourceFinalChainClosureOk"] is True
    assert payload["sourceArchivedCaseCount"] == 8
    assert payload["sourceArchivedPassedCount"] == 8
    assert payload["sourceArchivedFailedCount"] == 0
    assert payload["validationIssues"] == []
    assert payload["coveredTaskRange"] == "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"
    assert payload["chainCoverageTaskCount"] == 16
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


def test_task_131_canonical_markers() -> None:
    text = DOC_TASK_131.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_131_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_131_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_PLANNING_READY" in text
    assert "MILESTONE_19_TASK_131_MODE=PLANNING_ONLY_NO_FINAL_REVIEW_ARCHIVE_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_131_DECISION=PLAN_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_ONLY" in text
    assert "MILESTONE_19_TASK_131_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_PLANNING_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_131_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_AUTHORIZATION_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_131_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_131_FINAL_REVIEW_ARCHIVE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_131_FINAL_REVIEW_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_131_FINAL_REVIEW_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_131_FINAL_CHAIN_CLOSURE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_131_FINAL_CHAIN_CLOSURE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_131_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_131_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_131_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_131_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_131_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_131_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_131_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_131_NEXT_STAGE=MILESTONE_19_TASK_132_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_AUTHORIZATION_REVIEW_V1" in text


def test_task_131_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_131_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_PLANNING_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_PLANNING_READY"
    assert manifest["mode"] == "PLANNING_ONLY_NO_FINAL_REVIEW_ARCHIVE_IMPLEMENTATION"
    assert manifest["decision"] == "PLAN_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_ONLY"
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchivePlanningPerformed"] is True
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveAuthorizationRequiredNext"] is True
    assert manifest["implementationPerformedInTask131"] is False
    assert manifest["finalReviewArchiveImplemented"] is False
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
