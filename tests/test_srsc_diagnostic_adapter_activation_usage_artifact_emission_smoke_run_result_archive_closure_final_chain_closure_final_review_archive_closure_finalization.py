"""Tests for SRSC controlled final review archive closure finalization."""

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
    build_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure_finalization_plan,
    finalize_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure,
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure_finalization,
)


def _build_closure():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    finalization = finalize_controlled_smoke_run_result_archive_closure(closure)
    final_chain = close_controlled_smoke_run_result_archive_closure_final_chain(finalization)
    final_review = review_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain)
    final_review_archive = archive_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review(final_review)
    return close_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive(final_review_archive)


def test_final_review_archive_closure_finalization_plan_public_boundary() -> None:
    plan = build_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure_finalization_plan(
        metadata={"case": "plan"}
    )
    payload = plan.to_public_dict()

    assert plan.final_review_archive_closure_finalization_plan_id.startswith("SRSC-DIAG-SMOKE-FINAL-REVIEW-ARCHIVE-CLOSURE-FINALIZATION-PLAN-")
    assert payload["finalReviewArchiveClosureFinalizationRevision"] == FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_REVISION
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


def test_finalize_default_final_review_archive_closure() -> None:
    closure = _build_closure()
    finalization = finalize_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure(
        closure,
        metadata={"case": "default-final-review-archive-closure-finalization"},
    )

    assert TASK_ID == "MILESTONE_19_TASK_141_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_V1"
    assert finalization.final_review_archive_closure_finalization_id.startswith("SRSC-DIAG-SMOKE-FINAL-REVIEW-ARCHIVE-CLOSURE-FINALIZATION-")
    assert finalization.final_review_archive_closure_finalization_ok is True
    assert finalization.source_final_review_archive_closure_id == closure.final_review_archive_closure_id
    assert finalization.source_final_review_archive_closure_ok is True
    assert finalization.source_final_review_archive_closure_validation_issues == ()
    assert finalization.source_final_review_archive_ok is True
    assert finalization.source_final_review_ok is True
    assert finalization.source_archived_case_count == 8
    assert finalization.source_archived_passed_count == 8
    assert finalization.source_archived_failed_count == 0
    assert len(finalization.chain_coverage_tasks) == 16
    assert validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure_finalization(finalization) == ()


def test_final_review_archive_closure_finalization_public_payload_boundary() -> None:
    finalization = finalize_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure(_build_closure())
    payload = finalization.to_public_dict()

    assert payload["finalReviewArchiveClosureFinalizationOk"] is True
    assert payload["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveClosureFinalizationImplemented"] is True
    assert payload["diagnosticSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveClosureFinalizationOnly"] is True
    assert payload["chainCoverageTaskCount"] == 16
    assert payload["coveredTaskRange"] == "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"
    assert payload["sourceArchivedCaseCount"] == 8
    assert payload["sourceArchivedPassedCount"] == 8
    assert payload["sourceArchivedFailedCount"] == 0
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
    assert payload["failClosedActive"] is True


def test_final_review_archive_closure_finalization_is_deterministic_for_same_closure() -> None:
    closure = _build_closure()
    first = finalize_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure(closure)
    second = finalize_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure(closure)

    assert first.final_review_archive_closure_finalization_id == second.final_review_archive_closure_finalization_id
    assert first.to_public_dict() == second.to_public_dict()


def test_final_review_archive_closure_finalization_constants() -> None:
    assert FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_V1"
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_ONLY is True
