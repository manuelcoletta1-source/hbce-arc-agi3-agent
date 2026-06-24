"""Tests for SRSC controlled artifact emission usage smoke-run."""

from __future__ import annotations

from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run import (
    ARTIFACT_EMITTER_MODIFIED,
    BENCHMARK_SCORE_CLAIMED,
    CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED,
    DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_ONLY,
    FAIL_CLOSED_ACTIVE,
    KAGGLE_SUBMISSION_SENT,
    LEGAL_CERTIFICATION,
    POC_V0_9_BENCHMARKED,
    POC_V0_9_FAULT_INJECTION_PERFORMED,
    POC_V0_9_MATURITY,
    POC_V0_9_PRODUCTION_READY,
    POC_V0_9_RUNTIME_IMPLEMENTED,
    POC_V0_9_SOURCE_DOCUMENT,
    POC_V0_9_STATUS,
    PRIVATE_CORE_EXPOSURE,
    RUNTIME_SOLVER_MODIFIED,
    RUNTIME_WIRING_ALLOWED,
    SMOKE_RUN_REVISION,
    SOLVER_RUNTIME_BINDING,
    TASK_ID,
    USAGE_RUNNER_MODIFIED,
    DiagnosticArtifactEmissionUsageSmokeRunCase,
    build_controlled_artifact_emission_usage_smoke_run_plan,
    default_smoke_run_cases,
    run_controlled_artifact_emission_usage_smoke_run,
    run_controlled_artifact_emission_usage_smoke_run_suite,
    run_default_batch_usage_smoke_run,
)


