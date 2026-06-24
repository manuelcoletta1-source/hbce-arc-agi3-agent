"""Tests for SRSC controlled diagnostic artifact emission usage runner."""

from __future__ import annotations

from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage import run_controlled_activation_usage
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_usage import (
    ACTIVATION_WRAPPER_MODIFIED,
    ADAPTER_MODIFIED,
    ARTIFACT_EMISSION_USAGE_REVISION,
    ARTIFACT_EMITTER_MODIFIED,
    AUTHORIZED_USAGE_CONTEXTS,
    BENCHMARK_BINDING,
    BENCHMARK_SCORE_CLAIMED,
    CANDIDATE_GENERATOR_BINDING,
    CANDIDATE_GENERATOR_MODIFIED,
    CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTED,
    DEFAULT_DIAGNOSTIC_ARTIFACT_FAMILIES,
    DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_ONLY,
    FAIL_CLOSED_ACTIVE,
    FORBIDDEN_USAGE_CONTEXTS,
    KAGGLE_SUBMISSION_BINDING,
    KAGGLE_SUBMISSION_SENT,
    LEGAL_CERTIFICATION,
    PRIVATE_CORE_EXPOSURE,
    RANKER_BINDING,
    RANKER_MODIFIED,
    RUNTIME_SOLVER_MODIFIED,
    RUNTIME_WIRING_ALLOWED,
    SOLVER_RUNTIME_BINDING,
    TASK_ID,
    USAGE_LAYER_MODIFIED,
    VERIFIER_BINDING,
    VERIFIER_MODIFIED,
    build_controlled_artifact_emission_usage_plan,
    run_controlled_artifact_emission_usage,
    run_controlled_artifact_emission_usage_batch,
)


def _valid_payload() -> dict[str, object]:
    return {
        "source_type": "CROSS_TRACE_DIAGNOSTIC_PLANNER_RECORD",
        "source_path": "examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-local-implementation-v1/task-105-manifest.json",
        "diagnostic_scope": "Task 105 controlled artifact emission usage",
        "srsc_claim_id": "SRSC-CLAIM-12619C6F83128C07",
        "srsc_gate_decision_id": "SRSC-GATE-447AC5ED3C956D7E",
        "claim_state": "VERIFIED",
        "evidence_state": "PRESENT",
        "evidence_refs": ("src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emitter.py",),
        "approved_for_record": True,
        "approved_as_verified": True,
        "metadata": {"source": "task-105"},
    }


def _usage_result():
    return run_controlled_activation_usage(
        _valid_payload(),
        usage_context="local SRSC diagnostic report generation",
        call_site="local diagnostic artifact emission usage tests",
        source_artifact_path="examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-local-implementation-v1/task-105-manifest.json",
        diagnostic_purpose="Task 105 local artifact emission usage",
    )


def test_build_controlled_artifact_emission_usage_plan() -> None:
    plan = build_controlled_artifact_emission_usage_plan(
        usage_context="local diagnostic artifact usage",
        artifact_families=("local diagnostic report JSON", "local deterministic index TXT"),
        output_name_prefix="task-105-diagnostic",
        emission_purpose="Task 105 plan check",
        milestone_id="MILESTONE_19",
        source_task_id=TASK_ID,
        metadata={"case": "plan"},
    )

    assert plan.plan_id.startswith("SRSC-DIAG-ARTIFACT-USAGE-PLAN-")
    assert plan.is_authorized_usage_context is True
    assert plan.is_forbidden_usage_context is False
    assert plan.canonical_usage_context == "local diagnostic artifact usage"
    assert plan.artifact_families == ("local diagnostic report JSON", "local deterministic index TXT")
    assert plan.to_public_dict()["noScoreClaimMarker"] is True
    assert plan.to_public_dict()["legalCertification"] is False


