from __future__ import annotations

import json

from hbce_arc_agi3.milestone_15_implementation_authorization_decision_gate import (
    BLOCK_REASON,
    GATE_DECISION,
    GATE_VERDICT,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    TASK_VALID,
    build_milestone_15_task_7_implementation_authorization_decision_gate,
    validate_milestone_15_task_7_implementation_authorization_decision_gate,
    write_milestone_15_task_7_implementation_authorization_decision_gate_artifacts,
)


def test_task_7_decision_gate_is_valid() -> None:
    gate = build_milestone_15_task_7_implementation_authorization_decision_gate(baseline_commit="TESTBASE")
    validation = validate_milestone_15_task_7_implementation_authorization_decision_gate(gate)

    assert validation.valid is True
    assert validation.status == TASK_VALID
    assert validation.issue_count == 0


def test_task_7_reviews_task_6_block() -> None:
    gate = build_milestone_15_task_7_implementation_authorization_decision_gate(baseline_commit="TESTBASE")

    assert gate.task_6_implementation_block_confirmed is True
    assert gate.source_task_6_final_baseline_commit == "c70df02"
    assert gate.source_task_6_final_signature == "D93E57F44AAF8A8E"


def test_task_7_chain_is_correct() -> None:
    gate = build_milestone_15_task_7_implementation_authorization_decision_gate(baseline_commit="TESTBASE")

    assert gate.previous_stage == PREVIOUS_STAGE
    assert gate.next_stage == NEXT_STAGE
    assert gate.source_task_5_final_baseline_commit == "cd005ad"
    assert gate.source_task_5_final_signature == "1065B790C4AE1364"


def test_task_7_gate_decision_blocks_implementation() -> None:
    gate = build_milestone_15_task_7_implementation_authorization_decision_gate(baseline_commit="TESTBASE")

    assert gate.gate_verdict == GATE_VERDICT
    assert gate.gate_decision == GATE_DECISION
    assert gate.block_reason == BLOCK_REASON
    assert gate.implementation_authorization_granted is False


def test_task_7_operator_decision_is_still_pending() -> None:
    gate = build_milestone_15_task_7_implementation_authorization_decision_gate(baseline_commit="TESTBASE")

    assert gate.operator_decision_required is True
    assert gate.operator_decision_received is False
    assert gate.operator_decision_value == "PENDING_EXPLICIT_OPERATOR_DECISION"


def test_task_7_explicit_authorization_not_received() -> None:
    gate = build_milestone_15_task_7_implementation_authorization_decision_gate(baseline_commit="TESTBASE")

    assert gate.explicit_operator_authorization_required is True
    assert gate.explicit_operator_authorization_received is False
    assert gate.explicit_operator_authorization_value == "NO_EXPLICIT_OPERATOR_AUTHORIZATION_RECEIVED"


def test_task_7_implementation_authorization_decision_not_received() -> None:
    gate = build_milestone_15_task_7_implementation_authorization_decision_gate(baseline_commit="TESTBASE")

    assert gate.implementation_authorization_decision_required is True
    assert gate.implementation_authorization_decision_received is False
    assert gate.implementation_authorization_decision_value == "PENDING_EXPLICIT_OPERATOR_AUTHORIZATION"


def test_task_7_implementation_remains_blocked() -> None:
    gate = build_milestone_15_task_7_implementation_authorization_decision_gate(baseline_commit="TESTBASE")

    assert gate.implementation_authorized is False
    assert gate.implementation_blocked is True
    assert gate.implementation_performed is False
    assert gate.implementation_patch_created is False
    assert gate.implementation_patch_applied is False


def test_task_7_runtime_patch_and_wiring_are_not_allowed() -> None:
    gate = build_milestone_15_task_7_implementation_authorization_decision_gate(baseline_commit="TESTBASE")

    assert gate.runtime_solver_patch_allowed is False
    assert gate.runtime_solver_modified is False
    assert gate.ranker_runtime_patch_allowed is False
    assert gate.ranker_runtime_modified is False
    assert gate.candidate_generator_patch_allowed is False
    assert gate.candidate_generator_modified is False
    assert gate.runtime_wiring_allowed is False
    assert gate.runtime_wiring_performed is False


def test_task_7_runtime_activation_and_execution_stay_blocked() -> None:
    gate = build_milestone_15_task_7_implementation_authorization_decision_gate(baseline_commit="TESTBASE")

    assert gate.runtime_activation_authorized is False
    assert gate.runtime_activation_blocked is True
    assert gate.runtime_activation_performed is False
    assert gate.runtime_execution_allowed is False
    assert gate.runtime_execution_performed is False


def test_task_7_no_real_submission_path_is_open() -> None:
    gate = build_milestone_15_task_7_implementation_authorization_decision_gate(baseline_commit="TESTBASE")

    assert gate.real_evaluation_performed is False
    assert gate.real_submission_allowed is False
    assert gate.ready_for_real_kaggle_submission is False
    assert gate.manual_upload_allowed is False
    assert gate.kaggle_authentication_allowed is False
    assert gate.kaggle_authentication_performed is False
    assert gate.kaggle_upload_allowed is False
    assert gate.kaggle_upload_performed is False
    assert gate.kaggle_submission_sent is False


def test_task_7_public_boundary_is_preserved() -> None:
    gate = build_milestone_15_task_7_implementation_authorization_decision_gate(baseline_commit="TESTBASE")

    assert gate.external_api_dependency is False
    assert gate.internet_during_eval is False
    assert gate.private_core_exposure is False
    assert gate.legal_certification is False
    assert gate.official_score_claim_allowed is False
    assert gate.competitive_score_claim_allowed is False
    assert gate.public_overfit_allowed is False
    assert gate.public_overfit_guard_required is True


def test_task_7_fail_closed_gate_is_active() -> None:
    gate = build_milestone_15_task_7_implementation_authorization_decision_gate(baseline_commit="TESTBASE")

    assert gate.fail_closed_required is True
    assert gate.fail_closed_active is True
    assert gate.implementation_authorization_decision_failure_count == 0
    assert gate.implementation_authorization_decision_check_count == len(gate.implementation_authorization_decision_checks)
    assert gate.implementation_authorization_decision_check_count == 21


def test_task_7_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "m15_task7"
    doc_path = tmp_path / "m15_task7.md"

    gate, validation, paths = write_milestone_15_task_7_implementation_authorization_decision_gate_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation.valid is True
    assert gate.implementation_authorization_decision_gate_created is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-15-implementation-authorization-decision-gate-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["record"]["gate_decision"] == GATE_DECISION
    assert payload["record"]["implementation_authorization_granted"] is False
    assert payload["record"]["implementation_authorized"] is False
    assert payload["record"]["implementation_performed"] is False
