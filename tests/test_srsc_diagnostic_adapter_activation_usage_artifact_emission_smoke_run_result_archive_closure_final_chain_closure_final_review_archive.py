"""Tests for SRSC controlled final review archive."""

from __future__ import annotations

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
    build_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_plan,
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive,
)


def _build_final_review():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    finalization = finalize_controlled_smoke_run_result_archive_closure(closure)
    final_chain = close_controlled_smoke_run_result_archive_closure_final_chain(finalization)
    return review_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain)


def test_final_review_archive_plan_public_boundary() -> None:
    plan = build_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_plan(metadata={"case": "plan"})
    payload = plan.to_public_dict()

    assert plan.final_review_archive_plan_id.startswith("SRSC-DIAG-SMOKE-FINAL-REVIEW-ARCHIVE-PLAN-")
    assert payload["finalReviewArchiveRevision"] == FINAL_REVIEW_ARCHIVE_REVISION
    assert payload["coveredTaskRange"] == "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"
    assert payload["localOnly"] is True
    assert payload["technicalContinuityEvidenceOnly"] is True
    assert payload["noScoreClaimMarker"] is True
    assert payload["noSubmissionMarker"] is True
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True
    assert payload["pocV09RuntimeImplemented"] is False
    assert payload["pocV09Benchmarked"] is False
    assert payload["pocV09FaultInjectionPerformed"] is False
    assert payload["pocV09ProductionReady"] is False


def test_archive_default_final_review() -> None:
    final_review = _build_final_review()
    archive = archive_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review(
        final_review,
        metadata={"case": "default-final-review-archive"},
    )

    assert TASK_ID == "MILESTONE_19_TASK_133_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_LOCAL_IMPLEMENTATION_V1"
    assert archive.final_review_archive_id.startswith("SRSC-DIAG-SMOKE-FINAL-REVIEW-ARCHIVE-")
    assert archive.final_review_archive_ok is True
    assert archive.source_final_review_id == final_review.final_review_id
    assert archive.source_final_review_ok is True
    assert archive.source_final_review_validation_issues == ()
    assert archive.source_archived_case_count == 8
    assert archive.source_archived_passed_count == 8
    assert archive.source_archived_failed_count == 0
    assert len(archive.chain_coverage_tasks) == 16
    assert validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive(archive) == ()


def test_final_review_archive_public_payload_boundary() -> None:
    archive = archive_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review(_build_final_review())
    payload = archive.to_public_dict()

    assert payload["finalReviewArchiveOk"] is True
    assert payload["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveImplemented"] is True
    assert payload["diagnosticSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveOnly"] is True
    assert payload["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewImplemented"] is True
    assert payload["diagnosticSmokeRunResultArchiveClosureFinalChainClosureFinalReviewOnly"] is True
    assert payload["chainCoverageTaskCount"] == 16
    assert payload["coveredTaskRange"] == "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"
    assert payload["sourceArchivedCaseCount"] == 8
    assert payload["sourceArchivedPassedCount"] == 8
    assert payload["sourceArchivedFailedCount"] == 0
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


def test_final_review_archive_is_deterministic_for_same_final_review() -> None:
    final_review = _build_final_review()
    first = archive_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review(final_review)
    second = archive_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review(final_review)

    assert first.final_review_archive_id == second.final_review_archive_id
    assert first.to_public_dict() == second.to_public_dict()


def test_final_review_archive_constants() -> None:
    assert FINAL_REVIEW_ARCHIVE_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_LOCAL_V1"
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_ONLY is True
