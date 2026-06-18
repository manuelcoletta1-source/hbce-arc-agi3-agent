from __future__ import annotations

import json

from hbce_arc_agi3.milestone_15_explicit_operator_decision_gate import (
    BLOCK_REASON,
    GATE_DECISION,
    GATE_VERDICT,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    SOURCE_MILESTONE_14_FINAL_CLOSURE,
    TASK_VALID,
    build_milestone_15_task_1_decision_gate,
    validate_milestone_15_task_1_decision_gate,
    write_milestone_15_task_1_decision_gate_artifacts,
)


def test_milestone_15_task_1_gate_is_valid() -> None:
    gate = build_milestone_15_task_1_decision_gate(baseline_commit="TESTBASE")
    validation = validate_milestone_15_task_1_decision_gate(gate)

    assert validation.valid is True
    assert validation.status == TASK_VALID
    assert validation.issue_count == 0


def test_milestone_15_opens_as_decision_gate_only() -> None:
    gate = build_milestone_15_task_1_decision_gate(baseline_commit="TESTBASE")

    assert gate.milestone_15_opened is True
    assert gate.explicit_operator_decision_gate_created is True
    assert gate.gate_verdict == GATE_VERDICT
    assert gate.gate_decision == GATE_DECISION
    assert gate.block_reason == BLOCK_REASON


def test_milestone_15_references_milestone_14_final_closure() -> None:
    gate = build_milestone_15_task_1_decision_gate(baseline_commit="TESTBASE")

    assert gate.previous_stage == PREVIOUS_STAGE
    assert gate.source_milestone_14_final_closure == SOURCE_MILESTONE_14_FINAL_CLOSURE
    assert gate.next_stage == NEXT_STAGE
    assert gate.source_milestone_14_final_baseline_commit == "f7ee729"
    assert gate.source_milestone_14_final_signature == "05F1CDD559B63B8C"


def test_operator_decision_is_required_but_not_received() -> None:
    gate = build_milestone_15_task_1_decision_gate(baseline_commit="TESTBASE")

    assert gate.operator_decision_required is True
    assert gate.operator_decision_received is False
    assert gate.operator_decision_recorded is False
    assert gate.operator_decision_value == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert gate.no_implicit_authorization is True


def test_no_implementation_authorization_exists() -> None:
    gate = build_milestone_15_task_1_decision_gate(baseline_commit="TESTBASE")

    assert gate.implementation_authorized is False
    assert gate.implementation_blocked is True
    assert gate.runtime_activation_authorized is False
    assert gate.runtime_activation_performed is False
    assert gate.runtime_execution_performed is False
    assert gate.implementation_performed is False


def test_runtime_modules_remain_unmodified() -> None:
    gate = build_milestone_15_task_1_decision_gate(baseline_commit="TESTBASE")

    assert gate.runtime_solver_modified is False
    assert gate.ranker_runtime_modified is False
    assert gate.candidate_generator_modified is False


def test_no_real_submission_path_is_open() -> None:
    gate = build_milestone_15_task_1_decision_gate(baseline_commit="TESTBASE")

    assert gate.real_evaluation_performed is False
    assert gate.real_submission_allowed is False
    assert gate.ready_for_real_kaggle_submission is False
    assert gate.manual_upload_allowed is False
    assert gate.kaggle_authentication_allowed is False
    assert gate.kaggle_authentication_performed is False
    assert gate.kaggle_upload_allowed is False
    assert gate.kaggle_upload_performed is False
    assert gate.kaggle_submission_sent is False


def test_public_boundary_is_preserved() -> None:
    gate = build_milestone_15_task_1_decision_gate(baseline_commit="TESTBASE")

    assert gate.external_api_dependency is False
    assert gate.internet_during_eval is False
    assert gate.private_core_exposure is False
    assert gate.legal_certification is False
    assert gate.official_score_claim_allowed is False
    assert gate.competitive_score_claim_allowed is False
    assert gate.public_overfit_allowed is False
    assert gate.public_overfit_guard_required is True


def test_fail_closed_boundary_is_active() -> None:
    gate = build_milestone_15_task_1_decision_gate(baseline_commit="TESTBASE")

    assert gate.fail_closed_required is True
    assert gate.fail_closed_active is True
    assert gate.decision_gate_failure_count == 0
    assert gate.decision_gate_check_count == len(gate.decision_gate_checks)
    assert gate.decision_gate_check_count == 9


def test_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_15_task_1_decision_gate(baseline_commit="TESTBASE")
    second = build_milestone_15_task_1_decision_gate(baseline_commit="TESTBASE")

    assert first.signature == second.signature


def test_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "m15_task1"
    doc_path = tmp_path / "m15_task1.md"

    gate, validation, paths = write_milestone_15_task_1_decision_gate_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation.valid is True
    assert gate.milestone_15_opened is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-15-explicit-operator-decision-gate-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["record"]["gate_decision"] == GATE_DECISION
    assert payload["record"]["operator_decision_received"] is False
    assert payload["record"]["implementation_authorized"] is False
