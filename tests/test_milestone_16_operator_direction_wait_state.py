from __future__ import annotations

import json

from hbce_arc_agi3.milestone_16_operator_direction_wait_state import (
    BLOCK_REASON,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    TASK_VALID,
    WAIT_STATE_DECISION,
    WAIT_STATE_VERDICT,
    build_milestone_16_task_5_operator_direction_wait_state,
    validate_milestone_16_task_5_operator_direction_wait_state,
    write_milestone_16_task_5_operator_direction_wait_state_artifacts,
)


def test_task_5_operator_direction_wait_state_is_valid() -> None:
    wait_state = build_milestone_16_task_5_operator_direction_wait_state(baseline_commit="TESTBASE")
    validation = validate_milestone_16_task_5_operator_direction_wait_state(wait_state)

    assert validation["valid"] is True
    assert validation["status"] == TASK_VALID
    assert validation["issue_count"] == 0


def test_task_5_chain_from_task_4_is_correct() -> None:
    wait_state = build_milestone_16_task_5_operator_direction_wait_state(baseline_commit="TESTBASE")

    assert wait_state["previous_stage"] == PREVIOUS_STAGE
    assert wait_state["next_stage"] == NEXT_STAGE
    assert wait_state["source_task_4_final_baseline_commit"] == "36887a0"
    assert wait_state["source_task_4_final_signature"] == "7A0DD6F0A4F3F4C8"


def test_task_5_wait_state_is_active() -> None:
    wait_state = build_milestone_16_task_5_operator_direction_wait_state(baseline_commit="TESTBASE")

    assert wait_state["wait_state_verdict"] == WAIT_STATE_VERDICT
    assert wait_state["wait_state_decision"] == WAIT_STATE_DECISION
    assert wait_state["block_reason"] == BLOCK_REASON
    assert wait_state["wait_state_ready"] is True
    assert wait_state["wait_state_active"] is True
    assert wait_state["wait_state_closed"] is False


def test_task_5_decision_gate_remains_blocked() -> None:
    wait_state = build_milestone_16_task_5_operator_direction_wait_state(baseline_commit="TESTBASE")

    assert wait_state["decision_gate_ready"] is True
    assert wait_state["decision_gate_open"] is False
    assert wait_state["decision_gate_blocked"] is True


def test_task_5_no_direction_option_selected() -> None:
    wait_state = build_milestone_16_task_5_operator_direction_wait_state(baseline_commit="TESTBASE")

    assert wait_state["direction_options_reviewed"] is True
    assert wait_state["direction_option_count"] == 5
    assert wait_state["direction_option_selected"] is False
    assert wait_state["selected_direction_option_id"] == "NONE"
    assert wait_state["selected_direction_option_count"] == 0


def test_task_5_operator_direction_not_received() -> None:
    wait_state = build_milestone_16_task_5_operator_direction_wait_state(baseline_commit="TESTBASE")

    assert wait_state["operator_direction_required"] is True
    assert wait_state["operator_direction_received"] is False
    assert wait_state["operator_direction_value"] == "PENDING_EXPLICIT_OPERATOR_DIRECTION"
    assert wait_state["wait_state_reason"] == "NO_EXPLICIT_OPERATOR_DIRECTION_RECEIVED"


def test_task_5_operator_authorization_not_received() -> None:
    wait_state = build_milestone_16_task_5_operator_direction_wait_state(baseline_commit="TESTBASE")

    assert wait_state["operator_decision_required"] is True
    assert wait_state["operator_decision_received"] is False
    assert wait_state["explicit_operator_authorization_required"] is True
    assert wait_state["explicit_operator_authorization_received"] is False


def test_task_5_no_implementation_is_authorized() -> None:
    wait_state = build_milestone_16_task_5_operator_direction_wait_state(baseline_commit="TESTBASE")

    assert wait_state["implementation_authorization_granted"] is False
    assert wait_state["implementation_authorized"] is False
    assert wait_state["implementation_blocked"] is True
    assert wait_state["implementation_performed"] is False
    assert wait_state["implementation_patch_created"] is False
    assert wait_state["implementation_patch_applied"] is False


