"""Tests for SRSC controlled smoke-run result archive."""

from __future__ import annotations

from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run import (
    POC_V0_9_STATUS,
    run_controlled_artifact_emission_usage_smoke_run_suite,
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive import (
    ARTIFACT_EMITTER_MODIFIED,
    BENCHMARK_BINDING,
    CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTED,
    DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_ONLY,
    FAIL_CLOSED_ACTIVE,
    KAGGLE_AUTHENTICATION_PERFORMED,
    LEGAL_CERTIFICATION,
    POC_V0_9_BENCHMARKED,
    POC_V0_9_FAULT_INJECTION_PERFORMED,
    POC_V0_9_PRODUCTION_READY,
    POC_V0_9_RUNTIME_IMPLEMENTED,
    PRIVATE_CORE_EXPOSURE,
    RAW_REQUEST_BODY_PERSISTED,
    RESULT_ARCHIVE_REVISION,
    RUNTIME_SOLVER_MODIFIED_IN_ARCHIVE,
    RUNTIME_WIRING_ALLOWED_IN_ARCHIVE,
    SECRET_PERSISTED,
    SMOKE_RUN_MODULE_MODIFIED,
    SOLVER_RUNTIME_BINDING_IN_ARCHIVE,
    TASK_ID,
    USAGE_RUNNER_MODIFIED,
    archive_controlled_smoke_run_suite_result,
    build_controlled_smoke_run_result_archive_plan,
    validate_controlled_smoke_run_result_archive,
)


def test_build_archive_plan_boundary() -> None:
    plan = build_controlled_smoke_run_result_archive_plan(metadata={"case": "plan"})

    assert plan.plan_id.startswith("SRSC-DIAG-SMOKE-ARCHIVE-PLAN-")

    payload = plan.to_public_dict()
    assert payload["resultArchiveRevision"] == RESULT_ARCHIVE_REVISION
    assert payload["pocV09Status"] == "POC_V0_9_SPECIFICATION_READY / IMPLEMENTATION_NOT_STARTED"
    assert payload["pocV09RuntimeImplemented"] is False
    assert payload["pocV09Benchmarked"] is False
    assert payload["pocV09FaultInjectionPerformed"] is False
    assert payload["pocV09ProductionReady"] is False
    assert payload["noScoreClaimMarker"] is True
    assert payload["noSubmissionMarker"] is True
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True


def test_archive_default_smoke_run_suite_result() -> None:
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(
        suite,
        metadata={"case": "default-suite"},
    )

    assert archive.archive_id.startswith("SRSC-DIAG-SMOKE-ARCHIVE-")
    assert archive.archive_ok is True
    assert archive.source_suite_result_id == suite.suite_result_id
    assert archive.source_suite_ok is True
    assert archive.source_case_count == 8
    assert archive.source_passed_count == 8
    assert archive.source_failed_count == 0
    assert archive.archived_case_count == 8
    assert archive.archived_passed_count == 8
    assert archive.archived_failed_count == 0
    assert archive.emitted_artifact_count == 9
    assert archive.blocked_artifact_count == 2
    assert archive.blocked_usage_request_count == 1
    assert validate_controlled_smoke_run_result_archive(archive) == ()


def test_archive_entries_are_public_safe() -> None:
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)

    assert archive.entries
    assert all(entry.entry_id.startswith("SRSC-DIAG-SMOKE-ARCHIVE-ENTRY-") for entry in archive.entries)
    assert all(entry.no_score_claim_marker is True for entry in archive.entries)
    assert all(entry.no_submission_marker is True for entry in archive.entries)
    assert all(entry.legal_certification is False for entry in archive.entries)
    assert all(entry.fail_closed_active is True for entry in archive.entries)

    payload = archive.to_public_dict()
    assert payload["technicalContinuityEvidenceOnly"] is True
    assert payload["noScoreClaimMarker"] is True
    assert payload["noSubmissionMarker"] is True
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True
    assert payload["rawRequestBodyPersisted"] is False
    assert payload["secretPersisted"] is False
    assert payload["credentialPersisted"] is False
    assert payload["apiKeyPersisted"] is False


def test_archive_boundary_flags_remain_closed() -> None:
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    payload = archive.to_public_dict()

    assert TASK_ID == "MILESTONE_19_TASK_113_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_IMPLEMENTATION_V1"
    assert CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTED is True
    assert DIAGNOSTIC_SMOKE_RUN_RESULT_ARCHIVE_ONLY is True
    assert SMOKE_RUN_MODULE_MODIFIED is False
    assert USAGE_RUNNER_MODIFIED is False
    assert ARTIFACT_EMITTER_MODIFIED is False
    assert RUNTIME_SOLVER_MODIFIED_IN_ARCHIVE is False
    assert RUNTIME_WIRING_ALLOWED_IN_ARCHIVE is False
    assert SOLVER_RUNTIME_BINDING_IN_ARCHIVE is False
    assert BENCHMARK_BINDING is False
    assert KAGGLE_AUTHENTICATION_PERFORMED is False
    assert PRIVATE_CORE_EXPOSURE is False
    assert LEGAL_CERTIFICATION is False
    assert RAW_REQUEST_BODY_PERSISTED is False
    assert SECRET_PERSISTED is False
    assert FAIL_CLOSED_ACTIVE is True
    assert POC_V0_9_STATUS == "POC_V0_9_SPECIFICATION_READY / IMPLEMENTATION_NOT_STARTED"
    assert POC_V0_9_RUNTIME_IMPLEMENTED is False
    assert POC_V0_9_BENCHMARKED is False
    assert POC_V0_9_FAULT_INJECTION_PERFORMED is False
    assert POC_V0_9_PRODUCTION_READY is False

    assert payload["controlledSmokeRunResultArchiveImplemented"] is True
    assert payload["diagnosticSmokeRunResultArchiveOnly"] is True
    assert payload["smokeRunModuleModified"] is False
    assert payload["usageRunnerModified"] is False
    assert payload["artifactEmitterModified"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["solverRuntimeBinding"] is False
    assert payload["benchmarkScoreClaimed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["privateCoreExposure"] is False
    assert payload["legalCertification"] is False


def test_archive_is_deterministic_for_same_suite() -> None:
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    first = archive_controlled_smoke_run_suite_result(suite)
    second = archive_controlled_smoke_run_suite_result(suite)

    assert first.archive_id == second.archive_id
    assert first.to_public_dict() == second.to_public_dict()
