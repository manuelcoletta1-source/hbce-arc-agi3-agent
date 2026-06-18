from __future__ import annotations

import json

from hbce_arc_agi3.milestone_16_operator_direction_decision_gate import (
    BLOCK_REASON,
    GATE_DECISION,
    GATE_VERDICT,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    TASK_VALID,
    build_milestone_16_task_4_operator_direction_decision_gate,
    validate_milestone_16_task_4_operator_direction_decision_gate,
    write_milestone_16_task_4_operator_direction_decision_gate_artifacts,
)


def test_task_4_operator_direction_decision_gate_is_valid() -> None:
    gate = build_milestone_16_task_4_operator_direction_decision_gate(baseline_commit="TESTBASE")
    validation = validate_milestone_16_task_4_operator_direction_decision_gate(gate)

    assert validation["valid"] is True
    assert validation["status"] == TASK_VALID
    assert validation["issue_count"] == 0


def test_task_4_chain_from_task_3_is_correct() -> None:
    gate = build_milestone_16_task_4_operator_direction_decision_gate(baseline_commit="TESTBASE")

    assert gate["previous_stage"] == PREVIOUS_STAGE
    assert gate["next_stage"] == NEXT_STAGE
    assert gate["source_task_3_final_baseline_commit"] == "38a72a0"
    assert gate["source_task_3_final_signature"] == "BF984E621D7692D6"


def test_task_4_decision_gate_is_blocked() -> None:
    gate = build_milestone_16_task_4_operator_direction_decision_gate(baseline_commit="TESTBASE")

    assert gate["gate_verdict"] == GATE_VERDICT
    assert gate["gate_decision"] == GATE_DECISION
    assert gate["block_reason"] == BLOCK_REASON
    assert gate["decision_gate_ready"] is True
    assert gate["decision_gate_open"] is False
    assert gate["decision_gate_blocked"] is True


def test_task_4_no_direction_option_selected() -> None:
    gate = build_milestone_16_task_4_operator_direction_decision_gate(baseline_commit="TESTBASE")

    assert gate["direction_options_reviewed"] is True
    assert gate["direction_option_count"] == 5
    assert gate["direction_option_selected"] is False
    assert gate["selected_direction_option_id"] == "NONE"
    assert gate["selected_direction_option_count"] == 0


def test_task_4_operator_direction_not_received() -> None:
    gate = build_milestone_16_task_4_operator_direction_decision_gate(baseline_commit="TESTBASE")

    assert gate["operator_direction_required"] is True
    assert gate["operator_direction_received"] is False
    assert gate["operator_direction_value"] == "PENDING_EXPLICIT_OPERATOR_DIRECTION"


def test_task_4_operator_authorization_not_received() -> None:
    gate = build_milestone_16_task_4_operator_direction_decision_gate(baseline_commit="TESTBASE")

    assert gate["operator_decision_required"] is True
    assert gate["operator_decision_received"] is False
    assert gate["explicit_operator_authorization_required"] is True
    assert gate["explicit_operator_authorization_received"] is False


def test_task_4_no_implementation_is_authorized() -> None:
    gate = build_milestone_16_task_4_operator_direction_decision_gate(baseline_commit="TESTBASE")

    assert gate["implementation_authorization_granted"] is False
    assert gate["implementation_authorized"] is False
    assert gate["implementation_blocked"] is True
    assert gate["implementation_performed"] is False
    assert gate["implementation_patch_created"] is False
    assert gate["implementation_patch_applied"] is False


def test_task_4_no_runtime_modification_is_allowed() -> None:
    gate = build_milestone_16_task_4_operator_direction_decision_gate(baseline_commit="TESTBASE")

    assert gate["runtime_solver_patch_allowed"] is False
    assert gate["runtime_solver_modified"] is False
    assert gate["ranker_runtime_patch_allowed"] is False
    assert gate["ranker_runtime_modified"] is False
    assert gate["candidate_generator_patch_allowed"] is False
    assert gate["candidate_generator_modified"] is False


def test_task_4_no_runtime_wiring_activation_execution() -> None:
    gate = build_milestone_16_task_4_operator_direction_decision_gate(baseline_commit="TESTBASE")

    assert gate["runtime_wiring_allowed"] is False
    assert gate["runtime_wiring_performed"] is False
    assert gate["runtime_activation_authorized"] is False
    assert gate["runtime_activation_blocked"] is True
    assert gate["runtime_activation_performed"] is False
    assert gate["runtime_execution_allowed"] is False
    assert gate["runtime_execution_performed"] is False


def test_task_4_no_real_submission_path_is_open() -> None:
    gate = build_milestone_16_task_4_operator_direction_decision_gate(baseline_commit="TESTBASE")

    assert gate["real_evaluation_allowed"] is False
    assert gate["real_submission_allowed"] is False
    assert gate["ready_for_real_kaggle_submission"] is False
    assert gate["manual_upload_allowed"] is False
    assert gate["kaggle_authentication_allowed"] is False
    assert gate["kaggle_upload_allowed"] is False
    assert gate["kaggle_submission_sent"] is False


def test_task_4_public_boundary_is_preserved() -> None:
    gate = build_milestone_16_task_4_operator_direction_decision_gate(baseline_commit="TESTBASE")

    assert gate["external_api_dependency"] is False
    assert gate["internet_during_eval"] is False
    assert gate["private_core_exposure"] is False
    assert gate["legal_certification"] is False
    assert gate["official_score_claim_allowed"] is False
    assert gate["competitive_score_claim_allowed"] is False
    assert gate["public_overfit_allowed"] is False
    assert gate["public_overfit_guard_required"] is True


def test_task_4_fail_closed_gate_is_active() -> None:
    gate = build_milestone_16_task_4_operator_direction_decision_gate(baseline_commit="TESTBASE")

    assert gate["fail_closed_required"] is True
    assert gate["fail_closed_active"] is True
    assert gate["milestone_16_operator_direction_decision_gate_failure_count"] == 0
    assert gate["milestone_16_operator_direction_decision_gate_check_count"] == len(gate["milestone_16_operator_direction_decision_gate_checks"])
    assert gate["milestone_16_operator_direction_decision_gate_check_count"] == 33


def test_task_4_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_16_task_4_operator_direction_decision_gate(baseline_commit="TESTBASE")
    second = build_milestone_16_task_4_operator_direction_decision_gate(baseline_commit="TESTBASE")

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16


def test_task_4_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "m16_task4"
    doc_path = tmp_path / "m16_task4.md"

    gate, validation, paths = write_milestone_16_task_4_operator_direction_decision_gate_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation["valid"] is True
    assert gate["operator_direction_decision_gate_created"] is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-16-operator-direction-decision-gate-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["gate"]["gate_decision"] == GATE_DECISION
    assert payload["gate"]["decision_gate_open"] is False
    assert payload["gate"]["decision_gate_blocked"] is True
    assert payload["gate"]["implementation_authorized"] is False
    assert payload["gate"]["runtime_activation_performed"] is False
