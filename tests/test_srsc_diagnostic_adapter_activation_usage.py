"""Tests for SRSC Diagnostic Adapter Controlled Activation Usage Layer."""

from __future__ import annotations

import json

from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage import (
    ACTIVATION_WRAPPER_MODIFIED,
    ADAPTER_MODIFIED,
    ALLOWED_USAGE_CONTEXTS,
    BENCHMARK_BINDING,
    BENCHMARK_SCORE_CLAIMED,
    CANDIDATE_GENERATOR_BINDING,
    CANDIDATE_GENERATOR_MODIFIED,
    CONTROLLED_USAGE_IMPLEMENTED,
    DIAGNOSTIC_USAGE_ONLY,
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
    USAGE_REVISION,
    VERIFIER_BINDING,
    VERIFIER_MODIFIED,
    DiagnosticActivationUsageRequest,
    run_controlled_activation_usage,
    run_controlled_activation_usage_batch,
)


def _valid_payload() -> dict[str, object]:
    return {
        "source_type": "CROSS_TRACE_DIAGNOSTIC_PLANNER_RECORD",
        "source_path": "examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-planning-v1/task-95-manifest.json",
        "diagnostic_scope": "Task 97 controlled diagnostic usage",
        "srsc_claim_id": "SRSC-CLAIM-12619C6F83128C07",
        "srsc_gate_decision_id": "SRSC-GATE-447AC5ED3C956D7E",
        "claim_state": "VERIFIED",
        "evidence_state": "PRESENT",
        "evidence_refs": ("src/hbce_arc_agi3/srsc_diagnostic_adapter_activation.py",),
        "approved_for_record": True,
        "approved_as_verified": True,
        "metadata": {"source": "task-97"},
    }


def _run_valid_usage():
    return run_controlled_activation_usage(
        _valid_payload(),
        usage_context="local SRSC diagnostic report generation",
        call_site="local diagnostic scripts",
        source_artifact_path="examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-planning-v1/task-95-manifest.json",
        diagnostic_purpose="Task 97 local usage check",
    )


def test_usage_request_classifies_allowed_context() -> None:
    request = DiagnosticActivationUsageRequest(
        usage_context="local SRSC diagnostic report generation",
        call_site="local diagnostic scripts",
        diagnostic_payload=_valid_payload(),
        source_artifact_path="examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-planning-v1/task-95-manifest.json",
        diagnostic_purpose="Task 97 request classification",
    )

    assert request.request_id.startswith("SRSC-DIAG-ACT-USAGE-REQ-")
    assert request.is_allowed_usage_context is True
    assert request.is_forbidden_usage_context is False
    assert request.to_public_dict()["noScoreClaimMarker"] is True
    assert request.to_public_dict()["noSubmissionMarker"] is True


def test_usage_accepts_allowed_context_and_call_site() -> None:
    result = _run_valid_usage()

    assert result.accepted_count == 1
    assert result.blocked_reference_count == 0
    assert result.blocked_call_count == 0
    assert result.blocked_usage_request_count == 0
    assert result.usage_ok is True
    assert result.activation_result.accepted_count == 1


def test_usage_blocks_forbidden_usage_context() -> None:
    result = run_controlled_activation_usage(
        _valid_payload(),
        usage_context="solver runtime execution",
        call_site="local diagnostic scripts",
        source_artifact_path="examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-planning-v1/task-95-manifest.json",
        diagnostic_purpose="Forbidden runtime usage",
    )

    assert result.accepted_count == 0
    assert result.blocked_reference_count == 0
    assert result.blocked_call_count == 0
    assert result.blocked_usage_request_count == 1
    assert result.blocked_requests[0].reason == "FORBIDDEN_USAGE_CONTEXT"
    assert result.usage_ok is True


def test_usage_blocks_unknown_usage_context() -> None:
    result = run_controlled_activation_usage(
        _valid_payload(),
        usage_context="experimental magical runtime bridge",
        call_site="local diagnostic scripts",
        source_artifact_path="examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-planning-v1/task-95-manifest.json",
        diagnostic_purpose="Unknown usage context",
    )

    assert result.accepted_count == 0
    assert result.blocked_usage_request_count == 1
    assert result.blocked_requests[0].reason == "UNKNOWN_USAGE_CONTEXT"


def test_usage_allows_activation_to_block_forbidden_call_site() -> None:
    result = run_controlled_activation_usage(
        _valid_payload(),
        usage_context="local SRSC diagnostic report generation",
        call_site="solver runtime loop",
        source_artifact_path="examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-planning-v1/task-95-manifest.json",
        diagnostic_purpose="Forbidden call site check",
    )

    assert result.accepted_count == 0
    assert result.blocked_usage_request_count == 0
    assert result.blocked_call_count == 1
    assert result.activation_result.blocked_calls[0].reason == "FORBIDDEN_CALL_SITE"
    assert result.usage_ok is True


