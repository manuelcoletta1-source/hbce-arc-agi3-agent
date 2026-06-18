from __future__ import annotations

import json

from hbce_arc_agi3.milestone_15_implementation_block_closure_review import (
    BLOCK_REASON,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    REVIEW_DECISION,
    REVIEW_VERDICT,
    TASK_VALID,
    build_milestone_15_task_9_implementation_block_closure_review,
    validate_milestone_15_task_9_implementation_block_closure_review,
    write_milestone_15_task_9_implementation_block_closure_review_artifacts,
)


def test_task_9_closure_review_is_valid() -> None:
    review = build_milestone_15_task_9_implementation_block_closure_review(baseline_commit="TESTBASE")
    validation = validate_milestone_15_task_9_implementation_block_closure_review(review)

    assert validation["valid"] is True
    assert validation["status"] == TASK_VALID
    assert validation["issue_count"] == 0


def test_task_9_reviews_task_8_record() -> None:
    review = build_milestone_15_task_9_implementation_block_closure_review(baseline_commit="TESTBASE")

    assert review["task_8_authorization_record_confirmed"] is True
    assert review["source_task_8_final_baseline_commit"] == "115a6a9"
    assert review["source_task_8_final_signature"] == "C08A4A04B5EBA5C9"


def test_task_9_chain_is_correct() -> None:
    review = build_milestone_15_task_9_implementation_block_closure_review(baseline_commit="TESTBASE")

    assert review["previous_stage"] == PREVIOUS_STAGE
    assert review["next_stage"] == NEXT_STAGE
    assert review["source_task_7_final_baseline_commit"] == "73a7fbd"
    assert review["source_task_6_final_baseline_commit"] == "c70df02"


def test_task_9_review_decision_keeps_block_active() -> None:
    review = build_milestone_15_task_9_implementation_block_closure_review(baseline_commit="TESTBASE")

    assert review["review_verdict"] == REVIEW_VERDICT
    assert review["review_decision"] == REVIEW_DECISION
    assert review["block_reason"] == BLOCK_REASON


def test_task_9_operator_authorization_is_still_missing() -> None:
    review = build_milestone_15_task_9_implementation_block_closure_review(baseline_commit="TESTBASE")

    assert review["operator_decision_required"] is True
    assert review["operator_decision_received"] is False
    assert review["explicit_operator_authorization_required"] is True
    assert review["explicit_operator_authorization_received"] is False


def test_task_9_implementation_is_not_authorized() -> None:
    review = build_milestone_15_task_9_implementation_block_closure_review(baseline_commit="TESTBASE")

    assert review["implementation_authorization_granted"] is False
    assert review["implementation_authorized"] is False
    assert review["implementation_blocked"] is True
    assert review["implementation_performed"] is False
    assert review["implementation_patch_created"] is False
    assert review["implementation_patch_applied"] is False


def test_task_9_runtime_modification_is_blocked() -> None:
    review = build_milestone_15_task_9_implementation_block_closure_review(baseline_commit="TESTBASE")

    assert review["runtime_solver_patch_allowed"] is False
    assert review["runtime_solver_modified"] is False
    assert review["ranker_runtime_patch_allowed"] is False
    assert review["ranker_runtime_modified"] is False
    assert review["candidate_generator_patch_allowed"] is False
    assert review["candidate_generator_modified"] is False


def test_task_9_runtime_wiring_activation_and_execution_are_blocked() -> None:
    review = build_milestone_15_task_9_implementation_block_closure_review(baseline_commit="TESTBASE")

    assert review["runtime_wiring_allowed"] is False
    assert review["runtime_wiring_performed"] is False
    assert review["runtime_activation_authorized"] is False
    assert review["runtime_activation_blocked"] is True
    assert review["runtime_activation_performed"] is False
    assert review["runtime_execution_allowed"] is False
    assert review["runtime_execution_performed"] is False


def test_task_9_no_real_submission_path_is_open() -> None:
    review = build_milestone_15_task_9_implementation_block_closure_review(baseline_commit="TESTBASE")

    assert review["real_evaluation_performed"] is False
    assert review["real_submission_allowed"] is False
    assert review["ready_for_real_kaggle_submission"] is False
    assert review["manual_upload_allowed"] is False
    assert review["kaggle_authentication_allowed"] is False
    assert review["kaggle_authentication_performed"] is False
    assert review["kaggle_upload_allowed"] is False
    assert review["kaggle_upload_performed"] is False
    assert review["kaggle_submission_sent"] is False


def test_task_9_public_boundary_is_preserved() -> None:
    review = build_milestone_15_task_9_implementation_block_closure_review(baseline_commit="TESTBASE")

    assert review["external_api_dependency"] is False
    assert review["internet_during_eval"] is False
    assert review["private_core_exposure"] is False
    assert review["legal_certification"] is False
    assert review["official_score_claim_allowed"] is False
    assert review["competitive_score_claim_allowed"] is False
    assert review["public_overfit_allowed"] is False
    assert review["public_overfit_guard_required"] is True


def test_task_9_fail_closed_review_is_active() -> None:
    review = build_milestone_15_task_9_implementation_block_closure_review(baseline_commit="TESTBASE")

    assert review["fail_closed_required"] is True
    assert review["fail_closed_active"] is True
    assert review["implementation_block_closure_review_failure_count"] == 0
    assert review["implementation_block_closure_review_check_count"] == len(review["implementation_block_closure_review_checks"])
    assert review["implementation_block_closure_review_check_count"] == 22


def test_task_9_ready_for_final_closure_only() -> None:
    review = build_milestone_15_task_9_implementation_block_closure_review(baseline_commit="TESTBASE")

    assert review["ready_for_milestone_15_final_closure"] is True
    assert review["ready_for_real_kaggle_submission"] is False


def test_task_9_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_15_task_9_implementation_block_closure_review(baseline_commit="TESTBASE")
    second = build_milestone_15_task_9_implementation_block_closure_review(baseline_commit="TESTBASE")

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16


def test_task_9_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "m15_task9"
    doc_path = tmp_path / "m15_task9.md"

    review, validation, paths = write_milestone_15_task_9_implementation_block_closure_review_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation["valid"] is True
    assert review["implementation_block_closure_review_created"] is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-15-implementation-block-closure-review-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["review"]["review_decision"] == REVIEW_DECISION
    assert payload["review"]["implementation_authorization_granted"] is False
    assert payload["review"]["implementation_authorized"] is False
    assert payload["review"]["implementation_performed"] is False
