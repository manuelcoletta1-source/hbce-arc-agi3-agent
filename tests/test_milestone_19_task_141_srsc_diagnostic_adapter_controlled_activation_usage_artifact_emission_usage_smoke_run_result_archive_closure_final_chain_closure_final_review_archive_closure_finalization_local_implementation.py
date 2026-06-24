"""Milestone #19 Task 141 - SRSC final review archive closure finalization local implementation validation."""

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
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure_finalization import (
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_ONLY,
    FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_REVISION,
    TASK_ID,
    finalize_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure,
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure_finalization,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_140 = ROOT / "docs" / "milestone-19-task-140-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-finalization-authorization-review-v1.md"
DOC_TASK_141 = ROOT / "docs" / "milestone-19-task-141-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-finalization-local-implementation-v1.md"
FINALIZATION_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure_finalization.py"
FINALIZATION_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure_finalization.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-finalization-local-implementation-v1" / "task-141-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-finalization-local-implementation-v1" / "task-141-index.txt"
FINALIZATION_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-finalization-local-implementation-v1" / "task-141-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-finalization.json"
FINALIZATION_MD = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-finalization-local-implementation-v1" / "task-141-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-finalization.md"


def _build_finalization():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    finalization = finalize_controlled_smoke_run_result_archive_closure(closure)
    final_chain = close_controlled_smoke_run_result_archive_closure_final_chain(finalization)
    final_review = review_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain)
    final_review_archive = archive_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review(final_review)
    final_review_archive_closure = close_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive(final_review_archive)
    return finalize_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure(final_review_archive_closure)


def test_task_141_required_files_exist() -> None:
    assert DOC_TASK_140.exists()
    assert DOC_TASK_141.exists()
    assert FINALIZATION_MODULE.exists()
    assert FINALIZATION_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert FINALIZATION_JSON.exists()
    assert FINALIZATION_MD.exists()


def test_task_141_dependency_markers() -> None:
    text = DOC_TASK_140.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_140_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_140_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_140_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_140_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_140_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_140_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_140_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_140_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_140_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_140_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_140_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_140_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_140_LEGAL_CERTIFICATION=false" in text


def test_task_141_finalization_contract() -> None:
    finalization = _build_finalization()
    assert TASK_ID == "MILESTONE_19_TASK_141_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_V1"
    assert FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_V1"
    assert finalization.final_review_archive_closure_finalization_ok is True
    assert finalization.source_final_review_archive_closure_ok is True
    assert finalization.source_final_review_archive_ok is True
    assert finalization.source_final_review_ok is True
    assert finalization.source_archived_case_count == 8
    assert finalization.source_archived_passed_count == 8
    assert finalization.source_archived_failed_count == 0
    assert len(finalization.chain_coverage_tasks) == 16
    assert validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure_finalization(finalization) == ()
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_ONLY is True


def test_task_141_canonical_markers() -> None:
    text = DOC_TASK_141.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_141_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_141_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_READY" in text
    assert "MILESTONE_19_TASK_141_MODE=LOCAL_DIAGNOSTIC_ONLY_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_NO_RUNTIME_WIRING" in text
    assert "MILESTONE_19_TASK_141_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_141_DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_ONLY=true" in text
    assert "MILESTONE_19_TASK_141_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_ONLY=true" in text
    assert "MILESTONE_19_TASK_141_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_TECHNICAL_CONTINUITY_EVIDENCE_ONLY=true" in text
    assert "MILESTONE_19_TASK_141_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_MODIFIES_SOURCE_CLOSURE=false" in text
    assert "MILESTONE_19_TASK_141_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_MODIFIES_SOURCE_ARCHIVE=false" in text
    assert "MILESTONE_19_TASK_141_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_MODIFIES_SOURCE_FINAL_REVIEW=false" in text
    assert "MILESTONE_19_TASK_141_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_141_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_141_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_141_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_141_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_141_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_141_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_141_NEXT_STAGE=MILESTONE_19_TASK_142_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTATION_REVIEW_V1" in text


def test_task_141_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_141_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_READY"
    assert manifest["mode"] == "LOCAL_DIAGNOSTIC_ONLY_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_NO_RUNTIME_WIRING"
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveClosureFinalizationImplemented"] is True
    assert manifest["diagnosticSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveClosureFinalizationOnly"] is True
    assert manifest["finalReviewArchiveClosureFinalizationLocalOnly"] is True
    assert manifest["finalReviewArchiveClosureFinalizationTechnicalContinuityEvidenceOnly"] is True
    assert manifest["finalReviewArchiveClosureFinalizationModifiesSourceClosure"] is False
    assert manifest["finalReviewArchiveClosureFinalizationModifiesSourceArchive"] is False
    assert manifest["finalReviewArchiveClosureFinalizationModifiesSourceFinalReview"] is False
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


def test_task_141_static_finalization_artifact() -> None:
    payload = json.loads(FINALIZATION_JSON.read_text(encoding="utf-8"))
    assert payload["finalReviewArchiveClosureFinalizationId"].startswith("SRSC-DIAG-SMOKE-FINAL-REVIEW-ARCHIVE-CLOSURE-FINALIZATION-")
    assert payload["finalReviewArchiveClosureFinalizationOk"] is True
    assert payload["sourceFinalReviewArchiveClosureOk"] is True
    assert payload["sourceFinalReviewArchiveOk"] is True
    assert payload["sourceFinalReviewOk"] is True
    assert payload["sourceArchivedCaseCount"] == 8
    assert payload["sourceArchivedPassedCount"] == 8
    assert payload["sourceArchivedFailedCount"] == 0
    assert payload["validationIssues"] == []
    assert payload["coveredTaskRange"] == "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"
    assert payload["chainCoverageTaskCount"] == 16
    assert payload["finalReviewArchiveClosureFinalizationLocalOnly"] is True
    assert payload["finalReviewArchiveClosureFinalizationTechnicalContinuityEvidenceOnly"] is True
    assert payload["finalReviewArchiveClosureFinalizationModifiesSourceClosure"] is False
    assert payload["finalReviewArchiveClosureFinalizationModifiesSourceArchive"] is False
    assert payload["finalReviewArchiveClosureFinalizationModifiesSourceFinalReview"] is False
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