def test_usage_batch_records_accepted_and_blocked_reference_counts() -> None:
    valid = _valid_payload()
    invalid = dict(_valid_payload())
    invalid["evidence_state"] = "MISSING"
    invalid["evidence_refs"] = ()

    result = run_controlled_activation_usage_batch(
        [valid, invalid],
        usage_context="local cross-trace planner evidence attachment",
        call_site="cross-trace diagnostic planners",
        source_artifact_path="examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-planning-v1/task-95-manifest.json",
        diagnostic_purpose="Task 97 batch usage",
    )

    assert result.accepted_count == 1
    assert result.blocked_reference_count == 1
    assert result.blocked_call_count == 0
    assert result.blocked_usage_request_count == 0
    assert result.usage_ok is True


def test_usage_batch_blocks_forbidden_context_before_activation() -> None:
    result = run_controlled_activation_usage_batch(
        [_valid_payload()],
        usage_context="benchmark execution",
        call_site="cross-trace diagnostic planners",
        source_artifact_path="examples/milestone-19/srsc-diagnostic-adapter-controlled-activation-usage-planning-v1/task-95-manifest.json",
        diagnostic_purpose="Forbidden benchmark usage",
    )

    assert result.accepted_count == 0
    assert result.blocked_reference_count == 0
    assert result.blocked_call_count == 0
    assert result.blocked_usage_request_count == 1
    assert result.blocked_requests[0].reason == "FORBIDDEN_USAGE_CONTEXT"


def test_usage_json_is_deterministic_and_serializable() -> None:
    result = _run_valid_usage()
    encoded = result.to_json()
    decoded = json.loads(encoded)

    assert decoded["resultId"] == result.result_id
    assert decoded["usageRevision"] == USAGE_REVISION
    assert decoded["acceptedCount"] == 1
    assert decoded["blockedUsageRequestCount"] == 0
    assert decoded["controlledUsageImplemented"] is True
    assert decoded["diagnosticUsageOnly"] is True
    assert decoded["noScoreClaimMarker"] is True
    assert decoded["noSubmissionMarker"] is True


def test_usage_boundary_flags_remain_closed() -> None:
    result = _run_valid_usage()
    payload = result.to_public_dict()

    assert CONTROLLED_USAGE_IMPLEMENTED is True
    assert DIAGNOSTIC_USAGE_ONLY is True
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

    assert payload["activationWrapperModified"] is False
    assert payload["adapterModified"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["solverRuntimeBinding"] is False
    assert payload["candidateGeneratorModified"] is False
    assert payload["candidateGeneratorBinding"] is False
    assert payload["rankerModified"] is False
    assert payload["rankerBinding"] is False
    assert payload["verifierModified"] is False
    assert payload["verifierBinding"] is False
    assert payload["benchmarkScoreClaimed"] is False
    assert payload["benchmarkBinding"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["kaggleSubmissionBinding"] is False
    assert payload["privateCoreExposure"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True


def test_usage_context_registry_is_explicit() -> None:
    assert "local SRSC diagnostic report generation" in ALLOWED_USAGE_CONTEXTS
    assert "local milestone evidence packaging" in ALLOWED_USAGE_CONTEXTS
    assert "local public-safe audit summary creation" in ALLOWED_USAGE_CONTEXTS
    assert "local cross-trace planner evidence attachment" in ALLOWED_USAGE_CONTEXTS
    assert "local blocked-call report generation" in ALLOWED_USAGE_CONTEXTS

    assert "solver runtime execution" in FORBIDDEN_USAGE_CONTEXTS
    assert "candidate generation" in FORBIDDEN_USAGE_CONTEXTS
    assert "candidate ranking" in FORBIDDEN_USAGE_CONTEXTS
    assert "verifier execution" in FORBIDDEN_USAGE_CONTEXTS
    assert "benchmark execution" in FORBIDDEN_USAGE_CONTEXTS
    assert "Kaggle submission packaging" in FORBIDDEN_USAGE_CONTEXTS
    assert "network/API execution" in FORBIDDEN_USAGE_CONTEXTS


def test_usage_task_markers() -> None:
    assert TASK_ID == "MILESTONE_19_TASK_97_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_LOCAL_IMPLEMENTATION_V1"
    assert USAGE_REVISION == "SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_LOCAL_STANDALONE_V1"
