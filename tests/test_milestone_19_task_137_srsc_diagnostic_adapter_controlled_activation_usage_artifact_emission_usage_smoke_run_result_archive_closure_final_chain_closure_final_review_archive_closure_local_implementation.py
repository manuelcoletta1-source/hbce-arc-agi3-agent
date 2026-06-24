"""Milestone #19 Task 137 - SRSC final review archive closure local implementation validation."""

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
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_IMPLEMENTED,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_ONLY,
    FINAL_REVIEW_ARCHIVE_CLOSURE_REVISION,
    TASK_ID,
    close_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive,
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_136 = ROOT / "docs" / "milestone-19-task-136-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-authorization-review-v1.md"
DOC_TASK_137 = ROOT / "docs" / "milestone-19-task-137-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-local-implementation-v1.md"
CLOSURE_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure.py"
CLOSURE_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-local-implementation-v1" / "task-137-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-local-implementation-v1" / "task-137-index.txt"
CLOSURE_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-local-implementation-v1" / "task-137-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure.json"
CLOSURE_MD = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-local-implementation-v1" / "task-137-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure.md"


def _build_closure():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    finalization = finalize_controlled_smoke_run_result_archive_closure(closure)
    final_chain = close_controlled_smoke_run_result_archive_closure_final_chain(finalization)
    final_review = review_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain)
    final_review_archive = archive_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review(final_review)
    return close_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive(final_review_archive)


def test_task_137_required_files_exist() -> None:
    assert DOC_TASK_136.exists()
    assert DOC_TASK_137.exists()
    assert CLOSURE_MODULE.exists()
    assert CLOSURE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert CLOSURE_JSON.exists()
    assert CLOSURE_MD.exists()


def test_task_137_dependency_markers() -> None:
    text = DOC_TASK_136.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_136_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_136_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_LOCAL_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_136_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_LOCAL_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_136_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_136_FINAL_REVIEW_ARCHIVE_CLOSURE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_136_FINAL_REVIEW_ARCHIVE_CLOSURE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_136_FINAL_REVIEW_ARCHIVE_CLOSURE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_136_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_136_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_136_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_136_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_136_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_136_LEGAL_CERTIFICATION=false" in text


def test_task_137_closure_contract() -> None:
    closure = _build_closure()
    assert TASK_ID == "MILESTONE_19_TASK_137_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_LOCAL_IMPLEMENTATION_V1"
    assert FINAL_REVIEW_ARCHIVE_CLOSURE_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_LOCAL_V1"
    assert closure.final_review_archive_closure_ok is True
    assert closure.source_final_review_archive_ok is True
    assert closure.source_final_review_ok is True
    assert closure.source_archived_case_count == 8
    assert closure.source_archived_passed_count == 8
    assert closure.source_archived_failed_count == 0
    assert len(closure.chain_coverage_tasks) == 16
    assert validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure(closure) == ()
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_ONLY is True


def test_task_137_canonical_markers() -> None:
    text = DOC_TASK_137.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_137_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_137_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_LOCAL_IMPLEMENTATION_READY" in text
    assert "MILESTONE_19_TASK_137_MODE=LOCAL_DIAGNOSTIC_ONLY_FINAL_REVIEW_ARCHIVE_CLOSURE_NO_RUNTIME_WIRING" in text
    assert "MILESTONE_19_TASK_137_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_137_DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_ONLY=true" in text
    assert "MILESTONE_19_TASK_137_FINAL_REVIEW_ARCHIVE_CLOSURE_LOCAL_ONLY=true" in text
    assert "MILESTONE_19_TASK_137_FINAL_REVIEW_ARCHIVE_CLOSURE_TECHNICAL_CONTINUITY_EVIDENCE_ONLY=true" in text
    assert "MILESTONE_19_TASK_137_FINAL_REVIEW_ARCHIVE_CLOSURE_MODIFIES_SOURCE_ARCHIVE=false" in text
    assert "MILESTONE_19_TASK_137_FINAL_REVIEW_ARCHIVE_CLOSURE_MODIFIES_SOURCE_FINAL_REVIEW=false" in text
    assert "MILESTONE_19_TASK_137_FINAL_REVIEW_ARCHIVE_CLOSURE_MODIFIES_SOURCE_FINAL_CHAIN_CLOSURE=false" in text
    assert "MILESTONE_19_TASK_137_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_137_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_137_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_137_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_137_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_137_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_137_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_137_NEXT_STAGE=MILESTONE_19_TASK_138_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_IMPLEMENTATION_REVIEW_V1" in text


def test_task_137_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_137_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_LOCAL_IMPLEMENTATION_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_LOCAL_IMPLEMENTATION_READY"
    assert manifest["mode"] == "LOCAL_DIAGNOSTIC_ONLY_FINAL_REVIEW_ARCHIVE_CLOSURE_NO_RUNTIME_WIRING"
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveClosureImplemented"] is True
    assert manifest["diagnosticSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveClosureOnly"] is True
    assert manifest["finalReviewArchiveClosureLocalOnly"] is True
    assert manifest["finalReviewArchiveClosureTechnicalContinuityEvidenceOnly"] is True
    assert manifest["finalReviewArchiveClosureModifiesSourceArchive"] is False
    assert manifest["finalReviewArchiveClosureModifiesSourceFinalReview"] is False
    assert manifest["finalReviewArchiveClosureModifiesSourceFinalChainClosure"] is False
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


def test_task_137_static_closure_artifact() -> None:
    payload = json.loads(CLOSURE_JSON.read_text(encoding="utf-8"))
    assert payload["finalReviewArchiveClosureId"].startswith("SRSC-DIAG-SMOKE-FINAL-REVIEW-ARCHIVE-CLOSURE-")
    assert payload["finalReviewArchiveClosureOk"] is True
    assert payload["sourceFinalReviewArchiveOk"] is True
    assert payload["sourceFinalReviewOk"] is True
    assert payload["sourceArchivedCaseCount"] == 8
    assert payload["sourceArchivedPassedCount"] == 8
    assert payload["sourceArchivedFailedCount"] == 0
    assert payload["validationIssues"] == []
    assert payload["coveredTaskRange"] == "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"
    assert payload["chainCoverageTaskCount"] == 16
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
