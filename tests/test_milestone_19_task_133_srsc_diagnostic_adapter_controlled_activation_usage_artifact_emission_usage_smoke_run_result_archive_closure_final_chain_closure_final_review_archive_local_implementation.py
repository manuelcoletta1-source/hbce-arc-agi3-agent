"""Milestone #19 Task 133 - SRSC final review archive local implementation validation."""

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
    TASK_ID,
    archive_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review,
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_132 = ROOT / "docs" / "milestone-19-task-132-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-authorization-review-v1.md"
DOC_TASK_133 = ROOT / "docs" / "milestone-19-task-133-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-local-implementation-v1.md"
ARCHIVE_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive.py"
ARCHIVE_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review_archive.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-local-implementation-v1" / "task-133-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-local-implementation-v1" / "task-133-index.txt"
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


def test_task_133_required_files_exist() -> None:
    assert DOC_TASK_132.exists()
    assert DOC_TASK_133.exists()
    assert ARCHIVE_MODULE.exists()
    assert ARCHIVE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert ARCHIVE_JSON.exists()
    assert ARCHIVE_MD.exists()


def test_task_133_dependency_markers() -> None:
    text = DOC_TASK_132.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_132_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_132_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_LOCAL_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_132_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_LOCAL_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_132_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_132_FINAL_REVIEW_ARCHIVE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_132_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_132_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_132_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_132_LEGAL_CERTIFICATION=false" in text


def test_task_133_archive_contract() -> None:
    archive = _build_archive()
    assert TASK_ID == "MILESTONE_19_TASK_133_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_LOCAL_IMPLEMENTATION_V1"
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


def test_task_133_canonical_markers() -> None:
    text = DOC_TASK_133.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_133_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_133_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_LOCAL_IMPLEMENTATION_READY" in text
    assert "MILESTONE_19_TASK_133_MODE=LOCAL_DIAGNOSTIC_ONLY_FINAL_REVIEW_ARCHIVE_NO_RUNTIME_WIRING" in text
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
    assert "MILESTONE_19_TASK_133_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_133_NEXT_STAGE=MILESTONE_19_TASK_134_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_IMPLEMENTATION_REVIEW_V1" in text


def test_task_133_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_133_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_LOCAL_IMPLEMENTATION_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_LOCAL_IMPLEMENTATION_READY"
    assert manifest["mode"] == "LOCAL_DIAGNOSTIC_ONLY_FINAL_REVIEW_ARCHIVE_NO_RUNTIME_WIRING"
    assert manifest["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveImplemented"] is True
    assert manifest["diagnosticSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveOnly"] is True
    assert manifest["finalReviewArchiveLocalOnly"] is True
    assert manifest["finalReviewArchiveTechnicalContinuityEvidenceOnly"] is True
    assert manifest["finalReviewArchiveModifiesSourceFinalReview"] is False
    assert manifest["finalReviewArchiveModifiesSourceFinalChainClosure"] is False
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


def test_task_133_static_archive_artifact() -> None:
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