def test_task_5_no_runtime_modification_is_allowed() -> None:
    wait_state = build_milestone_16_task_5_operator_direction_wait_state(baseline_commit="TESTBASE")

    assert wait_state["runtime_solver_patch_allowed"] is False
    assert wait_state["runtime_solver_modified"] is False
    assert wait_state["ranker_runtime_patch_allowed"] is False
    assert wait_state["ranker_runtime_modified"] is False
    assert wait_state["candidate_generator_patch_allowed"] is False
    assert wait_state["candidate_generator_modified"] is False


def test_task_5_no_runtime_wiring_activation_execution() -> None:
    wait_state = build_milestone_16_task_5_operator_direction_wait_state(baseline_commit="TESTBASE")

    assert wait_state["runtime_wiring_allowed"] is False
    assert wait_state["runtime_wiring_performed"] is False
    assert wait_state["runtime_activation_authorized"] is False
    assert wait_state["runtime_activation_blocked"] is True
    assert wait_state["runtime_activation_performed"] is False
    assert wait_state["runtime_execution_allowed"] is False
    assert wait_state["runtime_execution_performed"] is False


def test_task_5_no_real_submission_path_is_open() -> None:
    wait_state = build_milestone_16_task_5_operator_direction_wait_state(baseline_commit="TESTBASE")

    assert wait_state["real_evaluation_allowed"] is False
    assert wait_state["real_submission_allowed"] is False
    assert wait_state["ready_for_real_kaggle_submission"] is False
    assert wait_state["manual_upload_allowed"] is False
    assert wait_state["kaggle_authentication_allowed"] is False
    assert wait_state["kaggle_upload_allowed"] is False
    assert wait_state["kaggle_submission_sent"] is False


def test_task_5_public_boundary_is_preserved() -> None:
    wait_state = build_milestone_16_task_5_operator_direction_wait_state(baseline_commit="TESTBASE")

    assert wait_state["external_api_dependency"] is False
    assert wait_state["internet_during_eval"] is False
    assert wait_state["private_core_exposure"] is False
    assert wait_state["legal_certification"] is False
    assert wait_state["official_score_claim_allowed"] is False
    assert wait_state["competitive_score_claim_allowed"] is False
    assert wait_state["public_overfit_allowed"] is False
    assert wait_state["public_overfit_guard_required"] is True


def test_task_5_fail_closed_wait_state_is_active() -> None:
    wait_state = build_milestone_16_task_5_operator_direction_wait_state(baseline_commit="TESTBASE")

    assert wait_state["fail_closed_required"] is True
    assert wait_state["fail_closed_active"] is True
    assert wait_state["wait_state_only"] is True
    assert wait_state["milestone_16_operator_direction_wait_state_failure_count"] == 0
    assert wait_state["milestone_16_operator_direction_wait_state_check_count"] == len(wait_state["milestone_16_operator_direction_wait_state_checks"])
    assert wait_state["milestone_16_operator_direction_wait_state_check_count"] == 33


def test_task_5_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_16_task_5_operator_direction_wait_state(baseline_commit="TESTBASE")
    second = build_milestone_16_task_5_operator_direction_wait_state(baseline_commit="TESTBASE")

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16


def test_task_5_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "m16_task5"
    doc_path = tmp_path / "m16_task5.md"

    wait_state, validation, paths = write_milestone_16_task_5_operator_direction_wait_state_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation["valid"] is True
    assert wait_state["operator_direction_wait_state_created"] is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-16-operator-direction-wait-state-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["wait_state"]["wait_state_decision"] == WAIT_STATE_DECISION
    assert payload["wait_state"]["wait_state_active"] is True
    assert payload["wait_state"]["wait_state_closed"] is False
    assert payload["wait_state"]["implementation_authorized"] is False
    assert payload["wait_state"]["runtime_activation_performed"] is False
