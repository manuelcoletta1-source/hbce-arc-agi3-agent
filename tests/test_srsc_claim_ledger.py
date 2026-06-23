"""Tests for SRSC Claim Ledger."""

from __future__ import annotations

import json
import pytest

from hbce_arc_agi3.srsc_claim_ledger import (
    BoundaryState,
    ClaimLedger,
    ClaimState,
    EvidenceState,
    FAIL_CLOSED_ACTIVE,
    KAGGLE_SUBMISSION_SENT,
    LEGAL_CERTIFICATION,
    PRIVATE_CORE_EXPOSURE,
    RUNTIME_SOLVER_MODIFIED,
    RUNTIME_WIRING_ALLOWED,
    TASK_ID,
    create_claim_record,
    stable_json,
)


def test_srsc_claim_record_is_deterministic() -> None:
    first = create_claim_record(
        claim_text="Task 81 implements a local standalone SRSC claim ledger.",
        claim_state=ClaimState.VERIFIED,
        evidence_state=EvidenceState.PRESENT,
        evidence_refs=["docs/milestone-19-task-80-srsc-claim-ledger-implementation-authorization-review-v1.md"],
        scope="Milestone 19 Task 81 local implementation",
    )
    second = create_claim_record(
        claim_text="  Task 81 implements a local standalone SRSC claim ledger.  ",
        claim_state="VERIFIED",
        evidence_state="PRESENT",
        evidence_refs=["docs/milestone-19-task-80-srsc-claim-ledger-implementation-authorization-review-v1.md"],
        scope="Milestone 19 Task 81 local implementation",
    )
    assert first.claim_id == second.claim_id
    assert first.claim_id.startswith("SRSC-CLAIM-")


def test_srsc_claim_record_public_boundary_flags_are_fail_closed() -> None:
    record = create_claim_record(
        claim_text="SRSC boundary remains public-safe.",
        claim_state=ClaimState.REPORTED,
        evidence_state=EvidenceState.PRESENT,
        evidence_refs=["task-81-manifest.json"],
        scope="Boundary check",
    )
    payload = record.to_public_dict()
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["privateCoreExposure"] is False
    assert payload["legalCertification"] is False
    assert payload["failClosedActive"] is True
    assert RUNTIME_SOLVER_MODIFIED is False
    assert RUNTIME_WIRING_ALLOWED is False
    assert KAGGLE_SUBMISSION_SENT is False
    assert PRIVATE_CORE_EXPOSURE is False
    assert LEGAL_CERTIFICATION is False
    assert FAIL_CLOSED_ACTIVE is True


def test_srsc_recordable_claim_requires_evidence_scope_and_public_boundary() -> None:
    record = create_claim_record(
        claim_text="Evidence gate exists as a local standalone module.",
        claim_state=ClaimState.VERIFIED,
        evidence_state=EvidenceState.PRESENT,
        evidence_refs=["src/hbce_arc_agi3/srsc_evidence_gate.py"],
        scope="Task 81 local implementation",
    )
    assert record.is_recordable is True


def test_srsc_missing_evidence_is_not_recordable() -> None:
    record = create_claim_record(
        claim_text="Unsupported claim must fail closed.",
        claim_state=ClaimState.VERIFIED,
        evidence_state=EvidenceState.MISSING,
        evidence_refs=[],
        scope="Fail closed check",
    )
    assert record.is_recordable is False


def test_srsc_unknown_claim_is_not_recordable_even_with_evidence() -> None:
    record = create_claim_record(
        claim_text="Unknown claim remains blocked.",
        claim_state=ClaimState.UNKNOWN,
        evidence_state=EvidenceState.PRESENT,
        evidence_refs=["some-source"],
        scope="Fail closed check",
    )
    assert record.is_recordable is False


def test_srsc_private_boundary_is_not_recordable() -> None:
    record = create_claim_record(
        claim_text="Private boundary must be blocked.",
        claim_state=ClaimState.REPORTED,
        evidence_state=EvidenceState.PRESENT,
        evidence_refs=["some-source"],
        scope="Boundary check",
        boundary_state=BoundaryState.BLOCKED_PRIVATE,
    )
    assert record.is_recordable is False


def test_srsc_ledger_adds_record_and_deduplicates() -> None:
    record = create_claim_record(
        claim_text="Ledger stores deterministic claim records.",
        claim_state=ClaimState.VERIFIED,
        evidence_state=EvidenceState.PRESENT,
        evidence_refs=["tests/test_srsc_claim_ledger.py"],
        scope="Unit test",
    )
    ledger = ClaimLedger().add(record).add(record)
    assert ledger.record_count == 1
    assert ledger.get(record.claim_id) == record
    assert ledger.ledger_id.startswith("SRSC-LEDGER-")


def test_srsc_ledger_rejects_unrecordable_claim() -> None:
    record = create_claim_record(
        claim_text="Blocked claim cannot enter ledger.",
        claim_state=ClaimState.BLOCKED,
        evidence_state=EvidenceState.MISSING,
        evidence_refs=[],
        scope="Unit test",
    )
    with pytest.raises(ValueError):
        ClaimLedger().add(record)


def test_srsc_public_payload_is_json_serializable() -> None:
    record = create_claim_record(
        claim_text="Public payload remains serializable.",
        claim_state=ClaimState.HYPOTHESIS,
        evidence_state=EvidenceState.PRESENT,
        evidence_refs=["tests/test_srsc_claim_ledger.py"],
        scope="Serialization check",
        metadata={"b": 2, "a": 1},
    )
    payload = record.to_public_dict()
    encoded = json.dumps(payload, sort_keys=True)
    assert "Public payload remains serializable." in encoded
    assert stable_json({"b": 2, "a": 1}) == '{"a":1,"b":2}'


def test_srsc_task_id_is_task_81() -> None:
    assert TASK_ID == "MILESTONE_19_TASK_81_SRSC_CLAIM_LEDGER_EVIDENCE_GATE_LOCAL_IMPLEMENTATION_V1"
