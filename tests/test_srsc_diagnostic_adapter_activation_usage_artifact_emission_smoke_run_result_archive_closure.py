"""Tests for SRSC controlled smoke-run result archive closure."""

from __future__ import annotations

from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run import (
    run_controlled_artifact_emission_usage_smoke_run_suite,
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive import (
    archive_controlled_smoke_run_suite_result,
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive_closure import (
    CLOSURE_REVISION,
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTED,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_ONLY,
    TASK_ID,
    build_controlled_smoke_run_result_archive_closure_plan,
    close_controlled_smoke_run_result_archive,
    validate_controlled_smoke_run_result_archive_closure,
)


def _build_archive():
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    return archive_controlled_smoke_run_suite_result(suite)


def test_closure_plan_public_boundary() -> None:
    plan = build_controlled_smoke_run_result_archive_closure_plan(metadata={"case": "plan"})
    payload = plan.to_public_dict()

    assert plan.closure_plan_id.startswith("SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-PLAN-")
    assert payload["closureRevision"] == CLOSURE_REVISION
    assert payload["technicalContinuityEvidenceOnly"] is True
    assert payload["noScoreClaimMarker"] is True
    assert payload["noSubmissionMarker"] is True
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True
    assert payload["pocV09RuntimeImplemented"] is False
    assert payload["pocV09Benchmarked"] is False
    assert payload["pocV09FaultInjectionPerformed"] is False
    assert payload["pocV09ProductionReady"] is False


def test_close_default_archive() -> None:
    archive = _build_archive()
    closure = close_controlled_smoke_run_result_archive(
        archive,
        metadata={"case": "default-closure"},
    )

    assert TASK_ID == "MILESTONE_19_TASK_117_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_LOCAL_IMPLEMENTATION_V1"
    assert closure.closure_id.startswith("SRSC-DIAG-SMOKE-ARCHIVE-CLOSURE-")
    assert closure.closure_ok is True
    assert closure.source_archive_id == archive.archive_id
    assert closure.source_suite_result_id == archive.source_suite_result_id
    assert closure.source_archive_ok is True
    assert closure.source_archived_case_count == 8
    assert closure.source_archived_passed_count == 8
    assert closure.source_archived_failed_count == 0
    assert validate_controlled_smoke_run_result_archive_closure(closure) == ()


def test_closure_public_payload_boundary() -> None:
    closure = close_controlled_smoke_run_result_archive(_build_archive())
    payload = closure.to_public_dict()

    assert payload["closureOk"] is True
    assert payload["controlledSmokeRunResultArchiveClosureImplemented"] is True
    assert payload["diagnosticSmokeRunResultArchiveClosureOnly"] is True
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


def test_closure_is_deterministic_for_same_archive() -> None:
    archive = _build_archive()
    first = close_controlled_smoke_run_result_archive(archive)
    second = close_controlled_smoke_run_result_archive(archive)

    assert first.closure_id == second.closure_id
    assert first.to_public_dict() == second.to_public_dict()


def test_closure_constants() -> None:
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_ONLY is True
