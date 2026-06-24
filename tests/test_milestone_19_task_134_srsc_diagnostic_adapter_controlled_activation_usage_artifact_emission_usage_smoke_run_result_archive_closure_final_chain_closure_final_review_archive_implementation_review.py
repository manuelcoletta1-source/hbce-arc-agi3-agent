"""Milestone #19 Task 134 - SRSC final review archive implementation review validation."""

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
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_IMPLEMENTED,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_ONLY,
    FINAL_REVIEW_ARCHIVE_REVISION,
    TASK_ID as TASK_133_ID,
    archive_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review,
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_133 = ROOT / "docs" / "milestone-19-task-133-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-local-implementation-v1.md"
DOC_TASK_134 = ROOT / "docs" / "milestone-19-task-134-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-implementation-review-v1.md"
ARCHIVE_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive.py"
ARCHIVE_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive.py"
TASK_133_TEST = ROOT / "tests" / "test_milestone_19_task_133_srsc_diagnostic_adapter_controlled_activation_usage_artifact_emission_usage_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_local_implementation.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-implementation-review-v1" / "task-134-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-implementation-review-v1" / "task-134-index.txt"
ARCHIVE_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-local-implementation-v1" / "task-133-smoke-run-result-archive-closure-final-chain-closure-final-review-archive.json"
ARCHIVE_MD = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-local-implementation-v1" / "task-133-smoke-run-result-archive-closure-final-chain-closure-final-review-archive.md"


def _build_archive():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    finalization = finalize_controlled_smoke_run_result_archive_closure(closure)
    final_chain = close_controlled_smoke_run_result_archive_closure_final_chain(finalization)
    final_review = review_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain)
    return archive_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review(final_review)


def test_task_134_required_files_exist() -> None:
    assert DOC_TASK_133.exists()
    assert DOC_TASK_134.exists()
    assert ARCHIVE_MODULE.exists()
    assert ARCHIVE_TEST.exists()
    assert TASK_133_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert ARCHIVE_JSON.exists()
    assert ARCHIVE_MD.exists()


def test_task_134_dependency_markers() -> None:
    text = DOC_TASK_133.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_133_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_133_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_133_DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_ONLY=true" in text
    assert "MILESTONE_19_TASK_133_FINAL_REVIEW_ARCHIVE_LOCAL_ONLY=true" in text
    assert "MILESTONE_19_TASK_133_FINAL_REVIEW_ARCHIVE_TECHNICAL_CONTINUITY_EVIDENCE_ONLY=true" in text
    assert "MILESTONE_19_TASK_133_FINAL_REVIEW_ARCHIVE_MODIFIES_SOURCE_FINAL_REVIEW=false" in text
    assert "MILESTONE_19_TASK_133_FINAL_REVIEW_ARCHIVE_MODIFIES_SOURCE_FINAL_CHAIN_CLOSURE=false" in text
    assert "MILESTONE_19_TASK_133_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_133_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_133_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_133_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_133_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_133_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_133_NEXT_STAGE=MILESTONE_19_TASK_134_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_IMPLEMENTATION_REVIEW_V1" in text


def test_task_134_archive_contract_still_valid() -> None:
    archive = _build_archive()
    assert TASK_133_ID == "MILESTONE_19_TASK_133_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_LOCAL_IMPLEMENTATION_V1"
    assert FINAL_REVIEW_ARCHIVE_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_LOCAL_V1"
    assert archive.final_review_archive_ok is True
    assert archive.source_final_review_ok is True
    assert archive.source_archived_case_count == 8
    assert archive.source_archived_passed_count == 8
    assert archive.source_archived_failed_count == 0
    assert len(archive.chain_coverage_tasks) == 16
    assert validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive(archive) == ()
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_ONLY is True


def test_task_134_static_archive_artifact_public_safe() -> None:
    payload = json.loads(ARCHIVE_JSON.read_text(encoding="utf-8"))
    assert payload["finalReviewArchiveId"].startswith("SRSC-DIAG-SMOKE-FINAL-REVIEW-ARCHIVE-")
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


def test_task_134_canonical_markers() -> None:
    text = DOC_TASK_134.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_134_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_134_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_IMPLEMENTATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_134_MODE=REVIEW_ONLY_NO_FINAL_REVIEW_ARCHIVE_MODIFICATION" in text
    assert "MILESTONE_19_TASK_134_DECISION=ACCEPT_TASK_133_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_LOCAL_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_134_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_IMPLEMENTATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_134_TASK_133_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_IMPLEMENTATION_ACCEPTED=true" in text
    assert "MILESTONE_19_TASK_134_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_134_FINAL_REVIEW_ARCHIVE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_134_FINAL_REVIEW_ARCHIVE_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_134_FINAL_REVIEW_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_134_FINAL_REVIEW_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_134_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_134_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_134_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_134_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_134_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_134_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_134_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_134_NEXT_STAGE=MILESTONE_19_TASK_135_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_PLANNING_V1" in text


def test_task_134_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_134_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_IMPLEMENTATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_IMPLEMENTATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_FINAL_REVIEW_ARCHIVE_MODIFICATION"
    assert manifest["decision"] == "ACCEPT_TASK_133_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_LOCAL_IMPLEMENTATION"
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveImplementationReviewPerformed"] is True
    assert manifest["task133SmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveImplementationAccepted"] is True
    assert manifest["implementationPerformedInTask134"] is False
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
    assert manifest["coveredTaskRange"] == "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"
