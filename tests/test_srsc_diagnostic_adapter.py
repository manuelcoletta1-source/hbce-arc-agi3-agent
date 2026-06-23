"""Tests for SRSC Diagnostic Adapter."""

from __future__ import annotations

import json

from hbce_arc_agi3.srsc_claim_ledger import ClaimState, EvidenceState
from hbce_arc_agi3.srsc_diagnostic_adapter import (
    ADAPTER_ACTIVATED,
    ADAPTER_IMPLEMENTED,
    ADAPTER_REVISION,
    DIAGNOSTIC_ADAPTER_LOCAL_ONLY,
    FAIL_CLOSED_ACTIVE,
    KAGGLE_SUBMISSION_SENT,
    LEGAL_CERTIFICATION,
    PRIVATE_CORE_EXPOSURE,
    RUNTIME_SOLVER_MODIFIED,
    RUNTIME_WIRING_ALLOWED,
    TASK_ID,
    DiagnosticAdapterInput,
    adapt_diagnostic_input_to_reference,
    adapt_diagnostic_inputs_to_references,
)
from hbce_arc_agi3.srsc_diagnostic_reference import DiagnosticReferenceSourceType


def _valid_payload() -> dict[str, object]:
    return {
        "source_type": "CROSS_TRACE_DIAGNOSTIC_PLANNER_RECORD",
        "source_path": "examples/milestone-19/srsc-diagnostic-adapter-planning-v1/task-87-manifest.json",
        "diagnostic_scope": "Task 89 adapter local implementation",
        "srsc_claim_id": "SRSC-CLAIM-12619C6F83128C07",
        "srsc_gate_decision_id": "SRSC-GATE-447AC5ED3C956D7E",
        "claim_state": "VERIFIED",
        "evidence_state": "PRESENT",
        "evidence_refs": ("src/hbce_arc_agi3/srsc_diagnostic_reference.py",),
        "approved_for_record": True,
        "approved_as_verified": True,
        "metadata": {"source": "task-89"},
    }


def test_adapter_input_is_deterministic() -> None:
    first = DiagnosticAdapterInput(**_valid_payload())
    second = DiagnosticAdapterInput(**_valid_payload())
    assert first.input_id == second.input_id
    assert first.input_id.startswith("SRSC-DIAG-ADAPTER-IN-")


def test_adapter_accepts_valid_payload() -> None:
    result = adapt_diagnostic_input_to_reference(_valid_payload())
    assert result.accepted_count == 1
    assert result.blocked_count == 0
    assert result.all_references_valid is True
    assert result.fail_closed_ok is True
    reference = result.accepted_references[0]
    assert reference.is_valid_reference is True
    assert reference.source_type == DiagnosticReferenceSourceType.CROSS_TRACE_DIAGNOSTIC_PLANNER_RECORD
    assert reference.srsc_claim_id == "SRSC-CLAIM-12619C6F83128C07"


def test_adapter_blocks_missing_evidence() -> None:
    payload = dict(_valid_payload())
    payload["evidence_state"] = "MISSING"
    payload["evidence_refs"] = ()
    result = adapt_diagnostic_input_to_reference(payload)
    assert result.accepted_count == 0
    assert result.blocked_count == 1
    assert result.blocked_references[0].reason == "REFERENCE_VALIDATION_FAILED"


def test_adapter_blocks_invalid_input_fail_closed() -> None:
    payload = dict(_valid_payload())
    payload["source_path"] = ""
    result = adapt_diagnostic_input_to_reference(payload)
    assert result.accepted_count == 0
    assert result.blocked_count == 1
    assert result.blocked_references[0].reason.startswith("INPUT_REJECTED:")


def test_adapter_blocks_non_srsc_identifiers() -> None:
    payload = dict(_valid_payload())
    payload["srsc_claim_id"] = "CLAIM-NOT-SRSC"
    payload["srsc_gate_decision_id"] = "GATE-NOT-SRSC"
    result = adapt_diagnostic_input_to_reference(payload)
    assert result.accepted_count == 0
    assert result.blocked_count == 1


def test_adapter_handles_batch_payloads() -> None:
    valid = _valid_payload()
    invalid = dict(_valid_payload())
    invalid["claim_state"] = "UNKNOWN"

    result = adapt_diagnostic_inputs_to_references([valid, invalid])
    assert result.accepted_count == 1
    assert result.blocked_count == 1
    assert result.fail_closed_ok is True


def test_adapter_result_json_is_deterministic_and_serializable() -> None:
    result = adapt_diagnostic_input_to_reference(_valid_payload())
    encoded = result.to_json()
    decoded = json.loads(encoded)

    assert decoded["resultId"] == result.result_id
    assert decoded["adapterRevision"] == ADAPTER_REVISION
    assert decoded["acceptedCount"] == 1
    assert decoded["blockedCount"] == 0
    assert decoded["adapterImplemented"] is True
    assert decoded["adapterActivated"] is False


def test_adapter_boundary_flags_remain_closed() -> None:
    result = adapt_diagnostic_input_to_reference(_valid_payload())
    payload = result.to_public_dict()

    assert ADAPTER_IMPLEMENTED is True
    assert ADAPTER_ACTIVATED is False
    assert DIAGNOSTIC_ADAPTER_LOCAL_ONLY is True
    assert RUNTIME_SOLVER_MODIFIED is False
    assert RUNTIME_WIRING_ALLOWED is False
    assert KAGGLE_SUBMISSION_SENT is False
    assert PRIVATE_CORE_EXPOSURE is False
    assert LEGAL_CERTIFICATION is False
    assert FAIL_CLOSED_ACTIVE is True

    assert payload["runtimeActivationAuthorized"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["candidateGeneratorModified"] is False
    assert payload["rankerModified"] is False
    assert payload["verifierModified"] is False
    assert payload["benchmarkScoreClaimed"] is False
    assert payload["realEvaluationPerformed"] is False
    assert payload["realSubmissionAuthorized"] is False
    assert payload["kaggleAuthenticationPerformed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["internetDuringEval"] is False
    assert payload["externalApiDependency"] is False
    assert payload["privateCoreExposure"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True


def test_adapter_accepts_enum_input() -> None:
    adapter_input = DiagnosticAdapterInput(
        source_type=DiagnosticReferenceSourceType.PUBLIC_SAFE_AUDIT_SUMMARY,
        source_path="docs/audit.md",
        diagnostic_scope="Enum input check",
        srsc_claim_id="SRSC-CLAIM-12619C6F83128C07",
        srsc_gate_decision_id="SRSC-GATE-447AC5ED3C956D7E",
        claim_state=ClaimState.REPORTED,
        evidence_state=EvidenceState.PRESENT,
        evidence_refs=("docs/audit.md",),
        approved_for_record=True,
    )
    result = adapt_diagnostic_input_to_reference(adapter_input)
    assert result.accepted_count == 1
    assert result.blocked_count == 0


def test_adapter_task_markers() -> None:
    assert TASK_ID == "MILESTONE_19_TASK_89_SRSC_DIAGNOSTIC_ADAPTER_LOCAL_IMPLEMENTATION_V1"
    assert ADAPTER_REVISION == "SRSC_DIAGNOSTIC_ADAPTER_LOCAL_STANDALONE_V1"
