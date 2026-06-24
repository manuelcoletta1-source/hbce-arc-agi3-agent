"""Tests for SRSC controlled smoke-run result archive closure finalization."""

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
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_ONLY,
    FINALIZATION_REVISION,
    TASK_ID,
    build_controlled_smoke_run_result_archive_closure_finalization_plan,
    finalize_controlled_smoke_run_result_archive_closure,
    validate_controlled_smoke_run_result_archive_closure_finalization,
)


def _build_closure():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    return close_controlled_smoke_run_result_archive(archive)


def test_finalization_plan_public_boundary() -> None:
    plan = build_controlled_smoke_run_result_archive_closure_finalization_plan(metadata={"case": "plan"})
    payload = plan.to_public_dict()

    assert plan.finalization_plan_id.startswith("SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-FINALIZATION-PLAN-")
    assert payload["finalizationRevision"] == FINALIZATION_REVISION
    assert payload["technicalContinuityEvidenceOnly"] is True
    assert payload["noScoreClaimMarker"] is True
    assert payload["noSubmissionMarker"] is True
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True
    assert payload["pocV09RuntimeImplemented"] is False
    assert payload["pocV09Benchmarked"] is False
    assert payload["pocV09FaultInjectionPerformed"] is False
    assert payload["pocV09ProductionReady"] is False


def test_finalize_default_closure() -> None:
    closure = _build_closure()
    finalization = finalize_controlled_smoke_run_result_archive_closure(
        closure,
        metadata={"case": "default-finalization"},
    )

    assert TASK_ID == "MILESTONE_19_TASK_121_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_V1"
    assert finalization.finalization_id.startswith("SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-FINALIZATION-")
    assert finalization.finalization_ok is True
    assert finalization.source_closure_id == closure.closure_id
    assert finalization.source_archive_id == closure.source_archive_id
    assert finalization.source_suite_result_id == closure.source_suite_result_id
    assert finalization.source_closure_ok is True
    assert finalization.source_archived_case_count == 8
    assert finalization.source_archived_passed_count == 8
    assert finalization.source_archived_failed_count == 0
    assert validate_controlled_smoke_run_result_archive_closure_finalization(finalization) == ()


def test_finalization_public_payload_boundary() -> None:
    finalization = finalize_controlled_smoke_run_result_archive_closure(_build_closure())
    payload = finalization.to_public_dict()

    assert payload["finalizationOk"] is True
    assert payload["controlledSmokeRunResultArchiveClosureFinalizationImplemented"] is True
    assert payload["diagnosticSmokeRunResultArchiveClosureFinalizationOnly"] is True
    assert payload["closureModified"] is False
    assert payload["closureModuleModified"] is False
    assert payload["resultArchiveModified"] is False
    assert payload["resultArchiveModuleModified"] is False
    assert payload["smokeRunModuleModified"] is False
    assert payload["usageRunnerModified"] is False
    assert payload["artifactEmitterModified"] is False
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
    assert payload["technicalContinuityEvidenceOnly"] is True


def test_finalization_is_deterministic_for_same_closure() -> None:
    closure = _build_closure()
    first = finalize_controlled_smoke_run_result_archive_closure(closure)
    second = finalize_controlled_smoke_run_result_archive_closure(closure)

    assert first.finalization_id == second.finalization_id
    assert first.to_public_dict() == second.to_public_dict()


def test_finalization_constants() -> None:
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINALIZATION_ONLY is True
