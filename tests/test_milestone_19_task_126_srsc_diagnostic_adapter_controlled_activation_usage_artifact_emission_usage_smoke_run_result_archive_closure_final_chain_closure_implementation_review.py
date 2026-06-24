"""Milestone #19 Task 126 - SRSC final-chain closure implementation review validation."""

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
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTED,
    COVERED_TASK_RANGE,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_ONLY,
    FINAL_CHAIN_CLOSURE_REVISION,
    TASK_ID as TASK_125_ID,
    close_controlled_smoke_run_result_archive_closure_final_chain,
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_125 = ROOT / "docs" / "milestone-19-task-125-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-local-implementation-v1.md"
DOC_TASK_126 = ROOT / "docs" / "milestone-19-task-126-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-implementation-review-v1.md"
FINAL_CHAIN_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure.py"
FINAL_CHAIN_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure.py"
TASK_125_TEST = ROOT / "tests" / "test_milestone_19_task_125_srsc_diagnostic_adapter_controlled_activation_usage_artifact_emission_usage_smoke_run_result_archive_closure_final_chain_closure_local_implementation.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-implementation-review-v1" / "task-126-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-implementation-review-v1" / "task-126-index.txt"
FINAL_CHAIN_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-local-implementation-v1" / "task-125-smoke-run-result-archive-closure-final-chain-closure.json"
FINAL_CHAIN_MD = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-local-implementation-v1" / "task-125-smoke-run-result-archive-closure-final-chain-closure.md"


def _build_final_chain_closure():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    finalization = finalize_controlled_smoke_run_result_archive_closure(closure)
    return close_controlled_smoke_run_result_archive_closure_final_chain(finalization)


def test_task_126_required_files_exist() -> None:
    assert DOC_TASK_125.exists()
    assert DOC_TASK_126.exists()
    assert FINAL_CHAIN_MODULE.exists()
    assert FINAL_CHAIN_TEST.exists()
    assert TASK_125_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert FINAL_CHAIN_JSON.exists()
    assert FINAL_CHAIN_MD.exists()


def test_task_126_dependency_markers() -> None:
    text = DOC_TASK_125.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_125_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_125_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_125_DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_ONLY=true" in text
    assert "MILESTONE_19_TASK_125_CLOSURE_FINALIZATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_125_CLOSURE_FINALIZATION_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_125_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_125_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_125_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_125_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_125_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_125_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_125_NEXT_STAGE=MILESTONE_19_TASK_126_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTATION_REVIEW_V1" in text


def test_task_126_final_chain_contract_review() -> None:
    final_chain = _build_final_chain_closure()
    assert TASK_125_ID == "MILESTONE_19_TASK_125_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_IMPLEMENTATION_V1"
    assert FINAL_CHAIN_CLOSURE_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_V1"
    assert final_chain.final_chain_closure_ok is True
    assert final_chain.source_archived_case_count == 8
    assert final_chain.source_archived_passed_count == 8
    assert final_chain.source_archived_failed_count == 0
    assert final_chain.plan.covered_task_range == COVERED_TASK_RANGE
    assert len(final_chain.chain_coverage_tasks) == 16
    assert final_chain.chain_coverage_tasks[0] == "MILESTONE_19_TASK_107"
    assert final_chain.chain_coverage_tasks[-1] == "MILESTONE_19_TASK_122"
    assert validate_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain) == ()
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_ONLY is True


def test_task_126_static_final_chain_artifact_review() -> None:
    payload = json.loads(FINAL_CHAIN_JSON.read_text(encoding="utf-8"))
    assert payload["finalChainClosureId"].startswith("SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-FINAL-CHAIN-CLOSURE-")
    assert payload["finalChainClosureOk"] is True
    assert payload["sourceArchivedCaseCount"] == 8
    assert payload["sourceArchivedPassedCount"] == 8
    assert payload["sourceArchivedFailedCount"] == 0
    assert payload["validationIssues"] == []
    assert payload["coveredTaskRange"] == "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"
    assert payload["chainCoverageTaskCount"] == 16
    assert payload["closureFinalizationModified"] is False
    assert payload["closureFinalizationModuleModified"] is False
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
    assert payload["pocV09RuntimeImplemented"] is False
    assert payload["pocV09Benchmarked"] is False
    assert payload["pocV09FaultInjectionPerformed"] is False
    assert payload["pocV09ProductionReady"] is False


def test_task_126_canonical_markers() -> None:
    text = DOC_TASK_126.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_126_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_126_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_126_MODE=REVIEW_ONLY_NO_FINAL_CHAIN_CLOSURE_MODIFICATION" in text
    assert "MILESTONE_19_TASK_126_DECISION=ACCEPT_TASK_125_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_126_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_126_TASK_125_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTATION_ACCEPTED=true" in text
    assert "MILESTONE_19_TASK_126_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_126_FINAL_CHAIN_CLOSURE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_126_FINAL_CHAIN_CLOSURE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_126_CLOSURE_FINALIZATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_126_CLOSURE_FINALIZATION_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_126_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_126_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_126_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_126_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_126_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_126_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_126_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_126_NEXT_STAGE=MILESTONE_19_TASK_127_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_PLANNING_V1" in text


def test_task_126_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_126_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_FINAL_CHAIN_CLOSURE_MODIFICATION"
    assert manifest["decision"] == "ACCEPT_TASK_125_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_IMPLEMENTATION"
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosureImplementationReviewPerformed"] is True
    assert manifest["task125SmokeRunResultArchiveClosureFinalChainClosureImplementationAccepted"] is True
    assert manifest["implementationPerformedInTask126"] is False
    assert manifest["finalChainClosureModified"] is False
    assert manifest["finalChainClosureModuleModified"] is False
    assert manifest["closureFinalizationModified"] is False
    assert manifest["closureFinalizationModuleModified"] is False
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
