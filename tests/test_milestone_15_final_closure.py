from __future__ import annotations

import json

from hbce_arc_agi3.milestone_15_final_closure import (
    BLOCK_REASON,
    CLOSURE_DECISION,
    CLOSURE_VERDICT,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    TASK_VALID,
    build_milestone_15_task_10_final_closure,
    validate_milestone_15_task_10_final_closure,
    write_milestone_15_task_10_final_closure_artifacts,
)


def test_task_10_final_closure_is_valid() -> None:
    closure = build_milestone_15_task_10_final_closure(baseline_commit="TESTBASE")
    validation = validate_milestone_15_task_10_final_closure(closure)

    assert validation["valid"] is True
    assert validation["status"] == TASK_VALID
    assert validation["issue_count"] == 0


def test_task_10_closes_milestone_15() -> None:
    closure = build_milestone_15_task_10_final_closure(baseline_commit="TESTBASE")

    assert closure["milestone_15_final_closure_created"] is True
    assert closure["milestone_15_closed"] is True
    assert closure["closure_verdict"] == CLOSURE_VERDICT
    assert closure["closure_decision"] == CLOSURE_DECISION
    assert closure["block_reason"] == BLOCK_REASON


def test_task_10_chain_is_correct() -> None:
    closure = build_milestone_15_task_10_final_closure(baseline_commit="TESTBASE")

    assert closure["previous_stage"] == PREVIOUS_STAGE
    assert closure["next_stage"] == NEXT_STAGE
    assert closure["source_task_9_final_baseline_commit"] == "ff4aa9f"
    assert closure["source_task_9_final_signature"] == "3409B78DFD78F374"


def test_task_10_confirms_task_1_to_9_chain() -> None:
    closure = build_milestone_15_task_10_final_closure(baseline_commit="TESTBASE")

    assert closure["task_9_closure_review_confirmed"] is True
    assert closure["task_8_authorization_record_confirmed"] is True
    assert closure["task_7_decision_gate_confirmed"] is True
    assert closure["task_6_implementation_block_confirmed"] is True


def test_task_10_operator_authorization_was_not_received() -> None:
    closure = build_milestone_15_task_10_final_closure(baseline_commit="TESTBASE")

    assert closure["operator_decision_required"] is True
    assert closure["operator_decision_received"] is False
    assert closure["operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert closure["explicit_operator_authorization_required"] is True
    assert closure["explicit_operator_authorization_received"] is False


def test_task_10_implementation_remains_blocked() -> None:
    closure = build_milestone_15_task_10_final_closure(baseline_commit="TESTBASE")

    assert closure["implementation_authorization_granted"] is False
    assert closure["implementation_authorized"] is False
    assert closure["implementation_blocked"] is True
    assert closure["implementation_performed"] is False
    assert closure["implementation_patch_created"] is False
    assert closure["implementation_patch_applied"] is False


def test_task_10_runtime_modification_is_blocked() -> None:
    closure = build_milestone_15_task_10_final_closure(baseline_commit="TESTBASE")

    assert closure["runtime_solver_patch_allowed"] is False
    assert closure["runtime_solver_modified"] is False
    assert closure["ranker_runtime_patch_allowed"] is False
    assert closure["ranker_runtime_modified"] is False
    assert closure["candidate_generator_patch_allowed"] is False
    assert closure["candidate_generator_modified"] is False


def test_task_10_runtime_wiring_activation_and_execution_are_blocked() -> None:
    closure = build_milestone_15_task_10_final_closure(baseline_commit="TESTBASE")

    assert closure["runtime_wiring_allowed"] is False
    assert closure["runtime_wiring_performed"] is False
    assert closure["runtime_activation_authorized"] is False
    assert closure["runtime_activation_blocked"] is True
    assert closure["runtime_activation_performed"] is False
    assert closure["runtime_execution_allowed"] is False
    assert closure["runtime_execution_performed"] is False


def test_task_10_no_submission_or_kaggle_path_is_open() -> None:
    closure = build_milestone_15_task_10_final_closure(baseline_commit="TESTBASE")

    assert closure["real_evaluation_performed"] is False
    assert closure["real_submission_allowed"] is False
    assert closure["ready_for_real_kaggle_submission"] is False
    assert closure["manual_upload_allowed"] is False
    assert closure["kaggle_authentication_allowed"] is False
    assert closure["kaggle_authentication_performed"] is False
    assert closure["kaggle_upload_allowed"] is False
    assert closure["kaggle_upload_performed"] is False
    assert closure["kaggle_submission_sent"] is False


def test_task_10_public_boundary_is_preserved() -> None:
    closure = build_milestone_15_task_10_final_closure(baseline_commit="TESTBASE")

    assert closure["external_api_dependency"] is False
    assert closure["internet_during_eval"] is False
    assert closure["private_core_exposure"] is False
    assert closure["legal_certification"] is False
    assert closure["official_score_claim_allowed"] is False
    assert closure["competitive_score_claim_allowed"] is False
    assert closure["public_overfit_allowed"] is False
    assert closure["public_overfit_guard_required"] is True


def test_task_10_fail_closed_closure_is_active() -> None:
    closure = build_milestone_15_task_10_final_closure(baseline_commit="TESTBASE")

    assert closure["fail_closed_required"] is True
    assert closure["fail_closed_active"] is True
    assert closure["milestone_15_final_closure_failure_count"] == 0
    assert closure["milestone_15_final_closure_check_count"] == len(closure["milestone_15_final_closure_checks"])
    assert closure["milestone_15_final_closure_check_count"] == 31


def test_task_10_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_15_task_10_final_closure(baseline_commit="TESTBASE")
    second = build_milestone_15_task_10_final_closure(baseline_commit="TESTBASE")

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16


def test_task_10_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "m15_task10"
    doc_path = tmp_path / "m15_task10.md"

    closure, validation, paths = write_milestone_15_task_10_final_closure_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation["valid"] is True
    assert closure["milestone_15_closed"] is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-15-final-closure-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["closure"]["closure_decision"] == CLOSURE_DECISION
    assert payload["closure"]["milestone_15_closed"] is True
    assert payload["closure"]["implementation_authorized"] is False
    assert payload["closure"]["implementation_performed"] is False


def test_task_10_is_final_closure_not_runtime_activation() -> None:
    closure = build_milestone_15_task_10_final_closure(baseline_commit="TESTBASE")

    assert closure["milestone_15_closed"] is True
    assert closure["runtime_activation_performed"] is False
    assert closure["runtime_execution_performed"] is False
    assert closure["real_submission_allowed"] is False
