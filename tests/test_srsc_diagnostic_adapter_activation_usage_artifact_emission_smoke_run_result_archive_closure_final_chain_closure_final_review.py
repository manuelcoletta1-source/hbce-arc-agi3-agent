"""Tests for SRSC controlled smoke-run result archive closure final-chain closure final review."""

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
    COVERED_TASK_RANGE,
    close_controlled_smoke_run_result_archive_closure_final_chain,
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure_final_chain_closure_final_review import (
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_IMPLEMENTED,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ONLY,
    FINAL_REVIEW_REVISION,
    TASK_ID,
    build_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_plan,
    review_controlled_smoke_run_result_archive_closure_final_chain_closure,
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review,
)


def _build_final_chain_closure():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    finalization = finalize_controlled_smoke_run_result_archive_closure(closure)
    return close_controlled_smoke_run_result_archive_closure_final_chain(finalization)


def test_final_review_plan_public_boundary() -> None:
    plan = build_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review_plan(metadata={"case": "plan"})
    payload = plan.to_public_dict()

    assert plan.final_review_plan_id.startswith("SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-FINAL-CHAIN-FINAL-REVIEW-PLAN-")
    assert payload["finalReviewRevision"] == FINAL_REVIEW_REVISION
    assert payload["coveredTaskRange"] == COVERED_TASK_RANGE
    assert payload["technicalContinuityEvidenceOnly"] is True
    assert payload["noScoreClaimMarker"] is True
    assert payload["noSubmissionMarker"] is True
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True
    assert payload["pocV09RuntimeImplemented"] is False
    assert payload["pocV09Benchmarked"] is False
    assert payload["pocV09FaultInjectionPerformed"] is False
    assert payload["pocV09ProductionReady"] is False


def test_review_default_final_chain_closure() -> None:
    final_chain = _build_final_chain_closure()
    final_review = review_controlled_smoke_run_result_archive_closure_final_chain_closure(
        final_chain,
        metadata={"case": "default-final-review"},
    )

    assert TASK_ID == "MILESTONE_19_TASK_129_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_LOCAL_IMPLEMENTATION_V1"
    assert final_review.final_review_id.startswith("SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-FINAL-CHAIN-FINAL-REVIEW-")
    assert final_review.final_review_ok is True
    assert final_review.source_final_chain_closure_id == final_chain.final_chain_closure_id
    assert final_review.source_final_chain_closure_ok is True
    assert final_review.source_archived_case_count == 8
    assert final_review.source_archived_passed_count == 8
    assert final_review.source_archived_failed_count == 0
    assert final_review.plan.covered_task_range == COVERED_TASK_RANGE
    assert len(final_review.chain_coverage_tasks) == 16
    assert validate_controlled_smoke_run_result_archive_closure_final_chain_closure_final_review(final_review) == ()


def test_final_review_public_payload_boundary() -> None:
    final_review = review_controlled_smoke_run_result_archive_closure_final_chain_closure(_build_final_chain_closure())
    payload = final_review.to_public_dict()

    assert payload["finalReviewOk"] is True
    assert payload["controlledSmokeRunResultArchiveClosureFinalChainClosureFinalReviewImplemented"] is True
    assert payload["diagnosticSmokeRunResultArchiveClosureFinalChainClosureFinalReviewOnly"] is True
    assert payload["controlledSmokeRunResultArchiveClosureFinalChainClosureImplemented"] is True
    assert payload["diagnosticSmokeRunResultArchiveClosureFinalChainClosureOnly"] is True
    assert payload["chainCoverageTaskCount"] == 16
    assert payload["coveredTaskRange"] == COVERED_TASK_RANGE
    assert payload["sourceArchivedCaseCount"] == 8
    assert payload["sourceArchivedPassedCount"] == 8
    assert payload["sourceArchivedFailedCount"] == 0
    assert payload["finalChainClosureModified"] is False
    assert payload["finalChainClosureModuleModified"] is False
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


def test_final_review_is_deterministic_for_same_final_chain_closure() -> None:
    final_chain = _build_final_chain_closure()
    first = review_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain)
    second = review_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain)

    assert first.final_review_id == second.final_review_id
    assert first.to_public_dict() == second.to_public_dict()


def test_final_review_constants() -> None:
    assert FINAL_REVIEW_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_LOCAL_V1"
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ONLY is True
