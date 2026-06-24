"""Tests for SRSC controlled final review archive closure."""

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
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_IMPLEMENTED,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_ONLY,
    FINAL_REVIEW_ARCHIVE_CLOSURE_REVISION,
    TASK_ID,
    build_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure_plan,
    close_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive,
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure,
)


def _build_archive():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    finalization = finalize_controlled_smoke_run_result_archive_closure(closure)
    final_chain = close_controlled_smoke_run_result_archive_closure_final_chain(finalization)
    final_review = review_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain)
    return archive_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review(final_review)


def test_final_review_archive_closure_plan_public_boundary() -> None:
    plan = build_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure_plan(metadata={"case": "plan"})
    payload = plan.to_public_dict()

    assert plan.final_review_archive_closure_plan_id.startswith("SRSC-DIAG-SMOKE-FINAL-REVIEW-ARCHIVE-CLOSURE-PLAN-")
    assert payload["finalReviewArchiveClosureRevision"] == FINAL_REVIEW_ARCHIVE_CLOSURE_REVISION
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


def test_close_default_final_review_archive() -> None:
    archive = _build_archive()
    closure = close_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive(
        archive,
        metadata={"case": "default-final-review-archive-closure"},
    )

    assert TASK_ID == "MILESTONE_19_TASK_137_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_LOCAL_IMPLEMENTATION_V1"
    assert closure.final_review_archive_closure_id.startswith("SRSC-DIAG-SMOKE-FINAL-REVIEW-ARCHIVE-CLOSURE-")
    assert closure.final_review_archive_closure_ok is True
    assert closure.source_final_review_archive_id == archive.final_review_archive_id
    assert closure.source_final_review_archive_ok is True
    assert closure.source_final_review_archive_validation_issues == ()
    assert closure.source_final_review_ok is True
    assert closure.source_archived_case_count == 8
    assert closure.source_archived_passed_count == 8
    assert closure.source_archived_failed_count == 0
    assert len(closure.chain_coverage_tasks) == 16
    assert validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive_closure(closure) == ()


def test_final_review_archive_closure_public_payload_boundary() -> None:
    closure = close_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive(_build_archive())
    payload = closure.to_public_dict()

    assert payload["finalReviewArchiveClosureOk"] is True
    assert payload["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveClosureImplemented"] is True
    assert payload["diagnosticSmokeRunResultArchiveClosureFinalChainClosureFinalReviewArchiveClosureOnly"] is True
    assert payload["chainCoverageTaskCount"] == 16
    assert payload["coveredTaskRange"] == "MILESTONE_19_TASK_107_THROUGH_MILESTONE_19_TASK_122"
    assert payload["sourceArchivedCaseCount"] == 8
    assert payload["sourceArchivedPassedCount"] == 8
    assert payload["sourceArchivedFailedCount"] == 0
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
    assert payload["failClosedActive"] is True


def test_final_review_archive_closure_is_deterministic_for_same_archive() -> None:
    archive = _build_archive()
    first = close_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive(archive)
    second = close_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_archive(archive)

    assert first.final_review_archive_closure_id == second.final_review_archive_closure_id
    assert first.to_public_dict() == second.to_public_dict()


def test_final_review_archive_closure_constants() -> None:
    assert FINAL_REVIEW_ARCHIVE_CLOSURE_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_LOCAL_V1"
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_ONLY is True
