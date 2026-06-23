"""Tests for SRSC Evidence Gate."""

from __future__ import annotations

from hbce_arc_agi3.srsc_claim_ledger import (
    BoundaryState,
    ClaimState,
    EvidenceState,
    create_claim_record,
)
from hbce_arc_agi3.srsc_evidence_gate import (
    GATE_REVISION,
    evaluate_claim_record,
    evaluate_claim_records,
)


def test_evidence_gate_approves_verified_claim_with_present_evidence() -> None:
    record = create_claim_record(
        claim_text="Claim ledger module exists.",
        claim_state=ClaimState.VERIFIED,
        evidence_state=EvidenceState.PRESENT,
        evidence_refs=["src/hbce_arc_agi3/srsc_claim_ledger.py"],
        scope="Task 81 local implementation",
    )
    decision = evaluate_claim_record(record)
    assert decision.gate_status == "APPROVED_VERIFIED_CLAIM"
    assert decision.approved_for_record is True
    assert decision.approved_as_verified is True
    assert "VERIFIED_WITH_PRESENT_EVIDENCE_PUBLIC_SAFE" in decision.reasons
    assert decision.decision_id.startswith("SRSC-GATE-")


def test_evidence_gate_allows_hypothesis_as_record_not_verified() -> None:
    record = create_claim_record(
        claim_text="Future wiring may use the claim ledger after separate authorization.",
        claim_state=ClaimState.HYPOTHESIS,
        evidence_state=EvidenceState.PRESENT,
        evidence_refs=["docs/milestone-19-task-80-srsc-claim-ledger-implementation-authorization-review-v1.md"],
        scope="Future planning",
    )
    decision = evaluate_claim_record(record)
    assert decision.gate_status == "APPROVED_NON_VERIFIED_RECORD"
    assert decision.approved_for_record is True
    assert decision.approved_as_verified is False
    assert "RECORDABLE_HYPOTHESIS" in decision.reasons


def test_evidence_gate_blocks_missing_evidence() -> None:
    record = create_claim_record(
        claim_text="Missing evidence blocks the claim.",
        claim_state=ClaimState.VERIFIED,
        evidence_state=EvidenceState.MISSING,
        evidence_refs=[],
        scope="Fail closed check",
    )
    decision = evaluate_claim_record(record)
    assert decision.gate_status == "BLOCKED_FAIL_CLOSED"
    assert decision.approved_for_record is False
    assert decision.approved_as_verified is False
    assert "EVIDENCE_STATE_MISSING" in decision.reasons
    assert "EVIDENCE_REFS_MISSING" in decision.reasons


def test_evidence_gate_blocks_unknown_claim_state() -> None:
    record = create_claim_record(
        claim_text="Unknown remains blocked.",
        claim_state=ClaimState.UNKNOWN,
        evidence_state=EvidenceState.PRESENT,
        evidence_refs=["some-source"],
        scope="Fail closed check",
    )
    decision = evaluate_claim_record(record)
    assert decision.gate_status == "BLOCKED_FAIL_CLOSED"
    assert "CLAIM_STATE_UNKNOWN" in decision.reasons


def test_evidence_gate_blocks_private_boundary() -> None:
    record = create_claim_record(
        claim_text="Private boundary blocks the record.",
        claim_state=ClaimState.REPORTED,
        evidence_state=EvidenceState.PRESENT,
        evidence_refs=["some-source"],
        scope="Boundary check",
        boundary_state=BoundaryState.BLOCKED_PRIVATE,
    )
    decision = evaluate_claim_record(record)
    assert decision.gate_status == "BLOCKED_FAIL_CLOSED"
    assert "BOUNDARY_BLOCKED_PRIVATE" in decision.reasons


def test_evidence_gate_multiple_records() -> None:
    approved = create_claim_record(
        claim_text="Approved record.",
        claim_state=ClaimState.REPORTED,
        evidence_state=EvidenceState.PRESENT,
        evidence_refs=["source-a"],
        scope="Batch check",
    )
    blocked = create_claim_record(
        claim_text="Blocked record.",
        claim_state=ClaimState.CONFLICTING,
        evidence_state=EvidenceState.CONFLICTING,
        evidence_refs=["source-b"],
        scope="Batch check",
    )
    decisions = evaluate_claim_records([approved, blocked])
    assert len(decisions) == 2
    assert decisions[0].approved_for_record is True
    assert decisions[1].approved_for_record is False


def test_evidence_gate_boundary_flags_remain_fail_closed() -> None:
    record = create_claim_record(
        claim_text="Gate remains standalone.",
        claim_state=ClaimState.VERIFIED,
        evidence_state=EvidenceState.PRESENT,
        evidence_refs=["tests/test_srsc_evidence_gate.py"],
        scope="Boundary check",
    )
    decision = evaluate_claim_record(record)
    payload = decision.to_public_dict()
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["privateCoreExposure"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True


def test_evidence_gate_revision_marker() -> None:
    assert GATE_REVISION == "SRSC_EVIDENCE_GATE_LOCAL_STANDALONE_V1"