def test_run_controlled_artifact_emission_usage_emits_default_artifacts() -> None:
    result = run_controlled_artifact_emission_usage(
        _usage_result(),
        usage_context="local diagnostic artifact usage",
        output_name_prefix="task-105-default",
        emission_purpose="Task 105 default artifact emission usage",
        metadata={"case": "default"},
    )

    assert result.result_id.startswith("SRSC-DIAG-ARTIFACT-USAGE-RESULT-")
    assert result.usage_ok is True
    assert result.emitted_artifact_count == len(DEFAULT_DIAGNOSTIC_ARTIFACT_FAMILIES)
    assert result.blocked_artifact_count == 0
    assert result.blocked_usage_request_count == 0
    assert result.artifact_emission_result is not None
    assert result.artifact_emission_result.emission_ok is True

    payload = result.to_public_dict()
    assert payload["controlledArtifactEmissionUsageImplemented"] is True
    assert payload["diagnosticArtifactEmissionUsageOnly"] is True
    assert payload["artifactEmitterModified"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False


def test_run_controlled_artifact_emission_usage_allows_custom_diagnostic_families() -> None:
    result = run_controlled_artifact_emission_usage(
        _usage_result(),
        usage_context="local milestone artifact bundle usage",
        artifact_families=(
            "local diagnostic report JSON",
            "local public-safe audit summary JSON",
            "local deterministic index TXT",
        ),
        output_name_prefix="task-105-bundle",
        emission_purpose="Task 105 bundle emission usage",
    )

    assert result.usage_ok is True
    assert result.emitted_artifact_count == 3
    assert result.blocked_artifact_count == 0
    assert result.blocked_usage_request_count == 0
    assert result.artifact_emission_result is not None
    assert [artifact.content_type for artifact in result.artifact_emission_result.artifacts] == [
        "application/json",
        "application/json",
        "text/plain",
    ]


def test_run_controlled_artifact_emission_usage_blocks_forbidden_usage_context() -> None:
    result = run_controlled_artifact_emission_usage(
        _usage_result(),
        usage_context="benchmark artifact usage",
        output_name_prefix="task-105-forbidden",
        emission_purpose="Forbidden benchmark usage",
    )

    assert result.usage_ok is True
    assert result.emitted_artifact_count == 0
    assert result.blocked_artifact_count == 0
    assert result.blocked_usage_request_count == 1
    assert result.artifact_emission_result is None
    assert result.blocked_requests[0].reason == "FORBIDDEN_USAGE_CONTEXT"


def test_run_controlled_artifact_emission_usage_blocks_unknown_usage_context() -> None:
    result = run_controlled_artifact_emission_usage(
        _usage_result(),
        usage_context="mystery artifact carnival",
        output_name_prefix="task-105-unknown",
        emission_purpose="Unknown usage context",
    )

    assert result.usage_ok is True
    assert result.emitted_artifact_count == 0
    assert result.blocked_usage_request_count == 1
    assert result.blocked_requests[0].reason == "UNKNOWN_USAGE_CONTEXT"


def test_run_controlled_artifact_emission_usage_preserves_emitter_family_blocks() -> None:
    result = run_controlled_artifact_emission_usage(
        _usage_result(),
        usage_context="local diagnostic artifact usage",
        artifact_families=(
            "local diagnostic report JSON",
            "score report",
            "local deterministic index TXT",
        ),
        output_name_prefix="task-105-family-block",
        emission_purpose="Task 105 family block check",
    )

    assert result.usage_ok is True
    assert result.emitted_artifact_count == 2
    assert result.blocked_artifact_count == 1
    assert result.blocked_usage_request_count == 0
    assert result.artifact_emission_result is not None
    assert result.artifact_emission_result.blocked_requests[0].reason == "FORBIDDEN_ARTIFACT_FAMILY"


def test_run_controlled_artifact_emission_usage_batch() -> None:
    usage_a = _usage_result()
    usage_b = _usage_result()
    results = run_controlled_artifact_emission_usage_batch(
        (usage_a, usage_b),
        usage_context="local deterministic index artifact usage",
        artifact_families=("local deterministic index TXT",),
        output_name_prefix="task-105-batch",
        emission_purpose="Task 105 batch usage",
    )

    assert len(results) == 2
    assert all(result.usage_ok for result in results)
    assert [result.emitted_artifact_count for result in results] == [1, 1]
    assert results[0].usage_request.usage_plan.output_name_prefix == "task-105-batch-01"
    assert results[1].usage_request.usage_plan.output_name_prefix == "task-105-batch-02"


def test_usage_context_registries_are_explicit() -> None:
    assert "local diagnostic artifact usage" in AUTHORIZED_USAGE_CONTEXTS
    assert "local milestone artifact bundle usage" in AUTHORIZED_USAGE_CONTEXTS
    assert "local evidence package artifact usage" in AUTHORIZED_USAGE_CONTEXTS
    assert "local public-safe audit artifact usage" in AUTHORIZED_USAGE_CONTEXTS
    assert "local deterministic index artifact usage" in AUTHORIZED_USAGE_CONTEXTS

    assert "solver runtime artifact usage" in FORBIDDEN_USAGE_CONTEXTS
    assert "candidate generator artifact usage" in FORBIDDEN_USAGE_CONTEXTS
    assert "ranker score artifact usage" in FORBIDDEN_USAGE_CONTEXTS
    assert "verifier score artifact usage" in FORBIDDEN_USAGE_CONTEXTS
    assert "benchmark artifact usage" in FORBIDDEN_USAGE_CONTEXTS
    assert "Kaggle submission artifact usage" in FORBIDDEN_USAGE_CONTEXTS
    assert "legal certification artifact usage" in FORBIDDEN_USAGE_CONTEXTS


def test_artifact_emission_usage_boundary_flags_remain_closed() -> None:
    result = run_controlled_artifact_emission_usage(
        _usage_result(),
        usage_context="local diagnostic artifact usage",
        output_name_prefix="task-105-boundary",
        emission_purpose="Task 105 boundary check",
    )
    payload = result.to_public_dict()

    assert CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTED is True
    assert DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_ONLY is True
    assert ARTIFACT_EMITTER_MODIFIED is False
    assert USAGE_LAYER_MODIFIED is False
    assert ACTIVATION_WRAPPER_MODIFIED is False
    assert ADAPTER_MODIFIED is False
    assert RUNTIME_SOLVER_MODIFIED is False
    assert RUNTIME_WIRING_ALLOWED is False
    assert SOLVER_RUNTIME_BINDING is False
    assert CANDIDATE_GENERATOR_MODIFIED is False
    assert CANDIDATE_GENERATOR_BINDING is False
    assert RANKER_MODIFIED is False
    assert RANKER_BINDING is False
    assert VERIFIER_MODIFIED is False
    assert VERIFIER_BINDING is False
    assert BENCHMARK_SCORE_CLAIMED is False
    assert BENCHMARK_BINDING is False
    assert KAGGLE_SUBMISSION_SENT is False
    assert KAGGLE_SUBMISSION_BINDING is False
    assert PRIVATE_CORE_EXPOSURE is False
    assert LEGAL_CERTIFICATION is False
    assert FAIL_CLOSED_ACTIVE is True

    assert payload["controlledArtifactEmissionUsageImplemented"] is True
    assert payload["diagnosticArtifactEmissionUsageOnly"] is True
    assert payload["artifactEmitterModified"] is False
    assert payload["usageLayerModified"] is False
    assert payload["activationWrapperModified"] is False
    assert payload["adapterModified"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["solverRuntimeBinding"] is False
    assert payload["benchmarkScoreClaimed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True


def test_artifact_emission_usage_task_markers() -> None:
    assert TASK_ID == "MILESTONE_19_TASK_105_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_LOCAL_IMPLEMENTATION_V1"
    assert ARTIFACT_EMISSION_USAGE_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_LOCAL_STANDALONE_V1"
