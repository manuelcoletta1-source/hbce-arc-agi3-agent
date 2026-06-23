"""Tests for SRSC Diagnostic Adapter Controlled Activation."""

from __future__ import annotations

import json

from hbce_arc_agi3.srsc_diagnostic_adapter_activation import (
    ACTIVATION_REVISION,
    ADAPTER_ACTIVATED_FOR_DIAGNOSTIC_PATH_ONLY,
    ALLOWED_CALL_SITES,
    BENCHMARK_BINDING,
    BENCHMARK_SCORE_CLAIMED,
    CANDIDATE_GENERATOR_BINDING,
    CANDIDATE_GENERATOR_MODIFIED,
    CONTROLLED_ACTIVATION_IMPLEMENTED,
    DIAGNOSTIC_ONLY_ACTIVATION,
    FAIL_CLOSED_ACTIVE,
    FORBIDDEN_CALL_SITES,
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
    VERIFIER_BINDING,
    VERIFIER_MODIFIED,
    DiagnosticAdapterActivationInput,
    activate_diagnostic_adapter_batch_for_diagnostic_path,
    activate_diagnostic_adapter_for_diagnostic_path,
)


def _valid_payload() -> dict[str, object]:
    return {
        "source_type": "CROSS_TRACE_DIAGNOSTIC_PLANNER_RECORD",
        "source_path": "examples/milestone-19/srsc-diagnostic-adapter-activation-planning-v1/task-91-manifest.json",
        "diagnostic_scope": "Task 93 controlled diagnostic activation",
        "srsc_claim_id": "SRSC-CLAIM-12619C6F83128C07",
        "srsc_gate_decision_id": "SRSC-GATE-447AC5ED3C956D7E",
        "claim_state": "VERIFIED",
        "evidence_state": "PRESENT",
        "evidence_refs": ("src/hbce_arc_agi3/srsc_diagnostic_adapter.py",),
        "approved_for_record": True,
        "approved_as_verified": True,
        "metadata": {"source": "task-93"},
    }


def test_activation_input_classifies_allowed_call_site() -> None:
    activation_input = DiagnosticAdapterActivationInput(
        call_site="local diagnostic scripts",
        diagnostic_payload=_valid_payload(),
    )

    assert activation_input.input_id.startswith("SRSC-DIAG-ACT-IN-")
    assert activation_input.is_allowed_call_site is True
    assert activation_input.is_forbidden_call_site is False


def test_activation_accepts_allowed_diagnostic_call_site() -> None:
    result = activate_diagnostic_adapter_for_diagnostic_path(
        _valid_payload(),
        call_site="local diagnostic scripts",
    )

    assert result.accepted_count == 1
    assert result.blocked_reference_count == 0
    assert result.blocked_call_count == 0
    assert result.diagnostic_activation_ok is True
    assert result.adapter_result.accepted_count == 1


def test_activation_blocks_forbidden_solver_call_site() -> None:
    result = activate_diagnostic_adapter_for_diagnostic_path(
        _valid_payload(),
        call_site="solver runtime loop",
    )

    assert result.accepted_count == 0
    assert result.blocked_reference_count == 0
    assert result.blocked_call_count == 1
    assert result.blocked_calls[0].reason == "FORBIDDEN_CALL_SITE"
    assert result.diagnostic_activation_ok is True


def test_activation_blocks_unknown_call_site() -> None:
    result = activate_diagnostic_adapter_for_diagnostic_path(
        _valid_payload(),
        call_site="random experimental runtime hook",
    )

    assert result.accepted_count == 0
    assert result.blocked_call_count == 1
    assert result.blocked_calls[0].reason == "UNKNOWN_CALL_SITE"


def test_activation_allows_batch_for_diagnostic_path() -> None:
    valid = _valid_payload()
    invalid = dict(_valid_payload())
    invalid["evidence_state"] = "MISSING"
    invalid["evidence_refs"] = ()

    result = activate_diagnostic_adapter_batch_for_diagnostic_path(
        [valid, invalid],
        call_site="cross-trace diagnostic planners",
    )

    assert result.accepted_count == 1
    assert result.blocked_reference_count == 1
    assert result.blocked_call_count == 0
    assert result.diagnostic_activation_ok is True


def test_activation_batch_blocks_forbidden_call_site_without_adapter_records() -> None:
    result = activate_diagnostic_adapter_batch_for_diagnostic_path(
        [_valid_payload()],
        call_site="benchmark executor",
    )

    assert result.accepted_count == 0
    assert result.blocked_reference_count == 0
    assert result.blocked_call_count == 1
    assert result.blocked_calls[0].reason == "FORBIDDEN_CALL_SITE"


def test_activation_json_is_deterministic_and_serializable() -> None:
    result = activate_diagnostic_adapter_for_diagnostic_path(
        _valid_payload(),
        call_site="public-safe audit artifact builders",
    )

    encoded = result.to_json()
    decoded = json.loads(encoded)

    assert decoded["resultId"] == result.result_id
    assert decoded["activationRevision"] == ACTIVATION_REVISION
    assert decoded["acceptedCount"] == 1
    assert decoded["blockedCallCount"] == 0
    assert decoded["controlledActivationImplemented"] is True
    assert decoded["diagnosticOnlyActivation"] is True


def test_activation_boundary_flags_remain_closed() -> None:
    result = activate_diagnostic_adapter_for_diagnostic_path(
        _valid_payload(),
        call_site="milestone closure evidence builders",
    )
    payload = result.to_public_dict()

    assert CONTROLLED_ACTIVATION_IMPLEMENTED is True
    assert DIAGNOSTIC_ONLY_ACTIVATION is True
    assert ADAPTER_ACTIVATED_FOR_DIAGNOSTIC_PATH_ONLY is True
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

    assert payload["runtimeActivationAuthorized"] is False
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


def test_activation_call_site_registry_is_explicit() -> None:
    assert "local diagnostic scripts" in ALLOWED_CALL_SITES
    assert "cross-trace diagnostic planners" in ALLOWED_CALL_SITES

    assert "solver runtime loop" in FORBIDDEN_CALL_SITES
    assert "candidate generator" in FORBIDDEN_CALL_SITES
    assert "candidate ranker" in FORBIDDEN_CALL_SITES
    assert "verifier" in FORBIDDEN_CALL_SITES
    assert "benchmark executor" in FORBIDDEN_CALL_SITES
    assert "Kaggle submission package builder" in FORBIDDEN_CALL_SITES


def test_activation_task_markers() -> None:
    assert TASK_ID == "MILESTONE_19_TASK_93_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_LOCAL_IMPLEMENTATION_V1"
    assert ACTIVATION_REVISION == "SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_LOCAL_STANDALONE_V1"
