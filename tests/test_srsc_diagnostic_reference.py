"""Tests for SRSC Diagnostic Reference Record schema."""

from __future__ import annotations

import json
import pytest

from hbce_arc_agi3.srsc_claim_ledger import ClaimState, EvidenceState
from hbce_arc_agi3.srsc_diagnostic_reference import (
    BENCHMARK_SCORE_CLAIMED,
    CANDIDATE_GENERATOR_MODIFIED,
    DiagnosticReferenceBoundary,
    DiagnosticReferenceSourceType,
    EXTERNAL_API_DEPENDENCY,
    INTERNET_DURING_EVAL,
    RANKER_MODIFIED,
    REAL_EVALUATION_PERFORMED,
    REAL_SUBMISSION_AUTHORIZED,
    RUNTIME_ACTIVATION_AUTHORIZED,
    SCHEMA_REVISION,
    TASK_ID,
    VERIFIER_MODIFIED,
    create_diagnostic_reference_record,
)


def _valid_record():
    return create_diagnostic_reference_record(
        source_type=DiagnosticReferenceSourceType.CROSS_TRACE_DIAGNOSTIC_PLANNER_RECORD,
        source_path="examples/milestone-19/srsc-diagnostic-reference-planning-v1/task-83-manifest.json",
        srsc_claim_id="SRSC-CLAIM-12619C6F83128C07",
        srsc_gate_decision_id="SRSC-GATE-447AC5ED3C956D7E",
        claim_state=ClaimState.VERIFIED,
        evidence_state=EvidenceState.PRESENT,
        evidence_refs=["src/hbce_arc_agi3/srsc_claim_ledger.py", "src/hbce_arc_agi3/srsc_evidence_gate.py"],
        diagnostic_scope="Task 85 schema local implementation",
        approved_for_record=True,
        approved_as_verified=True,
    )


def test_diagnostic_reference_record_is_deterministic() -> None:
    first = _valid_record()
    second = _valid_record()
    assert first.diagnostic_reference_id == second.diagnostic_reference_id
    assert first.diagnostic_reference_id.startswith("SRSC-DIAG-REF-")


def test_diagnostic_reference_record_is_valid_when_public_safe_and_evidence_present() -> None:
    record = _valid_record()
    assert record.is_valid_reference is True
    assert record.has_srsc_identifiers is True
    assert record.has_evidence is True
    assert record.is_runtime_isolated is True


def test_diagnostic_reference_record_public_payload_contains_boundary_flags() -> None:
    payload = _valid_record().to_public_dict()
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


def test_diagnostic_reference_record_rejects_missing_evidence() -> None:
    record = create_diagnostic_reference_record(
        source_type="PUBLIC_SAFE_AUDIT_SUMMARY",
        source_path="docs/audit.md",
        srsc_claim_id="SRSC-CLAIM-12619C6F83128C07",
        srsc_gate_decision_id="SRSC-GATE-447AC5ED3C956D7E",
        claim_state="VERIFIED",
        evidence_state="MISSING",
        evidence_refs=[],
        diagnostic_scope="Missing evidence check",
        approved_for_record=True,
        approved_as_verified=True,
    )
    assert record.is_valid_reference is False


def test_diagnostic_reference_record_rejects_non_srsc_identifiers() -> None:
    record = create_diagnostic_reference_record(
        source_type="LOCAL_CLAIM_REVIEW_REPORT",
        source_path="docs/report.md",
        srsc_claim_id="CLAIM-NOT-SRSC",
        srsc_gate_decision_id="GATE-NOT-SRSC",
        claim_state="REPORTED",
        evidence_state="PRESENT",
        evidence_refs=["docs/report.md"],
        diagnostic_scope="Identifier check",
        approved_for_record=True,
        approved_as_verified=False,
    )
    assert record.is_valid_reference is False


def test_diagnostic_reference_record_rejects_blocked_boundary() -> None:
    record = create_diagnostic_reference_record(
        source_type="EVIDENCE_BOUND_DIAGNOSTIC_NOTE",
        source_path="docs/note.md",
        srsc_claim_id="SRSC-CLAIM-12619C6F83128C07",
        srsc_gate_decision_id="SRSC-GATE-447AC5ED3C956D7E",
        claim_state="REPORTED",
        evidence_state="PRESENT",
        evidence_refs=["docs/note.md"],
        diagnostic_scope="Boundary check",
        boundary_state=DiagnosticReferenceBoundary.BLOCKED_RUNTIME_WIRING,
        approved_for_record=True,
    )
    assert record.is_valid_reference is False


