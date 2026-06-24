"""Milestone #19 Task 125 - SRSC smoke-run result archive closure final-chain closure local implementation validation."""

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
    TASK_ID,
    close_controlled_smoke_run_result_archive_closure_final_chain,
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_124 = ROOT / "docs" / "milestone-19-task-124-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-authorization-review-v1.md"
DOC_TASK_125 = ROOT / "docs" / "milestone-19-task-125-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-local-implementation-v1.md"
FINAL_CHAIN_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure.py"
FINAL_CHAIN_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-local-implementation-v1" / "task-125-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-local-implementation-v1" / "task-125-index.txt"
FINAL_CHAIN_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-local-implementation-v1" / "task-125-smoke-run-result-archive-closure-final-chain-closure.json"
FINAL_CHAIN_MD = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-local-implementation-v1" / "task-125-smoke-run-result-archive-closure-final-chain-closure.md"


def _build_final_chain_closure():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    finalization = finalize_controlled_smoke_run_result_archive_closure(closure)
    return close_controlled_smoke_run_result_archive_closure_final_chain(finalization)


def test_task_125_required_files_exist() -> None:
    assert DOC_TASK_124.exists()
    assert DOC_TASK_125.exists()
    assert FINAL_CHAIN_MODULE.exists()
    assert FINAL_CHAIN_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert FINAL_CHAIN_JSON.exists()
    assert FINAL_CHAIN_MD.exists()


def test_task_125_dependency_markers() -> None:
    text = DOC_TASK_124.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_124_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_124_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_124_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_124_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_124_FINAL_CHAIN_CLOSURE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_124_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_124_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_124_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_124_LEGAL_CERTIFICATION=false" in text


def test_task_125_final_chain_closure_contract() -> None:
    final_chain = _build_final_chain_closure()
    assert TASK_ID == "MILESTONE_19_TASK_125_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_IMPLEMENTATION_V1"
    assert FINAL_CHAIN_CLOSURE_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_V1"
    assert final_chain.final_chain_closure_ok is True
    assert final_chain.source_archived_case_count == 8
    assert final_chain.source_archived_passed_count == 8
    assert final_chain.source_archived_failed_count == 0
    assert final_chain.plan.covered_task_range == COVERED_TASK_RANGE
    assert len(final_chain.chain_coverage_tasks) == 16
    assert validate_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain) == ()
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_ONLY is True


def test_task_125_canonical_markers() -> None:
    text = DOC_TASK_125.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_125_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_125_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_IMPLEMENTATION_READY" in text
    assert "MILESTONE_19_TASK_125_MODE=LOCAL_DIAGNOSTIC_ONLY_FINAL_CHAIN_CLOSURE_NO_RUNTIME_WIRING" in text
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
    assert "MILESTONE_19_TASK_125_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_125_NEXT_STAGE=MILESTONE_19_TASK_126_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTATION_REVIEW_V1" in text


def test_task_125_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_125_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_IMPLEMENTATION_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_IMPLEMENTATION_READY"
    assert manifest["mode"] == "LOCAL_DIAGNOSTIC_ONLY_FINAL_CHAIN_CLOSURE_NO_RUNTIME_WIRING"
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosureImplemented"] is True
    assert manifest["diagnosticSmokeRunResultArchiveClosureFinalChainClosureOnly"] is True
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
    assert manifest["coveredTaskRange"] == "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"


def test_task_125_static_final_chain_closure_artifact() -> None:
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
