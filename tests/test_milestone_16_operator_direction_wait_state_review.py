from __future__ import annotations

import json

from hbce_arc_agi3.milestone_16_operator_direction_wait_state_review import (
    BLOCK_REASON,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    REVIEW_DECISION,
    REVIEW_VERDICT,
    TASK_VALID,
    build_milestone_16_task_6_operator_direction_wait_state_review,
    validate_milestone_16_task_6_operator_direction_wait_state_review,
    write_milestone_16_task_6_operator_direction_wait_state_review_artifacts,
)


def test_task_6_operator_direction_wait_state_review_is_valid() -> None:
    review = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")
    validation = validate_milestone_16_task_6_operator_direction_wait_state_review(review)

    assert validation["valid"] is True
    assert validation["status"] == TASK_VALID
    assert validation["issue_count"] == 0


def test_task_6_chain_from_task_5_is_correct() -> None:
    review = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")

    assert review["previous_stage"] == PREVIOUS_STAGE
    assert review["next_stage"] == NEXT_STAGE
    assert review["source_task_5_final_baseline_commit"] == "03acb5a"
    assert review["source_task_5_final_signature"] == "EC9F02EC0CF5AC8F"


def test_task_6_review_passes_active_wait_state() -> None:
    review = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")

    assert review["review_verdict"] == REVIEW_VERDICT
    assert review["review_decision"] == REVIEW_DECISION
    assert review["block_reason"] == BLOCK_REASON
    assert review["wait_state_review_ready"] is True
    assert review["wait_state_review_passed"] is True
    assert review["wait_state_review_closed"] is True


def test_task_6_wait_state_remains_active() -> None:
    review = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")

    assert review["wait_state_ready"] is True
    assert review["wait_state_active"] is True
    assert review["wait_state_closed"] is False
    assert review["wait_state_reason"] == "NO_EXPLICIT_OPERATOR_DIRECTION_RECEIVED"


def test_task_6_decision_gate_remains_blocked() -> None:
    review = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")

    assert review["decision_gate_ready"] is True
    assert review["decision_gate_open"] is False
    assert review["decision_gate_blocked"] is True


def test_task_6_no_direction_option_selected() -> None:
    review = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")

    assert review["direction_options_reviewed"] is True
    assert review["direction_option_count"] == 5
    assert review["direction_option_selected"] is False
    assert review["selected_direction_option_id"] == "NONE"
    assert review["selected_direction_option_count"] == 0


def test_task_6_operator_direction_not_received() -> None:
    review = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")

    assert review["operator_direction_required"] is True
    assert review["operator_direction_received"] is False
    assert review["operator_direction_value"] == "PENDING_EXPLICIT_OPERATOR_DIRECTION"


def test_task_6_operator_authorization_not_received() -> None:
    review = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")

    assert review["operator_decision_required"] is True
    assert review["operator_decision_received"] is False
    assert review["explicit_operator_authorization_required"] is True
    assert review["explicit_operator_authorization_received"] is False


def test_task_6_no_implementation_is_authorized() -> None:
    review = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")

    assert review["implementation_authorization_granted"] is False
    assert review["implementation_authorized"] is False
    assert review["implementation_blocked"] is True
    assert review["implementation_performed"] is False
    assert review["implementation_patch_created"] is False
    assert review["implementation_patch_applied"] is False


def test_task_6_no_runtime_modification_is_allowed() -> None:
    review = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")

    assert review["runtime_solver_patch_allowed"] is False
    assert review["runtime_solver_modified"] is False
    assert review["ranker_runtime_patch_allowed"] is False
    assert review["ranker_runtime_modified"] is False
    assert review["candidate_generator_patch_allowed"] is False
    assert review["candidate_generator_modified"] is False


def test_task_6_no_runtime_wiring_activation_execution() -> None:
    review = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")

    assert review["runtime_wiring_allowed"] is False
    assert review["runtime_wiring_performed"] is False
    assert review["runtime_activation_authorized"] is False
    assert review["runtime_activation_blocked"] is True
    assert review["runtime_activation_performed"] is False
    assert review["runtime_execution_allowed"] is False
    assert review["runtime_execution_performed"] is False


def test_task_6_no_real_submission_path_is_open() -> None:
    review = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")

    assert review["real_evaluation_allowed"] is False
    assert review["real_submission_allowed"] is False
    assert review["ready_for_real_kaggle_submission"] is False
    assert review["manual_upload_allowed"] is False
    assert review["kaggle_authentication_allowed"] is False
    assert review["kaggle_upload_allowed"] is False
    assert review["kaggle_submission_sent"] is False


def test_task_6_public_boundary_is_preserved() -> None:
    review = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")

    assert review["external_api_dependency"] is False
    assert review["internet_during_eval"] is False
    assert review["private_core_exposure"] is False
    assert review["legal_certification"] is False
    assert review["official_score_claim_allowed"] is False
    assert review["competitive_score_claim_allowed"] is False
    assert review["public_overfit_allowed"] is False
    assert review["public_overfit_guard_required"] is True


def test_task_6_fail_closed_review_only_is_active() -> None:
    review = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")

    assert review["fail_closed_required"] is True
    assert review["fail_closed_active"] is True
    assert review["review_only"] is True
    assert review["milestone_16_operator_direction_wait_state_review_failure_count"] == 0
    assert review["milestone_16_operator_direction_wait_state_review_check_count"] == len(review["milestone_16_operator_direction_wait_state_review_checks"])
    assert review["milestone_16_operator_direction_wait_state_review_check_count"] == 33


def test_task_6_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")
    second = build_milestone_16_task_6_operator_direction_wait_state_review(baseline_commit="TESTBASE")

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16


def test_task_6_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "m16_task6"
    doc_path = tmp_path / "m16_task6.md"

    review, validation, paths = write_milestone_16_task_6_operator_direction_wait_state_review_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation["valid"] is True
    assert review["operator_direction_wait_state_review_created"] is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-16-operator-direction-wait-state-review-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["review"]["review_decision"] == REVIEW_DECISION
    assert payload["review"]["wait_state_review_passed"] is True
    assert payload["review"]["wait_state_active"] is True
    assert payload["review"]["implementation_authorized"] is False
    assert payload["review"]["runtime_activation_performed"] is False