def test_diagnostic_reference_record_rejects_verified_without_record_approval() -> None:
    record = create_diagnostic_reference_record(
        source_type="MILESTONE_CLOSURE_RECORD",
        source_path="docs/closure.md",
        srsc_claim_id="SRSC-CLAIM-12619C6F83128C07",
        srsc_gate_decision_id="SRSC-GATE-447AC5ED3C956D7E",
        claim_state="VERIFIED",
        evidence_state="PRESENT",
        evidence_refs=["docs/closure.md"],
        diagnostic_scope="Approval consistency check",
        approved_for_record=False,
        approved_as_verified=True,
    )
    assert record.is_valid_reference is False


def test_diagnostic_reference_record_rejects_unknown_claim_state() -> None:
    record = create_diagnostic_reference_record(
        source_type="SOURCE_FILE_EVIDENCE_NOTE",
        source_path="src/hbce_arc_agi3/srsc_diagnostic_reference.py",
        srsc_claim_id="SRSC-CLAIM-12619C6F83128C07",
        srsc_gate_decision_id="SRSC-GATE-447AC5ED3C956D7E",
        claim_state="UNKNOWN",
        evidence_state="PRESENT",
        evidence_refs=["src/hbce_arc_agi3/srsc_diagnostic_reference.py"],
        diagnostic_scope="Unknown claim check",
        approved_for_record=True,
    )
    assert record.is_valid_reference is False


def test_diagnostic_reference_record_source_types_are_diagnostic_only() -> None:
    values = {item.value for item in DiagnosticReferenceSourceType}
    assert "CROSS_TRACE_DIAGNOSTIC_PLANNER_RECORD" in values
    assert "PUBLIC_SAFE_AUDIT_SUMMARY" in values
    assert "LOCAL_CLAIM_REVIEW_REPORT" in values
    assert "EVIDENCE_BOUND_DIAGNOSTIC_NOTE" in values
    assert "MILESTONE_CLOSURE_RECORD" in values
    assert "SOURCE_FILE_EVIDENCE_NOTE" in values
    assert all("SOLVER_RUNTIME" not in value for value in values)
    assert all("KAGGLE_SUBMISSION" not in value for value in values)


def test_diagnostic_reference_record_json_is_deterministic_and_serializable() -> None:
    record = create_diagnostic_reference_record(
        source_type="PUBLIC_SAFE_AUDIT_SUMMARY",
        source_path="docs/audit.md",
        srsc_claim_id="SRSC-CLAIM-12619C6F83128C07",
        srsc_gate_decision_id="SRSC-GATE-447AC5ED3C956D7E",
        claim_state="HYPOTHESIS",
        evidence_state="PRESENT",
        evidence_refs=["docs/audit.md"],
        diagnostic_scope="Serialization check",
        approved_for_record=True,
        approved_as_verified=False,
        metadata={"z": 3, "a": 1},
    )
    encoded = record.to_json()
    decoded = json.loads(encoded)
    assert decoded["diagnosticReferenceId"] == record.diagnostic_reference_id
    assert decoded["metadata"] == {"a": 1, "z": 3}


def test_diagnostic_reference_record_rejects_empty_fields() -> None:
    with pytest.raises(ValueError):
        create_diagnostic_reference_record(
            source_type="PUBLIC_SAFE_AUDIT_SUMMARY",
            source_path="",
            srsc_claim_id="SRSC-CLAIM-12619C6F83128C07",
            srsc_gate_decision_id="SRSC-GATE-447AC5ED3C956D7E",
            claim_state="REPORTED",
            evidence_state="PRESENT",
            evidence_refs=["docs/audit.md"],
            diagnostic_scope="Serialization check",
        )


def test_task_85_schema_markers() -> None:
    assert TASK_ID == "MILESTONE_19_TASK_85_SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_LOCAL_IMPLEMENTATION_V1"
    assert SCHEMA_REVISION == "SRSC_DIAGNOSTIC_REFERENCE_RECORD_SCHEMA_LOCAL_STANDALONE_V1"
    assert RUNTIME_ACTIVATION_AUTHORIZED is False
    assert CANDIDATE_GENERATOR_MODIFIED is False
    assert RANKER_MODIFIED is False
    assert VERIFIER_MODIFIED is False
    assert BENCHMARK_SCORE_CLAIMED is False
    assert REAL_EVALUATION_PERFORMED is False
    assert REAL_SUBMISSION_AUTHORIZED is False
    assert INTERNET_DURING_EVAL is False
    assert EXTERNAL_API_DEPENDENCY is False