def test_build_smoke_run_plan_includes_poc_v0_9_boundary() -> None:
    plan = build_controlled_artifact_emission_usage_smoke_run_plan(metadata={"case": "plan"})
    payload = plan.to_public_dict()
    assert plan.plan_id.startswith("SRSC-DIAG-ARTIFACT-SMOKE-RUN-PLAN-")
    assert payload["pocV09SourceDocument"] == POC_V0_9_SOURCE_DOCUMENT
    assert payload["pocV09Status"] == "POC_V0_9_SPECIFICATION_READY / IMPLEMENTATION_NOT_STARTED"
    assert payload["pocV09Maturity"] == "DESIGNED / NOT_IMPLEMENTED / NOT_TESTED"
    assert payload["pocV09RuntimeImplemented"] is False
    assert payload["pocV09Benchmarked"] is False
    assert payload["pocV09FaultInjectionPerformed"] is False
    assert payload["pocV09ProductionReady"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True


def test_default_smoke_run_cases_are_deterministic_and_diagnostic() -> None:
    cases = default_smoke_run_cases()
    assert len(cases) == 8
    assert all(case.is_authorized_case for case in cases)
    assert not any(case.is_forbidden_case for case in cases)


def test_happy_path_smoke_run() -> None:
    case = DiagnosticArtifactEmissionUsageSmokeRunCase(
        case_id="TEST-001",
        case_name="happy-path diagnostic report smoke-run",
        usage_context="local diagnostic artifact usage",
        artifact_families=("local diagnostic report JSON",),
        output_name_prefix="test-happy",
        emission_purpose="happy-path smoke test",
        expected_emitted_count=1,
        expected_blocked_artifact_count=0,
        expected_blocked_usage_request_count=0,
    )
    result = run_controlled_artifact_emission_usage_smoke_run(case)
    assert result.smoke_run_result_id.startswith("SRSC-DIAG-ARTIFACT-SMOKE-RESULT-")
    assert result.smoke_run_ok is True
    assert result.expectation_ok is True
    assert result.emitted_artifact_count == 1
    assert result.blocked_artifact_count == 0
    assert result.blocked_usage_request_count == 0
    assert result.artifact_emission_usage_result is not None
    assert result.to_public_dict()["noScoreClaimMarker"] is True
    assert result.to_public_dict()["noSubmissionMarker"] is True


def test_forbidden_usage_context_smoke_run_remains_controlled() -> None:
    case = DiagnosticArtifactEmissionUsageSmokeRunCase(
        case_id="TEST-002",
        case_name="forbidden usage context smoke-run",
        usage_context="benchmark artifact usage",
        artifact_families=("local diagnostic report JSON",),
        output_name_prefix="test-forbidden-context",
        emission_purpose="forbidden usage context smoke test",
        expected_emitted_count=0,
        expected_blocked_artifact_count=0,
        expected_blocked_usage_request_count=1,
    )
    result = run_controlled_artifact_emission_usage_smoke_run(case)
    assert result.smoke_run_ok is True
    assert result.artifact_emission_usage_result is not None
    assert result.emitted_artifact_count == 0
    assert result.blocked_usage_request_count == 1
    assert result.blocked_reason is None


def test_forbidden_artifact_family_smoke_run_remains_controlled() -> None:
    case = DiagnosticArtifactEmissionUsageSmokeRunCase(
        case_id="TEST-003",
        case_name="forbidden artifact family smoke-run",
        usage_context="local diagnostic artifact usage",
        artifact_families=("score report",),
        output_name_prefix="test-forbidden-family",
        emission_purpose="forbidden artifact family smoke test",
        expected_emitted_count=0,
        expected_blocked_artifact_count=1,
        expected_blocked_usage_request_count=0,
    )
    result = run_controlled_artifact_emission_usage_smoke_run(case)
    assert result.smoke_run_ok is True
    assert result.artifact_emission_usage_result is not None
    assert result.emitted_artifact_count == 0
    assert result.blocked_artifact_count == 1


def test_unknown_smoke_run_case_is_blocked_fail_closed() -> None:
    case = DiagnosticArtifactEmissionUsageSmokeRunCase(
        case_id="TEST-004",
        case_name="mystery smoke-run for leaderboard goblins",
        usage_context="local diagnostic artifact usage",
        artifact_families=("local diagnostic report JSON",),
        output_name_prefix="test-unknown",
        emission_purpose="unknown smoke run test",
    )
    result = run_controlled_artifact_emission_usage_smoke_run(case)
    assert result.smoke_run_ok is False
    assert result.blocked_reason == "UNKNOWN_SMOKE_RUN_CASE"
    assert result.artifact_emission_usage_result is None
    assert result.emitted_artifact_count == 0
    assert result.blocked_usage_request_count == 1


def test_forbidden_smoke_run_case_is_blocked_before_usage_execution() -> None:
    case = DiagnosticArtifactEmissionUsageSmokeRunCase(
        case_id="TEST-005",
        case_name="benchmark smoke-run",
        usage_context="local diagnostic artifact usage",
        artifact_families=("local diagnostic report JSON",),
        output_name_prefix="test-forbidden-smoke-case",
        emission_purpose="forbidden benchmark smoke-run case",
    )
    result = run_controlled_artifact_emission_usage_smoke_run(case)
    assert result.smoke_run_ok is False
    assert result.blocked_reason == "FORBIDDEN_SMOKE_RUN_CASE"
    assert result.artifact_emission_usage_result is None
    assert result.emitted_artifact_count == 0
    assert result.blocked_usage_request_count == 1


def test_default_smoke_run_suite_passes() -> None:
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    payload = suite.to_public_dict()
    assert suite.suite_result_id.startswith("SRSC-DIAG-ARTIFACT-SMOKE-SUITE-")
    assert suite.case_count == 8
    assert suite.passed_count == 8
    assert suite.failed_count == 0
    assert suite.suite_ok is True
    assert payload["pocV09Status"] == POC_V0_9_STATUS
    assert payload["pocV09Maturity"] == POC_V0_9_MATURITY
    assert payload["pocV09RuntimeImplemented"] is False
    assert payload["pocV09Benchmarked"] is False
    assert payload["benchmarkScoreClaimed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False


def test_batch_usage_smoke_run() -> None:
    batch_results = run_default_batch_usage_smoke_run()
    assert len(batch_results) == 2
    assert all(result.usage_ok for result in batch_results)
    assert [result.emitted_artifact_count for result in batch_results] == [1, 1]
    assert [result.blocked_artifact_count for result in batch_results] == [0, 0]
    assert [result.blocked_usage_request_count for result in batch_results] == [0, 0]


def test_smoke_run_boundary_flags_remain_closed() -> None:
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    payload = suite.to_public_dict()
    assert TASK_ID == "MILESTONE_19_TASK_109_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_IMPLEMENTATION_V1"
    assert SMOKE_RUN_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_STANDALONE_V1"
    assert CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED is True
    assert DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_ONLY is True
    assert USAGE_RUNNER_MODIFIED is False
    assert ARTIFACT_EMITTER_MODIFIED is False
    assert RUNTIME_SOLVER_MODIFIED is False
    assert RUNTIME_WIRING_ALLOWED is False
    assert SOLVER_RUNTIME_BINDING is False
    assert BENCHMARK_SCORE_CLAIMED is False
    assert KAGGLE_SUBMISSION_SENT is False
    assert PRIVATE_CORE_EXPOSURE is False
    assert LEGAL_CERTIFICATION is False
    assert FAIL_CLOSED_ACTIVE is True
    assert POC_V0_9_RUNTIME_IMPLEMENTED is False
    assert POC_V0_9_BENCHMARKED is False
    assert POC_V0_9_FAULT_INJECTION_PERFORMED is False
    assert POC_V0_9_PRODUCTION_READY is False
    assert payload["controlledArtifactEmissionUsageSmokeRunImplemented"] is True
    assert payload["diagnosticArtifactEmissionUsageSmokeRunOnly"] is True
    assert payload["usageRunnerModified"] is False
    assert payload["artifactEmitterModified"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["solverRuntimeBinding"] is False
    assert payload["benchmarkScoreClaimed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["privateCoreExposure"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True
