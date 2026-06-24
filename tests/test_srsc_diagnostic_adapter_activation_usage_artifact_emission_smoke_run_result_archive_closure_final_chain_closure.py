"""Tests for SRSC controlled smoke-run result archive closure final-chain closure."""

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
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTED,
    COVERED_TASK_RANGE,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_ONLY,
    FINAL_CHAIN_CLOSURE_REVISION,
    TASK_ID,
    build_controlled_smoke_run_result_archive_closure_final_chain_closure_plan,
    close_controlled_smoke_run_result_archive_closure_final_chain,
    default_chain_coverage_tasks,
    validate_controlled_smoke_run_result_archive_closure_final_chain_closure,
)


def _build_finalization():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    closure = close_controlled_smoke_run_result_archive(archive)
    return finalize_controlled_smoke_run_result_archive_closure(closure)


def test_final_chain_closure_plan_public_boundary() -> None:
    plan = build_controlled_smoke_run_result_archive_closure_final_chain_closure_plan(metadata={"case": "plan"})
    payload = plan.to_public_dict()

    assert plan.final_chain_closure_plan_id.startswith("SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-FINAL-CHAIN-CLOSURE-PLAN-")
    assert payload["finalChainClosureRevision"] == FINAL_CHAIN_CLOSURE_REVISION
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


def test_default_chain_coverage_tasks() -> None:
    tasks = default_chain_coverage_tasks()
    assert len(tasks) == 16
    assert tasks[0] == "MILESTONE_19_TASK_107"
    assert tasks[-1] == "MILESTONE_19_TASK_122"


def test_close_default_final_chain() -> None:
    finalization = _build_finalization()
    final_chain = close_controlled_smoke_run_result_archive_closure_final_chain(
        finalization,
        metadata={"case": "default-final-chain-closure"},
    )

    assert TASK_ID == "MILESTONE_19_TASK_125_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_LOCAL_IMPLEMENTATION_V1"
    assert final_chain.final_chain_closure_id.startswith("SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-FINAL-CHAIN-CLOSURE-")
    assert final_chain.final_chain_closure_ok is True
    assert final_chain.source_finalization_id == finalization.finalization_id
    assert final_chain.source_closure_id == finalization.source_closure_id
    assert final_chain.source_archive_id == finalization.source_archive_id
    assert final_chain.source_suite_result_id == finalization.source_suite_result_id
    assert final_chain.source_finalization_ok is True
    assert final_chain.source_archived_case_count == 8
    assert final_chain.source_archived_passed_count == 8
    assert final_chain.source_archived_failed_count == 0
    assert final_chain.plan.covered_task_range == COVERED_TASK_RANGE
    assert len(final_chain.chain_coverage_tasks) == 16
    assert validate_controlled_smoke_run_result_archive_closure_final_chain_closure(final_chain) == ()


def test_final_chain_public_payload_boundary() -> None:
    final_chain = close_controlled_smoke_run_result_archive_closure_final_chain(_build_finalization())
    payload = final_chain.to_public_dict()

    assert payload["finalChainClosureOk"] is True
    assert payload["controlledSmokeRunResultArchiveClosureFinalChainClosureImplemented"] is True
    assert payload["diagnosticSmokeRunResultArchiveClosureFinalChainClosureOnly"] is True
    assert payload["chainCoverageTaskCount"] == 16
    assert payload["coveredTaskRange"] == COVERED_TASK_RANGE
    assert payload["closureFinalizationModified"] is False
    assert payload["closureFinalizationModuleModified"] is False
    assert payload["closureModified"] is False
    assert payload["closureModuleModified"] is False
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


def test_final_chain_closure_is_deterministic_for_same_finalization() -> None:
    finalization = _build_finalization()
    first = close_controlled_smoke_run_result_archive_closure_final_chain(finalization)
    second = close_controlled_smoke_run_result_archive_closure_final_chain(finalization)

    assert first.final_chain_closure_id == second.final_chain_closure_id
    assert first.to_public_dict() == second.to_public_dict()


def test_final_chain_closure_constants() -> None:
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_ONLY is True
