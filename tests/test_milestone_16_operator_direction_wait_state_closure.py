from __future__ import annotations

import json

from hbce_arc_agi3.milestone_16_operator_direction_wait_state_closure import (
    BLOCK_REASON,
    CLOSURE_DECISION,
    CLOSURE_VERDICT,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    TASK_VALID,
    build_milestone_16_task_7_operator_direction_wait_state_closure,
    validate_milestone_16_task_7_operator_direction_wait_state_closure,
    write_milestone_16_task_7_operator_direction_wait_state_closure_artifacts,
)


def test_task_7_operator_direction_wait_state_closure_is_valid() -> None:
    closure = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")
    validation = validate_milestone_16_task_7_operator_direction_wait_state_closure(closure)

    assert validation["valid"] is True
    assert validation["status"] == TASK_VALID
    assert validation["issue_count"] == 0


def test_task_7_chain_from_task_6_is_correct() -> None:
    closure = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")

    assert closure["previous_stage"] == PREVIOUS_STAGE
    assert closure["next_stage"] == NEXT_STAGE
    assert closure["source_task_6_final_baseline_commit"] == "0c60e2f"
    assert closure["source_task_6_final_signature"] == "82CD7B4CA93E692A"


def test_task_7_closure_passes_but_wait_state_stays_active() -> None:
    closure = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")

    assert closure["closure_verdict"] == CLOSURE_VERDICT
    assert closure["closure_decision"] == CLOSURE_DECISION
    assert closure["block_reason"] == BLOCK_REASON
    assert closure["wait_state_closure_ready"] is True
    assert closure["wait_state_closure_passed"] is True
    assert closure["wait_state_closure_closed"] is True
    assert closure["wait_state_active"] is True
    assert closure["wait_state_closed"] is False


def test_task_7_review_cycle_is_closed() -> None:
    closure = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")

    assert closure["task_6_wait_state_review_confirmed"] is True
    assert closure["wait_state_review_ready"] is True
    assert closure["wait_state_review_passed"] is True
    assert closure["wait_state_review_closed"] is True


def test_task_7_decision_gate_remains_blocked() -> None:
    closure = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")

    assert closure["decision_gate_ready"] is True
    assert closure["decision_gate_open"] is False
    assert closure["decision_gate_blocked"] is True


def test_task_7_no_direction_option_selected() -> None:
    closure = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")

    assert closure["direction_options_reviewed"] is True
    assert closure["direction_option_count"] == 5
    assert closure["direction_option_selected"] is False
    assert closure["selected_direction_option_id"] == "NONE"
    assert closure["selected_direction_option_count"] == 0


def test_task_7_operator_direction_not_received() -> None:
    closure = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")

    assert closure["operator_direction_required"] is True
    assert closure["operator_direction_received"] is False
    assert closure["operator_direction_value"] == "PENDING_EXPLICIT_OPERATOR_DIRECTION"
    assert closure["wait_state_reason"] == "NO_EXPLICIT_OPERATOR_DIRECTION_RECEIVED"


def test_task_7_operator_authorization_not_received() -> None:
    closure = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")

    assert closure["operator_decision_required"] is True
    assert closure["operator_decision_received"] is False
    assert closure["explicit_operator_authorization_required"] is True
    assert closure["explicit_operator_authorization_received"] is False


def test_task_7_no_implementation_is_authorized() -> None:
    closure = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")

    assert closure["implementation_authorization_granted"] is False
    assert closure["implementation_authorized"] is False
    assert closure["implementation_blocked"] is True
    assert closure["implementation_performed"] is False
    assert closure["implementation_patch_created"] is False
    assert closure["implementation_patch_applied"] is False


def test_task_7_no_runtime_modification_is_allowed() -> None:
    closure = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")

    assert closure["runtime_solver_patch_allowed"] is False
    assert closure["runtime_solver_modified"] is False
    assert closure["ranker_runtime_patch_allowed"] is False
    assert closure["ranker_runtime_modified"] is False
    assert closure["candidate_generator_patch_allowed"] is False
    assert closure["candidate_generator_modified"] is False


def test_task_7_no_runtime_wiring_activation_execution() -> None:
    closure = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")

    assert closure["runtime_wiring_allowed"] is False
    assert closure["runtime_wiring_performed"] is False
    assert closure["runtime_activation_authorized"] is False
    assert closure["runtime_activation_blocked"] is True
    assert closure["runtime_activation_performed"] is False
    assert closure["runtime_execution_allowed"] is False
    assert closure["runtime_execution_performed"] is False


def test_task_7_no_real_submission_path_is_open() -> None:
    closure = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")

    assert closure["real_evaluation_allowed"] is False
    assert closure["real_submission_allowed"] is False
    assert closure["ready_for_real_kaggle_submission"] is False
    assert closure["manual_upload_allowed"] is False
    assert closure["kaggle_authentication_allowed"] is False
    assert closure["kaggle_upload_allowed"] is False
    assert closure["kaggle_submission_sent"] is False


def test_task_7_public_boundary_is_preserved() -> None:
    closure = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")

    assert closure["external_api_dependency"] is False
    assert closure["internet_during_eval"] is False
    assert closure["private_core_exposure"] is False
    assert closure["legal_certification"] is False
    assert closure["official_score_claim_allowed"] is False
    assert closure["competitive_score_claim_allowed"] is False
    assert closure["public_overfit_allowed"] is False
    assert closure["public_overfit_guard_required"] is True


def test_task_7_fail_closed_closure_only_is_active() -> None:
    closure = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")

    assert closure["fail_closed_required"] is True
    assert closure["fail_closed_active"] is True
    assert closure["closure_only"] is True
    assert closure["milestone_16_operator_direction_wait_state_closure_failure_count"] == 0
    assert closure["milestone_16_operator_direction_wait_state_closure_check_count"] == len(closure["milestone_16_operator_direction_wait_state_closure_checks"])
    assert closure["milestone_16_operator_direction_wait_state_closure_check_count"] == 34


def test_task_7_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")
    second = build_milestone_16_task_7_operator_direction_wait_state_closure(baseline_commit="TESTBASE")

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16


def test_task_7_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "m16_task7"
    doc_path = tmp_path / "m16_task7.md"

    closure, validation, paths = write_milestone_16_task_7_operator_direction_wait_state_closure_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation["valid"] is True
    assert closure["operator_direction_wait_state_closure_created"] is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-16-operator-direction-wait-state-closure-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["closure"]["closure_decision"] == CLOSURE_DECISION
    assert payload["closure"]["wait_state_closure_closed"] is True
    assert payload["closure"]["wait_state_active"] is True
    assert payload["closure"]["wait_state_closed"] is False
    assert payload["closure"]["implementation_authorized"] is False
    assert payload["closure"]["runtime_activation_performed"] is False
