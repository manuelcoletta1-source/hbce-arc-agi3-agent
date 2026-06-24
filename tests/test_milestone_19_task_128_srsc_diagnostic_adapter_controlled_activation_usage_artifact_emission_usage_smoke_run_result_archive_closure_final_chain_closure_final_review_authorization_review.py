"""Milestone #19 Task 128 - SRSC final-chain closure final review authorization validation."""

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
    COVERED_TASK_RANGE,
    close_controlled_smoke_run_result_archive_closure_final_chain,
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_127 = ROOT / "docs" / "milestone-19-task-127-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-planning-v1.md"
DOC_TASK_128 = ROOT / "docs" / "milestone-19-task-128-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-authorization-review-v1.md"
FINAL_CHAIN_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure.py"
FINAL_CHAIN_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-authorization-review-v1" / "task-128-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-authorization-review-v1" / "task-128-index.txt"
FINAL_CHAIN_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-local-implementation-v1" / "task-125-smoke-run-result-archive-closure-final-chain-closure.json"


def _build_final_chain_closure():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    finalization = finalize_controlled_smoke_run_result_archive_closure(closure)
    return close_controlled_smoke_run_result_archive_closure_final_chain(finalization)


def test_task_128_required_files_exist() -> None:
    assert DOC_TASK_127.exists()
    assert DOC_TASK_128.exists()
    assert FINAL_CHAIN_MODULE.exists()
    assert FINAL_CHAIN_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert FINAL_CHAIN_JSON.exists()


def test_task_128_dependency_markers() -> None:
    text = DOC_TASK_127.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_127_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_127_DECISION=PLAN_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ONLY" in text
    assert "MILESTONE_19_TASK_127_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_AUTHORIZATION_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_127_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_127_FINAL_REVIEW_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_127_FINAL_CHAIN_CLOSURE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_127_FINAL_CHAIN_CLOSURE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_127_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_127_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_127_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_127_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_127_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_127_LEGAL_CERTIFICATION=false" in text


def test_task_128_final_chain_closure_still_valid_for_authorization_review() -> None:
    final_chain = _build_final_chain_closure()
    assert final_chain.final_chain_closure_ok is True
    assert final_chain.source_archived_case_count == 8
    assert final_chain.source_archived_passed_count == 8
    assert final_chain.source_archived_failed_count == 0
    assert final_chain.plan.covered_task_range == COVERED_TASK_RANGE
    assert len(final_chain.chain_coverage_tasks) == 16
    assert final_chain.chain_coverage_tasks[0] == "MILESTONE_19_TASK_107"
    assert final_chain.chain_coverage_tasks[-1] == "MILESTONE_19_TASK_122"
    assert validate_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain) == ()


def test_task_128_static_final_chain_artifact_is_public_safe() -> None:
    payload = json.loads(FINAL_CHAIN_JSON.read_text(encoding="utf-8"))
    assert payload["finalChainClosureOk"] is True
    assert payload["validationIssues"] == []
    assert payload["coveredTaskRange"] == "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"
    assert payload["chainCoverageTaskCount"] == 16
    assert payload["sourceArchivedCaseCount"] == 8
    assert payload["sourceArchivedPassedCount"] == 8
    assert payload["sourceArchivedFailedCount"] == 0
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
    assert payload["pocV09RuntimeImplemented"] is False
    assert payload["pocV09Benchmarked"] is False
    assert payload["pocV09FaultInjectionPerformed"] is False
    assert payload["pocV09ProductionReady"] is False


def test_task_128_canonical_markers() -> None:
    text = DOC_TASK_128.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_128_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_128_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_AUTHORIZATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_128_MODE=AUTHORIZATION_REVIEW_ONLY_NO_FINAL_REVIEW_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_128_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_LOCAL_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_128_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_AUTHORIZATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_128_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_LOCAL_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_128_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_128_FINAL_REVIEW_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_128_FINAL_CHAIN_CLOSURE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_128_FINAL_CHAIN_CLOSURE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_128_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_128_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_128_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_128_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_128_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_128_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_128_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_128_NEXT_STAGE=MILESTONE_19_TASK_129_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_LOCAL_IMPLEMENTATION_V1" in text


def test_task_128_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_128_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_AUTHORIZATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_AUTHORIZATION_REVIEW_READY"
    assert manifest["mode"] == "AUTHORIZATION_REVIEW_ONLY_NO_FINAL_REVIEW_IMPLEMENTATION"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_LOCAL_IMPLEMENTATION_ONLY"
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewAuthorizationReviewPerformed"] is True
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewLocalImplementationAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask128"] is False
    assert manifest["finalReviewImplemented"] is False
    assert manifest["finalChainClosureModified"] is False
    assert manifest["finalChainClosureModuleModified"] is False
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
    assert "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review.py" in manifest["authorizedFutureModules"]
